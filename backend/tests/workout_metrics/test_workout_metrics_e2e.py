import requests

from app.config import settings
from app.database.sheets_client import get_spreadsheet


BASE_URL = "http://127.0.0.1:8000"

TEST_DATE = "2099-01-01"
TEST_WORKOUT_START_TIME = "2099-01-01T10:00:00"
TEST_SHEET_WORKOUT_START_TIME = "January 01, 2099 10:00:00"


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
            and row[start_time_column_index] == TEST_SHEET_WORKOUT_START_TIME
        ):
            matching_row_numbers.append(sheet_row_number)

    # Delete bottom-to-top so row numbers do not shift.
    for sheet_row_number in reversed(matching_row_numbers):
        worksheet.delete_rows(sheet_row_number)


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
            "workout_duration": "01:00:00",
            "total_energy_kcal": 600,
            "active_energy_kcal": 500,
            "max_heart_rate_bpm": 175,
            "avg_heart_rate_bpm": 145,
            "distance_mi": 5.0,
            "avg_speed_mph": 5.0,
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

        assert workout_metric["workout_duration"] == "01:00:00"

        assert workout_metric["total_energy_kcal"] == 600
        assert workout_metric["active_energy_kcal"] == 500
        assert workout_metric["max_heart_rate_bpm"] == 175
        assert workout_metric["avg_heart_rate_bpm"] == 145
        assert workout_metric["distance_mi"] == 5.0
        assert workout_metric["avg_speed_mph"] == 5.0

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

        # ---------------------------------------------------------
        # 4. UPDATE
        # ---------------------------------------------------------

        update_payload = create_payload.copy()

        update_payload["workout_type"] = "Outdoor Running"
        update_payload["workout_end_time"] = "2099-01-01T11:15:00"
        update_payload["workout_duration"] = "01:15:00"
        update_payload["active_energy_kcal"] = 650
        update_payload["distance_mi"] = 6.0

        response = requests.put(
            f"{BASE_URL}/health/workout-metrics",
            json=update_payload,
            timeout=10,
        )

        assert response.status_code == 200, response.text

        # ---------------------------------------------------------
        # 5. READ AGAIN AND VERIFY UPDATE
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

        assert updated_workout["workout_duration"] == "01:15:00"
        assert updated_workout["active_energy_kcal"] == 650
        assert updated_workout["distance_mi"] == 6.0

        # Verify unchanged fields were preserved.
        assert updated_workout["total_energy_kcal"] == 600
        assert updated_workout["max_heart_rate_bpm"] == 175
        assert updated_workout["avg_heart_rate_bpm"] == 145
        assert updated_workout["avg_speed_mph"] == 5.0

    finally:

        # Always remove test rows, even when an assertion fails.
        delete_test_rows_from_google_sheets()