from datetime import date
from unittest.mock import Mock, call, patch

from app.modules.health.orchestrators.heart_rate_notifications_orchestrator import (
    get_heart_rate_notifications_file_date,
    process_heart_rate_notifications_files,
)


def test_get_heart_rate_notifications_file_date():

    result = get_heart_rate_notifications_file_date(
        "HeartRateNotifications-2026-07-02.json"
    )

    assert result == date(2026, 7, 2)


def test_get_heart_rate_notifications_file_date_with_wrong_prefix():

    result = get_heart_rate_notifications_file_date(
        "HealthMetrics-2026-07-02.json"
    )

    assert result is None


def test_get_heart_rate_notifications_file_date_with_wrong_suffix():

    result = get_heart_rate_notifications_file_date(
        "HeartRateNotifications-2026-07-02.txt"
    )

    assert result is None


def test_get_heart_rate_notifications_file_date_with_invalid_date():

    result = get_heart_rate_notifications_file_date(
        "HeartRateNotifications-2026-99-99.json"
    )

    assert result is None


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.import_heart_rate_notifications"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_success(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_heart_rate_notifications,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": "HeartRateNotifications-2026-07-02.json",
        }
    ]

    export_data = {
        "data": {
            "heartRateNotifications": [
                {
                    "heartNotification": "low_heart_rate_notification",
                }
            ]
        }
    }

    drive_client.read_json_file.return_value = export_data

    notification_results = [
        {
            "notification_type": "Low Heart Rate",
        }
    ]

    mock_import_heart_rate_notifications.return_value = notification_results

    results = process_heart_rate_notifications_files()

    drive_client.list_files.assert_called_once()

    drive_client.read_json_file.assert_called_once_with(
        "file-123"
    )

    mock_import_heart_rate_notifications.assert_called_once_with(
        export_data,
        backend_client,
    )

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name="PROCESSED_HeartRateNotifications-2026-07-02.json",
    )

    assert results == [
        {
            "file_name": "HeartRateNotifications-2026-07-02.json",
            "heart_rate_notifications": notification_results,
        }
    ]


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.import_heart_rate_notifications"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_multiple_files(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_heart_rate_notifications,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "HeartRateNotifications-2026-07-01.json",
        },
        {
            "id": "file-2",
            "name": "HeartRateNotifications-2026-07-02.json",
        },
    ]

    first_export = {
        "data": {
            "heartRateNotifications": [
                {"heartNotification": "high_heart_rate_notification"}
            ]
        }
    }

    second_export = {
        "data": {
            "heartRateNotifications": [
                {"heartNotification": "low_heart_rate_notification"}
            ]
        }
    }

    drive_client.read_json_file.side_effect = [
        first_export,
        second_export,
    ]

    mock_import_heart_rate_notifications.side_effect = [
        [{"notification_type": "High Heart Rate"}],
        [{"notification_type": "Low Heart Rate"}],
    ]

    results = process_heart_rate_notifications_files()

    assert drive_client.read_json_file.call_count == 2
    assert mock_import_heart_rate_notifications.call_count == 2

    assert len(results) == 2

    assert results[0]["file_name"] == (
        "HeartRateNotifications-2026-07-01.json"
    )

    assert results[1]["file_name"] == (
        "HeartRateNotifications-2026-07-02.json"
    )

    assert drive_client.rename_file.call_args_list == [
        call(
            file_id="file-1",
            new_name=(
                "PROCESSED_HeartRateNotifications-2026-07-01.json"
            ),
        ),
        call(
            file_id="file-2",
            new_name=(
                "PROCESSED_HeartRateNotifications-2026-07-02.json"
            ),
        ),
    ]


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_with_no_files(
    mock_drive_client_class,
    mock_backend_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = []

    results = process_heart_rate_notifications_files()

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.import_heart_rate_notifications"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_marks_failed_file(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_heart_rate_notifications,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": "HeartRateNotifications-2026-07-02.json",
        }
    ]

    export_data = {
        "data": {
            "heartRateNotifications": []
        }
    }

    drive_client.read_json_file.return_value = export_data

    mock_import_heart_rate_notifications.side_effect = Exception(
        "Backend unavailable"
    )

    results = process_heart_rate_notifications_files()

    assert results == []

    mock_import_heart_rate_notifications.assert_called_once_with(
        export_data,
        backend_client,
    )

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name="FAILED_HeartRateNotifications-2026-07-02.json",
    )


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.import_heart_rate_notifications"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_does_not_double_prefix_failed_file(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_heart_rate_notifications,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": (
                "FAILED_HeartRateNotifications-2026-07-02.json"
            ),
        }
    ]

    drive_client.read_json_file.return_value = {
        "data": {
            "heartRateNotifications": []
        }
    }

    mock_import_heart_rate_notifications.side_effect = Exception(
        "Backend unavailable"
    )

    results = process_heart_rate_notifications_files()

    assert results == []

    drive_client.rename_file.assert_not_called()


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.import_heart_rate_notifications"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_marks_failed_file_as_processed_after_success(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_heart_rate_notifications,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": (
                "FAILED_HeartRateNotifications-2026-07-02.json"
            ),
        }
    ]

    export_data = {
        "data": {
            "heartRateNotifications": [
                {
                    "heartNotification": "low_heart_rate_notification",
                }
            ]
        }
    }

    drive_client.read_json_file.return_value = export_data

    mock_import_heart_rate_notifications.return_value = [
        {
            "notification_type": "Low Heart Rate",
        }
    ]

    results = process_heart_rate_notifications_files()

    drive_client.rename_file.assert_called_once_with(
        file_id="file-123",
        new_name=(
            "PROCESSED_HeartRateNotifications-2026-07-02.json"
        ),
    )

    assert len(results) == 1


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.import_heart_rate_notifications"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_continues_if_failed_rename_fails(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_heart_rate_notifications,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": "HeartRateNotifications-2026-07-02.json",
        }
    ]

    drive_client.read_json_file.return_value = {
        "data": {
            "heartRateNotifications": []
        }
    }

    mock_import_heart_rate_notifications.side_effect = Exception(
        "Backend unavailable"
    )

    drive_client.rename_file.side_effect = Exception(
        "Google Drive rename failed"
    )

    results = process_heart_rate_notifications_files()

    assert results == []

    drive_client.rename_file.assert_called_once()


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_skips_processed_files(
    mock_drive_client_class,
    mock_backend_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = [
        {
            "id": "file-123",
            "name": (
                "PROCESSED_HeartRateNotifications-2026-07-02.json"
            ),
        }
    ]

    results = process_heart_rate_notifications_files()

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.import_heart_rate_notifications"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_with_specific_file_name(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_heart_rate_notifications,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "HeartRateNotifications-2026-07-01.json",
        },
        {
            "id": "file-2",
            "name": "HeartRateNotifications-2026-07-02.json",
        },
    ]

    export_data = {
        "data": {
            "heartRateNotifications": [
                {
                    "heartNotification": "low_heart_rate_notification",
                }
            ]
        }
    }

    drive_client.read_json_file.return_value = export_data

    notification_results = [
        {
            "notification_type": "Low Heart Rate",
        }
    ]

    mock_import_heart_rate_notifications.return_value = notification_results

    results = process_heart_rate_notifications_files(
        file_name="HeartRateNotifications-2026-07-02.json"
    )

    drive_client.read_json_file.assert_called_once_with(
        "file-2"
    )

    mock_import_heart_rate_notifications.assert_called_once_with(
        export_data,
        backend_client,
    )

    drive_client.rename_file.assert_called_once_with(
        file_id="file-2",
        new_name=(
            "PROCESSED_HeartRateNotifications-2026-07-02.json"
        ),
    )

    assert results == [
        {
            "file_name": "HeartRateNotifications-2026-07-02.json",
            "heart_rate_notifications": notification_results,
        }
    ]


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_with_specific_file_name_not_found(
    mock_drive_client_class,
    mock_backend_client_class,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "HeartRateNotifications-2026-07-01.json",
        },
        {
            "id": "file-2",
            "name": "HeartRateNotifications-2026-07-02.json",
        },
    ]

    results = process_heart_rate_notifications_files(
        file_name="HeartRateNotifications-2026-07-03.json"
    )

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()

