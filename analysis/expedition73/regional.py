"""Experimental unmasked rectangular-window means, separate from point results.

Cell edges are an explicit midpoint reconstruction on the MERRA-2 output grid.
No polygon, land fraction, elevation adjustment, interpolation or inference.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .power import (PilotError, finite, loads, normalize as normalize_point,
                    validate_config as validate_point_config, validate_schema)

VERSION = "0.1.0"
RADIUS_M = 6_371_008.8  # Declared spherical approximation, not provider cell areas.
DLON, DLAT = 0.625, 0.5
ENDPOINT = "https://power.larc.nasa.gov/api/temporal/monthly/regional"
MAX_BYTES = 2_000_000


def validate_config(config, *, tiled=False):
    validate_schema(config, "window-request.schema.json")
    west, south, east, north = config["candidate_bbox"]
    point_config = {k: v for k, v in config.items() if k != "mask"}
    point_config["point"] = {"longitude": (west + east) / 2, "latitude": (south + north) / 2}
    validate_point_config(point_config)
    bounds = [west - DLON / 2, south - DLAT / 2, east + DLON / 2, north + DLAT / 2]
    if bounds[0] < -180 or bounds[2] > 180 or bounds[1] < -90 or bounds[3] > 90:
        raise PilotError("This window pilot does not support a halo crossing poles/dateline.")
    if not tiled and (bounds[2] - bounds[0] > 5 or bounds[3] - bounds[1] > 5):
        raise PilotError("Single-request limit: padded window must be at most 5 degrees per axis; use fetch-power-tiled-window.")
    if config["end_year"] - config["start_year"] > 1:
        raise PilotError("Window access pilot supports at most two years per request.")
    return bounds


def request_url(config):
    west, south, east, north = validate_config(config)
    return ENDPOINT + "?" + urlencode({
        "parameters": "T2M", "community": "SB", "longitude-min": west,
        "longitude-max": east, "latitude-min": south, "latitude-max": north,
        "format": "JSON", "start": config["start_year"], "end": config["end_year"],
    })


def fetch(config):
    url = request_url(config)
    try:
        with urlopen(Request(url, headers={"User-Agent": "Expedition73/0.1 window-pilot"}), timeout=40) as response:
            raw = response.read(MAX_BYTES + 1)
    except HTTPError as exc:
        raise PilotError(f"NASA POWER returned HTTP {exc.code}; no window result produced.") from exc
    except (URLError, TimeoutError) as exc:
        raise PilotError("NASA POWER window request failed or timed out; retry explicitly.") from exc
    if len(raw) > MAX_BYTES:
        raise PilotError("NASA POWER response exceeds the window pilot size limit.")
    return raw, datetime.now(timezone.utc).isoformat(timespec="seconds")


def spherical_area(bounds):
    """Exact rectangle integral on the declared sphere, in square metres."""
    west, south, east, north = bounds
    return RADIUS_M ** 2 * math.radians(east - west) * (
        math.sin(math.radians(north)) - math.sin(math.radians(south)))


def expected_cells(bounds):
    west, south, east, north = bounds
    lons = [-180 + i * DLON for i in range(576)
            if -180 + i * DLON + DLON / 2 > west and -180 + i * DLON - DLON / 2 < east]
    lats = [-90 + j * DLAT for j in range(361)
            if -90 + j * DLAT + DLAT / 2 > south and -90 + j * DLAT - DLAT / 2 < north]
    return {(lon, lat): [max(west, lon - DLON / 2), max(south, lat - DLAT / 2),
                         min(east, lon + DLON / 2), min(north, lat + DLAT / 2)]
            for lat in lats for lon in lons}


def normalize(raw, config, retrieved_at, *, _access=None):
    # _access is supplied only by the tiled orchestrator after each API response
    # and overlapping cell has been checked. Single-request 0.1 remains intact.
    halo = validate_config(config, tiled=_access is not None)
    data = loads(raw)
    expected = expected_cells(config["candidate_bbox"])
    try:
        if data["type"] != "FeatureCollection" or not isinstance(data["features"], list):
            raise PilotError("A POWER regional FeatureCollection is required.")
        if data["header"]["sources"] != ["MERRA2"]:
            raise PilotError("Only the MERRA2 output grid is supported by this window adapter.")
        if data["header"]["api"]["name"] != "POWER Monthly and Annual API":
            raise PilotError("Unsupported POWER service metadata.")
        cells, seen = [], set()
        for feature in data["features"]:
            if feature["type"] != "Feature" or feature["geometry"]["type"] != "Point":
                raise PilotError("Regional features must be grid-centre Points.")
            lon, lat = [finite(x, "grid coordinate") for x in feature["geometry"]["coordinates"][:2]]
            for value, origin, step in [(lon, -180, DLON), (lat, -90, DLAT)]:
                if not math.isclose((value - origin) / step, round((value - origin) / step), abs_tol=1e-8, rel_tol=0):
                    raise PilotError("Provider coordinates do not match the supported MERRA2 grid.")
            if not (halo[0] <= lon <= halo[2] and halo[1] <= lat <= halo[3]):
                raise PilotError("Provider coordinate lies outside the requested halo.")
            if (lon, lat) in seen:
                raise PilotError("Duplicate provider grid cell.")
            seen.add((lon, lat))
            # Reuse the strict monthly value/unit/header decoder. This internal
            # point profile describes the API halo, not the scientific window.
            point_config = {k: v for k, v in config.items() if k != "mask"}
            point_config.update(candidate_bbox=halo, point={"longitude": lon, "latitude": lat})
            point_data = dict(feature, header=data["header"], parameters=data["parameters"], messages=data.get("messages", []))
            decoded = normalize_point(json.dumps(point_data, allow_nan=False).encode(), point_config, retrieved_at)
            if (lon, lat) not in expected:
                continue  # A halo-only cell has zero intersection weight.
            intersection = expected[(lon, lat)]
            cells.append({"longitude": lon, "latitude": lat, "intersection_bbox": intersection,
                          "area_m2": spherical_area(intersection), "series": decoded["series"],
                          "provider_annual_summary": decoded["module_details"]["provider_annual_summary"]})
        if set(expected) - seen:
            raise PilotError("Regional response omits cells intersecting the window; refusing a partial spatial support.")
        cells.sort(key=lambda c: (c["latitude"], c["longitude"]))
        total_area = math.fsum(c["area_m2"] for c in cells)
        window_area = spherical_area(config["candidate_bbox"])
        if not math.isclose(total_area, window_area, rel_tol=1e-10):
            raise PilotError("Cell intersections do not cover the declared window.")
        series = []
        for index, row in enumerate(cells[0]["series"]):
            valid = [c for c in cells if c["series"][index]["value"] is not None]
            valid_area = math.fsum(c["area_m2"] for c in valid)
            complete = len(valid) == len(cells)
            series.append({"date": row["date"], "value": math.fsum(
                c["area_m2"] * c["series"][index]["value"] for c in valid) / total_area if complete else None,
                "status": "complete" if complete else "incomplete",
                "valid_cells": len(valid), "valid_area_fraction": valid_area / total_area})
        complete_months = sum(r["status"] == "complete" for r in series)
        result = {
            "schema_version": VERSION, "output_type": "monthly_window_series",
            "module": {"id": "air_temperature_2m", "version": VERSION},
            "region": {"id": config["region_id"], **{k: config[k] for k in ("label", "selection_status", "candidate_bbox", "candidate_window_version")}},
            "variable": {"id": "air_temperature_2m", "unit": "degC", "height_m": 2},
            "time": {"frequency": "monthly", "start": series[0]["date"], "end": series[-1]["date"],
                     "calendar": "gregorian", "provider_time_standard": data["header"]["time_standard"]},
            "spatial_support": {"kind": "unmasked_rectangular_window", "mask": "none",
                                "request_bbox": halo, "cell_count": len(cells), "window_area_m2": window_area,
                                "grid_step_degrees": {"longitude": DLON, "latitude": DLAT}},
            "method": {"id": "spherical_midpoint_cell_intersection", "version": VERSION,
                       "sphere_radius_m": RADIUS_M, "missing_policy": "require_all_intersecting_cells",
                       "inference": "not_performed"},
            "provenance": _access["provenance"] if _access is not None else {"provider": "NASA POWER", "product": "POWER Monthly and Annual API", "request_url": request_url(config),
                           "retrieved_at": retrieved_at, "response_sha256": hashlib.sha256(raw).hexdigest(),
                           "api_version": data["header"]["api"]["version"], "sources": data["header"]["sources"]},
            "quality": {"expected_months": len(series), "complete_months": complete_months,
                        "warnings": ["CANDIDATE_WINDOW_NOT_ACCEPTED_REGION", "NO_LAND_WATER_MASK",
                                     "RECONSTRUCTED_CELL_BOUNDS_SPHERICAL_AREA", "PROVIDER_PIXEL_QA_NOT_SUPPLIED", "INFERENCE_NOT_PERFORMED"]},
            "series": series, "module_details": {"cells": cells, "provider_header": data["header"],
                "provider_parameter": data["parameters"]["T2M"], "provider_messages": data.get("messages", [])},
        }
    except (KeyError, TypeError, IndexError, ValueError) as exc:
        if isinstance(exc, PilotError):
            raise
        raise PilotError("Malformed POWER regional response.") from exc
    if _access is not None:
        result["schema_version"] = "0.2.0"
        result["module"]["version"] = "0.2.0"
        result["provenance"] = _access["provenance"]
        result["spatial_support"]["request_envelope_bbox"] = result["spatial_support"].pop("request_bbox")
        result["module_details"]["access"] = _access["summary"]
    validate_schema(result, "monthly-tiled-window-series.schema.json" if _access is not None else "monthly-window-series.schema.json")
    return result


def validate_run(directory):
    """Offline replay checks the complete derivation, not just a plausible mean."""
    request = loads((directory / "request.json").read_bytes())
    stored = loads((directory / "result.json").read_bytes())
    validate_schema(stored, "monthly-window-series.schema.json")
    replay = normalize((directory / "response.json").read_bytes(), request, stored["provenance"]["retrieved_at"])
    if not _same_result(stored, replay):
        raise PilotError("Window result differs from raw-response replay (values, geometry, quality or provenance).")
    return stored


def _same_result(left, right):
    # libm can differ in the last bits between Windows and Linux/macOS.
    # Hashes/strings/keys/order remain exact; only finite numbers have tolerance.
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(_same_result(left[k], right[k]) for k in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(_same_result(a, b) for a, b in zip(left, right))
    if type(left) in (int, float) and type(right) in (int, float):
        return math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-10)
    return type(left) is type(right) and left == right
