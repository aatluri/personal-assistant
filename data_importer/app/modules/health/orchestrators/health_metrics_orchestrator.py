from datetime import date, datetime

from app.clients.backend_client import BackendClient
from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.importers.body_measurements_metrics_importer import (
    import_body_measurements_metrics,
)
from app.modules.health.importers.health_metrics_importer import (
    import_health_metrics,
)
from app.modules.health.importers.nutrition_metrics_importer import (
    import_nutrition_metrics,
)
from app.modules.health.importers.sleep_metrics_importer import (
    import_sleep_metrics,
)

from app.modules.health.constants import (
    FAILED_PREFIX,
    PROCESSED_PREFIX,
)



FILE_PREFIX = "HealthMetrics-"
FILE_SUFFIX = ".json"


def process_health_metrics_files(
    file_name: str | None = None,
) -> list[dict]:
    """
    Process Health Metrics JSON files currently waiting
    in the Google Drive incoming folder.

    If file_name is provided, only that specific file
    will be processed. Otherwise, all unprocessed and
    failed files in the incoming folder will be processed.

    Each file contains Health Metrics, Nutrition Metrics,
    Sleep Metrics, and Body Measurements Metrics data.
    """

    drive_client = GoogleDriveClient()
    backend_client = BackendClient()

    files = drive_client.list_files(
        settings.HEALTH_METRICS_DRIVE_FOLDER_ID
    )

    # Processed files remain in the incoming folder until
    # the separate archive process moves them.
    files = [
        file
        for file in files
        if not file["name"].startswith(PROCESSED_PREFIX)
    ]

    if file_name is not None:
        files = [
            file
            for file in files
            if file["name"] == file_name
        ]

    files.sort(
        key=lambda file: (
            get_health_metrics_file_date(
                file["name"].removeprefix(FAILED_PREFIX)
            )
            or date.max
        )
    )

    if not files:
        if file_name is not None:
            print(
                f"Health Metrics file not found "
                f"or already processed: {file_name}"
            )
        else:
            print(
                "No Health Metrics files found to process."
            )

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

            # Import Health Metrics.
            health_result = import_health_metrics(
                export_data,
                backend_client,
            )

            # Import Nutrition Metrics.
            nutrition_result = import_nutrition_metrics(
                export_data,
                backend_client,
            )

            # Import Sleep Metrics.
            sleep_result = import_sleep_metrics(
                export_data,
                backend_client,
            )

            # Import Body Measurements Metrics.
            body_measurements_result = (
                import_body_measurements_metrics(
                    export_data,
                    backend_client,
                )
            )

            # The file is considered successfully processed
            # only if all four imports complete successfully.
            results.append(
                {
                    "file_name": current_file_name,
                    "health_metrics": health_result,
                    "nutrition_metrics": nutrition_result,
                    "sleep_metrics": sleep_result,
                    "body_measurements_metrics": (
                        body_measurements_result
                    ),
                }
            )

            # Remove FAILED_ if this is a successful retry.
            original_name = current_file_name.removeprefix(
                FAILED_PREFIX
            )

            # Mark the successfully imported file as processed.
            processed_name = (
                f"{PROCESSED_PREFIX}{original_name}"
            )

            drive_client.rename_file(
                file_id=file_id,
                new_name=processed_name,
            )

            print(
                f"Successfully imported and marked "
                f"as processed: {processed_name}"
            )

        except Exception as error:
            print(
                f"Failed to import "
                f"{current_file_name}: {error}"
            )

            # Mark the file as failed so it can be retried
            # on a later run.
            if not current_file_name.startswith(
                FAILED_PREFIX
            ):
                try:
                    failed_name = (
                        f"{FAILED_PREFIX}"
                        f"{current_file_name}"
                    )

                    drive_client.rename_file(
                        file_id=file_id,
                        new_name=failed_name,
                    )

                    print(
                        f"Marked as failed: "
                        f"{failed_name}"
                    )

                except Exception as rename_error:
                    print(
                        f"Unable to rename failed file "
                        f"{current_file_name}: "
                        f"{rename_error}"
                    )

            continue

    return results


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