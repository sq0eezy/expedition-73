@echo off
setlocal
cd /d "%~dp0.."
if not exist "analysis\.venv\Scripts\python.exe" (
    py -3 scripts\workspace.py setup
    if errorlevel 1 exit /b 1
)
analysis\.venv\Scripts\python.exe scripts\workspace.py preview %*