@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.import_heart_rate_notifications"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_skips_unrecognised_files(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_heart_rate_notifications,
):

    drive_client = Mock()
    backend_client = Mock()

    mock_drive_client_class.return_value = drive_client
    mock_backend_client_class.return_value = backend_client

    # Only file-4 matches HeartRateNotifications-YYYY-MM-DD.json. The others
    # (a TEST_ fixture, a Drive duplicate and a stray file) must be
    # skipped and never imported.
    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "TEST_HeartRateNotifications-2099-01-01.json",
        },
        {
            "id": "file-2",
            "name": "HeartRateNotifications-2026-07-02 (1).json",
        },
        {
            "id": "file-3",
            "name": "notes.txt",
        },
        {
            "id": "file-4",
            "name": "HeartRateNotifications-2026-07-02.json",
        },
    ]

    export_data = {
        "data": {
            "heartRateNotifications": []
        }
    }

    drive_client.read_json_file.return_value = export_data

    mock_import_heart_rate_notifications.return_value = []

    results = process_heart_rate_notifications_files()

    # Only the recognised file is read, imported and renamed.
    drive_client.read_json_file.assert_called_once_with(
        "file-4"
    )

    mock_import_heart_rate_notifications.assert_called_once_with(
        export_data,
        backend_client,
    )

    drive_client.rename_file.assert_called_once_with(
        file_id="file-4",
        new_name="PROCESSED_HeartRateNotifications-2026-07-02.json",
    )

    assert [result["file_name"] for result in results] == [
        "HeartRateNotifications-2026-07-02.json",
    ]


@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.import_heart_rate_notifications"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.BackendClient"
)
@patch(
    "app.modules.health.orchestrators."
    "heart_rate_notifications_orchestrator.GoogleDriveClient"
)
def test_process_heart_rate_notifications_files_does_not_import_requested_unrecognised_file(
    mock_drive_client_class,
    mock_backend_client_class,
    mock_import_heart_rate_notifications,
):

    drive_client = Mock()

    mock_drive_client_class.return_value = drive_client

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "TEST_HeartRateNotifications-2099-01-01.json",
        },
    ]

    # Requesting an unrecognised file by name must not import it either.
    results = process_heart_rate_notifications_files(
        file_name="TEST_HeartRateNotifications-2099-01-01.json"
    )

    assert results == []

    drive_client.read_json_file.assert_not_called()
    drive_client.rename_file.assert_not_called()
    mock_import_heart_rate_notifications.assert_not_called()
