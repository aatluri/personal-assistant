import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet


BASE_URL = "http://127.0.0.1:8000/health/lab-marker-interpretations"

TEST_MARKER_KEY = "TEST_API_LDL"
TEST_LABEL = "Optimal"

OPTIONAL_TEST_MARKER_KEY = "TEST_API_OPTIONAL_LIMIT"
OPTIONAL_TEST_LABEL = "Detected"


def delete_test_rows_from_google_sheets() -> None:
    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.LAB_MARKER_INTERPRETATIONS_WORKSHEET
    )

    rows = worksheet.get_all_values()

    if not rows:
        return

    headers = rows[0]

    marker_key_column_index = headers.index("Marker_Key")
    label_column_index = headers.index("Label")

    test_keys = {
        (TEST_MARKER_KEY, TEST_LABEL),
        (OPTIONAL_TEST_MARKER_KEY, OPTIONAL_TEST_LABEL),
    }

    matching_row_numbers = []

    for sheet_row_number, row in enumerate(rows[1:], start=2):
        if (
            len(row)
            > max(
                marker_key_column_index,
                label_column_index,
            )
            and (
                row[marker_key_column_index],
                row[label_column_index],
            )
            in test_keys
        ):
            matching_row_numbers.append(sheet_row_number)

    # Delete from bottom to top so row numbers do not shift.
    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)


def test_lab_marker_interpretations_e2e():
    # Remove any test rows left behind by an interrupted previous run.
    delete_test_rows_from_google_sheets()

    try:
        # ---------------------------------------------------------
        # Create
        # ---------------------------------------------------------

        new_interpretation = {
            "marker_key": TEST_MARKER_KEY,
            "label": TEST_LABEL,
            "lower_limit": 0,
            "upper_limit": 100,
        }

        response = requests.post(
            BASE_URL,
            json=new_interpretation,
        )

        assert response.status_code == 201, response.text

        created_interpretation = response.json()

        assert created_interpretation["marker_key"] == TEST_MARKER_KEY
        assert created_interpretation["label"] == TEST_LABEL
        assert created_interpretation["lower_limit"] == 0
        assert created_interpretation["upper_limit"] == 100

        # ---------------------------------------------------------
        # Get
        # ---------------------------------------------------------

        params = {
            "label": TEST_LABEL,
        }

        response = requests.get(
            f"{BASE_URL}/{TEST_MARKER_KEY}",
            params=params,
        )

        assert response.status_code == 200, response.text

        retrieved_interpretation = response.json()

        assert retrieved_interpretation["marker_key"] == TEST_MARKER_KEY
        assert retrieved_interpretation["label"] == TEST_LABEL
        assert retrieved_interpretation["lower_limit"] == 0
        assert retrieved_interpretation["upper_limit"] == 100

        # ---------------------------------------------------------
        # List All
        # ---------------------------------------------------------

        response = requests.get(BASE_URL)

        assert response.status_code == 200, response.text

        interpretations = response.json()

        assert isinstance(interpretations, list)

        assert any(
            interpretation["marker_key"] == TEST_MARKER_KEY
            and interpretation["label"] == TEST_LABEL
            for interpretation in interpretations
        )

        # ---------------------------------------------------------
        # List By Marker_Key
        # ---------------------------------------------------------

        response = requests.get(
            BASE_URL,
            params={"marker_key": TEST_MARKER_KEY},
        )

        assert response.status_code == 200, response.text

        marker_interpretations = response.json()

        assert isinstance(marker_interpretations, list)
        assert len(marker_interpretations) >= 1

        assert all(
            interpretation["marker_key"] == TEST_MARKER_KEY
            for interpretation in marker_interpretations
        )

        # ---------------------------------------------------------
        # Update
        # ---------------------------------------------------------

        updated_data = {
            "marker_key": "THIS_KEY_SHOULD_NOT_BE_SAVED",
            "label": "THIS_LABEL_SHOULD_NOT_BE_SAVED",
            "lower_limit": 10,
            "upper_limit": 90,
        }

        response = requests.put(
            f"{BASE_URL}/{TEST_MARKER_KEY}",
            params=params,
            json=updated_data,
        )

        assert response.status_code == 200, response.text

        updated_interpretation = response.json()

        assert updated_interpretation["marker_key"] == TEST_MARKER_KEY
        assert updated_interpretation["label"] == TEST_LABEL
        assert updated_interpretation["lower_limit"] == 10
        assert updated_interpretation["upper_limit"] == 90

        # ---------------------------------------------------------
        # Verify Update
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{TEST_MARKER_KEY}",
            params=params,
        )

        assert response.status_code == 200, response.text

        retrieved_updated_interpretation = response.json()

        assert (
            retrieved_updated_interpretation["marker_key"]
            == TEST_MARKER_KEY
        )
        assert (
            retrieved_updated_interpretation["label"]
            == TEST_LABEL
        )
        assert retrieved_updated_interpretation["lower_limit"] == 10
        assert retrieved_updated_interpretation["upper_limit"] == 90

        # ---------------------------------------------------------
        # Verify Unique Key Immutability
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/THIS_KEY_SHOULD_NOT_BE_SAVED",
            params={
                "label": "THIS_LABEL_SHOULD_NOT_BE_SAVED",
            },
        )

        assert response.status_code == 404

        response = requests.get(
            f"{BASE_URL}/{TEST_MARKER_KEY}",
            params=params,
        )

        assert response.status_code == 200

        original_interpretation = response.json()

        assert original_interpretation["marker_key"] == TEST_MARKER_KEY
        assert original_interpretation["label"] == TEST_LABEL

        # ---------------------------------------------------------
        # Get Non-Existent Interpretation
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
            params={
                "label": "LABEL_DOES_NOT_EXIST",
            },
        )

        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "Lab marker interpretation not found"
        )

        # ---------------------------------------------------------
        # Update Non-Existent Interpretation
        # ---------------------------------------------------------

        response = requests.put(
            f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
            params={
                "label": "LABEL_DOES_NOT_EXIST",
            },
            json=updated_data,
        )

        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == "Lab marker interpretation not found"
        )

        # ---------------------------------------------------------
        # Optional Limit Values
        # ---------------------------------------------------------

        optional_interpretation = {
            "marker_key": OPTIONAL_TEST_MARKER_KEY,
            "label": OPTIONAL_TEST_LABEL,
            "lower_limit": None,
            "upper_limit": None,
        }

        response = requests.post(
            BASE_URL,
            json=optional_interpretation,
        )

        assert response.status_code == 201, response.text

        response = requests.get(
            f"{BASE_URL}/{OPTIONAL_TEST_MARKER_KEY}",
            params={
                "label": OPTIONAL_TEST_LABEL,
            },
        )

        assert response.status_code == 200, response.text

        retrieved_optional_interpretation = response.json()

        assert retrieved_optional_interpretation["lower_limit"] is None
        assert retrieved_optional_interpretation["upper_limit"] is None

    finally:
        # Always remove test data, even if an assertion fails.
        delete_test_rows_from_google_sheets()