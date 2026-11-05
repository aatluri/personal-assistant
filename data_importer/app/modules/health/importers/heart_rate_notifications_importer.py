from datetime import datetime

from app.clients.backend_client import BackendClient
from app.modules.health.constants import (
    HEALTH_AUTO_EXPORT_TIMESTAMP_FORMAT,
    SOURCE,
)


# Readable labels stored in the Sheet for each Health Auto Export
# notification type. A type not listed here is stored as its raw text.
NOTIFICATION_TYPE_LABELS = {
    "low_heart_rate_notification": "Low Heart Rate",
    "high_heart_rate_notification": "High Heart Rate",
    "irregular_heart_rhythm_notification": "Irregular Rhythm",
}


def format_reading(value: float) -> str:
    """
    Format one heart rate reading for the Readings column: whole numbers
    without a decimal point ("39"), anything else as is ("39.5").
    """

    return f"{value:g}"


def build_heart_rate_notification_payloads(
    export_data: dict,
) -> list[dict]:
    """
    Transform a Health Auto Export heart rate notifications file into the
    payloads expected by the Personal Assistant backend, one per
    notification.

    Notifications without a start or end time are skipped: the start time
    is the record's unique key, and both are required by the backend.
    """

    notifications = (
        export_data
        .get("data", {})
        .get("heartRateNotifications", [])
    )

    payloads = []

    for notification in notifications:

        start = notification.get("start")
        end = notification.get("end")

        if not start or not end:
            continue

        start_time = datetime.strptime(start, HEALTH_AUTO_EXPORT_TIMESTAMP_FORMAT)
        end_time = datetime.strptime(end, HEALTH_AUTO_EXPORT_TIMESTAMP_FORMAT)

        # Readings in time order. Health Auto Export does not guarantee
        # the order of heartRateData.
        readings = sorted(
            notification.get("heartRateData") or [],
            key=lambda reading: reading.get("start", 0),
        )

        values = [
            reading["qty"]
            for reading in readings
            if reading.get("qty") is not None
        ]

        threshold = notification.get("threshold")
        raw_type = notification.get("heartNotification") or "Unknown"

        payloads.append(
            {
                "date": start_time.date().isoformat(),
                "notification_type": NOTIFICATION_TYPE_LABELS.get(
                    raw_type,
                    raw_type,
                ),
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "threshold_bpm": (
                    int(round(threshold)) if threshold is not None else None
                ),
                "min_heart_rate_bpm": (
                    int(round(min(values))) if values else None
                ),
                "max_heart_rate_bpm": (
                    int(round(max(values))) if values else None
                ),
                "avg_heart_rate_bpm": (
                    round(sum(values) / len(values), 2) if values else None
                ),
                # The comma is always followed by a space: without it,
                # Google Sheets could read "39,40" as the number 3,940.
                "readings": (
                    ", ".join(format_reading(value) for value in values)
                    or None
                ),
                "source": SOURCE,
            }
        )

    return payloads


def import_heart_rate_notifications(
    export_data: dict,
    backend_client: BackendClient,
) -> list[dict]:
    """
    Import every heart rate notification in the file into the backend.

    Each notification is sent separately; the backend updates the one
    with the same start time, or creates it.
    """

    return [
        backend_client.update_heart_rate_notification(payload)
        for payload in build_heart_rate_notification_payloads(export_data)
    ]
