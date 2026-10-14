from datetime import date, datetime, timedelta

from app.clients.backend_client import BackendClient
from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.importers.health_metrics_importer import (
    import_health_metrics,
)


FAILED_PREFIX = "FAILED_"
ARCHIVE_AFTER_DAYS = 30
FILE_PREFIX = "HealthMetrics-"
FILE_SUFFIX = ".json"


def process_health_metrics_files() -> list[dict]:
    """
    Process all Health Metrics JSON files currently waiting
    in the Google Drive incoming folder.
    """

    drive_client = GoogleDriveClient()
    backend_client = BackendClient()

    files = drive_client.list_files(
        settings.HEALTH_METRICS_DRIVE_FOLDER_ID
    )

    if not files:
        print("No Health Metrics files found to process.")
        return []

    results = []

    for file in files:
        file_id = file["id"]
        file_name = file["name"]

        print(f"Processing: {file_name}")

        try:
            export_data = drive_client.read_json_file(
                file_id
            )

            result = import_health_metrics(
                export_data,
                backend_client,
            )

            results.append(result)

            # If this file failed during a previous run,
            # restore its original filename after success.
            if file_name.startswith(FAILED_PREFIX):
                original_name = file_name.removeprefix(
                    FAILED_PREFIX
                )

                drive_client.rename_file(
                    file_id=file_id,
                    new_name=original_name,
                )

                file_name = original_name

            print(
                f"Successfully imported: {file_name}"
            )

        except Exception as error:
            print(
                f"Failed to import {file_name}: {error}"
            )

            # Mark the file as failed so it is immediately
            # visible in Google Drive.
            if not file_name.startswith(FAILED_PREFIX):
                try:
                    drive_client.rename_file(
                        file_id=file_id,
                        new_name=f"{FAILED_PREFIX}{file_name}",
                    )

                    print(
                        f"Marked as failed: "
                        f"{FAILED_PREFIX}{file_name}"
                    )

                except Exception as rename_error:
                    print(
                        f"Unable to rename failed file "
                        f"{file_name}: {rename_error}"
                    )

            continue

    # Perform housekeeping only after all files have
    # been attempted.
    archive_old_health_metrics_files(
        drive_client=drive_client,
    )

    return results


def archive_old_health_metrics_files(
    drive_client: GoogleDriveClient,
) -> None:
    """
    Move Health Metrics files older than 30 days to the
    processed archive folder.

    The age of the file is determined from the date contained
    in its filename, not from Google Drive metadata.

    Failed files are never archived.
    """

    files = drive_client.list_files(
        settings.HEALTH_METRICS_DRIVE_FOLDER_ID
    )

    cutoff_date = (
        date.today()
        - timedelta(days=ARCHIVE_AFTER_DAYS)
    )

    for file in files:
        file_name = file["name"]

        # Failed files remain in the incoming folder
        # so they can be retried.
        if file_name.startswith(FAILED_PREFIX):
            continue

        file_date = get_health_metrics_file_date(
            file_name
        )

        # Ignore files whose names do not match the expected
        # Health Metrics filename format.
        if file_date is None:
            print(
                f"Skipping archive check for "
                f"unrecognized file: {file_name}"
            )
            continue

        # Keep the latest 30 days in the incoming folder.
        if file_date >= cutoff_date:
            continue

        try:
            drive_client.move_file(
                file_id=file["id"],
                source_folder_id=(
                    settings.HEALTH_METRICS_DRIVE_FOLDER_ID
                ),
                destination_folder_id=(
                    settings
                    .HEALTH_METRICS_PROCESSED_DRIVE_FOLDER_ID
                ),
            )

            print(
                f"Archived old file: {file_name}"
            )

        except Exception as error:
            print(
                f"Unable to archive "
                f"{file_name}: {error}"
            )


def get_health_metrics_file_date(
    file_name: str,
) -> date | None:
    """
    Extract the health-data date from a filename.

    Expected format:
        HealthMetrics-2026-10-12.json

    Returns None if the filename does not match the
    expected format.
    """

    if not (
        file_name.startswith(FILE_PREFIX)
        and file_name.endswith(FILE_SUFFIX)
    ):
        return None

    date_text = file_name[
        len(FILE_PREFIX):-len(FILE_SUFFIX)
    ]

    try:
        return datetime.strptime(
            date_text,
            "%Y-%m-%d",
        ).date()

    except ValueError:
        return None