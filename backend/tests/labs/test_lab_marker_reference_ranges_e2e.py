import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet


BASE_URL = "http://127.0.0.1:8000/health/lab-marker-reference-ranges"

TEST_MARKER_KEY = "TEST_API_LDL"
TEST_GENDER = "Male"
TEST_MIN_AGE = 18
TEST_MAX_AGE = 65

OPTIONAL_TEST_MARKER_KEY = "TEST_API_OPTIONAL_AGE"
OPTIONAL_TEST_GENDER = "All"


def delete_test_rows_from_google_sheets() -> None:
    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.LAB_MARKER_REFERENCE_RANGES_WORKSHEET
    )

    rows = worksheet.get_all_values()

    if not rows:
        return

    headers = rows[0]

    marker_key_column_index = headers.index("Marker_Key")
    gender_column_index = headers.index("Gender")
    min_age_column_index = headers.index("Min_Age")
    max_age_column_index = headers.index("Max_Age")

    matching_row_numbers = []

    for sheet_row_number, row in enumerate(rows[1:], start=2):
        if len(row) <= max(
            marker_key_column_index,
            gender_column_index,
            min_age_column_index,
            max_age_column_index,
        ):
            continue

        marker_key = row[marker_key_column_index]
        gender = row[gender_column_index]
        min_age = row[min_age_column_index]
        max_age = row[max_age_column_index]

        is_main_test_row = (
            marker_key == TEST_MARKER_KEY
            and gender == TEST_GENDER
            and min_age == str(TEST_MIN_AGE)
            and max_age == str(TEST_MAX_AGE)
        )

        is_optional_test_row = (
            marker_key == OPTIONAL_TEST_MARKER_KEY
            and gender == OPTIONAL_TEST_GENDER
            and min_age == ""
            and max_age == ""
        )

        if is_main_test_row or is_optional_test_row:
            matching_row_numbers.append(sheet_row_number)

    # Delete bottom-to-top so row numbers do not shift.
    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)


