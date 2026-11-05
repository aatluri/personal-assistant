import time
from datetime import datetime

import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet
from tests.helpers.e2e_guards import (
    require_test_date,
)


"""
Heart Rate Notifications E2E Test

Runs against the real backend and the real Google Sheet, using a test
notification dated 2099-01-01 that is removed afterwards.

Requires the backend to be running on port 8000. Live test: skipped by
default; run it deliberately with `pytest -m e2e`.
"""


BASE_URL = "http://127.0.0.1:8000"

TEST_DATE = "2099-01-01"
TEST_START_TIME = "2099-01-01T07:00:00"
TEST_SHEET_START_TIME = "January 01, 2099 07:00:00"

DATETIME_FORMAT = "%B %d, %Y %H:%M:%S"


def delete_test_rows_from_google_sheets() -> None:
    """
    Delete the E2E test notification rows directly from Google Sheets.
    """

    # Never delete anything that is not clearly test data.
    require_test_date(TEST_SHEET_START_TIME)

    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.HEALTH_HEART_RATE_NOTIFICATIONS_WORKSHEET
    )

    rows = worksheet.get_all_values()

    if not rows:
        return

    start_time_column_index = rows[0].index("StartDateTime")

    matching_row_numbers = [
        sheet_row_number
        for sheet_row_number, row in enumerate(rows[1:], start=2)
        if len(row) > start_time_column_index
        and row[start_time_column_index] == TEST_SHEET_START_TIME
    ]

    # Delete bottom-to-top so row numbers do not shift.
    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)


def get_test_row_from_google_sheets() -> dict | None:
    """
    Return the E2E test notification row directly from Google Sheets.
    """

    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.HEALTH_HEART_RATE_NOTIFICATIONS_WORKSHEET
    )

    for row in worksheet.get_all_records():
        if row["StartDateTime"] == TEST_SHEET_START_TIME:
            return row

    return None


def test_heart_rate_notifications_e2e():
    """
    Flow: POST, GET by date, verify the Sheet row, PUT (partial update),
    GET by start time, verify Updated_DateTime changed, clean up.
    """

    # Remove any test rows left behind by a previous interrupted run.
    delete_test_rows_from_google_sheets()

    try:

        # ---------------------------------------------------------
        # 1. CREATE
        # ---------------------------------------------------------

        create_payload = {
            "date": TEST_DATE,
            "notification_type": "Low Heart Rate",
            "start_time": TEST_START_TIME,
            "end_time": "2099-01-01T07:10:00",
            "threshold_bpm": 40,
            "min_heart_rate_bpm": 38,
            "max_heart_rate_bpm": 40,
            "avg_heart_rate_bpm": 39.0,
            "readings": "38, 39, 40, 39",
            "source": "E2E Test",
        }

        response = requests.post(
            f"{BASE_URL}/health/heart-rate-notifications",
            json=create_payload,
            timeout=10,
        )

        assert response.status_code == 201, response.text

        # ---------------------------------------------------------
        # 2. READ BY DATE
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/heart-rate-notifications",
            params={"notification_date": TEST_DATE},
            timeout=10,
        )

        assert response.status_code == 200, response.text

        notifications = response.json()

        assert len(notifications) == 1

        notification = notifications[0]

        assert notification["notification_type"] == "Low Heart Rate"
        assert notification["start_time"] == TEST_START_TIME
        assert notification["threshold_bpm"] == 40
        assert notification["min_heart_rate_bpm"] == 38
        assert notification["avg_heart_rate_bpm"] == 39.0
        assert notification["readings"] == "38, 39, 40, 39"

        # ---------------------------------------------------------
        # 3. VERIFY THE SHEET ROW
        # ---------------------------------------------------------

        created_row = get_test_row_from_google_sheets()

        assert created_row is not None
        assert created_row["Readings"] == "38, 39, 40, 39"

        created_updated_datetime = datetime.strptime(
            created_row["Updated_DateTime"],
            DATETIME_FORMAT,
        )

        # Updated_DateTime has second-level precision.
        time.sleep(1.1)

        # ---------------------------------------------------------
        # 4. PARTIAL UPDATE
        # ---------------------------------------------------------

        update_payload = {
            "date": TEST_DATE,
            "notification_type": "Low Heart Rate",
            "start_time": TEST_START_TIME,
            "end_time": "2099-01-01T07:10:00",
            "max_heart_rate_bpm": 41,
            "readings": "38, 41",
        }

        response = requests.put(
            f"{BASE_URL}/health/heart-rate-notifications",
            json=update_payload,
            timeout=10,
        )

        assert response.status_code == 200, response.text

        # ---------------------------------------------------------
        # 5. READ BY START TIME AND VERIFY THE UPDATE
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/heart-rate-notification",
            params={"start_time": TEST_START_TIME},
            timeout=10,
        )

        assert response.status_code == 200, response.text

        updated = response.json()

        # Supplied fields were updated.
        assert updated["max_heart_rate_bpm"] == 41
        assert updated["readings"] == "38, 41"

        # Fields not supplied kept their values.
        assert updated["threshold_bpm"] == 40
        assert updated["min_heart_rate_bpm"] == 38
        assert updated["avg_heart_rate_bpm"] == 39.0
        assert updated["source"] == "E2E Test"

        updated_row = get_test_row_from_google_sheets()

        assert updated_row is not None

        assert datetime.strptime(
            updated_row["Updated_DateTime"],
            DATETIME_FORMAT,
        ) > created_updated_datetime

    finally:

        # Always remove the test row, even when an assertion fails.
        delete_test_rows_from_google_sheets()
