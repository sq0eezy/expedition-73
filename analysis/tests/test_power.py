"""Offline provider replay and contract boundary checks. No calls to NASA in CI."""
import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from expedition73.__main__ import main
from expedition73.power import (PilotError, compatibility, fetch, loads, normalize,
                                request_url, validate_config, validate_result)

ROOT = Path(__file__).resolve().parents[1]
CAPTURED_AT = "2026-10-16T00:00:00+00:00"


class PowerTests(unittest.TestCase):
    def setUp(self):
        self.config = loads((ROOT / "examples/a-point-2024.config.json").read_bytes())
        self.raw = (ROOT / "examples/a-point-2024/response.json").read_bytes()
        self.provider = loads(self.raw)

    def result(self, data=None):
        return normalize(self.raw if data is None else json.dumps(data).encode(), self.config, CAPTURED_AT)

    def test_real_response_is_twelve_months_and_preserves_annual_summary(self):
        result = self.result()
        self.assertEqual(len(result["series"]), 12)
        self.assertEqual(result["series"][0], {"date": "2024-01", "value": 0.6, "status": "valid"})
        self.assertEqual(result["series"][-1]["value"], 2.39)
        self.assertEqual(result["module_details"]["provider_annual_summary"], {"2024": 13.57})
        self.assertEqual(result["spatial_support"]["kind"], "point_sample")
        self.assertIn("POINT_SAMPLE_NOT_REGION_AVERAGE", result["quality"]["warnings"])

    def test_missing_and_fill_are_distinct_nulls_but_zero_is_valid(self):
        data = self.provider
        values = data["properties"]["parameter"]["T2M"]
        values["202401"] = 0
        values["202402"] = data["header"]["fill_value"]
        del values["202403"]
        result = self.result(data)
        self.assertEqual(result["quality"]["valid_months"], 10)
        self.assertEqual(result["series"][0]["value"], 0)
        self.assertEqual(result["series"][1], {"date": "2024-02", "value": None, "status": "provider_fill"})
        self.assertEqual(result["series"][2]["status"], "not_returned")

    def test_response_order_does_not_change_chronology(self):
        data = self.provider
        values = data["properties"]["parameter"]["T2M"]
        data["properties"]["parameter"]["T2M"] = dict(reversed(list(values.items())))
        self.assertEqual(self.result()["series"], self.result(data)["series"])

    def test_other_unit_or_temperature_definition_is_rejected(self):
        for key, value in [("units", "K"), ("longname", "Surface Skin Temperature")]:
            with self.subTest(key=key):
                data = copy.deepcopy(self.provider)
                data["parameters"]["T2M"][key] = value
                with self.assertRaises(PilotError):
                    self.result(data)

    def test_unexpected_or_out_of_range_periods_fail(self):
        for key in ["202414", "202301", "2024Q1"]:
            with self.subTest(key=key):
                data = copy.deepcopy(self.provider)
                data["properties"]["parameter"]["T2M"][key] = 10
                with self.assertRaises(PilotError):
                    self.result(data)

    def test_mismatched_response_dates_are_rejected(self):
        self.provider["header"]["start"] = "20230101"
        with self.assertRaises(PilotError): self.result(self.provider)

    def test_wrong_point_or_regional_response_is_rejected(self):
        data = copy.deepcopy(self.provider)
        data["geometry"]["coordinates"][0] = -112
        with self.assertRaises(PilotError): self.result(data)
        with self.assertRaises(PilotError): self.result({"type": "FeatureCollection", "features": []})

    def test_non_numeric_boolean_and_infinite_values_fail(self):
        for value in [True, "12.0", float("inf"), float("nan")]:
            with self.subTest(value=value):
                data = copy.deepcopy(self.provider)
                data["properties"]["parameter"]["T2M"]["202401"] = value
                with self.assertRaises(PilotError): self.result(data)

    def test_duplicate_json_keys_and_numeric_overflow_fail(self):
        for raw in [b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":1e999}', b'<html>error</html>']:
            with self.subTest(raw=raw):
                with self.assertRaises(PilotError): loads(raw)

    def test_candidate_window_and_year_validation(self):
        for change in [{"point": {"longitude": 0, "latitude": 0}},
                       {"candidate_bbox": [-109, 36, -113, 39]},
                       {"start_year": 2025, "end_year": 2024},
                       {"selection_status": "accepted"}, {"end_year": 9999}]:
            with self.subTest(change=change):
                with self.assertRaises(PilotError): validate_config({**self.config, **change})

    def test_request_uses_point_api_and_only_t2m(self):
        url = request_url(self.config)
        self.assertIn('/monthly/point?', url)
        self.assertIn('parameters=T2M&', url)
        self.assertNotIn('T2M_MAX', url)

    def test_malformed_provider_structure_fails(self):
        del self.provider["parameters"]
        with self.assertRaises(PilotError): self.result(self.provider)

    def test_duplicate_or_reordered_output_months_fail(self):
        for change in ['duplicate', 'reverse']:
            result = self.result()
            if change == 'duplicate': result["series"][1] = copy.deepcopy(result["series"][0])
            else: result["series"].reverse()
            with self.assertRaises(PilotError): validate_result(result)

    def test_inconsistent_counts_and_null_status_fail(self):
        result = self.result()
        result["quality"]["valid_months"] = 11
        with self.assertRaises(PilotError): validate_result(result)
        result = self.result()
        result["series"][0]["value"] = None
        with self.assertRaises(PilotError): validate_result(result)

    def test_output_cannot_claim_regional_support_or_include_uncomputed_trend(self):
        result = self.result()
        result["spatial_support"]["kind"] = 'regional_mean'
        with self.assertRaises(PilotError): validate_result(result)
        result = self.result()
        result['trend'] = {'p_value': 0.01}
        with self.assertRaises(PilotError): validate_result(result)

    def test_alignment_never_authorizes_inference(self):
        report = compatibility(self.result(), self.result())
        self.assertEqual(report['status'], 'aligned_point_series')
        self.assertEqual(report['paired_valid_months'], 12)
        self.assertFalse(report['inference_allowed'])

    def test_different_dates_have_no_false_paired_months(self):
        left = self.result()
        data = copy.deepcopy(self.provider)
        data['header']['start'], data['header']['end'] = '20230101', '20231231'
        data['properties']['parameter']['T2M'] = {
            key.replace('2024', '2023'): value for key, value in data['properties']['parameter']['T2M'].items()}
        config = {**self.config, 'start_year': 2023, 'end_year': 2023}
        right = normalize(json.dumps(data).encode(), config, CAPTURED_AT)
        report = compatibility(left, right)
        self.assertEqual(report['status'], 'incompatible')
        self.assertEqual(report['paired_valid_months'], 0)

    def test_provider_api_or_module_version_mismatch_is_not_silently_aligned(self):
        right = self.result()
        right['provenance']['api_version'] = 'v9.0.0'
        right['module_details']['provider_header']['api']['version'] = 'v9.0.0'
        self.assertEqual(compatibility(self.result(), right)['status'], 'incompatible')

    def test_all_missing_data_is_not_comparable(self):
        data = self.provider
        data['properties']['parameter']['T2M'] = {}
        report = compatibility(self.result(data), self.result())
        self.assertEqual(report['status'], 'incompatible')
        self.assertEqual(report['paired_valid_months'], 0)

    def test_cli_will_not_overwrite_existing_run_or_make_a_network_call(self):
        with tempfile.TemporaryDirectory() as output, patch('expedition73.__main__.fetch') as network, redirect_stderr(io.StringIO()):
            code = main(['fetch-power-point', '--config', str(ROOT/'examples/a-point-2024.config.json'), '--output-dir', output])
            self.assertEqual(code, 1)
            network.assert_not_called()

    def test_http_error_is_actionable_without_fake_output(self):
        with patch('expedition73.power.urlopen', side_effect=HTTPError('url', 429, 'limit', {}, None)):
            with self.assertRaisesRegex(PilotError, 'HTTP 429'): fetch(self.config)

    def test_point_or_time_metadata_cannot_be_relabelled(self):
        result = self.result()
        result['spatial_support']['longitude'] = -112
        with self.assertRaises(PilotError): validate_result(result)
        result = self.result()
        result['provenance']['api_version'] = 'unrecorded-version'
        with self.assertRaises(PilotError): validate_result(result)

    def test_saved_real_example_replays_exactly(self):
        saved = loads((ROOT/'examples/a-point-2024/result.json').read_bytes())
        self.assertEqual(normalize(self.raw, self.config, saved['provenance']['retrieved_at']), saved)

    def test_integer_coordinate_is_canonically_equivalent(self):
        config = copy.deepcopy(self.config)
        config['point']['longitude'] = -111
        self.assertEqual(request_url(config), request_url(self.config))
        normalize(self.raw, config, CAPTURED_AT)

    def test_float_year_is_rejected_before_network(self):
        with self.assertRaises(PilotError):
            validate_config({**self.config, 'start_year': 2024.0})

    def test_capture_time_requires_a_real_date_and_timezone(self):
        for stamp in ['2026-02-30T12:00:00+00:00', '2026-10-16T12:00:00', 'not-a-date']:
            with self.subTest(stamp=stamp):
                result = self.result()
                result['provenance']['retrieved_at'] = stamp
                with self.assertRaises(PilotError): validate_result(result)

    def test_saved_real_b_example_replays_and_aligns(self):
        config_b = loads((ROOT / "examples/b-point-2024.config.json").read_bytes())
        raw_b = (ROOT / "examples/b-point-2024/response.json").read_bytes()
        saved_b = loads((ROOT / "examples/b-point-2024/result.json").read_bytes())
        self.assertEqual(normalize(raw_b, config_b, saved_b["provenance"]["retrieved_at"]), saved_b)
        saved_a = loads((ROOT / "examples/a-point-2024/result.json").read_bytes())
        report = compatibility(saved_a, saved_b)
        self.assertEqual(report["status"], "aligned_point_series")
        self.assertEqual(report["paired_valid_months"], 12)


if __name__ == '__main__':
    unittest.main()
