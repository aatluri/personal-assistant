"""
Body Measurement Repository Helper Tests

Tests the repository's helper methods responsible for:

- Converting worksheet values into Python objects.
- Converting Python objects into worksheet rows.
- Handling empty worksheet values.
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


# Verify that a BodyMeasurements object is converted into a worksheet row.
def test_body_measurement_to_row():

    repository = BodyMeasurementsRepository()

    measurement = create_body_measurement()

    row = repository._body_measurement_to_row(measurement)

    assert row[0] == "August 26, 2026"

    assert row[1] == 80
    assert row[2] == 26.7
    assert row[3] == 18
    assert row[4] == 42
    assert row[5] == 8


# Verify that a worksheet row is converted into a BodyMeasurements object.
def test_row_to_body_measurement():

    repository = BodyMeasurementsRepository()

    row = create_body_measurement_row()

    measurement = repository._row_to_body_measurement(row)

    assert measurement.date == date(2026, 8, 26)

    assert measurement.weight_kg == 80
    assert measurement.body_mass_index == 26.7
    assert measurement.body_fat_percent == 18
    assert measurement.muscle_mass_percent == 42
    assert measurement.visceral_fat == 8