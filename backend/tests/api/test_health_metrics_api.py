from datetime import date
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.modules.health import api
from tests.helpers.test_data import (
    create_health_metric,
)


client = TestClient(app)


"""
Health Metrics API Tests

These tests verify the HTTP API layer for Health Metrics.

The real HealthMetricsService is replaced with a mock so that
the API can be tested independently of the service and
repository layers.
"""


# ============================================================================
# Health Metrics
# ============================================================================


# Verify that all Health Metrics records are returned successfully.

def test_get_health_metrics():
    service = Mock()

    service.get_health_metrics.return_value = [
        create_health_metric()
    ]

    api.health_metrics_service = service

    response = client.get(
        "/health/health-metrics"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    service.get_health_metrics.assert_called_once()


# Verify that Health Metrics are returned when the requested date exists.

def test_get_health_metric_found():
    service = Mock()

    service.get_health_metric.return_value = (
        create_health_metric()
    )

    api.health_metrics_service = service

    response = client.get(
        "/health/health-metrics/2026-10-08"
    )

    assert response.status_code == 200

    service.get_health_metric.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that a 404 response is returned when Health Metrics do not exist.

def test_get_health_metric_not_found():
    service = Mock()

    service.get_health_metric.return_value = None

    api.health_metrics_service = service

    response = client.get(
        "/health/health-metrics/2026-10-08"
    )

    assert response.status_code == 404

    service.get_health_metric.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that a new Health Metrics record can be created.

def test_create_health_metric():
    service = Mock()

    api.health_metrics_service = service

    health_metric = create_health_metric()

    response = client.post(
        "/health/health-metrics",
        json=health_metric.model_dump(
            mode="json"
        ),
    )

    assert response.status_code == 201

    service.create_health_metric.assert_called_once_with(
        health_metric
    )


# Verify that a Health Metrics record can be updated or created.

def test_update_health_metric():
    service = Mock()

    api.health_metrics_service = service

    health_metric = create_health_metric()

    payload = health_metric.model_dump(
        mode="json"
    )

    response = client.put(
        "/health/health-metrics",
        json=payload,
    )

    assert response.status_code == 200

    service.upsert_health_metric.assert_called_once_with(
        health_metric.date,
        health_metric,
    )