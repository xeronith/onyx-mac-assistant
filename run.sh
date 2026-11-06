#!/usr/bin/env bash
# Onyx: On-Device macOS Assistant Runner
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Enforce 100% offline air-gapped environment
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

# Onyx Model & Engine Paths
export ONYX_MODEL_PATH="${ONYX_MODEL_PATH:-$SCRIPT_DIR/models/onyx-core.bin}"
export ONYX_LIB_PATH="${ONYX_LIB_PATH:-$SCRIPT_DIR/models/libonyx.dylib}"

# Check virtual environment
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Virtual environment not found. Setting up..."
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
fi

# Run Onyx
exec "$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/agent.py" "$@"
