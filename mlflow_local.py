from __future__ import annotations

import os
import sqlite3
import tempfile
from pathlib import Path

import mlflow


PROJECT_ROOT = Path(__file__).resolve().parent
RUNTIME_ROOT = PROJECT_ROOT / ".runtime"
TMP_DIR = RUNTIME_ROOT / "tmp"
MODEL_STAGING_DIR = RUNTIME_ROOT / "model_staging"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"
TRACKING_DB = PROJECT_ROOT / "mlflow.db"


def configure_runtime() -> None:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_STAGING_DIR.mkdir(parents=True, exist_ok=True)
    for env_var in ("TMP", "TEMP", "TMPDIR"):
        os.environ[env_var] = str(TMP_DIR)
    tempfile.tempdir = str(TMP_DIR)


def configure_tracking(experiment_name: str | None = None) -> None:
    MLRUNS_DIR.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(f"sqlite:///{TRACKING_DB.as_posix()}")
    repair_artifact_locations()
    if experiment_name:
        mlflow.set_experiment(experiment_name)


def repair_artifact_locations() -> None:
    expected_locations = {
        str(experiment_id): (MLRUNS_DIR / str(experiment_id)).resolve().as_uri()
        for experiment_id in _get_experiment_ids()
    }

    with sqlite3.connect(TRACKING_DB) as conn:
        updates = [
            (artifact_location, experiment_id)
            for experiment_id, artifact_location in expected_locations.items()
        ]
        conn.executemany(
            "UPDATE experiments SET artifact_location = ? WHERE experiment_id = ?",
            updates,
        )
        conn.commit()


def _get_experiment_ids() -> list[str]:
    with sqlite3.connect(TRACKING_DB) as conn:
        rows = conn.execute("SELECT experiment_id FROM experiments").fetchall()
    return [str(experiment_id) for (experiment_id,) in rows]
