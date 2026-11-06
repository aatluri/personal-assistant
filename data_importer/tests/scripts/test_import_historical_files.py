from datetime import date
from unittest.mock import Mock, call, patch

import pytest

from app.config import settings
from app.modules.health.orchestrators.health_metrics_orchestrator import (
    get_health_metrics_file_date,
    process_health_metrics_files,
)
from app.modules.health.orchestrators.heart_rate_notifications_orchestrator import (
    get_heart_rate_notifications_file_date,
    process_heart_rate_notifications_files,
)
from app.modules.health.orchestrators.workout_metrics_orchestrator import (
    get_workout_metrics_file_date,
    process_workout_metrics_files,
)
from scripts.import_historical_files import (
    BATCH_DELAY_SECONDS,
    FILE_TYPES,
    FileType,
    get_historical_files,
    import_all_historical_files,
    import_historical_files,
    main,
)


SCRIPT = "scripts.import_historical_files"


# ============================================================================
# FILE_TYPES
# ============================================================================


# Verify that each data type uses its own Drive folder, filename rule
# and orchestrator.
@pytest.mark.parametrize(
    "type_name, drive_folder_setting, get_file_date, process_files",
    [
        (
            "health",
            "HEALTH_METRICS_DRIVE_FOLDER_ID",
            get_health_metrics_file_date,
            process_health_metrics_files,
        ),
        (
            "workout",
            "WORKOUT_METRICS_DRIVE_FOLDER_ID",
            get_workout_metrics_file_date,
            process_workout_metrics_files,
        ),
        (
            "heart-rate-notifications",
            "HEART_RATE_NOTIFICATIONS_DRIVE_FOLDER_ID",
            get_heart_rate_notifications_file_date,
            process_heart_rate_notifications_files,
        ),
    ],
)
def test_file_types_are_wired_to_their_folder_and_orchestrator(
    type_name,
    drive_folder_setting,
    get_file_date,
    process_files,
):

    file_type = FILE_TYPES[type_name]

    assert file_type.drive_folder_setting == drive_folder_setting
    assert file_type.get_file_date is get_file_date
    assert file_type.process_files is process_files


# ============================================================================
# get_historical_files
# ============================================================================


# Verify that, for every data type, only eligible files are returned,
# sorted oldest first: recognised and FAILED_ files are kept; PROCESSED_,
# TEST_, other types' files, Drive duplicates and stray files are not.
@pytest.mark.parametrize(
    "type_name, file_prefix, other_prefix",
    [
        ("health", "HealthMetrics-", "WorkoutMetrics-"),
        ("workout", "WorkoutMetrics-", "HealthMetrics-"),
        ("heart-rate-notifications", "HeartRateNotifications-", "HealthMetrics-"),
    ],
)
@patch(f"{SCRIPT}.GoogleDriveClient")
def test_get_historical_files_filters_and_sorts(
    mock_drive_client_class,
    type_name,
    file_prefix,
    other_prefix,
):

    file_type = FILE_TYPES[type_name]
    drive_client = mock_drive_client_class.return_value

    drive_client.list_files.return_value = [
        {"id": "file-1", "name": f"{file_prefix}2026-10-12.json"},
        {"id": "file-2", "name": f"PROCESSED_{file_prefix}2026-10-01.json"},
        {"id": "file-3", "name": f"FAILED_{file_prefix}2026-10-05.json"},
        {"id": "file-4", "name": f"TEST_{file_prefix}2099-01-01.json"},
        {"id": "file-5", "name": "notes.txt"},
        {"id": "file-6", "name": f"{file_prefix}2026-10-08.json"},
        {"id": "file-7", "name": f"{other_prefix}2026-10-09.json"},
        {"id": "file-8", "name": f"{file_prefix}2026-10-10 (1).json"},
    ]

    files = get_historical_files(file_type)

    drive_client.list_files.assert_called_once_with(
        getattr(settings, file_type.drive_folder_setting)
    )

    assert files == [
        {
            "id": "file-3",
            "name": f"FAILED_{file_prefix}2026-10-05.json",
            "date": date(2026, 10, 5),
        },
        {
            "id": "file-6",
            "name": f"{file_prefix}2026-10-08.json",
            "date": date(2026, 10, 8),
        },
        {
            "id": "file-1",
            "name": f"{file_prefix}2026-10-12.json",
            "date": date(2026, 10, 12),
        },
    ]


