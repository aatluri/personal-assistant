"""
Import a large backlog of Health Auto Export files, oldest first.

Usage (from data_importer/, with .venv activated):

    python -m scripts.import_historical_files health
    python -m scripts.import_historical_files workout
    python -m scripts.import_historical_files heart-rate-notifications
    python -m scripts.import_historical_files all

Each file is imported by the same orchestrator the import endpoint uses,
one file at a time, with a pause after every batch to stay within the
Google Sheets API quotas. The Drive folder is listed only once per run.
"""

import argparse
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
import time

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.constants import FAILED_PREFIX
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

MAX_FILES = 500
BATCH_SIZE = 15
BATCH_DELAY_SECONDS = 60


@dataclass(frozen=True)
class FileType:
    """
    Everything the script needs to know about one kind of export file.
    """

    # Shown in the progress messages, e.g. "Workout Metrics".
    label: str

    # Name of the settings field holding the incoming Drive folder ID.
    drive_folder_setting: str

    # Returns the date in a recognised filename, or None for any
    # other name (including PROCESSED_ and TEST_ files).
    get_file_date: Callable[[str], date | None]

    # The orchestrator that imports the files it is given.
    process_files: Callable[..., list[dict]]


# The data type given on the command line -> how to import its files.
# To support another export, add an entry here.
#
# "all" imports every type in this order: the small backlogs first, so
# they are not left waiting behind the long workout run.
FILE_TYPES: dict[str, FileType] = {
    "health": FileType(
        label="Health Metrics",
        drive_folder_setting="HEALTH_METRICS_DRIVE_FOLDER_ID",
        get_file_date=get_health_metrics_file_date,
        process_files=process_health_metrics_files,
    ),
    "heart-rate-notifications": FileType(
        label="Heart Rate Notifications",
        drive_folder_setting="HEART_RATE_NOTIFICATIONS_DRIVE_FOLDER_ID",
        get_file_date=get_heart_rate_notifications_file_date,
        process_files=process_heart_rate_notifications_files,
    ),
    "workout": FileType(
        label="Workout Metrics",
        drive_folder_setting="WORKOUT_METRICS_DRIVE_FOLDER_ID",
        get_file_date=get_workout_metrics_file_date,
        process_files=process_workout_metrics_files,
    ),
}

ALL = "all"


def get_historical_files(file_type: FileType) -> list[dict]:
    """
    Get the unprocessed and failed files of one type from Google Drive,
    sorted oldest to newest.

    FAILED_ files are eligible for retry. Any other name that is not a
    recognised export filename, including PROCESSED_ and TEST_ files,
    is ignored.
    """

    drive_client = GoogleDriveClient()

    files = drive_client.list_files(
        getattr(settings, file_type.drive_folder_setting)
    )

    historical_files = []

    for file in files:

        file_date = file_type.get_file_date(
            file["name"].removeprefix(FAILED_PREFIX)
        )

        if file_date is None:
            continue

        historical_files.append(
            {
                "id": file["id"],
                "name": file["name"],
                "date": file_date,
            }
        )

    historical_files.sort(
        key=lambda file: file["date"]
    )

    return historical_files


def import_historical_files(file_type: FileType) -> None:
    """
    Import the historical files of one type from oldest to newest.

    The folder is listed once, here. Each file (with its Drive id) is
    passed to the orchestrator, so it does not list the folder again
    for every file.
    """

    files = get_historical_files(file_type)

    print(
        f"Found {len(files)} {file_type.label} files "
        f"waiting to be processed."
    )

    files = files[:MAX_FILES]

    print(
        f"Processing a maximum of {MAX_FILES} files "
        f"in this run."
    )

    for index, file in enumerate(
        files,
        start=1,
    ):

        print(
            f"\n[{index}/{len(files)}] "
            f"Processing {file['name']}"
        )

        results = file_type.process_files(
            files=[file]
        )

        if results:
            print(
                f"Completed: {file['name']}"
            )
        else:
            print(
                f"Failed: {file['name']}"
            )

        # Pause after every batch, unless this was
        # the final file in the current run.
        if (
            index % BATCH_SIZE == 0
            and index < len(files)
        ):
            print(
                f"\nProcessed {BATCH_SIZE} files. "
                f"Waiting {BATCH_DELAY_SECONDS} seconds..."
            )

            time.sleep(BATCH_DELAY_SECONDS)


def import_all_historical_files() -> None:
    """
    Import the historical files of every type, in FILE_TYPES order.

    MAX_FILES applies to each type separately. A failed file does not
    stop the run; it is renamed FAILED_ and retried on the next run.
    """

    file_types = list(FILE_TYPES.values())

    for index, file_type in enumerate(
        file_types,
        start=1,
    ):

        print(f"\n=== {file_type.label} ===")

        import_historical_files(file_type)

        # Let the Google Sheets quota recover before the next type.
        if index < len(file_types):
            print(
                f"\nFinished {file_type.label}. "
                f"Waiting {BATCH_DELAY_SECONDS} seconds..."
            )

            time.sleep(BATCH_DELAY_SECONDS)


def main(argv: list[str] | None = None) -> None:
    """
    Read the data type from the command line and import its backlog.

    The data type is required, so running the script without one never
    imports anything by accident.
    """

    parser = argparse.ArgumentParser(
        description="Import a backlog of Health Auto Export files.",
    )
    parser.add_argument(
        "file_type",
        choices=[*FILE_TYPES, ALL],
        help=f"which export files to import, or '{ALL}' for every type",
    )

    args = parser.parse_args(argv)

    if args.file_type == ALL:
        import_all_historical_files()
    else:
        import_historical_files(FILE_TYPES[args.file_type])


if __name__ == "__main__":
    main()
