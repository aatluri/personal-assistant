from datetime import date, datetime
from unittest.mock import Mock

from app.modules.health.nutrition_metrics.nutrition_metrics_google_sheets_repository import (
    NutritionMetricsGoogleSheetsRepository,
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

    repository = NutritionMetricsGoogleSheetsRepository()

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

    assert nutrition_metric.source == "Foodnoms"

    worksheet.get_all_records.assert_called_once()


# Verify that Nutrition Metrics are returned when the requested date exists.
def test_get_nutrition_metric_found():

    repository = NutritionMetricsGoogleSheetsRepository()

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

    repository = NutritionMetricsGoogleSheetsRepository()

    repository.get_nutrition_metrics = Mock(
        return_value=[]
    )

    nutrition_metric = repository.get_nutrition_metric(
        date(2026, 10, 8)
    )

    assert nutrition_metric is None


# Verify that a new Nutrition Metrics record is appended to the worksheet.
def test_create_nutrition_metric():

    repository = NutritionMetricsGoogleSheetsRepository()

    worksheet = Mock()

    repository._get_nutrition_metrics_worksheet = Mock(
        return_value=worksheet
    )

    nutrition_metric = create_nutrition_metric()

    repository.create_nutrition_metric(
        nutrition_metric
    )

    worksheet.append_row.assert_called_once()

    appended_row = worksheet.append_row.call_args.args[0]

    assert appended_row[0] == "October 08, 2026"

    assert appended_row[12] == "Foodnoms"

    assert len(appended_row) == 14

    datetime.strptime(
        appended_row[13],
        "%B %d, %Y %H:%M:%S",
    )

    assert (
        worksheet.append_row.call_args.kwargs["value_input_option"]
        == "USER_ENTERED"
    )


# Verify that an existing Nutrition Metrics record is updated when the date is found.
def test_update_nutrition_metric_found():
    repository = NutritionMetricsGoogleSheetsRepository()

    worksheet = Mock()

    existing_row = create_nutrition_metric_row()

    headers = list(existing_row.keys())
    values = list(existing_row.values())

    worksheet.get_all_values.return_value = [
        headers,
        values,
    ]

    repository._get_nutrition_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated_nutrition_metric = create_nutrition_metric()

    # These fields should be updated.
    updated_nutrition_metric.dietary_energy_kcal = 2000
    updated_nutrition_metric.protein_g = 130
    updated_nutrition_metric.source = "Health Auto Export"

    # These fields should retain their existing values.
    updated_nutrition_metric.carbohydrates_g = None
    updated_nutrition_metric.fiber_g = None

    updated = repository.update_nutrition_metric(
        date(2026, 10, 8),
        updated_nutrition_metric,
    )

    assert updated is True

    worksheet.update.assert_called_once()

    assert (
        worksheet.update.call_args.kwargs["range_name"]
        == "A2:N2"
    )

    updated_row = (
        worksheet.update.call_args.kwargs["values"][0]
    )

    # Supplied values should be updated.
    assert updated_row[1] == 2000
    assert updated_row[2] == 130
    assert updated_row[12] == "Health Auto Export"

    # None values should preserve the existing values.
    assert updated_row[3] == 180
    assert updated_row[4] == 30

    assert len(updated_row) == 14

    datetime.strptime(
        updated_row[13],
        "%B %d, %Y %H:%M:%S",
    )

    assert (
        worksheet.update.call_args.kwargs[
            "value_input_option"
        ]
        == "USER_ENTERED"
    )


# Verify that no update occurs when the Nutrition Metrics date is not found.
def test_update_nutrition_metric_not_found():

    repository = NutritionMetricsGoogleSheetsRepository()

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


# ============================================================================
# Nutrition Metrics Repository Helper Tests
# ============================================================================

# Verify that a NutritionMetrics object is converted into a worksheet row.
def test_nutrition_metric_to_row():

    repository = NutritionMetricsGoogleSheetsRepository()

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

    assert len(row) == 14

    datetime.strptime(
        row[13],
        "%B %d, %Y %H:%M:%S",
    )


# Verify that a worksheet row is converted into a NutritionMetrics object.
def test_row_to_nutrition_metric():

    repository = NutritionMetricsGoogleSheetsRepository()

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

    repository = NutritionMetricsGoogleSheetsRepository()

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