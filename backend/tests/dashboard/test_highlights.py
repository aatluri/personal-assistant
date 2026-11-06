from datetime import date, datetime, timedelta

from app.modules.health.dashboard.dashboard_schema import (
    DailyValues,
    Goals,
)
from app.modules.health.dashboard.highlights import (
    DAY_RULES,
    PERIOD_RULES,
    HighlightContext,
    build_highlights,
)
from app.modules.health.workout_metrics.workout_metrics_schema import (
    WorkoutMetrics,
)


"""
Highlight Tests

The highlight rules are plain functions of a period's daily values and
workouts, so these tests build those directly; no cache or services are
involved. The week used is Monday, November 2 to Sunday, November 8,
2026; Oct 2026 is used for months.
"""


GOALS = Goals(steps=10_000, protein_g=140, sleep_hours=7, water_ml=3_000)


def week_days(**values_by_day: dict) -> list[DailyValues]:
    """
    The days of the week of Nov 2, 2026 with the given values, e.g.
    week_days(mon={"steps": 11000}). Days not given have no data.
    """

    names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    return [
        DailyValues(
            date=date(2026, 11, 2) + timedelta(days=index),
            **values_by_day.get(name, {}),
        )
        for index, name in enumerate(names)
    ]


def context(
    days: list[DailyValues],
    period="week",
    workouts=(),
    is_current=False,
) -> HighlightContext:

    return HighlightContext(
        period=period,
        days=days,
        workouts=list(workouts),
        goals=GOALS,
        is_current=is_current,
    )


def texts(highlight_context: HighlightContext) -> list[str]:
    return [h.text for h in build_highlights(highlight_context)]


def workout(day: date, workout_type: str, minutes: int, distance_km=None):

    start = datetime(day.year, day.month, day.day, 7, 0)

    return WorkoutMetrics(
        date=day,
        workout_type=workout_type,
        workout_start_time=start,
        workout_end_time=start + timedelta(minutes=minutes),
        workout_duration_min=minutes,
        distance_km=distance_km,
    )


# ============================================================================
# Day
# ============================================================================


# Verify the Day chips: progress towards each goal, in order.
def test_day_shows_progress_towards_each_goal():

    day = DailyValues(
        date=date(2026, 11, 5),
        steps=8240,
        protein_g=92,
        water_ml=2100,
        sleep_hours=7.2,
    )

    result = build_highlights(context([day], period="day"))

    assert [h.text for h in result] == [
        "Steps 8,240 of 10,000",
        "Protein 92 of 140 g",
        "Water 2.1 of 3 L",
        "Sleep 7h 12m · goal 7h met",
    ]
    assert [h.topic for h in result] == ["steps", "protein", "water", "sleep"]


# Verify that a Day chip is left out when its value is missing, and a
# missed sleep goal says so.
def test_day_leaves_out_missing_values():

    day = DailyValues(date=date(2026, 11, 5), sleep_hours=6.5)

    assert texts(context([day], period="day")) == [
        "Sleep 6h 30m · goal 7h not met",
    ]


# ============================================================================
# Week / Month: goal hit rates
# ============================================================================


# Verify that goal rates count only days with a value for that metric.
def test_goal_rates_count_only_days_with_data():

    days = week_days(
        mon={"steps": 11000, "protein_g": 150, "sleep_hours": 7.5, "water_ml": 3200},
        tue={"steps": 8000, "protein_g": 120, "sleep_hours": 6.0},
        wed={"steps": 12000},
    )

    result = texts(context(days))

    assert "Steps goal met 2 of 3 days" in result
    assert "Protein goal met 1 of 2 logged days" in result
    assert "Sleep goal met 1 of 2 nights" in result
    assert "Water goal met 1 of 1 day" in result


# ============================================================================
# Week / Month: step streak
# ============================================================================


# Verify that a finished period shows its longest streak, and that a day
# with no data breaks it.
def test_finished_period_shows_the_longest_streak():

    days = week_days(
        mon={"steps": 11000},
        tue={"steps": 12000},
        # Wednesday has no data: the streak breaks.
        thu={"steps": 10500},
        fri={"steps": 10000},
        sat={"steps": 13000},
        sun={"steps": 4000},
    )

    assert "Longest 10k streak · 3 days" in texts(context(days))


# Verify that a period in progress shows the current streak, ending on
# its last day with data.
def test_period_in_progress_shows_the_current_streak():

    days = week_days(
        mon={"steps": 4000},
        tue={"steps": 11000},
        wed={"steps": 12000},
        # Thursday (today) not imported yet.
    )[:4]

    assert "10k steps · 2-day streak" in texts(context(days, is_current=True))


# Verify that no streak is shown below 2 days.
def test_no_streak_below_two_days():

    days = week_days(mon={"steps": 11000}, tue={"steps": 4000})

    assert not any("streak" in text for text in texts(context(days)))
    assert not any(
        "streak" in text for text in texts(context(days, is_current=True))
    )


# ============================================================================
# Week / Month: bests
# ============================================================================


# Verify the best sleep and most steps, with the day named by weekday in
# a week; a tie goes to the earlier day.
def test_bests_in_a_week():

    days = week_days(
        mon={"steps": 9000, "sleep_hours": 7.0},
        tue={"steps": 14320, "sleep_hours": 7.8},
        wed={"steps": 14320, "sleep_hours": 7.8},
    )

    result = texts(context(days))

    assert "Best sleep Tue · 7h 48m" in result
    assert "Most steps Tue · 14,320" in result


