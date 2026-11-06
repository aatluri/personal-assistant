from datetime import date, datetime
from unittest.mock import Mock, call

import pytest
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from app import main
from app.data_cache import DataCache
from app.main import app
from app.modules.health import api
from app.modules.health.dashboard.dashboard_service import DashboardService
from tests.helpers.test_data import (
    create_body_measurement,
    create_health_metric,
    create_heart_rate_notification,
    create_nutrition_metric,
    create_sleep_metric,
    create_workout_metric,
)


client = TestClient(app)


"""
Overview API Tests

These tests verify the Overview endpoint, that every metric save
endpoint marks its worksheet as stale in the shared data cache, and that
the cache is loaded when the backend starts.

The services and the cache are replaced with mocks (or a cache over
empty fake sources), so nothing reaches Google Sheets.
"""


SOURCES = ("health", "sleep", "nutrition", "body", "workouts", "notifications")


@pytest.fixture
def overview(monkeypatch):
    """
    Replace the API's cache and Overview service with test versions.

    The service is a real DashboardService over a cache of empty sources,
    wrapped in a Mock so tests can check how it was called. Returns
    (data_cache, dashboard_service).
    """

    data_cache = Mock(
        wraps=DataCache(
            loaders={source: Mock(return_value=[]) for source in SOURCES},
            now=lambda: datetime(2026, 11, 5, 12, 0),
        )
    )

    dashboard_service = Mock(
        wraps=DashboardService(
            data_cache,
            now=lambda: datetime(2026, 11, 5, 12, 0),
        )
    )

    monkeypatch.setattr(api, "data_cache", data_cache)
    monkeypatch.setattr(api, "dashboard_service", dashboard_service)

    return data_cache, dashboard_service


# ============================================================================
# GET /health/dashboard/summary
# ============================================================================


# Verify that the period and date are passed to the service and the
# summary is returned.
def test_get_dashboard_summary(overview):

    data_cache, dashboard_service = overview

    response = client.get(
        "/health/dashboard/summary?period=week&date=2026-11-05"
    )

    assert response.status_code == 200

    dashboard_service.get_summary.assert_called_once_with(
        "week", date(2026, 11, 5)
    )

    body = response.json()

    assert body["period"] == "week"
    assert body["start"] == "2026-11-02"
    assert body["end"] == "2026-11-08"
    assert body["goals"]["steps"] == 10000

    data_cache.refresh.assert_not_called()


# Verify that the date is optional: without it, the service uses today.
def test_get_dashboard_summary_defaults_to_today(overview):

    _, dashboard_service = overview

    response = client.get("/health/dashboard/summary?period=day")

    assert response.status_code == 200

    dashboard_service.get_summary.assert_called_once_with("day", None)

    assert response.json()["date"] == "2026-11-05"


# Verify that refresh=true reloads the cache before the summary reads it.
def test_get_dashboard_summary_with_refresh(overview):

    data_cache, _ = overview

    response = client.get(
        "/health/dashboard/summary?period=month&refresh=true"
    )

    assert response.status_code == 200

    # The cache mock records every call in order: the refresh first,
    # then the summary's reads.
    assert data_cache.mock_calls[0] == call.refresh()
    assert call.get("health") in data_cache.mock_calls[1:]


# Verify that an unknown period or an invalid date is rejected before
# the service is called.
@pytest.mark.parametrize(
    "query",
    [
        "period=year",
        "",
        "period=day&date=2026-13-01",
        "period=day&date=yesterday",
    ],
)
def test_get_dashboard_summary_rejects_invalid_input(overview, query):

    _, dashboard_service = overview

    response = client.get(f"/health/dashboard/summary?{query}")

    assert response.status_code == 422

    dashboard_service.get_summary.assert_not_called()


# ============================================================================
# Saves mark the data cache as stale
# ============================================================================


