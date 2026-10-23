from fastapi import FastAPI

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.archivers.file_archiver import (
    archive_processed_files,
)
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
def import_health_metrics(
    file_name: str | None = None,
):
    """
    Process Health Metrics Automation files.

    If file_name is provided, only that specific file
    will be processed. Otherwise, all files in the
    incoming folder will be processed.

    Each file may contain:
    - Health Metrics
    - Nutrition Metrics
    - Sleep Metrics
    - Body Measurements
    """

    results = process_health_metrics_files(
        file_name=file_name,
    )

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


@app.post("/health/archive")
def archive_health_files():
    """
    Archive successfully processed health data files.

    Only files marked with the PROCESSED_ prefix and
    older than the configured archive threshold are
    eligible for archival.
    """

    drive_client = GoogleDriveClient()

    health_metrics_archived = archive_processed_files(
        drive_client=drive_client,
        source_folder_id=(
            settings.HEALTH_METRICS_DRIVE_FOLDER_ID
        ),
        destination_folder_id=(
            settings.HEALTH_METRICS_PROCESSED_DRIVE_FOLDER_ID
        ),
        file_prefix="HealthMetrics-",
        file_suffix=".json",
        archive_after_days=(
            settings.DATA_IMPORTER_ARCHIVE_AFTER_DAYS
        ),
    )

    workout_metrics_archived = archive_processed_files(
        drive_client=drive_client,
        source_folder_id=(
            settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
        ),
        destination_folder_id=(
            settings.WORKOUT_METRICS_PROCESSED_DRIVE_FOLDER_ID
        ),
        file_prefix="WorkoutMetrics-",
        file_suffix=".json",
        archive_after_days=(
            settings.DATA_IMPORTER_ARCHIVE_AFTER_DAYS
        ),
    )

    return {
        "status": "success",
        "files_archived": (
            len(health_metrics_archived)
            + len(workout_metrics_archived)
        ),
        "health_metrics": {
            "files_archived": len(
                health_metrics_archived
            ),
            "files": health_metrics_archived,
        },
        "workout_metrics": {
            "files_archived": len(
                workout_metrics_archived
            ),
            "files": workout_metrics_archived,
        },
    }