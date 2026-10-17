"""Run locally: hidden token input, one NASA metadata request, no saved token."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from expedition73.earthdata import probe, read_token  # noqa: E402
from expedition73.power import PilotError  # noqa: E402


def main():
    output = ROOT / "artifacts" / ("earthdata-access-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        token = read_token()
        try:
            raw, report = probe(token)
        finally:
            token = None  # No file, environment variable or command-line credential.
        output.mkdir(parents=True, exist_ok=False)
        (output / "metadata.dmr.xml").write_bytes(raw)
        (output / "access-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("NASA metadata access succeeded. No mask values have been fetched yet.")
        print("Saved: analysis/artifacts/" + output.name)
        print("Surface variables found: " + ", ".join(v["name"] for v in report["surface_variables_found"]))
    except (PilotError, OSError) as exc:
        if isinstance(exc, PilotError):
            print("ERROR: " + str(exc), file=sys.stderr)
        else:
            print("ERROR: Could not save metadata; choose a writable project directory.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
