"""Read-only checks; application functionality and remote links are not assessed."""
from pathlib import Path

from portal_core import check_content


def main() -> int:
    errors = check_content(Path(__file__).resolve().parents[1])
    for error in errors:
        print("ERROR:", error)
    if errors:
        print(f"{len(errors)} content error(s).")
        return 1
    print("Portal content checks passed (local links, state, navigation, tokens).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
