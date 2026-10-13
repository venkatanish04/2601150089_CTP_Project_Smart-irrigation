#!/usr/bin/env bash

set -euo pipefail

PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Error: Python 3 was not found. Set PYTHON to a Python 3.12 executable." >&2
    exit 1
fi

if [ ! -d ".venv" ]; then
    "$PYTHON" -m venv .venv
fi

if [ -x ".venv/bin/python" ]; then
    VENV_PYTHON=".venv/bin/python"
else
    VENV_PYTHON=".venv/Scripts/python.exe"
fi

"$VENV_PYTHON" -m pip install -e ".[dev]"
"$VENV_PYTHON" -m app.main "$@"
