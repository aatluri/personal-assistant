from datetime import date
from unittest.mock import Mock

from app.modules.health.service import HealthService
from tests.helpers.test_data import (
    create_daily_log,
    create_body_measurement,
)


"""
Health Service Tests

Each test follows the same sequence:

1. Create a HealthService instance.
2. Replace the repository with a mock repository.
3. Configure the mock repository to return predefined data.
4. Call the service method being tested.
5. Verify that the service returns the expected result
   or calls the repository with the expected arguments.
"""


# ============================================================================
# Daily Log
# ============================================================================

# Verify that all Daily Logs are retrieved from the repository.
def test_get_daily_logs():

    # -------------------------------------------------------------
    # Create the HealthService being tested.
    # -------------------------------------------------------------
    service = HealthService()

    # -------------------------------------------------------------
    # Create a mock repository.
    #
    # This replaces the real repository so the test can run
    # without connecting to Google Sheets.
    # -------------------------------------------------------------
    repository = Mock()

    # -------------------------------------------------------------
    # Configure the mock repository.
    #
    # Whenever the service calls:
    #
    #     repository.get_daily_logs()
    #
    # return one predefined DailyLog object.
    # -------------------------------------------------------------
    repository.get_daily_logs.return_value = [
        create_daily_log(),
    ]

    # -------------------------------------------------------------
    # Replace the service's repository with our mock.
    #
    # From this point onwards, every repository call made by the
    # service will use the mock instead of the real repository.
    # -------------------------------------------------------------
    service._repository = repository

    # -------------------------------------------------------------
    # Execute the method being tested.
    # -------------------------------------------------------------
    daily_logs = service.get_daily_logs()

    # -------------------------------------------------------------
    # Verify that the service returned the expected Daily Logs.
    # -------------------------------------------------------------
    assert len(daily_logs) == 1
    assert daily_logs[0].date == date(2026, 8, 26)

    # -------------------------------------------------------------
    # Verify that the service called the expected repository method
    # exactly once.
    # -------------------------------------------------------------
    repository.get_daily_logs.assert_called_once()


# Verify that a Daily Log is returned when the requested date exists.
def test_get_daily_log():

    service = HealthService()

    repository = Mock()

    repository.get_daily_log.return_value = create_daily_log()

    service._repository = repository

    daily_log = service.get_daily_log(
        date(2026, 8, 26)
    )

    assert daily_log is not None
    assert daily_log.date == date(2026, 8, 26)

    repository.get_daily_log.assert_called_once_with(
        date(2026, 8, 26)
    )


# Verify that the latest Daily Log is returned.
def test_get_latest_daily_log():

    service = HealthService()

    repository = Mock()

    repository.get_latest_daily_log.return_value = (
        create_daily_log()
    )

    service._repository = repository

    latest = service.get_latest_daily_log()

    assert latest is not None
    assert latest.date == date(2026, 8, 26)

    repository.get_latest_daily_log.assert_called_once()


# Verify that a new Daily Log is created through the repository.
def test_create_daily_log():

    service = HealthService()

    repository = Mock()

    service._repository = repository

    daily_log = create_daily_log()

    service.create_daily_log(
        daily_log
    )

    repository.create_daily_log.assert_called_once_with(
        daily_log
    )


# Verify that an existing Daily Log is updated.
def test_upsert_daily_log_update():

    service = HealthService()

    repository = Mock()

    repository.update_daily_log.return_value = True

    service._repository = repository

    daily_log = create_daily_log()

    service.upsert_daily_log(
        date(2026, 8, 26),
        daily_log,
    )

    repository.update_daily_log.assert_called_once_with(
        date(2026, 8, 26),
        daily_log,
    )

    repository.create_daily_log.assert_not_called()


# Verify that a new Daily Log is created when no existing record is found.
def test_upsert_daily_log_create():

    service = HealthService()

    repository = Mock()

    repository.update_daily_log.return_value = False

    service._repository = repository

    daily_log = create_daily_log()

    service.upsert_daily_log(
        date(2026, 8, 26),
        daily_log,
    )

    repository.update_daily_log.assert_called_once()

    repository.create_daily_log.assert_called_once_with(
        daily_log
    )


# ============================================================================
# Body Measurements
# ============================================================================

# Verify that all Body Measurements are retrieved from the repository.
def test_get_body_measurements():

    service = HealthService()

    repository = Mock()

    repository.get_body_measurements.return_value = [
        create_body_measurement()
    ]

    service._repository = repository

    measurements = service.get_body_measurements()

    assert len(measurements) == 1
    assert measurements[0].date == date(2026, 8, 26)

    repository.get_body_measurements.assert_called_once()


# Verify that Body Measurements are returned when the requested date exists.
def test_get_body_measurement():

    service = HealthService()

    repository = Mock()

    repository.get_body_measurement.return_value = (
        create_body_measurement()
    )

    service._repository = repository

    measurement = service.get_body_measurement(
        date(2026, 8, 26)
    )

    assert measurement is not None
    assert measurement.date == date(2026, 8, 26)

    repository.get_body_measurement.assert_called_once_with(
        date(2026, 8, 26)
    )


# Verify that a new Body Measurements record is created through the repository.
def test_create_body_measurement():

    service = HealthService()

    repository = Mock()

    service._repository = repository

    measurement = create_body_measurement()

    service.create_body_measurement(
        measurement
    )

    repository.create_body_measurement.assert_called_once_with(
        measurement
    )


# Verify that an existing Body Measurements record is updated.
def test_upsert_body_measurement_update():

    service = HealthService()

    repository = Mock()

    repository.update_body_measurement.return_value = True

    service._repository = repository

    measurement = create_body_measurement()

    service.upsert_body_measurement(
        date(2026, 8, 26),
        measurement,
    )

    repository.update_body_measurement.assert_called_once_with(
        date(2026, 8, 26),
        measurement,
    )

    repository.create_body_measurement.assert_not_called()


# Verify that a new Body Measurements record is created when no existing record is found.
def test_upsert_body_measurement_create():

    service = HealthService()

    repository = Mock()

    repository.update_body_measurement.return_value = False

    service._repository = repository

    measurement = create_body_measurement()

    service.upsert_body_measurement(
        date(2026, 8, 26),
        measurement,
    )

    repository.update_body_measurement.assert_called_once()

    repository.create_body_measurement.assert_called_once_with(
        measurement
    )