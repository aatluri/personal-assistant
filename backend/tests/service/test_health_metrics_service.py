from datetime import date
from unittest.mock import Mock

from app.modules.health.health_metrics_service import (
    HealthMetricsService,
)
from tests.helpers.test_data import create_health_metric


# ============================================================================
# Health Metrics
# ============================================================================

# Verify that all Health Metrics are retrieved from the repository.

def test_get_health_metrics():

    service = HealthMetricsService()

    repository = Mock()

    repository.get_health_metrics.return_value = [
        create_health_metric()
    ]

    service._repository = repository

    health_metrics = service.get_health_metrics()

    assert len(health_metrics) == 1
    assert health_metrics[0].date == date(2026, 10, 8)

    repository.get_health_metrics.assert_called_once()


# Verify that Health Metrics are returned when the requested date exists.

def test_get_health_metric():

    service = HealthMetricsService()

    repository = Mock()

    repository.get_health_metric.return_value = (
        create_health_metric()
    )

    service._repository = repository

    health_metric = service.get_health_metric(
        date(2026, 10, 8)
    )

    assert health_metric is not None
    assert health_metric.date == date(2026, 10, 8)

    repository.get_health_metric.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that a new Health Metrics record is created through the repository.

def test_create_health_metric():

    service = HealthMetricsService()

    repository = Mock()

    service._repository = repository

    health_metric = create_health_metric()

    service.create_health_metric(
        health_metric
    )

    repository.create_health_metric.assert_called_once_with(
        health_metric
    )


# Verify that an existing Health Metrics record is updated.

def test_upsert_health_metric_update():

    service = HealthMetricsService()

    repository = Mock()

    repository.update_health_metric.return_value = True

    service._repository = repository

    health_metric = create_health_metric()

    service.upsert_health_metric(
        date(2026, 10, 8),
        health_metric,
    )

    repository.update_health_metric.assert_called_once_with(
        date(2026, 10, 8),
        health_metric,
    )

    repository.create_health_metric.assert_not_called()


# Verify that a new Health Metrics record is created when no existing record is found.

def test_upsert_health_metric_create():

    service = HealthMetricsService()

    repository = Mock()

    repository.update_health_metric.return_value = False

    service._repository = repository

    health_metric = create_health_metric()

    service.upsert_health_metric(
        date(2026, 10, 8),
        health_metric,
    )

    repository.update_health_metric.assert_called_once()

    repository.create_health_metric.assert_called_once_with(
        health_metric
    )