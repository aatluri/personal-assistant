"""
Highlights for the Overview page, above the headline numbers, e.g.
"12/31 · days ≥ 10k steps" (a goal) or "8h 00m · best sleep · May 14"
(a record).

Each highlight is a small rule function that returns a Highlight (its
topic, value, caption, optional detail and progress, and the same as
one sentence), or None when it has nothing to say (no data), so a
highlight like "0/0" is never shown. DAY_RULES and PERIOD_RULES list the rules in
display order: to add, remove or reorder a highlight, change those lists.
Every highlight that has data is shown.

The rules only read the period's daily values and workouts, which the
DashboardService has already worked out (with its rules: a 0 counts as
nothing recorded, macros only on days with calories, and so on).
"""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date

from app.modules.health.dashboard.dashboard_schema import (
    DailyValues,
    Goals,
    Highlight,
    Period,
)
from app.modules.health.workout_metrics.workout_metrics_schema import (
    WorkoutMetrics,
)


@dataclass(frozen=True)
class HighlightContext:
    """
    What the rules can look at.

    days: the period's daily values, from its start up to today (Day
    view: the one day). workouts: the period's workouts.
    """

    period: Period
    days: list[DailyValues]
    workouts: list[WorkoutMetrics]
    goals: Goals
    is_current: bool


Rule = Callable[[HighlightContext], Highlight | None]


# -----------------------------------------------------------------------------
# Text
# -----------------------------------------------------------------------------

def _number(value: float) -> str:
    """
    14320 -> "14,320"
    """

    return f"{round(value):,}"


def _hours(hours: float) -> str:
    """
    7.8 -> "7h 48m"; 0.5 -> "30m"
    """

    minutes = round(hours * 60)

    if minutes < 60:
        return f"{minutes}m"

    return f"{minutes // 60}h {minutes % 60:02d}m"


def _litres(millilitres: float) -> str:
    """
    2100 -> "2.1"; 3000 -> "3"
    """

    return f"{millilitres / 1000:.1f}".rstrip("0").rstrip(".")


def _steps_goal(goal: int) -> str:
    """
    10000 -> "10k"; 8500 -> "8,500"
    """

    return f"{goal // 1000}k" if goal % 1000 == 0 else _number(goal)


def _when(day: date, period: Period) -> str:
    """
    A day within the period: "Tue" in a week, "Oct 18" in a month.
    """

    return day.strftime("%a") if period == "week" else f"{day:%b} {day.day}"


def _best(days: list[DailyValues], field: str) -> DailyValues | None:
    """
    The day with the highest value; on a tie, the earlier day.
    """

    best = None

    for day in days:
        value = getattr(day, field)

        if value is not None and (best is None or value > getattr(best, field)):
            best = day

    return best


# -----------------------------------------------------------------------------
# Day rules: progress towards the day's goals
# -----------------------------------------------------------------------------

def _the_day(context: HighlightContext) -> DailyValues | None:
    return context.days[-1] if context.days else None


def _progress(value: float, goal: float) -> float:
    """
    How far towards the goal, from 0 to 1 (a goal beaten counts as 1).
    """

    return min(value / goal, 1.0) if goal else 0.0


def steps_progress(context: HighlightContext) -> Highlight | None:

    day = _the_day(context)

    if day is None or day.steps is None:
        return None

    goal = context.goals.steps

    return Highlight(
        topic="steps",
        value=_number(day.steps),
        label="steps",
        detail=f"of {_number(goal)}",
        progress=_progress(day.steps, goal),
        goal_met=day.steps >= goal,
        text=f"Steps {_number(day.steps)} of {_number(goal)}",
    )


