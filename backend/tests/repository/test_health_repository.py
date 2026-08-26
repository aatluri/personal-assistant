"""
Health Repository Tests

Each test follows the same sequence:

1. Create a HealthRepository instance.
2. Create a mock worksheet (instead of connecting to Google Sheets).
3. Configure the mock worksheet to return predefined data.
4. Replace the repository's worksheet with the mock.
5. Call the repository method being tested.
6. Verify that the repository returns the expected result
   or calls the worksheet with the expected arguments.
"""


from datetime import date
from unittest.mock import Mock

from app.modules.health.repository import HealthRepository
from tests.helpers.test_data import (
    create_body_measurement,
    create_body_measurement_row,
    create_daily_log,
    create_daily_log_row,
)

# Verify that all Daily Log records are retrieved and converted correctly.
def test_get_daily_logs():
    """
    Verify that get_daily_logs():

    - Reads all rows from the Daily_Log worksheet.
    - Converts each worksheet row into a DailyLog object.
    - Returns the expected list of DailyLog objects.
    """

    # -------------------------------------------------------------
    # Create the repository being tested.
    # -------------------------------------------------------------
    repository = HealthRepository()

    # -------------------------------------------------------------
    # Create a fake Google Sheets worksheet.
    #
    # This mock replaces the real worksheet so the test can run
    # without connecting to Google Sheets.
    # -------------------------------------------------------------
    worksheet = Mock()

    # -------------------------------------------------------------
    # Configure the fake worksheet.
    #
    # Whenever the repository calls:
    #
    #     worksheet.get_all_records()
    #
    # return one predefined Daily Log row.
    # -------------------------------------------------------------
    worksheet.get_all_records.return_value = [
        create_daily_log_row()
    ]

    # -------------------------------------------------------------
    # Replace the repository's worksheet with our fake worksheet.
    #
    # From this point onwards, every call to
    # _get_daily_log_worksheet() returns the mock instead of
    # connecting to Google Sheets.
    # -------------------------------------------------------------
    repository._get_daily_log_worksheet = Mock(
        return_value=worksheet
    )

    # -------------------------------------------------------------
    # Execute the method being tested.
    # -------------------------------------------------------------
    daily_logs = repository.get_daily_logs()

    # -------------------------------------------------------------
    # Verify that one DailyLog object was returned.
    # -------------------------------------------------------------
    assert len(daily_logs) == 1

    # Retrieve the first (and only) DailyLog.
    daily_log = daily_logs[0]

    # -------------------------------------------------------------
    # Verify that the worksheet values were correctly converted
    # into the DailyLog object.
    # -------------------------------------------------------------
    assert daily_log.date == date(2026, 8, 26)
    assert daily_log.weight_kg == 80
    assert daily_log.workout_type == "HIIT"

    # -------------------------------------------------------------
    # Verify that the repository actually attempted to read
    # all rows from the worksheet.
    # -------------------------------------------------------------
    worksheet.get_all_records.assert_called_once()

# Verify that a Daily Log is returned when the requested date exists.
def test_get_daily_log_found():

    repository = HealthRepository()

    repository.get_daily_logs = Mock(
        return_value=[
            create_daily_log(),
        ]
    )

    daily_log = repository.get_daily_log(
        date(2026, 8, 26)
    )

    assert daily_log is not None
    assert daily_log.date == date(2026, 8, 26)

# Verify that None is returned when the requested Daily Log does not exist.
def test_get_daily_log_not_found():

    repository = HealthRepository()

    repository.get_daily_logs = Mock(return_value=[])

    daily_log = repository.get_daily_log(
        date(2026, 8, 26)
    )

    assert daily_log is None


# Verify that the Daily Log with the most recent date is returned.
def test_get_latest_daily_log():

    repository = HealthRepository()

    repository.get_daily_logs = Mock(
        return_value=[
            create_daily_log(date=date(2026, 8, 24)),
            create_daily_log(date=date(2026, 8, 26)),
            create_daily_log(date=date(2026, 8, 25)),
        ]
    )

    latest = repository.get_latest_daily_log()

    assert latest is not None
    assert latest.date == date(2026, 8, 26)

