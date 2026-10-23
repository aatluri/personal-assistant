from datetime import date, datetime
from unittest.mock import Mock

from app.modules.health.workout_metrics.workout_metrics_google_sheets_repository import (
    WorkoutMetricsGoogleSheetsRepository,
)
from tests.helpers.test_data import (
    create_workout_metric,
    create_workout_metric_row,
)


# ============================================================================
# Workout Metrics
# ============================================================================


# Verify that all Workout Metrics are retrieved and converted correctly.
def test_get_workout_metrics():
    repository = WorkoutMetricsGoogleSheetsRepository()

    worksheet = Mock()

    worksheet.get_all_records.return_value = [
        create_workout_metric_row()
    ]

    repository._get_workout_metrics_worksheet = Mock(
        return_value=worksheet
    )

    workout_metrics = repository.get_workout_metrics()

    assert len(workout_metrics) == 1

    workout_metric = workout_metrics[0]

    assert workout_metric.workout_type == "Functional Strength Training"

    assert workout_metric.workout_start_time == datetime(
        2026, 10, 8, 6, 30, 0
    )

    assert workout_metric.total_energy_kcal == 500
    assert workout_metric.active_energy_kcal == 420

    assert workout_metric.source == "Apple Watch"

    worksheet.get_all_records.assert_called_once()


# Verify that Workout Metrics are returned when the requested
# Workout Start Time exists.
def test_get_workout_metric_found():
    repository = WorkoutMetricsGoogleSheetsRepository()

    repository.get_workout_metrics = Mock(
        return_value=[
            create_workout_metric(),
        ]
    )

    workout_metric = repository.get_workout_metric(
        datetime(2026, 10, 8, 6, 30, 0)
    )

    assert workout_metric is not None

    assert workout_metric.workout_start_time == datetime(
        2026, 10, 8, 6, 30, 0
    )


# Verify that a timezone-aware Workout Start Time matches
# the same stored Workout Start Time without timezone information.
def test_get_workout_metric_matches_timezone_aware_datetime():
    repository = WorkoutMetricsGoogleSheetsRepository()

    repository.get_workout_metrics = Mock(
        return_value=[
            create_workout_metric(),
        ]
    )

    workout_metric = repository.get_workout_metric(
        datetime.fromisoformat(
            "2026-10-08T06:30:00+05:30"
        )
    )

    assert workout_metric is not None

    assert workout_metric.workout_start_time == datetime(
        2026, 10, 8, 6, 30, 0
    )


# Verify that None is returned when the requested
# Workout Metrics record does not exist.
def test_get_workout_metric_not_found():
    repository = WorkoutMetricsGoogleSheetsRepository()

    repository.get_workout_metrics = Mock(
        return_value=[]
    )

    workout_metric = repository.get_workout_metric(
        datetime(2026, 10, 8, 6, 30, 0)
    )

    assert workout_metric is None


# Verify that a new Workout Metrics record is appended
# to the worksheet.
def test_create_workout_metric():
    repository = WorkoutMetricsGoogleSheetsRepository()

    worksheet = Mock()

    repository._get_workout_metrics_worksheet = Mock(
        return_value=worksheet
    )

    workout_metric = create_workout_metric()

    repository.create_workout_metric(
        workout_metric
    )

    worksheet.append_row.assert_called_once()

    appended_row = worksheet.append_row.call_args.args[0]

    assert appended_row[0] == "October 08, 2026"
    assert appended_row[1] == "Functional Strength Training"

    assert appended_row[11] == "Apple Watch"

    assert len(appended_row) == 13

    datetime.strptime(
        appended_row[12],
        "%B %d, %Y %H:%M:%S",
    )

    assert (
        worksheet.append_row.call_args.kwargs["value_input_option"]
        == "USER_ENTERED"
    )


# Verify that an existing Workout Metrics record is updated
# when the Workout Start Time is found.
def test_update_workout_metric_found():
    repository = WorkoutMetricsGoogleSheetsRepository()

    worksheet = Mock()

    existing_row = create_workout_metric_row()

    headers = list(existing_row.keys())
    values = list(existing_row.values())

    worksheet.get_all_values.return_value = [
        headers,
        values,
    ]

    repository._get_workout_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated_workout_metric = create_workout_metric()

    # These fields should be updated.
    updated_workout_metric.total_energy_kcal = 550
    updated_workout_metric.avg_heart_rate_bpm = 150
    updated_workout_metric.source = "Health Auto Export"

    # These fields should retain their existing values.
    updated_workout_metric.distance_km = None
    updated_workout_metric.max_heart_rate_bpm = None

    updated = repository.update_workout_metric(
        datetime(2026, 10, 8, 6, 30, 0),
        updated_workout_metric,
    )

    assert updated is True

    worksheet.update.assert_called_once()

    assert (
        worksheet.update.call_args.kwargs["range_name"]
        == "A2:M2"
    )

    updated_row = worksheet.update.call_args.kwargs["values"][0]

    # Supplied values should be updated.
    assert updated_row[5] == 550
    assert updated_row[8] == 150
    assert updated_row[11] == "Health Auto Export"

    # None values should preserve existing values.
    assert updated_row[7] == 175
    assert updated_row[9] == 3.2

    # Unique key should remain unchanged.
    assert updated_row[2] == "October 08, 2026 06:30:00"

    assert len(updated_row) == 13

    datetime.strptime(
        updated_row[12],
        "%B %d, %Y %H:%M:%S",
    )

    assert (
        worksheet.update.call_args.kwargs["value_input_option"]
        == "USER_ENTERED"
    )


