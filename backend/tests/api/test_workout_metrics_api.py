from datetime import date, datetime
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.modules.health import api
from tests.helpers.test_data import (
    create_workout_metric,
)


client = TestClient(app)


"""
Workout Metrics API Tests

These tests verify the HTTP API layer for Workout Metrics.

The real WorkoutMetricsService is replaced with a mock so that
the API can be tested independently of the service and
repository layers.
"""


# ============================================================================
# Workout Metrics
# ============================================================================


# Verify that all Workout Metrics are returned successfully.

def test_get_workout_metrics():
    service = Mock()

    service.get_workout_metrics.return_value = [
        create_workout_metric()
    ]

    api.workout_metrics_service = service

    response = client.get(
        "/health/workout-metrics"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    service.get_workout_metrics.assert_called_once()


# Verify that Workout Metrics for a specific date are returned successfully.

def test_get_workout_metrics_by_date():
    workout_metric = create_workout_metric()

    service = Mock()

    service.get_workout_metrics_by_date.return_value = [
        workout_metric
    ]

    api.workout_metrics_service = service

    response = client.get(
        "/health/workout-metrics",
        params={
            "workout_date": "2026-10-08",
        },
    )

    assert response.status_code == 200

    service.get_workout_metrics_by_date.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that Workout Metrics are returned when the requested
# Workout Start Time exists.

def test_get_workout_metric_found():
    service = Mock()

    service.get_workout_metric.return_value = (
        create_workout_metric()
    )

    api.workout_metrics_service = service

    response = client.get(
        "/health/workout-metric",
        params={
            "workout_start_time": "2026-10-08T06:30:00"
        },
    )

    assert response.status_code == 200

    service.get_workout_metric.assert_called_once_with(
        datetime(2026, 10, 8, 6, 30, 0)
    )


# Verify that a 404 response is returned when
# Workout Metrics do not exist.

def test_get_workout_metric_not_found():
    service = Mock()

    service.get_workout_metric.return_value = None

    api.workout_metrics_service = service

    response = client.get(
        "/health/workout-metric",
        params={
            "workout_start_time": "2026-10-08T06:30:00"
        },
    )

    assert response.status_code == 404

    service.get_workout_metric.assert_called_once_with(
        datetime(2026, 10, 8, 6, 30, 0)
    )


# Verify that a new Workout Metrics record can be created.

def test_create_workout_metric():
    service = Mock()

    api.workout_metrics_service = service

    workout_metric = create_workout_metric()

    response = client.post(
        "/health/workout-metrics",
        json=workout_metric.model_dump(
            mode="json"
        ),
    )

    assert response.status_code == 201

    service.create_workout_metric.assert_called_once_with(
        workout_metric
    )


# Verify that a Workout Metrics record can be updated or created.

def test_update_workout_metric():
    service = Mock()

    api.workout_metrics_service = service

    workout_metric = create_workout_metric()

    payload = workout_metric.model_dump(
        mode="json"
    )

    response = client.put(
        "/health/workout-metrics",
        json=payload,
    )

    assert response.status_code == 200

    service.upsert_workout_metric.assert_called_once_with(
        workout_metric.workout_start_time,
        workout_metric,
    )