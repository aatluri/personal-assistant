from datetime import date, datetime, timedelta
from unittest.mock import Mock

from app.data_cache import DataCache
from app.modules.health.body_measurements_metrics.body_measurements_schema import (
    BodyMeasurements,
)
from app.modules.health.dashboard import goals
from app.modules.health.dashboard.dashboard_service import (
    DashboardService,
    get_comparison_bounds,
    get_period_bounds,
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


"""
Dashboard Service Tests

The six metric services are fakes behind a real DataCache, and the
clock is fixed, so these tests never reach Google Sheets. "Today" is
Thursday, November 5, 2026; that week runs Monday, November 2 to
Sunday, November 8. The cache itself is tested in tests/test_data_cache.py.
"""


TODAY = datetime(2026, 11, 5, 12, 0)


class Clock:
    """
    A clock the tests can move forward.
    """

    def __init__(self, now: datetime):
        self.now = now

    def __call__(self) -> datetime:
        return self.now


def make_service(
    health=(),
    sleep=(),
    nutrition=(),
    body=(),
    workouts=(),
    notifications=(),
    clock=None,
):
    """
    Build a DashboardService over a DataCache of fake services
    returning these rows, wired the way api.py wires the real ones.

    Returns the service and the fake services, so tests can count reads.
    """

    fakes = {
        "health": Mock(**{"get_health_metrics.return_value": list(health)}),
        "sleep": Mock(**{"get_sleep_metrics.return_value": list(sleep)}),
        "nutrition": Mock(
            **{"get_nutrition_metrics.return_value": list(nutrition)}
        ),
        "body": Mock(**{"get_body_measurements.return_value": list(body)}),
        "workouts": Mock(**{"get_workout_metrics.return_value": list(workouts)}),
        "notifications": Mock(
            **{"get_heart_rate_notifications.return_value": list(notifications)}
        ),
    }

    clock = clock or Clock(TODAY)

    data_cache = DataCache(
        loaders={
            "health": fakes["health"].get_health_metrics,
            "sleep": fakes["sleep"].get_sleep_metrics,
            "nutrition": fakes["nutrition"].get_nutrition_metrics,
            "body": fakes["body"].get_body_measurements,
            "workouts": fakes["workouts"].get_workout_metrics,
            "notifications": (
                fakes["notifications"].get_heart_rate_notifications
            ),
        },
        now=clock,
    )

    service = DashboardService(data_cache, now=clock)

    return service, fakes


def read_counts(fakes) -> dict[str, int]:
    """
    How many times each worksheet has been read.
    """

    return {
        "health": fakes["health"].get_health_metrics.call_count,
        "sleep": fakes["sleep"].get_sleep_metrics.call_count,
        "nutrition": fakes["nutrition"].get_nutrition_metrics.call_count,
        "body": fakes["body"].get_body_measurements.call_count,
        "workouts": fakes["workouts"].get_workout_metrics.call_count,
        "notifications": (
            fakes["notifications"].get_heart_rate_notifications.call_count
        ),
    }


def workout(day: date, workout_type: str, hour: int, minutes: int, **fields):
    start = datetime(day.year, day.month, day.day, hour, 0)

    return WorkoutMetrics(
        date=day,
        workout_type=workout_type,
        workout_start_time=start,
        workout_end_time=start + timedelta(minutes=minutes),
        workout_duration_min=minutes,
        **fields,
    )


# ============================================================================
# Periods
# ============================================================================


# Verify that weeks run Monday to Sunday, including a week that crosses
# into a new month.
def test_week_bounds_run_monday_to_sunday():

    assert get_period_bounds("week", date(2026, 11, 5)) == (
        date(2026, 11, 2), date(2026, 11, 8)
    )
    assert get_period_bounds("week", date(2026, 11, 8)) == (
        date(2026, 11, 2), date(2026, 11, 8)
    )
    assert get_period_bounds("week", date(2026, 11, 1)) == (
        date(2026, 10, 26), date(2026, 11, 1)
    )


# Verify that months are calendar months, including February in a leap
# year and December.
def test_month_bounds_are_calendar_months():

    assert get_period_bounds("month", date(2026, 10, 15)) == (
        date(2026, 10, 1), date(2026, 10, 31)
    )
    assert get_period_bounds("month", date(2028, 2, 10)) == (
        date(2028, 2, 1), date(2028, 2, 29)
    )
    assert get_period_bounds("month", date(2026, 12, 31)) == (
        date(2026, 12, 1), date(2026, 12, 31)
    )


# Verify that a day is compared with the 30 days before it, a week with
# the previous week and a month with the previous month.
def test_comparison_bounds():

    assert get_comparison_bounds(
        "day", date(2026, 11, 5), date(2026, 11, 5)
    ) == (date(2026, 10, 6), date(2026, 11, 4))

    assert get_comparison_bounds(
        "week", date(2026, 11, 2), date(2026, 11, 8)
    ) == (date(2026, 10, 26), date(2026, 11, 1))

    assert get_comparison_bounds(
        "month", date(2026, 11, 1), date(2026, 11, 30)
    ) == (date(2026, 10, 1), date(2026, 10, 31))

    assert get_comparison_bounds(
        "month", date(2027, 1, 1), date(2027, 1, 31)
    ) == (date(2026, 12, 1), date(2026, 12, 31))


# Verify the period details of a week in progress.
def test_summary_describes_a_week_in_progress():

    service, _ = make_service()

    summary = service.get_summary("week", date(2026, 11, 5))

    assert summary.start == date(2026, 11, 2)
    assert summary.end == date(2026, 11, 8)
    assert summary.days_in_period == 7
    assert summary.days_elapsed == 4
    assert summary.is_current is True

    # The chart series covers the whole week, including days to come.
    assert [day.date for day in summary.days] == [
        date(2026, 11, 2) + timedelta(days=offset) for offset in range(7)
    ]


# Verify that without a date, the summary is for today.
def test_summary_defaults_to_today():

    service, _ = make_service()

    summary = service.get_summary("day")

    assert summary.date == date(2026, 11, 5)
    assert summary.start == date(2026, 11, 5)


# Verify that a future period has no elapsed days and no values.
def test_summary_for_a_future_period_is_empty():

    service, _ = make_service(
        health=[HealthMetrics(date=date(2026, 11, 5), step_count=8000)]
    )

    summary = service.get_summary("week", date(2026, 11, 12))

    assert summary.days_elapsed == 0
    assert summary.is_current is False
    assert summary.current.steps_average is None


# ============================================================================
# Daily values, averages and coverage
# ============================================================================


# Verify that days with no data, or a 0, are gaps: they are left out of
# averages and coverage instead of counting as zero.
def test_days_without_data_are_gaps_not_zeros():

    service, _ = make_service(
        health=[
            HealthMetrics(date=date(2026, 11, 2), step_count=10000),
            # Nov 3 has no row at all.
            HealthMetrics(date=date(2026, 11, 4), step_count=0),
            HealthMetrics(date=date(2026, 11, 5), step_count=8000),
        ]
    )

    summary = service.get_summary("week", date(2026, 11, 5))

    assert summary.current.steps_average == 9000
    assert summary.current.steps_total == 18000
    assert summary.current.activity_days == 2
    assert summary.current.days == 4

    assert [day.steps for day in summary.days] == [
        10000, None, None, 8000, None, None, None
    ]


# Verify that active energy only counts on days with steps.
def test_active_energy_only_counts_on_days_with_steps():

    service, _ = make_service(
        health=[
            HealthMetrics(
                date=date(2026, 11, 2), step_count=10000, active_energy_kcal=500
            ),
            HealthMetrics(
                date=date(2026, 11, 3), step_count=0, active_energy_kcal=20
            ),
        ]
    )

    summary = service.get_summary("week", date(2026, 11, 5))

    assert summary.current.active_energy_kcal_average == 500
    assert summary.current.active_energy_kcal_total == 500


# Verify that a sleep total of 0 counts as no sleep data, with no stages.
def test_sleep_total_of_zero_is_a_gap():

    service, _ = make_service(
        sleep=[
            SleepMetrics(
                date=date(2026, 11, 2),
                total_sleep_duration_hr=7.0,
                deep_sleep_hr=1.0,
            ),
            SleepMetrics(
                date=date(2026, 11, 3),
                total_sleep_duration_hr=0.0,
                deep_sleep_hr=0.5,
            ),
        ]
    )

    summary = service.get_summary("week", date(2026, 11, 5))

    assert summary.current.sleep_hours_average == 7.0
    assert summary.current.deep_sleep_hours_average == 1.0
    assert summary.current.sleep_nights == 1

    assert summary.days[1].sleep_hours is None
    assert summary.days[1].deep_sleep_hours is None


# Verify that sleep uses its stored date: the night that ended that
# morning, as Health Auto Export stores it.
def test_sleep_uses_the_stored_wake_up_date():

    service, _ = make_service(
        sleep=[
            SleepMetrics(
                date=date(2026, 11, 5),
                sleep_start_time=datetime(2026, 11, 4, 23, 40),
                sleep_end_time=datetime(2026, 11, 5, 6, 52),
                total_sleep_duration_hr=7.2,
            )
        ]
    )

    summary = service.get_summary("day", date(2026, 11, 5))

    assert summary.current.sleep_hours_average == 7.2
    assert summary.days[-1].date == date(2026, 11, 5)
    assert summary.days[-1].sleep_start_time == datetime(2026, 11, 4, 23, 40)


# Verify that nutrition averages use logged days only: macros count only
# on days with calories, and water counts on days with water.
def test_nutrition_averages_use_logged_days_only():

    service, _ = make_service(
        nutrition=[
            NutritionMetrics(
                date=date(2026, 11, 2),
                dietary_energy_kcal=2000,
                protein_g=150,
                water_ml=2500,
            ),
            # Water logged, but no food.
            NutritionMetrics(
                date=date(2026, 11, 3),
                dietary_energy_kcal=0,
                protein_g=0,
                water_ml=3000,
            ),
        ]
    )

    summary = service.get_summary("week", date(2026, 11, 5))

    assert summary.current.dietary_energy_kcal_average == 2000
    assert summary.current.protein_g_average == 150
    assert summary.current.water_ml_average == 2750
    assert summary.current.nutrition_days == 1
    assert summary.current.water_days == 2


# Verify that Day view compares with the average of the 30 days before
# the selected day, using only days with data, and charts the 7 days
# ending on that day.
def test_day_is_compared_with_the_30_days_before_it():

    service, _ = make_service(
        health=[
            HealthMetrics(date=date(2026, 11, 5), resting_heart_rate_bpm=50),
            HealthMetrics(date=date(2026, 11, 4), resting_heart_rate_bpm=55),
            HealthMetrics(date=date(2026, 10, 6), resting_heart_rate_bpm=57),
            # Outside the 30 days.
            HealthMetrics(date=date(2026, 10, 5), resting_heart_rate_bpm=99),
        ]
    )

    summary = service.get_summary("day", date(2026, 11, 5))

    assert summary.current.resting_heart_rate_bpm_average == 50
    assert summary.comparison.start == date(2026, 10, 6)
    assert summary.comparison.end == date(2026, 11, 4)
    assert summary.comparison.resting_heart_rate_bpm_average == 56

    assert [day.date for day in summary.days] == [
        date(2026, 10, 30) + timedelta(days=offset) for offset in range(7)
    ]


# Verify that a week is compared with the previous week.
def test_week_is_compared_with_the_previous_week():

    service, _ = make_service(
        health=[
            HealthMetrics(date=date(2026, 11, 2), step_count=9000),
            HealthMetrics(date=date(2026, 10, 27), step_count=6000),
            HealthMetrics(date=date(2026, 10, 28), step_count=8000),
        ]
    )

    summary = service.get_summary("week", date(2026, 11, 5))

    assert summary.comparison.start == date(2026, 10, 26)
    assert summary.comparison.steps_average == 7000
    assert summary.comparison.days == 7


# ============================================================================
# Workouts and notifications
# ============================================================================


# Verify that workouts are added up per day, per period and per type,
# most frequent type first.
def test_workouts_are_totalled_per_day_period_and_type():

    service, _ = make_service(
        workouts=[
            workout(date(2026, 11, 2), "Strength", 7, 55, active_energy_kcal=398),
            workout(
                date(2026, 11, 2), "Outdoor Run", 18, 34,
                active_energy_kcal=421, distance_km=6.2,
            ),
            workout(date(2026, 11, 4), "Strength", 7, 60, active_energy_kcal=430),
            # Previous week.
            workout(date(2026, 10, 27), "Strength", 7, 50),
        ]
    )

    summary = service.get_summary("week", date(2026, 11, 5))

    assert summary.current.workouts.count == 3
    assert summary.current.workouts.minutes == 149
    assert summary.current.workouts.active_energy_kcal == 1249
    assert summary.current.workouts.distance_km == 6.2

    assert summary.days[0].workout_count == 2
    assert summary.days[0].workout_minutes == 89

    assert [w.workout_type for w in summary.workouts] == [
        "Strength", "Outdoor Run", "Strength"
    ]
    assert [(t.workout_type, t.count) for t in summary.workout_types] == [
        ("Strength", 2), ("Outdoor Run", 1)
    ]


# Verify that workout totals are not compared for a week in progress or
# a single day, but are for a complete week.
def test_workout_totals_are_only_compared_for_complete_periods():

    service, _ = make_service(
        workouts=[
            workout(date(2026, 10, 20), "Strength", 7, 50),
            workout(date(2026, 10, 27), "Strength", 7, 55),
        ]
    )

    in_progress = service.get_summary("week", date(2026, 11, 5))
    one_day = service.get_summary("day", date(2026, 10, 27))
    complete = service.get_summary("week", date(2026, 10, 27))

    assert in_progress.comparison.workouts is None
    assert one_day.comparison.workouts is None

    assert complete.comparison.workouts.count == 1
    assert complete.comparison.workouts.minutes == 50


# Verify that only the period's heart rate notifications are returned.
def test_notifications_are_limited_to_the_period():

    def notification(day: date) -> HeartRateNotification:
        start = datetime(day.year, day.month, day.day, 3, 12)

        return HeartRateNotification(
            date=day,
            notification_type="Low Heart Rate",
            start_time=start,
            end_time=start + timedelta(minutes=10),
            min_heart_rate_bpm=39,
        )

    service, _ = make_service(
        notifications=[
            notification(date(2026, 11, 3)),
            notification(date(2026, 11, 1)),
        ]
    )

    summary = service.get_summary("week", date(2026, 11, 5))

    assert [n.date for n in summary.notifications] == [date(2026, 11, 3)]


# ============================================================================
# Body
# ============================================================================


BODY = [
    BodyMeasurements(date=date(2026, 10, 20), weight_kg=80.0, body_fat_percent=19.0),
    BodyMeasurements(date=date(2026, 11, 3), weight_kg=79.0, waist_cm=85),
    BodyMeasurements(date=date(2026, 11, 4), weight_kg=78.6, waist_cm=84),
]


# Verify the Body card for a month: latest values (even from before the
# month), how old the weight is, and the change within the month.
def test_body_summary_for_a_month():

    service, _ = make_service(body=BODY)

    body = service.get_summary("month", date(2026, 11, 5)).body

    assert body.latest_weight_kg == 78.6
    assert body.latest_weight_date == date(2026, 11, 4)
    assert body.weight_days_old == 1
    assert body.weight_change_kg == -0.4
    assert body.weigh_ins == 2
    assert [point.date for point in body.trend] == [
        date(2026, 11, 3), date(2026, 11, 4)
    ]

    # Body fat was last measured in October: shown, but no change.
    assert body.latest_body_fat_percent == 19.0
    assert body.body_fat_change_percent is None

    assert body.latest_waist_cm == 84
    assert body.waist_change_cm == -1


# Verify that Day view looks back 30 days for the body trend.
def test_body_summary_for_a_day_looks_back_30_days():

    service, _ = make_service(body=BODY)

    body = service.get_summary("day", date(2026, 11, 5)).body

    assert body.weigh_ins == 3
    assert body.weight_change_kg == -1.4


# Verify that a 0 for weight, body fat or waist counts as not measured:
# it is never the latest value, and is left out of the trend and change.
def test_body_summary_ignores_zero_values():

    service, _ = make_service(
        body=[
            *BODY,
            BodyMeasurements(
                date=date(2026, 11, 5),
                weight_kg=0.0,
                body_fat_percent=0.0,
                waist_cm=0.0,
            ),
        ]
    )

    summary = service.get_summary("month", date(2026, 11, 5))
    body = summary.body

    assert body.latest_weight_kg == 78.6
    assert body.latest_body_fat_percent == 19.0
    assert body.latest_waist_cm == 84
    assert body.weight_change_kg == -0.4
    assert body.weigh_ins == 2

    assert summary.days[4].weight_kg is None


# Verify that a measurement after the period is not used as "latest".
def test_body_summary_ignores_later_measurements():

    service, _ = make_service(body=BODY)

    body = service.get_summary("day", date(2026, 10, 25)).body

    assert body.latest_weight_kg == 80.0
    assert body.weight_days_old == 5


# ============================================================================
# Data through and goals
# ============================================================================


# Verify that "data through" is the latest date with any data, ignoring
# dates after today (such as leftover test rows dated 2099).
def test_data_through_is_the_latest_past_date_with_data():

    service, _ = make_service(
        health=[HealthMetrics(date=date(2026, 11, 3), step_count=5000)],
        sleep=[SleepMetrics(date=date(2026, 11, 4), total_sleep_duration_hr=7)],
        nutrition=[NutritionMetrics(date=date(2099, 1, 1))],
    )

    summary = service.get_summary("day", date(2026, 11, 5))

    assert summary.data_through == date(2026, 11, 4)


# Verify that there is no "data through" date when there is no data.
def test_data_through_is_none_without_data():

    service, _ = make_service()

    assert service.get_summary("day", date(2026, 11, 5)).data_through is None


# Verify that the goals are returned for the page.
def test_summary_includes_the_goals():

    service, _ = make_service()

    summary_goals = service.get_summary("day", date(2026, 11, 5)).goals

    assert summary_goals.steps == goals.STEPS
    assert summary_goals.protein_g == goals.PROTEIN_G
    assert summary_goals.sleep_hours == goals.SLEEP_HOURS
    assert summary_goals.water_ml == goals.WATER_ML


# ============================================================================
# Reading through the cache
# ============================================================================


# Verify that the service reads the worksheets through the DataCache:
# several summaries, for any period or date, read each worksheet once.
def test_summaries_read_each_worksheet_once_through_the_cache():

    service, fakes = make_service()

    service.get_summary("day", date(2026, 11, 5))
    service.get_summary("week", date(2026, 11, 5))
    service.get_summary("month", date(2022, 3, 10))

    assert read_counts(fakes) == {
        "health": 1,
        "sleep": 1,
        "nutrition": 1,
        "body": 1,
        "workouts": 1,
        "notifications": 1,
    }
