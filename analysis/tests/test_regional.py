"""Known-answer area integration, actual response replay, and fail-closed checks."""
import copy
import io
import json
import math
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from expedition73 import regional
from expedition73.__main__ import main
from expedition73.power import PilotError, loads

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "examples/a-window-2024"
STAMP = "2026-10-16T08:19:19+00:00"


class RegionalTests(unittest.TestCase):
    def setUp(self):
        self.config = loads((RUN / "request.json").read_bytes())
        self.raw = (RUN / "response.json").read_bytes()
        self.provider = loads(self.raw)

    def result(self, data=None):
        return regional.normalize(self.raw if data is None else json.dumps(data).encode(), self.config, STAMP)

    def constant(self, value):
        data = copy.deepcopy(self.provider)
        for feature in data["features"]:
            feature["properties"]["parameter"]["T2M"] = {
                k: value for k in feature["properties"]["parameter"]["T2M"]}
        return data

    def test_real_replay_matches_saved_result(self):
        self.assertEqual(self.result(), regional.validate_run(RUN))
        self.assertEqual(self.result()["spatial_support"]["cell_count"], 56)

    def test_halo_and_edges_cover_entire_window(self):
        self.assertEqual(regional.validate_config(self.config), [-113.3125, 35.75, -108.6875, 39.25])
        result = self.result()
        cells = result["module_details"]["cells"]
        self.assertEqual(cells[0]["intersection_bbox"], [-113, 36, -112.8125, 36.25])
        self.assertEqual(cells[-1]["intersection_bbox"], [-109.0625, 38.75, -109, 39])
        self.assertAlmostEqual(math.fsum(c["area_m2"] for c in cells) / result["spatial_support"]["window_area_m2"], 1, places=12)

    def test_independent_january_reference_uses_explicit_row_widths(self):
        # Independent 7-row quadrature: edge widths 3/64 and 1/64;
        # six interior widths 10/64. No production area/grid helpers.
        by_lat = {}
        for feature in self.provider["features"]:
            lon, lat = feature["geometry"]["coordinates"][:2]
            by_lat.setdefault(lat, {})[lon] = feature["properties"]["parameter"]["T2M"]["202401"]
        weights = [3, 10, 10, 10, 10, 10, 10, 1]
        numerator, denominator = 0, 0
        for lat, values in sorted(by_lat.items()):
            lo, hi = max(36, lat - .25), min(39, lat + .25)
            band = math.sin(math.radians(hi)) - math.sin(math.radians(lo))
            row_mean = sum(w * values[lon] for w, lon in zip(weights, sorted(values), strict=True)) / 64
            numerator += band * row_mean
            denominator += band
        self.assertAlmostEqual(self.result()["series"][0]["value"], numerator / denominator, places=12)

    def test_known_hemisphere_area_on_declared_sphere(self):
        expected = 2 * math.pi * 6_371_008.8 ** 2
        self.assertAlmostEqual(regional.spherical_area([-90, -90, 90, 90]) / expected, 1, places=14)

    def test_constant_field_and_true_zero_remain_constant(self):
        for value in (0, -7.25):
            result = self.result(self.constant(value))
            for row in result["series"]:
                self.assertAlmostEqual(row["value"], value, places=12)
                self.assertEqual(row["valid_area_fraction"], 1)

    def test_missing_cell_month_nulls_mean_and_reports_area(self):
        for fill in (True, False):
            data = self.constant(10)
            values = data["features"][0]["properties"]["parameter"]["T2M"]
            if fill:
                values["202401"] = -999
            else:
                del values["202401"]
            result = self.result(data)
            row = result["series"][0]
            self.assertIsNone(row["value"])
            self.assertEqual(row["status"], "incomplete")
            self.assertEqual(row["valid_cells"], 55)
            self.assertGreater(row["valid_area_fraction"], 0)
            self.assertLess(row["valid_area_fraction"], 1)
            self.assertEqual(result["quality"]["complete_months"], 11)
            self.assertEqual(result["series"][1]["value"], 10)

    def test_all_missing_returns_null_and_zero_area(self):
        row = self.result(self.constant(-999))["series"][0]
        self.assertIsNone(row["value"])
        self.assertEqual((row["valid_cells"], row["valid_area_fraction"]), (0, 0))

    def test_annual_summary_never_enters_monthly_mean(self):
        data = self.constant(5)
        for feature in data["features"]:
            feature["properties"]["parameter"]["T2M"]["202413"] = 10000
        result = self.result(data)
        self.assertEqual(len(result["series"]), 12)
        self.assertTrue(all(abs(r["value"] - 5) < 1e-12 for r in result["series"]))
        self.assertEqual(result["module_details"]["cells"][0]["provider_annual_summary"], {"2024": 10000})

    def test_order_does_not_change_result(self):
        data = copy.deepcopy(self.provider)
        data["features"].reverse()
        self.assertEqual(self.result()["series"], self.result(data)["series"])
        self.assertEqual(self.result()["module_details"]["cells"], self.result(data)["module_details"]["cells"])

    def test_missing_or_duplicate_geographic_cell_is_rejected(self):
        for duplicate in (True, False):
            data = copy.deepcopy(self.provider)
            if duplicate:
                data["features"].append(copy.deepcopy(data["features"][0]))
            else:
                data["features"].pop(0)
            with self.assertRaises(PilotError):
                self.result(data)

    def test_unsupported_grid_source_unit_and_coordinates_fail(self):
        for variant in ("grid", "source", "unit", "outside", "type", "service"):
            data = copy.deepcopy(self.provider)
            if variant == "grid": data["features"][0]["geometry"]["coordinates"][0] += .01
            if variant == "source": data["header"]["sources"] = ["OTHER"]
            if variant == "unit": data["parameters"]["T2M"]["units"] = "K"
            if variant == "outside": data["features"][0]["geometry"]["coordinates"][0] = 0
            if variant == "type": data["type"] = "Feature"
            if variant == "service": data["header"]["api"]["name"] = "OTHER"
            with self.subTest(variant=variant), self.assertRaises(PilotError): self.result(data)

    def test_invalid_or_unsupported_config_fails_before_network(self):
        for key, value in [("mask", "land"), ("candidate_bbox", [-156,68,-150,70]),
                           ("candidate_bbox", [179,0,180,1]), ("candidate_bbox", [-113,39,-109,36]),
                           ("start_year", 2001), ("end_year", 2024.0)]:
            config = copy.deepcopy(self.config); config[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(PilotError): regional.request_url(config)

    def test_replay_rejects_tampered_result_and_raw(self):
        with tempfile.TemporaryDirectory() as path:
            directory = Path(path)
            for name in ("request.json", "response.json", "result.json"):
                (directory / name).write_bytes((RUN / name).read_bytes())
            result = loads((RUN / "result.json").read_bytes())
            result["series"][0]["value"] += 1
            (directory / "result.json").write_text(json.dumps(result), encoding="utf-8")
            with self.assertRaises(PilotError): regional.validate_run(directory)
            (directory / "result.json").write_bytes((RUN / "result.json").read_bytes())
            (directory / "response.json").write_bytes(self.raw + b" ")
            with self.assertRaises(PilotError): regional.validate_run(directory)

    def test_replay_numeric_tolerance_is_narrow_and_metadata_exact(self):
        self.assertTrue(regional._same_result({"value": 26.5}, {"value": 26.5 + 1e-13}))
        self.assertFalse(regional._same_result({"value": 26.5}, {"value": 26.51}))
        self.assertFalse(regional._same_result({"hash": "abc"}, {"hash": "abd"}))
        self.assertFalse(regional._same_result([1, 2], [2, 1]))

    def test_cli_offline_replay_and_no_overwrite(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(["validate-window", str(RUN)]), 0)
        with patch("expedition73.regional.fetch") as network, redirect_stderr(io.StringIO()):
            self.assertEqual(main(["fetch-power-window", "--config", str(RUN / "request.json"), "--output-dir", str(RUN)]), 1)
            network.assert_not_called()

    def test_http_error_is_actionable(self):
        with patch("expedition73.regional.urlopen", side_effect=HTTPError("url",429,"rate limit",{},None)):
            with self.assertRaisesRegex(PilotError, "HTTP 429"): regional.fetch(self.config)


if __name__ == "__main__":
    unittest.main()
