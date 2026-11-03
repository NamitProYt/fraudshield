@echo off
title FraudShield Guardian
set PY=
py --version >nul 2>nul && set PY=py
if not defined PY (
  python --version >nul 2>nul && set PY=python
)
if not defined PY (
  echo Python was not found. Run install-windows.bat first.
  pause
  exit /b 1
)
echo FraudShield Guardian is running. Copy any message to check it.
%PY% -m fraudshield.cli watch
pause
