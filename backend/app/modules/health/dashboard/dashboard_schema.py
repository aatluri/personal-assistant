from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel

from app.modules.health.heart_rate_notifications.heart_rate_notifications_schema import (
    HeartRateNotification,
)
from app.modules.health.workout_metrics.workout_metrics_schema import (
    WorkoutMetrics,
)


Period = Literal["day", "week", "month"]


class DailyValues(BaseModel):
    """
    Every metric for one date: one row of the combined daily table.

    None means nothing was recorded that day, so charts can show a gap
    instead of a zero.
    """

    date: date

    # Activity
    steps: int | None = None
    active_energy_kcal: float | None = None
    flights_climbed: int | None = None

    # Sleep: the night that ended on this date, as Health Auto Export
    # stores it.
    sleep_hours: float | None = None
    deep_sleep_hours: float | None = None
    core_sleep_hours: float | None = None
    rem_sleep_hours: float | None = None
    awake_hours: float | None = None
    sleep_start_time: datetime | None = None
    sleep_end_time: datetime | None = None

    # Recovery
    resting_heart_rate_bpm: float | None = None
    heart_rate_variability_ms: float | None = None
    blood_oxygen_saturation_percent: float | None = None
    respiratory_rate_bpm: float | None = None

    # Nutrition
    dietary_energy_kcal: float | None = None
    protein_g: float | None = None
    carbohydrates_g: float | None = None
    total_fat_g: float | None = None
    water_ml: float | None = None

    # Workouts and body
    workout_count: int = 0
    workout_minutes: int = 0
    weight_kg: float | None = None


class WorkoutTotals(BaseModel):
    """
    Workouts added up over a period, or for one workout type.
    """

    count: int = 0
    minutes: int = 0
    active_energy_kcal: float = 0
    distance_km: float = 0


class WorkoutTypeTotals(WorkoutTotals):
    workout_type: str


class PeriodSummary(BaseModel):
    """
    The combined values for one period (a day, a week, a month or the
    30-day baseline).

    Averages count only the days that have a value. The *_days fields
    say how many days that was.
    """

    start: date
    end: date

    # Days from start up to today (or the end, for a past period).
    days: int

    steps_average: float | None = None
    steps_total: int = 0
    active_energy_kcal_average: float | None = None
    active_energy_kcal_total: float = 0

    sleep_hours_average: float | None = None
    deep_sleep_hours_average: float | None = None
    core_sleep_hours_average: float | None = None
    rem_sleep_hours_average: float | None = None
    awake_hours_average: float | None = None

    resting_heart_rate_bpm_average: float | None = None
    heart_rate_variability_ms_average: float | None = None
    blood_oxygen_saturation_percent_average: float | None = None
    respiratory_rate_bpm_average: float | None = None

    dietary_energy_kcal_average: float | None = None
    protein_g_average: float | None = None
    carbohydrates_g_average: float | None = None
    total_fat_g_average: float | None = None
    water_ml_average: float | None = None

    # None in a comparison where workout totals are not compared.
    workouts: WorkoutTotals | None = None

    # Coverage, e.g. "Logged 5 of 7 days".
    activity_days: int = 0
    sleep_nights: int = 0
    nutrition_days: int = 0
    water_days: int = 0


class BodyWeightPoint(BaseModel):
    date: date
    weight_kg: float


class BodySummary(BaseModel):
    """
    Body measurements for the Body card.

    Latest values are the most recent on or before the end of the
    period, even if older than the period. Changes compare the first and
    last measurement inside the window (the period, or the 30 days up
    to the selected day in Day view).
    """

    latest_weight_kg: float | None = None
    latest_weight_date: date | None = None
    weight_days_old: int | None = None
    weight_change_kg: float | None = None
    weigh_ins: int = 0
    trend: list[BodyWeightPoint] = []

    latest_body_fat_percent: float | None = None
    body_fat_change_percent: float | None = None

    latest_waist_cm: float | None = None
    waist_change_cm: float | None = None


class Goals(BaseModel):
    steps: int
    protein_g: float
    sleep_hours: float
    water_ml: float


class DashboardSummary(BaseModel):
    """
    Everything the Overview page shows for one Day, Week or Month.
    """

    period: Period
    date: date
    start: date
    end: date
    days_in_period: int
    days_elapsed: int
    is_current: bool

    # The earliest and latest dates (up to today) that have any data:
    # the range the page lets the user move through.
    data_from: date | None = None
    data_through: date | None = None

    current: PeriodSummary

    # Day: the 30 days before the selected day ("vs usual").
    # Week / Month: the previous week or month.
    comparison: PeriodSummary

    # One entry per date for the small charts: every date in the week
    # or month, or the 7 days ending on the selected day in Day view.
    days: list[DailyValues]

    workouts: list[WorkoutMetrics]
    workout_types: list[WorkoutTypeTotals]
    notifications: list[HeartRateNotification]
    body: BodySummary
    goals: Goals
