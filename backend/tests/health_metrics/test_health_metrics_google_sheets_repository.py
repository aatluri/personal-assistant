from datetime import date, datetime
from unittest.mock import Mock

from app.modules.health.health_metrics.health_metrics_google_sheets_repository import (
    HealthMetricsGoogleSheetsRepository,
)
from tests.helpers.test_data import (
    create_health_metric,
    create_health_metric_row,
)


# ============================================================================
# Health Metrics
# ============================================================================

# Verify that all Health Metrics are retrieved and converted correctly.
def test_get_health_metrics():

    repository = HealthMetricsGoogleSheetsRepository()

    worksheet = Mock()

    worksheet.get_all_records.return_value = [
        create_health_metric_row()
    ]

    repository._get_health_metrics_worksheet = Mock(
        return_value=worksheet
    )

    health_metrics = repository.get_health_metrics()

    assert len(health_metrics) == 1

    health_metric = health_metrics[0]

    assert health_metric.date == date(2026, 10, 8)

    assert health_metric.step_count == 10000
    assert health_metric.active_energy_kcal == 650
    assert health_metric.resting_energy_kcal == 1800

    assert health_metric.source == "Apple Watch"

    worksheet.get_all_records.assert_called_once()


# Verify that Health Metrics are returned when the requested date exists.
def test_get_health_metric_found():

    repository = HealthMetricsGoogleSheetsRepository()

    repository.get_health_metrics = Mock(
        return_value=[
            create_health_metric(),
        ]
    )

    health_metric = repository.get_health_metric(
        date(2026, 10, 8)
    )

    assert health_metric is not None
    assert health_metric.date == date(2026, 10, 8)


# Verify that None is returned when the requested Health Metrics do not exist.
def test_get_health_metric_not_found():

    repository = HealthMetricsGoogleSheetsRepository()

    repository.get_health_metrics = Mock(
        return_value=[]
    )

    health_metric = repository.get_health_metric(
        date(2026, 10, 8)
    )

    assert health_metric is None


# Verify that a new Health Metrics record is appended to the worksheet.
def test_create_health_metric():

    repository = HealthMetricsGoogleSheetsRepository()

    worksheet = Mock()

    repository._get_health_metrics_worksheet = Mock(
        return_value=worksheet
    )

    health_metric = create_health_metric()

    repository.create_health_metric(
        health_metric
    )

    worksheet.append_row.assert_called_once()

    appended_row = worksheet.append_row.call_args.args[0]

    assert appended_row[0] == "October 08, 2026"

    assert appended_row[15] == "Apple Watch"

    assert len(appended_row) == 17

    datetime.strptime(
        appended_row[16],
        "%B %d, %Y %H:%M:%S",
    )

    assert (
        worksheet.append_row.call_args.kwargs["value_input_option"]
        == "USER_ENTERED"
    )


# Verify that an existing Health Metrics record is updated when the date is found.
def test_update_health_metric_found():
    repository = HealthMetricsGoogleSheetsRepository()

    worksheet = Mock()

    existing_row = create_health_metric_row()

    headers = list(existing_row.keys())
    values = list(existing_row.values())

    worksheet.get_all_values.return_value = [
        headers,
        values,
    ]

    repository._get_health_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated_health_metric = create_health_metric()

    # These fields should be updated.
    updated_health_metric.step_count = 12000
    updated_health_metric.resting_heart_rate_bpm = 50
    updated_health_metric.source = "Health Auto Export"

    # These fields should retain their existing values.
    updated_health_metric.active_energy_kcal = None
    updated_health_metric.heart_rate_variability_ms = None

    updated = repository.update_health_metric(
        date(2026, 10, 8),
        updated_health_metric,
    )

    assert updated is True

    worksheet.update.assert_called_once()

    assert (
        worksheet.update.call_args.kwargs["range_name"]
        == "A2:Q2"
    )

    updated_row = (
        worksheet.update.call_args.kwargs["values"][0]
    )

    # Supplied values should be updated.
    assert updated_row[1] == 12000
    assert updated_row[14] == 50
    assert updated_row[15] == "Health Auto Export"

    # None values should preserve the existing values.
    assert updated_row[2] == 650
    assert updated_row[11] == 55

    assert len(updated_row) == 17

    datetime.strptime(
        updated_row[16],
        "%B %d, %Y %H:%M:%S",
    )

    assert (
        worksheet.update.call_args.kwargs[
            "value_input_option"
        ]
        == "USER_ENTERED"
    )

