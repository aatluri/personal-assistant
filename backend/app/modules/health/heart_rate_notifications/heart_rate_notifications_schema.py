from datetime import date, datetime

from pydantic import BaseModel


class HeartRateNotification(BaseModel):
    """
    Represents a single heart rate notification from the watch, such as
    a low heart rate alert.

    Each instance corresponds to one row in the HR_Rate_Notifications
    worksheet. The start time is the unique key.
    """

    date: date
    notification_type: str  # readable label, e.g. "Low Heart Rate"
    start_time: datetime  # unique key
    end_time: datetime

    threshold_bpm: int | None = None
    min_heart_rate_bpm: int | None = None
    max_heart_rate_bpm: int | None = None
    avg_heart_rate_bpm: float | None = None

    # The heart rate readings in time order, as text, e.g. "39, 40, 39".
    readings: str | None = None

    source: str | None = None
