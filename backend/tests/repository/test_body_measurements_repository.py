"""
Body Measurement Repository Tests

Each test follows the same sequence:

1. Create a Body Measurement instance.
2. Create a mock worksheet (instead of connecting to Google Sheets).
3. Configure the mock worksheet to return predefined data.
4. Replace the repository's worksheet with the mock.
5. Call the repository method being tested.
6. Verify that the repository returns the expected result
   or calls the worksheet with the expected arguments.
"""


from datetime import date
from unittest.mock import Mock

from app.modules.health.body_measurements_repository import (
    BodyMeasurementsRepository,
)
from tests.helpers.test_data import (
    create_body_measurement,
    create_body_measurement_row,
)





# ============================================================================
# Body Measurements
# ============================================================================

# Verify that all Body Measurements are retrieved and converted correctly.
def test_get_body_measurements():

    repository = BodyMeasurementsRepository()

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

    assert measurement.weight_kg == 80
    assert measurement.body_mass_index == 26.7
    assert measurement.body_fat_percent == 18

    worksheet.get_all_records.assert_called_once()


# Verify that Body Measurements are returned when the requested date exists.
def test_get_body_measurement_found():

    repository = BodyMeasurementsRepository()

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

    repository = BodyMeasurementsRepository()

    repository.get_body_measurements = Mock(
        return_value=[]
    )

    measurement = repository.get_body_measurement(
        date(2026, 8, 26)
    )

    assert measurement is None


# Verify that a new Body Measurements record is appended to the worksheet.
def test_create_body_measurement():

    repository = BodyMeasurementsRepository()

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

    repository = BodyMeasurementsRepository()

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

    repository = BodyMeasurementsRepository()

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