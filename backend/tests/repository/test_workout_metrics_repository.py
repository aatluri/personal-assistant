"""
Workout Metrics Repository Tests

Each test follows the same sequence:

1. Create a Workout Metrics instance.
2. Create a mock worksheet (instead of connecting to Google Sheets).
3. Configure the mock worksheet to return predefined data.
4. Replace the repository's worksheet with the mock.
5. Call the repository method being tested.
6. Verify that the repository returns the expected result
   or calls the worksheet with the expected arguments.
"""

from datetime import datetime
from unittest.mock import Mock

from app.modules.health.workout_metrics_repository import (
    WorkoutMetricsRepository,
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

    repository = WorkoutMetricsRepository()

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

    worksheet.get_all_records.assert_called_once()


# Verify that Workout Metrics are returned when the requested
# Workout Start Time exists.

def test_get_workout_metric_found():

    repository = WorkoutMetricsRepository()

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


# Verify that None is returned when the requested
# Workout Metrics record does not exist.

def test_get_workout_metric_not_found():

    repository = WorkoutMetricsRepository()

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

    repository = WorkoutMetricsRepository()

    worksheet = Mock()

    repository._get_workout_metrics_worksheet = Mock(
        return_value=worksheet
    )

    workout_metric = create_workout_metric()

    repository.create_workout_metric(
        workout_metric
    )

    worksheet.append_row.assert_called_once_with(
        repository._workout_metric_to_row(
            workout_metric
        ),
        value_input_option="USER_ENTERED",
    )


# Verify that an existing Workout Metrics record is updated
# when the Workout Start Time is found.

def test_update_workout_metric_found():

    repository = WorkoutMetricsRepository()

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
            "October 08, 2026 06:30:00",
        ],
    ]

    repository._get_workout_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_workout_metric(
        datetime(2026, 10, 8, 6, 30, 0),
        create_workout_metric(),
    )

    assert updated is True

    worksheet.update.assert_called_once()


# Verify that no update occurs when the Workout Start Time
# is not found.

def test_update_workout_metric_not_found():

    repository = WorkoutMetricsRepository()

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