"""Small A/B NASA subsets with local .env or hidden token; offline replay."""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from expedition73 import earthdata, surface_source  # noqa: E402
from expedition73.power import PilotError, loads  # noqa: E402


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", type=Path, help="Validate one saved region directory without any token/network.")
    parser.add_argument("--save-token", action="store_true", help="Enter a token hidden and save/replace only EARTHDATA_TOKEN in project .env.")
    args = parser.parse_args(argv)
    if args.replay and args.save_token:
        parser.error("--replay does not read or save credentials; omit --save-token.")
    try:
        if args.replay:
            result = surface_source.replay(args.replay)
            print(f"Surface conversion replay passed: {len(result['cells'])} cells. No scientific profile accepted.")
            return 0
        surface_source.dependencies()  # Check before asking for any credential.
        configs = [loads((ROOT / "examples" / f"{region}-window-2024.config.json").read_bytes()) for region in ("a", "b")]
        for config in configs:
            surface_source.request_url(config)
        output = ROOT / "artifacts" / ("surface-fractions-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
        if output.exists():
            raise PilotError("Output directory already exists; start a new run later.")
        token, stored = earthdata.get_token(env_path=ROOT.parent / ".env", save=args.save_token)
        if args.save_token:
            print("Token saved to local project .env (Git ignored).", flush=True)
        runs = []
        try:
            print("Checking NASA source metadata...", flush=True)
            metadata, _ = earthdata.probe(token)
            surface_source.metadata_spec(metadata)
            for config in configs:
                print(f"Requesting small candidate {config['region_id']} subset...", flush=True)
                raw, stamp = surface_source.fetch_subset(token, config)
                fractions = surface_source.convert(raw, metadata, config, stamp)
                runs.append((config, raw, fractions))
        finally:
            token = None
        # Do not save an incomplete A/B run, server error bodies or credentials.
        output.mkdir(parents=True, exist_ok=False)
        for config, raw, fractions in runs:
            directory = output / config["region_id"].lower()
            directory.mkdir()
            write_json(directory / "request.json", config)
            (directory / "response.nc4").write_bytes(raw)
            (directory / "metadata.dmr.xml").write_bytes(metadata)
            write_json(directory / "fractions.json", fractions)
            write_json(directory / "conversion-report.json", {
                "converter_version": surface_source.CONVERTER_VERSION,
                "metadata_sha256": hashlib.sha256(metadata).hexdigest(),
                "response_sha256": hashlib.sha256(raw).hexdigest(), "response_bytes": len(raw),
                "cells": len(fractions["cells"]), "credentials_persisted": stored,
                "status": "source_subset_converted", "scientific_profile_accepted": False,
                "scope": "coordinate_fill_fraction_checks_not_land_temperature_validation"})
            surface_source.replay(directory)
        print("NASA A/B surface subsets converted and replayed. No land/ice policy was selected.")
        print("Saved: analysis/artifacts/" + output.name)
    except (PilotError, OSError) as exc:
        message = str(exc) if isinstance(exc, PilotError) else "Could not read or write the local subset run."
        print("ERROR: " + message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
