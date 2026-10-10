"""
Nutrition Metrics Repository Helper Tests

Tests the repository's helper methods responsible for:

- Converting worksheet values into Python objects.
- Converting Python objects into worksheet rows.
- Handling empty worksheet values.
"""

from datetime import date

from app.modules.health.nutrition_metrics_repository import (
    NutritionMetricsRepository,
)
from tests.helpers.test_data import (
    create_nutrition_metric,
    create_nutrition_metric_row,
)


# Verify that a NutritionMetrics object is converted into a worksheet row.

def test_nutrition_metric_to_row():

    repository = NutritionMetricsRepository()

    nutrition_metric = create_nutrition_metric()

    row = repository._nutrition_metric_to_row(nutrition_metric)

    assert row[0] == "October 08, 2026"

    assert row[1] == 1800

    assert row[2] == 110
    assert row[3] == 180
    assert row[4] == 30
    assert row[5] == 40

    assert row[6] == 60
    assert row[7] == 18
    assert row[8] == 12
    assert row[9] == 25

    assert row[10] == 100
    assert row[11] == 250

    assert row[12] == "Foodnoms"


# Verify that a worksheet row is converted into a NutritionMetrics object.

def test_row_to_nutrition_metric():

    repository = NutritionMetricsRepository()

    row = create_nutrition_metric_row()

    nutrition_metric = repository._row_to_nutrition_metrics(row)

    assert nutrition_metric.date == date(2026, 10, 8)

    assert nutrition_metric.dietary_energy_kcal == 1800

    assert nutrition_metric.protein_g == 110
    assert nutrition_metric.carbohydrates_g == 180
    assert nutrition_metric.fiber_g == 30
    assert nutrition_metric.sugar_g == 40

    assert nutrition_metric.total_fat_g == 60
    assert nutrition_metric.saturated_fat_g == 18
    assert nutrition_metric.polyunsaturated_fat_g == 12
    assert nutrition_metric.monounsaturated_fat_g == 25

    assert nutrition_metric.water_fl_oz_us == 100
    assert nutrition_metric.cholesterol_mg == 250

    assert nutrition_metric.source == "Foodnoms"


# Verify that empty worksheet values are converted into None.

def test_row_to_nutrition_metric_handles_empty_values():

    repository = NutritionMetricsRepository()

    row = create_nutrition_metric_row(
        **{
            "Dietary Energy (kcal)": "",
            "Protein (g)": "",
            "Carbohydrates (g)": "",
            "Fiber (g)": "",
            "Sugar (g)": "",
            "Total Fat (g)": "",
            "Saturated Fat (g)": "",
            "Polyunsaturated Fat (g)": "",
            "Monounsaturated Fat (g)": "",
            "Water (fl_oz_us)": "",
            "Cholesterol (mg)": "",
            "Source": "",
        }
    )

    nutrition_metric = repository._row_to_nutrition_metrics(row)

    assert nutrition_metric.dietary_energy_kcal is None

    assert nutrition_metric.protein_g is None
    assert nutrition_metric.carbohydrates_g is None
    assert nutrition_metric.fiber_g is None
    assert nutrition_metric.sugar_g is None

    assert nutrition_metric.total_fat_g is None
    assert nutrition_metric.saturated_fat_g is None
    assert nutrition_metric.polyunsaturated_fat_g is None
    assert nutrition_metric.monounsaturated_fat_g is None

    assert nutrition_metric.water_fl_oz_us is None
    assert nutrition_metric.cholesterol_mg is None

    assert nutrition_metric.source is None