@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Could not find .venv\Scripts\python.exe
    echo Make sure the project virtual environment exists.
    pause
    exit /b 1
)

echo Starting MLflow UI from %cd%
echo A browser tab should open to the MLflow UI.
echo Keep this window open while you use the MLflow UI.
start "" "http://127.0.0.1:5000"
".venv\Scripts\python.exe" -m mlflow ui --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db
