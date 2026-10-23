import time
from datetime import datetime

import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet


BASE_URL = "http://127.0.0.1:8000"

TEST_DATE = "2099-01-01"
TEST_SHEET_DATE = "January 01, 2099"
TEST_SOURCE = "E2E Test"

DATETIME_FORMAT = "%B %d, %Y %H:%M:%S"


def delete_test_rows_from_google_sheets() -> None:
    """
    Delete all E2E test rows directly from Google Sheets.
    """

    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.HEALTH_HEALTH_METRICS_WORKSHEET
    )

    rows = worksheet.get_all_values()

    if not rows:
        return

    headers = rows[0]
    date_column_index = headers.index("Date")

    matching_row_numbers = []

    for sheet_row_number, row in enumerate(rows[1:], start=2):

        if (
            len(row) > date_column_index
            and row[date_column_index] == TEST_SHEET_DATE
        ):
            matching_row_numbers.append(sheet_row_number)

    # Delete bottom-to-top so row numbers do not shift.
    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)


def get_test_row_from_google_sheets() -> dict | None:
    """
    Return the E2E test row directly from Google Sheets.
    """

    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.HEALTH_HEALTH_METRICS_WORKSHEET
    )

    rows = worksheet.get_all_records()

    for row in rows:

        if row["Date"] == TEST_SHEET_DATE:
            return row

    return None


def test_health_metrics_e2e():
    """
    Test the complete Health Metrics flow against the real backend
    and real Google Sheet.

    Flow:
        POST
        GET
        Verify Google Sheet metadata
        PUT
        GET
        Verify Google Sheet metadata
        Cleanup directly in Google Sheets
    """

    # Remove any test row left behind by a previous interrupted run.
    delete_test_rows_from_google_sheets()

    try:

        # ---------------------------------------------------------
        # 1. CREATE
        # ---------------------------------------------------------

        create_payload = {
            "date": TEST_DATE,
            "step_count": 12345,
            "active_energy_kcal": 500,
            "resting_energy_kcal": 1700,
            "atrial_fibrillation_burden_percent": 1,
            "blood_oxygen_saturation_percent": 98,
            "breathing_disturbances_count": 2,
            "cardio_recovery_bpm": 25,
            "flights_climbed": 10,
            "heart_rate_min_bpm": 50,
            "heart_rate_max_bpm": 150,
            "heart_rate_variability_ms": 45,
            "physical_effort_kcal_hr_kg": 8,
            "respiratory_rate_bpm": 16,
            "resting_heart_rate_bpm": 55,
            "source": TEST_SOURCE,
        }

        response = requests.post(
            f"{BASE_URL}/health/health-metrics",
            json=create_payload,
            timeout=10,
        )

        assert response.status_code == 201, response.text

        # ---------------------------------------------------------
        # 2. READ
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/health-metrics/{TEST_DATE}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        health_metric = response.json()

        assert health_metric["date"] == TEST_DATE

        assert health_metric["step_count"] == 12345

        assert health_metric["active_energy_kcal"] == 500
        assert health_metric["resting_energy_kcal"] == 1700

        assert health_metric["atrial_fibrillation_burden_percent"] == 1
        assert health_metric["blood_oxygen_saturation_percent"] == 98
        assert health_metric["breathing_disturbances_count"] == 2
        assert health_metric["cardio_recovery_bpm"] == 25

        assert health_metric["flights_climbed"] == 10

        assert health_metric["heart_rate_min_bpm"] == 50
        assert health_metric["heart_rate_max_bpm"] == 150
        assert health_metric["heart_rate_variability_ms"] == 45

        assert health_metric["physical_effort_kcal_hr_kg"] == 8

        assert health_metric["respiratory_rate_bpm"] == 16
        assert health_metric["resting_heart_rate_bpm"] == 55

        assert health_metric["source"] == TEST_SOURCE

        # ---------------------------------------------------------
        # 3. VERIFY CREATE METADATA IN GOOGLE SHEETS
        # ---------------------------------------------------------

        created_sheet_row = get_test_row_from_google_sheets()

        assert created_sheet_row is not None

        assert created_sheet_row["Source"] == TEST_SOURCE

        created_updated_datetime = datetime.strptime(
            created_sheet_row["Updated_DateTime"],
            DATETIME_FORMAT,
        )

        # Updated_DateTime has second-level precision.
        # Ensure the PUT occurs in a later second.
        time.sleep(1.1)

        # ---------------------------------------------------------
        # 4. UPDATE
        # ---------------------------------------------------------

        # Send only the fields we want to update.
        # Fields not supplied should retain their existing values.
        update_payload = {
            "date": TEST_DATE,
            "step_count": 15000,
            "active_energy_kcal": 650,
            "resting_heart_rate_bpm": 52,
            "source": TEST_SOURCE,
        }

        response = requests.put(
            f"{BASE_URL}/health/health-metrics",
            json=update_payload,
            timeout=10,
        )

        assert response.status_code == 200, response.text

        # ---------------------------------------------------------
        # 5. READ AGAIN AND VERIFY UPDATE
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/health-metrics/{TEST_DATE}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        updated_health_metric = response.json()

        assert updated_health_metric["date"] == TEST_DATE

        # Verify supplied fields were updated.
        assert updated_health_metric["step_count"] == 15000
        assert updated_health_metric["active_energy_kcal"] == 650
        assert updated_health_metric["resting_heart_rate_bpm"] == 52

        # Verify fields not supplied by the PUT were preserved.
        assert updated_health_metric["resting_energy_kcal"] == 1700

        assert (
            updated_health_metric[
                "atrial_fibrillation_burden_percent"
            ]
            == 1
        )

        assert (
            updated_health_metric[
                "blood_oxygen_saturation_percent"
            ]
            == 98
        )

        assert (
            updated_health_metric[
                "breathing_disturbances_count"
            ]
            == 2
        )

        assert updated_health_metric["cardio_recovery_bpm"] == 25
        assert updated_health_metric["flights_climbed"] == 10

        assert updated_health_metric["heart_rate_min_bpm"] == 50
        assert updated_health_metric["heart_rate_max_bpm"] == 150
        assert updated_health_metric["heart_rate_variability_ms"] == 45

        assert (
            updated_health_metric[
                "physical_effort_kcal_hr_kg"
            ]
            == 8
        )

        assert updated_health_metric["respiratory_rate_bpm"] == 16

        assert updated_health_metric["source"] == TEST_SOURCE

        # ---------------------------------------------------------
        # 6. VERIFY UPDATE METADATA IN GOOGLE SHEETS
        # ---------------------------------------------------------

        updated_sheet_row = get_test_row_from_google_sheets()

        assert updated_sheet_row is not None

        assert updated_sheet_row["Source"] == TEST_SOURCE

        updated_datetime = datetime.strptime(
            updated_sheet_row["Updated_DateTime"],
            DATETIME_FORMAT,
        )

        assert updated_datetime > created_updated_datetime

    finally:

        # Always remove the test row, even when an assertion fails.
        delete_test_rows_from_google_sheets()