from datetime import date, datetime

from app.modules.health.heart_rate_notifications.heart_rate_notifications_google_sheets_repository import (
    HeartRateNotificationsGoogleSheetsRepository,
)
from app.modules.health.heart_rate_notifications.heart_rate_notifications_schema import (
    HeartRateNotification,
)


class HeartRateNotificationsService:
    """
    Service layer for Heart Rate Notifications.

    The service acts as the bridge between the repository and the
    rest of the application. It should not know how data is stored.
    """

    def __init__(self):
        """
        Create the repository used by the service.

        The Service delegates all data access to the Repository.
        """
        self._repository = HeartRateNotificationsGoogleSheetsRepository()


    def get_heart_rate_notifications(self) -> list[HeartRateNotification]:
        """
        Retrieve all heart rate notifications.
        """
        return self._repository.get_heart_rate_notifications()


    def get_heart_rate_notifications_by_date(
        self,
        notification_date: date,
    ) -> list[HeartRateNotification]:
        """
        Return the notifications on the given date, earliest first.
        """
        return self._repository.get_heart_rate_notifications_by_date(
            notification_date
        )


    def get_heart_rate_notification(
        self,
        start_time: datetime,
    ) -> HeartRateNotification | None:
        """
        Return the notification with the given start time, or None.
        """
        return self._repository.get_heart_rate_notification(start_time)


    def create_heart_rate_notification(
        self,
        notification: HeartRateNotification,
    ) -> None:
        """
        Create a new heart rate notification record.
        """
        self._repository.create_heart_rate_notification(notification)


    def upsert_heart_rate_notification(
        self,
        start_time: datetime,
        notification: HeartRateNotification,
    ) -> None:
        """
        Update the notification with this start time if it already
        exists; otherwise create it. Re-importing a file therefore
        updates its notifications instead of duplicating them.
        """

        updated = self._repository.update_heart_rate_notification(
            start_time,
            notification,
        )

        if not updated:
            self._repository.create_heart_rate_notification(
                notification
            )
