from datetime import date, datetime

from app.clients.backend_client import BackendClient
from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.importers.workout_metrics_importer import (
    import_workout_metrics,
)
from app.modules.health.constants import (
    FAILED_PREFIX,
    PROCESSED_PREFIX,
)


FILE_PREFIX = "WorkoutMetrics-"
FILE_SUFFIX = ".json"


def process_workout_metrics_files(
    file_name: str | None = None,
) -> list[dict]:
    """
    Process all Workout Metrics JSON files currently waiting
    in the Google Drive incoming folder.

    Each file may contain multiple workouts.
    """

    drive_client = GoogleDriveClient()
    backend_client = BackendClient()

    files = drive_client.list_files(
        settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
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

    # Process files oldest to newest.
    # FAILED_ files remain eligible for retry.
    files.sort(
        key=lambda file: (
            get_workout_metrics_file_date(
                file["name"].removeprefix(FAILED_PREFIX)
            )
            or date.max
        )
    )

    if not files:
        print("No Workout Metrics files found to process.")
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

            # Import all workouts contained in the file.
            workout_results = import_workout_metrics(
                export_data,
                backend_client,
            )

            results.append(
                {
                    "file_name": current_file_name,
                    "workout_metrics": workout_results,
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


def get_workout_metrics_file_date(
    file_name: str,
) -> date | None:
    """
    Extract the workout-data date from a filename.

    Expected format:
        WorkoutMetrics-2026-07-02.json

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