# Verify that a month names the day by date.
def test_bests_in_a_month():

    days = [
        DailyValues(date=date(2026, 10, 11), sleep_hours=6.5),
        DailyValues(date=date(2026, 10, 12), sleep_hours=8.08),
    ]

    assert "Best sleep Oct 12 · 8h 05m" in texts(context(days, period="month"))


# Verify that bests need at least two days to compare.
def test_bests_need_two_days():

    days = week_days(mon={"steps": 9000, "sleep_hours": 7.0})

    result = texts(context(days))

    assert not any(text.startswith("Best sleep") for text in result)
    assert not any(text.startswith("Most steps") for text in result)


# Verify the furthest workout, falling back to the longest when no
# workout has a distance, and nothing without workouts.
def test_furthest_or_longest_workout():

    run = workout(date(2026, 10, 18), "Outdoor Run", 45, distance_km=8.2)
    walk = workout(date(2026, 10, 20), "Walk", 60, distance_km=4.0)
    strength = workout(date(2026, 10, 21), "Strength", 75)

    assert "Furthest workout · Outdoor Run 8.2 km on Oct 18" in texts(
        context([], period="month", workouts=[strength, walk, run])
    )

    assert "Longest workout · Strength 75 min on Oct 21" in texts(
        context([], period="month", workouts=[strength])
    )

    assert texts(context([], period="month")) == []


# ============================================================================
# Order and empty periods
# ============================================================================


# Verify that chips follow the rule order.
def test_chips_follow_the_rule_order():

    days = week_days(
        mon={"steps": 11000, "protein_g": 150, "sleep_hours": 7.5, "water_ml": 3200},
        tue={"steps": 12000, "protein_g": 150, "sleep_hours": 8.0, "water_ml": 3200},
    )

    result = texts(context(days, workouts=[workout(date(2026, 11, 3), "Run", 30, 5.0)]))

    assert result == [
        "Steps goal met 2 of 2 days",
        "Protein goal met 2 of 2 logged days",
        "Sleep goal met 2 of 2 nights",
        "Water goal met 2 of 2 days",
        "Longest 10k streak · 2 days",
        "Best sleep Tue · 8h 00m",
        "Most steps Tue · 12,000",
        "Furthest workout · Run 5.0 km on Tue",
    ]

    assert len(PERIOD_RULES) == 8
    assert len(DAY_RULES) == 4


# Verify that a period with no data has no highlights.
def test_no_data_means_no_highlights():

    assert texts(context(week_days())) == []
    assert texts(context([], period="day")) == []


# ============================================================================
# Tile parts: value, caption, detail, progress, goal met
# ============================================================================


# Verify a Day tile's parts: the value, "of <goal>", progress towards the
# goal (capped at 1 when beaten), and whether the goal was met.
def test_day_tile_parts():

    below = build_highlights(context(
        [DailyValues(date=date(2026, 11, 5), steps=8240)], period="day"
    ))[0]

    assert below.topic == "steps"
    assert below.value == "8,240"
    assert below.label == "steps"
    assert below.detail == "of 10,000"
    assert below.progress == 0.824
    assert below.goal_met is False

    beaten = build_highlights(context(
        [DailyValues(date=date(2026, 11, 5), steps=12000)], period="day"
    ))[0]

    assert beaten.progress == 1.0
    assert beaten.goal_met is True


# Verify a goal-rate tile: "met/total", its caption, progress, and that
# the goal counts as met only when it was met on every day.
def test_goal_rate_tile_parts():

    some = build_highlights(context(week_days(
        mon={"steps": 11000}, tue={"steps": 12000}, wed={"steps": 4000},
    )))[0]

    assert some.value == "2/3"
    assert some.label == "days ≥ 10k steps"
    assert some.progress == 2 / 3
    assert some.goal_met is False

    every = build_highlights(context(week_days(
        mon={"steps": 11000}, tue={"steps": 12000},
    )))[0]

    assert every.value == "2/2"
    assert every.goal_met is True


# Verify the streak tiles: no bar, and a caption saying whether the
# streak is the current one or the longest.
def test_streak_tile_parts():

    days = week_days(mon={"steps": 11000}, tue={"steps": 12000})

    longest = [h for h in build_highlights(context(days)) if h.topic == "streak"][0]
    current = [
        h for h in build_highlights(context(days, is_current=True))
        if h.topic == "streak"
    ][0]

    assert (longest.value, longest.label, longest.progress) == (
        "2 days", "longest 10k streak", None
    )
    assert (current.value, current.label) == ("2 days", "10k streak so far")


# Verify the best tiles: the value, what it is, and when.
def test_best_tile_parts():

    days = week_days(
        mon={"sleep_hours": 7.0, "steps": 9000},
        tue={"sleep_hours": 7.8, "steps": 14320},
    )

    run = workout(date(2026, 11, 3), "Outdoor Run", 45, distance_km=8.2)

    bests = [
        (h.value, h.label, h.detail, h.progress)
        for h in build_highlights(context(days, workouts=[run]))
        if h.topic == "best"
    ]

    assert bests == [
        ("7h 48m", "best sleep", "Tue", None),
        ("14,320", "most steps", "Tue", None),
        ("8.2 km", "furthest workout", "Outdoor Run · Tue", None),
    ]
