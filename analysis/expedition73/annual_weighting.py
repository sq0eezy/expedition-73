"""Compare two candidate annual summaries of replayed unmasked T2M; no trend."""
from __future__ import annotations

import calendar
import copy
import hashlib
import math
from pathlib import Path

from . import history, regional, surface_workflow
from .power import PilotError, loads, months, validate_schema

METHOD = {"id": "compare_annual_temperature_weighting", "version": "0.1.0",
          "selection_status": "candidate", "selected_weighting": None,
          "missing_policy": "require_12_complete_months", "inference": "not_performed",
          "provider_value_role": "comparison_only"}
DEFINITIONS = [
    {"id": "equal_months", "formula": "sum(T_m / 12)", "target": "mean_of_twelve_monthly_values"},
    {"id": "calendar_days", "formula": "sum(T_m * days_m / days_year)", "target": "calendar_day_weighted_monthly_values"},
]


def _number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def _mean(values, weights):
    try:
        total = math.fsum(weights)
        value = math.fsum(v * (w / total) for v, w in zip(values, weights, strict=True))
    except (OverflowError, ValueError, ZeroDivisionError) as exc:
        raise PilotError("Annual weighting arithmetic is not finite.") from exc
    if not math.isfinite(value):
        raise PilotError("Annual weighting arithmetic is not finite.")
    return value


def _delta(left, right):
    if left is None or right is None:
        return None
    value = left - right
    if not math.isfinite(value):
        raise PilotError("Annual weighting difference is not finite.")
    return value


def summarize_year(year, rows, cells):
    """Pure arithmetic; the public run entry point first replays raw sources."""
    if type(year) is not int or not 1981 <= year <= 9999 or not isinstance(rows, list) or len(rows) != 12 or any(not isinstance(r, dict) for r in rows) or [r.get("date") for r in rows] != months(year, year):
        raise PilotError("Annual summaries require twelve ordered calendar months.")
    for row in rows:
        if row.get("status") not in {"complete", "incomplete"} or not (row.get("value") is None or _number(row["value"])):
            raise PilotError("Invalid monthly value or completeness status.")
        if (row["status"] == "complete") != (row["value"] is not None):
            raise PilotError("Monthly completeness disagrees with its value.")
    days = [calendar.monthrange(year, month)[1] for month in range(1, 13)]
    total_days = sum(days)
    valid = [i for i, row in enumerate(rows) if row["status"] == "complete"]
    complete = len(valid) == 12
    values = [row["value"] for row in rows]
    equal = _mean(values, [1] * 12) if complete else None
    weighted = _mean(values, days) if complete else None
    if not isinstance(cells, list) or not cells or any(not isinstance(c, dict) or not _number(c.get("area_m2")) or c["area_m2"] <= 0 or not isinstance(c.get("provider_annual_summary", {}), dict) for c in cells):
        raise PilotError("Provider comparison requires positive recorded intersection areas.")
    provider_values = [c.get("provider_annual_summary", {}).get(str(year)) for c in cells]
    if any(v is not None and not _number(v) for v in provider_values):
        raise PilotError("Provider annual cell value is not finite.")
    provider_count = sum(v is not None for v in provider_values)
    provider_value = _mean(provider_values, [c["area_m2"] for c in cells]) if provider_count == len(cells) else None
    return {"year": year, "status": "complete" if complete else "incomplete",
            "valid_months": len(valid), "missing_months": [r["date"] for r in rows if r["status"] != "complete"],
            "calendar_days": total_days, "valid_calendar_days": sum(days[i] for i in valid),
            "weights": [{"date": row["date"], "days": days[i], "equal_month_weight": 1 / 12,
                         "calendar_day_weight": days[i] / total_days} for i, row in enumerate(rows)],
            "equal_month_mean_degC": equal, "calendar_day_mean_degC": weighted,
            "calendar_minus_equal_degC": _delta(weighted, equal),
            "provider_annual": {"status": "complete" if provider_value is not None else "incomplete",
                                "expected_cells": len(cells), "valid_cells": provider_count,
                                "area_weighted_mean_degC": provider_value,
                                "provider_minus_equal_degC": _delta(provider_value, equal),
                                "provider_minus_calendar_degC": _delta(provider_value, weighted)}}