def protein_progress(context: HighlightContext) -> Highlight | None:

    day = _the_day(context)

    if day is None or day.protein_g is None:
        return None

    goal = context.goals.protein_g

    return Highlight(
        topic="protein",
        value=f"{_number(day.protein_g)} g",
        label="protein",
        detail=f"of {_number(goal)} g",
        progress=_progress(day.protein_g, goal),
        goal_met=day.protein_g >= goal,
        text=f"Protein {_number(day.protein_g)} of {_number(goal)} g",
    )


def water_progress(context: HighlightContext) -> Highlight | None:

    day = _the_day(context)

    if day is None or day.water_ml is None:
        return None

    goal = context.goals.water_ml

    return Highlight(
        topic="water",
        value=f"{_litres(day.water_ml)} L",
        label="water",
        detail=f"of {_litres(goal)} L",
        progress=_progress(day.water_ml, goal),
        goal_met=day.water_ml >= goal,
        text=f"Water {_litres(day.water_ml)} of {_litres(goal)} L",
    )


def sleep_progress(context: HighlightContext) -> Highlight | None:

    day = _the_day(context)

    if day is None or day.sleep_hours is None:
        return None

    goal = context.goals.sleep_hours
    is_met = day.sleep_hours >= goal

    return Highlight(
        topic="sleep",
        value=_hours(day.sleep_hours),
        label="sleep",
        detail=f"goal {_number(goal)}h",
        progress=_progress(day.sleep_hours, goal),
        goal_met=is_met,
        text=(
            f"Sleep {_hours(day.sleep_hours)} · goal {_number(goal)}h "
            f"{'met' if is_met else 'not met'}"
        ),
    )


# -----------------------------------------------------------------------------
# Week / Month rules
# -----------------------------------------------------------------------------

def _goal_rate(
    context: HighlightContext,
    field: str,
    goal: float,
    topic: str,
    label: str,
    caption: str,
    unit: str,
) -> Highlight | None:
    """
    How many days reached the goal, counting only days that have a value
    for field: "12/31" with the caption, e.g. "days ≥ 10k steps", and
    the sentence "<label> goal met <n> of <m> <unit>". unit is plural
    ("logged days"); it is made singular for one day.
    """

    values = [
        getattr(day, field)
        for day in context.days
        if getattr(day, field) is not None
    ]

    if not values:
        return None

    met = sum(1 for value in values if value >= goal)
    total = len(values)

    if total == 1:
        unit = unit.removesuffix("s")

    return Highlight(
        topic=topic,
        value=f"{met}/{total}",
        label=caption,
        progress=met / total,
        goal_met=met == total,
        text=f"{label} goal met {met} of {total} {unit}",
    )


def steps_goal_rate(context: HighlightContext) -> Highlight | None:
    goal = context.goals.steps
    return _goal_rate(
        context, "steps", goal, "steps", "Steps",
        f"days ≥ {_steps_goal(goal)} steps", "days",
    )


def protein_goal_rate(context: HighlightContext) -> Highlight | None:
    goal = context.goals.protein_g
    return _goal_rate(
        context, "protein_g", goal, "protein", "Protein",
        f"logged days ≥ {_number(goal)} g protein", "logged days",
    )


def sleep_goal_rate(context: HighlightContext) -> Highlight | None:
    goal = context.goals.sleep_hours
    return _goal_rate(
        context, "sleep_hours", goal, "sleep", "Sleep",
        f"nights ≥ {_number(goal)}h sleep", "nights",
    )


def water_goal_rate(context: HighlightContext) -> Highlight | None:
    goal = context.goals.water_ml
    return _goal_rate(
        context, "water_ml", goal, "water", "Water",
        f"days ≥ {_litres(goal)} L water", "days",
    )


