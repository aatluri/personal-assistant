from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from app.data_cache import DataCache
from app.modules.health.body_measurements_metrics.body_measurements_schema import (
    BodyMeasurements,
)
from app.modules.health.dashboard import goals
from app.modules.health.dashboard.dashboard_schema import (
    BodySummary,
    BodyWeightPoint,
    DailyValues,
    DashboardSummary,
    Goals,
    Period,
    PeriodSummary,
    WorkoutTotals,
    WorkoutTypeTotals,
)
from app.modules.health.health_metrics.health_metrics_schema import (
    HealthMetrics,
)
from app.modules.health.heart_rate_notifications.heart_rate_notifications_schema import (
    HeartRateNotification,
)
from app.modules.health.nutrition_metrics.nutrition_metrics_schema import (
    NutritionMetrics,
)
from app.modules.health.sleep_metrics.sleep_metrics_schema import (
    SleepMetrics,
)
from app.modules.health.workout_metrics.workout_metrics_schema import (
    WorkoutMetrics,
)


# Day view compares the selected day with the average of the 30 days
# before it ("vs usual").
BASELINE_DAYS = 30

# Day view charts show the 7 days ending on the selected day, and the
# Body card looks back 30 days for its trend.
DAY_VIEW_CHART_DAYS = 7
DAY_VIEW_BODY_DAYS = 30


def get_period_bounds(
    period: Period,
    selected_date: date,
) -> tuple[date, date]:
    """
    Return the first and last date of the day, week or month that
    contains selected_date. Weeks run Monday to Sunday.
    """

    if period == "day":
        return selected_date, selected_date

    if period == "week":
        start = selected_date - timedelta(days=selected_date.weekday())
        return start, start + timedelta(days=6)

    start = selected_date.replace(day=1)
    next_month = (start + timedelta(days=32)).replace(day=1)
    return start, next_month - timedelta(days=1)


def get_comparison_bounds(
    period: Period,
    start: date,
    end: date,
) -> tuple[date, date]:
    """
    Return the range a period is compared with: the 30 days before a
    day, the previous week, or the previous month.
    """

    if period == "day":
        return start - timedelta(days=BASELINE_DAYS), start - timedelta(days=1)

    if period == "week":
        return start - timedelta(days=7), end - timedelta(days=7)

    return get_period_bounds("month", start - timedelta(days=1))


def _recorded(value):
    """
    Return the value, or None when nothing was recorded.

    For steps, sleep, calories, water and the recovery values (resting
    heart rate, HRV, blood oxygen, respiratory rate), a 0 means the day
    has no data (for example, the watch was not worn), so it is treated
    as missing rather than pulling averages down.
    """

    return None if not value else value


def _average(values: list) -> float | None:
    present = [value for value in values if value is not None]

    if not present:
        return None

    return round(sum(present) / len(present), 2)


def _dates(start: date, end: date) -> list[date]:
    return [
        start + timedelta(days=offset)
        for offset in range((end - start).days + 1)
    ]


@dataclass
class _DashboardData:
    """
    The six worksheets, indexed for lookups by date.
    """

    health: dict[date, HealthMetrics]
    sleep: dict[date, SleepMetrics]
    nutrition: dict[date, NutritionMetrics]
    body: list[BodyMeasurements]
    workouts: list[WorkoutMetrics]
    notifications: list[HeartRateNotification]

    # The same rows, grouped by date for the daily table.
    body_by_date: dict[date, BodyMeasurements]
    workouts_by_date: dict[date, list[WorkoutMetrics]]