def test_lab_marker_reference_ranges_e2e():
    # Remove leftovers from an interrupted previous test run.
    delete_test_rows_from_google_sheets()

    try:
        # ---------------------------------------------------------
        # Create
        # ---------------------------------------------------------

        new_reference_range = {
            "marker_key": TEST_MARKER_KEY,
            "gender": TEST_GENDER,
            "min_age": TEST_MIN_AGE,
            "max_age": TEST_MAX_AGE,
            "lower_limit": 0,
            "upper_limit": 130,
            "unit": "mg/dL",
            "source": "API Test",
        }

        response = requests.post(
            BASE_URL,
            json=new_reference_range,
        )

        assert response.status_code == 201, response.text

        created_reference_range = response.json()

        assert created_reference_range["marker_key"] == TEST_MARKER_KEY
        assert created_reference_range["gender"] == TEST_GENDER
        assert created_reference_range["min_age"] == TEST_MIN_AGE
        assert created_reference_range["max_age"] == TEST_MAX_AGE
        assert created_reference_range["lower_limit"] == 0
        assert created_reference_range["upper_limit"] == 130
        assert created_reference_range["unit"] == "mg/dL"

        # ---------------------------------------------------------
        # Get
        # ---------------------------------------------------------

        params = {
            "gender": TEST_GENDER,
            "min_age": TEST_MIN_AGE,
            "max_age": TEST_MAX_AGE,
        }

        response = requests.get(
            f"{BASE_URL}/{TEST_MARKER_KEY}",
            params=params,
        )

        assert response.status_code == 200, response.text

        retrieved_reference_range = response.json()

        assert retrieved_reference_range["marker_key"] == TEST_MARKER_KEY
        assert retrieved_reference_range["gender"] == TEST_GENDER
        assert retrieved_reference_range["min_age"] == TEST_MIN_AGE
        assert retrieved_reference_range["max_age"] == TEST_MAX_AGE
        assert retrieved_reference_range["lower_limit"] == 0
        assert retrieved_reference_range["upper_limit"] == 130
        assert retrieved_reference_range["unit"] == "mg/dL"
        assert retrieved_reference_range["source"] == "API Test"

        # ---------------------------------------------------------
        # List All
        # ---------------------------------------------------------

        response = requests.get(BASE_URL)

        assert response.status_code == 200, response.text

        reference_ranges = response.json()

        assert isinstance(reference_ranges, list)

        assert any(
            reference_range["marker_key"] == TEST_MARKER_KEY
            and reference_range["gender"] == TEST_GENDER
            and reference_range["min_age"] == TEST_MIN_AGE
            and reference_range["max_age"] == TEST_MAX_AGE
            for reference_range in reference_ranges
        )

        # ---------------------------------------------------------
        # List By Marker_Key
        # ---------------------------------------------------------

        response = requests.get(
            BASE_URL,
            params={"marker_key": TEST_MARKER_KEY},
        )

        assert response.status_code == 200, response.text

        marker_reference_ranges = response.json()

        assert isinstance(marker_reference_ranges, list)
        assert len(marker_reference_ranges) >= 1

        assert all(
            reference_range["marker_key"] == TEST_MARKER_KEY
            for reference_range in marker_reference_ranges
        )

        # ---------------------------------------------------------
        # Update
        # ---------------------------------------------------------

        updated_data = {
            "marker_key": "THIS_KEY_SHOULD_NOT_BE_SAVED",
            "gender": "Female",
            "min_age": 99,
            "max_age": 100,
            "lower_limit": 10,
            "upper_limit": 120,
            "unit": "mmol/L",
            "source": "Updated API Test",
        }

        response = requests.put(
            f"{BASE_URL}/{TEST_MARKER_KEY}",
            params=params,
            json=updated_data,
        )

        assert response.status_code == 200, response.text

        updated_reference_range = response.json()

        assert updated_reference_range["marker_key"] == TEST_MARKER_KEY
        assert updated_reference_range["gender"] == TEST_GENDER
        assert updated_reference_range["min_age"] == TEST_MIN_AGE
        assert updated_reference_range["max_age"] == TEST_MAX_AGE

        # ---------------------------------------------------------
        # Verify Update
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{TEST_MARKER_KEY}",
            params=params,
        )

        assert response.status_code == 200, response.text

        retrieved_updated_range = response.json()

        assert retrieved_updated_range["lower_limit"] == 10
        assert retrieved_updated_range["upper_limit"] == 120
        assert retrieved_updated_range["unit"] == "mmol/L"
        assert retrieved_updated_range["source"] == "Updated API Test"

        # ---------------------------------------------------------
        # Verify Unique Key Immutability
        # ---------------------------------------------------------

        wrong_params = {
            "gender": "Female",
            "min_age": 99,
            "max_age": 100,
        }

        response = requests.get(
            f"{BASE_URL}/THIS_KEY_SHOULD_NOT_BE_SAVED",
            params=wrong_params,
        )

        assert response.status_code == 404

        response = requests.get(
            f"{BASE_URL}/{TEST_MARKER_KEY}",
            params=params,
        )

        assert response.status_code == 200

        original_range = response.json()

        assert original_range["marker_key"] == TEST_MARKER_KEY
        assert original_range["gender"] == TEST_GENDER
        assert original_range["min_age"] == TEST_MIN_AGE
        assert original_range["max_age"] == TEST_MAX_AGE

        # ---------------------------------------------------------
        # Get Non-Existent Reference Range
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
            params=params,
        )

        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "Lab marker reference range not found"
        )

        # ---------------------------------------------------------
        # Update Non-Existent Reference Range
        # ---------------------------------------------------------

        response = requests.put(
            f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
            params=params,
            json=updated_data,
        )

        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "Lab marker reference range not found"
        )

        # ---------------------------------------------------------
        # Optional Age Values
        # ---------------------------------------------------------

        optional_age_range = {
            "marker_key": OPTIONAL_TEST_MARKER_KEY,
            "gender": OPTIONAL_TEST_GENDER,
            "min_age": None,
            "max_age": None,
            "lower_limit": 5,
            "upper_limit": 10,
            "unit": "mg/dL",
            "source": "API Test",
        }

        response = requests.post(
            BASE_URL,
            json=optional_age_range,
        )

        assert response.status_code == 201, response.text

        response = requests.get(
            f"{BASE_URL}/{OPTIONAL_TEST_MARKER_KEY}",
            params={
                "gender": OPTIONAL_TEST_GENDER,
            },
        )

        assert response.status_code == 200, response.text

        retrieved_optional_range = response.json()

        assert retrieved_optional_range["min_age"] is None
        assert retrieved_optional_range["max_age"] is None
        assert retrieved_optional_range["lower_limit"] == 5
        assert retrieved_optional_range["upper_limit"] == 10

    finally:
        # Always remove test data, even if the test fails.
        delete_test_rows_from_google_sheets()