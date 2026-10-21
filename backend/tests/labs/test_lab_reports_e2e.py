import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet
from app.modules.health.labs.lab_service import generate_report_key


BASE_URL = "http://127.0.0.1:8000/health/lab-reports"

TEST_REPORT_DATE = "2026-08-29"
TEST_FILE_NAME = "api_test_report.pdf"

TEST_REPORT_KEY = generate_report_key(
    TEST_REPORT_DATE,
    TEST_FILE_NAME,
)


def delete_test_rows_from_google_sheets() -> None:
    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.LAB_REPORTS_WORKSHEET
    )

    rows = worksheet.get_all_values()

    if not rows:
        return

    headers = rows[0]

    report_key_column_index = headers.index("Report_Key")

    matching_row_numbers = []

    for sheet_row_number, row in enumerate(rows[1:], start=2):
        if (
            len(row) > report_key_column_index
            and row[report_key_column_index] == TEST_REPORT_KEY
        ):
            matching_row_numbers.append(sheet_row_number)

    # Delete bottom-to-top so row numbers do not shift.
    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)


def test_lab_reports_e2e():
    # Remove leftovers from an interrupted previous test run.
    delete_test_rows_from_google_sheets()

    try:
        # ---------------------------------------------------------
        # Create
        # ---------------------------------------------------------

        new_report = {
            "report_date": TEST_REPORT_DATE,
            "collection_date": "2026-08-29",
            "report_datetime": "2026-08-29 09:30:00",
            "report_type": "Blood Work",
            "laboratory_name": "API Test Laboratory",
            "file_name": TEST_FILE_NAME,
            "notes": "Created through E2E test",
        }

        response = requests.post(
            BASE_URL,
            json=new_report,
        )

        assert response.status_code == 201, response.text

        created_report = response.json()
        test_report_key = created_report["report_key"]

        assert test_report_key == TEST_REPORT_KEY
        assert test_report_key.startswith("LAB_20260829_")
        assert len(test_report_key) == 25
        assert created_report["report_date"] == "2026-08-29"
        assert created_report["file_name"] == "api_test_report.pdf"
        assert (
            created_report["laboratory_name"]
            == "API Test Laboratory"
        )

        # ---------------------------------------------------------
        # Get
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{test_report_key}"
        )

        assert response.status_code == 200, response.text

        retrieved_report = response.json()

        assert retrieved_report["report_key"] == test_report_key
        assert retrieved_report["report_date"] == "2026-08-29"
        assert (
            retrieved_report["laboratory_name"]
            == "API Test Laboratory"
        )
        assert retrieved_report["file_name"] == "api_test_report.pdf"

        # ---------------------------------------------------------
        # List
        # ---------------------------------------------------------

        response = requests.get(BASE_URL)

        assert response.status_code == 200, response.text

        reports = response.json()

        assert isinstance(reports, list)

        assert any(
            report["report_key"] == test_report_key
            for report in reports
        )

        # ---------------------------------------------------------
        # Update
        # ---------------------------------------------------------

        updated_data = {
            "report_key": "THIS_KEY_SHOULD_NOT_BE_SAVED",
            "report_date": "2026-08-30",
            "collection_date": "2026-08-30",
            "report_datetime": "2026-08-30 10:45:00",
            "report_type": "Updated Blood Work",
            "laboratory_name": "Updated API Test Laboratory",
            "file_name": "updated_api_test_report.pdf",
            "notes": "Updated through E2E test",
        }

        response = requests.put(
            f"{BASE_URL}/{test_report_key}",
            json=updated_data,
        )

        assert response.status_code == 200, response.text

        updated_report = response.json()

        assert updated_report["report_key"] == test_report_key
        assert (
            updated_report["laboratory_name"]
            == "Updated API Test Laboratory"
        )

        # ---------------------------------------------------------
        # Verify Update + Report_Key Immutability
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/{test_report_key}"
        )

        assert response.status_code == 200, response.text

        retrieved_updated_report = response.json()

        assert retrieved_updated_report["report_key"] == test_report_key
        assert retrieved_updated_report["report_date"] == "2026-08-30"
        assert (
            retrieved_updated_report["laboratory_name"]
            == "Updated API Test Laboratory"
        )
        assert (
            retrieved_updated_report["notes"]
            == "Updated through E2E test"
        )

        # The Report_Key supplied in the PUT body must not replace
        # the existing Report_Key.
        assert (
            retrieved_updated_report["report_key"]
            != "THIS_KEY_SHOULD_NOT_BE_SAVED"
        )

    finally:
        # Always remove test data, even if an assertion fails.
        delete_test_rows_from_google_sheets()