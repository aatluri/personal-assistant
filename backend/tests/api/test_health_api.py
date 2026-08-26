from datetime import date
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.modules.health import api
from tests.helpers.test_data import (
    create_daily_log,
    create_body_measurement,
)

client = TestClient(app)


"""
Health API Tests

Each test follows the same sequence:

1. Create a mock HealthService.
2. Replace the API's HealthService with the mock.
3. Configure the mock service to return predefined data.
4. Send an HTTP request using the FastAPI TestClient.
5. Verify the HTTP response and confirm the correct
   service method was called.
"""


# ============================================================================
# Daily Log
# ============================================================================

# Verify that all Daily Logs are returned successfully.
def test_get_daily_logs():

    # -------------------------------------------------------------
    # Create a mock HealthService.
    #
    # This replaces the real service so the API can be tested
    # without calling the actual business logic or repository.
    # -------------------------------------------------------------
    service = Mock()

    # -------------------------------------------------------------
    # Configure the mock service.
    #
    # Whenever the API calls:
    #
    #     health_service.get_daily_logs()
    #
    # return one predefined DailyLog object.
    # -------------------------------------------------------------
    service.get_daily_logs.return_value = [
        create_daily_log()
    ]

    # -------------------------------------------------------------
    # Replace the HealthService used by the API with our mock.
    #
    # From this point onwards, all API requests use the mock
    # instead of the real service implementation.
    # -------------------------------------------------------------
    api.health_service = service

    # -------------------------------------------------------------
    # Send an HTTP GET request to the API endpoint.
    #
    # TestClient behaves like a real client making an HTTP request,
    # but everything runs locally without starting the web server.
    # -------------------------------------------------------------
    response = client.get("/health/daily-logs")

    # -------------------------------------------------------------
    # Verify that the API returned HTTP 200 (Success).
    # -------------------------------------------------------------
    assert response.status_code == 200

    # -------------------------------------------------------------
    # Convert the JSON response into a Python object so that
    # individual fields can be verified.
    # -------------------------------------------------------------
    data = response.json()

    # -------------------------------------------------------------
    # Verify that the API returned the expected data.
    # -------------------------------------------------------------
    assert len(data) == 1
    assert data[0]["weight_kg"] == 80

    # -------------------------------------------------------------
    # Verify that the API called the expected service method exactly once.
    # -------------------------------------------------------------
    service.get_daily_logs.assert_called_once()


# Verify that a Daily Log is returned when the requested date exists.
def test_get_daily_log_found():

    service = Mock()

    service.get_daily_log.return_value = (
        create_daily_log()
    )

    api.health_service = service

    response = client.get(
        "/health/daily-logs/2026-08-26"
    )

    assert response.status_code == 200

    service.get_daily_log.assert_called_once_with(
        date(2026, 8, 26)
    )


# Verify that a 404 response is returned when the Daily Log does not exist.
def test_get_daily_log_not_found():

    service = Mock()

    service.get_daily_log.return_value = None

    api.health_service = service

    response = client.get(
        "/health/daily-logs/2026-08-26"
    )

    assert response.status_code == 404


# Verify that the latest Daily Log is returned.
def test_get_latest_daily_log():

    service = Mock()

    service.get_latest_daily_log.return_value = (
        create_daily_log()
    )

    api.health_service = service

    response = client.get("/health/latest")

    assert response.status_code == 200

    service.get_latest_daily_log.assert_called_once()


# Verify that a new Daily Log can be created.
def test_create_daily_log():

    service = Mock()

    api.health_service = service

    response = client.post(
        "/health/daily-logs",
        json=create_daily_log().model_dump(
            mode="json"
        ),
    )

    assert response.status_code == 201

    service.create_daily_log.assert_called_once()


# Verify that an existing Daily Log is updated.
def test_update_daily_log():

    service = Mock()

    api.health_service = service

    payload = create_daily_log().model_dump(
        mode="json"
    )

    response = client.put(
        "/health/daily-logs/2026-08-26",
        json=payload,
    )

    assert response.status_code == 200

    service.upsert_daily_log.assert_called_once()


# Verify that a 400 response is returned when the URL date
# does not match the request body date.
def test_update_daily_log_date_mismatch():

    service = Mock()

    api.health_service = service

    payload = create_daily_log().model_dump(
        mode="json"
    )

    payload["date"] = "2026-08-25"

    response = client.put(
        "/health/daily-logs/2026-08-26",
        json=payload,
    )

    assert response.status_code == 400


# ============================================================================
# Body Measurements
# ============================================================================

# Verify that all Body Measurements are returned successfully.
def test_get_body_measurements():

    service = Mock()

    service.get_body_measurements.return_value = [
        create_body_measurement()
    ]

    api.health_service = service

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

    api.health_service = service

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

    api.health_service = service

    response = client.get(
        "/health/body-measurements/2026-08-26"
    )

    assert response.status_code == 404


# Verify that a new Body Measurements record can be created.
def test_create_body_measurement():

    service = Mock()

    api.health_service = service

    response = client.post(
        "/health/body-measurements",
        json=create_body_measurement().model_dump(
            mode="json"
        ),
    )

    assert response.status_code == 201

    service.create_body_measurement.assert_called_once()


# Verify that an existing Body Measurements record is updated.
def test_update_body_measurement():

    service = Mock()

    api.health_service = service

    payload = create_body_measurement().model_dump(
        mode="json"
    )

    response = client.put(
        "/health/body-measurements/2026-08-26",
        json=payload,
    )

    assert response.status_code == 200

    service.upsert_body_measurement.assert_called_once()


# Verify that a 400 response is returned when the URL date
# does not match the request body date.
def test_update_body_measurement_date_mismatch():

    service = Mock()

    api.health_service = service

    payload = create_body_measurement().model_dump(
        mode="json"
    )

    payload["date"] = "2026-08-25"

    response = client.put(
        "/health/body-measurements/2026-08-26",
        json=payload,
    )

    assert response.status_code == 400