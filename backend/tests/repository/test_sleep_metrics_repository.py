"""
Sleep Metrics Repository Tests

Each test follows the same sequence:

1. Create a Sleep Metrics instance.
2. Create a mock worksheet (instead of connecting to Google Sheets).
3. Configure the mock worksheet to return predefined data.
4. Replace the repository's worksheet with the mock.
5. Call the repository method being tested.
6. Verify that the repository returns the expected result
   or calls the worksheet with the expected arguments.
"""

from datetime import date
from unittest.mock import Mock

from app.modules.health.sleep_metrics_repository import (
    SleepMetricsRepository,
)
from tests.helpers.test_data import (
    create_sleep_metric,
    create_sleep_metric_row,
)


# ============================================================================
# Sleep Metrics
# ============================================================================

# Verify that all Sleep Metrics are retrieved and converted correctly.

def test_get_sleep_metrics():

    repository = SleepMetricsRepository()

    worksheet = Mock()

    worksheet.get_all_records.return_value = [
        create_sleep_metric_row()
    ]

    repository._get_sleep_metrics_worksheet = Mock(
        return_value=worksheet
    )

    sleep_metrics = repository.get_sleep_metrics()

    assert len(sleep_metrics) == 1

    sleep_metric = sleep_metrics[0]

    assert sleep_metric.date == date(2026, 10, 8)

    assert sleep_metric.total_sleep_duration_hr == 7.5
    assert sleep_metric.core_sleep_hr == 4.0
    assert sleep_metric.deep_sleep_hr == 1.5

    worksheet.get_all_records.assert_called_once()


# Verify that Sleep Metrics are returned when the requested date exists.

def test_get_sleep_metric_found():

    repository = SleepMetricsRepository()

    repository.get_sleep_metrics = Mock(
        return_value=[
            create_sleep_metric(),
        ]
    )

    sleep_metric = repository.get_sleep_metric(
        date(2026, 10, 8)
    )

    assert sleep_metric is not None
    assert sleep_metric.date == date(2026, 10, 8)


# Verify that None is returned when the requested Sleep Metrics do not exist.

def test_get_sleep_metric_not_found():

    repository = SleepMetricsRepository()

    repository.get_sleep_metrics = Mock(
        return_value=[]
    )

    sleep_metric = repository.get_sleep_metric(
        date(2026, 10, 8)
    )

    assert sleep_metric is None


# Verify that a new Sleep Metrics record is appended to the worksheet.

def test_create_sleep_metric():

    repository = SleepMetricsRepository()

    worksheet = Mock()

    repository._get_sleep_metrics_worksheet = Mock(
        return_value=worksheet
    )

    sleep_metric = create_sleep_metric()

    repository.create_sleep_metric(
        sleep_metric
    )

    worksheet.append_row.assert_called_once_with(
        repository._sleep_metric_to_row(
            sleep_metric
        ),
        value_input_option="USER_ENTERED",
    )


# Verify that an existing Sleep Metrics record is updated when the date is found.

def test_update_sleep_metric_found():

    repository = SleepMetricsRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["October 08, 2026"],
    ]

    repository._get_sleep_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_sleep_metric(
        date(2026, 10, 8),
        create_sleep_metric(),
    )

    assert updated is True

    worksheet.update.assert_called_once()


# Verify that no update occurs when the Sleep Metrics date is not found.

def test_update_sleep_metric_not_found():

    repository = SleepMetricsRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["October 07, 2026"],
    ]

    repository._get_sleep_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_sleep_metric(
        date(2026, 10, 8),
        create_sleep_metric(),
    )

    assert updated is False

    worksheet.update.assert_not_called()