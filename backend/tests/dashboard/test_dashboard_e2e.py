from datetime import date, timedelta

import pytest
import requests

from app.modules.health.dashboard import goals


"""
Overview End-to-End Tests

Calls GET /health/dashboard/summary on the running backend, which reads
the real Google Sheet through its cache. These tests only read: nothing
is written, so there is nothing to clean up.

Real data changes all the time, so the tests do not check particular
numbers. They check rules that must hold for any data: the period
surrounds the date, coverage never exceeds the days counted, missing
values are null rather than 0, and so on.

Needs the backend running at BASE_URL. Live tests are opt-in: run with
pytest -m e2e (see CLAUDE.md).
"""


BASE_URL = "http://127.0.0.1:8000"
SUMMARY_URL = f"{BASE_URL}/health/dashboard/summary"

# The first request may wait for the cache to load all six worksheets.
TIMEOUT_SECONDS = 120

# Today's day, week and month, plus a past month and week that have
# data in the Sheet.
CASES = [
    ("day", None),
    ("week", None),
    ("month", None),
    ("month", "2023-05-15"),
    ("week", "2023-05-15"),
]

DAILY_FIELDS = [
    "steps",
    "sleep_hours",
    "resting_heart_rate_bpm",
    "heart_rate_variability_ms",
    "blood_oxygen_saturation_percent",
    "respiratory_rate_bpm",
    "dietary_energy_kcal",
    "water_ml",
    "weight_kg",
]

AVERAGE_FIELDS = [
    "steps_average",
    "sleep_hours_average",
    "resting_heart_rate_bpm_average",
    "heart_rate_variability_ms_average",
    "blood_oxygen_saturation_percent_average",
    "respiratory_rate_bpm_average",
    "dietary_energy_kcal_average",
    "protein_g_average",
    "water_ml_average",
]


def get_summary(period: str, summary_date: str | None, refresh=False) -> dict:

    params = {"period": period}

    if summary_date:
        params["date"] = summary_date

    if refresh:
        params["refresh"] = "true"

    response = requests.get(
        SUMMARY_URL,
        params=params,
        timeout=TIMEOUT_SECONDS,
    )

    assert response.status_code == 200, response.text

    return response.json()


def as_date(text: str | None) -> date | None:
    return None if text is None else date.fromisoformat(text)


# Verify the period dates: they surround the requested date, weeks run
# Monday to Sunday, months start on the 1st, and "current" means the
# period contains today.
@pytest.mark.parametrize("period, summary_date", CASES)
def test_period_dates(period, summary_date):

    summary = get_summary(period, summary_date)
    today = date.today()

    start = as_date(summary["start"])
    end = as_date(summary["end"])
    selected = as_date(summary["date"])

    assert summary["period"] == period
    assert selected == (as_date(summary_date) or today)
    assert start <= selected <= end
    assert summary["days_in_period"] == (end - start).days + 1

    if period == "day":
        assert start == end
    elif period == "week":
        assert start.weekday() == 0 and end.weekday() == 6
    else:
        assert start.day == 1 and (end + timedelta(days=1)).day == 1

    assert summary["is_current"] == (start <= today <= end)
    assert summary["days_elapsed"] == summary["current"]["days"]
    assert 0 <= summary["days_elapsed"] <= summary["days_in_period"]

    data_from = as_date(summary["data_from"])
    data_through = as_date(summary["data_through"])

    if data_through is None:
        assert data_from is None
    else:
        assert data_from <= data_through <= today


# Verify the chart days: consecutive dates ending on the period's end
# (7 for a day or week, the whole month otherwise), and missing values
# are null, never 0.
@pytest.mark.parametrize("period, summary_date", CASES)
def test_chart_days(period, summary_date):

    summary = get_summary(period, summary_date)
    days = summary["days"]

    expected = 7 if period in ("day", "week") else summary["days_in_period"]
    assert len(days) == expected

    dates = [as_date(day["date"]) for day in days]
    assert dates[-1] == as_date(summary["end"])
    assert all(
        later - earlier == timedelta(days=1)
        for earlier, later in zip(dates, dates[1:])
    )

    for day in days:
        for field in DAILY_FIELDS:
            assert day[field] is None or day[field] > 0, (day["date"], field)


# Verify averages and coverage: averages are null or positive, and no
# coverage count exceeds the days counted.
@pytest.mark.parametrize("period, summary_date", CASES)
def test_averages_and_coverage(period, summary_date):

    summary = get_summary(period, summary_date)

    for name in ("current", "comparison"):
        values = summary[name]

        for field in AVERAGE_FIELDS:
            assert values[field] is None or values[field] > 0, (name, field)

        for coverage in (
            "activity_days", "sleep_nights", "nutrition_days", "water_days"
        ):
            assert 0 <= values[coverage] <= values["days"], (name, coverage)

    # Workout totals are not compared for a day or a period in progress.
    if period == "day" or summary["is_current"]:
        assert summary["comparison"]["workouts"] is None


# Verify the body values, workouts, notifications and goals.
@pytest.mark.parametrize("period, summary_date", CASES)
def test_body_workouts_notifications_and_goals(period, summary_date):

    summary = get_summary(period, summary_date)
    start = as_date(summary["start"])
    end = as_date(summary["end"])

    body = summary["body"]
    latest = as_date(body["latest_weight_date"])

    assert latest is None or latest <= end
    assert body["latest_weight_kg"] is None or body["latest_weight_kg"] > 0
    assert body["weigh_ins"] == len(body["trend"])

    for workout in summary["workouts"]:
        assert start <= as_date(workout["date"]) <= end

    for notification in summary["notifications"]:
        assert start <= as_date(notification["date"]) <= end

    assert summary["goals"] == {
        "steps": goals.STEPS,
        "protein_g": goals.PROTEIN_G,
        "sleep_hours": goals.SLEEP_HOURS,
        "water_ml": goals.WATER_ML,
    }


# Verify that refresh=true reads the Sheet again and returns the same
# period.
def test_refresh_returns_the_same_period():

    cached = get_summary("week", "2023-05-15")
    refreshed = get_summary("week", "2023-05-15", refresh=True)

    assert refreshed["start"] == cached["start"]
    assert refreshed["end"] == cached["end"]