class DashboardService:
    """
    Service layer for the Overview page.

    Combines the six metric worksheets into one table with a row per
    date, and applies the Overview rules: periods, averages over days
    with data, coverage, comparisons and body trends.

    It reads the six worksheets through the shared DataCache, which
    must have these sources: "health", "sleep", "nutrition", "body",
    "workouts" and "notifications".
    """

    def __init__(
        self,
        data_cache: DataCache,
        now: Callable[[], datetime] = datetime.now,
    ):
        """
        The clock is passed in, so tests can fix "today".
        """

        self._data_cache = data_cache
        self._now = now


    def _get_data(self) -> _DashboardData:
        body = sorted(self._data_cache.get("body"), key=lambda row: row.date)
        workouts = sorted(
            self._data_cache.get("workouts"),
            key=lambda row: row.workout_start_time,
        )

        workouts_by_date: dict[date, list[WorkoutMetrics]] = {}

        for workout in workouts:
            workouts_by_date.setdefault(workout.date, []).append(workout)

        return _DashboardData(
            health={row.date: row for row in self._data_cache.get("health")},
            sleep={row.date: row for row in self._data_cache.get("sleep")},
            nutrition={
                row.date: row for row in self._data_cache.get("nutrition")
            },
            body=body,
            workouts=workouts,
            notifications=sorted(
                self._data_cache.get("notifications"),
                key=lambda row: row.start_time,
            ),
            body_by_date={row.date: row for row in body},
            workouts_by_date=workouts_by_date,
        )


    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    def get_summary(
        self,
        period: Period,
        selected_date: date | None = None,
    ) -> DashboardSummary:
        """
        Return everything the Overview page shows for the day, week or
        month that contains selected_date (default: today).
        """

        today = self._now().date()
        selected_date = selected_date or today
        data = self._get_data()

        start, end = get_period_bounds(period, selected_date)
        comparison_start, comparison_end = get_comparison_bounds(
            period, start, end
        )
        is_current = start <= today <= end

        if period == "day":
            chart_start = end - timedelta(days=DAY_VIEW_CHART_DAYS - 1)
            body_start = end - timedelta(days=DAY_VIEW_BODY_DAYS - 1)
        else:
            chart_start = start
            body_start = start

        current = self._summarize(data, start, end, today)
        comparison = self._summarize(
            data, comparison_start, comparison_end, today
        )

        # Workout counts and minutes are only compared between complete
        # weeks or months. A single day has nothing useful to compare,
        # and a period in progress would always look behind.
        if period == "day" or is_current:
            comparison.workouts = None

        workouts = [
            workout
            for workout in data.workouts
            if start <= workout.date <= end
        ]

        return DashboardSummary(
            period=period,
            date=selected_date,
            start=start,
            end=end,
            days_in_period=(end - start).days + 1,
            days_elapsed=current.days,
            is_current=is_current,
            data_through=self._data_through(data, today),
            current=current,
            comparison=comparison,
            days=[
                self._daily_values(data, day)
                for day in _dates(chart_start, end)
            ],
            workouts=workouts,
            workout_types=self._workout_type_totals(workouts),
            notifications=[
                notification
                for notification in data.notifications
                if start <= notification.date <= end
            ],
            body=self._body_summary(data, body_start, end, today),
            goals=Goals(
                steps=goals.STEPS,
                protein_g=goals.PROTEIN_G,
                sleep_hours=goals.SLEEP_HOURS,
                water_ml=goals.WATER_ML,
            ),
        )


    def _daily_values(
        self,
        data: _DashboardData,
        day: date,
    ) -> DailyValues:
        """
        Build one row of the combined daily table.
        """

        values = DailyValues(date=day)

        health = data.health.get(day)

        if health is not None:
            # Active energy and flights belong to the same day's activity,
            # so they only count on days with steps.
            values.steps = _recorded(health.step_count)

            if values.steps is not None:
                values.active_energy_kcal = health.active_energy_kcal
                values.flights_climbed = health.flights_climbed

            values.resting_heart_rate_bpm = _recorded(
                health.resting_heart_rate_bpm
            )
            values.heart_rate_variability_ms = _recorded(
                health.heart_rate_variability_ms
            )
            values.blood_oxygen_saturation_percent = _recorded(
                health.blood_oxygen_saturation_percent
            )
            values.respiratory_rate_bpm = _recorded(
                health.respiratory_rate_bpm
            )

        sleep = data.sleep.get(day)

        if sleep is not None and _recorded(sleep.total_sleep_duration_hr):
            values.sleep_hours = sleep.total_sleep_duration_hr
            values.deep_sleep_hours = sleep.deep_sleep_hr
            values.core_sleep_hours = sleep.core_sleep_hr
            values.rem_sleep_hours = sleep.rem_sleep_hr
            values.awake_hours = sleep.awake_hr
            values.sleep_start_time = sleep.sleep_start_time
            values.sleep_end_time = sleep.sleep_end_time

        nutrition = data.nutrition.get(day)

        if nutrition is not None:
            # Macros only count on days with food logged, so a day with
            # only water logged does not pull the protein average down.
            values.dietary_energy_kcal = _recorded(
                nutrition.dietary_energy_kcal
            )

            if values.dietary_energy_kcal is not None:
                values.protein_g = nutrition.protein_g
                values.carbohydrates_g = nutrition.carbohydrates_g
                values.total_fat_g = nutrition.total_fat_g

            values.water_ml = _recorded(nutrition.water_ml)

        day_workouts = data.workouts_by_date.get(day, [])

        values.workout_count = len(day_workouts)
        values.workout_minutes = sum(
            workout.workout_duration_min or 0
            for workout in day_workouts
        )

        measurement = data.body_by_date.get(day)

        if measurement is not None:
            values.weight_kg = measurement.weight_kg

        return values


    def _summarize(
        self,
        data: _DashboardData,
        start: date,
        end: date,
        today: date,
    ) -> PeriodSummary:
        """
        Combine the daily values from start to end (or to today, for a
        period in progress).
        """

        last = min(end, today)

        days = (
            [self._daily_values(data, day) for day in _dates(start, last)]
            if last >= start
            else []
        )

        def average(field: str) -> float | None:
            return _average([getattr(day, field) for day in days])

        def total(field: str):
            return sum(
                getattr(day, field)
                for day in days
                if getattr(day, field) is not None
            )

        workouts = [
            workout
            for workout in data.workouts
            if start <= workout.date <= last
        ]

        return PeriodSummary(
            start=start,
            end=end,
            days=len(days),
            steps_average=average("steps"),
            steps_total=total("steps"),
            active_energy_kcal_average=average("active_energy_kcal"),
            active_energy_kcal_total=round(total("active_energy_kcal"), 2),
            sleep_hours_average=average("sleep_hours"),
            deep_sleep_hours_average=average("deep_sleep_hours"),
            core_sleep_hours_average=average("core_sleep_hours"),
            rem_sleep_hours_average=average("rem_sleep_hours"),
            awake_hours_average=average("awake_hours"),
            resting_heart_rate_bpm_average=average("resting_heart_rate_bpm"),
            heart_rate_variability_ms_average=average(
                "heart_rate_variability_ms"
            ),
            blood_oxygen_saturation_percent_average=average(
                "blood_oxygen_saturation_percent"
            ),
            respiratory_rate_bpm_average=average("respiratory_rate_bpm"),
            dietary_energy_kcal_average=average("dietary_energy_kcal"),
            protein_g_average=average("protein_g"),
            carbohydrates_g_average=average("carbohydrates_g"),
            total_fat_g_average=average("total_fat_g"),
            water_ml_average=average("water_ml"),
            workouts=self._workout_totals(workouts),
            activity_days=sum(1 for day in days if day.steps is not None),
            sleep_nights=sum(1 for day in days if day.sleep_hours is not None),
            nutrition_days=sum(
                1 for day in days if day.dietary_energy_kcal is not None
            ),
            water_days=sum(1 for day in days if day.water_ml is not None),
        )


    def _workout_totals(
        self,
        workouts: list[WorkoutMetrics],
    ) -> WorkoutTotals:
        return WorkoutTotals(
            count=len(workouts),
            minutes=sum(w.workout_duration_min or 0 for w in workouts),
            active_energy_kcal=round(
                sum(w.active_energy_kcal or 0 for w in workouts), 2
            ),
            distance_km=round(sum(w.distance_km or 0 for w in workouts), 2),
        )


    def _workout_type_totals(
        self,
        workouts: list[WorkoutMetrics],
    ) -> list[WorkoutTypeTotals]:
        """
        Total the workouts per type, most frequent first (the Month
        view of the Training card).
        """

        by_type: dict[str, list[WorkoutMetrics]] = {}

        for workout in workouts:
            by_type.setdefault(workout.workout_type, []).append(workout)

        totals = [
            WorkoutTypeTotals(
                workout_type=workout_type,
                **self._workout_totals(type_workouts).model_dump(),
            )
            for workout_type, type_workouts in by_type.items()
        ]

        return sorted(totals, key=lambda total: total.count, reverse=True)


    def _body_summary(
        self,
        data: _DashboardData,
        window_start: date,
        end: date,
        today: date,
    ) -> BodySummary:
        """
        Latest body values on or before the end of the period, and the
        change from the first to the last measurement in the window.
        """

        up_to_end = [row for row in data.body if row.date <= end]
        in_window = [row for row in up_to_end if row.date >= window_start]

        def latest(field: str) -> BodyMeasurements | None:
            for row in reversed(up_to_end):
                if getattr(row, field) is not None:
                    return row
            return None

        def change(field: str) -> float | None:
            values = [
                getattr(row, field)
                for row in in_window
                if getattr(row, field) is not None
            ]

            if len(values) < 2:
                return None

            return round(values[-1] - values[0], 2)

        summary = BodySummary(
            weight_change_kg=change("weight_kg"),
            body_fat_change_percent=change("body_fat_percent"),
            waist_change_cm=change("waist_cm"),
            trend=[
                BodyWeightPoint(date=row.date, weight_kg=row.weight_kg)
                for row in in_window
                if row.weight_kg is not None
            ],
        )

        summary.weigh_ins = len(summary.trend)

        latest_weight = latest("weight_kg")

        if latest_weight is not None:
            summary.latest_weight_kg = latest_weight.weight_kg
            summary.latest_weight_date = latest_weight.date
            summary.weight_days_old = (
                min(end, today) - latest_weight.date
            ).days

        latest_body_fat = latest("body_fat_percent")

        if latest_body_fat is not None:
            summary.latest_body_fat_percent = latest_body_fat.body_fat_percent

        latest_waist = latest("waist_cm")

        if latest_waist is not None:
            summary.latest_waist_cm = latest_waist.waist_cm

        return summary


    def _data_through(
        self,
        data: _DashboardData,
        today: date,
    ) -> date | None:
        """
        The latest date, up to today, that has any data. Imports run
        behind real time, so this tells the user how current the page is.
        """

        dates = [
            *data.health,
            *data.sleep,
            *data.nutrition,
            *(row.date for row in data.body),
            *(row.date for row in data.workouts),
            *(row.date for row in data.notifications),
        ]

        past_dates = [day for day in dates if day <= today]

        return max(past_dates, default=None)
