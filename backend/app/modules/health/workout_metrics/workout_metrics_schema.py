from datetime import date, datetime, timedelta

from pydantic import BaseModel, field_serializer


class WorkoutMetrics(BaseModel):
    """
    Represents a single Workout Metrics entry.

    Each instance corresponds to one row in the Workout_Metrics worksheet.
    """

    date: date
    workout_type: str
    workout_start_time: datetime  # unique key
    workout_end_time: datetime
    workout_duration: timedelta

    total_energy_kcal: float | None = None
    active_energy_kcal: float | None = None
    max_heart_rate_bpm: float | None = None
    avg_heart_rate_bpm: float | None = None
    distance_mi: float | None = None
    avg_speed_mph: float | None = None

    @field_serializer("workout_duration")
    def serialize_workout_duration(
        self,
        value: timedelta,
    ) -> str:
        total_seconds = int(value.total_seconds())

        hours, remainder = divmod(
            total_seconds,
            3600,
        )

        minutes, seconds = divmod(
            remainder,
            60,
        )

        return f"{hours:02}:{minutes:02}:{seconds:02}"