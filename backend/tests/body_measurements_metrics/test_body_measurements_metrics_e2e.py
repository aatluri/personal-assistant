import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet


BASE_URL = "http://127.0.0.1:8000"

TEST_DATE = "2099-01-01"
TEST_SHEET_DATE = "January 01, 2099"


def delete_test_rows_from_google_sheets() -> None:
    """
    Delete all E2E test rows directly from Google Sheets.
    """

    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.HEALTH_BODY_MEASUREMENTS_WORKSHEET
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

    # Delete from bottom to top so row numbers don't shift underneath us.
    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)

def test_body_measurements_e2e():
    """
    Test the complete Body Measurements flow against the real backend
    and real Google Sheet.

    Flow:
        POST
        GET
        PUT
        GET
        Cleanup directly in Google Sheets
    """

    # Remove any row left behind by a previous interrupted test.
    delete_test_rows_from_google_sheets()

    try:

        # ---------------------------------------------------------
        # 1. CREATE
        # ---------------------------------------------------------

        create_payload = {
            "date": TEST_DATE,
            "weight_kg": 80.5,
            "body_mass_index": 26.9,
            "body_fat_percent": 22.5,
            "muscle_mass_percent": 40.5,
            "visceral_fat": 10.0,
            "neck_cm": 38.0,
            "chest_cm": 100.0,
            "waist_cm": 90.0,
            "stomach_cm": 94.0,
            "hips_cm": 98.0,
            "left_arm_cm": 34.0,
            "right_arm_cm": 34.5,
            "left_forearm_cm": 28.0,
            "right_forearm_cm": 28.5,
            "left_thigh_cm": 56.0,
            "right_thigh_cm": 56.5,
            "left_calf_cm": 38.0,
            "right_calf_cm": 38.5,
            "notes": "E2E Test",
        }

        response = requests.post(
            f"{BASE_URL}/health/body-measurements",
            json=create_payload,
            timeout=10,
        )

        assert response.status_code == 201, response.text

        # ---------------------------------------------------------
        # 2. READ
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/body-measurements/{TEST_DATE}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        body_measurement = response.json()

        assert body_measurement["date"] == TEST_DATE

        assert body_measurement["weight_kg"] == 80.5
        assert body_measurement["body_mass_index"] == 26.9
        assert body_measurement["body_fat_percent"] == 22.5
        assert body_measurement["muscle_mass_percent"] == 40.5
        assert body_measurement["visceral_fat"] == 10.0

        assert body_measurement["neck_cm"] == 38.0
        assert body_measurement["chest_cm"] == 100.0
        assert body_measurement["waist_cm"] == 90.0
        assert body_measurement["stomach_cm"] == 94.0
        assert body_measurement["hips_cm"] == 98.0

        assert body_measurement["left_arm_cm"] == 34.0
        assert body_measurement["right_arm_cm"] == 34.5

        assert body_measurement["left_forearm_cm"] == 28.0
        assert body_measurement["right_forearm_cm"] == 28.5

        assert body_measurement["left_thigh_cm"] == 56.0
        assert body_measurement["right_thigh_cm"] == 56.5

        assert body_measurement["left_calf_cm"] == 38.0
        assert body_measurement["right_calf_cm"] == 38.5

        assert body_measurement["notes"] == "E2E Test"

        # ---------------------------------------------------------
        # 3. UPDATE
        # ---------------------------------------------------------

        update_payload = create_payload.copy()

        update_payload["weight_kg"] = 79.5
        update_payload["waist_cm"] = 88.0
        update_payload["body_fat_percent"] = 21.5
        update_payload["notes"] = "E2E Test Updated"

        response = requests.put(
            f"{BASE_URL}/health/body-measurements",
            json=update_payload,
            timeout=10,
        )

        assert response.status_code == 200, response.text

        # ---------------------------------------------------------
        # 4. READ AGAIN AND VERIFY UPDATE
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/body-measurements/{TEST_DATE}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        updated_body_measurement = response.json()

        assert updated_body_measurement["date"] == TEST_DATE

        # Verify fields that were changed.
        assert updated_body_measurement["weight_kg"] == 79.5
        assert updated_body_measurement["waist_cm"] == 88.0
        assert updated_body_measurement["body_fat_percent"] == 21.5
        assert updated_body_measurement["notes"] == "E2E Test Updated"

        # Verify some unchanged fields were preserved.
        assert updated_body_measurement["chest_cm"] == 100.0
        assert updated_body_measurement["right_arm_cm"] == 34.5
        assert updated_body_measurement["right_thigh_cm"] == 56.5

    finally:

        # Always remove the test row, even if an assertion fails.
        delete_test_rows_from_google_sheets()