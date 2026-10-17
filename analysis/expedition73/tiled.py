"""Bounded sequential POWER requests with lossless cell union and offline replay."""
from __future__ import annotations

import copy
import hashlib
import json
import math
from datetime import datetime

from . import regional
from .power import PilotError, loads, validate_schema

MAX_TILES = 16
BODY_DEGREES = 4.0  # Plus the halo remains strictly inside the per-request cap.


def plan(config):
    regional.validate_config(config, tiled=True)
    west, south, east, north = config["candidate_bbox"]
    nx, ny = math.ceil((east - west) / BODY_DEGREES), math.ceil((north - south) / BODY_DEGREES)
    if nx * ny > MAX_TILES:
        raise PilotError(f"Tiled pilot supports at most {MAX_TILES} requests; reduce the technical sample extent.")
    tiles = []
    for j in range(ny):
        for i in range(nx):
            tile = copy.deepcopy(config)
            tile["candidate_bbox"] = [west + (east - west) * i / nx, south + (north - south) * j / ny,
                                      west + (east - west) * (i + 1) / nx, south + (north - south) * (j + 1) / ny]
            tiles.append({"id": f"tile-{len(tiles) + 1:03d}", "config": tile,
                          "request_bbox": regional.validate_config(tile), "request_url": regional.request_url(tile)})
    return tiles


def manifest_entry(tile, raw, stamp):
    return {"id": tile["id"], "filename": tile["id"] + ".json", "request_url": tile["request_url"],
            "retrieved_at": stamp, "response_sha256": hashlib.sha256(raw).hexdigest()}


def fetch(config):
    # No concurrency or automatic retries: a failed tile never becomes an
    # apparently complete result. Nothing is written by the CLI until success.
    parts, entries = [], []
    for tile in plan(config):
        raw, stamp = regional.fetch(tile["config"])
        regional.normalize(raw, tile["config"], stamp)
        parts.append(raw)
        entries.append(manifest_entry(tile, raw, stamp))
    manifest = {"schema_version": "0.1.0", "format": "power_tiled_run", "tiles": entries}
    return parts, manifest


def normalize(parts, config, manifest):
    tiles = plan(config)
    validate_schema(manifest, "tiled-run-manifest.schema.json")
    if len(parts) != len(tiles) or len(manifest["tiles"]) != len(tiles):
        raise PilotError("Missing or extra tile responses; a complete deterministic plan is required.")
    cells, duplicate_count, first, requests = {}, 0, None, []
    for tile, raw, entry in zip(tiles, parts, manifest["tiles"], strict=True):
        expected_entry = manifest_entry(tile, raw, entry["retrieved_at"])
        if entry != expected_entry:
            raise PilotError("Tile manifest does not match the plan, URL, filename or raw-response hash.")
        # This checks even halo-only cells, coordinates, months and per-tile
        # completeness before the cross-tile union can cover up an omission.
        regional.normalize(raw, tile["config"], entry["retrieved_at"])
        data = loads(raw)
        if first is None:
            first = data
        elif data["header"] != first["header"] or data["parameters"] != first["parameters"]:
            raise PilotError("Tile source, API, units, time standard, fill value or dates disagree.")
        for feature in data["features"]:
            key = tuple(feature["geometry"]["coordinates"][:2])
            if key in cells:
                if cells[key] != feature:
                    raise PilotError(f"Overlapping cell {key} differs between tiles; refusing to blend responses.")
                duplicate_count += 1
            else:
                cells[key] = feature
        requests.append({**entry, "candidate_bbox": tile["config"]["candidate_bbox"], "request_bbox": tile["request_bbox"],
                         "provider_messages": data.get("messages", [])})
    # Keep provider values on their original grid, then apply the original
    # scientific window exactly once. Tile means are deliberately unused.
    merged = {"type": "FeatureCollection", "header": first["header"], "parameters": first["parameters"],
              "messages": [], "features": list(cells.values())}
    completed_at = max((entry["retrieved_at"] for entry in manifest["tiles"]),
                       key=lambda stamp: datetime.fromisoformat(stamp.replace("Z", "+00:00")))
    access = {"provenance": {"provider": "NASA POWER", "product": "POWER Monthly and Annual API",
              "api_version": first["header"]["api"]["version"], "sources": first["header"]["sources"],
              "retrieved_at": completed_at, "requests": requests},
              "summary": {"strategy": "sequential_grid_cell_union", "version": "0.1.0", "tile_count": len(tiles),
                          "duplicate_cells_removed": duplicate_count, "unique_returned_cells": len(cells)}}
    return regional.normalize(json.dumps(merged, allow_nan=False).encode(), config, completed_at, _access=access)


def validate_run(directory):
    config = loads((directory / "request.json").read_bytes())
    manifest = loads((directory / "manifest.json").read_bytes())
    # Filenames come only from the recomputed plan, never from untrusted paths.
    parts = [(directory / (tile["id"] + ".json")).read_bytes() for tile in plan(config)]
    stored = loads((directory / "result.json").read_bytes())
    validate_schema(stored, "monthly-tiled-window-series.schema.json")
    replay = normalize(parts, config, manifest)
    if not regional._same_result(stored, replay):
        raise PilotError("Tiled result differs from full raw-tile replay.")
    return stored
