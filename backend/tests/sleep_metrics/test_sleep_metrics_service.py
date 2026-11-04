from datetime import date, datetime, timedelta, timezone
from unittest.mock import Mock

from app.modules.health.sleep_metrics.sleep_metrics_service import (
    SleepMetricsService,
)
from tests.helpers.test_data import create_sleep_metric


# ============================================================================
# Sleep Metrics
# ============================================================================

# Verify that all Sleep Metrics are retrieved from the repository.

def test_get_sleep_metrics():

    service = SleepMetricsService()

    repository = Mock()

    repository.get_sleep_metrics.return_value = [
        create_sleep_metric()
    ]

    service._repository = repository

    sleep_metrics = service.get_sleep_metrics()

    assert len(sleep_metrics) == 1
    assert sleep_metrics[0].date == date(2026, 10, 8)

    repository.get_sleep_metrics.assert_called_once()


# Verify that Sleep Metrics are returned when the requested date exists.

def test_get_sleep_metric():

    service = SleepMetricsService()

    repository = Mock()

    repository.get_sleep_metric.return_value = (
        create_sleep_metric()
    )

    service._repository = repository

    sleep_metric = service.get_sleep_metric(
        date(2026, 10, 8)
    )

    assert sleep_metric is not None
    assert sleep_metric.date == date(2026, 10, 8)

    repository.get_sleep_metric.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that a new Sleep Metrics record is created through the repository.

def test_create_sleep_metric():

    service = SleepMetricsService()

    repository = Mock()

    service._repository = repository

    sleep_metric = create_sleep_metric()

    service.create_sleep_metric(
        sleep_metric
    )

    repository.create_sleep_metric.assert_called_once_with(
        sleep_metric
    )


# Verify that an existing Sleep Metrics record is updated.

def test_upsert_sleep_metric_update():

    service = SleepMetricsService()

    repository = Mock()

    repository.update_sleep_metric.return_value = True

    service._repository = repository

    sleep_metric = create_sleep_metric()

    service.upsert_sleep_metric(
        date(2026, 10, 8),
        sleep_metric,
    )

    repository.update_sleep_metric.assert_called_once_with(
        date(2026, 10, 8),
        sleep_metric,
    )

    repository.create_sleep_metric.assert_not_called()


# Verify that a new Sleep Metrics record is created when no existing record is found.

def test_upsert_sleep_metric_create():

    service = SleepMetricsService()

    repository = Mock()

    repository.update_sleep_metric.return_value = False

    service._repository = repository

    sleep_metric = create_sleep_metric()

    service.upsert_sleep_metric(
        date(2026, 10, 8),
        sleep_metric,
    )

    repository.update_sleep_metric.assert_called_once()

    repository.create_sleep_metric.assert_called_once_with(
        sleep_metric
    )

# ============================================================================
# Missing total sleep duration
#
# When the incoming total is 0 or empty, the service keeps a real stored
# total, otherwise calculates it from the start and end times (1 to 16
# hours), otherwise saves it as sent.
# ============================================================================


def saved_sleep_metric(repository: Mock):
    """
    Return the record the service passed to update_sleep_metric().
    """

    return repository.update_sleep_metric.call_args.args[1]


# Verify that a real incoming total is saved as sent, without a lookup.

def test_upsert_sleep_metric_keeps_real_incoming_total():

    service = SleepMetricsService()
    repository = Mock()
    service._repository = repository

    sleep_metric = create_sleep_metric(total_sleep_duration_hr=7.5)

    service.upsert_sleep_metric(date(2026, 10, 8), sleep_metric)

    assert saved_sleep_metric(repository).total_sleep_duration_hr == 7.5
    repository.get_sleep_metric.assert_not_called()


# Verify that an empty total is calculated from the start and end times.

def test_upsert_sleep_metric_calculates_empty_total():

    service = SleepMetricsService()
    repository = Mock()
    repository.get_sleep_metric.return_value = None
    service._repository = repository

    # 23:00 to 07:00 is 8 hours.
    sleep_metric = create_sleep_metric(total_sleep_duration_hr=None)

    service.upsert_sleep_metric(date(2026, 10, 8), sleep_metric)

    assert saved_sleep_metric(repository).total_sleep_duration_hr == 8.0


# Verify that a total of 0 is treated as missing and calculated.

def test_upsert_sleep_metric_calculates_zero_total():

    service = SleepMetricsService()
    repository = Mock()
    repository.get_sleep_metric.return_value = None
    service._repository = repository

    sleep_metric = create_sleep_metric(
        total_sleep_duration_hr=0.0,
        sleep_start_time=datetime(2026, 10, 7, 23, 30, 0),
        sleep_end_time=datetime(2026, 10, 8, 6, 15, 0),
    )

    service.upsert_sleep_metric(date(2026, 10, 8), sleep_metric)

    # 23:30 to 06:15 is 6.75 hours.
    assert saved_sleep_metric(repository).total_sleep_duration_hr == 6.75


