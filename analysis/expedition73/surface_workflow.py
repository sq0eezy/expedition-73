"""Recorded NASA subsets -> candidate weight sensitivity, entirely offline.

Every source is replayed. Grid correspondence is checked, not scientific mask
acceptance. Full-cell fractions on clipped pieces remain an approximation.
"""
from __future__ import annotations

import hashlib
import copy
from pathlib import Path

from . import masking, regional, surface_source, tiled
from .power import PilotError, loads, validate_schema
from .workflow import Operation, execute

VERSION = "0.1.0"
WINDOW = {"type": "verified_power_window", "schema_version": VERSION, "unit": "degC"}
FRACTIONS = {"type": "verified_surface_fractions", "schema_version": VERSION, "unit": "1"}
PREVIEW = {"type": "candidate_surface_weight_preview", "schema_version": VERSION, "unit": "degC"}
SENSITIVITY = {"type": "candidate_surface_sensitivity", "schema_version": VERSION, "unit": "degC"}


def _read(directory, filename, limit=2_000_000):
    # Only fixed filenames or tile ids from the recomputed plan are read.
    with (Path(directory) / filename).open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise PilotError("Recorded source file exceeds the pilot size limit.")
    return raw


def _hashes(files):
    return {name: hashlib.sha256(raw).hexdigest() for name, raw in sorted(files.items())}


def _identity(request):
    return {key: request[key] for key in ("region_id", "candidate_bbox", "candidate_window_version")}


def _window_replay(files):
    request, stored = loads(files["request.json"]), loads(files["result.json"])
    if "manifest.json" in files:
        validate_schema(stored, "monthly-tiled-window-series.schema.json")
        parts = [files[tile["id"] + ".json"] for tile in tiled.plan(request)]
        replayed = tiled.normalize(parts, request, loads(files["manifest.json"]))
    else:
        validate_schema(stored, "monthly-window-series.schema.json")
        replayed = regional.normalize(files["response.json"], request, stored["provenance"]["retrieved_at"])
    if not regional._same_result(stored, replayed):
        raise PilotError("Temperature snapshot differs from source replay.")
    return {"request": request, "result": replayed}


def _summarize(window, land, land_ice):
    if (land["method"]["selected_components"] != ["FRLAND"]
            or land_ice["method"]["selected_components"] != ["FRLAND", "FRLANDICE"]):
        raise PilotError("Sensitivity policy labels differ from actual selected components.")
    series = []
    for original, left, right in zip(window["series"], land["series"], land_ice["series"], strict=True):
        if not original["date"] == left["date"] == right["date"]:
            raise PilotError("Sensitivity inputs have different dates.")
        u, a, b = original["value"], left["value"], right["value"]
        series.append({"date": original["date"], "unmasked": u, "land": a, "land_and_ice": b,
                       "land_minus_unmasked": a - u if a is not None and u is not None else None,
                       "land_ice_minus_land": b - a if b is not None and a is not None else None})
    def maximum(field):
        values = [abs(item[field]) for item in series if item[field] is not None]
        return max(values) if values else None
    return {"schema_version": VERSION, "output_type": SENSITIVITY["type"], "selection_status": "candidate",
            "data_origin": "recorded_provider_subsets", "region": window["region"],
            "variable": window["variable"], "time": window["time"],
            "method": {"id": "surface_component_sensitivity", "version": VERSION,
                       "weight_method": land["method"]["id"], "weight_method_version": land["method"]["version"],
                       "policies": {"land": ["FRLAND"], "land_and_ice": ["FRLAND", "FRLANDICE"]},
                       "mask_policy_accepted": False, "inference": "not_performed"},
            "spatial_support": {"unmasked_area_m2": window["spatial_support"]["window_area_m2"],
                                "land": land["spatial_support"], "land_and_ice": land_ice["spatial_support"]},
            "diagnostics": {"months": len(series),
                            "complete_paired_months": sum(all(row[key] is not None for key in
                                                              ("unmasked", "land", "land_and_ice")) for row in series),
                            "max_abs_land_minus_unmasked_degC": maximum("land_minus_unmasked"),
                            "max_abs_land_ice_minus_land_degC": maximum("land_ice_minus_land")},
            "warnings": sorted(set(land["warnings"] + land_ice["warnings"] + [
                "RECORDED_SOURCE_REPLAY_NOT_INDEPENDENT_SOURCE_AUTHENTICATION",
                "GRID_CORRESPONDENCE_NOT_ACCEPTED_SCIENTIFIC_PROFILE"])), "series": series}


