"""Synthetic fraction math only. No NASA mask measurements are claimed."""
import copy
import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from expedition73 import masking
from expedition73.__main__ import main
from expedition73.power import PilotError, loads

ROOT = Path(__file__).resolve().parents[1]


class MaskingTests(unittest.TestCase):
    def setUp(self):
        self.config = loads((ROOT / "examples/a-window-2024/request.json").read_bytes())
        self.window = loads((ROOT / "examples/a-window-2024/result.json").read_bytes())
        self.mask = {"schema_version": "0.1.0", "output_type": "source_cell_surface_fractions",
                     "data_origin": "synthetic_fixture", "grid_id": "merra2_output_0.625x0.5",
                     "spatial_support": "whole_source_cell", "unit": "1",
                     "source": {"dataset": "synthetic_fixture", "version": "test-1",
                                "uri": "urn:expedition73:synthetic-fixture", "retrieved_at": "2026-10-17T00:00:00Z",
                                "response_sha256": hashlib.sha256(b"synthetic unit test only").hexdigest()},
                     "cells": [{"longitude": c["longitude"], "latitude": c["latitude"],
                                "fractions": {"FRLAND": 1, "FRLANDICE": 0, "FRLAKE": 0, "FROCEAN": 0}}
                               for c in self.window["module_details"]["cells"]]}

    def preview(self, components=None):
        return masking.preview_series(self.window, self.mask, self.config,
                                      ["FRLAND"] if components is None else components, allow_synthetic=True)

    def test_plans_match_a_and_b_saved_native_coordinates_and_indices(self):
        for name, count, xs, ys in [("a",56,[107,114],[252,258]),("b",55,[38,48],[316,320])]:
            config=loads((ROOT / f"examples/{name}-window-2024/request.json").read_bytes())
            plan=masking.request_plan(config)
            self.assertEqual(plan["expected_cells"],count)
            self.assertEqual(plan["zero_based_inclusive_indices"],{"longitude":xs,"latitude":ys})
            self.assertFalse(plan["source_candidate"]["access_verified"])
            self.assertEqual(plan["status"],"plan_only_no_provider_fractions")
            self.assertEqual(plan,loads((ROOT / f"examples/{name}-surface-mask-plan.json").read_bytes()))

    def test_full_land_synthetic_field_recovers_unmasked_values(self):
        result=self.preview()
        self.assertEqual(result["data_origin"],"synthetic_fixture")
        self.assertEqual(result["output_type"],"candidate_surface_weight_preview")
        self.assertTrue(all(abs(a["value"]-b["value"])<1e-12 for a,b in zip(result["series"],self.window["series"])))
        self.assertAlmostEqual(result["spatial_support"]["effective_fraction_of_window"],1,places=12)

    def test_known_two_cell_fraction_weighted_mean(self):
        # Adjacent interior columns on the same latitude have equal clip area.
        for cell in self.mask["cells"]:
            cell["fractions"]={"FRLAND":0,"FRLANDICE":0,"FRLAKE":1,"FROCEAN":0}
        self.mask["cells"][1]["fractions"].update(FRLAND=.75,FRLAKE=.25)
        self.mask["cells"][2]["fractions"].update(FRLAND=.25,FRLAKE=.75)
        for value,cell in [(10,self.window["module_details"]["cells"][1]),(20,self.window["module_details"]["cells"][2])]:
            for row in cell["series"]:row["value"]=value
        self.assertAlmostEqual(self.preview()["series"][0]["value"],12.5,places=12)
        self.assertEqual(self.preview()["series"][0]["active_cells"],2)

    def test_ice_policy_must_be_explicit_and_changes_support(self):
        for cell in self.mask["cells"]:cell["fractions"].update(FRLAND=.25,FRLANDICE=.75)
        land=self.preview(["FRLAND"]);both=self.preview(["FRLAND","FRLANDICE"])
        self.assertAlmostEqual(land["spatial_support"]["effective_area_m2"]*4,both["spatial_support"]["effective_area_m2"],places=4)
        for components in ([],["FRLAND","FRLAND"],["FRLAKE"]):
            with self.assertRaises(PilotError):self.preview(components)

    def test_positive_weight_missing_value_nulls_month_but_zero_weight_does_not(self):
        self.window["module_details"]["cells"][0]["series"][0]["value"]=None
        self.assertIsNone(self.preview()["series"][0]["value"])
        self.mask["cells"][0]["fractions"].update(FRLAND=0,FRLAKE=1)
        row=self.preview()["series"][0]
        self.assertIsNotNone(row["value"])
        self.assertEqual(row["valid_effective_area_fraction"],1)
        self.assertEqual(row["active_cells"],55)

    def test_missing_month_at_all_land_cells_has_zero_coverage_and_null(self):
        for cell in self.window["module_details"]["cells"]:cell["series"][0]["value"]=None
        row=self.preview()["series"][0]
        self.assertIsNone(row["value"]);self.assertEqual(row["valid_effective_area_fraction"],0)

    def test_real_zero_temperature_is_valid(self):
        for cell in self.window["module_details"]["cells"]:
            for row in cell["series"]:row["value"]=0
        self.assertEqual(self.preview()["series"][0]["value"],0)
        self.assertEqual(self.preview()["series"][0]["status"],"complete")

    def test_missing_extra_duplicate_and_shifted_mask_coordinates_fail(self):
        original=copy.deepcopy(self.mask)
        for variant in ("missing","extra","duplicate","shifted"):
            self.mask=copy.deepcopy(original)
            if variant=="missing":self.mask["cells"].pop()
            if variant=="extra":self.mask["cells"].append({**self.mask["cells"][0],"longitude":0})
            if variant=="duplicate":self.mask["cells"].append(copy.deepcopy(self.mask["cells"][0]))
            if variant=="shifted":self.mask["cells"][0]["longitude"]+=.001
            with self.subTest(variant=variant),self.assertRaises(PilotError):self.preview()

    def test_invalid_fraction_values_sum_units_and_grid_fail(self):
        original=copy.deepcopy(self.mask)
        for variant in ("negative","overone","fill","null","boolean","sum","unit","grid","ice_rounding"):
            self.mask=copy.deepcopy(original);frac=self.mask["cells"][0]["fractions"]
            if variant=="negative":frac["FRLAND"]=-.1
            if variant=="overone":frac["FRLAND"]=1.1
            if variant=="fill":frac["FRLAND"]=-999
            if variant=="null":frac["FRLAND"]=None
            if variant=="boolean":frac["FRLAND"]=True
            if variant=="sum":frac["FRLAND"]=.2
            if variant=="unit":self.mask["unit"]="percent"
            if variant=="grid":self.mask["grid_id"]="resampled"
            if variant=="ice_rounding":frac.update(FRLAND=.5,FRLANDICE=.5000001)
            with self.subTest(variant=variant),self.assertRaises(PilotError):self.preview(["FRLAND","FRLANDICE"])

    def test_zero_effective_area_is_rejected(self):
        for cell in self.mask["cells"]:cell["fractions"].update(FRLAND=0,FROCEAN=1)
        with self.assertRaisesRegex(PilotError,"zero effective area"):self.preview()

    def test_synthetic_data_is_rejected_without_explicit_opt_in(self):
        with self.assertRaisesRegex(PilotError,"Synthetic fractions"):
            masking.preview_series(self.window,self.mask,self.config,["FRLAND"])

    def test_source_label_and_timestamp_are_checked(self):
        original=copy.deepcopy(self.mask)
        for key,value in [("uri","https://example.com"),("retrieved_at","2026-02-30T00:00:00Z"),("dataset","M2C0NXASM")]:
            self.mask=copy.deepcopy(original);self.mask["source"][key]=value
            with self.subTest(key=key),self.assertRaises(PilotError):self.preview()

    def test_window_identity_cannot_be_relabelled(self):
        self.config["candidate_window_version"]="changed"
        with self.assertRaises(PilotError):self.preview()

    def test_cli_plan_is_offline_and_preview_requires_opt_in(self):
        with redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(["plan-surface-mask","--config",str(ROOT/"examples/b-window-2024.config.json")]),0)
        self.assertEqual(json.loads(output.getvalue())["expected_cells"],55)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"synthetic.json";path.write_text(json.dumps(self.mask),encoding="utf-8")
            args=["preview-surface-mask","--run",str(ROOT/"examples/a-window-2024"),"--mask",str(path),"--components","FRLAND"]
            with redirect_stderr(io.StringIO()):self.assertEqual(main(args),1)
            with redirect_stdout(io.StringIO()) as output:self.assertEqual(main(args+["--allow-synthetic"]),0)
            result=json.loads(output.getvalue())
            self.assertEqual(result["provenance"]["mask_input_sha256"],hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(result["data_origin"],"synthetic_fixture")


if __name__=="__main__":unittest.main()
