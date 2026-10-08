from datetime import date, datetime, timedelta


from app.modules.health.workout_metrics_repository import (
    WorkoutMetricsRepository,
)

from tests.helpers.test_data import (
    create_workout_metric,
    create_workout_metric_row,
)


# ============================================================================
# Workout Metrics Repository Helper Tests
# ============================================================================


# Verify that a WorkoutMetrics object is correctly converted
# into a Google Sheets row.

def test_workout_metric_to_row():

    repository = WorkoutMetricsRepository()

    workout_metric = create_workout_metric()

    row = repository._workout_metric_to_row(
        workout_metric
    )

    assert row[0] == "October 08, 2026"
    assert row[1] == "Functional Strength Training"
    assert row[2] == "October 08, 2026 06:30:00"
    assert row[3] == "October 08, 2026 07:30:00"
    assert row[4] == "01:00:00"

    assert row[5] == 500
    assert row[6] == 420
    assert row[7] == 175
    assert row[8] == 145
    assert row[9] == 3.2
    assert row[10] == 6.4


# Verify that a Google Sheets row is correctly converted
# into a WorkoutMetrics object.

def test_row_to_workout_metric():

    repository = WorkoutMetricsRepository()

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

    assert workout_metric.workout_duration == timedelta(
        hours=1
    )

    assert workout_metric.total_energy_kcal == 500
    assert workout_metric.active_energy_kcal == 420
    assert workout_metric.max_heart_rate_bpm == 175
    assert workout_metric.avg_heart_rate_bpm == 145
    assert workout_metric.distance_mi == 3.2
    assert workout_metric.avg_speed_mph == 6.4


# Verify that an HH:MM:SS duration is converted
# into a Python timedelta.

def test_duration_to_timedelta():

    repository = WorkoutMetricsRepository()

    duration = repository._duration_to_timedelta(
        "01:30:45"
    )

    assert duration == timedelta(
        hours=1,
        minutes=30,
        seconds=45,
    )


# Verify that a Python timedelta is converted
# into an HH:MM:SS duration.

def test_timedelta_to_duration():

    repository = WorkoutMetricsRepository()

    duration = timedelta(
        hours=1,
        minutes=30,
        seconds=45,
    )

    result = repository._timedelta_to_duration(
        duration
    )

    assert result == "01:30:45"