#!/usr/bin/env bash
# Install Python dependencies for Whereisfire.py.
# Run from project root or from the verification directory.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

if [[ ! -f "$REQUIREMENTS" ]]; then
  echo "Error: requirements.txt not found at $REQUIREMENTS" >&2
  exit 1
fi

echo "Installing requirements from $REQUIREMENTS ..."
pip install -r "$REQUIREMENTS"
echo "Done."
