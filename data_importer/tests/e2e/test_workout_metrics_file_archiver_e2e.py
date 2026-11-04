from datetime import date, timedelta

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.archivers.file_archiver import (
    archive_processed_files,
)
from tests.e2e.e2e_helpers import (
    WORKOUT_FIXTURE_TEST_PREFIX,
    workout_metrics_fixture,
)

TEST_FILE_PREFIX = WORKOUT_FIXTURE_TEST_PREFIX
FILE_SUFFIX = ".json"

FAILED_PREFIX = "FAILED_"
PROCESSED_PREFIX = "PROCESSED_"


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

    # The permanent fixture shared with the importer E2E tests. Restoring
    # it first repairs anything an interrupted run left behind (a
    # temporary name, or the file left in the processed folder).
    fixture = workout_metrics_fixture(drive_client)

    fixture.restore()

    file_id = fixture.file_id

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

        # Move it back from the processed folder if it was archived,
        # and restore its permanent TEST_ name.
        fixture.restore()
