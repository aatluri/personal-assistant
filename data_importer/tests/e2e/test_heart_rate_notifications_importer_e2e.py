import json
from pathlib import Path

import requests

from app.clients.google_drive_client import GoogleDriveClient
from app.modules.health.constants import PROCESSED_PREFIX
from tests.e2e.e2e_helpers import (
    HEART_RATE_NOTIFICATIONS_FIXTURE_IMPORT_NAME,
    SharedFixture,
    assert_record_matches,
    delete_test_rows_from_google_sheets,
    heart_rate_notifications_fixture,
)


"""
Heart Rate Notifications Importer E2E Test

Imports a synthetic Health Auto Export heart rate notifications file
through the real importer, backend and Google Sheet, and checks the
stored values against values written out by hand: readings in time order
(the fixture lists them out of order), readable type labels, Min/Max/Avg
and timestamps without timezone.

It does not check whether Health Auto Export's real file format has
changed; test_export_format_e2e.py does that.

It uses a permanent fixture file, TEST_HeartRateNotifications-2099-01-01.json,
in the Heart Rate Notifications incoming folder, because service accounts
cannot create files in a personal Drive. Upload it once (any notification
file, renamed). Each run overwrites its content with the committed
fixture, renames it so the importer recognises it, imports it, then
restores its TEST_ name.

Requires the backend (port 8000) and the importer (port 8001) to be
running, and GOOGLE_SHEETS_SPREADSHEET_ID in data_importer/.env for
cleanup. All test rows use the date 2099-02-01 and are removed afterwards.
"""


DATA_IMPORTER_BASE_URL = "http://127.0.0.1:8001"
BACKEND_BASE_URL = "http://127.0.0.1:8000"

# The committed fixture, and the name the shared Drive file is given
# while it is imported (the importer only accepts recognised names).
FIXTURE_NAME = HEART_RATE_NOTIFICATIONS_FIXTURE_IMPORT_NAME
FIXTURE_PATH = (
    Path(__file__).parent.parent / "test_data" / "e2e" / FIXTURE_NAME
)

TEST_DATE = "2099-02-01"
TEST_SHEET_DATE = "February 01, 2099"
SOURCE = "Health Auto Export"


# Values the backend should store for the two fixture notifications,
# earliest first. Worked out by hand from the fixture, applying the
# importer's rules: readings sorted by time, Min/Max as whole numbers,
# Avg to 2 decimals, readable type labels, timestamps without timezone.
EXPECTED_NOTIFICATIONS = [
    {
        "date": TEST_DATE,
        "notification_type": "Low Heart Rate",
        "start_time": "2099-02-01T06:05:00",
        "end_time": "2099-02-01T06:15:00",
        "threshold_bpm": 40,
        "min_heart_rate_bpm": 38,
        "max_heart_rate_bpm": 40,
        "avg_heart_rate_bpm": 39.0,
        "readings": "38, 40, 39",        # fixture order is 39, 38, 40
        "source": SOURCE,
    },
    {
        "date": TEST_DATE,
        "notification_type": "High Heart Rate",
        "start_time": "2099-02-01T18:30:00",
        "end_time": "2099-02-01T18:40:00",
        "threshold_bpm": 120,
        "min_heart_rate_bpm": 125,
        "max_heart_rate_bpm": 130,       # 130.4 rounded
        "avg_heart_rate_bpm": 127.7,     # (125 + 130.4) / 2
        "readings": "125, 130.4",
        "source": SOURCE,
    },
]


def clean_up(
    fixture: SharedFixture,
) -> None:
    """
    Restore the shared fixture's TEST_ name and remove the test rows.
    """

    fixture.restore()

    delete_test_rows_from_google_sheets(TEST_SHEET_DATE)


def test_heart_rate_notifications_importer_e2e():

    fixture = heart_rate_notifications_fixture(GoogleDriveClient())

    # Repair anything left behind by a previous interrupted run.
    clean_up(fixture)

    try:

        # ---------------------------------------------------------
        # 1. LOAD THE COMMITTED FIXTURE INTO THE SHARED DRIVE FILE
        # ---------------------------------------------------------

        with FIXTURE_PATH.open(encoding="utf-8") as file:
            fixture_data = json.load(file)

        fixture.overwrite_content(fixture_data)
        fixture.rename_for_import()

        # ---------------------------------------------------------
        # 2. IMPORT ONLY THE FIXTURE
        # ---------------------------------------------------------

        response = requests.put(
            f"{DATA_IMPORTER_BASE_URL}/health/import/heart-rate-notifications",
            params={"file_name": FIXTURE_NAME},
            timeout=300,
        )

        assert response.status_code == 200, response.text

        import_result = response.json()

        assert import_result["status"] == "success"
        assert import_result["files_processed"] == 1

        file_result = import_result["results"][0]

        assert file_result["file_name"] == FIXTURE_NAME
        assert len(file_result["heart_rate_notifications"]) == 2

        # ---------------------------------------------------------
        # 3. VERIFY THE STORED NOTIFICATIONS THROUGH THE BACKEND
        # ---------------------------------------------------------

        response = requests.get(
            f"{BACKEND_BASE_URL}/health/heart-rate-notifications",
            params={"notification_date": TEST_DATE},
            timeout=120,
        )

        assert response.status_code == 200, response.text

        stored = response.json()

        assert len(stored) == len(EXPECTED_NOTIFICATIONS), stored

        for expected, actual in zip(EXPECTED_NOTIFICATIONS, stored):
            assert_record_matches(expected, actual)

        # ---------------------------------------------------------
        # 4. VERIFY THE FILE WAS MARKED AS PROCESSED
        # ---------------------------------------------------------

        assert fixture.current_name() == f"{PROCESSED_PREFIX}{FIXTURE_NAME}", (
            f"Expected {PROCESSED_PREFIX}{FIXTURE_NAME} after the import."
        )

    finally:

        # Always restore the fixture and remove the rows, even if a
        # check fails.
        clean_up(fixture)
