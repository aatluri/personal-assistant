import requests
from app.config import settings
from app.database.sheets_client import get_spreadsheet

BASE_URL = "http://127.0.0.1:8000/health/lab-marker-definitions"

TEST_MARKER_KEY = "TEST_API_LDL"

def delete_test_rows_from_google_sheets() -> None:
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(
        settings.LAB_MARKER_DEFINITIONS_WORKSHEET
    )

    rows = worksheet.get_all_values()

    if not rows:
        return

    headers = rows[0]
    marker_key_column_index = headers.index("Marker_Key")

    matching_row_numbers = []

    for sheet_row_number, row in enumerate(rows[1:], start=2):
        if (
            len(row) > marker_key_column_index
            and row[marker_key_column_index] == TEST_MARKER_KEY
        ):
            matching_row_numbers.append(sheet_row_number)

    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)

def test_lab_marker_definitions_e2e():

    # Remove leftovers from a previous failed/interrupted run.
    delete_test_rows_from_google_sheets()
    try:
        # ---------------------------------------------------------
        # Create
        # ---------------------------------------------------------

        new_definition = {
            "marker_key": TEST_MARKER_KEY,
            "display_name": "API Test LDL Cholesterol",
            "category": "Cardiovascular",
            "panel": "Lipid Profile",
            "sample_type": "Serum",
            "value_type": "Numeric",
            "default_unit": "mg/dL",
            "is_active": True,
        }

        response = requests.post(
            BASE_URL,
            json=new_definition,
        )

        assert response.status_code == 201, response.text

        created_definition = response.json()

        assert created_definition["marker_key"] == TEST_MARKER_KEY
        assert (
            created_definition["display_name"]
            == "API Test LDL Cholesterol"
        )
        assert created_definition["is_active"] is True

        # ---------------------------------------------------------
        # Get
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{TEST_MARKER_KEY}"
        )

        assert response.status_code == 200, response.text

        retrieved_definition = response.json()

        assert retrieved_definition["marker_key"] == TEST_MARKER_KEY
        assert (
            retrieved_definition["display_name"]
            == "API Test LDL Cholesterol"
        )
        assert retrieved_definition["category"] == "Cardiovascular"
        assert retrieved_definition["panel"] == "Lipid Profile"
        assert retrieved_definition["sample_type"] == "Serum"
        assert retrieved_definition["value_type"] == "Numeric"
        assert retrieved_definition["default_unit"] == "mg/dL"
        assert retrieved_definition["is_active"] is True

        # ---------------------------------------------------------
        # List
        # ---------------------------------------------------------

        response = requests.get(BASE_URL)

        assert response.status_code == 200, response.text

        definitions = response.json()

        assert isinstance(definitions, list)

        assert any(
            definition["marker_key"] == TEST_MARKER_KEY
            for definition in definitions
        )

        # ---------------------------------------------------------
        # Update
        # ---------------------------------------------------------

        updated_data = {
            "marker_key": "THIS_KEY_SHOULD_NOT_BE_SAVED",
            "display_name": "Updated API LDL Cholesterol",
            "category": "Updated Cardiovascular",
            "panel": "Updated Lipid Profile",
            "sample_type": "Plasma",
            "value_type": "Numeric",
            "default_unit": "mmol/L",
            "is_active": False,
        }

        response = requests.put(
            f"{BASE_URL}/{TEST_MARKER_KEY}",
            json=updated_data,
        )

        assert response.status_code == 200, response.text

        updated_definition = response.json()

        assert updated_definition["marker_key"] == TEST_MARKER_KEY
        assert (
            updated_definition["display_name"]
            == "Updated API LDL Cholesterol"
        )
        assert updated_definition["is_active"] is False

        # ---------------------------------------------------------
        # Verify Update
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{TEST_MARKER_KEY}"
        )

        assert response.status_code == 200, response.text

        retrieved_updated_definition = response.json()

        assert (
            retrieved_updated_definition["marker_key"]
            == TEST_MARKER_KEY
        )
        assert (
            retrieved_updated_definition["display_name"]
            == "Updated API LDL Cholesterol"
        )
        assert (
            retrieved_updated_definition["category"]
            == "Updated Cardiovascular"
        )
        assert (
            retrieved_updated_definition["sample_type"]
            == "Plasma"
        )
        assert (
            retrieved_updated_definition["default_unit"]
            == "mmol/L"
        )
        assert retrieved_updated_definition["is_active"] is False

        # ---------------------------------------------------------
        # Verify Marker_Key Immutability
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/THIS_KEY_SHOULD_NOT_BE_SAVED"
        )

        assert response.status_code == 404

        response = requests.get(
            f"{BASE_URL}/{TEST_MARKER_KEY}"
        )

        assert response.status_code == 200
        assert response.json()["marker_key"] == TEST_MARKER_KEY

        # ---------------------------------------------------------
        # Get Non-Existent Marker
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/MARKER_DOES_NOT_EXIST"
        )

        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "Lab marker definition not found"
        )

        # ---------------------------------------------------------
        # Update Non-Existent Marker
        # ---------------------------------------------------------

        response = requests.put(
            f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
            json=updated_data,
        )

        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "Lab marker definition not found"
        )
    finally:
        delete_test_rows_from_google_sheets()