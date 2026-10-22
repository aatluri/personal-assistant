from datetime import date
from unittest.mock import Mock, patch

from app.modules.health.orchestrators.workout_metrics_orchestrator import (
    archive_old_workout_metrics_files,
    get_workout_metrics_file_date,
    process_workout_metrics_files,
)


# ---------------------------------------------------------
# Filename parsing
# ---------------------------------------------------------


def test_get_workout_metrics_file_date():

    result = get_workout_metrics_file_date(
        "WorkoutMetrics-2026-07-02.json"
    )

    assert result == date(2026, 7, 2)


def test_get_workout_metrics_file_date_with_wrong_prefix():

    result = get_workout_metrics_file_date(
        "HealthMetrics-2026-07-02.json"
    )

    assert result is None


def test_get_workout_metrics_file_date_with_wrong_suffix():

    result = get_workout_metrics_file_date(
        "WorkoutMetrics-2026-07-02.txt"
    )

    assert result is None


def test_get_workout_metrics_file_date_with_invalid_date():

    result = get_workout_metrics_file_date(
        "WorkoutMetrics-2026-99-99.json"
    )

    assert result is None


# ---------------------------------------------------------
# Successful processing
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.archive_old_workout_metrics_files"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.import_workout_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
def test_process_workout_metrics_files_success(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_workout_metrics,
    mock_archive,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": "WorkoutMetrics-2026-07-02.json",
        }
    ]

    export_data = {
        "data": {
            "workouts": [
                {
                    "name": "Outdoor Run",
                }
            ]
        }
    }

    drive_client.read_json_file.return_value = export_data

    workout_results = [
        {
            "workout_type": "Outdoor Run",
        }
    ]

    mock_import_workout_metrics.return_value = workout_results

    results = process_workout_metrics_files()

    drive_client.list_files.assert_called_once()

    drive_client.read_json_file.assert_called_once_with(
        "file-123"
    )

    mock_import_workout_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    drive_client.rename_file.assert_not_called()

    assert results == [
        {
            "file_name": "WorkoutMetrics-2026-07-02.json",
            "workout_metrics": workout_results,
        }
    ]

    mock_archive.assert_called_once_with(
        drive_client=drive_client,
    )


# ---------------------------------------------------------
# Multiple files
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.archive_old_workout_metrics_files"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.import_workout_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
def test_process_workout_metrics_files_multiple_files(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_workout_metrics,
    mock_archive,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "WorkoutMetrics-2026-07-01.json",
        },
        {
            "id": "file-2",
            "name": "WorkoutMetrics-2026-07-02.json",
        },
    ]

    first_export = {
        "data": {
            "workouts": [
                {"name": "Indoor Walk"}
            ]
        }
    }

    second_export = {
        "data": {
            "workouts": [
                {"name": "Outdoor Run"}
            ]
        }
    }

    drive_client.read_json_file.side_effect = [
        first_export,
        second_export,
    ]

    mock_import_workout_metrics.side_effect = [
        [{"workout_type": "Indoor Walk"}],
        [{"workout_type": "Outdoor Run"}],
    ]

    results = process_workout_metrics_files()

    assert drive_client.read_json_file.call_count == 2
    assert mock_import_workout_metrics.call_count == 2

    assert len(results) == 2

    assert results[0]["file_name"] == (
        "WorkoutMetrics-2026-07-01.json"
    )

    assert results[1]["file_name"] == (
        "WorkoutMetrics-2026-07-02.json"
    )

    mock_archive.assert_called_once_with(
        drive_client=drive_client,
    )


# ---------------------------------------------------------
# No files
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
def test_process_workout_metrics_files_with_no_files(
    mock_backend_client_class,
    mock_drive_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = []

    results = process_workout_metrics_files()

    assert results == []

    drive_client.read_json_file.assert_not_called()


# ---------------------------------------------------------
# Failed import
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.archive_old_workout_metrics_files"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.import_workout_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
def test_process_workout_metrics_files_marks_failed_file(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_workout_metrics,
    mock_archive,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": "WorkoutMetrics-2026-07-02.json",
        }
    ]

    export_data = {
        "data": {
            "workouts": []
        }
    }

    drive_client.read_json_file.return_value = export_data

    mock_import_workout_metrics.side_effect = Exception(
        "Backend unavailable"
    )

    results = process_workout_metrics_files()

    assert results == []

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name="FAILED_WorkoutMetrics-2026-07-02.json",
    )

    mock_archive.assert_called_once_with(
        drive_client=drive_client,
    )


# ---------------------------------------------------------
# Already failed file
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.archive_old_workout_metrics_files"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.import_workout_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
def test_process_workout_metrics_files_does_not_double_prefix_failed_file(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_workout_metrics,
    mock_archive,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": (
                "FAILED_WorkoutMetrics-2026-07-02.json"
            ),
        }
    ]

    drive_client.read_json_file.return_value = {
        "data": {
            "workouts": []
        }
    }

    mock_import_workout_metrics.side_effect = Exception(
        "Backend unavailable"
    )

    results = process_workout_metrics_files()

    assert results == []

    drive_client.rename_file.assert_not_called()

    mock_archive.assert_called_once_with(
        drive_client=drive_client,
    )


