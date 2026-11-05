from datetime import date, datetime
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.main import app
from app.modules.health import api
from tests.helpers.test_data import create_heart_rate_notification


client = TestClient(app)


"""
Heart Rate Notifications API Tests

These tests verify the HTTP API layer for heart rate notifications.

The real HeartRateNotificationsService is replaced with a mock so that
the API can be tested independently of the service and repository
layers.

Each test swaps in its mock with pytest's monkeypatch fixture, which
puts the real service back when the test ends, so no test leaks its
mock into another.
"""


# Verify that all notifications are returned when no date is given.
def test_get_heart_rate_notifications(monkeypatch):

    service = Mock()
    service.get_heart_rate_notifications.return_value = [
        create_heart_rate_notification()
    ]

    monkeypatch.setattr(api, "heart_rate_notifications_service", service)

    response = client.get("/health/heart-rate-notifications")

    assert response.status_code == 200
    assert len(response.json()) == 1

    service.get_heart_rate_notifications.assert_called_once()
    service.get_heart_rate_notifications_by_date.assert_not_called()


# Verify that the date filter is passed to the service.
def test_get_heart_rate_notifications_by_date(monkeypatch):

    service = Mock()
    service.get_heart_rate_notifications_by_date.return_value = [
        create_heart_rate_notification()
    ]

    monkeypatch.setattr(api, "heart_rate_notifications_service", service)

    response = client.get(
        "/health/heart-rate-notifications",
        params={"notification_date": "2026-10-29"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body[0]["notification_type"] == "Low Heart Rate"
    assert body[0]["readings"] == "39, 40, 39, 39"

    service.get_heart_rate_notifications_by_date.assert_called_once_with(
        date(2026, 10, 29)
    )


# Verify that a notification is returned by its start time.
def test_get_heart_rate_notification_found(monkeypatch):

    service = Mock()
    service.get_heart_rate_notification.return_value = (
        create_heart_rate_notification()
    )

    monkeypatch.setattr(api, "heart_rate_notifications_service", service)

    response = client.get(
        "/health/heart-rate-notification",
        params={"start_time": "2026-10-29T08:00:08"},
    )

    assert response.status_code == 200

    service.get_heart_rate_notification.assert_called_once_with(
        datetime(2026, 10, 29, 8, 0, 8)
    )


# Verify that 404 is returned when no notification has that start time.
def test_get_heart_rate_notification_not_found(monkeypatch):

    service = Mock()
    service.get_heart_rate_notification.return_value = None

    monkeypatch.setattr(api, "heart_rate_notifications_service", service)

    response = client.get(
        "/health/heart-rate-notification",
        params={"start_time": "2026-10-29T09:00:00"},
    )

    assert response.status_code == 404


# Verify that a new notification can be created.
def test_create_heart_rate_notification(monkeypatch):

    service = Mock()

    monkeypatch.setattr(api, "heart_rate_notifications_service", service)

    notification = create_heart_rate_notification()

    response = client.post(
        "/health/heart-rate-notifications",
        json=notification.model_dump(mode="json"),
    )

    assert response.status_code == 201

    service.create_heart_rate_notification.assert_called_once_with(
        notification
    )


# Verify that PUT upserts using the start time from the body.
def test_update_heart_rate_notification(monkeypatch):

    service = Mock()

    monkeypatch.setattr(api, "heart_rate_notifications_service", service)

    notification = create_heart_rate_notification()

    response = client.put(
        "/health/heart-rate-notifications",
        json=notification.model_dump(mode="json"),
    )

    assert response.status_code == 200

    service.upsert_heart_rate_notification.assert_called_once_with(
        notification.start_time,
        notification,
    )
