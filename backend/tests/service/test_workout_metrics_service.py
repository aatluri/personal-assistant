from datetime import date,datetime
from unittest.mock import Mock

from app.modules.health.workout_metrics_service import (
    WorkoutMetricsService,
)
from tests.helpers.test_data import create_workout_metric


# ============================================================================
# Workout Metrics
# ============================================================================


# Verify that all Workout Metrics are retrieved from the repository.

def test_get_workout_metrics():

    service = WorkoutMetricsService()

    repository = Mock()

    repository.get_workout_metrics.return_value = [
        create_workout_metric()
    ]

    service._repository = repository

    workout_metrics = service.get_workout_metrics()

    assert len(workout_metrics) == 1

    assert workout_metrics[0].workout_start_time == datetime(
        2026, 10, 8, 6, 30, 0
    )

    repository.get_workout_metrics.assert_called_once()



# Verify that Workout Metrics are returned when the requested
# Workout Start Time exists.

def test_get_workout_metric():

    service = WorkoutMetricsService()

    repository = Mock()

    repository.get_workout_metric.return_value = (
        create_workout_metric()
    )

    service._repository = repository

    workout_metric = service.get_workout_metric(
        datetime(2026, 10, 8, 6, 30, 0)
    )

    assert workout_metric is not None

    assert workout_metric.workout_start_time == datetime(
        2026, 10, 8, 6, 30, 0
    )

    repository.get_workout_metric.assert_called_once_with(
        datetime(2026, 10, 8, 6, 30, 0)
    )


# Verify that a new Workout Metrics record is created
# through the repository.

def test_create_workout_metric():

    service = WorkoutMetricsService()

    repository = Mock()

    service._repository = repository

    workout_metric = create_workout_metric()

    service.create_workout_metric(
        workout_metric
    )

    repository.create_workout_metric.assert_called_once_with(
        workout_metric
    )


# Verify that an existing Workout Metrics record is updated.

def test_upsert_workout_metric_update():

    service = WorkoutMetricsService()

    repository = Mock()

    repository.update_workout_metric.return_value = True

    service._repository = repository

    workout_metric = create_workout_metric()

    workout_start_time = datetime(
        2026, 10, 8, 6, 30, 0
    )

    service.upsert_workout_metric(
        workout_start_time,
        workout_metric,
    )

    repository.update_workout_metric.assert_called_once_with(
        workout_start_time,
        workout_metric,
    )

    repository.create_workout_metric.assert_not_called()


# Verify that a new Workout Metrics record is created
# when no existing record is found.

def test_upsert_workout_metric_create():

    service = WorkoutMetricsService()

    repository = Mock()

    repository.update_workout_metric.return_value = False

    service._repository = repository

    workout_metric = create_workout_metric()

    workout_start_time = datetime(
        2026, 10, 8, 6, 30, 0
    )

    service.upsert_workout_metric(
        workout_start_time,
        workout_metric,
    )

    repository.update_workout_metric.assert_called_once_with(
        workout_start_time,
        workout_metric,
    )

    repository.create_workout_metric.assert_called_once_with(
        workout_metric
    )

def test_get_workout_metrics_by_date():
    service = WorkoutMetricsService()

    workout_metrics = [
        create_workout_metric(),
    ]

    service._repository = Mock()
    service._repository.get_workout_metrics_by_date.return_value = (
        workout_metrics
    )

    result = service.get_workout_metrics_by_date(
        date(2026, 10, 8)
    )

    assert result == workout_metrics

    service._repository.get_workout_metrics_by_date.assert_called_once_with(
        date(2026, 10, 8)
    )