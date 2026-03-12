@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Could not find .venv\Scripts\python.exe
    echo Make sure the project virtual environment exists.
    pause
    exit /b 1
)

echo Starting JupyterLab from %cd%
echo A browser tab should open to JupyterLab. Keep this window open while you use notebooks.
".venv\Scripts\python.exe" -m jupyter lab --ServerApp.open_browser=True
