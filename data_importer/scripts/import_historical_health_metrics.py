from datetime import date, datetime

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings


FAILED_PREFIX = "FAILED_"
FILE_PREFIX = "HealthMetrics-"
FILE_SUFFIX = ".json"


def get_health_metrics_file_date(
    file_name: str,
) -> date | None:
    """
    Extract the date from a valid Health Metrics filename.
    """

    if file_name.startswith(FAILED_PREFIX):
        return None

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


def get_historical_health_metrics_files() -> list[dict]:
    """
    Get valid Health Metrics files from Google Drive,
    sorted from oldest to newest.
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


if __name__ == "__main__":

    files = get_historical_health_metrics_files()

    print(
        f"Found {len(files)} valid "
        f"Health Metrics files."
    )

    for file in files:
        print(
            f"{file['date']} - {file['name']}"
        )