"""Run from analysis/: python -m expedition73 --help."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .power import PilotError, compatibility, fetch, loads, normalize, validate_result
from . import regional


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    probe = commands.add_parser("fetch-power-point", help="Fetch and validate a small candidate point sample; no trend.")
    probe.add_argument("--config", type=Path, required=True)
    probe.add_argument("--output-dir", type=Path, required=True)
    window = commands.add_parser("fetch-power-window", help="Experimental unmasked rectangle means; no trend.")
    window.add_argument("--config", type=Path, required=True)
    window.add_argument("--output-dir", type=Path, required=True)
    replay = commands.add_parser("validate-window", help="Replay a complete window run offline, including geometry and weights.")
    replay.add_argument("directory", type=Path)
    validate = commands.add_parser("validate", help="Validate schema and monthly consistency offline.")
    validate.add_argument("input", type=Path)
    compare = commands.add_parser("check-alignment", help="Check point-series transport alignment; no inference.")
    compare.add_argument("left", type=Path)
    compare.add_argument("right", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command in ("fetch-power-point", "fetch-power-window"):
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