def build(window_directory, fraction_directory):
    """Capture the bounded sources once; callbacks never reopen files or fetch."""
    window_files = {name: _read(window_directory, name) for name in ("request.json", "result.json")}
    request = loads(window_files["request.json"])
    if (Path(window_directory) / "manifest.json").is_file():
        window_files["manifest.json"] = _read(window_directory, "manifest.json")
        for tile in tiled.plan(request):
            name = tile["id"] + ".json"
            window_files[name] = _read(window_directory, name)
    else:
        window_files["response.json"] = _read(window_directory, "response.json")
    fraction_files = {name: _read(fraction_directory, name) for name in
                      ("request.json", "conversion-report.json", "metadata.dmr.xml", "response.nc4", "fractions.json")}
    context = {"scope": "candidate_surface_sensitivity", "region": _identity(request),
               "period": {"start_year": request["start_year"], "end_year": request["end_year"]},
               "source_files_sha256": {"temperature": _hashes(window_files), "fractions": _hashes(fraction_files)}}

    def load_window(inputs, parameters, context):
        return _window_replay(window_files)

    def validate_window(value, context):
        if _identity(value["request"]) != context["region"]:
            raise PilotError("Window belongs to a different region context.")
        result = value["result"]
        if result["variable"] != {"id": "air_temperature_2m", "unit": "degC", "height_m": 2}:
            raise PilotError("Unexpected temperature quantity.")
        validate_schema(result, "monthly-tiled-window-series.schema.json" if result["schema_version"] == "0.2.0"
                        else "monthly-window-series.schema.json")

    def load_fractions(inputs, parameters, context):
        fraction_request = loads(fraction_files["request.json"])
        temperature = inputs["temperature"]["value"]
        if _identity(fraction_request) != _identity(temperature["request"]):
            raise PilotError("Mask and temperature candidate identities/bounds disagree.")
        mask = surface_source.replay_data(
            fraction_request, loads(fraction_files["conversion-report.json"]), fraction_files["metadata.dmr.xml"],
            fraction_files["response.nc4"], loads(fraction_files["fractions.json"]))
        masking.validate_mask(mask, temperature["request"])
        return {"request": fraction_request, "result": mask,
                "conversion_audit": "recorded_provider_subset_replay_passed"}

    def validate_fractions(value, context):
        if _identity(value["request"]) != context["region"]:
            raise PilotError("Fractions belong to a different region context.")
        masking.validate_mask(value["result"], value["request"])
        if value["result"]["data_origin"] != "provider_subset":
            raise PilotError("This workflow requires a recorded provider subset, not synthetic fractions.")

    def preview(inputs, parameters, context):
        temperature = inputs["temperature"]["value"]
        mask = inputs["fractions"]["value"]["result"]
        result = masking.preview_series(temperature["result"], mask, temperature["request"], parameters["components"])
        result["provenance"]["workflow_inputs"] = {name: artifact["artifact_id"] for name, artifact in inputs.items()}
        result["provenance"]["conversion_audit"] = "recorded_provider_subset_replay_passed"
        return result

    def validate_preview(value, context, components):
        if (value["output_type"] != PREVIEW["type"] or value["selection_status"] != "candidate"
                or value["region"]["id"] != context["region"]["region_id"]
                or value["method"]["inference"] != "not_performed"
                or value["method"]["selected_components"] != components):
            raise PilotError("Invalid candidate preview envelope.")

    def summarize(inputs, parameters, context):
        window = inputs["temperature"]["value"]["result"]
        land = inputs["land"]["value"]
        result = _summarize(window, land, inputs["land_and_ice"]["value"])
        result["provenance"] = {"temperature": window["provenance"],
                                "surface_fractions": land["provenance"]["mask_source"],
                                "source_files_sha256": context["source_files_sha256"],
                                "conversion_audit": "recorded_provider_subset_replay_passed"}
        return result

    def validate_summary(value, context):
        if (value["output_type"] != SENSITIVITY["type"] or value["method"]["mask_policy_accepted"] is not False
                or value["region"]["id"] != context["region"]["region_id"]):
            raise PilotError("Invalid candidate sensitivity envelope.")

    def link(node, contract):
        return {"node": node, "output": "result", "contract": dict(contract)}
    def node(name, inputs, contract, parameters=None):
        return {"id": name, "operation": name, "version": VERSION, "inputs": copy.deepcopy(inputs),
                "parameters": parameters or {}, "output_contract": dict(contract)}
    preview_inputs = {"temperature": link("Temperature", WINDOW), "fractions": link("Fractions", FRACTIONS)}
    nodes = [node("Temperature", {}, WINDOW),
             node("Fractions", {"temperature": link("Temperature", WINDOW)}, FRACTIONS),
             node("Land", preview_inputs, PREVIEW, {"components": ["FRLAND"]}),
             node("LandIce", preview_inputs, PREVIEW, {"components": ["FRLAND", "FRLANDICE"]}),
             node("Sensitivity", {"temperature": link("Temperature", WINDOW), "land": link("Land", PREVIEW),
                                  "land_and_ice": link("LandIce", PREVIEW)}, SENSITIVITY)]
    callbacks = [(load_window, validate_window), (load_fractions, validate_fractions),
                 (preview, lambda value, context: validate_preview(value, context, ["FRLAND"])),
                 (preview, lambda value, context: validate_preview(value, context, ["FRLAND", "FRLANDICE"])),
                 (summarize, validate_summary)]
    registry = {definition["id"]: Operation(VERSION, definition["output_contract"], compute, validate)
                for definition, (compute, validate) in zip(nodes, callbacks, strict=True)}
    return {"schema_version": VERSION, "context": context, "nodes": nodes}, registry


def run(window_directory, fraction_directory):
    spec, registry = build(window_directory, fraction_directory)
    return spec, execute(spec, "Sensitivity", registry)