# Verify that no update occurs when the Health Metrics date is not found.
def test_update_health_metric_not_found():

    repository = HealthMetricsGoogleSheetsRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["October 07, 2026"],
    ]

    repository._get_health_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_health_metric(
        date(2026, 10, 8),
        create_health_metric(),
    )

    assert updated is False

    worksheet.update.assert_not_called()


# ============================================================================
# Health Metrics Helpers Tests
# ============================================================================

# Verify that a HealthMetrics object is converted into a worksheet row.
def test_health_metric_to_row():

    repository = HealthMetricsGoogleSheetsRepository()

    health_metric = create_health_metric()

    row = repository._health_metric_to_row(health_metric)

    assert row[0] == "October 08, 2026"

    assert row[1] == 10000

    assert row[2] == 650
    assert row[3] == 1800

    assert row[4] == 0
    assert row[5] == 98
    assert row[6] == 2
    assert row[7] == 30

    assert row[8] == 8

    assert row[9] == 45
    assert row[10] == 175
    assert row[11] == 55

    assert row[12] == 4.5

    assert row[13] == 16
    assert row[14] == 52

    assert row[15] == "Apple Watch"

    assert len(row) == 17

    datetime.strptime(
        row[16],
        "%B %d, %Y %H:%M:%S",
    )


# Verify that a worksheet row is converted into a HealthMetrics object.
def test_row_to_health_metric():

    repository = HealthMetricsGoogleSheetsRepository()

    row = create_health_metric_row()

    health_metric = repository._row_to_health_metrics(row)

    assert health_metric.date == date(2026, 10, 8)

    assert health_metric.step_count == 10000

    assert health_metric.active_energy_kcal == 650
    assert health_metric.resting_energy_kcal == 1800

    assert health_metric.atrial_fibrillation_burden_percent == 0
    assert health_metric.blood_oxygen_saturation_percent == 98
    assert health_metric.breathing_disturbances_count == 2
    assert health_metric.cardio_recovery_bpm == 30

    assert health_metric.flights_climbed == 8

    assert health_metric.heart_rate_min_bpm == 45
    assert health_metric.heart_rate_max_bpm == 175
    assert health_metric.heart_rate_variability_ms == 55

    assert health_metric.physical_effort_kcal_hr_kg == 4.5

    assert health_metric.respiratory_rate_bpm == 16
    assert health_metric.resting_heart_rate_bpm == 52

    assert health_metric.source == "Apple Watch"


# Verify that empty worksheet values are converted into None.
def test_row_to_health_metric_handles_empty_values():

    repository = HealthMetricsGoogleSheetsRepository()

    row = create_health_metric_row(
        **{
            "Step Count (count)": "",
            "Active Energy (kcal)": "",
            "Resting Energy (kcal)": "",
            "Atrial Fibrillation Burden (%)": "",
            "Blood Oxygen Saturation (%)": "",
            "Breathing Disturbances (count)": "",
            "Cardio Recovery (count/min)": "",
            "Flights Climbed (count)": "",
            "Heart Rate [Min] (count/min)": "",
            "Heart Rate [Max] (count/min)": "",
            "Heart Rate Variability (ms)": "",
            "Physical Effort (kcal/hr¬∑kg)": "",
            "Respiratory Rate (count/min)": "",
            "Resting Heart Rate (count/min)": "",
            "Source": "",
        }
    )

    health_metric = repository._row_to_health_metrics(row)

    assert health_metric.step_count is None
    assert health_metric.active_energy_kcal is None
    assert health_metric.resting_energy_kcal is None

    assert health_metric.atrial_fibrillation_burden_percent is None
    assert health_metric.blood_oxygen_saturation_percent is None
    assert health_metric.breathing_disturbances_count is None
    assert health_metric.cardio_recovery_bpm is None

    assert health_metric.flights_climbed is None

    assert health_metric.heart_rate_min_bpm is None
    assert health_metric.heart_rate_max_bpm is None
    assert health_metric.heart_rate_variability_ms is None

    assert health_metric.physical_effort_kcal_hr_kg is None

    assert health_metric.respiratory_rate_bpm is None
    assert health_metric.resting_heart_rate_bpm is None

    assert health_metric.source is None