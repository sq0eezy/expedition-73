"""Annual source snapshots -> continuous unmasked monthly history; no inference."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from contextlib import contextmanager
import shutil
from uuid import uuid4

from . import regional, surface_workflow, tiled
from .power import PilotError, loads, months, validate_schema

MAX_YEARS = 50


@contextmanager
def staging(parent):
    # Inherit the output parent's permissions. TemporaryDirectory's private
    # Windows ACL would otherwise survive rename and block the normal runner.
    stage = parent / (".history-" + uuid4().hex)
    stage.mkdir()
    try:
        yield stage
    finally:
        if stage.exists():
            if stage.is_symlink() or not stage.resolve().is_relative_to(parent.resolve()):
                raise PilotError("Refusing cleanup outside the owned history staging directory.")
            shutil.rmtree(stage)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def plan(config):
    validate_schema(config, "window-request.schema.json")
    if any(type(config[k]) is not int for k in ("start_year", "end_year")):
        raise PilotError("History years must be integer JSON values.")
    count = config["end_year"] - config["start_year"] + 1
    if not 1 <= count <= MAX_YEARS:
        raise PilotError("History requires one to fifty ordered calendar years.")
    result = []
    for year in range(config["start_year"], config["end_year"] + 1):
        request = {**copy.deepcopy(config), "start_year": year, "end_year": year}
        regional.validate_config(request, tiled=True)
        # Bound both time and geographic work before making any request.
        tiled.plan(request)
        result.append(request)
    return result


def capture(directory):
    files = {name: surface_workflow._read(directory, name) for name in ("request.json", "result.json")}
    request = loads(files["request.json"])
    validate_schema(request, "window-request.schema.json")
    if request["start_year"] != request["end_year"]:
        raise PilotError("History inputs must be single complete calendar-year runs.")
    if (Path(directory) / "manifest.json").exists():
        files["manifest.json"] = surface_workflow._read(directory, "manifest.json")
        for tile in tiled.plan(request):
            name = tile["id"] + ".json"
            files[name] = surface_workflow._read(directory, name)
    else:
        files["response.json"] = surface_workflow._read(directory, "response.json")
    return files


def signature(result):
    provider = result["provenance"]
    support = copy.deepcopy(result["spatial_support"])
    if "request_bbox" in support:
        support["request_envelope_bbox"] = support.pop("request_bbox")
    return {"region": result["region"], "variable": result["variable"], "method": result["method"],
            "time": {k: result["time"][k] for k in ("frequency", "calendar", "provider_time_standard")},
            "provider": {k: provider[k] for k in ("provider", "product", "api_version", "sources")},
            "spatial_support": support,
            "grid": [{k: c[k] for k in ("longitude", "latitude", "intersection_bbox", "area_m2")}
                     for c in result["module_details"]["cells"]]}


def assemble(config, annual_files):
    requests = plan(config)
    if len(annual_files) != len(requests):
        raise PilotError("Every planned year requires exactly one source run.")
    rows, entries, baseline, first = [], [], None, None
    for request, files in zip(requests, annual_files, strict=True):
        expected_files = {"request.json", "result.json"} | (
            {"manifest.json", *(tile["id"] + ".json" for tile in tiled.plan(request))}
            if "manifest.json" in files else {"response.json"})
        if set(files) != expected_files:
            raise PilotError("Annual snapshot has unexpected or missing source files.")
        if loads(files["request.json"]) != request:
            raise PilotError("Annual source request differs from planned year, window or configuration.")
        snapshot = surface_workflow._window_replay(files)
        result = snapshot["result"]
        current = signature(result)
        if baseline is not None and not regional._same_result(current, baseline):
            raise PilotError("Years disagree on source/API, variable, time standard, method, grid or spatial support.")
        if first is None:
            baseline, first = current, result
        rows.extend(copy.deepcopy(result["series"]))
        entries.append({"year": request["start_year"], "files_sha256": surface_workflow._hashes(files)})
    if [r["date"] for r in rows] != list(months(config["start_year"], config["end_year"])):
        raise PilotError("Missing, overlapping or out-of-order history months.")
    manifest = {"schema_version": "0.1.0", "format": "annual_verified_window_runs", "years": entries}
    result = {"schema_version": "0.1.0", "output_type": "recorded_window_history", "selection_status": "candidate",
              **{k: copy.deepcopy(first[k]) for k in ("region", "variable", "method", "spatial_support")},
              "time": {**baseline["time"], "start": rows[0]["date"], "end": rows[-1]["date"]},
              "provenance": {**baseline["provider"], "annual_sources": entries},
              "quality": {"expected_months": len(rows), "complete_months": sum(r["status"] == "complete" for r in rows),
                          "missing_months": [r["date"] for r in rows if r["status"] != "complete"],
                          "warnings": first["quality"]["warnings"] + ["NO_TREND_OR_SCIENTIFIC_PROFILE_ACCEPTANCE"]},
              "series": rows}
    support = result["spatial_support"]
    if "request_bbox" in support:
        support["request_envelope_bbox"] = support.pop("request_bbox")
    validate_schema(result, "window-history.schema.json")
    return manifest, result


def validate_run(directory):
    directory = Path(directory)
    config = loads(surface_workflow._read(directory, "request.json"))
    files = [capture(directory / f"year-{c['start_year']}") for c in plan(config)]
    manifest, replay = assemble(config, files)
    if loads(surface_workflow._read(directory, "history.json")) != manifest:
        raise PilotError("History manifest differs from replayed annual source hashes.")
    stored = loads(surface_workflow._read(directory, "result.json", limit=8_000_000))
    validate_schema(stored, "window-history.schema.json")
    if not regional._same_result(stored, replay):
        raise PilotError("Stored history differs from complete annual-source replay.")
    return replay


def collect(config, destination, seeds=(), *, fetch_missing=False):
    """Explicit recorded seeds, no persistent cache; publish only a complete run."""
    config = copy.deepcopy(config)
    requests = plan(config)
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise PilotError("History output already exists; choose a new directory.")
    available = {}
    for directory in seeds:
        files = capture(directory)
        request = loads(files["request.json"])
        year = request["start_year"]
        if year in available or request not in requests:
            raise PilotError("Duplicate, extra or incompatible annual seed run.")
        # Check every supplied seed before any network operation.
        surface_workflow._window_replay(files)
        available[year] = files
    if not fetch_missing and set(available) != {c["start_year"] for c in requests}:
        raise PilotError("Offline assembly is missing annual source runs.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with staging(destination.parent) as stage:
        if not stage.resolve().is_relative_to(destination.parent.resolve()):
            raise PilotError("History staging directory escaped its intended parent.")
        annual = []
        for request in requests:
            year = request["start_year"]
            files = available.get(year)
            if files is None:
                try:
                    regional.validate_config(request)
                    single = True
                except PilotError:
                    single = False  # All other validation has already passed in plan().
                if single:
                    raw, stamp = regional.fetch(request)
                    result = regional.normalize(raw, request, stamp)
                    files = {"response.json": raw, "result.json": encoded(result)}
                else:
                    parts, manifest = tiled.fetch(request)
                    result = tiled.normalize(parts, request, manifest)
                    files = {"manifest.json": encoded(manifest), "result.json": encoded(result),
                             **{tile["id"] + ".json": raw for tile, raw in zip(tiled.plan(request), parts, strict=True)}}
                files["request.json"] = encoded(request)
            annual.append(files)
            child = stage / f"year-{year}"
            child.mkdir()
            for name, raw in files.items():
                (child / name).write_bytes(raw)
        manifest, result = assemble(config, annual)
        for name, value in (("request.json", config), ("history.json", manifest), ("result.json", result)):
            (stage / name).write_bytes(encoded(value))
        validate_run(stage)
        # The destination was absent; no existing recorded run is overwritten.
        if destination.exists() or destination.is_symlink():
            raise PilotError("History destination appeared during collection; previous files preserved.")
        stage.rename(destination)
    return result
