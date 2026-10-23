from datetime import date
from unittest.mock import Mock, call, patch

from app.modules.health.orchestrators.workout_metrics_orchestrator import (
    get_workout_metrics_file_date,
    process_workout_metrics_files,
)


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

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name="PROCESSED_WorkoutMetrics-2026-07-02.json",
    )

    assert results == [
        {
            "file_name": "WorkoutMetrics-2026-07-02.json",
            "workout_metrics": workout_results,
        }
    ]


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

    assert drive_client.rename_file.call_args_list == [
        call(
            file_id="file-1",
            new_name=(
                "PROCESSED_WorkoutMetrics-2026-07-01.json"
            ),
        ),
        call(
            file_id="file-2",
            new_name=(
                "PROCESSED_WorkoutMetrics-2026-07-02.json"
            ),
        ),
    ]


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
def test_process_workout_metrics_files_with_no_files(
    mock_drive_client_class,
    mock_backend_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = []

    results = process_workout_metrics_files()

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()


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

    mock_import_workout_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name="FAILED_WorkoutMetrics-2026-07-02.json",
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
def test_process_workout_metrics_files_marks_failed_file_as_processed_after_success(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_workout_metrics,
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
        new_name=(
            "PROCESSED_WorkoutMetrics-2026-07-02.json"
        ),
    )

    assert len(results) == 1


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


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
def test_process_workout_metrics_files_skips_processed_files(
    mock_drive_client_class,
    mock_backend_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": (
                "PROCESSED_WorkoutMetrics-2026-07-02.json"
            ),
        }
    ]

    results = process_workout_metrics_files()

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()


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
def test_process_workout_metrics_files_with_specific_file_name(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_workout_metrics,
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

    results = process_workout_metrics_files(
        file_name="WorkoutMetrics-2026-07-02.json"
    )

    drive_client.read_json_file.assert_called_once_with(
        "file-2"
    )

    mock_import_workout_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    drive_client.rename_file.assert_called_once_with(
        file_id="file-2",
        new_name=(
            "PROCESSED_WorkoutMetrics-2026-07-02.json"
        ),
    )

    assert results == [
        {
            "file_name": "WorkoutMetrics-2026-07-02.json",
            "workout_metrics": workout_results,
        }
    ]


@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "workout_metrics_orchestrator.GoogleDriveClient"
)
def test_process_workout_metrics_files_with_specific_file_name_not_found(
    mock_drive_client_class,
    mock_backend_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

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

    results = process_workout_metrics_files(
        file_name="WorkoutMetrics-2026-07-03.json"
    )

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()