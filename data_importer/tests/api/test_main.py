from unittest.mock import call, patch

from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.modules.health.constants import (
    FILE_SUFFIX,
    HEALTH_METRICS_FILE_PREFIX,
    HEART_RATE_NOTIFICATIONS_FILE_PREFIX,
    WORKOUT_METRICS_FILE_PREFIX,
)


"""
Data Importer API Tests

These tests verify the HTTP endpoints in app/main.py.

The orchestrators, the archiver and the Google Drive client are
replaced with mocks, so no request reaches Google Drive or the
backend. The tests check that each endpoint calls the right
function with the right arguments and returns the right response.
"""


client = TestClient(app)


# Verify that the health-check endpoint reports the service is running.
def test_health_check_returns_ok():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Verify that importing without a file name processes every waiting file.
@patch("app.main.process_health_metrics_files")
def test_import_health_metrics_processes_all_waiting_files(
    mock_process_health_metrics_files,
):

    results = [
        {"file_name": "HealthMetrics-2026-10-11.json"},
        {"file_name": "HealthMetrics-2026-10-12.json"},
    ]

    mock_process_health_metrics_files.return_value = results

    response = client.put("/health/import/health-metrics")

    assert response.status_code == 200

    mock_process_health_metrics_files.assert_called_once_with(
        file_name=None,
    )

    assert response.json() == {
        "status": "success",
        "files_processed": 2,
        "results": results,
    }


# Verify that a file name in the query string is passed to the orchestrator.
@patch("app.main.process_health_metrics_files")
def test_import_health_metrics_with_specific_file_name(
    mock_process_health_metrics_files,
):

    results = [
        {"file_name": "HealthMetrics-2026-10-12.json"},
    ]

    mock_process_health_metrics_files.return_value = results

    response = client.put(
        "/health/import/health-metrics",
        params={"file_name": "HealthMetrics-2026-10-12.json"},
    )

    assert response.status_code == 200

    mock_process_health_metrics_files.assert_called_once_with(
        file_name="HealthMetrics-2026-10-12.json",
    )

    assert response.json() == {
        "status": "success",
        "files_processed": 1,
        "results": results,
    }


# Verify that importing without a file name processes every waiting file.
@patch("app.main.process_workout_metrics_files")
def test_import_workout_metrics_processes_all_waiting_files(
    mock_process_workout_metrics_files,
):

    results = [
        {"file_name": "WorkoutMetrics-2026-07-01.json"},
        {"file_name": "WorkoutMetrics-2026-07-02.json"},
    ]

    mock_process_workout_metrics_files.return_value = results

    response = client.put("/health/import/workout-metrics")

    assert response.status_code == 200

    mock_process_workout_metrics_files.assert_called_once_with(
        file_name=None,
    )

    assert response.json() == {
        "status": "success",
        "files_processed": 2,
        "results": results,
    }


# Verify that a file name in the query string is passed to the orchestrator.
@patch("app.main.process_workout_metrics_files")
def test_import_workout_metrics_with_specific_file_name(
    mock_process_workout_metrics_files,
):

    results = [
        {"file_name": "WorkoutMetrics-2026-07-02.json"},
    ]

    mock_process_workout_metrics_files.return_value = results

    response = client.put(
        "/health/import/workout-metrics",
        params={"file_name": "WorkoutMetrics-2026-07-02.json"},
    )

    assert response.status_code == 200

    mock_process_workout_metrics_files.assert_called_once_with(
        file_name="WorkoutMetrics-2026-07-02.json",
    )

    assert response.json() == {
        "status": "success",
        "files_processed": 1,
        "results": results,
    }


# Verify that importing without a file name processes every waiting file.
@patch("app.main.process_heart_rate_notifications_files")
def test_import_heart_rate_notifications_processes_all_waiting_files(
    mock_process_heart_rate_notifications_files,
):

    results = [
        {"file_name": "HeartRateNotifications-2026-10-28.json"},
        {"file_name": "HeartRateNotifications-2026-10-29.json"},
    ]

    mock_process_heart_rate_notifications_files.return_value = results

    response = client.put("/health/import/heart-rate-notifications")

    assert response.status_code == 200

    mock_process_heart_rate_notifications_files.assert_called_once_with(
        file_name=None,
    )

    assert response.json() == {
        "status": "success",
        "files_processed": 2,
        "results": results,
    }


