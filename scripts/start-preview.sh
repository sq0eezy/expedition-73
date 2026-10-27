#!/bin/sh
set -eu
CDPATH= cd -P "$(dirname "$0")/.."
if [ ! -x analysis/.venv/bin/python ]; then
    python3 scripts/workspace.py setup
fi
exec analysis/.venv/bin/python scripts/workspace.py preview "$@"
