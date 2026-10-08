from datetime import date
from unittest.mock import Mock

from app.modules.health.body_measurements_service import (
    BodyMeasurementsService,
)
from tests.helpers.test_data import create_body_measurement


# ============================================================================
# Body Measurements
# ============================================================================

# Verify that all Body Measurements are retrieved from the repository.
def test_get_body_measurements():

    service = BodyMeasurementsService()

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

    service = BodyMeasurementsService()

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

    service = BodyMeasurementsService()

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

    service = BodyMeasurementsService()

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

    service = BodyMeasurementsService()

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