def step_streak(context: HighlightContext) -> Highlight | None:
    """
    Consecutive days reaching the steps goal. A day with no data breaks
    the streak.

    A period in progress shows the current streak, ending on its last
    day with data (today's steps may not be imported yet); a finished
    period shows its longest. Nothing is shown below 2 days.
    """

    reached = [
        day.steps is not None and day.steps >= context.goals.steps
        for day in context.days
    ]

    goal = _steps_goal(context.goals.steps)

    if context.is_current:
        recorded = [
            index
            for index, day in enumerate(context.days)
            if day.steps is not None
        ]

        streak = 0

        if recorded:
            for index in range(recorded[-1], -1, -1):
                if not reached[index]:
                    break
                streak += 1

        if streak < 2:
            return None

        return Highlight(
            topic="streak",
            value=f"{streak} days",
            label=f"{goal} streak so far",
            text=f"{goal} steps · {streak}-day streak",
        )

    longest = current = 0

    for is_reached in reached:
        current = current + 1 if is_reached else 0
        longest = max(longest, current)

    if longest < 2:
        return None

    return Highlight(
        topic="streak",
        value=f"{longest} days",
        label=f"longest {goal} streak",
        text=f"Longest {goal} streak · {longest} days",
    )


def best_sleep(context: HighlightContext) -> Highlight | None:
    """
    The longest night, once there are at least two to compare.
    """

    nights = [day for day in context.days if day.sleep_hours is not None]

    if len(nights) < 2:
        return None

    best = _best(nights, "sleep_hours")
    when = _when(best.date, context.period)

    return Highlight(
        topic="best",
        value=_hours(best.sleep_hours),
        label="best sleep",
        detail=when,
        text=f"Best sleep {when} · {_hours(best.sleep_hours)}",
    )


def most_steps(context: HighlightContext) -> Highlight | None:
    """
    The day with the most steps, once there are at least two to compare.
    """

    days = [day for day in context.days if day.steps is not None]

    if len(days) < 2:
        return None

    best = _best(days, "steps")
    when = _when(best.date, context.period)

    return Highlight(
        topic="best",
        value=_number(best.steps),
        label="most steps",
        detail=when,
        text=f"Most steps {when} · {_number(best.steps)}",
    )


def furthest_workout(context: HighlightContext) -> Highlight | None:
    """
    The workout that went furthest, or, when no workout has a distance
    (e.g. only strength training), the longest one. On a tie, the
    earlier workout.
    """

    workouts = sorted(context.workouts, key=lambda w: w.workout_start_time)

    with_distance = [w for w in workouts if w.distance_km]

    if with_distance:
        best = max(with_distance, key=lambda w: w.distance_km)
        when = _when(best.date, context.period)
        distance = f"{best.distance_km:.1f} km"

        return Highlight(
            topic="best",
            value=distance,
            label="furthest workout",
            detail=f"{best.workout_type} · {when}",
            text=f"Furthest workout · {best.workout_type} {distance} on {when}",
        )

    with_duration = [w for w in workouts if w.workout_duration_min]

    if not with_duration:
        return None

    best = max(with_duration, key=lambda w: w.workout_duration_min)
    when = _when(best.date, context.period)
    duration = f"{best.workout_duration_min} min"

    return Highlight(
        topic="best",
        value=duration,
        label="longest workout",
        detail=f"{best.workout_type} · {when}",
        text=f"Longest workout · {best.workout_type} {duration} on {when}",
    )


# -----------------------------------------------------------------------------
# The rules, in display order
# -----------------------------------------------------------------------------

DAY_RULES: list[Rule] = [
    steps_progress,
    protein_progress,
    water_progress,
    sleep_progress,
]

PERIOD_RULES: list[Rule] = [
    steps_goal_rate,
    protein_goal_rate,
    sleep_goal_rate,
    water_goal_rate,
    step_streak,
    best_sleep,
    most_steps,
    furthest_workout,
]


def build_highlights(context: HighlightContext) -> list[Highlight]:
    """
    Every highlight that has something to say, in display order: the
    Day rules for a day, the period rules for a week or month.
    """

    rules = DAY_RULES if context.period == "day" else PERIOD_RULES

    return [
        highlight
        for rule in rules
        if (highlight := rule(context)) is not None
    ]
