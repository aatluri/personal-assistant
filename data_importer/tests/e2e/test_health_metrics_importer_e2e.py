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
Health Metrics Importer E2E Test

Imports a synthetic Health Auto Export file through the real importer,
backend and Google Sheet, and checks the stored values against values
written out by hand. Because the expected values do not come from the
importer's own code, mapping and unit-conversion bugs make it fail.

It does not check whether Health Auto Export's real file format has
changed; test_export_format_e2e.py does that.

It reuses the archiver test's permanent fixture file
(TEST_HealthMetrics-2099-01-01.json in the incoming folder), because
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
FIXTURE_NAME = "HealthMetrics-2099-02-01.json"

# The shared Drive file's name between runs (skipped by the importer).
PERMANENT_NAME = "TEST_HealthMetrics-2099-01-01.json"
TEST_PREFIX = "TEST_HealthMetrics-"
FIXTURE_PATH = (
    Path(__file__).parent.parent / "test_data" / "e2e" / FIXTURE_NAME
)

TEST_DATE = "2099-02-01"
TEST_SHEET_DATE = "February 01, 2099"
SOURCE = "Health Auto Export"


# Values the backend should store for the fixture. Worked out by hand
# from the fixture, applying the importer's rules: health and nutrition
# values rounded to whole numbers, water fl oz → ml, weight lb → kg,
# sleep rounded to 2 decimals, timestamps stored without timezone.

EXPECTED_HEALTH_METRICS = {
    "date": TEST_DATE,
    "step_count": 8000,
    "active_energy_kcal": 450,
    "resting_energy_kcal": 1801,
    "atrial_fibrillation_burden_percent": 1,
    "blood_oxygen_saturation_percent": 96,
    "breathing_disturbances_count": 3,
    "cardio_recovery_bpm": 26,
    "flights_climbed": 12,
    "heart_rate_min_bpm": 45,
    "heart_rate_max_bpm": 150,
    "heart_rate_variability_ms": 61,
    "physical_effort_kcal_hr_kg": 2,
    "respiratory_rate_bpm": 15,
    "resting_heart_rate_bpm": 50,
    "source": SOURCE,
}

EXPECTED_NUTRITION_METRICS = {
    "date": TEST_DATE,
    "dietary_energy_kcal": 2100,
    "protein_g": 121,
    "carbohydrates_g": 200,
    "fiber_g": 30,
    "sugar_g": 41,
    "total_fat_g": 70,
    "saturated_fat_g": 20,
    "polyunsaturated_fat_g": 16,
    "monounsaturated_fat_g": 25,
    "water_ml": 2957,           # 100 US fl oz × 29.5735
    "cholesterol_mg": 250,
    "source": SOURCE,
}

EXPECTED_SLEEP_METRICS = {
    "date": TEST_DATE,
    "sleep_start_time": "2099-01-31T23:30:00",
    "sleep_end_time": "2099-02-01T07:00:00",
    "total_sleep_duration_hr": 7.12,
    "core_sleep_hr": 4.11,
    "rem_sleep_hr": 2.0,
    "deep_sleep_hr": 1.0,
    "awake_hr": 0.26,
    "source": SOURCE,
}

EXPECTED_BODY_MEASUREMENTS = {
    "date": TEST_DATE,
    "weight_kg": 79.83,         # 176 lb × 0.45359237
    "body_mass_index": 25.3,
    "body_fat_percent": 22.5,
    "source": SOURCE,
}


def get_shared_fixture(
    drive_client: GoogleDriveClient,
) -> SharedFixture:
    """
    Find the shared Health Metrics fixture file in Drive.
    """

    return SharedFixture(
        drive_client=drive_client,
        incoming_folder_id=settings.HEALTH_METRICS_DRIVE_FOLDER_ID,
        processed_folder_id=(
            settings.HEALTH_METRICS_PROCESSED_DRIVE_FOLDER_ID
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


def get_backend_record(
    path: str,
) -> dict:
    """
    Fetch one record from the backend and fail clearly if it is missing.
    """

    response = requests.get(
        f"{BACKEND_BASE_URL}{path}",
        timeout=10,
    )

    assert response.status_code == 200, (
        f"GET {path} returned {response.status_code}: {response.text}"
    )

    return response.json()


def test_health_metrics_importer_e2e():

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
            f"{DATA_IMPORTER_BASE_URL}/health/import/health-metrics",
            params={"file_name": FIXTURE_NAME},
            timeout=60,
        )

        assert response.status_code == 200, response.text

        import_result = response.json()

        assert import_result["status"] == "success"
        assert import_result["files_processed"] == 1

        file_result = import_result["results"][0]

        assert file_result["file_name"] == FIXTURE_NAME

        # The fixture contains all four kinds of data.
        assert file_result["health_metrics"] is not None
        assert file_result["nutrition_metrics"] is not None
        assert file_result["sleep_metrics"] is not None
        assert file_result["body_measurements_metrics"] is not None

        # ---------------------------------------------------------
        # 3. VERIFY THE STORED VALUES THROUGH THE BACKEND
        # ---------------------------------------------------------

        assert_record_matches(
            EXPECTED_HEALTH_METRICS,
            get_backend_record(f"/health/health-metrics/{TEST_DATE}"),
        )

        assert_record_matches(
            EXPECTED_NUTRITION_METRICS,
            get_backend_record(f"/health/nutrition-metrics/{TEST_DATE}"),
        )

        assert_record_matches(
            EXPECTED_SLEEP_METRICS,
            get_backend_record(f"/health/sleep-metrics/{TEST_DATE}"),
        )

        assert_record_matches(
            EXPECTED_BODY_MEASUREMENTS,
            get_backend_record(f"/health/body-measurements/{TEST_DATE}"),
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
