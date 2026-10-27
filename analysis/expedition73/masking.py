"""Candidate surface-fraction checks; no automatic mask/method selection.

Small recorded NASA subsets are bundled; fresh OPeNDAP access needs login.
Whole-cell fractions on clipped window pieces are a declared approximation.
"""
from __future__ import annotations

import math
from datetime import datetime

from . import regional, tiled
from .power import PilotError, finite, validate_schema

COMPONENTS = ("FRLAND", "FRLANDICE", "FRLAKE", "FROCEAN")
FRACTION_TOLERANCE = 1e-6


def request_plan(config):
    # Reuse the bounded pilot's geographic/time checks without fetching T2M.
    tiled.plan(config)
    coordinates = sorted(regional.expected_cells(config["candidate_bbox"]), key=lambda p: (p[1], p[0]))
    xs = sorted({round((lon + 180) / regional.DLON) for lon, _ in coordinates})
    ys = sorted({round((lat + 90) / regional.DLAT) for _, lat in coordinates})
    return {"schema_version": "0.1.0", "output_type": "surface_mask_request_plan",
            "region_id": config["region_id"], "candidate_bbox": config["candidate_bbox"],
            "candidate_window_version": config["candidate_window_version"],
            "source_candidate": {"dataset": "M2C0NXASM", "version": "5.12.4",
                                 "collection_id": "C1276812819-GES_DISC", "access_verified": False},
            "grid": {"id": "merra2_output_0.625x0.5", "shape_lat_lon": [361, 576],
                     "origin_lon_lat": [-180, -90], "step_lon_lat": [0.625, 0.5]},
            "required_components": list(COMPONENTS), "unit": "1", "time_index": 0,
            "zero_based_inclusive_indices": {"longitude": [min(xs), max(xs)], "latitude": [min(ys), max(ys)]},
            "expected_cells": len(coordinates),
            "cells": [{"longitude": lon, "latitude": lat} for lon, lat in coordinates],
            "status": "plan_only_no_provider_fractions", "inference_allowed": False,
            "warnings": ["SOURCE_METADATA_AND_DIMENSION_ORDER_REQUIRE_AUTHENTICATED_VERIFICATION",
                         "NO_MASK_VALUES_FETCHED", "NOT_AN_ACCEPTED_ANALYSIS_PROFILE"]}


def validate_mask(mask, config, *, allow_synthetic=False):
    validate_schema(mask, "surface-fractions.schema.json")
    if mask["data_origin"] == "synthetic_fixture" and not allow_synthetic:
        raise PilotError("Synthetic fractions require explicit --allow-synthetic; they are not NASA measurements.")
    try:
        stamp = datetime.fromisoformat(mask["source"]["retrieved_at"].replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError("Timezone missing")
    except ValueError as exc:
        raise PilotError("Mask source timestamp must be valid and timezone-aware.") from exc
    if mask["data_origin"] == "synthetic_fixture" and mask["source"]["uri"] != "urn:expedition73:synthetic-fixture":
        raise PilotError("Synthetic fractions must use the synthetic source label.")
    if mask["data_origin"] == "provider_subset" and not mask["source"]["uri"].startswith("https://"):
        raise PilotError("Provider fractions require their HTTPS subset source URI.")
    wanted = {(c["longitude"], c["latitude"]) for c in request_plan(config)["cells"]}
    found = {}
    for cell in mask["cells"]:
        coordinate = (finite(cell["longitude"], "mask longitude"), finite(cell["latitude"], "mask latitude"))
        if coordinate in found:
            raise PilotError("Duplicate mask cell.")
        if coordinate not in wanted:
            raise PilotError("Mask coordinate is outside the expected native-grid window; regridding is not implicit.")
        fractions = cell["fractions"]
        total = math.fsum(finite(fractions[name], name) for name in COMPONENTS)
        if not math.isclose(total, 1, rel_tol=0, abs_tol=FRACTION_TOLERANCE):
            raise PilotError("Surface fractions must partition each whole source cell within 1e-6.")
        found[coordinate] = fractions
    if found.keys() != wanted:
        raise PilotError("Mask must cover every intersecting source cell, including zero-land cells.")
    return found


def preview_series(window, mask, config, components, *, allow_synthetic=False):
    """Called after the CLI has replay-validated the original window run."""
    if (not components or len(set(components)) != len(components)
            or not set(components) <= {"FRLAND", "FRLANDICE"}):
        raise PilotError("Choose FRLAND and/or FRLANDICE explicitly, without duplicates; no default land/ice policy.")
    if (window["region"]["candidate_bbox"] != config["candidate_bbox"]
            or window["region"]["candidate_window_version"] != config["candidate_window_version"]
            or window["region"]["id"] != config["region_id"]):
        raise PilotError("Window result and request geometry/identity disagree.")
    fractions = validate_mask(mask, config, allow_synthetic=allow_synthetic)
    cells = window["module_details"]["cells"]
    weights = []
    for cell in cells:
        key = (cell["longitude"], cell["latitude"])
        fraction = math.fsum(fractions[key][name] for name in components)
        if fraction > 1:
            raise PilotError("Chosen components exceed one; fractions were not silently renormalized.")
        weights.append(cell["area_m2"] * fraction)
    support_area = math.fsum(weights)
    if support_area <= 0:
        raise PilotError("Selected mask has zero effective area; no temperature can be calculated.")
    active = [(cell, weight) for cell, weight in zip(cells, weights, strict=True) if weight > 0]
    series = []
    for index, original in enumerate(window["series"]):
        valid = [(c, w) for c, w in active if c["series"][index]["value"] is not None]
        complete = len(valid) == len(active)
        series.append({"date": original["date"], "value": math.fsum(
            w * c["series"][index]["value"] for c, w in valid) / support_area if complete else None,
            "status": "complete" if complete else "incomplete", "active_cells": len(active),
            "valid_active_cells": len(valid), "valid_effective_area_fraction": math.fsum(w for _, w in valid) / support_area})
    return {"schema_version": "0.1.0", "output_type": "candidate_surface_weight_preview",
            "selection_status": "candidate", "data_origin": mask["data_origin"],
            "region": window["region"], "variable": window["variable"], "time": window["time"],
            "method": {"id": "whole_cell_fraction_on_window_intersection", "version": "0.1.0",
                       "selected_components": list(components), "fraction_sum_tolerance": FRACTION_TOLERANCE,
                       "missing_policy": "require_all_positive_weight_cells", "inference": "not_performed"},
            "spatial_support": {"effective_area_m2": support_area,
                                "effective_fraction_of_window": support_area / window["spatial_support"]["window_area_m2"]},
            "provenance": {"temperature": window["provenance"], "mask_source": mask["source"],
                           "mask_source_authenticity": "not_checked_by_preview"},
            "warnings": ["CANDIDATE_PREVIEW_NOT_ACCEPTED_REGION_MEAN", "FRACTION_ASSUMED_UNIFORM_WITHIN_SOURCE_CELL",
                         "T2M_REMAINS_SOURCE_GRID_TEMPERATURE_NOT_LAND_TILE_TEMPERATURE",
                         "NO_FINE_SCALE_COASTLINE_RECOVERY", "INFERENCE_NOT_PERFORMED"], "series": series}
