"""NASA POWER monthly T2M point access and strict, loss-aware normalization."""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

from . import __version__

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://power.larc.nasa.gov/api/temporal/monthly/point"
MAX_RESPONSE_BYTES = 2_000_000


class PilotError(ValueError):
    """Invalid input, provider response, or unsupported scientific interpretation."""


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise PilotError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _bad_constant(value):
    raise PilotError(f"Non-finite JSON number: {value}")


def loads(raw: bytes | str):
    try:
        return json.loads(raw, object_pairs_hook=_pairs, parse_constant=_bad_constant,
                          parse_float=lambda value: finite(float(value), "JSON number"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise PilotError("Input is not valid UTF-8 JSON.") from exc


@lru_cache(maxsize=16)
def _validator(name):
    # Schemas are immutable during a CLI run. Reusing compiled validators keeps
    # per-cell validation affordable when several API tiles are replayed.
    schema = loads((ROOT / "schemas" / name).read_bytes())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_schema(value, name: str) -> None:
    try:
        json.dumps(value, allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise PilotError("Contract values must be finite JSON data.") from exc
    try:
        _validator(name).validate(value)
    except ValidationError as exc:
        location = ".".join(map(str, exc.absolute_path)) or "document"
        raise PilotError(f"{location}: {exc.message}") from exc


def finite(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise PilotError(f"{label} must be a finite number.")
    return float(value)


def validate_config(config: dict) -> None:
    validate_schema(config, "point-request.schema.json")
    point = config["point"]
    lon = finite(point["longitude"], "longitude")
    lat = finite(point["latitude"], "latitude")
    west, south, east, north = config["candidate_bbox"]
    for number in config["candidate_bbox"]:
        finite(number, "candidate_bbox")
    if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
        raise PilotError("candidate_bbox must be ordered west,south,east,north; dateline crossing is unsupported.")
    if not (west <= lon <= east and south <= lat <= north):
        raise PilotError("Probe point must lie inside its candidate search window.")
    if config["start_year"] > config["end_year"]:
        raise PilotError("start_year must not exceed end_year.")
    if type(config["start_year"]) is not int or type(config["end_year"]) is not int:
        raise PilotError("Years must be integer JSON values.")
    if config["end_year"] > datetime.now(timezone.utc).year:
        raise PilotError("Future years are outside the point probe scope.")


def request_url(config: dict) -> str:
    validate_config(config)
    return ENDPOINT + "?" + urlencode({
        "parameters": "T2M", "community": "SB",
        "longitude": float(config["point"]["longitude"]), "latitude": float(config["point"]["latitude"]),
        "format": "JSON", "start": config["start_year"], "end": config["end_year"],
    })


def fetch(config: dict) -> tuple[bytes, str]:
    url = request_url(config)
    try:
        with urlopen(Request(url, headers={"User-Agent": "Expedition73/0.1 science-pilot"}), timeout=40) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    except HTTPError as exc:
        raise PilotError(f"NASA POWER returned HTTP {exc.code}; no sample was produced.") from exc
    except (URLError, TimeoutError) as exc:
        raise PilotError("NASA POWER request failed or timed out; retry explicitly.") from exc
    if len(raw) > MAX_RESPONSE_BYTES:
        raise PilotError("NASA POWER response exceeds the point pilot size limit.")
    return raw, datetime.now(timezone.utc).isoformat(timespec="seconds")


def months(start: int, end: int) -> list[str]:
    return [f"{year:04d}-{month:02d}" for year in range(start, end + 1) for month in range(1, 13)]


def normalize(raw: bytes, config: dict, retrieved_at: str) -> dict:
    validate_config(config)
    data = loads(raw)
    try:
        if data["type"] != "Feature" or data["geometry"]["type"] != "Point":
            raise PilotError("Only POWER point samples are supported; regional data needs a separate adapter.")
        header = data["header"]
        meta = data["parameters"]["T2M"]
        values = data["properties"]["parameter"]["T2M"]
        coordinates = data["geometry"]["coordinates"]
        if meta["units"] != "C" or meta["longname"] != "Temperature at 2 Meters":
            raise PilotError("Unsupported T2M definition/unit; no implicit conversion was performed.")
        if header["start"] != f"{config['start_year']}0101" or header["end"] != f"{config['end_year']}1231":
            raise PilotError("Provider date range does not match the request.")
        if len(coordinates) < 2:
            raise PilotError("Provider point coordinates are missing.")
        lon, lat = (finite(coordinates[i], "provider coordinates") for i in (0, 1))
        if not (math.isclose(lon, config["point"]["longitude"], abs_tol=1e-6, rel_tol=0)
                and math.isclose(lat, config["point"]["latitude"], abs_tol=1e-6, rel_tol=0)):
            raise PilotError("Provider point does not match the requested location.")
        fill = finite(header["fill_value"], "fill_value")
        if not isinstance(values, dict) or not isinstance(header["sources"], list) or not header["sources"]:
            raise PilotError("Provider values/sources are missing or malformed.")
        annual = {}
        for key, value in values.items():
            if len(key) != 6 or not key.isdigit():
                raise PilotError(f"Unexpected POWER period key: {key}")
            year, month = int(key[:4]), int(key[4:])
            if not config["start_year"] <= year <= config["end_year"] or not 1 <= month <= 13:
                raise PilotError(f"Out-of-range POWER period: {key}")
            number = finite(value, f"T2M[{key}]")
            if month == 13:
                annual[str(year)] = None if number == fill else number
        series = []
        for date in months(config["start_year"], config["end_year"]):
            key = date.replace("-", "")
            if key not in values:
                value, status = None, "not_returned"
            elif values[key] == fill:
                value, status = None, "provider_fill"
            else:
                value, status = finite(values[key], key), "valid"
            series.append({"date": date, "value": value, "status": status})
        valid = sum(row["status"] == "valid" for row in series)
        digest = hashlib.sha256(raw).hexdigest()
        result = {
            "schema_version": "0.1.0", "output_type": "monthly_point_series",
            "module": {"id": "air_temperature_2m", "version": __version__},
            "region": {"id": config["region_id"], "label": config["label"],
                       "selection_status": "candidate", "candidate_bbox": config["candidate_bbox"],
                       "candidate_window_version": config["candidate_window_version"]},
            "spatial_support": {"kind": "point_sample", "longitude": lon, "latitude": lat},
            "variable": {"id": "air_temperature_2m", "unit": "degC", "height_m": 2},
            "time": {"frequency": "monthly", "start": series[0]["date"], "end": series[-1]["date"],
                     "calendar": "gregorian", "provider_time_standard": header["time_standard"]},
            "provenance": {"provider": "NASA POWER", "product": "POWER Monthly and Annual API",
                           "api_version": header["api"]["version"], "sources": header["sources"],
                           "request_url": request_url(config), "retrieved_at": retrieved_at,
                           "response_sha256": digest},
            "method": {"id": "power_t2m_point_normalization", "version": __version__,
                       "inference": "not_performed"},
            "quality": {"expected_months": len(series), "valid_months": valid,
                        "missing_months": len(series) - valid,
                        "status": "complete" if valid == len(series) else "incomplete",
                        "warnings": ["POINT_SAMPLE_NOT_REGION_AVERAGE", "INFERENCE_NOT_PERFORMED",
                                     "PROVIDER_PIXEL_QA_NOT_SUPPLIED"]},
            "series": series,
            "module_details": {"provider_header": header, "provider_parameter": meta,
                               "provider_coordinates": coordinates, "provider_annual_summary": annual,
                               "provider_messages": data.get("messages", [])},
        }
    except (KeyError, TypeError, IndexError) as exc:
        raise PilotError("Malformed POWER response: required structure is absent.") from exc
    validate_result(result)
    return result


def validate_result(result: dict) -> None:
    validate_schema(result, "monthly-point-series.schema.json")
    try:
        stamp = datetime.fromisoformat(result["provenance"]["retrieved_at"].replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError("Timezone required")
    except ValueError as exc:
        raise PilotError("retrieved_at must be a valid timestamp with timezone.") from exc
    finite(result["spatial_support"]["longitude"], "longitude")
    finite(result["spatial_support"]["latitude"], "latitude")
    start, end = result["time"]["start"], result["time"]["end"]
    request = {"schema_version": result["schema_version"], "region_id": result["region"]["id"],
               "label": result["region"]["label"], "selection_status": result["region"]["selection_status"],
               "candidate_bbox": result["region"]["candidate_bbox"],
               "candidate_window_version": result["region"]["candidate_window_version"],
               "point": {key: result["spatial_support"][key] for key in ("longitude", "latitude")},
               "start_year": int(start[:4]), "end_year": int(end[:4])}
    if result["provenance"]["request_url"] != request_url(request):
        raise PilotError("Request provenance does not match the point/date window.")
    header = result["module_details"]["provider_header"]
    try:
        if (header["start"] != start.replace("-", "") + "01"
                or header["end"] != end.replace("-", "") + "31"
                or header["api"]["version"] != result["provenance"]["api_version"]
                or header["sources"] != result["provenance"]["sources"]
                or header["time_standard"] != result["time"]["provider_time_standard"]):
            raise PilotError("Provider metadata and normalized provenance disagree.")
    except (KeyError, TypeError) as exc:
        raise PilotError("Provider metadata is incomplete.") from exc
    expected = months(int(start[:4]), int(end[:4]))
    if start[5:] != "01" or end[5:] != "12" or [r["date"] for r in result["series"]] != expected:
        raise PilotError("Series must contain each requested month exactly once in chronological order.")
    for row in result["series"]:
        if (row["status"] == "valid") != (row["value"] is not None):
            raise PilotError("Null/value and observation status disagree.")
        if row["value"] is not None:
            finite(row["value"], "series value")
    quality = result["quality"]
    valid = sum(row["status"] == "valid" for row in result["series"])
    if (quality["expected_months"], quality["valid_months"], quality["missing_months"]) != (len(expected), valid, len(expected) - valid):
        raise PilotError("Quality counts do not match the series.")
    if quality["status"] != ("complete" if valid == len(expected) else "incomplete"):
        raise PilotError("Quality status does not match coverage.")


def compatibility(left: dict, right: dict) -> dict:
    """Report time-series alignment only; this does not authorize regional inference."""
    validate_result(left)
    validate_result(right)
    paths = [("schema_version",), ("output_type",), ("module", "version"), ("method",),
             ("variable",), ("time",), ("provenance", "provider"),
             ("provenance", "product"), ("provenance", "api_version"), ("provenance", "sources")]
    reasons = []
    for path in paths:
        a, b = left, right
        for key in path:
            a, b = a[key], b[key]
        if a != b:
            reasons.append(".".join(path))
    right_values = {row["date"]: row["value"] for row in right["series"]}
    paired = sum(row["value"] is not None and right_values.get(row["date"]) is not None
                 for row in left["series"])
    if paired == 0:
        reasons.append("no_paired_valid_months")
    return {"status": "incompatible" if reasons else "aligned_point_series",
            "reasons": reasons, "paired_valid_months": paired,
            "inference_allowed": False, "scope": "transport_and_time_alignment_only"}
