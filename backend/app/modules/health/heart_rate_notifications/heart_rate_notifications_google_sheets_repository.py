from datetime import date, datetime

from app.config import settings
from app.database.sheet_formats import DATE_FORMAT, DATETIME_FORMAT
from app.database.sheets_client import get_spreadsheet
from app.modules.health.heart_rate_notifications.heart_rate_notifications_schema import (
    HeartRateNotification,
)


class HeartRateNotificationsGoogleSheetsRepository:
    """
    Repository responsible for Heart Rate Notifications data access.

    Responsibilities:
    - Connect to Google Sheets.
    - Read and write data from the HR_Rate_Notifications worksheet.
    - Convert raw worksheet rows into HeartRateNotification objects.
    - Convert HeartRateNotification objects into worksheet rows.

    Business rules, calculations and analytics belong in the Service
    layer, except the partial-update merge in update_heart_rate_notification().

    How this class depends on the worksheet layout:
    - Reads look up values by header name, so the header text must match.
    - Writes depend on column order (see _notification_to_row()), so
      adding, removing or reordering columns requires a code change.
    """

    def _empty_to_none(self, value):
        """
        Convert empty worksheet values into None.

        Google Sheets returns an empty string for blank cells.
        Numeric values, including 0, are preserved.
        """
        return None if value == "" else value

    def get_heart_rate_notifications(self) -> list[HeartRateNotification]:
        """
        Retrieve every record from the HR_Rate_Notifications worksheet.
        """

        worksheet = self._get_heart_rate_notifications_worksheet()

        rows = worksheet.get_all_records()

        return [
            self._row_to_notification(row)
            for row in rows
        ]

    def get_heart_rate_notifications_by_date(
        self,
        notification_date: date,
    ) -> list[HeartRateNotification]:
        """
        Return all notifications on the given date, earliest first.
        """

        notifications = [
            notification
            for notification in self.get_heart_rate_notifications()
            if notification.date == notification_date
        ]

        return sorted(
            notifications,
            key=lambda notification: notification.start_time,
        )

    def get_heart_rate_notification(
        self,
        start_time: datetime,
    ) -> HeartRateNotification | None:
        """
        Return the notification with the given start time, or None if
        there is none. The start time is the unique key.
        """

        # The worksheet stores times without timezone information.
        normalized_start_time = start_time.replace(tzinfo=None)

        for notification in self.get_heart_rate_notifications():
            if notification.start_time == normalized_start_time:
                return notification

        return None

    def create_heart_rate_notification(
        self,
        notification: HeartRateNotification,
    ) -> None:
        """
        Append a new row without checking whether the start time already
        exists.

        Use HeartRateNotificationsService.upsert_heart_rate_notification()
        to avoid creating duplicate rows for the same notification.
        """

        worksheet = self._get_heart_rate_notifications_worksheet()

        # USER_ENTERED makes Sheets parse values as if typed by a user,
        # so dates and numbers are stored as real dates and numbers
        # rather than plain text.
        worksheet.append_row(
            self._notification_to_row(notification),
            value_input_option="USER_ENTERED",
        )

    def update_heart_rate_notification(
        self,
        start_time: datetime,
        notification: HeartRateNotification,
    ) -> bool:
        """
        Update an existing notification identified by its start time.

        This is a partial update: an incoming None means "not provided",
        not "clear this field". Only non-None incoming values overwrite
        the existing row.

        Returns:
            True if the matching row was found and updated.
            False if no matching row exists.
        """

        worksheet = self._get_heart_rate_notifications_worksheet()

        rows = worksheet.get_all_values()

        # Row 1 contains the worksheet headers.
        headers = rows[0]

        normalized_start_time = start_time.replace(tzinfo=None)

        # start=2 gives the real Sheet row number (Sheet rows are
        # 1-based and row 1 is the header), used in the update range.
        for row_number, row in enumerate(
            rows[1:],
            start=2,
        ):

            # StartDateTime is column C. Skip blank or incomplete rows.
            if len(row) < 3 or not row[2]:
                continue

            row_start_time = datetime.strptime(
                row[2],
                DATETIME_FORMAT,
            )

            if row_start_time != normalized_start_time:
                continue

            existing_notification = self._row_to_notification(
                dict(zip(headers, row))
            )

            merged_data = existing_notification.model_dump()

            for field, value in notification.model_dump().items():

                # The start time is the unique key and is never changed.
                if field == "start_time":
                    continue

                if value is not None:
                    merged_data[field] = value

            updated_row = self._notification_to_row(
                HeartRateNotification(**merged_data)
            )

            # Columns A-K are the 11 worksheet columns, Date through
            # Updated_DateTime. Change this together with the Sheet
            # and _notification_to_row().
            worksheet.update(
                range_name=f"A{row_number}:K{row_number}",
                values=[updated_row],
                value_input_option="USER_ENTERED",
            )

            return True

        return False

    def _get_heart_rate_notifications_worksheet(self):
        """
        Return the HR_Rate_Notifications worksheet.
        """

        spreadsheet = get_spreadsheet()

        return spreadsheet.worksheet(
            settings.HEALTH_HEART_RATE_NOTIFICATIONS_WORKSHEET
        )

    def _notification_to_row(
        self,
        notification: HeartRateNotification,
    ) -> list:
        """
        Convert a HeartRateNotification object into a worksheet row.

        The list order must match the worksheet's column order (A-K).
        The last value is Updated_DateTime, set to the time of this write.
        """

        return [
            notification.date.strftime(DATE_FORMAT),

            notification.notification_type,

            notification.start_time.strftime(DATETIME_FORMAT),
            notification.end_time.strftime(DATETIME_FORMAT),

            notification.threshold_bpm,

            notification.min_heart_rate_bpm,
            notification.max_heart_rate_bpm,
            notification.avg_heart_rate_bpm,

            notification.readings,

            notification.source,

            datetime.now().strftime(DATETIME_FORMAT),
        ]

    def _row_to_notification(
        self,
        row: dict,
    ) -> HeartRateNotification:
        """
        Convert a single Google Sheets row into a HeartRateNotification.

        The row is a header-keyed dict (as returned by get_all_records()),
        so column order does not matter here, but header text does.
        """

        readings = self._empty_to_none(row["Readings"])

        return HeartRateNotification(
            date=datetime.strptime(
                row["Date"],
                DATE_FORMAT,
            ).date(),

            notification_type=row["Notification Type"],

            start_time=datetime.strptime(
                row["StartDateTime"],
                DATETIME_FORMAT,
            ),

            end_time=datetime.strptime(
                row["EndDateTime"],
                DATETIME_FORMAT,
            ),

            threshold_bpm=self._empty_to_none(
                row["Threshold (bpm)"]
            ),

            min_heart_rate_bpm=self._empty_to_none(
                row["Min Heart Rate (bpm)"]
            ),

            max_heart_rate_bpm=self._empty_to_none(
                row["Max Heart Rate (bpm)"]
            ),

            avg_heart_rate_bpm=self._empty_to_none(
                row["Avg Heart Rate (bpm)"]
            ),

            # Sheets returns a single reading such as "39" as the number
            # 39, so always convert the readings back to text.
            readings=str(readings) if readings is not None else None,

            source=row["Source"] or None,
        )