# ============================================================================
# import_historical_files
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


def make_file_type() -> FileType:
    """
    Build a FileType whose orchestrator is a mock that always succeeds.
    """

    return FileType(
        label="Test Metrics",
        drive_folder_setting="HEALTH_METRICS_DRIVE_FOLDER_ID",
        get_file_date=Mock(),
        process_files=Mock(return_value=[{}]),
    )


# Verify that each file is imported in order, with a pause after every
# full batch except when the batch ends on the last file.
@patch(f"{SCRIPT}.time.sleep")
@patch(f"{SCRIPT}.get_historical_files")
@patch(f"{SCRIPT}.BATCH_SIZE", 2)
def test_import_historical_files_imports_in_order_with_batch_pauses(
    mock_get_files,
    mock_sleep,
):

    file_type = make_file_type()
    files = make_files(5)

    mock_get_files.return_value = files

    import_historical_files(file_type)

    mock_get_files.assert_called_once_with(file_type)

    assert file_type.process_files.call_args_list == [
        call(files=[file])
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
@patch(f"{SCRIPT}.get_historical_files")
@patch(f"{SCRIPT}.BATCH_SIZE", 2)
def test_import_historical_files_does_not_pause_after_last_file(
    mock_get_files,
    mock_sleep,
):

    mock_get_files.return_value = make_files(4)

    import_historical_files(make_file_type())

    # Batches of 2 out of 4 files: pause after file 2 only.
    assert mock_sleep.call_args_list == [
        call(BATCH_DELAY_SECONDS),
    ]


# Verify that at most MAX_FILES files are imported in one run.
@patch(f"{SCRIPT}.time.sleep")
@patch(f"{SCRIPT}.get_historical_files")
@patch(f"{SCRIPT}.MAX_FILES", 3)
def test_import_historical_files_stops_at_max_files(
    mock_get_files,
    mock_sleep,
):

    file_type = make_file_type()
    files = make_files(5)

    mock_get_files.return_value = files

    import_historical_files(file_type)

    assert file_type.process_files.call_args_list == [
        call(files=[file])
        for file in files[:3]
    ]


# ============================================================================
# import_all_historical_files
# ============================================================================


# Verify that every type is imported, small backlogs first and workouts
# last, with a pause between types but not after the last one.
@patch(f"{SCRIPT}.time.sleep")
@patch(f"{SCRIPT}.import_historical_files")
def test_import_all_historical_files_imports_every_type_in_order(
    mock_import_historical_files,
    mock_sleep,
):

    import_all_historical_files()

    assert mock_import_historical_files.call_args_list == [
        call(FILE_TYPES["health"]),
        call(FILE_TYPES["heart-rate-notifications"]),
        call(FILE_TYPES["workout"]),
    ]

    assert mock_sleep.call_args_list == [
        call(BATCH_DELAY_SECONDS),
        call(BATCH_DELAY_SECONDS),
    ]


# ============================================================================
# main
# ============================================================================


# Verify that "all" on the command line imports every type.
@patch(f"{SCRIPT}.import_historical_files")
@patch(f"{SCRIPT}.import_all_historical_files")
def test_main_all_imports_every_type(
    mock_import_all_historical_files,
    mock_import_historical_files,
):

    main(["all"])

    mock_import_all_historical_files.assert_called_once_with()
    mock_import_historical_files.assert_not_called()


# Verify that the data type on the command line selects its FileType.
@pytest.mark.parametrize(
    "type_name",
    ["health", "workout", "heart-rate-notifications"],
)
@patch(f"{SCRIPT}.import_historical_files")
def test_main_imports_the_requested_file_type(
    mock_import_historical_files,
    type_name,
):

    main([type_name])

    mock_import_historical_files.assert_called_once_with(
        FILE_TYPES[type_name]
    )


# Verify that an unknown or missing data type is rejected before
# anything is imported.
@pytest.mark.parametrize("argv", [["sleep"], []])
@patch(f"{SCRIPT}.import_historical_files")
@patch(f"{SCRIPT}.import_all_historical_files")
def test_main_rejects_unknown_or_missing_file_type(
    mock_import_all_historical_files,
    mock_import_historical_files,
    argv,
):

    with pytest.raises(SystemExit):
        main(argv)

    mock_import_historical_files.assert_not_called()
    mock_import_all_historical_files.assert_not_called()
