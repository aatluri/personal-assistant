from datetime import date, datetime, timedelta, timezone
from unittest.mock import Mock

from app.modules.health.heart_rate_notifications.heart_rate_notifications_google_sheets_repository import (
    HeartRateNotificationsGoogleSheetsRepository,
)
from tests.helpers.test_data import (
    create_heart_rate_notification,
    create_heart_rate_notification_row,
)


"""
Heart Rate Notifications Repository Tests

The worksheet is replaced with a mock, so these tests never reach
Google Sheets.
"""


def make_repository(worksheet: Mock) -> HeartRateNotificationsGoogleSheetsRepository:
    """
    Return a repository whose worksheet is the given mock.
    """

    repository = HeartRateNotificationsGoogleSheetsRepository()

    repository._get_heart_rate_notifications_worksheet = Mock(
        return_value=worksheet
    )

    return repository


# Verify that all notifications are retrieved and converted correctly.
def test_get_heart_rate_notifications():

    worksheet = Mock()
    worksheet.get_all_records.return_value = [
        create_heart_rate_notification_row()
    ]

    notifications = make_repository(worksheet).get_heart_rate_notifications()

    assert len(notifications) == 1

    notification = notifications[0]

    assert notification.date == date(2026, 10, 29)
    assert notification.notification_type == "Low Heart Rate"
    assert notification.start_time == datetime(2026, 10, 29, 8, 0, 8)
    assert notification.end_time == datetime(2026, 10, 29, 8, 10, 8)
    assert notification.threshold_bpm == 40
    assert notification.min_heart_rate_bpm == 39
    assert notification.max_heart_rate_bpm == 40
    assert notification.avg_heart_rate_bpm == 39.25
    assert notification.readings == "39, 40, 39, 39"
    assert notification.source == "Health Auto Export"


# Verify that only the requested date is returned, earliest first.
def test_get_heart_rate_notifications_by_date_filters_and_sorts():

    worksheet = Mock()
    worksheet.get_all_records.return_value = [
        create_heart_rate_notification_row(
            StartDateTime="October 29, 2026 08:00:08",
        ),
        create_heart_rate_notification_row(
            Date="October 28, 2026",
            StartDateTime="October 28, 2026 07:00:00",
            EndDateTime="October 28, 2026 07:10:00",
        ),
        create_heart_rate_notification_row(
            StartDateTime="October 29, 2026 06:31:32",
        ),
    ]

    notifications = make_repository(
        worksheet
    ).get_heart_rate_notifications_by_date(date(2026, 10, 29))

    assert [n.start_time for n in notifications] == [
        datetime(2026, 10, 29, 6, 31, 32),
        datetime(2026, 10, 29, 8, 0, 8),
    ]


# Verify that a notification is found by its start time, ignoring timezone.
def test_get_heart_rate_notification_found_by_start_time():

    worksheet = Mock()
    worksheet.get_all_records.return_value = [
        create_heart_rate_notification_row()
    ]

    ist = timezone(timedelta(hours=5, minutes=30))

    notification = make_repository(worksheet).get_heart_rate_notification(
        datetime(2026, 10, 29, 8, 0, 8, tzinfo=ist)
    )

    assert notification is not None
    assert notification.start_time == datetime(2026, 10, 29, 8, 0, 8)


# Verify that None is returned when no notification has that start time.
def test_get_heart_rate_notification_not_found():

    worksheet = Mock()
    worksheet.get_all_records.return_value = [
        create_heart_rate_notification_row()
    ]

    notification = make_repository(worksheet).get_heart_rate_notification(
        datetime(2026, 10, 29, 9, 0, 0)
    )

    assert notification is None


# Verify that a new notification is appended as a full row.
def test_create_heart_rate_notification():

    worksheet = Mock()

    make_repository(worksheet).create_heart_rate_notification(
        create_heart_rate_notification()
    )

    worksheet.append_row.assert_called_once()

    row = worksheet.append_row.call_args.args[0]

    assert row[:10] == [
        "October 29, 2026",
        "Low Heart Rate",
        "October 29, 2026 08:00:08",
        "October 29, 2026 08:10:08",
        40,
        39,
        40,
        39.25,
        "39, 40, 39, 39",
        "Health Auto Export",
    ]

    # Updated_DateTime is the time of the write.
    datetime.strptime(row[10], "%B %d, %Y %H:%M:%S")
    assert len(row) == 11

    assert (
        worksheet.append_row.call_args.kwargs["value_input_option"]
        == "USER_ENTERED"
    )


# Verify that an update overwrites only supplied fields, in the right row.
def test_update_heart_rate_notification_found():

    existing_row = create_heart_rate_notification_row()

    worksheet = Mock()
    worksheet.get_all_values.return_value = [
        list(existing_row.keys()),
        [str(value) for value in existing_row.values()],
    ]

    incoming = create_heart_rate_notification(
        max_heart_rate_bpm=42,
        readings="39, 42",
        threshold_bpm=None,
        avg_heart_rate_bpm=None,
    )

    updated = make_repository(worksheet).update_heart_rate_notification(
        datetime(2026, 10, 29, 8, 0, 8),
        incoming,
    )

    assert updated is True

    worksheet.update.assert_called_once()

    assert worksheet.update.call_args.kwargs["range_name"] == "A2:K2"

    row = worksheet.update.call_args.kwargs["values"][0]

    # Supplied values overwrite.
    assert row[6] == 42
    assert row[8] == "39, 42"

    # None keeps the existing values.
    assert row[4] == 40
    assert row[7] == 39.25

    assert len(row) == 11


# Verify that no update happens when the start time is not found.
def test_update_heart_rate_notification_not_found():

    existing_row = create_heart_rate_notification_row()

    worksheet = Mock()
    worksheet.get_all_values.return_value = [
        list(existing_row.keys()),
        [str(value) for value in existing_row.values()],
    ]

    updated = make_repository(worksheet).update_heart_rate_notification(
        datetime(2026, 10, 29, 9, 0, 0),
        create_heart_rate_notification(),
    )

    assert updated is False
    worksheet.update.assert_not_called()


# Verify that a single reading, which Sheets returns as a number, is text.
def test_row_to_notification_converts_single_reading_to_text():

    repository = HeartRateNotificationsGoogleSheetsRepository()

    notification = repository._row_to_notification(
        create_heart_rate_notification_row(Readings=39)
    )

    assert notification.readings == "39"


# Verify that empty cells become None.
def test_row_to_notification_handles_empty_values():

    repository = HeartRateNotificationsGoogleSheetsRepository()

    notification = repository._row_to_notification(
        create_heart_rate_notification_row(
            **{
                "Threshold (bpm)": "",
                "Min Heart Rate (bpm)": "",
                "Max Heart Rate (bpm)": "",
                "Avg Heart Rate (bpm)": "",
                "Readings": "",
                "Source": "",
            }
        )
    )

    assert notification.threshold_bpm is None
    assert notification.min_heart_rate_bpm is None
    assert notification.max_heart_rate_bpm is None
    assert notification.avg_heart_rate_bpm is None
    assert notification.readings is None
    assert notification.source is None