def run(directory):
    """Replay the entire history; bind every subsequent annual read to its hashes."""
    directory = Path(directory)
    verified = history.validate_run(directory)
    recorded_history = surface_workflow._read(directory, "result.json", limit=8_000_000)
    if not regional._same_result(loads(recorded_history), verified):
        raise PilotError("Recorded history changed after raw-source replay; no audit produced.")
    if verified["spatial_support"]["kind"] != "unmasked_rectangular_window" or verified["spatial_support"]["mask"] != "none":
        raise PilotError("This candidate audit accepts only replayed unmasked window histories.")
    series = []
    for entry in verified["provenance"]["annual_sources"]:
        files = history.capture(directory / f"year-{entry['year']}")
        if surface_workflow._hashes(files) != entry["files_sha256"]:
            raise PilotError("Annual source changed after complete history replay; no audit produced.")
        # These exact result bytes have already been checked against every raw
        # annual response by validate_run. Never substitute an unbound re-read.
        annual = loads(files["result.json"])
        series.append(summarize_year(entry["year"], annual["series"], annual["module_details"]["cells"]))
    valid = [row for row in series if row["calendar_minus_equal_degC"] is not None]
    maximum = max((abs(r["calendar_minus_equal_degC"]) for r in valid), default=None)
    result = {"schema_version": "0.1.0", "output_type": "candidate_annual_weighting_audit",
              "selection_status": "candidate", "inference_performed": False, "scientific_acceptance": "not_performed",
              "module": {"id": "air_temperature_2m_annual_weighting", "version": "0.1.0"},
              **{k: copy.deepcopy(verified[k]) for k in ("region", "variable", "spatial_support")},
              "time": {"frequency": "annual", "input_frequency": "monthly", "calendar": "gregorian",
                       "provider_time_standard": verified["time"]["provider_time_standard"],
                       "start": verified["time"]["start"][:4], "end": verified["time"]["end"][:4]},
              "method": copy.deepcopy(METHOD), "weighting_definitions": copy.deepcopy(DEFINITIONS),
              "provenance": {**copy.deepcopy(verified["provenance"]),
                             "source_history_schema_version": verified["schema_version"],
                             "source_history_result_sha256": hashlib.sha256(recorded_history).hexdigest()},
              "series": series,
              "quality": {"expected_years": len(series), "complete_years": len(valid),
                          "incomplete_years": [r["year"] for r in series if r["status"] != "complete"],
                          "provider_complete_years": sum(r["provider_annual"]["status"] == "complete" for r in series),
                          "warnings": ["CANDIDATE_UNMASKED_WINDOW_NOT_ACCEPTED_SCIENTIFIC_PROFILE",
                                       "TWO_DISTINCT_ANNUAL_SUMMARY_TARGETS_NO_SELECTION",
                                       "PROVIDER_ANNUAL_IS_SAME_SOURCE_COMPARISON_NOT_INDEPENDENT_VALIDATION",
                                       "MONTHLY_API_VALUES_HAVE_SOURCE_PRECISION_NO_EXTRA_ACCURACY",
                                       "NO_IMPUTATION_TREND_ANOMALY_OR_CLIMATE_NORMAL"]},
              "sensitivity": {"valid_years": len(valid), "max_abs_calendar_minus_equal_degC": maximum,
                              "years_at_maximum": [r["year"] for r in valid if abs(r["calendar_minus_equal_degC"]) == maximum]}}
    validate_schema(result, "annual-weighting.schema.json")
    return result


def validate_report(directory, report_path):
    stored = loads(surface_workflow._read(Path(report_path).parent, Path(report_path).name, limit=2_000_000))
    validate_schema(stored, "annual-weighting.schema.json")
    replay = run(directory)
    if not regional._same_result(stored, replay):
        raise PilotError("Annual audit differs from raw-source replay, source identity, weights or candidate flags.")
    return replay
