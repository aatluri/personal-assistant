"""
Health Metrics Repository Helper Tests

Tests the repository's helper methods responsible for:

- Converting worksheet values into Python objects.
- Converting Python objects into worksheet rows.
- Handling empty worksheet values.
"""

from datetime import date

from app.modules.health.health_metrics_repository import (
    HealthMetricsRepository,
)
from tests.helpers.test_data import (
    create_health_metric,
    create_health_metric_row,
)


# Verify that a HealthMetrics object is converted into a worksheet row.

def test_health_metric_to_row():

    repository = HealthMetricsRepository()

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


# Verify that a worksheet row is converted into a HealthMetrics object.

def test_row_to_health_metric():

    repository = HealthMetricsRepository()

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

    repository = HealthMetricsRepository()

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