# Every metric save route: (method, path) -> (cache source, the API's
# service attribute, a request body).
SAVE_ROUTES = {
    ("POST", "/health/body-measurements"): ("body", "body_measurements_service", create_body_measurement),
    ("PUT", "/health/body-measurements"): ("body", "body_measurements_service", create_body_measurement),
    ("POST", "/health/workout-metrics"): ("workouts", "workout_metrics_service", create_workout_metric),
    ("PUT", "/health/workout-metrics"): ("workouts", "workout_metrics_service", create_workout_metric),
    ("POST", "/health/sleep-metrics"): ("sleep", "sleep_metrics_service", create_sleep_metric),
    ("PUT", "/health/sleep-metrics"): ("sleep", "sleep_metrics_service", create_sleep_metric),
    ("POST", "/health/health-metrics"): ("health", "health_metrics_service", create_health_metric),
    ("PUT", "/health/health-metrics"): ("health", "health_metrics_service", create_health_metric),
    ("POST", "/health/nutrition-metrics"): ("nutrition", "nutrition_metrics_service", create_nutrition_metric),
    ("PUT", "/health/nutrition-metrics"): ("nutrition", "nutrition_metrics_service", create_nutrition_metric),
    ("POST", "/health/heart-rate-notifications"): ("notifications", "heart_rate_notifications_service", create_heart_rate_notification),
    ("PUT", "/health/heart-rate-notifications"): ("notifications", "heart_rate_notifications_service", create_heart_rate_notification),
}


# Verify that SAVE_ROUTES lists every metric save route, so a new save
# endpoint that forgets to mark the cache fails this test. Lab routes
# are not cached, so they are left out.
def test_every_metric_save_route_is_covered():

    save_routes = {
        (method, route.path)
        for route in api.router.routes
        if isinstance(route, APIRoute)
        and not route.path.startswith("/health/lab")
        for method in route.methods
        if method in {"POST", "PUT", "PATCH", "DELETE"}
    }

    assert save_routes == set(SAVE_ROUTES)


# Verify that each metric save route marks its worksheet as stale after
# a successful save.
@pytest.mark.parametrize("method, path", list(SAVE_ROUTES))
def test_save_marks_its_worksheet_as_stale(monkeypatch, method, path):

    source, service_name, create_record = SAVE_ROUTES[(method, path)]

    data_cache = Mock()

    monkeypatch.setattr(api, service_name, Mock())
    monkeypatch.setattr(api, "data_cache", data_cache)

    response = client.request(
        method,
        path,
        json=create_record().model_dump(mode="json"),
    )

    assert response.status_code in (200, 201)

    data_cache.mark_stale.assert_called_once_with(source)


# Verify that a failed save does not mark the worksheet as stale.
def test_failed_save_does_not_mark_stale(monkeypatch):

    service = Mock()
    service.upsert_sleep_metric.side_effect = RuntimeError("Sheets unavailable")

    data_cache = Mock()

    monkeypatch.setattr(api, "sleep_metrics_service", service)
    monkeypatch.setattr(api, "data_cache", data_cache)

    failing_client = TestClient(app, raise_server_exceptions=False)

    response = failing_client.put(
        "/health/sleep-metrics",
        json=create_sleep_metric().model_dump(mode="json"),
    )

    assert response.status_code == 500

    data_cache.mark_stale.assert_not_called()


# ============================================================================
# Startup
# ============================================================================


# Verify that starting the backend loads the data cache in a background
# thread, so startup does not wait for the Sheet.
def test_startup_loads_the_data_cache_in_the_background(monkeypatch):

    thread_class = Mock()
    data_cache = Mock()

    # Replace only main.py's view of the threading module: the test
    # client itself needs the real threads.
    monkeypatch.setattr(main, "threading", Mock(Thread=thread_class))
    monkeypatch.setattr(main, "data_cache", data_cache)

    # Entering the client runs the app's startup code.
    with TestClient(app):
        pass

    thread_class.assert_called_once_with(
        target=data_cache.load_all,
        daemon=True,
    )
    thread_class.return_value.start.assert_called_once()
