import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet


BASE_URL = "http://127.0.0.1:8000/health/lab-results"

TEST_REPORT_KEY = "TEST_API_REPORT_001"
TEST_MARKER_KEY = "TEST_API_LDL"
TEST_TEXT_MARKER_KEY = "TEST_API_TEXT_RESULT"


def delete_test_rows_from_google_sheets() -> None:
    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.LAB_RESULTS_WORKSHEET
    )

    rows = worksheet.get_all_values()

    if not rows:
        return

    headers = rows[0]

    report_key_column_index = headers.index("Report_Key")
    marker_key_column_index = headers.index("Marker_Key")

    test_keys = {
        (TEST_REPORT_KEY, TEST_MARKER_KEY),
        (TEST_REPORT_KEY, TEST_TEXT_MARKER_KEY),
    }

    matching_row_numbers = []

    for sheet_row_number, row in enumerate(rows[1:], start=2):
        if (
            len(row)
            > max(
                report_key_column_index,
                marker_key_column_index,
            )
            and (
                row[report_key_column_index],
                row[marker_key_column_index],
            )
            in test_keys
        ):
            matching_row_numbers.append(sheet_row_number)

    # Delete bottom-to-top so row numbers do not shift.
    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)


def test_lab_results_e2e():
    # Remove leftovers from an interrupted previous test run.
    delete_test_rows_from_google_sheets()

    try:
        # ---------------------------------------------------------
        # Create
        # ---------------------------------------------------------

        new_result = {
            "report_key": TEST_REPORT_KEY,
            "marker_key": TEST_MARKER_KEY,
            "numerical_value": 110,
            "text_value": "",
            "unit": "mg/dL",
        }

        response = requests.post(
            BASE_URL,
            json=new_result,
        )

        assert response.status_code == 201, response.text

        created_result = response.json()

        assert created_result["report_key"] == TEST_REPORT_KEY
        assert created_result["marker_key"] == TEST_MARKER_KEY
        assert created_result["numerical_value"] == 110
        assert created_result["text_value"] == ""
        assert created_result["unit"] == "mg/dL"

        # ---------------------------------------------------------
        # Get
        # ---------------------------------------------------------

        params = {
            "marker_key": TEST_MARKER_KEY,
        }

        response = requests.get(
            f"{BASE_URL}/{TEST_REPORT_KEY}",
            params=params,
        )

        assert response.status_code == 200, response.text

        retrieved_result = response.json()

        assert retrieved_result["report_key"] == TEST_REPORT_KEY
        assert retrieved_result["marker_key"] == TEST_MARKER_KEY
        assert retrieved_result["numerical_value"] == 110
        assert retrieved_result["unit"] == "mg/dL"

        # ---------------------------------------------------------
        # List All
        # ---------------------------------------------------------

        response = requests.get(BASE_URL)

        assert response.status_code == 200, response.text

        results = response.json()

        assert isinstance(results, list)

        assert any(
            result["report_key"] == TEST_REPORT_KEY
            and result["marker_key"] == TEST_MARKER_KEY
            for result in results
        )

        # ---------------------------------------------------------
        # List By Report_Key
        # ---------------------------------------------------------

        response = requests.get(
            BASE_URL,
            params={
                "report_key": TEST_REPORT_KEY,
            },
        )

        assert response.status_code == 200, response.text

        report_results = response.json()

        assert isinstance(report_results, list)
        assert len(report_results) >= 1

        assert all(
            result["report_key"] == TEST_REPORT_KEY
            for result in report_results
        )

        # ---------------------------------------------------------
        # List By Marker_Key
        # ---------------------------------------------------------

        response = requests.get(
            BASE_URL,
            params={
                "marker_key": TEST_MARKER_KEY,
            },
        )

        assert response.status_code == 200, response.text

        marker_results = response.json()

        assert isinstance(marker_results, list)
        assert len(marker_results) >= 1

        assert all(
            result["marker_key"] == TEST_MARKER_KEY
            for result in marker_results
        )

        # ---------------------------------------------------------
        # List By Report_Key + Marker_Key
        # ---------------------------------------------------------

        response = requests.get(
            BASE_URL,
            params={
                "report_key": TEST_REPORT_KEY,
                "marker_key": TEST_MARKER_KEY,
            },
        )

        assert response.status_code == 200, response.text

        filtered_results = response.json()

        assert isinstance(filtered_results, list)
        assert len(filtered_results) >= 1

        assert all(
            result["report_key"] == TEST_REPORT_KEY
            and result["marker_key"] == TEST_MARKER_KEY
            for result in filtered_results
        )

        # ---------------------------------------------------------
        # Update
        # ---------------------------------------------------------

        updated_data = {
            "report_key": "THIS_REPORT_KEY_SHOULD_NOT_BE_SAVED",
            "marker_key": "THIS_MARKER_KEY_SHOULD_NOT_BE_SAVED",
            "numerical_value": 125,
            "text_value": "",
            "unit": "mg/dL",
        }

        response = requests.put(
            f"{BASE_URL}/{TEST_REPORT_KEY}",
            params=params,
            json=updated_data,
        )

        assert response.status_code == 200, response.text

        updated_result = response.json()

        assert updated_result["report_key"] == TEST_REPORT_KEY
        assert updated_result["marker_key"] == TEST_MARKER_KEY
        assert updated_result["numerical_value"] == 125

        # ---------------------------------------------------------
        # Verify Update
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{TEST_REPORT_KEY}",
            params=params,
        )

        assert response.status_code == 200, response.text

        retrieved_updated_result = response.json()

        assert retrieved_updated_result["report_key"] == TEST_REPORT_KEY
        assert retrieved_updated_result["marker_key"] == TEST_MARKER_KEY
        assert retrieved_updated_result["numerical_value"] == 125
        assert retrieved_updated_result["unit"] == "mg/dL"

        # ---------------------------------------------------------
        # Verify Unique Key Immutability
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/THIS_REPORT_KEY_SHOULD_NOT_BE_SAVED",
            params={
                "marker_key": "THIS_MARKER_KEY_SHOULD_NOT_BE_SAVED",
            },
        )

        assert response.status_code == 404

        response = requests.get(
            f"{BASE_URL}/{TEST_REPORT_KEY}",
            params=params,
        )

        assert response.status_code == 200

        original_result = response.json()

        assert original_result["report_key"] == TEST_REPORT_KEY
        assert original_result["marker_key"] == TEST_MARKER_KEY

        # ---------------------------------------------------------
        # Get Non-Existent Lab Result
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/REPORT_DOES_NOT_EXIST",
            params={
                "marker_key": "MARKER_DOES_NOT_EXIST",
            },
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Lab result not found"

        # ---------------------------------------------------------
        # Update Non-Existent Lab Result
        # ---------------------------------------------------------

        response = requests.put(
            f"{BASE_URL}/REPORT_DOES_NOT_EXIST",
            params={
                "marker_key": "MARKER_DOES_NOT_EXIST",
            },
            json=updated_data,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Lab result not found"

        # ---------------------------------------------------------
        # Text Result
        # ---------------------------------------------------------

        text_result = {
            "report_key": TEST_REPORT_KEY,
            "marker_key": TEST_TEXT_MARKER_KEY,
            "numerical_value": None,
            "text_value": "Negative",
            "unit": "",
        }

        response = requests.post(
            BASE_URL,
            json=text_result,
        )

        assert response.status_code == 201, response.text

        created_text_result = response.json()

        assert created_text_result["report_key"] == TEST_REPORT_KEY
        assert created_text_result["marker_key"] == TEST_TEXT_MARKER_KEY
        assert created_text_result["numerical_value"] is None
        assert created_text_result["text_value"] == "Negative"
        assert created_text_result["unit"] == ""

    finally:
        # Always remove test data, even if an assertion fails.
        delete_test_rows_from_google_sheets()