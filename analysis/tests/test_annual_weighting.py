"""Calendar arithmetic, missingness and real source-bound candidate annual audits."""
import calendar
import copy
from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal, localcontext
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from expedition73 import annual_weighting as annual, history, regional, surface_workflow
from expedition73.__main__ import main
from expedition73.power import PilotError, loads, months, validate_schema

ROOT = Path(__file__).resolve().parents[1]


def rows(year, value=10):
    return [{"date": date, "value": value, "status": "complete"} for date in months(year, year)]


def cells(year, value=10):
    return [{"area_m2": 1, "provider_annual_summary": {str(year): value}}]


class AnnualArithmeticTests(unittest.TestCase):
    def test_constant_series_and_gregorian_leap_rules(self):
        for year, days in [(2000,366),(2001,365),(2024,366),(2100,365)]:
            result = annual.summarize_year(year, rows(year, -5), cells(year, -5))
            self.assertEqual(result["calendar_days"], days)
            self.assertEqual(result["valid_calendar_days"], days)
            self.assertAlmostEqual(result["equal_month_mean_degC"], -5)
            self.assertAlmostEqual(result["calendar_day_mean_degC"], -5)
            self.assertAlmostEqual(sum(w["calendar_day_weight"] for w in result["weights"]), 1)

    def test_february_is_weighted_by_its_actual_calendar_length(self):
        for year, february, total in [(2023,28,365),(2024,29,366)]:
            data = rows(year, 0); data[1]["value"] = 100
            result = annual.summarize_year(year, data, cells(year))
            self.assertAlmostEqual(result["equal_month_mean_degC"], 100/12)
            self.assertAlmostEqual(result["calendar_day_mean_degC"], 100*february/total)
            self.assertEqual(result["weights"][1]["days"], february)

    def test_missing_month_is_not_renormalized_or_filled_by_provider_annual(self):
        data = rows(2024); data[0].update(value=None,status="incomplete")
        result = annual.summarize_year(2024, data, cells(2024, 99))
        self.assertEqual(result["valid_months"],11)
        self.assertEqual(result["valid_calendar_days"],335)
        self.assertEqual(result["missing_months"],["2024-01"])
        for key in ("equal_month_mean_degC","calendar_day_mean_degC","calendar_minus_equal_degC"):
            self.assertIsNone(result[key])
        self.assertEqual(result["provider_annual"]["area_weighted_mean_degC"],99)
        self.assertIsNone(result["provider_annual"]["provider_minus_equal_degC"])

    def test_missing_provider_cell_never_becomes_a_partial_window_mean(self):
        data = cells(2024); data.append({"area_m2":9,"provider_annual_summary":{}})
        result = annual.summarize_year(2024, rows(2024), data)
        self.assertEqual(result["provider_annual"]["valid_cells"],1)
        self.assertIsNone(result["provider_annual"]["area_weighted_mean_degC"])
        self.assertEqual(result["status"],"complete")

    def test_provider_area_weighting_and_zero_remain_values(self):
        data = cells(2024, 0); data.append({"area_m2":3,"provider_annual_summary":{"2024":20}})
        result = annual.summarize_year(2024, rows(2024,0), data)
        self.assertEqual(result["equal_month_mean_degC"],0)
        self.assertEqual(result["calendar_day_mean_degC"],0)
        self.assertEqual(result["provider_annual"]["area_weighted_mean_degC"],15)

    def test_invalid_calendar_numeric_and_status_inputs_are_rejected(self):
        for mutate in [lambda r:r.pop(), lambda r:r.reverse(), lambda r:r[1].update(date="2024-01"),
                       lambda r:r[0].update(value=True),lambda r:r[0].update(value=float("nan")),
                       lambda r:r[0].update(value=float("inf")),lambda r:r[0].update(value=None),
                       lambda r:r[0].update(status="incomplete"),lambda r:r[0].update(status="other")]:
            data=rows(2024); mutate(data)
            with self.assertRaises(PilotError): annual.summarize_year(2024,data,cells(2024))
        for year in [True,2024.0,1980,10000]:
            with self.assertRaises(PilotError): annual.summarize_year(year,rows(2024),cells(2024))
        for data in [[],[{"area_m2":0}],[{"area_m2":-1}],[{"area_m2":float("nan")}],cells(2024,float("inf"))]:
            with self.assertRaises(PilotError): annual.summarize_year(2024,rows(2024),data)

    def test_large_finite_values_do_not_overflow_before_weight_normalization(self):
        result=annual.summarize_year(2024,rows(2024,1e307),cells(2024,1e307))
        self.assertAlmostEqual(result["calendar_day_mean_degC"]/1e307,1)
        with self.assertRaises(PilotError): annual._delta(1.7e308,-1.7e308)


class AnnualRecordedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runs={r:ROOT/f"examples/{r}-history-2001-2024" for r in ("a","b")}
        cls.reports={r:annual.run(path) for r,path in cls.runs.items()}

    def test_real_24_year_audits_are_complete_and_source_bound_candidates(self):
        for r,report in self.reports.items():
            validate_schema(report,"annual-weighting.schema.json")
            self.assertEqual(report["quality"]["complete_years"],24)
            self.assertEqual(report["quality"]["provider_complete_years"],24)
            self.assertEqual([row["year"] for row in report["series"]],list(range(2001,2025)))
            self.assertIsNone(report["method"]["selected_weighting"])
            self.assertFalse(report["inference_performed"])
            self.assertEqual(report["provenance"]["source_history_result_sha256"],hashlib.sha256((self.runs[r]/"result.json").read_bytes()).hexdigest())

    def test_all_real_annual_values_match_independent_decimal_arithmetic(self):
        with localcontext() as context:
            context.prec=40
            for r,report in self.reports.items():
                source=loads((self.runs[r]/"result.json").read_bytes())
                for index,row in enumerate(report["series"]):
                    values=[Decimal(str(v["value"])) for v in source["series"][index*12:(index+1)*12]]
                    days=[calendar.monthrange(row["year"],m)[1] for m in range(1,13)]
                    equal=sum(values)/Decimal(12)
                    weighted=sum(v*d for v,d in zip(values,days))/Decimal(sum(days))
                    self.assertAlmostEqual(row["equal_month_mean_degC"],float(equal),places=11)
                    self.assertAlmostEqual(row["calendar_day_mean_degC"],float(weighted),places=11)
                    self.assertAlmostEqual(row["calendar_minus_equal_degC"],float(weighted-equal),places=11)

    def test_real_provider_reference_uses_the_same_recorded_intersection_areas(self):
        for r,report in self.reports.items():
            year=2024
            source=loads((self.runs[r]/f"year-{year}/result.json").read_bytes())
            data=source["module_details"]["cells"]
            numerator=sum(Decimal(str(c["provider_annual_summary"][str(year)]))*Decimal(str(c["area_m2"])) for c in data)
            denominator=sum(Decimal(str(c["area_m2"])) for c in data)
            self.assertAlmostEqual(report["series"][-1]["provider_annual"]["area_weighted_mean_degC"],float(numerator/denominator),places=11)

    def test_source_change_after_replay_cannot_be_used_in_an_audit(self):
        original=history.capture
        def changed(path):
            result=original(path); result["result.json"]+=b" "
            return result
        verified=history.validate_run(self.runs["a"])
        with patch.object(history,"validate_run",return_value=verified),patch.object(history,"capture",side_effect=changed):
            with self.assertRaises(PilotError): annual.run(self.runs["a"])

    def test_parent_history_change_after_replay_is_rejected(self):
        verified=history.validate_run(self.runs["a"])
        damaged=copy.deepcopy(verified); damaged["series"][0]["value"]+=1
        with patch.object(history,"validate_run",return_value=verified),patch.object(surface_workflow,"_read",return_value=history.encoded(damaged)):
            with self.assertRaises(PilotError): annual.run(self.runs["a"])

    def test_replayed_missing_year_keeps_provider_reference_without_filling_months(self):
        source=ROOT/"examples/a-history-2023-2024/year-2024"
        files=history.capture(source)
        request=loads(files["request.json"])
        raw=loads(files["response.json"])
        for cell in raw["features"]:
            cell["properties"]["parameter"]["T2M"]["202401"]=raw["header"]["fill_value"]
        raw_bytes=history.encoded(raw)
        result=regional.normalize(raw_bytes,request,loads(files["result.json"])["provenance"]["retrieved_at"])
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp); seed=directory/"seed"; seed.mkdir()
            for name,data in {"request.json":files["request.json"],"response.json":raw_bytes,"result.json":history.encoded(result)}.items():
                (seed/name).write_bytes(data)
            target=directory/"history"; history.collect(request,target,[seed])
            audit=annual.run(target)
            self.assertEqual(audit["quality"]["complete_years"],0)
            self.assertEqual(audit["quality"]["provider_complete_years"],1)
            self.assertEqual(audit["quality"]["incomplete_years"],[2024])
            self.assertEqual(audit["sensitivity"],{"valid_years":0,"max_abs_calendar_minus_equal_degC":None,"years_at_maximum":[]})
            self.assertIsNone(audit["series"][0]["calendar_day_mean_degC"])

    def test_report_replay_rejects_values_sources_and_scientific_acceptance_changes(self):
        report=self.reports["a"]
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"audit.json"; path.write_bytes(history.encoded(report))
            self.assertEqual(annual.validate_report(self.runs["a"],path),report)
            for mutate in [lambda x:x["series"][0].update(equal_month_mean_degC=999),
                           lambda x:x["provenance"].update(source_history_result_sha256="0"*64),
                           lambda x:x.update(scientific_acceptance="accepted"),lambda x:x.update(p_value=0.01)]:
                bad=copy.deepcopy(report); mutate(bad); path.write_bytes(history.encoded(bad))
                with self.assertRaises(PilotError): annual.validate_report(self.runs["a"],path)

    def test_cli_emits_json_without_creating_source_or_output_files(self):
        output=io.StringIO()
        with redirect_stdout(output): self.assertEqual(main(["audit-annual-weighting","--run",str(ROOT/"examples/a-history-2023-2024")]),0)
        report=loads(output.getvalue().encode())
        self.assertEqual(len(report["series"]),2)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"audit.json"; path.write_bytes(history.encoded(report))
            args=["validate-annual-weighting","--run",str(ROOT/"examples/a-history-2023-2024"),"--input",str(path)]
            with redirect_stdout(io.StringIO()): self.assertEqual(main(args),0)
            report["series"][0]["year"]=2022; path.write_bytes(history.encoded(report))
            with redirect_stderr(io.StringIO()): self.assertEqual(main(args),1)
            self.assertEqual([p.name for p in Path(temp).iterdir()],["audit.json"])
