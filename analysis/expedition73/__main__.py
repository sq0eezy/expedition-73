"""Run from analysis/: python -m expedition73 --help."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from .power import PilotError, compatibility, fetch, loads, normalize, validate_result
from . import masking, regional, tiled


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("demo-workflow", help="Offline synthetic A -> B, A+B -> C dependency experiment; no science.")
    surface_run = commands.add_parser("run-surface-workflow", help="Replay local NASA inputs and compare two candidate fraction policies; offline.")
    surface_run.add_argument("--window-run", type=Path, required=True)
    surface_run.add_argument("--fraction-run", type=Path, required=True)
    surface_run.add_argument("--output-dir", type=Path, required=True)
    support = commands.add_parser("audit-surface-support", help="Conditional clipped-cell area bounds; offline, no policy selection.")
    support.add_argument("--window-run", type=Path, required=True)
    support.add_argument("--fraction-run", type=Path, required=True)
    probe = commands.add_parser("fetch-power-point", help="Fetch and validate a small candidate point sample; no trend.")
    probe.add_argument("--config", type=Path, required=True)
    probe.add_argument("--output-dir", type=Path, required=True)
    window = commands.add_parser("fetch-power-window", help="Experimental unmasked rectangle means; no trend.")
    window.add_argument("--config", type=Path, required=True)
    window.add_argument("--output-dir", type=Path, required=True)
    tiled_probe = commands.add_parser("fetch-power-tiled-window", help="Fetch a candidate window in bounded tiles; no trend.")
    tiled_probe.add_argument("--config", type=Path, required=True)
    tiled_probe.add_argument("--output-dir", type=Path, required=True)
    tiled_check = commands.add_parser("validate-tiled-window", help="Replay all raw tile responses offline.")
    tiled_check.add_argument("directory", type=Path)
    mask_plan = commands.add_parser("plan-surface-mask", help="List required native grid cells/indices; does not fetch fractions.")
    mask_plan.add_argument("--config", type=Path, required=True)
    mask_preview = commands.add_parser("preview-surface-mask", help="Experimental fraction weighting; no accepted analysis profile.")
    mask_preview.add_argument("--run", type=Path, required=True)
    mask_preview.add_argument("--mask", type=Path, required=True)
    mask_preview.add_argument("--components", nargs="+", required=True, choices=["FRLAND", "FRLANDICE"])
    mask_preview.add_argument("--allow-synthetic", action="store_true")
    replay = commands.add_parser("validate-window", help="Replay a complete window run offline, including geometry and weights.")
    replay.add_argument("directory", type=Path)
    validate = commands.add_parser("validate", help="Validate schema and monthly consistency offline.")
    validate.add_argument("input", type=Path)
    compare = commands.add_parser("check-alignment", help="Check point-series transport alignment; no inference.")
    compare.add_argument("left", type=Path)
    compare.add_argument("right", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "audit-surface-support":
            from .surface_support import run
            print(json.dumps(run(args.window_run, args.fraction_run), ensure_ascii=False, indent=2, allow_nan=False))
        elif args.command == "run-surface-workflow":
            from .surface_workflow import run
            if args.output_dir.exists():
                raise PilotError("Output directory already exists; choose a new run directory.")
            spec, report = run(args.window_run, args.fraction_run)
            args.output_dir.mkdir(parents=True, exist_ok=False)
            write_json(args.output_dir / "request.workflow.json", spec)
            write_json(args.output_dir / "workflow.json", report)
            summary = {"status": report["status"], "region": spec["context"]["region"]["region_id"],
                       "nodes": {name: record["status"] for name, record in report["nodes"].items()}}
            if report["status"] != "completed":
                print(json.dumps(summary, ensure_ascii=False))
                return 2
            result = report["nodes"]["Sensitivity"]["artifact"]["value"]
            write_json(args.output_dir / "sensitivity.json", result)
            print(json.dumps({**summary, "diagnostics": result["diagnostics"]}, ensure_ascii=False))
        elif args.command == "demo-workflow":
            from .workflow_demo import run
            print(json.dumps(run(), ensure_ascii=False, indent=2, allow_nan=False))
        elif args.command == "plan-surface-mask":
            print(json.dumps(masking.request_plan(loads(args.config.read_bytes())), ensure_ascii=False, indent=2))
        elif args.command == "preview-surface-mask":
            config = loads((args.run / "request.json").read_bytes())
            window = tiled.validate_run(args.run) if (args.run / "manifest.json").exists() else regional.validate_run(args.run)
            mask_raw = args.mask.read_bytes()
            mask = loads(mask_raw)
            result = masking.preview_series(window, mask, config, args.components, allow_synthetic=args.allow_synthetic)
            result["provenance"]["mask_input_sha256"] = hashlib.sha256(mask_raw).hexdigest()
            print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        elif args.command == "fetch-power-tiled-window":
            if args.output_dir.exists():
                raise PilotError("Output directory already exists; choose a new run directory.")
            config = loads(args.config.read_bytes())
            parts, manifest = tiled.fetch(config)
            result = tiled.normalize(parts, config, manifest)
            args.output_dir.mkdir(parents=True, exist_ok=False)
            for tile, raw in zip(tiled.plan(config), parts, strict=True):
                (args.output_dir / (tile["id"] + ".json")).write_bytes(raw)
            write_json(args.output_dir / "request.json", config)
            write_json(args.output_dir / "manifest.json", manifest)
            write_json(args.output_dir / "result.json", result)
            print(json.dumps({"output": str(args.output_dir), "access": result["module_details"]["access"], "quality": result["quality"]}))
        elif args.command == "validate-tiled-window":
            result = tiled.validate_run(args.directory)
            print(json.dumps({"status": "replay_passed", "access": result["module_details"]["access"], "quality": result["quality"]}))
        elif args.command in ("fetch-power-point", "fetch-power-window"):
            if args.output_dir.exists():
                raise PilotError("Output directory already exists; choose a new run directory.")
            config = loads(args.config.read_bytes())
            adapter_fetch, adapter_normalize = (regional.fetch, regional.normalize) if args.command == "fetch-power-window" else (fetch, normalize)
            raw, retrieved_at = adapter_fetch(config)
            result = adapter_normalize(raw, config, retrieved_at)
            args.output_dir.mkdir(parents=True, exist_ok=False)
            (args.output_dir / "response.json").write_bytes(raw)
            write_json(args.output_dir / "request.json", config)
            write_json(args.output_dir / "result.json", result)
            print(json.dumps({"output": str(args.output_dir), "quality": result["quality"]}, ensure_ascii=False))
        elif args.command == "validate-window":
            result = regional.validate_run(args.directory)
            print(json.dumps({"status": "replay_passed", "quality": result["quality"]}, ensure_ascii=False))
        elif args.command == "validate":
            validate_result(loads(args.input.read_bytes()))
            print("Monthly point-series contract and consistency checks passed.")
        else:
            report = compatibility(loads(args.left.read_bytes()), loads(args.right.read_bytes()))
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 2 if report["status"] == "incompatible" else 0
    except (PilotError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
