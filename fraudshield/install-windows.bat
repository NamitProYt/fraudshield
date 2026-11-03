@echo off
title FraudShield India - Installer
cd /d "%~dp0"
echo.
echo  FraudShield India - installing on this computer
echo  ------------------------------------------------
set PY=
py --version >nul 2>nul && set PY=py
if not defined PY (
  python --version >nul 2>nul && set PY=python
)
if not defined PY (
  echo.
  echo  Python was not found on this computer.
  echo  Opening the Python download page now.
  echo  IMPORTANT: on the first screen of the installer, tick "Add python.exe to PATH".
  echo  After Python is installed, double-click this file again.
  start https://www.python.org/downloads/
  echo.
  pause
  exit /b 1
)
echo  Using: %PY%
%PY% -m pip install --upgrade .
if errorlevel 1 (
  echo.
  echo  Install failed. Take a screenshot of this window and send it to the team.
  pause
  exit /b 1
)
echo.
echo  Installed! Starting FraudShield Guardian.
echo  Copy any message to check it. Close this window to stop.
echo.
%PY% -m fraudshield.cli watch
pause
