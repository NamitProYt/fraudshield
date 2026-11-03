#!/usr/bin/env bash
# FraudShield India - installer for macOS and Linux
cd "$(dirname "$0")" || exit 1
echo
echo " FraudShield India - installing on this computer"
echo " ------------------------------------------------"
PY="$(command -v python3 || command -v python)"
if [ -z "$PY" ]; then
  echo " Python 3 was not found."
  echo "  macOS : install it from https://www.python.org/downloads/"
  echo "  Ubuntu/Debian : sudo apt install python3 python3-venv python3-tk"
  echo " Then run this file again."
  exit 1
fi
if ! "$PY" -c "import tkinter" 2>/dev/null; then
  echo " tkinter (needed for the pop-up) is missing."
  echo "  macOS : install Python from https://www.python.org/downloads/ (it includes tkinter)"
  echo "  Ubuntu/Debian : sudo apt install python3-tk"
  exit 1
fi
"$PY" -m venv .venv || { echo " Could not create a virtual environment (try: sudo apt install python3-venv)."; exit 1; }
./.venv/bin/python -m pip install --upgrade . || { echo " Install failed. Take a screenshot of this window and send it to the team."; exit 1; }
echo
echo " Installed! Starting FraudShield Guardian."
echo " Copy any message to check it. Press Ctrl+C to stop."
echo
./.venv/bin/python -m fraudshield.cli watch
