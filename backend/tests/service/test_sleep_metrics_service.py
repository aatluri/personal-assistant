from datetime import date
from unittest.mock import Mock

from app.modules.health.sleep_metrics_service import (
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