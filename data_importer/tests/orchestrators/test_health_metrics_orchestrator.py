from datetime import date
from unittest.mock import Mock, call, patch

from app.modules.health.orchestrators.health_metrics_orchestrator import (
    get_health_metrics_file_date,
    process_health_metrics_files,
)


def test_get_health_metrics_file_date():

    result = get_health_metrics_file_date(
        "HealthMetrics-2026-10-12.json"
    )

    assert result == date(2026, 10, 12)


def test_get_health_metrics_file_date_with_wrong_prefix():

    result = get_health_metrics_file_date(
        "WorkoutMetrics-2026-10-12.json"
    )

    assert result is None


def test_get_health_metrics_file_date_with_wrong_suffix():

    result = get_health_metrics_file_date(
        "HealthMetrics-2026-10-12.txt"
    )

    assert result is None


def test_get_health_metrics_file_date_with_invalid_date():

    result = get_health_metrics_file_date(
        "HealthMetrics-2026-99-99.json"
    )

    assert result is None


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_body_measurements_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_sleep_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_nutrition_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_health_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_success(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_health_metrics,
    mock_import_nutrition_metrics,
    mock_import_sleep_metrics,
    mock_import_body_measurements_metrics,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": "HealthMetrics-2026-10-12.json",
        }
    ]

    export_data = {
        "data": {
            "metrics": []
        }
    }

    drive_client.read_json_file.return_value = export_data

    health_result = {
        "date": "2026-10-12",
        "step_count": 4042,
    }

    nutrition_result = {
        "date": "2026-10-12",
        "protein_g": 111,
    }

    sleep_result = {
        "date": "2026-10-12",
        "total_sleep_duration_hr": 7.23,
    }

    body_measurements_result = {
        "date": "2026-10-12",
        "weight_kg": 80.5,
        "body_mass_index": 27.2,
        "body_fat_percent": 26.1,
    }

    mock_import_health_metrics.return_value = health_result
    mock_import_nutrition_metrics.return_value = nutrition_result
    mock_import_sleep_metrics.return_value = sleep_result
    mock_import_body_measurements_metrics.return_value = (
        body_measurements_result
    )

    results = process_health_metrics_files()

    drive_client.read_json_file.assert_called_once_with(
        "file-123"
    )

    mock_import_health_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    mock_import_nutrition_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    mock_import_sleep_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    mock_import_body_measurements_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name=(
            "PROCESSED_HealthMetrics-2026-10-12.json"
        ),
    )

    assert results == [
        {
            "file_name": "HealthMetrics-2026-10-12.json",
            "health_metrics": health_result,
            "nutrition_metrics": nutrition_result,
            "sleep_metrics": sleep_result,
            "body_measurements_metrics": body_measurements_result,
        }
    ]


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_body_measurements_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_sleep_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_nutrition_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_health_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_multiple_files(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_health_metrics,
    mock_import_nutrition_metrics,
    mock_import_sleep_metrics,
    mock_import_body_measurements_metrics,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "HealthMetrics-2026-10-11.json",
        },
        {
            "id": "file-2",
            "name": "HealthMetrics-2026-10-12.json",
        },
    ]

    first_export = {
        "data": {
            "metrics": []
        }
    }

    second_export = {
        "data": {
            "metrics": []
        }
    }

    drive_client.read_json_file.side_effect = [
        first_export,
        second_export,
    ]

    mock_import_health_metrics.side_effect = [
        {"date": "2026-10-11"},
        {"date": "2026-10-12"},
    ]

    mock_import_nutrition_metrics.side_effect = [
        {"date": "2026-10-11"},
        {"date": "2026-10-12"},
    ]

    mock_import_sleep_metrics.side_effect = [
        {"date": "2026-10-11"},
        {"date": "2026-10-12"},
    ]

    mock_import_body_measurements_metrics.side_effect = [
        {"date": "2026-10-11"},
        {"date": "2026-10-12"},
    ]

    results = process_health_metrics_files()

    assert drive_client.read_json_file.call_count == 2

    assert mock_import_health_metrics.call_count == 2
    assert mock_import_nutrition_metrics.call_count == 2
    assert mock_import_sleep_metrics.call_count == 2
    assert mock_import_body_measurements_metrics.call_count == 2

    assert len(results) == 2

    assert results[0]["file_name"] == (
        "HealthMetrics-2026-10-11.json"
    )

    assert results[1]["file_name"] == (
        "HealthMetrics-2026-10-12.json"
    )

    assert drive_client.rename_file.call_args_list == [
        call(
            file_id="file-1",
            new_name=(
                "PROCESSED_HealthMetrics-2026-10-11.json"
            ),
        ),
        call(
            file_id="file-2",
            new_name=(
                "PROCESSED_HealthMetrics-2026-10-12.json"
            ),
        ),
    ]


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_with_no_files(
    mock_drive_client_class,
    mock_backend_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = []

    results = process_health_metrics_files()

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_body_measurements_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_sleep_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_nutrition_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_health_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_marks_failed_file(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_health_metrics,
    mock_import_nutrition_metrics,
    mock_import_sleep_metrics,
    mock_import_body_measurements_metrics,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": "HealthMetrics-2026-10-12.json",
        }
    ]

    export_data = {
        "data": {
            "metrics": []
        }
    }

    drive_client.read_json_file.return_value = export_data

    mock_import_health_metrics.return_value = {
        "date": "2026-10-12"
    }

    mock_import_nutrition_metrics.side_effect = Exception(
        "Backend unavailable"
    )

    results = process_health_metrics_files()

    assert results == []

    mock_import_health_metrics.assert_called_once()
    mock_import_nutrition_metrics.assert_called_once()

    mock_import_sleep_metrics.assert_not_called()
    mock_import_body_measurements_metrics.assert_not_called()

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name="FAILED_HealthMetrics-2026-10-12.json",
    )


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_health_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_does_not_double_prefix_failed_file(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_health_metrics,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": (
                "FAILED_HealthMetrics-2026-10-12.json"
            ),
        }
    ]

    drive_client.read_json_file.return_value = {
        "data": {
            "metrics": []
        }
    }

    mock_import_health_metrics.side_effect = Exception(
        "Backend unavailable"
    )

    results = process_health_metrics_files()

    assert results == []

    drive_client.rename_file.assert_not_called()


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_body_measurements_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_sleep_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_nutrition_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_health_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_marks_failed_file_as_processed_after_success(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_health_metrics,
    mock_import_nutrition_metrics,
    mock_import_sleep_metrics,
    mock_import_body_measurements_metrics,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": (
                "FAILED_HealthMetrics-2026-10-12.json"
            ),
        }
    ]

    export_data = {
        "data": {
            "metrics": []
        }
    }

    drive_client.read_json_file.return_value = export_data

    mock_import_health_metrics.return_value = {
        "date": "2026-10-12"
    }

    mock_import_nutrition_metrics.return_value = {
        "date": "2026-10-12"
    }

    mock_import_sleep_metrics.return_value = {
        "date": "2026-10-12"
    }

    mock_import_body_measurements_metrics.return_value = {
        "date": "2026-10-12"
    }

    results = process_health_metrics_files()

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name=(
            "PROCESSED_HealthMetrics-2026-10-12.json"
        ),
    )

    assert len(results) == 1


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_health_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_continues_if_failed_rename_fails(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_health_metrics,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": "HealthMetrics-2026-10-12.json",
        }
    ]

    drive_client.read_json_file.return_value = {
        "data": {
            "metrics": []
        }
    }

    mock_import_health_metrics.side_effect = Exception(
        "Backend unavailable"
    )

    drive_client.rename_file.side_effect = Exception(
        "Google Drive rename failed"
    )

    results = process_health_metrics_files()

    assert results == []

    drive_client.rename_file.assert_called_once()


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_body_measurements_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_sleep_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_nutrition_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.import_health_metrics"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_with_specific_file_name(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_health_metrics,
    mock_import_nutrition_metrics,
    mock_import_sleep_metrics,
    mock_import_body_measurements_metrics,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "HealthMetrics-2026-10-11.json",
        },
        {
            "id": "file-2",
            "name": "HealthMetrics-2026-10-12.json",
        },
    ]

    export_data = {
        "data": {
            "metrics": []
        }
    }

    drive_client.read_json_file.return_value = export_data

    health_result = {
        "date": "2026-10-12"
    }

    nutrition_result = {
        "date": "2026-10-12"
    }

    sleep_result = {
        "date": "2026-10-12"
    }

    body_measurements_result = {
        "date": "2026-10-12"
    }

    mock_import_health_metrics.return_value = health_result
    mock_import_nutrition_metrics.return_value = nutrition_result
    mock_import_sleep_metrics.return_value = sleep_result
    mock_import_body_measurements_metrics.return_value = (
        body_measurements_result
    )

    results = process_health_metrics_files(
        file_name="HealthMetrics-2026-10-12.json"
    )

    drive_client.read_json_file.assert_called_once_with(
        "file-2"
    )

    mock_import_health_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    mock_import_nutrition_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    mock_import_sleep_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    mock_import_body_measurements_metrics.assert_called_once_with(
        export_data,
        backend_client,
    )

    drive_client.rename_file.assert_called_once_with(
        file_id="file-2",
        new_name=(
            "PROCESSED_HealthMetrics-2026-10-12.json"
        ),
    )

    assert results == [
        {
            "file_name": "HealthMetrics-2026-10-12.json",
            "health_metrics": health_result,
            "nutrition_metrics": nutrition_result,
            "sleep_metrics": sleep_result,
            "body_measurements_metrics": body_measurements_result,
        }
    ]


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_with_specific_file_name_not_found(
    mock_drive_client_class,
    mock_backend_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "HealthMetrics-2026-10-11.json",
        },
        {
            "id": "file-2",
            "name": "HealthMetrics-2026-10-12.json",
        },
    ]

    results = process_health_metrics_files(
        file_name="HealthMetrics-2026-10-13.json"
    )

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()


@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "health_metrics_orchestrator.GoogleDriveClient"
)
def test_process_health_metrics_files_skips_processed_files(
    mock_drive_client_class,
    mock_backend_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": (
                "PROCESSED_HealthMetrics-2026-10-12.json"
            ),
        }
    ]

    results = process_health_metrics_files()

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()