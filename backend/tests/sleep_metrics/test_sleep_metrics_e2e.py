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
        settings.HEALTH_SLEEP_METRICS_WORKSHEET
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
        settings.HEALTH_SLEEP_METRICS_WORKSHEET
    )

    rows = worksheet.get_all_records()

    for row in rows:

        if row["Date"] == TEST_SHEET_DATE:
            return row

    return None


def test_sleep_metrics_e2e():
    """
    Test the complete Sleep Metrics flow against the real backend
    and real Google Sheet.
    """

    # Remove any test row left behind by a previous interrupted run.
    delete_test_rows_from_google_sheets()

    try:

        # ---------------------------------------------------------
        # 1. CREATE
        # ---------------------------------------------------------

        create_payload = {
            "date": TEST_DATE,
            "sleep_start_time": "2098-12-31T23:00:00",
            "sleep_end_time": "2099-01-01T07:00:00",
            "total_sleep_duration_hr": 7.5,
            "core_sleep_hr": 4.0,
            "rem_sleep_hr": 1.5,
            "deep_sleep_hr": 1.5,
            "awake_hr": 0.5,
            "source": TEST_SOURCE,
        }

        response = requests.post(
            f"{BASE_URL}/health/sleep-metrics",
            json=create_payload,
            timeout=10,
        )

        assert response.status_code == 201, response.text

        # ---------------------------------------------------------
        # 2. READ
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/sleep-metrics/{TEST_DATE}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        sleep_metric = response.json()

        assert sleep_metric["date"] == TEST_DATE

        assert (
            sleep_metric["sleep_start_time"]
            == "2098-12-31T23:00:00"
        )

        assert (
            sleep_metric["sleep_end_time"]
            == "2099-01-01T07:00:00"
        )

        assert sleep_metric["total_sleep_duration_hr"] == 7.5
        assert sleep_metric["core_sleep_hr"] == 4.0
        assert sleep_metric["rem_sleep_hr"] == 1.5
        assert sleep_metric["deep_sleep_hr"] == 1.5
        assert sleep_metric["awake_hr"] == 0.5

        assert sleep_metric["source"] == TEST_SOURCE

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
            "sleep_start_time": "2098-12-31T22:30:00",
            "total_sleep_duration_hr": 8.0,
            "deep_sleep_hr": 2.0,
            "source": TEST_SOURCE,
        }

        response = requests.put(
            f"{BASE_URL}/health/sleep-metrics",
            json=update_payload,
            timeout=10,
        )

        assert response.status_code == 200, response.text

        # ---------------------------------------------------------
        # 5. READ AGAIN AND VERIFY UPDATE
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/sleep-metrics/{TEST_DATE}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        updated_sleep_metric = response.json()

        assert updated_sleep_metric["date"] == TEST_DATE

        # Verify the fields we changed.
        assert (
            updated_sleep_metric["sleep_start_time"]
            == "2098-12-31T22:30:00"
        )

        assert updated_sleep_metric["total_sleep_duration_hr"] == 8.0
        assert updated_sleep_metric["deep_sleep_hr"] == 2.0

        # Verify unchanged fields were preserved.
        assert (
            updated_sleep_metric["sleep_end_time"]
            == "2099-01-01T07:00:00"
        )

        assert updated_sleep_metric["core_sleep_hr"] == 4.0
        assert updated_sleep_metric["rem_sleep_hr"] == 1.5
        assert updated_sleep_metric["awake_hr"] == 0.5

        assert updated_sleep_metric["source"] == TEST_SOURCE

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