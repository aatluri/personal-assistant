"""
Health Metrics Repository Tests

Each test follows the same sequence:

1. Create a Health Metrics instance.
2. Create a mock worksheet (instead of connecting to Google Sheets).
3. Configure the mock worksheet to return predefined data.
4. Replace the repository's worksheet with the mock.
5. Call the repository method being tested.
6. Verify that the repository returns the expected result
   or calls the worksheet with the expected arguments.
"""

from datetime import date
from unittest.mock import Mock

from app.modules.health.health_metrics_repository import (
    HealthMetricsRepository,
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

    repository = HealthMetricsRepository()

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

    worksheet.get_all_records.assert_called_once()


# Verify that Health Metrics are returned when the requested date exists.

def test_get_health_metric_found():

    repository = HealthMetricsRepository()

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

    repository = HealthMetricsRepository()

    repository.get_health_metrics = Mock(
        return_value=[]
    )

    health_metric = repository.get_health_metric(
        date(2026, 10, 8)
    )

    assert health_metric is None


# Verify that a new Health Metrics record is appended to the worksheet.

def test_create_health_metric():

    repository = HealthMetricsRepository()

    worksheet = Mock()

    repository._get_health_metrics_worksheet = Mock(
        return_value=worksheet
    )

    health_metric = create_health_metric()

    repository.create_health_metric(
        health_metric
    )

    worksheet.append_row.assert_called_once_with(
        repository._health_metric_to_row(
            health_metric
        ),
        value_input_option="USER_ENTERED",
    )


# Verify that an existing Health Metrics record is updated when the date is found.

def test_update_health_metric_found():

    repository = HealthMetricsRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["October 08, 2026"],
    ]

    repository._get_health_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_health_metric(
        date(2026, 10, 8),
        create_health_metric(),
    )

    assert updated is True

    worksheet.update.assert_called_once()


# Verify that no update occurs when the Health Metrics date is not found.

def test_update_health_metric_not_found():

    repository = HealthMetricsRepository()

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