"""
Nutrition Metrics Repository Tests

Each test follows the same sequence:

1. Create a Nutrition Metrics instance.
2. Create a mock worksheet (instead of connecting to Google Sheets).
3. Configure the mock worksheet to return predefined data.
4. Replace the repository's worksheet with the mock.
5. Call the repository method being tested.
6. Verify that the repository returns the expected result
   or calls the worksheet with the expected arguments.
"""

from datetime import date
from unittest.mock import Mock

from app.modules.health.nutrition_metrics_repository import (
    NutritionMetricsRepository,
)
from tests.helpers.test_data import (
    create_nutrition_metric,
    create_nutrition_metric_row,
)


# ============================================================================
# Nutrition Metrics
# ============================================================================

# Verify that all Nutrition Metrics are retrieved and converted correctly.

def test_get_nutrition_metrics():

    repository = NutritionMetricsRepository()

    worksheet = Mock()

    worksheet.get_all_records.return_value = [
        create_nutrition_metric_row()
    ]

    repository._get_nutrition_metrics_worksheet = Mock(
        return_value=worksheet
    )

    nutrition_metrics = repository.get_nutrition_metrics()

    assert len(nutrition_metrics) == 1

    nutrition_metric = nutrition_metrics[0]

    assert nutrition_metric.date == date(2026, 10, 8)

    assert nutrition_metric.dietary_energy_kcal == 1800
    assert nutrition_metric.protein_g == 110
    assert nutrition_metric.carbohydrates_g == 180

    worksheet.get_all_records.assert_called_once()


# Verify that Nutrition Metrics are returned when the requested date exists.

def test_get_nutrition_metric_found():

    repository = NutritionMetricsRepository()

    repository.get_nutrition_metrics = Mock(
        return_value=[
            create_nutrition_metric(),
        ]
    )

    nutrition_metric = repository.get_nutrition_metric(
        date(2026, 10, 8)
    )

    assert nutrition_metric is not None
    assert nutrition_metric.date == date(2026, 10, 8)


# Verify that None is returned when the requested Nutrition Metrics do not exist.

def test_get_nutrition_metric_not_found():

    repository = NutritionMetricsRepository()

    repository.get_nutrition_metrics = Mock(
        return_value=[]
    )

    nutrition_metric = repository.get_nutrition_metric(
        date(2026, 10, 8)
    )

    assert nutrition_metric is None


# Verify that a new Nutrition Metrics record is appended to the worksheet.

def test_create_nutrition_metric():

    repository = NutritionMetricsRepository()

    worksheet = Mock()

    repository._get_nutrition_metrics_worksheet = Mock(
        return_value=worksheet
    )

    nutrition_metric = create_nutrition_metric()

    repository.create_nutrition_metric(
        nutrition_metric
    )

    worksheet.append_row.assert_called_once_with(
        repository._nutrition_metric_to_row(
            nutrition_metric
        ),
        value_input_option="USER_ENTERED",
    )


# Verify that an existing Nutrition Metrics record is updated when the date is found.

def test_update_nutrition_metric_found():

    repository = NutritionMetricsRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["October 08, 2026"],
    ]

    repository._get_nutrition_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_nutrition_metric(
        date(2026, 10, 8),
        create_nutrition_metric(),
    )

    assert updated is True

    worksheet.update.assert_called_once()


# Verify that no update occurs when the Nutrition Metrics date is not found.

def test_update_nutrition_metric_not_found():

    repository = NutritionMetricsRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["October 07, 2026"],
    ]

    repository._get_nutrition_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_nutrition_metric(
        date(2026, 10, 8),
        create_nutrition_metric(),
    )

    assert updated is False

    worksheet.update.assert_not_called()