# Verify that None is returned when no Daily Logs exist.
def test_get_latest_daily_log_empty():

    repository = HealthRepository()

    repository.get_daily_logs = Mock(
        return_value=[]
    )

    assert repository.get_latest_daily_log() is None

# Verify that a new Daily Log is appended to the worksheet.
def test_create_daily_log():

    repository = HealthRepository()

    worksheet = Mock()

    repository._get_daily_log_worksheet = Mock(
        return_value=worksheet
    )

    daily_log = create_daily_log()

    repository.create_daily_log(
        daily_log
    )

    worksheet.append_row.assert_called_once_with(
        repository._daily_log_to_row(daily_log),
        value_input_option="USER_ENTERED",
    )


# Verify that an existing Daily Log is updated when the date is found.
def test_update_daily_log_found():

    repository = HealthRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["August 26, 2026"],
    ]

    repository._get_daily_log_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_daily_log(
        date(2026, 8, 26),
        create_daily_log(),
    )

    assert updated is True

    worksheet.update.assert_called_once()

# Verify that no update occurs when the Daily Log date is not found.
def test_update_daily_log_not_found():

    repository = HealthRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["August 25, 2026"],
    ]

    repository._get_daily_log_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_daily_log(
        date(2026, 8, 26),
        create_daily_log(),
    )

    assert updated is False

    worksheet.update.assert_not_called()


# ============================================================================
# Body Measurements
# ============================================================================

# Verify that all Body Measurements are retrieved and converted correctly.
def test_get_body_measurements():

    repository = HealthRepository()

    worksheet = Mock()

    worksheet.get_all_records.return_value = [
        create_body_measurement_row()
    ]

    repository._get_body_measurements_worksheet = Mock(
        return_value=worksheet
    )

    measurements = repository.get_body_measurements()

    assert len(measurements) == 1

    measurement = measurements[0]

    assert measurement.date == date(2026, 8, 26)
    assert measurement.body_fat_percent == 18

    worksheet.get_all_records.assert_called_once()


# Verify that Body Measurements are returned when the requested date exists.
def test_get_body_measurement_found():

    repository = HealthRepository()

    repository.get_body_measurements = Mock(
        return_value=[
            create_body_measurement(),
        ]
    )

    measurement = repository.get_body_measurement(
        date(2026, 8, 26)
    )

    assert measurement is not None
    assert measurement.date == date(2026, 8, 26)


# Verify that None is returned when the requested Body Measurements do not exist.
def test_get_body_measurement_not_found():

    repository = HealthRepository()

    repository.get_body_measurements = Mock(
        return_value=[]
    )

    measurement = repository.get_body_measurement(
        date(2026, 8, 26)
    )

    assert measurement is None


# Verify that a new Body Measurements record is appended to the worksheet.
def test_create_body_measurement():

    repository = HealthRepository()

    worksheet = Mock()

    repository._get_body_measurements_worksheet = Mock(
        return_value=worksheet
    )

    measurement = create_body_measurement()

    repository.create_body_measurement(
        measurement
    )

    worksheet.append_row.assert_called_once_with(
        repository._body_measurement_to_row(
            measurement
        ),
        value_input_option="USER_ENTERED",
    )

# Verify that an existing Body Measurements record is updated when the date is found.
def test_update_body_measurement_found():

    repository = HealthRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["August 26, 2026"],
    ]

    repository._get_body_measurements_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_body_measurement(
        date(2026, 8, 26),
        create_body_measurement(),
    )

    assert updated is True

    worksheet.update.assert_called_once()

# Verify that no update occurs when the Body Measurements date is not found.
def test_update_body_measurement_not_found():

    repository = HealthRepository()

    worksheet = Mock()

    worksheet.get_all_values.return_value = [
        ["Date"],
        ["August 25, 2026"],
    ]

    repository._get_body_measurements_worksheet = Mock(
        return_value=worksheet
    )

    updated = repository.update_body_measurement(
        date(2026, 8, 26),
        create_body_measurement(),
    )

    assert updated is False

    worksheet.update.assert_not_called()