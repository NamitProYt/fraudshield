#!/usr/bin/env bash
# FraudShield Guardian - start on macOS and Linux (run install-mac-linux.sh first)
cd "$(dirname "$0")" || exit 1
if [ ! -x ./.venv/bin/python ]; then
  echo "Not installed yet. Run:  bash install-mac-linux.sh"
  exit 1
fi
echo "FraudShield Guardian is running. Copy any message to check it. Ctrl+C to stop."
./.venv/bin/python -m fraudshield.cli watch
