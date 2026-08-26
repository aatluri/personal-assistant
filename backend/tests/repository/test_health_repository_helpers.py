"""
Health Repository Helper Tests

Tests the repository's helper methods responsible for:

- Converting worksheet values into Python objects.
- Converting Python objects into worksheet rows.
- Handling empty worksheet values.
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


# Verify that an empty string is converted to None.
def test_empty_to_none_empty_string():

    repository = HealthRepository()

    assert repository._empty_to_none("") is None


# Verify that non-empty values are returned unchanged.
def test_empty_to_none_value():

    repository = HealthRepository()

    assert repository._empty_to_none(25) == 25
    assert repository._empty_to_none("HIIT") == "HIIT"


# Verify that a DailyLog object is converted into a worksheet row.
def test_daily_log_to_row():

    repository = HealthRepository()

    daily_log = create_daily_log()

    row = repository._daily_log_to_row(daily_log)

    assert row[0] == "August 26, 2026"
    assert row[1] == 80
    assert row[2] == "HIIT"
    assert row[3] == "Push-ups"


# Verify that a worksheet row is converted into a DailyLog object.
def test_row_to_daily_log():

    repository = HealthRepository()

    row = create_daily_log_row()

    daily_log = repository._row_to_daily_log(row)

    assert daily_log.date == date(2026, 8, 26)
    assert daily_log.weight_kg == 80
    assert daily_log.workout_type == "HIIT"
    assert daily_log.workout_summary == "Push-ups"


# Verify that a BodyMeasurements object is converted into a worksheet row.
def test_body_measurement_to_row():

    repository = HealthRepository()

    measurement = create_body_measurement()

    row = repository._body_measurement_to_row(measurement)

    assert row[0] == "August 26, 2026"
    assert row[1] == 18
    assert row[2] == 42
    assert row[3] == 8


# Verify that a worksheet row is converted into a BodyMeasurements object.
def test_row_to_body_measurement():

    repository = HealthRepository()

    row = create_body_measurement_row()

    measurement = repository._row_to_body_measurement(row)

    assert measurement.date == date(2026, 8, 26)
    assert measurement.body_fat_percent == 18
    assert measurement.muscle_mass_percent == 42
    assert measurement.visceral_fat == 8