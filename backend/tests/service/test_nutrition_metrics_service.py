from datetime import date
from unittest.mock import Mock

from app.modules.health.nutrition_metrics_service import (
    NutritionMetricsService,
)
from tests.helpers.test_data import create_nutrition_metric


# ============================================================================
# Nutrition Metrics
# ============================================================================

# Verify that all Nutrition Metrics are retrieved from the repository.

def test_get_nutrition_metrics():

    service = NutritionMetricsService()

    repository = Mock()

    repository.get_nutrition_metrics.return_value = [
        create_nutrition_metric()
    ]

    service._repository = repository

    nutrition_metrics = service.get_nutrition_metrics()

    assert len(nutrition_metrics) == 1
    assert nutrition_metrics[0].date == date(2026, 10, 8)

    repository.get_nutrition_metrics.assert_called_once()


# Verify that Nutrition Metrics are returned when the requested date exists.

def test_get_nutrition_metric():

    service = NutritionMetricsService()

    repository = Mock()

    repository.get_nutrition_metric.return_value = (
        create_nutrition_metric()
    )

    service._repository = repository

    nutrition_metric = service.get_nutrition_metric(
        date(2026, 10, 8)
    )

    assert nutrition_metric is not None
    assert nutrition_metric.date == date(2026, 10, 8)

    repository.get_nutrition_metric.assert_called_once_with(
        date(2026, 10, 8)
    )


# Verify that a new Nutrition Metrics record is created through the repository.

def test_create_nutrition_metric():

    service = NutritionMetricsService()

    repository = Mock()

    service._repository = repository

    nutrition_metric = create_nutrition_metric()

    service.create_nutrition_metric(
        nutrition_metric
    )

    repository.create_nutrition_metric.assert_called_once_with(
        nutrition_metric
    )


# Verify that an existing Nutrition Metrics record is updated.

def test_upsert_nutrition_metric_update():

    service = NutritionMetricsService()

    repository = Mock()

    repository.update_nutrition_metric.return_value = True

    service._repository = repository

    nutrition_metric = create_nutrition_metric()

    service.upsert_nutrition_metric(
        date(2026, 10, 8),
        nutrition_metric,
    )

    repository.update_nutrition_metric.assert_called_once_with(
        date(2026, 10, 8),
        nutrition_metric,
    )

    repository.create_nutrition_metric.assert_not_called()


# Verify that a new Nutrition Metrics record is created when no existing record is found.

def test_upsert_nutrition_metric_create():

    service = NutritionMetricsService()

    repository = Mock()

    repository.update_nutrition_metric.return_value = False

    service._repository = repository

    nutrition_metric = create_nutrition_metric()

    service.upsert_nutrition_metric(
        date(2026, 10, 8),
        nutrition_metric,
    )

    repository.update_nutrition_metric.assert_called_once()

    repository.create_nutrition_metric.assert_called_once_with(
        nutrition_metric
    )