from datetime import date, timedelta
from unittest.mock import Mock

from app.modules.health.archivers.file_archiver import (
    archive_processed_files,
    get_file_date,
)


def test_get_file_date_returns_date_for_valid_filename():
    result = get_file_date(
        file_name="HealthMetrics-2026-10-12.json",
        file_prefix="HealthMetrics-",
        file_suffix=".json",
    )

    assert result == date(2026, 10, 12)


def test_get_file_date_returns_none_for_invalid_prefix():
    result = get_file_date(
        file_name="WorkoutMetrics-2026-10-12.json",
        file_prefix="HealthMetrics-",
        file_suffix=".json",
    )

    assert result is None


def test_get_file_date_returns_none_for_invalid_date():
    result = get_file_date(
        file_name="HealthMetrics-invalid.json",
        file_prefix="HealthMetrics-",
        file_suffix=".json",
    )

    assert result is None


def test_archive_processed_files_archives_old_processed_file():
    drive_client = Mock()

    old_date = (
        date.today()
        - timedelta(days=31)
    )

    file_name = (
        f"PROCESSED_HealthMetrics-"
        f"{old_date.isoformat()}.json"
    )

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": file_name,
        }
    ]

    result = archive_processed_files(
        drive_client=drive_client,
        source_folder_id="incoming-folder",
        destination_folder_id="archive-folder",
        file_prefix="HealthMetrics-",
        file_suffix=".json",
        archive_after_days=30,
    )

    drive_client.move_file.assert_called_once_with(
        file_id="file-1",
        source_folder_id="incoming-folder",
        destination_folder_id="archive-folder",
    )

    assert result == [file_name]


def test_archive_processed_files_does_not_archive_recent_processed_file():
    drive_client = Mock()

    recent_date = (
        date.today()
        - timedelta(days=10)
    )

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": (
                f"PROCESSED_HealthMetrics-"
                f"{recent_date.isoformat()}.json"
            ),
        }
    ]

    result = archive_processed_files(
        drive_client=drive_client,
        source_folder_id="incoming-folder",
        destination_folder_id="archive-folder",
        file_prefix="HealthMetrics-",
        file_suffix=".json",
        archive_after_days=30,
    )

    drive_client.move_file.assert_not_called()

    assert result == []


def test_archive_processed_files_does_not_archive_unprocessed_file():
    drive_client = Mock()

    old_date = (
        date.today()
        - timedelta(days=31)
    )

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": (
                f"HealthMetrics-"
                f"{old_date.isoformat()}.json"
            ),
        }
    ]

    result = archive_processed_files(
        drive_client=drive_client,
        source_folder_id="incoming-folder",
        destination_folder_id="archive-folder",
        file_prefix="HealthMetrics-",
        file_suffix=".json",
        archive_after_days=30,
    )

    drive_client.move_file.assert_not_called()

    assert result == []


def test_archive_processed_files_does_not_archive_failed_file():
    drive_client = Mock()

    old_date = (
        date.today()
        - timedelta(days=31)
    )

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": (
                f"FAILED_HealthMetrics-"
                f"{old_date.isoformat()}.json"
            ),
        }
    ]

    result = archive_processed_files(
        drive_client=drive_client,
        source_folder_id="incoming-folder",
        destination_folder_id="archive-folder",
        file_prefix="HealthMetrics-",
        file_suffix=".json",
        archive_after_days=30,
    )

    drive_client.move_file.assert_not_called()

    assert result == []


def test_archive_processed_files_ignores_unrecognized_processed_file():
    drive_client = Mock()

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": "PROCESSED_unknown-file.json",
        }
    ]

    result = archive_processed_files(
        drive_client=drive_client,
        source_folder_id="incoming-folder",
        destination_folder_id="archive-folder",
        file_prefix="HealthMetrics-",
        file_suffix=".json",
        archive_after_days=30,
    )

    drive_client.move_file.assert_not_called()

    assert result == []


def test_archive_processed_files_continues_when_move_fails():
    drive_client = Mock()

    old_date = (
        date.today()
        - timedelta(days=31)
    )

    file_name = (
        f"PROCESSED_HealthMetrics-"
        f"{old_date.isoformat()}.json"
    )

    drive_client.list_files.return_value = [
        {
            "id": "file-1",
            "name": file_name,
        }
    ]

    drive_client.move_file.side_effect = Exception(
        "Google Drive error"
    )

    result = archive_processed_files(
        drive_client=drive_client,
        source_folder_id="incoming-folder",
        destination_folder_id="archive-folder",
        file_prefix="HealthMetrics-",
        file_suffix=".json",
        archive_after_days=30,
    )

    assert result == []