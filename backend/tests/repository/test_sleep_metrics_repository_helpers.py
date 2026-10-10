"""
Sleep Metrics Repository Helper Tests

Tests the repository's helper methods responsible for:

- Converting worksheet values into Python objects.
- Converting Python objects into worksheet rows.
- Handling empty worksheet values.
"""

from datetime import date, datetime

from app.modules.health.sleep_metrics_repository import (
    SleepMetricsRepository,
)
from tests.helpers.test_data import (
    create_sleep_metric,
    create_sleep_metric_row,
)


# Verify that a SleepMetrics object is converted into a worksheet row.

def test_sleep_metric_to_row():

    repository = SleepMetricsRepository()

    sleep_metric = create_sleep_metric()

    row = repository._sleep_metric_to_row(sleep_metric)

    assert row[0] == "October 08, 2026"

    assert row[1] == "October 07, 2026 23:00:00"
    assert row[2] == "October 08, 2026 07:00:00"

    assert row[3] == 7.5
    assert row[4] == 4.0
    assert row[5] == 1.5
    assert row[6] == 1.5
    assert row[7] == 0.5

    assert row[8] == "Apple Watch"


# Verify that a worksheet row is converted into a SleepMetrics object.

def test_row_to_sleep_metric():

    repository = SleepMetricsRepository()

    row = create_sleep_metric_row()

    sleep_metric = repository._row_to_sleep_metrics(row)

    assert sleep_metric.date == date(2026, 10, 8)

    assert sleep_metric.sleep_start_time == datetime(
        2026, 10, 7, 23, 0, 0
    )

    assert sleep_metric.sleep_end_time == datetime(
        2026, 10, 8, 7, 0, 0
    )

    assert sleep_metric.total_sleep_duration_hr == 7.5
    assert sleep_metric.core_sleep_hr == 4.0
    assert sleep_metric.rem_sleep_hr == 1.5
    assert sleep_metric.deep_sleep_hr == 1.5
    assert sleep_metric.awake_hr == 0.5

    assert sleep_metric.source == "Apple Watch"


# Verify that empty worksheet values are converted into None.

def test_row_to_sleep_metric_handles_empty_values():

    repository = SleepMetricsRepository()

    row = create_sleep_metric_row(
        **{
            "Sleep Start Time": "",
            "Sleep End Time": "",
            "Core Sleep (hr)": "",
            "Rem Sleep (hr)": "",
            "Deep Sleep (hr)": "",
            "Awake (hr)": "",
            "Source": "",
        }
    )

    sleep_metric = repository._row_to_sleep_metrics(row)

    assert sleep_metric.sleep_start_time is None
    assert sleep_metric.sleep_end_time is None
    assert sleep_metric.core_sleep_hr is None
    assert sleep_metric.rem_sleep_hr is None
    assert sleep_metric.deep_sleep_hr is None
    assert sleep_metric.awake_hr is None
    assert sleep_metric.source is None