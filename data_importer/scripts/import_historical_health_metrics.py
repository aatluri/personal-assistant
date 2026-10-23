from datetime import date, datetime
import time
from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.constants import (
    FAILED_PREFIX,
    PROCESSED_PREFIX,
)
from app.modules.health.orchestrators.health_metrics_orchestrator import (
    process_health_metrics_files,
)

FILE_PREFIX = "HealthMetrics-"
FILE_SUFFIX = ".json"
TEST_PREFIX = "TEST_"
MAX_FILES = 1
BATCH_SIZE = 5
BATCH_DELAY_SECONDS = 60


def get_health_metrics_file_date(
    file_name: str,
) -> date | None:
    """
    Extract the date from a valid Health Metrics filename.

    FAILED_ files are eligible for retry.
    PROCESSED_ and TEST_ files are ignored.
    """

    if file_name.startswith(PROCESSED_PREFIX):
        return None

    if file_name.startswith(TEST_PREFIX):
        return None

    original_name = file_name.removeprefix(
        FAILED_PREFIX
    )

    if not (
        original_name.startswith(FILE_PREFIX)
        and original_name.endswith(FILE_SUFFIX)
    ):
        return None

    date_text = original_name[
        len(FILE_PREFIX):-len(FILE_SUFFIX)
    ]

    try:
        return datetime.strptime(
            date_text,
            "%Y-%m-%d",
        ).date()

    except ValueError:
        return None


def get_historical_health_metrics_files() -> list[dict]:
    """
    Get unprocessed and failed Health Metrics files
    from Google Drive, sorted oldest to newest.
    """

    drive_client = GoogleDriveClient()

    files = drive_client.list_files(
        settings.HEALTH_METRICS_DRIVE_FOLDER_ID
    )

    historical_files = []

    for file in files:

        file_date = get_health_metrics_file_date(
            file["name"]
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


def import_historical_health_metrics() -> None:
    """
    Import historical Health Metrics files
    from oldest to newest.
    """

    files = get_historical_health_metrics_files()

    print(
        f"Found {len(files)} Health Metrics files "
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

        results = process_health_metrics_files(
            file_name=file["name"]
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

if __name__ == "__main__":
    import_historical_health_metrics()