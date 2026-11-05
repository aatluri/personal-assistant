from unittest.mock import Mock

from app.modules.health.importers.heart_rate_notifications_importer import (
    build_heart_rate_notification_payloads,
    import_heart_rate_notifications,
)


"""
Heart Rate Notifications Importer Tests

These use synthetic Health Auto Export data written in the test, so no
real health data is needed.
"""


def make_reading(qty, start):
    """
    Return one heartRateData entry as Health Auto Export writes it.
    """

    return {"qty": qty, "units": "count/min", "start": start, "end": start}


def make_notification(**overrides):
    """
    Return one synthetic low heart rate notification, with overrides.
    """

    notification = {
        "heartNotification": "low_heart_rate_notification",
        "threshold": 40,
        "start": "2026-10-29 08:00:08 +0530",
        "end": "2026-10-29 08:10:08 +0530",
        "heartRateData": [
            make_reading(39, 1793241129.0),
            make_reading(40, 1793241309.0),
            make_reading(39, 1793241384.0),
            make_reading(39, 1793241511.0),
        ],
        "source": {"name": "Apple Watch", "identifier": "com.apple.health"},
    }

    notification.update(overrides)

    return notification


def export_with(*notifications):
    """
    Wrap notifications in the file structure Health Auto Export uses.
    """

    return {"data": {"heartRateNotifications": list(notifications)}}


# Verify that a notification becomes the payload the backend expects.
def test_build_payload_for_a_notification():

    payloads = build_heart_rate_notification_payloads(
        export_with(make_notification())
    )

    assert payloads == [
        {
            "date": "2026-10-29",
            "notification_type": "Low Heart Rate",
            "start_time": "2026-10-29T08:00:08+05:30",
            "end_time": "2026-10-29T08:10:08+05:30",
            "threshold_bpm": 40,
            "min_heart_rate_bpm": 39,
            "max_heart_rate_bpm": 40,
            "avg_heart_rate_bpm": 39.25,
            "readings": "39, 40, 39, 39",
            "source": "Health Auto Export",
        }
    ]


# Verify that readings are listed in time order, whatever the JSON order.
def test_readings_are_sorted_by_time():

    notification = make_notification(
        heartRateData=[
            make_reading(41, 300.0),
            make_reading(39, 100.0),
            make_reading(40, 200.0),
        ]
    )

    payload = build_heart_rate_notification_payloads(
        export_with(notification)
    )[0]

    assert payload["readings"] == "39, 40, 41"


# Verify that each known notification type gets its readable label.
def test_known_notification_types_get_readable_labels():

    payloads = build_heart_rate_notification_payloads(
        export_with(
            make_notification(heartNotification="low_heart_rate_notification"),
            make_notification(heartNotification="high_heart_rate_notification"),
            make_notification(
                heartNotification="irregular_heart_rhythm_notification"
            ),
        )
    )

    assert [payload["notification_type"] for payload in payloads] == [
        "Low Heart Rate",
        "High Heart Rate",
        "Irregular Rhythm",
    ]


# Verify that an unknown notification type is kept as its raw text.
def test_unknown_notification_type_is_kept_as_raw_text():

    payload = build_heart_rate_notification_payloads(
        export_with(make_notification(heartNotification="new_kind_of_alert"))
    )[0]

    assert payload["notification_type"] == "new_kind_of_alert"


# Verify that a missing threshold is sent empty.
def test_missing_threshold_is_sent_empty():

    payload = build_heart_rate_notification_payloads(
        export_with(make_notification(threshold=None))
    )[0]

    assert payload["threshold_bpm"] is None


# Verify that a notification without readings has empty statistics.
def test_notification_without_readings():

    payload = build_heart_rate_notification_payloads(
        export_with(make_notification(heartRateData=[]))
    )[0]

    assert payload["min_heart_rate_bpm"] is None
    assert payload["max_heart_rate_bpm"] is None
    assert payload["avg_heart_rate_bpm"] is None
    assert payload["readings"] is None


# Verify that a non-whole reading keeps its decimals.
def test_decimal_readings_keep_their_decimals():

    payload = build_heart_rate_notification_payloads(
        export_with(
            make_notification(
                heartRateData=[
                    make_reading(39.5, 100.0),
                    make_reading(40, 200.0),
                ]
            )
        )
    )[0]

    assert payload["readings"] == "39.5, 40"
    assert payload["avg_heart_rate_bpm"] == 39.75


# Verify that notifications without a start or end time are skipped.
def test_notifications_without_start_or_end_are_skipped():

    payloads = build_heart_rate_notification_payloads(
        export_with(
            make_notification(start=None),
            make_notification(end=None),
            make_notification(),
        )
    )

    assert len(payloads) == 1


# Verify that an export without notifications produces no payloads.
def test_export_without_notifications():

    assert build_heart_rate_notification_payloads({"data": {}}) == []


# Verify that every notification in the file is sent to the backend.
def test_import_heart_rate_notifications_sends_each_notification():

    backend_client = Mock()
    backend_client.update_heart_rate_notification.side_effect = (
        lambda payload: {"start_time": payload["start_time"]}
    )

    results = import_heart_rate_notifications(
        export_with(
            make_notification(start="2026-10-29 07:00:00 +0530"),
            make_notification(start="2026-10-29 08:00:08 +0530"),
        ),
        backend_client,
    )

    assert backend_client.update_heart_rate_notification.call_count == 2

    assert results == [
        {"start_time": "2026-10-29T07:00:00+05:30"},
        {"start_time": "2026-10-29T08:00:08+05:30"},
    ]
