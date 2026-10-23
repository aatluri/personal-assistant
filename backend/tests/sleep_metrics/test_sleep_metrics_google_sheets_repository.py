from datetime import date, datetime
from unittest.mock import Mock

from app.modules.health.sleep_metrics.sleep_metrics_google_sheets_repository import (
    SleepMetricsGoogleSheetsRepository,
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

    repository = SleepMetricsGoogleSheetsRepository()

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

    assert sleep_metric.source == "Apple Watch"

    worksheet.get_all_records.assert_called_once()


# Verify that Sleep Metrics are returned when the requested date exists.
def test_get_sleep_metric_found():

    repository = SleepMetricsGoogleSheetsRepository()

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

    repository = SleepMetricsGoogleSheetsRepository()

    repository.get_sleep_metrics = Mock(
        return_value=[]
    )

    sleep_metric = repository.get_sleep_metric(
        date(2026, 10, 8)
    )

    assert sleep_metric is None


# Verify that a new Sleep Metrics record is appended to the worksheet.
def test_create_sleep_metric():

    repository = SleepMetricsGoogleSheetsRepository()

    worksheet = Mock()

    repository._get_sleep_metrics_worksheet = Mock(
        return_value=worksheet
    )

    sleep_metric = create_sleep_metric()

    repository.create_sleep_metric(
        sleep_metric
    )

    worksheet.append_row.assert_called_once()

    appended_row = worksheet.append_row.call_args.args[0]

    assert appended_row[0] == "October 08, 2026"

    assert appended_row[8] == "Apple Watch"

    assert len(appended_row) == 10

    datetime.strptime(
        appended_row[9],
        "%B %d, %Y %H:%M:%S",
    )

    assert (
        worksheet.append_row.call_args.kwargs["value_input_option"]
        == "USER_ENTERED"
    )


# Verify that an existing Sleep Metrics record is updated when the date is found.
def test_update_sleep_metric_found():
    repository = SleepMetricsGoogleSheetsRepository()

    worksheet = Mock()

    existing_row = create_sleep_metric_row()

    headers = list(existing_row.keys())
    values = list(existing_row.values())

    worksheet.get_all_values.return_value = [
        headers,
        values,
    ]

    repository._get_sleep_metrics_worksheet = Mock(
        return_value=worksheet
    )

    updated_sleep_metric = create_sleep_metric()

    # These fields should be updated.
    updated_sleep_metric.total_sleep_duration_hr = 8.0
    updated_sleep_metric.deep_sleep_hr = 2.0
    updated_sleep_metric.source = "Health Auto Export"

    # These fields should retain their existing values.
    updated_sleep_metric.sleep_start_time = None
    updated_sleep_metric.rem_sleep_hr = None

    updated = repository.update_sleep_metric(
        date(2026, 10, 8),
        updated_sleep_metric,
    )

    assert updated is True

    worksheet.update.assert_called_once()

    assert (
        worksheet.update.call_args.kwargs["range_name"]
        == "A2:J2"
    )

    updated_row = (
        worksheet.update.call_args.kwargs["values"][0]
    )

    # Supplied values should be updated.
    assert updated_row[3] == 8.0
    assert updated_row[6] == 2.0
    assert updated_row[8] == "Health Auto Export"

    # None values should preserve the existing values.
    assert updated_row[1] == "October 07, 2026 23:00:00"
    assert updated_row[5] == 1.5

    assert len(updated_row) == 10

    datetime.strptime(
        updated_row[9],
        "%B %d, %Y %H:%M:%S",
    )

    assert (
        worksheet.update.call_args.kwargs[
            "value_input_option"
        ]
        == "USER_ENTERED"
    )

# Verify that no update occurs when the Sleep Metrics date is not found.
def test_update_sleep_metric_not_found():

    repository = SleepMetricsGoogleSheetsRepository()

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


# ============================================================================
# Sleep Metrics Repository Helper Tests
# ============================================================================

# Verify that a SleepMetrics object is converted into a worksheet row.
def test_sleep_metric_to_row():

    repository = SleepMetricsGoogleSheetsRepository()

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

    assert len(row) == 10

    datetime.strptime(
        row[9],
        "%B %d, %Y %H:%M:%S",
    )


# Verify that a worksheet row is converted into a SleepMetrics object.
def test_row_to_sleep_metric():

    repository = SleepMetricsGoogleSheetsRepository()

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

    repository = SleepMetricsGoogleSheetsRepository()

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