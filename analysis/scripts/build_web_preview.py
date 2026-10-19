"""Replay recorded inputs and build only public static preview files."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from expedition73.power import PilotError  # noqa: E402
from expedition73.web_preview import build  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT.parent / "web/dist")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(build(ROOT, ROOT.parent / "web", args.output_dir)))
    except (PilotError, OSError) as exc:
        print("ERROR: " + (str(exc) if isinstance(exc, PilotError) else "Could not build the local preview."), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
