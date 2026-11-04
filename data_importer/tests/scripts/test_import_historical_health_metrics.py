from datetime import date
from unittest.mock import call, patch

from app.config import settings
from scripts.import_historical_health_metrics import (
    BATCH_DELAY_SECONDS,
    get_health_metrics_file_date,
    get_historical_health_metrics_files,
    import_historical_health_metrics,
)


SCRIPT = "scripts.import_historical_health_metrics"


# ============================================================================
# get_health_metrics_file_date
# ============================================================================


def test_get_health_metrics_file_date_returns_date_for_valid_file():

    assert get_health_metrics_file_date(
        "HealthMetrics-2026-10-12.json"
    ) == date(2026, 10, 12)


def test_get_health_metrics_file_date_accepts_failed_file_for_retry():

    assert get_health_metrics_file_date(
        "FAILED_HealthMetrics-2026-10-12.json"
    ) == date(2026, 10, 12)


def test_get_health_metrics_file_date_ignores_processed_file():

    assert get_health_metrics_file_date(
        "PROCESSED_HealthMetrics-2026-10-12.json"
    ) is None


def test_get_health_metrics_file_date_ignores_test_file():

    assert get_health_metrics_file_date(
        "TEST_HealthMetrics-2099-01-01.json"
    ) is None


def test_get_health_metrics_file_date_ignores_unrecognised_names():

    assert get_health_metrics_file_date(
        "WorkoutMetrics-2026-10-12.json"
    ) is None

    assert get_health_metrics_file_date(
        "HealthMetrics-2026-10-12 (1).json"
    ) is None

    assert get_health_metrics_file_date(
        "HealthMetrics-2026-99-99.json"
    ) is None


# ============================================================================
# get_historical_health_metrics_files
# ============================================================================


# Verify that only eligible files are returned, sorted oldest first.
@patch(f"{SCRIPT}.GoogleDriveClient")
def test_get_historical_health_metrics_files_filters_and_sorts(
    mock_drive_client_class,
):

    drive_client = mock_drive_client_class.return_value

    drive_client.list_files.return_value = [
        {"id": "file-1", "name": "HealthMetrics-2026-10-12.json"},
        {"id": "file-2", "name": "PROCESSED_HealthMetrics-2026-10-01.json"},
        {"id": "file-3", "name": "FAILED_HealthMetrics-2026-10-05.json"},
        {"id": "file-4", "name": "TEST_HealthMetrics-2099-01-01.json"},
        {"id": "file-5", "name": "notes.txt"},
        {"id": "file-6", "name": "HealthMetrics-2026-10-08.json"},
    ]

    files = get_historical_health_metrics_files()

    drive_client.list_files.assert_called_once_with(
        settings.HEALTH_METRICS_DRIVE_FOLDER_ID
    )

    assert files == [
        {
            "id": "file-3",
            "name": "FAILED_HealthMetrics-2026-10-05.json",
            "date": date(2026, 10, 5),
        },
        {
            "id": "file-6",
            "name": "HealthMetrics-2026-10-08.json",
            "date": date(2026, 10, 8),
        },
        {
            "id": "file-1",
            "name": "HealthMetrics-2026-10-12.json",
            "date": date(2026, 10, 12),
        },
    ]


# ============================================================================
# import_historical_health_metrics
# ============================================================================


def make_files(count: int) -> list[dict]:
    """
    Build a list of eligible historical files, one per day.
    """

    return [
        {
            "id": f"file-{day}",
            "name": f"HealthMetrics-2026-01-{day:02d}.json",
            "date": date(2026, 1, day),
        }
        for day in range(1, count + 1)
    ]


# Verify that each file is imported in order, with a pause after every
# full batch except when the batch ends on the last file.
@patch(f"{SCRIPT}.time.sleep")
@patch(f"{SCRIPT}.process_health_metrics_files")
@patch(f"{SCRIPT}.get_historical_health_metrics_files")
@patch(f"{SCRIPT}.BATCH_SIZE", 2)
def test_import_historical_health_metrics_imports_in_order_with_batch_pauses(
    mock_get_files,
    mock_process_health_metrics_files,
    mock_sleep,
):

    files = make_files(5)

    mock_get_files.return_value = files
    mock_process_health_metrics_files.return_value = [{}]

    import_historical_health_metrics()

    assert mock_process_health_metrics_files.call_args_list == [
        call(file_name=file["name"])
        for file in files
    ]

    # Batches of 2 out of 5 files: pause after file 2 and file 4.
    assert mock_sleep.call_args_list == [
        call(BATCH_DELAY_SECONDS),
        call(BATCH_DELAY_SECONDS),
    ]


# Verify that no pause happens after the final file, even when it
# completes a batch.
@patch(f"{SCRIPT}.time.sleep")
@patch(f"{SCRIPT}.process_health_metrics_files")
@patch(f"{SCRIPT}.get_historical_health_metrics_files")
@patch(f"{SCRIPT}.BATCH_SIZE", 2)
def test_import_historical_health_metrics_does_not_pause_after_last_file(
    mock_get_files,
    mock_process_health_metrics_files,
    mock_sleep,
):

    mock_get_files.return_value = make_files(4)
    mock_process_health_metrics_files.return_value = [{}]

    import_historical_health_metrics()

    # Batches of 2 out of 4 files: pause after file 2 only.
    assert mock_sleep.call_args_list == [
        call(BATCH_DELAY_SECONDS),
    ]


# Verify that at most MAX_FILES files are imported in one run.
@patch(f"{SCRIPT}.time.sleep")
@patch(f"{SCRIPT}.process_health_metrics_files")
@patch(f"{SCRIPT}.get_historical_health_metrics_files")
@patch(f"{SCRIPT}.MAX_FILES", 3)
def test_import_historical_health_metrics_stops_at_max_files(
    mock_get_files,
    mock_process_health_metrics_files,
    mock_sleep,
):

    files = make_files(5)

    mock_get_files.return_value = files
    mock_process_health_metrics_files.return_value = [{}]

    import_historical_health_metrics()

    assert mock_process_health_metrics_files.call_args_list == [
        call(file_name=file["name"])
        for file in files[:3]
    ]
