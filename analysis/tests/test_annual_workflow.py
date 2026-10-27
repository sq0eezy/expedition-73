"""Real source identity, dependency blocking and offline annual calculation."""
import copy
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from expedition73 import annual_workflow, annual_weighting, earthdata, history, regional, workflow_trace
from expedition73.__main__ import main
from expedition73.power import PilotError, loads
from expedition73.workflow import Operation, compare_snapshot, execute, validate_artifact

ROOT = Path(__file__).resolve().parents[1]


class AnnualWorkflowTests(unittest.TestCase):
    def short(self):
        return ROOT / "examples/a-history-2023-2024"

    def test_real_24_year_outputs_preserve_stored_audits_and_actual_lineage(self):
        for region in ("a", "b"):
            path = ROOT / f"examples/{region}-history-2001-2024"
            spec, report = annual_workflow.run(path)
            with self.subTest(region=region):
                self.assertEqual(report["status"], "completed")
                self.assertEqual(report["order"], ["History", "AnnualWeighting"])
                self.assertEqual(report["scientific_validation"], "not_performed")
                upstream = report["nodes"]["History"]["artifact"]
                output = report["nodes"]["AnnualWeighting"]["artifact"]
                validate_artifact(upstream); validate_artifact(output)
                self.assertEqual(output["inputs"], {"history": upstream["artifact_id"]})
                self.assertEqual(output["lineage"], {"History": upstream["artifact_id"]})
                expected = loads((ROOT / f"examples/{region}-annual-weighting-audit.json").read_bytes())
                self.assertTrue(regional._same_result(output["value"], expected))
                self.assertEqual(output["value"]["quality"]["complete_years"], 24)
                self.assertEqual(output["value"]["provenance"]["source_history_result_sha256"],
                                 hashlib.sha256((path / "result.json").read_bytes()).hexdigest())
                trace = workflow_trace.project(spec, report)
                self.assertEqual(len(trace["nodes"]), 2)
                self.assertEqual(trace["nodes"][1]["inputs"][0]["node"], "History")
                self.assertNotIn(str(ROOT), str(spec))
                self.assertNotIn(report["run_id"], str(trace))

    def test_capture_is_once_and_execution_has_no_disk_source_reads_token_or_network(self):
        spec, registry = annual_workflow.build(self.short())
        with patch.object(history, "assemble", wraps=history.assemble) as replay, \
                patch.object(history, "capture", side_effect=AssertionError("source reopened")), \
                patch("expedition73.surface_workflow._read", side_effect=AssertionError("source reopened")), \
                patch.object(earthdata, "get_token", side_effect=AssertionError("token used")), \
                patch("expedition73.power.urlopen", side_effect=AssertionError("network used")):
            report = execute(spec, "AnnualWeighting", registry)
        self.assertEqual(report["status"], "completed")
        self.assertEqual(replay.call_count, 1)
        self.assertEqual(report["nodes"]["AnnualWeighting"]["artifact"]["value"], annual_weighting.run(self.short()))

    def test_corrupt_raw_source_blocks_annual_and_produces_no_fake_artifact(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "input"; shutil.copytree(self.short(), path)
            (path / "year-2024/response.json").write_bytes(b"corrupt raw source")
            _, report = annual_workflow.run(path)
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual(report["nodes"]["History"]["reason"], "COMPUTE_FAILED")
        self.assertEqual(report["nodes"]["AnnualWeighting"]["status"], "blocked")
        self.assertNotIn("artifact", report["nodes"]["AnnualWeighting"])

    def test_parent_manifest_and_parent_value_must_match_source_replay(self):
        for name in ("history.json", "result.json", "year-2024/result.json"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "input"; shutil.copytree(self.short(), path)
                file = path / name; data = loads(file.read_bytes())
                if name == "history.json": data["years"][0]["files_sha256"]["response.json"] = "0" * 64
                elif name == "result.json": data["series"][0]["value"] += 1
                else: del data["module_details"]
                file.write_bytes(history.encoded(data))
                _, report = annual_workflow.run(path)
                self.assertEqual(report["nodes"]["History"]["status"], "failed")
                self.assertEqual(report["nodes"]["AnnualWeighting"]["status"], "blocked")

    def test_frozen_sources_survive_later_edits_and_new_snapshot_marks_both_stale(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "input"; shutil.copytree(self.short(), path)
            spec, registry = annual_workflow.build(path)
            (path / "year-2024/response.json").write_bytes(b"changed after capture")
            report = execute(spec, "AnnualWeighting", registry)
            self.assertEqual(report["status"], "completed")
            changed_spec, changed_registry = annual_workflow.build(path)
            self.assertEqual(compare_snapshot(report, changed_spec, "AnnualWeighting"),
                             {"History": "stale", "AnnualWeighting": "stale"})
            self.assertEqual(execute(changed_spec, "AnnualWeighting", changed_registry)["status"], "incomplete")

    def test_context_cannot_relabel_the_captured_source_region_period_or_hash(self):
        spec, registry = annual_workflow.build(self.short())
        for mutate in [lambda c: c["region"].update(region_id="different"),
                       lambda c: c["period"].update(start_year=2001),
                       lambda c: c["source_files_sha256"]["history"].update(**{"result.json": "0" * 64})]:
            bad = copy.deepcopy(spec); mutate(bad["context"])
            report = execute(bad, "AnnualWeighting", registry)
            self.assertEqual(report["nodes"]["History"]["status"], "failed")
            self.assertEqual(report["nodes"]["AnnualWeighting"]["status"], "blocked")

    def test_invalid_history_payload_is_rejected_before_the_consumer_runs(self):
        spec, registry = annual_workflow.build(self.short())
        original = registry["ReplayRecordedHistory"]
        def damaged(*args):
            value = original.compute(*args)
            value["annual_inputs"][0]["cells"][0]["area_m2"] *= 2
            return value
        registry["ReplayRecordedHistory"] = Operation(original.version, original.contract, damaged, original.validate)
        report = execute(spec, "AnnualWeighting", registry)
        self.assertEqual(report["nodes"]["History"]["reason"], "OUTPUT_INVALID")
        self.assertEqual(report["nodes"]["AnnualWeighting"]["status"], "blocked")

    def test_implicit_contract_conversion_and_method_override_are_rejected(self):
        spec, registry = annual_workflow.build(self.short())
        bad = copy.deepcopy(spec)
        bad["nodes"][1]["inputs"]["history"]["contract"]["unit"] = "K"
        with self.assertRaises(PilotError): execute(bad, "AnnualWeighting", registry)
        spec["nodes"][1]["parameters"] = {"selected_weighting": "calendar_days"}
        report = execute(spec, "AnnualWeighting", registry)
        self.assertEqual(report["nodes"]["History"]["status"], "completed")
        self.assertEqual(report["nodes"]["AnnualWeighting"]["status"], "failed")

    def test_annual_output_cannot_claim_an_accepted_method(self):
        spec, registry = annual_workflow.build(self.short())
        original = registry["CompareAnnualWeighting"]
        def relabelled(*args):
            result = original.compute(*args)
            result["method"]["selected_weighting"] = "calendar_days"
            return result
        registry["CompareAnnualWeighting"] = Operation(original.version, original.contract, relabelled, original.validate)
        report = execute(spec, "AnnualWeighting", registry)
        self.assertEqual(report["nodes"]["History"]["status"], "completed")
        self.assertEqual(report["nodes"]["AnnualWeighting"]["reason"], "OUTPUT_INVALID")

    def test_replayed_missing_month_keeps_both_annual_candidates_null(self):
        files = history.capture(self.short() / "year-2024")
        request, raw = loads(files["request.json"]), loads(files["response.json"])
        raw["features"][0]["properties"]["parameter"]["T2M"]["202401"] = raw["header"]["fill_value"]
        files["response.json"] = history.encoded(raw)
        stored = loads(files["result.json"])
        files["result.json"] = history.encoded(regional.normalize(files["response.json"], request, stored["provenance"]["retrieved_at"]))
        with tempfile.TemporaryDirectory() as temp:
            seed = Path(temp) / "seed"; seed.mkdir()
            for name, data in files.items(): (seed / name).write_bytes(data)
            path = Path(temp) / "history"; history.collect(request, path, [seed])
            _, report = annual_workflow.run(path)
        self.assertEqual(report["status"], "completed")
        result = report["nodes"]["AnnualWeighting"]["artifact"]["value"]
        self.assertEqual(result["quality"]["incomplete_years"], [2024])
        self.assertIsNone(result["series"][0]["equal_month_mean_degC"])
        self.assertIsNone(result["series"][0]["calendar_day_mean_degC"])
        self.assertIsNotNone(result["series"][0]["provider_annual"]["area_weighted_mean_degC"])

    def test_cli_writes_result_and_real_trace_without_overwriting_a_previous_run(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "run"
            args = ["run-annual-workflow", "--run", str(self.short()), "--output-dir", str(output)]
            with redirect_stdout(io.StringIO()): self.assertEqual(main(args), 0)
            self.assertEqual(sorted(p.name for p in output.iterdir()),
                             ["annual-weighting.json", "request.workflow.json", "trace.json", "workflow.json"])
            before = {p.name: p.read_bytes() for p in output.iterdir()}
            with patch.object(annual_workflow, "run") as runner, redirect_stderr(io.StringIO()):
                self.assertEqual(main(args), 1)
            runner.assert_not_called()
            self.assertEqual({p.name: p.read_bytes() for p in output.iterdir()}, before)

    def test_cli_failed_run_retains_diagnostics_without_an_annual_or_trace_result(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "input"; shutil.copytree(self.short(), path)
            (path / "year-2024/response.json").write_bytes(b"corrupt raw source")
            output = Path(temp) / "run"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["run-annual-workflow", "--run", str(path), "--output-dir", str(output)]), 2)
            self.assertEqual(sorted(p.name for p in output.iterdir()), ["request.workflow.json", "workflow.json"])


if __name__ == "__main__":
    unittest.main()
