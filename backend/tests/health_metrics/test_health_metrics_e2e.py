import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet


BASE_URL = "http://127.0.0.1:8000"

TEST_DATE = "2099-01-01"
TEST_SHEET_DATE = "January 01, 2099"
TEST_SOURCE = "E2E Test"


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

def test_health_metrics_e2e():
    """
    Test the complete Health Metrics flow against the real backend
    and real Google Sheet.

    Flow:
        POST
        GET
        PUT
        GET
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
        # 3. UPDATE
        # ---------------------------------------------------------

        update_payload = create_payload.copy()

        update_payload["step_count"] = 15000
        update_payload["active_energy_kcal"] = 650
        update_payload["resting_heart_rate_bpm"] = 52

        response = requests.put(
            f"{BASE_URL}/health/health-metrics",
            json=update_payload,
            timeout=10,
        )

        assert response.status_code == 200, response.text

        # ---------------------------------------------------------
        # 4. READ AGAIN AND VERIFY UPDATE
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/health-metrics/{TEST_DATE}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        updated_health_metric = response.json()

        assert updated_health_metric["date"] == TEST_DATE

        # Verify the fields we changed.
        assert updated_health_metric["step_count"] == 15000
        assert updated_health_metric["active_energy_kcal"] == 650
        assert updated_health_metric["resting_heart_rate_bpm"] == 52

        # Verify an unchanged field was preserved.
        assert updated_health_metric["resting_energy_kcal"] == 1700

        assert updated_health_metric["source"] == TEST_SOURCE

    finally:

        # Always remove the test row, even when an assertion fails.
        delete_test_rows_from_google_sheets()