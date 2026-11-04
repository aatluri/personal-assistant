from datetime import date,datetime
from unittest.mock import Mock

from app.modules.health.workout_metrics.workout_metrics_service import (
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

# ============================================================================
# Missing workout duration
#
# When the incoming duration is 0 or empty, the service keeps a real stored
# duration, otherwise calculates it from the start and end times (1 minute
# to 24 hours), otherwise saves it as sent.
# ============================================================================


def make_workout_metric(**overrides):
    """
    Return the standard test workout (06:30 to 07:30) with overrides.
    """

    return create_workout_metric().model_copy(update=overrides)


def saved_workout_metric(repository: Mock):
    """
    Return the record the service passed to update_workout_metric().
    """

    return repository.update_workout_metric.call_args.args[1]


# Verify that a real incoming duration is saved as sent, without a lookup.

def test_upsert_workout_metric_keeps_real_incoming_duration():

    service = WorkoutMetricsService()
    repository = Mock()
    service._repository = repository

    workout_metric = make_workout_metric(workout_duration_min=45)

    service.upsert_workout_metric(
        workout_metric.workout_start_time,
        workout_metric,
    )

    assert saved_workout_metric(repository).workout_duration_min == 45
    repository.get_workout_metric.assert_not_called()


# Verify that an empty duration is calculated from the start and end times.

def test_upsert_workout_metric_calculates_empty_duration():

    service = WorkoutMetricsService()
    repository = Mock()
    repository.get_workout_metric.return_value = None
    service._repository = repository

    # 06:30 to 07:30 is 60 minutes.
    workout_metric = make_workout_metric(workout_duration_min=None)

    service.upsert_workout_metric(
        workout_metric.workout_start_time,
        workout_metric,
    )

    assert saved_workout_metric(repository).workout_duration_min == 60


# Verify that a duration of 0 is treated as missing and calculated.

def test_upsert_workout_metric_calculates_zero_duration():

    service = WorkoutMetricsService()
    repository = Mock()
    repository.get_workout_metric.return_value = None
    service._repository = repository

    workout_metric = make_workout_metric(
        workout_duration_min=0,
        workout_end_time=datetime(2026, 10, 8, 7, 12, 40),
    )

    service.upsert_workout_metric(
        workout_metric.workout_start_time,
        workout_metric,
    )

    # 06:30:00 to 07:12:40 is 42.7 minutes, rounded to 43.
    assert saved_workout_metric(repository).workout_duration_min == 43


# Verify that a real stored duration is never overwritten by an incoming 0.

def test_upsert_workout_metric_keeps_existing_real_duration_when_zero_sent():

    service = WorkoutMetricsService()
    repository = Mock()
    repository.get_workout_metric.return_value = make_workout_metric(
        workout_duration_min=55
    )
    service._repository = repository

    workout_metric = make_workout_metric(workout_duration_min=0)

    service.upsert_workout_metric(
        workout_metric.workout_start_time,
        workout_metric,
    )

    # None tells the update to keep the stored 55.
    assert saved_workout_metric(repository).workout_duration_min is None


# Verify that an implausible span keeps the incoming 0.

def test_upsert_workout_metric_outlier_keeps_incoming_zero():

    service = WorkoutMetricsService()
    repository = Mock()
    repository.get_workout_metric.return_value = None
    service._repository = repository

    # An end time before the start time cannot be a real workout.
    workout_metric = make_workout_metric(
        workout_duration_min=0,
        workout_end_time=datetime(2026, 10, 8, 6, 0, 0),
    )

    service.upsert_workout_metric(
        workout_metric.workout_start_time,
        workout_metric,
    )

    assert saved_workout_metric(repository).workout_duration_min == 0


# Verify that creating a record also calculates a missing duration.

def test_create_workout_metric_calculates_missing_duration():

    service = WorkoutMetricsService()
    repository = Mock()
    repository.get_workout_metric.return_value = None
    service._repository = repository

    workout_metric = make_workout_metric(workout_duration_min=None)

    service.create_workout_metric(workout_metric)

    created = repository.create_workout_metric.call_args.args[0]

    assert created.workout_duration_min == 60
