from datetime import date, timedelta

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.archivers.file_archiver import (
    archive_processed_files,
)

BASE_FILE_NAME = "TEST_WorkoutMetrics-2099-01-01.json"

TEST_FILE_PREFIX = "TEST_WorkoutMetrics-"
FILE_SUFFIX = ".json"

FAILED_PREFIX = "FAILED_"
PROCESSED_PREFIX = "PROCESSED_"


def get_test_file(
    drive_client: GoogleDriveClient,
) -> dict:
    """
    Find the permanent Workout Metrics test fixture
    in the incoming folder.
    """

    files = drive_client.list_files(
        settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
    )

    test_file = next(
        (
            file
            for file in files
            if file["name"] == BASE_FILE_NAME
        ),
        None,
    )

    assert test_file is not None, (
        f"Test fixture {BASE_FILE_NAME!r} was not found "
        "in the Workout Metrics incoming folder."
    )

    return test_file


def run_archiver(
    drive_client: GoogleDriveClient,
) -> list[str]:
    """
    Run the real file archiver against Workout Metrics
    using the test-specific filename prefix.
    """

    return archive_processed_files(
        drive_client=drive_client,
        source_folder_id=(
            settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
        ),
        destination_folder_id=(
            settings
            .WORKOUT_METRICS_PROCESSED_DRIVE_FOLDER_ID
        ),
        file_prefix=TEST_FILE_PREFIX,
        file_suffix=FILE_SUFFIX,
        archive_after_days=(
            settings.DATA_IMPORTER_ARCHIVE_AFTER_DAYS
        ),
    )


def test_workout_metrics_file_archiver_e2e():

    drive_client = GoogleDriveClient()

    test_file = get_test_file(
        drive_client
    )

    file_id = test_file["id"]

    archive_after_days = (
        settings.DATA_IMPORTER_ARCHIVE_AFTER_DAYS
    )

    cutoff_date = (
        date.today()
        - timedelta(days=archive_after_days)
    )

    old_date = cutoff_date - timedelta(days=1)

    old_date_text = old_date.strftime(
        "%Y-%m-%d"
    )

    normal_old_name = (
        f"{TEST_FILE_PREFIX}"
        f"{old_date_text}"
        f"{FILE_SUFFIX}"
    )

    failed_old_name = (
        f"{FAILED_PREFIX}"
        f"{TEST_FILE_PREFIX}"
        f"{old_date_text}"
        f"{FILE_SUFFIX}"
    )

    processed_old_name = (
        f"{PROCESSED_PREFIX}"
        f"{TEST_FILE_PREFIX}"
        f"{old_date_text}"
        f"{FILE_SUFFIX}"
    )

    try:

        # -----------------------------------------------------
        # 1. OLD NORMAL FILE SHOULD NOT BE ARCHIVED
        # -----------------------------------------------------

        drive_client.rename_file(
            file_id=file_id,
            new_name=normal_old_name,
        )

        archived_files = run_archiver(
            drive_client
        )

        assert normal_old_name not in archived_files

        incoming_files = drive_client.list_files(
            settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
        )

        incoming_ids = {
            file["id"]
            for file in incoming_files
        }

        assert file_id in incoming_ids, (
            "Old normal file should remain "
            "in the incoming folder."
        )

        # -----------------------------------------------------
        # 2. OLD FAILED FILE SHOULD NOT BE ARCHIVED
        # -----------------------------------------------------

        drive_client.rename_file(
            file_id=file_id,
            new_name=failed_old_name,
        )

        archived_files = run_archiver(
            drive_client
        )

        assert failed_old_name not in archived_files

        incoming_files = drive_client.list_files(
            settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
        )

        incoming_ids = {
            file["id"]
            for file in incoming_files
        }

        assert file_id in incoming_ids, (
            "Old failed file should remain "
            "in the incoming folder."
        )

        # -----------------------------------------------------
        # 3. OLD PROCESSED FILE SHOULD BE ARCHIVED
        # -----------------------------------------------------

        drive_client.rename_file(
            file_id=file_id,
            new_name=processed_old_name,
        )

        archived_files = run_archiver(
            drive_client
        )

        assert archived_files == [
            processed_old_name
        ]

        incoming_files = drive_client.list_files(
            settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
        )

        archive_files = drive_client.list_files(
            settings
            .WORKOUT_METRICS_PROCESSED_DRIVE_FOLDER_ID
        )

        incoming_ids = {
            file["id"]
            for file in incoming_files
        }

        archive_ids = {
            file["id"]
            for file in archive_files
        }

        assert file_id not in incoming_ids, (
            "Old processed file should no longer "
            "exist in the incoming folder."
        )

        assert file_id in archive_ids, (
            "Old processed file should have been "
            "moved to the archive folder."
        )

    finally:

        # -----------------------------------------------------
        # 4. RESTORE PERMANENT TEST FIXTURE
        # -----------------------------------------------------

        incoming_files = drive_client.list_files(
            settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
        )

        incoming_ids = {
            file["id"]
            for file in incoming_files
        }

        # If the test file was archived, move it back.
        if file_id not in incoming_ids:

            drive_client.move_file(
                file_id=file_id,
                source_folder_id=(
                    settings
                    .WORKOUT_METRICS_PROCESSED_DRIVE_FOLDER_ID
                ),
                destination_folder_id=(
                    settings
                    .WORKOUT_METRICS_DRIVE_FOLDER_ID
                ),
            )

        # Restore the permanent safe filename.
        drive_client.rename_file(
            file_id=file_id,
            new_name=BASE_FILE_NAME,
        )