import json
from pathlib import Path

import requests

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.constants import PROCESSED_PREFIX
from tests.e2e.e2e_helpers import (
    SharedFixture,
    assert_record_matches,
    delete_test_rows_from_google_sheets,
)


"""
Workout Metrics Importer E2E Test

Imports a synthetic Health Auto Export workout file through the real
importer, backend and Google Sheet, and checks the stored values against
values written out by hand. Because the expected values do not come from
the importer's own code, mapping and unit-conversion bugs make it fail.

It does not check whether Health Auto Export's real file format has
changed; test_export_format_e2e.py does that.

It reuses the archiver test's permanent fixture file
(TEST_WorkoutMetrics-2099-01-01.json in the incoming folder), because
service accounts cannot create files in a personal Drive. Each run
overwrites its content with the committed fixture, renames it so the
importer recognises it, imports it, then restores its TEST_ name.

Requires the backend (port 8000) and the importer (port 8001) to be
running, and GOOGLE_SHEETS_SPREADSHEET_ID in data_importer/.env for
cleanup. All test rows use the date 2099-02-01 and are removed afterwards.
"""


DATA_IMPORTER_BASE_URL = "http://127.0.0.1:8001"
BACKEND_BASE_URL = "http://127.0.0.1:8000"

# The committed fixture, and the name the shared Drive file is given
# while it is imported (the importer only accepts recognised names).
FIXTURE_NAME = "WorkoutMetrics-2099-02-01.json"

# The shared Drive file's name between runs (skipped by the importer).
PERMANENT_NAME = "TEST_WorkoutMetrics-2099-01-01.json"
TEST_PREFIX = "TEST_WorkoutMetrics-"
FIXTURE_PATH = (
    Path(__file__).parent.parent / "test_data" / "e2e" / FIXTURE_NAME
)

TEST_DATE = "2099-02-01"
TEST_SHEET_DATE = "February 01, 2099"
SOURCE = "Health Auto Export"


# Values the backend should store for the two fixture workouts, keyed by
# workout type. Worked out by hand from the fixture, applying the
# importer's rules: duration seconds → whole minutes, distance miles → km,
# speed m/s → km/h, numbers rounded to 2 decimals, timestamps stored
# without timezone.
EXPECTED_WORKOUTS = {
    "Outdoor Run": {
        "date": TEST_DATE,
        "workout_type": "Outdoor Run",
        "workout_start_time": "2099-02-01T07:00:00",
        "workout_end_time": "2099-02-01T07:30:00",
        "workout_duration_min": 30,     # 1800.4 s
        "total_energy_kcal": 350.46,
        "active_energy_kcal": 300.12,
        "max_heart_rate_bpm": 170,
        "avg_heart_rate_bpm": 150.4,
        "distance_km": 4.83,            # 3.0 mi × 1.609344
        "avg_speed_kmph": 9.0,          # 2.5 m/s × 3.6
        "source": SOURCE,
    },
    "High Intensity Interval Training": {
        "date": TEST_DATE,
        "workout_type": "High Intensity Interval Training",
        "workout_start_time": "2099-02-01T18:00:00",
        "workout_end_time": "2099-02-01T18:45:00",
        "workout_duration_min": 45,     # 2700 s
        "total_energy_kcal": 500.0,
        "active_energy_kcal": 420.0,
        "max_heart_rate_bpm": 165,
        "avg_heart_rate_bpm": 140.0,
        "distance_km": None,            # indoor workout: no distance
        "avg_speed_kmph": None,         # no activity speed recorded
        "source": SOURCE,
    },
}


def get_shared_fixture(
    drive_client: GoogleDriveClient,
) -> SharedFixture:
    """
    Find the shared Workout Metrics fixture file in Drive.
    """

    return SharedFixture(
        drive_client=drive_client,
        incoming_folder_id=settings.WORKOUT_METRICS_DRIVE_FOLDER_ID,
        processed_folder_id=(
            settings.WORKOUT_METRICS_PROCESSED_DRIVE_FOLDER_ID
        ),
        permanent_name=PERMANENT_NAME,
        test_prefix=TEST_PREFIX,
        import_name=FIXTURE_NAME,
    )


def clean_up(
    fixture: SharedFixture,
) -> None:
    """
    Restore the shared fixture's TEST_ name and remove the test rows.
    """

    fixture.restore()

    delete_test_rows_from_google_sheets(TEST_SHEET_DATE)


def test_workout_metrics_importer_e2e():

    fixture = get_shared_fixture(GoogleDriveClient())

    # Repair anything left behind by a previous interrupted run.
    clean_up(fixture)

    try:

        # ---------------------------------------------------------
        # 1. LOAD THE COMMITTED FIXTURE INTO THE SHARED DRIVE FILE
        # ---------------------------------------------------------

        with FIXTURE_PATH.open(encoding="utf-8") as file:
            fixture_data = json.load(file)

        fixture.overwrite_content(fixture_data)
        fixture.rename_for_import()

        # ---------------------------------------------------------
        # 2. IMPORT ONLY THE FIXTURE
        # ---------------------------------------------------------

        response = requests.put(
            f"{DATA_IMPORTER_BASE_URL}/health/import/workout-metrics",
            params={"file_name": FIXTURE_NAME},
            timeout=60,
        )

        assert response.status_code == 200, response.text

        import_result = response.json()

        assert import_result["status"] == "success"
        assert import_result["files_processed"] == 1

        file_result = import_result["results"][0]

        assert file_result["file_name"] == FIXTURE_NAME
        assert len(file_result["workout_metrics"]) == 2

        # ---------------------------------------------------------
        # 3. VERIFY THE STORED WORKOUTS THROUGH THE BACKEND
        # ---------------------------------------------------------

        response = requests.get(
            f"{BACKEND_BASE_URL}/health/workout-metrics",
            params={"workout_date": TEST_DATE},
            timeout=10,
        )

        assert response.status_code == 200, response.text

        stored_workouts = {
            workout["workout_type"]: workout
            for workout in response.json()
        }

        assert set(stored_workouts) == set(EXPECTED_WORKOUTS), (
            f"Expected workouts {sorted(EXPECTED_WORKOUTS)}, "
            f"got {sorted(stored_workouts)}"
        )

        for workout_type, expected in EXPECTED_WORKOUTS.items():
            assert_record_matches(
                expected,
                stored_workouts[workout_type],
            )

        # ---------------------------------------------------------
        # 4. VERIFY THE FILE WAS MARKED AS PROCESSED
        # ---------------------------------------------------------

        assert fixture.current_name() == f"{PROCESSED_PREFIX}{FIXTURE_NAME}", (
            f"Expected {PROCESSED_PREFIX}{FIXTURE_NAME} after the import."
        )

    finally:

        # Always restore the fixture and remove the rows, even if a
        # check fails.
        clean_up(fixture)
