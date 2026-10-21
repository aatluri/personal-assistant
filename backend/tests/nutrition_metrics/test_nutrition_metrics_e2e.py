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
        settings.HEALTH_NUTRITION_METRICS_WORKSHEET
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


def test_nutrition_metrics_e2e():
    """
    Test the complete Nutrition Metrics flow against the real backend
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
            "dietary_energy_kcal": 2000,
            "protein_g": 120,
            "carbohydrates_g": 220,
            "fiber_g": 30,
            "sugar_g": 40,
            "total_fat_g": 70,
            "saturated_fat_g": 20,
            "polyunsaturated_fat_g": 15,
            "monounsaturated_fat_g": 25,
            "water_fl_oz_us": 100,
            "cholesterol_mg": 250,
            "source": TEST_SOURCE,
        }

        response = requests.post(
            f"{BASE_URL}/health/nutrition-metrics",
            json=create_payload,
            timeout=10,
        )

        assert response.status_code == 201, response.text

        # ---------------------------------------------------------
        # 2. READ
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/nutrition-metrics/{TEST_DATE}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        nutrition_metric = response.json()

        assert nutrition_metric["date"] == TEST_DATE
        assert nutrition_metric["dietary_energy_kcal"] == 2000
        assert nutrition_metric["protein_g"] == 120
        assert nutrition_metric["carbohydrates_g"] == 220
        assert nutrition_metric["fiber_g"] == 30
        assert nutrition_metric["sugar_g"] == 40
        assert nutrition_metric["total_fat_g"] == 70
        assert nutrition_metric["saturated_fat_g"] == 20
        assert nutrition_metric["polyunsaturated_fat_g"] == 15
        assert nutrition_metric["monounsaturated_fat_g"] == 25
        assert nutrition_metric["water_fl_oz_us"] == 100
        assert nutrition_metric["cholesterol_mg"] == 250
        assert nutrition_metric["source"] == TEST_SOURCE

        # ---------------------------------------------------------
        # 3. UPDATE
        # ---------------------------------------------------------

        update_payload = create_payload.copy()

        update_payload["dietary_energy_kcal"] = 2200
        update_payload["protein_g"] = 135
        update_payload["water_fl_oz_us"] = 110

        response = requests.put(
            f"{BASE_URL}/health/nutrition-metrics",
            json=update_payload,
            timeout=10,
        )

        assert response.status_code == 200, response.text

        # ---------------------------------------------------------
        # 4. READ AGAIN AND VERIFY UPDATE
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/nutrition-metrics/{TEST_DATE}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        updated_nutrition_metric = response.json()

        assert updated_nutrition_metric["date"] == TEST_DATE

        # Verify the fields we changed.
        assert updated_nutrition_metric["dietary_energy_kcal"] == 2200
        assert updated_nutrition_metric["protein_g"] == 135
        assert updated_nutrition_metric["water_fl_oz_us"] == 110

        # Verify unchanged fields were preserved.
        assert updated_nutrition_metric["carbohydrates_g"] == 220
        assert updated_nutrition_metric["total_fat_g"] == 70

        assert updated_nutrition_metric["source"] == TEST_SOURCE

    finally:

        # Always remove the test row, even when an assertion fails.
        delete_test_rows_from_google_sheets()