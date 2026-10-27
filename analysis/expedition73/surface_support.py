"""Conditional area bounds for clipped cells, not physical error bars.

Treat a recorded fraction as an exact areal fraction on the pilot's declared
sphere. Its subcell placement is unknown. No temperature bounds or inference.
"""
from __future__ import annotations

import copy
import math

from . import masking, regional, surface_workflow
from .power import PilotError, finite

VERSION = "0.1.0"
POLICIES = {"land": ["FRLAND"], "land_and_ice": ["FRLAND", "FRLANDICE"]}


def area_bounds(full_area, intersection_area, fraction):
    """Conservation bounds if fraction is exact on the same declared area measure."""
    full = finite(full_area, "full cell area")
    part = finite(intersection_area, "intersection area")
    f = finite(fraction, "selected fraction")
    if full <= 0 or not 0 <= part <= full or not 0 <= f <= 1:
        raise PilotError("Area bounds require 0 <= intersection <= full area and fraction in [0,1].")
    # These endpoints avoid cancellation for full/empty selections and cells.
    if part == 0 or f == 0:
        low = high = estimate = 0.0
    elif f == 1:
        low = high = estimate = part
    elif part == full:
        low = high = estimate = full * f
    else:
        selected = full * f
        low = max(0.0, selected - (full - part))
        high = min(part, selected)
        estimate = part * f
    return {"lower_m2": low, "uniform_estimate_m2": estimate, "upper_m2": high}


def _summarize(window, mask, config):
    """Internal: caller supplies a replayed window; fractions still validated here."""
    fractions = masking.validate_mask(mask, config)
    expected = regional.expected_cells(config["candidate_bbox"])
    cells = window["module_details"]["cells"]
    if len(cells) != len(expected) or {(c["longitude"], c["latitude"]) for c in cells} != expected.keys():
        raise PilotError("Support audit requires the complete replayed native-grid window.")
    rows = []
    for cell in cells:
        lon, lat = cell["longitude"], cell["latitude"]
        full_bbox = [lon - regional.DLON / 2, lat - regional.DLAT / 2,
                     lon + regional.DLON / 2, lat + regional.DLAT / 2]
        intersection = expected[(lon, lat)]
        full, part = regional.spherical_area(full_bbox), regional.spherical_area(intersection)
        if cell["intersection_bbox"] != intersection or not math.isclose(cell["area_m2"], part, rel_tol=1e-12):
            raise PilotError("Replayed cell intersection geometry disagrees with the audit.")
        policies = {}
        for name, components in POLICIES.items():
            f = math.fsum(fractions[(lon, lat)][component] for component in components)
            policies[name] = {"selected_fraction": f, **area_bounds(full, part, f)}
        rows.append({"longitude": lon, "latitude": lat, "full_cell_bbox": full_bbox,
                     "intersection_bbox": intersection, "full_cell_area_m2": full,
                     "intersection_area_m2": part, "clipped": intersection != full_bbox,
                     "policies": policies})
    rows.sort(key=lambda row: (row["latitude"], row["longitude"]))
    area = math.fsum(row["intersection_area_m2"] for row in rows)
    if not math.isclose(area, window["spatial_support"]["window_area_m2"], rel_tol=1e-12):
        raise PilotError("Audit intersections do not cover the replayed window.")
    policies = {}
    for name, components in POLICIES.items():
        sums = {key: math.fsum(row["policies"][name][key] for row in rows)
                for key in ("lower_m2", "uniform_estimate_m2", "upper_m2")}
        policies[name] = {"selected_components": list(components), **sums,
                          "lower_fraction_of_window": sums["lower_m2"] / area,
                          "uniform_fraction_of_window": sums["uniform_estimate_m2"] / area,
                          "upper_fraction_of_window": sums["upper_m2"] / area,
                          "placement_range_m2": sums["upper_m2"] - sums["lower_m2"],
                          "ambiguous_clipped_cells": sum(
                              row["policies"][name]["upper_m2"] > row["policies"][name]["lower_m2"]
                              for row in rows)}
    return {"schema_version": VERSION, "output_type": "candidate_surface_support_audit",
            "selection_status": "candidate", "region": copy.deepcopy(window["region"]),
            "method": {"id": "conditional_subcell_area_conservation_bounds", "version": VERSION,
                       "area_measure": "pilot_midpoint_rectangles_on_declared_sphere",
                       "radius_m": regional.RADIUS_M, "fractions_treated_as_exact_areal_shares": True,
                       "subcell_placement": "unknown", "mask_policy_accepted": False,
                       "inference": "not_performed"},
            "window_area_m2": area, "cell_count": len(rows),
            "clipped_cells": sum(row["clipped"] for row in rows),
            "clipped_intersection_area_fraction": math.fsum(
                row["intersection_area_m2"] for row in rows if row["clipped"]) / area,
            "policies": policies, "cells": rows,
            "warnings": ["CONDITIONAL_AREA_BOUNDS_NOT_CONFIDENCE_INTERVALS",
                         "SOURCE_FRACTION_AND_AREA_MEASURE_COMPATIBILITY_NOT_VALIDATED",
                         "NO_SUBCELL_COASTLINE_OR_TEMPERATURE_RECOVERY",
                         "NO_TEMPERATURE_ERROR_OR_TREND_INFERENCE",
                         "NO_AUTOMATIC_MASK_POLICY_SELECTION"]}


def run(window_directory, fraction_directory):
    """Replay/freeze existing inputs once. No credential or network access."""
    _, report = surface_workflow.run(window_directory, fraction_directory)
    if report["status"] != "completed":
        raise PilotError("Source workflow did not complete; no support audit produced.")
    temperature = report["nodes"]["Temperature"]["artifact"]["value"]
    mask = report["nodes"]["Fractions"]["artifact"]["value"]["result"]
    result = _summarize(temperature["result"], mask, temperature["request"])
    result["provenance"] = copy.deepcopy(report["nodes"]["Sensitivity"]["artifact"]["value"]["provenance"])
    return result