# ---------------------------------------------------------
# Successful retry
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.archive_old_workout_metrics_files"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.import_workout_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
def test_process_workout_metrics_files_restores_failed_filename_after_success(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_workout_metrics,
    mock_archive,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": (
                "FAILED_WorkoutMetrics-2026-07-02.json"
            ),
        }
    ]

    export_data = {
        "data": {
            "workouts": [
                {
                    "name": "Outdoor Run",
                }
            ]
        }
    }

    drive_client.read_json_file.return_value = export_data

    mock_import_workout_metrics.return_value = [
        {
            "workout_type": "Outdoor Run",
        }
    ]

    results = process_workout_metrics_files()

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name="WorkoutMetrics-2026-07-02.json",
    )

    assert len(results) == 1

    mock_archive.assert_called_once_with(
        drive_client=drive_client,
    )


# ---------------------------------------------------------
# Rename failure
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.archive_old_workout_metrics_files"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.import_workout_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
def test_process_workout_metrics_files_continues_if_failed_rename_fails(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_workout_metrics,
    mock_archive,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": "WorkoutMetrics-2026-07-02.json",
        }
    ]

    drive_client.read_json_file.return_value = {
        "data": {
            "workouts": []
        }
    }

    mock_import_workout_metrics.side_effect = Exception(
        "Backend unavailable"
    )

    drive_client.rename_file.side_effect = Exception(
        "Google Drive rename failed"
    )

    results = process_workout_metrics_files()

    assert results == []

    drive_client.rename_file.assert_called_once()

    mock_archive.assert_called_once_with(
        drive_client=drive_client,
    )


# ---------------------------------------------------------
# Archive old files
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.date"
)
def test_archive_old_workout_metrics_files(
    mock_date,
):

    mock_date.today.return_value = date(
        2026,
        10,
        22,
    )

    drive_client = Mock()

    drive_client.list_files.return_value = [
        {
            "id": "old-file",
            "name": "WorkoutMetrics-2026-09-01.json",
        },
        {
            "id": "recent-file",
            "name": "WorkoutMetrics-2026-10-20.json",
        },
        {
            "id": "failed-file",
            "name": (
                "FAILED_WorkoutMetrics-2026-09-01.json"
            ),
        },
        {
            "id": "unknown-file",
            "name": "SomethingElse.json",
        },
    ]

    archive_old_workout_metrics_files(
        drive_client=drive_client,
    )

    drive_client.move_file.assert_called_once()

    call = drive_client.move_file.call_args

    assert call.kwargs["file_id"] == "old-file"


# ---------------------------------------------------------
# Recent file not archived
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.date"
)
def test_archive_recent_workout_metrics_file_is_not_moved(
    mock_date,
):

    mock_date.today.return_value = date(
        2026,
        10,
        22,
    )

    drive_client = Mock()

    drive_client.list_files.return_value = [
        {
            "id": "recent-file",
            "name": "WorkoutMetrics-2026-10-20.json",
        }
    ]

    archive_old_workout_metrics_files(
        drive_client=drive_client,
    )

    drive_client.move_file.assert_not_called()


# ---------------------------------------------------------
# Failed file not archived
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.date"
)
def test_archive_failed_workout_metrics_file_is_not_moved(
    mock_date,
):

    mock_date.today.return_value = date(
        2026,
        10,
        22,
    )

    drive_client = Mock()

    drive_client.list_files.return_value = [
        {
            "id": "failed-file",
            "name": (
                "FAILED_WorkoutMetrics-2026-01-01.json"
            ),
        }
    ]

    archive_old_workout_metrics_files(
        drive_client=drive_client,
    )

    drive_client.move_file.assert_not_called()


# ---------------------------------------------------------
# Invalid filename not archived
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.date"
)
def test_archive_invalid_workout_metrics_filename_is_not_moved(
    mock_date,
):

    mock_date.today.return_value = date(
        2026,
        10,
        22,
    )

    drive_client = Mock()

    drive_client.list_files.return_value = [
        {
            "id": "unknown-file",
            "name": "RandomFile.json",
        }
    ]

    archive_old_workout_metrics_files(
        drive_client=drive_client,
    )

    drive_client.move_file.assert_not_called()


# ---------------------------------------------------------
# Archive move failure
# ---------------------------------------------------------


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.date"
)
def test_archive_old_workout_metrics_file_move_failure_does_not_crash(
    mock_date,
):

    mock_date.today.return_value = date(
        2026,
        10,
        22,
    )

    drive_client = Mock()

    drive_client.list_files.return_value = [
        {
            "id": "old-file",
            "name": "WorkoutMetrics-2026-01-01.json",
        }
    ]

    drive_client.move_file.side_effect = Exception(
        "Google Drive move failed"
    )

    # The archive function should catch the Drive error
    # instead of allowing it to crash the orchestrator.
    archive_old_workout_metrics_files(
        drive_client=drive_client,
    )

    drive_client.move_file.assert_called_once()