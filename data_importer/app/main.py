from fastapi import FastAPI

from app.modules.health.orchestrators.health_metrics_orchestrator import (
    process_health_metrics_files,
)
from app.modules.health.orchestrators.workout_metrics_orchestrator import (
    process_workout_metrics_files,
)


app = FastAPI(
    title="Personal Assistant - Data Importer",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    """
    Simple health-check endpoint.

    This lets us verify that the Data Importer service
    is running and responding to HTTP requests.
    """

    return {"status": "ok"}


@app.put("/health/import/health-metrics")
def import_health_metrics():
    """
    Process all Health Metrics Automation files currently
    waiting in the Google Drive incoming folder.

    Each file may contain:
    - Health Metrics
    - Nutrition Metrics
    - Sleep Metrics
    """

    results = process_health_metrics_files()

    return {
        "status": "success",
        "files_processed": len(results),
        "results": results,
    }


@app.put("/health/import/workout-metrics")
def import_workout_metrics(
    file_name: str | None = None,
):
    """
    Process Workout Metrics Automation files.

    If file_name is provided, only that specific file
    will be processed. Otherwise, all files in the
    incoming folder will be processed.
    """

    results = process_workout_metrics_files(
        file_name=file_name,
    )

    return {
        "status": "success",
        "files_processed": len(results),
        "results": results,
    }