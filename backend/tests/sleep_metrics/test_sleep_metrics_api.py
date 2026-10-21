from datetime import date
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.modules.health import api
from tests.helpers.test_data import (
    create_sleep_metric,
)


client = TestClient(app)


"""
Sleep Metrics API Tests

These tests verify the HTTP API layer for Sleep Metrics.

The real SleepMetricsService is replaced with a mock so that
the API can be tested independently of the service and
repository layers.
"""


# ============================================================================
# Sleep Metrics
# ============================================================================


# Verify that all Sleep Metrics records are returned successfully.

def test_get_sleep_metrics():
    service = Mock()

    service.get_sleep_metrics.return_value = [
        create_sleep_metric()
    ]

    api.sleep_metrics_service = service

    response = client.get(
        "/health/sleep-metrics"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    service.get_sleep_metrics.assert_called_once()


# Verify that Sleep Metrics are returned when the requested date exists.

def test_get_sleep_metric_found():
    service = Mock()

    service.get_sleep_metric.return_value = (
        create_sleep_metric()
    )

    api.sleep_metrics_service = service

    response = client.get(
        "/health/sleep-metrics/2026-10-08"
    )

    assert response.status_code == 200

    service.get_sleep_metric.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that a 404 response is returned when Sleep Metrics do not exist.

def test_get_sleep_metric_not_found():
    service = Mock()

    service.get_sleep_metric.return_value = None

    api.sleep_metrics_service = service

    response = client.get(
        "/health/sleep-metrics/2026-10-08"
    )

    assert response.status_code == 404

    service.get_sleep_metric.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that a new Sleep Metrics record can be created.

def test_create_sleep_metric():
    service = Mock()

    api.sleep_metrics_service = service

    sleep_metric = create_sleep_metric()

    response = client.post(
        "/health/sleep-metrics",
        json=sleep_metric.model_dump(
            mode="json"
        ),
    )

    assert response.status_code == 201

    service.create_sleep_metric.assert_called_once_with(
        sleep_metric
    )


# Verify that a Sleep Metrics record can be updated or created.

def test_update_sleep_metric():
    service = Mock()

    api.sleep_metrics_service = service

    sleep_metric = create_sleep_metric()

    payload = sleep_metric.model_dump(
        mode="json"
    )

    response = client.put(
        "/health/sleep-metrics",
        json=payload,
    )

    assert response.status_code == 200

    service.upsert_sleep_metric.assert_called_once_with(
        sleep_metric.date,
        sleep_metric,
    )