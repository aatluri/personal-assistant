from datetime import date, datetime, timedelta

from app.clients.google_drive_client import GoogleDriveClient


PROCESSED_PREFIX = "PROCESSED_"


def archive_processed_files(
    drive_client: GoogleDriveClient,
    source_folder_id: str,
    destination_folder_id: str,
    file_prefix: str,
    file_suffix: str,
    archive_after_days: int,
) -> list[str]:
    """
    Archive successfully processed files that are older
    than the configured archive threshold.

    Only files beginning with PROCESSED_ are eligible
    for archival.

    The age of the file is determined from the date
    contained in its filename.
    """

    files = drive_client.list_files(
        source_folder_id
    )

    cutoff_date = (
        date.today()
        - timedelta(days=archive_after_days)
    )

    archived_files = []

    for file in files:
        file_id = file["id"]
        file_name = file["name"]

        # Only successfully processed files are eligible
        # for archival.
        if not file_name.startswith(PROCESSED_PREFIX):
            continue

        original_name = file_name.removeprefix(
            PROCESSED_PREFIX
        )

        file_date = get_file_date(
            file_name=original_name,
            file_prefix=file_prefix,
            file_suffix=file_suffix,
        )

        # Ignore files that do not match the expected
        # filename format.
        if file_date is None:
            print(
                f"Skipping archive check for "
                f"unrecognized file: {file_name}"
            )
            continue

        # Keep recently processed files in the
        # incoming folder.
        if file_date >= cutoff_date:
            continue

        try:
            drive_client.move_file(
                file_id=file_id,
                source_folder_id=source_folder_id,
                destination_folder_id=destination_folder_id,
            )

            archived_files.append(file_name)

            print(
                f"Archived processed file: "
                f"{file_name}"
            )

        except Exception as error:
            print(
                f"Unable to archive "
                f"{file_name}: {error}"
            )

    return archived_files


def get_file_date(
    file_name: str,
    file_prefix: str,
    file_suffix: str,
) -> date | None:
    """
    Extract a YYYY-MM-DD date from a filename.

    Example:
        HealthMetrics-2026-10-12.json

    With:
        file_prefix = "HealthMetrics-"
        file_suffix = ".json"
    """

    if not (
        file_name.startswith(file_prefix)
        and file_name.endswith(file_suffix)
    ):
        return None

    date_text = file_name[
        len(file_prefix):-len(file_suffix)
    ]

    try:
        return datetime.strptime(
            date_text,
            "%Y-%m-%d",
        ).date()

    except ValueError:
        return None