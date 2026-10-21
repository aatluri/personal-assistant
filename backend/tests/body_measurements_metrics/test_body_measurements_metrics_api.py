from datetime import date
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.modules.health import api
from tests.helpers.test_data import (
    create_body_measurement,
)


client = TestClient(app)


"""
Body Measurements API Tests

These tests verify the HTTP API layer for Body Measurements.

The real BodyMeasurementsService is replaced with a mock so that
the API can be tested independently of the service and
repository layers.
"""


# ============================================================================
# Body Measurements
# ============================================================================


# Verify that all Body Measurements are returned successfully.

def test_get_body_measurements():
    service = Mock()

    service.get_body_measurements.return_value = [
        create_body_measurement()
    ]

    api.body_measurements_service = service

    response = client.get(
        "/health/body-measurements"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    service.get_body_measurements.assert_called_once()


# Verify that Body Measurements are returned when the requested date exists.

def test_get_body_measurement_found():
    service = Mock()

    service.get_body_measurement.return_value = (
        create_body_measurement()
    )

    api.body_measurements_service = service

    response = client.get(
        "/health/body-measurements/2026-08-26"
    )

    assert response.status_code == 200

    service.get_body_measurement.assert_called_once_with(
        date(2026, 8, 26)
    )


# Verify that a 404 response is returned when Body Measurements do not exist.

def test_get_body_measurement_not_found():
    service = Mock()

    service.get_body_measurement.return_value = None

    api.body_measurements_service = service

    response = client.get(
        "/health/body-measurements/2026-08-26"
    )

    assert response.status_code == 404

    service.get_body_measurement.assert_called_once_with(
        date(2026, 8, 26)
    )


# Verify that a new Body Measurements record can be created.

def test_create_body_measurement():
    service = Mock()

    api.body_measurements_service = service

    body_measurement = create_body_measurement()

    response = client.post(
        "/health/body-measurements",
        json=body_measurement.model_dump(
            mode="json"
        ),
    )

    assert response.status_code == 201

    service.create_body_measurement.assert_called_once_with(
        body_measurement
    )


# Verify that a Body Measurements record can be updated or created.

def test_update_body_measurement():
    service = Mock()

    api.body_measurements_service = service

    body_measurement = create_body_measurement()

    payload = body_measurement.model_dump(
        mode="json"
    )

    response = client.put(
        "/health/body-measurements",
        json=payload,
    )

    assert response.status_code == 200

    service.upsert_body_measurement.assert_called_once_with(
        body_measurement.date,
        body_measurement,
    )