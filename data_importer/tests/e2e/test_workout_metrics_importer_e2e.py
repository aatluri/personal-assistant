from datetime import date, datetime

import pytest
import requests

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.importers.workout_metrics_importer import (
    build_workout_metrics_payloads,
)

DATA_IMPORTER_BASE_URL = "http://127.0.0.1:8001"
BACKEND_BASE_URL = "http://127.0.0.1:8000"

FAILED_PREFIX = "FAILED_"
PROCESSED_PREFIX = "PROCESSED_"
FILE_PREFIX = "WorkoutMetrics-"
FILE_SUFFIX = ".json"


def get_workout_metrics_file_date(
    file_name: str,
) -> date | None:
    """
    Extract the workout date from a valid unprocessed
    Workout Metrics filename.

    Failed and processed files are ignored.
    """

    if (
        file_name.startswith(FAILED_PREFIX)
        or file_name.startswith(PROCESSED_PREFIX)
    ):
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


def get_latest_workout_metrics_file(
    drive_client: GoogleDriveClient,
) -> dict:
    """
    Return the latest valid unprocessed Workout Metrics
    file from the incoming Google Drive folder.
    """

    files = drive_client.list_files(
        settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
    )

    valid_files = []

    for file in files:

        file_date = get_workout_metrics_file_date(
            file["name"]
        )

        if file_date is not None:
            valid_files.append(
                (
                    file_date,
                    file,
                )
            )

    assert valid_files, (
        "No valid unprocessed Workout Metrics files found "
        "in incoming Google Drive folder."
    )

    valid_files.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return valid_files[0][1]


def normalize_datetime(
    value: str | None,
) -> str | None:
    """
    Remove timezone information from an ISO datetime.

    Google Sheets stores Workout Metrics timestamps
    without timezone information.
    """

    if value is None:
        return None

    return (
        datetime.fromisoformat(value)
        .replace(tzinfo=None)
        .isoformat()
    )


def assert_payload_matches_record(
    expected: dict,
    actual: dict,
) -> None:
    """
    Verify that every expected payload field matches
    the value returned by the backend.
    """

    for field, expected_value in expected.items():

        assert field in actual, (
            f"Field '{field}' missing from backend response."
        )

        actual_value = actual[field]

        if isinstance(expected_value, float):
            assert actual_value == pytest.approx(
                expected_value,
                abs=0.01,
            ), (
                f"Mismatch for '{field}': "
                f"expected {expected_value!r}, "
                f"got {actual_value!r}"
            )
        else:
            assert actual_value == expected_value, (
                f"Mismatch for '{field}': "
                f"expected {expected_value!r}, "
                f"got {actual_value!r}"
            )


def test_workout_metrics_importer_e2e():

    drive_client = GoogleDriveClient()

    # ---------------------------------------------------------
    # 1. FIND THE LATEST REAL HEALTH AUTO EXPORT FILE
    # ---------------------------------------------------------

    file = get_latest_workout_metrics_file(
        drive_client
    )

    file_id = file["id"]
    file_name = file["name"]

    print(
        f"Testing Workout Metrics import with: "
        f"{file_name}"
    )

    # ---------------------------------------------------------
    # 2. READ THE REAL JSON FILE
    # ---------------------------------------------------------

    export_data = drive_client.read_json_file(
        file_id
    )

    assert export_data is not None

    assert "data" in export_data
    assert "workouts" in export_data["data"]

    # ---------------------------------------------------------
    # 3. BUILD THE EXPECTED BACKEND PAYLOADS
    # ---------------------------------------------------------

    expected_workouts = build_workout_metrics_payloads(
        export_data
    )

    assert expected_workouts, (
        f"{file_name} contains no Workout Metrics data."
    )

    # ---------------------------------------------------------
    # 4. RUN THE DATA IMPORTER
    # ---------------------------------------------------------

    response = requests.put(
        f"{DATA_IMPORTER_BASE_URL}"
        f"/health/import/workout-metrics",
        params={
            "file_name": file_name,
        },
        timeout=30,
    )

    assert response.status_code == 200, response.text

    import_result = response.json()

    assert import_result["status"] == "success"

    assert import_result["files_processed"] == 1

    assert len(import_result["results"]) == 1

    file_result = import_result["results"][0]

    assert file_result["file_name"] == file_name

    # ---------------------------------------------------------
    # 5. VERIFY IMPORTER RESULT
    # ---------------------------------------------------------

    workout_results = file_result["workout_metrics"]

    assert workout_results is not None

    assert len(workout_results) == len(
        expected_workouts
    )

    # ---------------------------------------------------------
    # 6. VERIFY EACH WORKOUT THROUGH THE BACKEND
    # ---------------------------------------------------------

    for expected_workout in expected_workouts:

        workout_start_time = (
            expected_workout["workout_start_time"]
        )

        response = requests.get(
            f"{BACKEND_BASE_URL}/health/workout-metric",
            params={
                "workout_start_time": workout_start_time,
            },
            timeout=10,
        )

        assert response.status_code == 200, response.text

        actual_workout = response.json()

        assert actual_workout["source"] == (
            "Health Auto Export"
        )

        # Google Sheets stores workout timestamps without
        # timezone information.
        expected_record = expected_workout.copy()

        expected_record["workout_start_time"] = (
            normalize_datetime(
                expected_record["workout_start_time"]
            )
        )

        expected_record["workout_end_time"] = (
            normalize_datetime(
                expected_record["workout_end_time"]
            )
        )

        assert_payload_matches_record(
            expected_record,
            actual_workout,
        )

    # ---------------------------------------------------------
    # 7. VERIFY FILE WAS MARKED AS PROCESSED
    # ---------------------------------------------------------

    files_after_import = drive_client.list_files(
        settings.WORKOUT_METRICS_DRIVE_FOLDER_ID
    )

    processed_file = next(
        (
            file
            for file in files_after_import
            if file["id"] == file_id
        ),
        None,
    )

    assert processed_file is not None, (
        f"Workout Metrics file {file_id} was not found "
        "in the incoming folder after import."
    )

    expected_processed_name = (
        f"{PROCESSED_PREFIX}{file_name}"
    )

    assert processed_file["name"] == (
        expected_processed_name
    ), (
        "Workout Metrics file was not marked as processed. "
        f"Expected {expected_processed_name!r}, "
        f"got {processed_file['name']!r}."
    )