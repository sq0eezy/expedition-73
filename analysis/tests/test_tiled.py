"""Offline real-tile replay, seam invariance and failure boundaries."""
import copy
import io
import json
import math
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from expedition73 import regional, tiled
from expedition73.__main__ import main
from expedition73.power import PilotError, loads

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "examples/b-window-2024"


class TiledTests(unittest.TestCase):
    def setUp(self):
        self.config = loads((RUN / "request.json").read_bytes())
        self.manifest = loads((RUN / "manifest.json").read_bytes())
        self.parts = [(RUN / (t["id"] + ".json")).read_bytes() for t in tiled.plan(self.config)]

    def result(self, parts=None, config=None, manifest=None):
        return tiled.normalize(self.parts if parts is None else parts,
                               self.config if config is None else config,
                               self.manifest if manifest is None else manifest)

    def updated(self, parts):
        manifest = copy.deepcopy(self.manifest)
        for tile, raw, entry in zip(tiled.plan(self.config), parts, manifest["tiles"], strict=True):
            entry.update(tiled.manifest_entry(tile, raw, entry["retrieved_at"]))
        return manifest

    def test_real_b_replay_deduplicates_five_cells_without_changing_extent(self):
        result = tiled.validate_run(RUN)
        self.assertTrue(regional._same_result(result, self.result()))
        self.assertEqual(result["region"]["candidate_bbox"], [-156, 68, -150, 70])
        self.assertEqual(result["schema_version"], "0.2.0")
        self.assertEqual(result["spatial_support"]["cell_count"], 55)
        self.assertEqual(result["module_details"]["access"]["duplicate_cells_removed"], 5)
        self.assertEqual(result["quality"]["complete_months"], 12)
        self.assertTrue(all(row["valid_cells"] == 55 and row["valid_area_fraction"] == 1 for row in result["series"]))

    def test_independent_january_rectangle_integral(self):
        # Eleven column widths are [1,10,...,10,5]/96 of the six-degree window.
        # Five latitude bands, with half-height northern/southern edges.
        cells = {}
        for raw in self.parts:
            for feature in loads(raw)["features"]:
                lon, lat = feature["geometry"]["coordinates"][:2]
                cells[(lon, lat)] = feature["properties"]["parameter"]["T2M"]["202401"]
        numerator, denominator = 0, 0
        for lat in [68, 68.5, 69, 69.5, 70]:
            band = math.sin(math.radians(min(70, lat + .25))) - math.sin(math.radians(max(68, lat - .25)))
            row = sorted((lon, value) for (lon, y), value in cells.items() if y == lat)
            self.assertEqual(len(row), 11)
            mean = sum(w * item[1] for w, item in zip([1] + [10] * 9 + [5], row, strict=True)) / 96
            numerator += band * mean
            denominator += band
        self.assertAlmostEqual(self.result()["series"][0]["value"], numerator / denominator, places=12)

    def test_two_axis_plan_has_no_gap_and_bounded_requests(self):
        config = copy.deepcopy(self.config);config["candidate_bbox"] = [-156, 64, -150, 70]
        plan = tiled.plan(config)
        self.assertEqual(len(plan), 4)
        area_degrees = 0
        for tile in plan:
            w, s, e, n = tile["config"]["candidate_bbox"]
            area_degrees += (e-w)*(n-s)
            a,b,c,d = tile["request_bbox"]
            self.assertLess(c-a,5);self.assertLess(d-b,5)
        self.assertEqual(area_degrees,36)
        self.assertEqual(plan[0]["config"]["candidate_bbox"][2],plan[1]["config"]["candidate_bbox"][0])
        self.assertEqual(plan[0]["config"]["candidate_bbox"][3],plan[2]["config"]["candidate_bbox"][1])

    def test_more_tiles_and_different_seams_leave_mean_and_weights_unchanged(self):
        by_coordinate = {}
        first = loads(self.parts[0])
        for raw in self.parts:
            for feature in loads(raw)["features"]:
                by_coordinate[tuple(feature["geometry"]["coordinates"][:2])] = feature
        with patch("expedition73.tiled.BODY_DEGREES", 2):
            parts, entries = [], []
            for tile in tiled.plan(self.config):
                w,s,e,n = tile["request_bbox"]
                data = copy.deepcopy(first)
                data["features"] = [f for (x,y),f in by_coordinate.items() if w<=x<=e and s<=y<=n]
                raw = json.dumps(data).encode();parts.append(raw)
                entries.append(tiled.manifest_entry(tile,raw,self.manifest["tiles"][0]["retrieved_at"]))
            result = self.result(parts=parts,manifest={"schema_version":"0.1.0","format":"power_tiled_run","tiles":entries})
        self.assertEqual(result["series"], self.result()["series"])
        self.assertEqual(result["module_details"]["cells"], self.result()["module_details"]["cells"])

    def test_four_tile_two_axis_constant_field_is_integrated_once(self):
        config=copy.deepcopy(self.config);config["candidate_bbox"]=[-156,64,-150,70]
        template=loads(self.parts[0]);all_features=[]
        for lon,lat in regional.expected_cells(config["candidate_bbox"]):
            all_features.append({"type":"Feature","geometry":{"type":"Point","coordinates":[lon,lat,0]},
                                 "properties":{"parameter":{"T2M":{f"2024{m:02d}":7.5 for m in range(1,14)}}}})
        parts,entries=[],[]
        for tile in tiled.plan(config):
            w,s,e,n=tile["request_bbox"];data=copy.deepcopy(template)
            data["features"]=[f for f in all_features if w<=f["geometry"]["coordinates"][0]<=e and s<=f["geometry"]["coordinates"][1]<=n]
            raw=json.dumps(data).encode();parts.append(raw)
            entries.append(tiled.manifest_entry(tile,raw,self.manifest["tiles"][0]["retrieved_at"]))
        result=self.result(parts=parts,config=config,manifest={"schema_version":"0.1.0","format":"power_tiled_run","tiles":entries})
        self.assertEqual(result["module_details"]["access"]["tile_count"],4)
        self.assertGreater(result["module_details"]["access"]["duplicate_cells_removed"],0)
        self.assertEqual(result["spatial_support"]["cell_count"],len(all_features))
        self.assertTrue(all(abs(r["value"]-7.5)<1e-12 and r["valid_area_fraction"]==1 for r in result["series"]))

    def test_single_tile_reproduces_old_a_values_and_keeps_old_profile(self):
        run = ROOT / "examples/a-window-2024"
        config = loads((run / "request.json").read_bytes());raw=(run / "response.json").read_bytes()
        tile = tiled.plan(config)[0]
        manifest = {"schema_version":"0.1.0","format":"power_tiled_run",
                    "tiles":[tiled.manifest_entry(tile,raw,self.manifest["tiles"][0]["retrieved_at"])]}
        result = self.result(parts=[raw],config=config,manifest=manifest)
        old = loads((run / "result.json").read_bytes())
        self.assertEqual(result["series"],old["series"])
        self.assertEqual(result["method"],old["method"])
        self.assertEqual(old["schema_version"],"0.1.0")

    def test_conflicting_overlap_value_elevation_or_missing_month_is_rejected(self):
        left_coords={tuple(f["geometry"]["coordinates"][:2]) for f in loads(self.parts[0])["features"]}
        for variant in ("value","elevation","missing"):
            data=loads(self.parts[1])
            shared=next(f for f in data["features"] if tuple(f["geometry"]["coordinates"][:2]) in left_coords)
            values=shared["properties"]["parameter"]["T2M"]
            if variant=="value":values["202401"]+=1
            if variant=="elevation":shared["geometry"]["coordinates"][2]+=1
            if variant=="missing":values.pop("202401")
            parts=[self.parts[0],json.dumps(data).encode()]
            with self.subTest(variant=variant),self.assertRaisesRegex(PilotError,"Overlapping cell"):
                self.result(parts=parts,manifest=self.updated(parts))

    def test_source_metadata_changes_between_tiles_fail(self):
        for key, value in [("time_standard","UTC"),("fill_value",-888),("api",{"version":"v2.11.0","name":"POWER Monthly and Annual API"})]:
            data=loads(self.parts[1]);data["header"][key]=value
            parts=[self.parts[0],json.dumps(data).encode()]
            with self.subTest(key=key),self.assertRaises(PilotError):self.result(parts=parts,manifest=self.updated(parts))

    def test_missing_tile_cell_and_duplicate_inside_tile_fail(self):
        for duplicate in (False,True):
            data=loads(self.parts[0])
            if duplicate:data["features"].append(copy.deepcopy(data["features"][0]))
            else:data["features"].pop(0)
            parts=[json.dumps(data).encode(),self.parts[1]]
            with self.subTest(duplicate=duplicate),self.assertRaises(PilotError):self.result(parts=parts,manifest=self.updated(parts))

    def test_missing_extra_swapped_or_corrupted_parts_fail(self):
        for parts in (self.parts[:1],self.parts+[self.parts[0]],list(reversed(self.parts)),[self.parts[0]+b" ",self.parts[1]]):
            with self.assertRaises(PilotError):self.result(parts=parts)

    def test_path_url_timestamp_and_manifest_id_tampering_fail(self):
        for key,value in [("filename","../elsewhere.json"),("id","tile-002"),("request_url","https://example.com"),("retrieved_at","2026-02-30T00:00:00Z")]:
            manifest=copy.deepcopy(self.manifest);manifest["tiles"][0][key]=value
            with self.subTest(key=key),self.assertRaises(PilotError):self.result(manifest=manifest)

    def test_unsupported_size_period_mask_poles_and_dateline_fail_before_network(self):
        for key,value in [("candidate_bbox",[-160,20,-100,70]),("candidate_bbox",[179,0,180,1]),("candidate_bbox",[0,89,1,90]),("start_year",2001),("mask","land")]:
            config=copy.deepcopy(self.config);config[key]=value
            with self.subTest(key=key),patch("expedition73.regional.fetch") as fetch,self.assertRaises(PilotError):
                tiled.fetch(config)
            fetch.assert_not_called()

    def test_missing_cell_value_retains_month_null_and_reports_fraction(self):
        data=loads(self.parts[0]);data["features"][0]["properties"]["parameter"]["T2M"]["202401"]=-999
        parts=[json.dumps(data).encode(),self.parts[1]]
        result=self.result(parts=parts,manifest=self.updated(parts))
        self.assertIsNone(result["series"][0]["value"])
        self.assertEqual(result["series"][0]["valid_cells"],54)
        self.assertLess(result["series"][0]["valid_area_fraction"],1)

    def test_cli_fetch_saves_and_replays_all_raw_files_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)/"run"
            with patch("expedition73.tiled.fetch",return_value=(self.parts,self.manifest)),redirect_stdout(io.StringIO()):
                self.assertEqual(main(["fetch-power-tiled-window","--config",str(RUN/"request.json"),"--output-dir",str(directory)]),0)
                self.assertEqual(main(["validate-tiled-window",str(directory)]),0)
            self.assertEqual((directory/"tile-001.json").read_bytes(),self.parts[0])
            result=loads((directory/"result.json").read_bytes());result["series"][0]["value"]+=1
            (directory/"result.json").write_text(json.dumps(result),encoding="utf-8")
            with self.assertRaises(PilotError):tiled.validate_run(directory)

    def test_failed_tile_never_writes_a_partial_run_and_existing_directory_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)/"failed"
            with patch("expedition73.regional.fetch",side_effect=[(self.parts[0],self.manifest["tiles"][0]["retrieved_at"]),PilotError("HTTP 503")]),redirect_stderr(io.StringIO()):
                self.assertEqual(main(["fetch-power-tiled-window","--config",str(RUN/"request.json"),"--output-dir",str(directory)]),1)
            self.assertFalse(directory.exists())
            with patch("expedition73.tiled.fetch") as fetch,redirect_stderr(io.StringIO()):
                self.assertEqual(main(["fetch-power-tiled-window","--config",str(RUN/"request.json"),"--output-dir",tmp]),1)
            fetch.assert_not_called()


if __name__=="__main__":unittest.main()