# Verify that a file name in the query string is passed to the orchestrator.
@patch("app.main.process_heart_rate_notifications_files")
def test_import_heart_rate_notifications_with_specific_file_name(
    mock_process_heart_rate_notifications_files,
):

    results = [
        {"file_name": "HeartRateNotifications-2026-10-29.json"},
    ]

    mock_process_heart_rate_notifications_files.return_value = results

    response = client.put(
        "/health/import/heart-rate-notifications",
        params={"file_name": "HeartRateNotifications-2026-10-29.json"},
    )

    assert response.status_code == 200

    mock_process_heart_rate_notifications_files.assert_called_once_with(
        file_name="HeartRateNotifications-2026-10-29.json",
    )

    assert response.json() == {
        "status": "success",
        "files_processed": 1,
        "results": results,
    }


# Verify that archiving runs for all three folders with the right settings
# and returns the combined and per-folder results.
@patch("app.main.archive_processed_files")
@patch("app.main.GoogleDriveClient")
def test_archive_archives_all_folders(
    mock_drive_client_class,
    mock_archive_processed_files,
):

    drive_client = mock_drive_client_class.return_value

    health_archived = [
        "PROCESSED_HealthMetrics-2026-01-01.json",
    ]

    workout_archived = [
        "PROCESSED_WorkoutMetrics-2026-01-01.json",
        "PROCESSED_WorkoutMetrics-2026-01-02.json",
    ]

    notifications_archived = [
        "PROCESSED_HeartRateNotifications-2026-01-01.json",
    ]

    # The calls archive Health Metrics, Workout Metrics, then Heart Rate
    # Notifications.
    mock_archive_processed_files.side_effect = [
        health_archived,
        workout_archived,
        notifications_archived,
    ]

    response = client.post("/health/archive")

    assert response.status_code == 200

    assert mock_archive_processed_files.call_args_list == [
        call(
            drive_client=drive_client,
            source_folder_id=settings.HEALTH_METRICS_DRIVE_FOLDER_ID,
            destination_folder_id=(
                settings.HEALTH_METRICS_PROCESSED_DRIVE_FOLDER_ID
            ),
            file_prefix=HEALTH_METRICS_FILE_PREFIX,
            file_suffix=FILE_SUFFIX,
            archive_after_days=settings.DATA_IMPORTER_ARCHIVE_AFTER_DAYS,
        ),
        call(
            drive_client=drive_client,
            source_folder_id=settings.WORKOUT_METRICS_DRIVE_FOLDER_ID,
            destination_folder_id=(
                settings.WORKOUT_METRICS_PROCESSED_DRIVE_FOLDER_ID
            ),
            file_prefix=WORKOUT_METRICS_FILE_PREFIX,
            file_suffix=FILE_SUFFIX,
            archive_after_days=settings.DATA_IMPORTER_ARCHIVE_AFTER_DAYS,
        ),
        call(
            drive_client=drive_client,
            source_folder_id=(
                settings.HEART_RATE_NOTIFICATIONS_DRIVE_FOLDER_ID
            ),
            destination_folder_id=(
                settings.HEART_RATE_NOTIFICATIONS_PROCESSED_DRIVE_FOLDER_ID
            ),
            file_prefix=HEART_RATE_NOTIFICATIONS_FILE_PREFIX,
            file_suffix=FILE_SUFFIX,
            archive_after_days=settings.DATA_IMPORTER_ARCHIVE_AFTER_DAYS,
        ),
    ]

    assert response.json() == {
        "status": "success",
        "files_archived": 4,
        "health_metrics": {
            "files_archived": 1,
            "files": health_archived,
        },
        "workout_metrics": {
            "files_archived": 2,
            "files": workout_archived,
        },
        "heart_rate_notifications": {
            "files_archived": 1,
            "files": notifications_archived,
        },
    }