# Verify that an existing Workout Metrics record is updated
# when the incoming Workout Start Time contains timezone information.
def test_update_workout_metric_matches_timezone_aware_datetime():
    repository = WorkoutMetricsGoogleSheetsRepository()

    worksheet = Mock()

    # Start with a complete worksheet row because the update
    # operation now reads and merges the existing record.
    existing_row = create_workout_metric_row()

    existing_row["Date"] = "July 02, 2026"
    existing_row["Workout Type"] = "Outdoor Run"
    existing_row["Workout Start Time"] = "July 02, 2026 15:40:44"

    headers = list(existing_row.keys())
    values = list(existing_row.values())

    worksheet.get_all_values.return_value = [
        headers,
        values,
    ]

    repository._get_workout_metrics_worksheet = Mock(
        return_value=worksheet
    )

    incoming_start_time = datetime.fromisoformat(
        "2026-07-02T15:40:44+05:30"
    )

    workout_metric = create_workout_metric().model_copy(
        update={
            "date": date(2026, 7, 2),
            "workout_start_time": incoming_start_time,
        }
    )

    updated = repository.update_workout_metric(
        incoming_start_time,
        workout_metric,
    )

    assert updated is True

    worksheet.update.assert_called_once()

    assert (
        worksheet.update.call_args.kwargs["range_name"]
        == "A2:M2"
    )

    updated_row = worksheet.update.call_args.kwargs["values"][0]

    # The stored unique key should remain unchanged.
    assert updated_row[2] == "July 02, 2026 15:40:44"

    assert updated_row[11] == "Apple Watch"

    assert len(updated_row) == 13

    datetime.strptime(
        updated_row[12],
        "%B %d, %Y %H:%M:%S",
    )


# Verify that no update occurs when the Workout Start Time
# is not found.
def test_update_workout_metric_not_found():
    repository = WorkoutMetricsGoogleSheetsRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        [
            "Date",
            "Workout Type",
            "Workout Start Time",
        ],
        [
            "October 08, 2026",
            "Functional Strength Training",
            "October 08, 2026 07:30:00",
        ],
    ]

    repository._get_workout_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_workout_metric(
        datetime(2026, 10, 8, 6, 30, 0),
        create_workout_metric(),
    )

    assert updated is False

    worksheet.update.assert_not_called()


# Verify that Workout Metrics can be filtered by date.
def test_get_workout_metrics_by_date():
    repository = WorkoutMetricsGoogleSheetsRepository()

    workout_1 = create_workout_metric()

    workout_2 = create_workout_metric().model_copy(
        update={
            "workout_start_time": datetime(
                2026,
                10,
                8,
                18,
                30,
            )
        }
    )

    workout_3 = create_workout_metric().model_copy(
        update={
            "date": date(2026, 10, 9),
            "workout_start_time": datetime(
                2026,
                10,
                9,
                6,
                30,
            ),
        }
    )

    repository.get_workout_metrics = Mock(
        return_value=[
            workout_1,
            workout_2,
            workout_3,
        ]
    )

    result = repository.get_workout_metrics_by_date(
        date(2026, 10, 8)
    )

    assert result == [
        workout_1,
        workout_2,
    ]


# Verify that an empty list is returned when no workouts
# exist for the requested date.
def test_get_workout_metrics_by_date_no_workouts():
    repository = WorkoutMetricsGoogleSheetsRepository()

    repository.get_workout_metrics = Mock(
        return_value=[
            create_workout_metric(),
        ]
    )

    result = repository.get_workout_metrics_by_date(
        date(2026, 10, 9)
    )

    assert result == []


# ============================================================================
# Workout Metrics Repository Helper Tests
# ============================================================================


# Verify that a WorkoutMetrics object is correctly converted
# into a Google Sheets row.
def test_workout_metric_to_row():
    repository = WorkoutMetricsGoogleSheetsRepository()

    workout_metric = create_workout_metric()

    row = repository._workout_metric_to_row(
        workout_metric
    )

    assert row[0] == "October 08, 2026"
    assert row[1] == "Functional Strength Training"
    assert row[2] == "October 08, 2026 06:30:00"
    assert row[3] == "October 08, 2026 07:30:00"
    assert row[4] == 60

    assert row[5] == 500
    assert row[6] == 420
    assert row[7] == 175
    assert row[8] == 145
    assert row[9] == 3.2
    assert row[10] == 6.4

    assert row[11] == "Apple Watch"

    assert len(row) == 13

    datetime.strptime(
        row[12],
        "%B %d, %Y %H:%M:%S",
    )


# Verify that a Google Sheets row is correctly converted
# into a WorkoutMetrics object.
def test_row_to_workout_metric():
    repository = WorkoutMetricsGoogleSheetsRepository()

    row = create_workout_metric_row()

    workout_metric = repository._row_to_workout_metrics(
        row
    )

    assert workout_metric.date == date(2026, 10, 8)
    assert workout_metric.workout_type == "Functional Strength Training"

    assert workout_metric.workout_start_time == datetime(
        2026, 10, 8, 6, 30, 0
    )

    assert workout_metric.workout_end_time == datetime(
        2026, 10, 8, 7, 30, 0
    )

    assert workout_metric.workout_duration_min == 60

    assert workout_metric.total_energy_kcal == 500
    assert workout_metric.active_energy_kcal == 420
    assert workout_metric.max_heart_rate_bpm == 175
    assert workout_metric.avg_heart_rate_bpm == 145
    assert workout_metric.distance_km == 3.2
    assert workout_metric.avg_speed_kmph == 6.4

    assert workout_metric.source == "Apple Watch"