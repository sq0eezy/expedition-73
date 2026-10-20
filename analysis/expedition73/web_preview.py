"""Build a bounded, credential-free static view from replayed recorded inputs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath

from . import masking, regional, surface_source, surface_support, surface_workflow
from .power import PilotError, loads

ASSETS = ("index.html", "styles.css", "app.js")


def _spatial(window, mask, config, audit):
    """Expose only recorded cell values and the existing audited geometry/weights."""
    fractions = masking.validate_mask(mask, config)
    cells = {(c["longitude"], c["latitude"]): c for c in window["module_details"]["cells"]}
    rows = []
    for cell in audit["cells"]:
        key = (cell["longitude"], cell["latitude"])
        rows.append({**{name: cell[name] for name in (
            "longitude", "latitude", "full_cell_bbox", "intersection_bbox", "clipped", "intersection_area_m2")},
            "fractions": dict(fractions[key]),
            "series": [{"date": row["date"], "value": row["value"]} for row in cells[key]["series"]],
            "weights_m2": {"unmasked": cell["intersection_area_m2"], **{
                policy: cell["policies"][policy]["uniform_estimate_m2"] for policy in surface_support.POLICIES}}})
    return {"geometry": "reconstructed_midpoint_rectangles", "longitude_step_deg": regional.DLON,
            "latitude_step_deg": regional.DLAT, "area_radius_m": regional.RADIUS_M,
            "fraction_placement": "uniform_within_full_cell_assumption", "cells": rows}


def _directory(root, name):
    if not isinstance(name, str) or not name or "\\" in name:
        raise PilotError("Preview inputs must use analysis-relative directories.")
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {"..", "."} for part in name.split("/")) or path.parts[0] not in {"examples", "artifacts"}:
        raise PilotError("Preview inputs must stay in analysis/examples or analysis/artifacts.")
    candidate = (root / name).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise PilotError("Preview input resolves outside analysis.")
    return candidate


def payload(analysis_root, registry):
    root = Path(analysis_root)
    if not isinstance(registry, list) or not 1 <= len(registry) <= 8:
        raise PilotError("Preview requires one to eight explicit region sources.")
    regions, dates, ids, context = [], None, set(), None
    for entry in registry:
        if not isinstance(entry, dict) or set(entry) != {"id", "display_name", "window", "fractions"}:
            raise PilotError("Unexpected preview registry fields.")
        if not isinstance(entry["display_name"], str) or not 1 <= len(entry["display_name"].strip()) <= 100:
            raise PilotError("Preview regions need an explicit short display name.")
        if not isinstance(entry["id"], str) or entry["id"] in ids:
            raise PilotError("Duplicate or invalid preview region identity.")
        window_dir, fraction_dir = _directory(root, entry["window"]), _directory(root, entry["fractions"])
        _, report = surface_workflow.run(window_dir, fraction_dir)
        if report["status"] != "completed":
            raise PilotError("A source workflow failed; no partial preview exported.")
        temperature = report["nodes"]["Temperature"]["artifact"]["value"]
        mask = report["nodes"]["Fractions"]["artifact"]["value"]["result"]
        summary = report["nodes"]["Sensitivity"]["artifact"]["value"]
        if summary["region"]["id"] != entry["id"]:
            raise PilotError("Registry identity disagrees with replayed region.")
        months = [row["date"] for row in summary["series"]]
        if len(months) != 12 or months != [months[0][:4] + f"-{month:02d}" for month in range(1, 13)]:
            raise PilotError("This first preview supports one complete calendar year of monthly records.")
        if dates is not None and months != dates:
            raise PilotError("Preview regions must use the same monthly calendar.")
        provider = summary["provenance"]["temperature"]
        signature = {"variable": summary["variable"], "time": summary["time"],
                     "provider": {key: provider[key] for key in ("provider", "product", "api_version", "sources")}}
        if context is not None and signature != context:
            raise PilotError("Preview regions disagree on indicator, time standard or provider metadata.")
        context = signature
        dates = months
        # Capabilities refer to precisely the metadata captured by the source run.
        with (fraction_dir / "metadata.dmr.xml").open("rb") as stream:
            metadata = stream.read(1_000_001)
        expected = summary["provenance"]["source_files_sha256"]["fractions"]["metadata.dmr.xml"]
        if hashlib.sha256(metadata).hexdigest() != expected:
            raise PilotError("Metadata changed after source replay; rebuild from a consistent snapshot.")
        audit = surface_support._summarize(temperature["result"], mask, temperature["request"])
        regions.append({"id": entry["id"], "display_name": entry["display_name"], "region": summary["region"],
                        "variable": summary["variable"], "time": summary["time"],
                        "series": summary["series"], "diagnostics": summary["diagnostics"],
                        "support": {key: value for key, value in audit.items()
                                    if key in {"window_area_m2", "cell_count", "clipped_cells", "policies"}},
                        "spatial": _spatial(temperature["result"], mask, temperature["request"], audit),
                        "source_area": surface_source.area_capability(metadata)["area"],
                        "provenance": summary["provenance"]})
        ids.add(entry["id"])
    return {"schema_version": "0.2.0", "output_type": "recorded_temperature_web_preview",
            "data_mode": "recorded_offline_replay", "selection_status": "candidate",
            "inference_performed": False, "dates": dates, "regions": regions}


def build(analysis_root, web_root, output):
    web, destination = Path(web_root), Path(output)
    if destination.resolve() in {web.resolve(), (web / "src").resolve(), Path(analysis_root).resolve(), web.parent.resolve()}:
        raise PilotError("Preview output must not overwrite source assets.")
    allowed = {*ASSETS, "data", "data/results.json"}
    if destination.is_symlink() or (destination.exists() and any(
            item.is_symlink() or item.relative_to(destination).as_posix() not in allowed
            for item in destination.rglob("*"))):
        raise PilotError("Preview output must be a dedicated directory containing only generated public assets.")
    data = payload(analysis_root, loads((web / "regions.json").read_bytes()))
    # Only enumerated public assets and validated preview data may be served.
    files = {name: (web / "src" / name).read_bytes() for name in ASSETS}
    files["data/results.json"] = (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    destination.mkdir(parents=True, exist_ok=True)
    for name, raw in files.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return {"status": "built", "regions": [item["id"] for item in data["regions"]],
            "months": len(data["dates"]), "files": sorted(files), "live_nasa_request": False}
