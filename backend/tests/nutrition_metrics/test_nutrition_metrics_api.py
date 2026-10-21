from datetime import date
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.modules.health import api
from tests.helpers.test_data import (
    create_nutrition_metric,
)


client = TestClient(app)


"""
Nutrition Metrics API Tests

These tests verify the HTTP API layer for Nutrition Metrics.

The real NutritionMetricsService is replaced with a mock so that
the API can be tested independently of the service and
repository layers.
"""


# ============================================================================
# Nutrition Metrics
# ============================================================================


# Verify that all Nutrition Metrics records are returned successfully.

def test_get_nutrition_metrics():
    service = Mock()

    service.get_nutrition_metrics.return_value = [
        create_nutrition_metric()
    ]

    api.nutrition_metrics_service = service

    response = client.get(
        "/health/nutrition-metrics"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    service.get_nutrition_metrics.assert_called_once()


# Verify that Nutrition Metrics are returned when the requested date exists.

def test_get_nutrition_metric_found():
    service = Mock()

    service.get_nutrition_metric.return_value = (
        create_nutrition_metric()
    )

    api.nutrition_metrics_service = service

    response = client.get(
        "/health/nutrition-metrics/2026-10-08"
    )

    assert response.status_code == 200

    service.get_nutrition_metric.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that a 404 response is returned when Nutrition Metrics do not exist.

def test_get_nutrition_metric_not_found():
    service = Mock()

    service.get_nutrition_metric.return_value = None

    api.nutrition_metrics_service = service

    response = client.get(
        "/health/nutrition-metrics/2026-10-08"
    )

    assert response.status_code == 404

    service.get_nutrition_metric.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that a new Nutrition Metrics record can be created.

def test_create_nutrition_metric():
    service = Mock()

    api.nutrition_metrics_service = service

    nutrition_metric = create_nutrition_metric()

    response = client.post(
        "/health/nutrition-metrics",
        json=nutrition_metric.model_dump(
            mode="json"
        ),
    )

    assert response.status_code == 201

    service.create_nutrition_metric.assert_called_once_with(
        nutrition_metric
    )


# Verify that a Nutrition Metrics record can be updated or created.

def test_update_nutrition_metric():
    service = Mock()

    api.nutrition_metrics_service = service

    nutrition_metric = create_nutrition_metric()

    payload = nutrition_metric.model_dump(
        mode="json"
    )

    response = client.put(
        "/health/nutrition-metrics",
        json=payload,
    )

    assert response.status_code == 200

    service.upsert_nutrition_metric.assert_called_once_with(
        nutrition_metric.date,
        nutrition_metric,
    )