# Verify that a real stored total is never overwritten by an incoming 0.

def test_upsert_sleep_metric_keeps_existing_real_total_when_zero_sent():

    service = SleepMetricsService()
    repository = Mock()
    repository.get_sleep_metric.return_value = create_sleep_metric(
        total_sleep_duration_hr=7.2
    )
    service._repository = repository

    sleep_metric = create_sleep_metric(total_sleep_duration_hr=0.0)

    service.upsert_sleep_metric(date(2026, 10, 8), sleep_metric)

    # None tells the update to keep the stored 7.2.
    assert saved_sleep_metric(repository).total_sleep_duration_hr is None


# Verify that an implausibly short span keeps the incoming 0.

def test_upsert_sleep_metric_outlier_keeps_incoming_zero():

    service = SleepMetricsService()
    repository = Mock()
    repository.get_sleep_metric.return_value = None
    service._repository = repository

    # 07:57 to 08:00 is a 3-minute fragment, not a night's sleep.
    sleep_metric = create_sleep_metric(
        total_sleep_duration_hr=0.0,
        sleep_start_time=datetime(2026, 10, 8, 7, 57, 0),
        sleep_end_time=datetime(2026, 10, 8, 8, 0, 0),
    )

    service.upsert_sleep_metric(date(2026, 10, 8), sleep_metric)

    assert saved_sleep_metric(repository).total_sleep_duration_hr == 0.0


# Verify that an implausibly long span keeps an empty total empty.

def test_upsert_sleep_metric_outlier_keeps_empty_total_empty():

    service = SleepMetricsService()
    repository = Mock()
    repository.get_sleep_metric.return_value = None
    service._repository = repository

    # 20 hours is longer than MAX_SLEEP_HOURS.
    sleep_metric = create_sleep_metric(
        total_sleep_duration_hr=None,
        sleep_start_time=datetime(2026, 10, 7, 12, 0, 0),
        sleep_end_time=datetime(2026, 10, 8, 8, 0, 0),
    )

    service.upsert_sleep_metric(date(2026, 10, 8), sleep_metric)

    assert saved_sleep_metric(repository).total_sleep_duration_hr is None


# Verify that nothing is calculated when a time is missing.

def test_upsert_sleep_metric_not_calculated_without_both_times():

    service = SleepMetricsService()
    repository = Mock()
    repository.get_sleep_metric.return_value = None
    service._repository = repository

    sleep_metric = create_sleep_metric(
        total_sleep_duration_hr=None,
        sleep_start_time=None,
    )

    service.upsert_sleep_metric(date(2026, 10, 8), sleep_metric)

    assert saved_sleep_metric(repository).total_sleep_duration_hr is None


# Verify that the stored times are used when the update does not send any.

def test_upsert_sleep_metric_calculates_from_stored_times():

    service = SleepMetricsService()
    repository = Mock()
    repository.get_sleep_metric.return_value = create_sleep_metric(
        total_sleep_duration_hr=0.0,
        sleep_start_time=datetime(2026, 10, 7, 23, 0, 0),
        sleep_end_time=datetime(2026, 10, 8, 6, 30, 0),
    )
    service._repository = repository

    sleep_metric = create_sleep_metric(
        total_sleep_duration_hr=None,
        sleep_start_time=None,
        sleep_end_time=None,
    )

    service.upsert_sleep_metric(date(2026, 10, 8), sleep_metric)

    # 23:00 to 06:30 is 7.5 hours.
    assert saved_sleep_metric(repository).total_sleep_duration_hr == 7.5


# Verify that timezone-aware incoming times are compared as local times.

def test_upsert_sleep_metric_calculates_with_timezone_aware_times():

    service = SleepMetricsService()
    repository = Mock()
    repository.get_sleep_metric.return_value = None
    service._repository = repository

    ist = timezone(timedelta(hours=5, minutes=30))

    sleep_metric = create_sleep_metric(
        total_sleep_duration_hr=0.0,
        sleep_start_time=datetime(2026, 10, 7, 23, 0, 0, tzinfo=ist),
        sleep_end_time=datetime(2026, 10, 8, 7, 0, 0, tzinfo=ist),
    )

    service.upsert_sleep_metric(date(2026, 10, 8), sleep_metric)

    assert saved_sleep_metric(repository).total_sleep_duration_hr == 8.0


# Verify that creating a record also calculates a missing total.

def test_create_sleep_metric_calculates_missing_total():

    service = SleepMetricsService()
    repository = Mock()
    repository.get_sleep_metric.return_value = None
    service._repository = repository

    sleep_metric = create_sleep_metric(total_sleep_duration_hr=None)

    service.create_sleep_metric(sleep_metric)

    created = repository.create_sleep_metric.call_args.args[0]

    assert created.total_sleep_duration_hr == 8.0
