from datetime import date, datetime

from app.clients.backend_client import BackendClient
from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.importers.heart_rate_notifications_importer import (
    import_heart_rate_notifications,
)
from app.modules.health.constants import (
    FAILED_PREFIX,
    FILENAME_DATE_FORMAT,
    FILE_SUFFIX,
    HEART_RATE_NOTIFICATIONS_FILE_PREFIX,
    PROCESSED_PREFIX,
)


def process_heart_rate_notifications_files(
    file_name: str | None = None,
    files: list[dict] | None = None,
) -> list[dict]:
    """
    Process all Heart Rate Notifications JSON files currently waiting
    in the Google Drive incoming folder.

    If files is provided (Drive files with "id" and "name", as
    returned by list_files), those are used instead of listing the
    folder again. The historical import script lists the folder once
    and passes each file in this way.

    Only files named HeartRateNotifications-YYYY-MM-DD.json (optionally
    with a FAILED_ prefix) are imported. Any other file in the
    folder, such as a TEST_ fixture, is skipped.

    Each file may contain multiple notifications.
    """

    drive_client = GoogleDriveClient()
    backend_client = BackendClient()

    if files is None:
        files = drive_client.list_files(
            settings.HEART_RATE_NOTIFICATIONS_DRIVE_FOLDER_ID
        )

    # Successfully processed files remain in the incoming
    # folder until the separate archiver moves them.
    # They must not be processed again.
    files = [
        file
        for file in files
        if not file["name"].startswith(PROCESSED_PREFIX)
    ]

    # If a specific filename was requested, process only
    # that file.
    if file_name is not None:
        files = [
            file
            for file in files
            if file["name"] == file_name
        ]

    # Only import files whose name matches the Health Auto Export
    # pattern. Anything else in the folder (TEST_ fixtures, Drive
    # duplicates, stray files) must never reach the backend.
    recognised_files = []

    for file in files:
        if get_heart_rate_notifications_file_date(
            file["name"].removeprefix(FAILED_PREFIX)
        ) is None:
            print(f"Skipping unrecognised file: {file['name']}")
            continue

        recognised_files.append(file)

    files = recognised_files

    # Process files oldest to newest.
    # FAILED_ files remain eligible for retry.
    files.sort(
        key=lambda file: get_heart_rate_notifications_file_date(
            file["name"].removeprefix(FAILED_PREFIX)
        )
    )

    if not files:
        print("No Heart Rate Notifications files found to process.")
        return []

    results = []

    for file in files:
        file_id = file["id"]
        current_file_name = file["name"]

        print(f"Processing: {current_file_name}")

        try:
            # Read the JSON file only once.
            export_data = drive_client.read_json_file(
                file_id
            )

            # Import all notifications contained in the file.
            notification_results = import_heart_rate_notifications(
                export_data,
                backend_client,
            )

            results.append(
                {
                    "file_name": current_file_name,
                    "heart_rate_notifications": notification_results,
                }
            )

            # Remove FAILED_ if this is a successful retry,
            # then mark the file as successfully processed.
            original_name = current_file_name.removeprefix(
                FAILED_PREFIX
            )

            processed_name = (
                f"{PROCESSED_PREFIX}{original_name}"
            )

            drive_client.rename_file(
                file_id=file_id,
                new_name=processed_name,
            )

            print(
                f"Successfully imported: "
                f"{current_file_name}"
            )

        except Exception as error:
            print(
                f"Failed to import "
                f"{current_file_name}: {error}"
            )

            # Mark the file as failed so it remains visible
            # and can be retried on a later run.
            if not current_file_name.startswith(
                FAILED_PREFIX
            ):
                try:
                    drive_client.rename_file(
                        file_id=file_id,
                        new_name=(
                            f"{FAILED_PREFIX}"
                            f"{current_file_name}"
                        ),
                    )

                    print(
                        f"Marked as failed: "
                        f"{FAILED_PREFIX}"
                        f"{current_file_name}"
                    )

                except Exception as rename_error:
                    print(
                        f"Unable to rename failed file "
                        f"{current_file_name}: "
                        f"{rename_error}"
                    )

            continue

    return results


def get_heart_rate_notifications_file_date(
    file_name: str,
) -> date | None:
    """
    Extract the notification date from a filename.

    Expected format:
        HeartRateNotifications-2026-07-02.json

    Returns None if the filename does not match the
    expected format.
    """

    if not (
        file_name.startswith(HEART_RATE_NOTIFICATIONS_FILE_PREFIX)
        and file_name.endswith(FILE_SUFFIX)
    ):
        return None

    date_text = file_name[
        len(HEART_RATE_NOTIFICATIONS_FILE_PREFIX):-len(FILE_SUFFIX)
    ]

    try:
        return datetime.strptime(
            date_text,
            FILENAME_DATE_FORMAT,
        ).date()

    except ValueError:
        return None