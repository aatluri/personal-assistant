import time
from datetime import datetime

import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet


BASE_URL = "http://127.0.0.1:8000"

TEST_DATE = "2099-01-01"
TEST_WORKOUT_START_TIME = "2099-01-01T10:00:00"
TEST_SHEET_WORKOUT_START_TIME = "January 01, 2099 10:00:00"
TEST_SOURCE = "E2E Test"

DATETIME_FORMAT = "%B %d, %Y %H:%M:%S"


def delete_test_rows_from_google_sheets() -> None:
    """
    Delete all E2E test workout rows directly from Google Sheets.
    """

    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.HEALTH_WORKOUT_METRICS_WORKSHEET
    )

    rows = worksheet.get_all_values()

    if not rows:
        return

    headers = rows[0]
    start_time_column_index = headers.index("Workout Start Time")

    matching_row_numbers = []

    for sheet_row_number, row in enumerate(rows[1:], start=2):

        if (
            len(row) > start_time_column_index
            and row[start_time_column_index]
            == TEST_SHEET_WORKOUT_START_TIME
        ):
            matching_row_numbers.append(sheet_row_number)

    # Delete bottom-to-top so row numbers do not shift.
    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)


def get_test_row_from_google_sheets() -> dict | None:
    """
    Return the E2E test workout row directly from Google Sheets.
    """

    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        settings.HEALTH_WORKOUT_METRICS_WORKSHEET
    )

    rows = worksheet.get_all_records()

    for row in rows:

        if (
            row["Workout Start Time"]
            == TEST_SHEET_WORKOUT_START_TIME
        ):
            return row

    return None


def test_workout_metrics_e2e():

    # Remove any test rows left behind by previous interrupted tests.
    delete_test_rows_from_google_sheets()

    try:

        # ---------------------------------------------------------
        # 1. CREATE
        # ---------------------------------------------------------

        create_payload = {
            "date": TEST_DATE,
            "workout_type": "Running",
            "workout_start_time": TEST_WORKOUT_START_TIME,
            "workout_end_time": "2099-01-01T11:00:00",
            "workout_duration_min": 60,
            "total_energy_kcal": 600,
            "active_energy_kcal": 500,
            "max_heart_rate_bpm": 175,
            "avg_heart_rate_bpm": 145,
            "distance_km": 5.0,
            "avg_speed_kmph": 5.0,
            "source": TEST_SOURCE,
        }

        response = requests.post(
            f"{BASE_URL}/health/workout-metrics",
            json=create_payload,
            timeout=10,
        )

        assert response.status_code == 201, response.text

        # ---------------------------------------------------------
        # 2. READ BY WORKOUT START TIME
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/workout-metric",
            params={
                "workout_start_time": TEST_WORKOUT_START_TIME
            },
            timeout=10,
        )

        assert response.status_code == 200, response.text

        workout_metric = response.json()

        assert workout_metric["date"] == TEST_DATE
        assert workout_metric["workout_type"] == "Running"

        assert (
            workout_metric["workout_start_time"]
            == TEST_WORKOUT_START_TIME
        )

        assert (
            workout_metric["workout_end_time"]
            == "2099-01-01T11:00:00"
        )

        assert workout_metric["workout_duration_min"] == 60

        assert workout_metric["total_energy_kcal"] == 600
        assert workout_metric["active_energy_kcal"] == 500
        assert workout_metric["max_heart_rate_bpm"] == 175
        assert workout_metric["avg_heart_rate_bpm"] == 145
        assert workout_metric["distance_km"] == 5.0
        assert workout_metric["avg_speed_kmph"] == 5.0

        assert workout_metric["source"] == TEST_SOURCE

        # ---------------------------------------------------------
        # 3. READ BY DATE
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/workout-metrics",
            params={
                "workout_date": TEST_DATE
            },
            timeout=10,
        )

        assert response.status_code == 200, response.text

        workouts = response.json()

        matching_workouts = [
            workout
            for workout in workouts
            if workout["workout_start_time"]
            == TEST_WORKOUT_START_TIME
        ]

        assert len(matching_workouts) == 1

        assert matching_workouts[0]["source"] == TEST_SOURCE

        # ---------------------------------------------------------
        # 4. VERIFY CREATE METADATA IN GOOGLE SHEETS
        # ---------------------------------------------------------

        created_sheet_row = get_test_row_from_google_sheets()

        assert created_sheet_row is not None

        # Verify Workout Metrics values stored in Google Sheets.
        assert created_sheet_row["Workout Duration (min)"] == 60
        assert created_sheet_row["Distance (km)"] == 5.0
        assert created_sheet_row["Avg Speed (km/hr)"] == 5.0
        # Verify metadata.
        assert created_sheet_row["Source"] == TEST_SOURCE

        created_updated_datetime = datetime.strptime(
            created_sheet_row["Updated_DateTime"],
            DATETIME_FORMAT,
        )

        # Updated_DateTime has second-level precision.
        # Ensure the PUT occurs in a later second.
        time.sleep(1.1)

        # ---------------------------------------------------------
        # 5. UPDATE
        # ---------------------------------------------------------

        update_payload = {
            "date": TEST_DATE,
            "workout_type": "Outdoor Running",
            "workout_start_time": TEST_WORKOUT_START_TIME,
            "workout_end_time": "2099-01-01T11:15:00",
            "workout_duration_min": 75,
            "active_energy_kcal": 650,
            "distance_km": 6.0,
            "source": TEST_SOURCE,
        }

        response = requests.put(
            f"{BASE_URL}/health/workout-metrics",
            json=update_payload,
            timeout=10,
        )

        assert response.status_code == 200, response.text

        # ---------------------------------------------------------
        # 6. READ AGAIN AND VERIFY UPDATE
        # ---------------------------------------------------------

        response = requests.get(
            f"{BASE_URL}/health/workout-metric",
            params={
                "workout_start_time": TEST_WORKOUT_START_TIME
            },
            timeout=10,
        )

        assert response.status_code == 200, response.text

        updated_workout = response.json()

        # Unique key must remain unchanged.
        assert (
            updated_workout["workout_start_time"]
            == TEST_WORKOUT_START_TIME
        )

        # Verify changed fields.
        assert updated_workout["workout_type"] == "Outdoor Running"

        assert (
            updated_workout["workout_end_time"]
            == "2099-01-01T11:15:00"
        )

        assert updated_workout["workout_duration_min"] == 75
        assert updated_workout["active_energy_kcal"] == 650
        assert updated_workout["distance_km"] == 6.0

        # Verify unchanged fields were preserved.
        assert updated_workout["total_energy_kcal"] == 600
        assert updated_workout["max_heart_rate_bpm"] == 175
        assert updated_workout["avg_heart_rate_bpm"] == 145
        assert updated_workout["avg_speed_kmph"] == 5.0

        assert updated_workout["source"] == TEST_SOURCE

        # ---------------------------------------------------------
        # 7. VERIFY UPDATE METADATA IN GOOGLE SHEETS
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

        # Always remove test rows, even when an assertion fails.
        delete_test_rows_from_google_sheets()