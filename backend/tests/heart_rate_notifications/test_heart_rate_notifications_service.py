from datetime import date, datetime
from unittest.mock import Mock

from app.modules.health.heart_rate_notifications.heart_rate_notifications_service import (
    HeartRateNotificationsService,
)
from tests.helpers.test_data import create_heart_rate_notification


"""
Heart Rate Notifications Service Tests

The repository is replaced with a mock, so these tests check only how
the service uses it.
"""


def make_service() -> tuple[HeartRateNotificationsService, Mock]:
    """
    Return a service and the mock repository it uses.
    """

    service = HeartRateNotificationsService()
    repository = Mock()
    service._repository = repository

    return service, repository


# Verify that all notifications are retrieved from the repository.
def test_get_heart_rate_notifications():

    service, repository = make_service()

    repository.get_heart_rate_notifications.return_value = [
        create_heart_rate_notification()
    ]

    notifications = service.get_heart_rate_notifications()

    assert len(notifications) == 1
    repository.get_heart_rate_notifications.assert_called_once()


# Verify that notifications are requested for the given date.
def test_get_heart_rate_notifications_by_date():

    service, repository = make_service()

    repository.get_heart_rate_notifications_by_date.return_value = [
        create_heart_rate_notification()
    ]

    notifications = service.get_heart_rate_notifications_by_date(
        date(2026, 10, 29)
    )

    assert len(notifications) == 1
    repository.get_heart_rate_notifications_by_date.assert_called_once_with(
        date(2026, 10, 29)
    )


# Verify that a notification is requested by its start time.
def test_get_heart_rate_notification():

    service, repository = make_service()

    repository.get_heart_rate_notification.return_value = (
        create_heart_rate_notification()
    )

    notification = service.get_heart_rate_notification(
        datetime(2026, 10, 29, 8, 0, 8)
    )

    assert notification is not None
    repository.get_heart_rate_notification.assert_called_once_with(
        datetime(2026, 10, 29, 8, 0, 8)
    )


# Verify that a new notification is created through the repository.
def test_create_heart_rate_notification():

    service, repository = make_service()

    notification = create_heart_rate_notification()

    service.create_heart_rate_notification(notification)

    repository.create_heart_rate_notification.assert_called_once_with(
        notification
    )


# Verify that an existing notification is updated, not duplicated.
def test_upsert_heart_rate_notification_update():

    service, repository = make_service()

    repository.update_heart_rate_notification.return_value = True

    notification = create_heart_rate_notification()

    service.upsert_heart_rate_notification(
        notification.start_time,
        notification,
    )

    repository.update_heart_rate_notification.assert_called_once_with(
        notification.start_time,
        notification,
    )
    repository.create_heart_rate_notification.assert_not_called()


# Verify that a new notification is created when none exists yet.
def test_upsert_heart_rate_notification_create():

    service, repository = make_service()

    repository.update_heart_rate_notification.return_value = False

    notification = create_heart_rate_notification()

    service.upsert_heart_rate_notification(
        notification.start_time,
        notification,
    )

    repository.create_heart_rate_notification.assert_called_once_with(
        notification
    )
