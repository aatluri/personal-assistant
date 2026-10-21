from datetime import date, datetime

from pydantic import BaseModel


class SleepMetrics(BaseModel):
    """
    Represents a single Sleep Metrics entry.

    Each instance corresponds to one row in the Sleep_Metrics worksheet.
    """

    date: date  # primary key

    sleep_start_time: datetime | None = None
    sleep_end_time: datetime | None = None

    total_sleep_duration_hr: float | None = None
    core_sleep_hr: float | None = None
    rem_sleep_hr: float | None = None
    deep_sleep_hr: float | None = None
    awake_hr: float | None = None

    source: str | None = None