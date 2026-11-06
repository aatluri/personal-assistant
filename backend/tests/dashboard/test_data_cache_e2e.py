from datetime import datetime

import requests

from tests.sleep_metrics.test_sleep_metrics_e2e import (
    TEST_DATE,
    TEST_SOURCE,
    delete_test_rows_from_google_sheets,
)


"""
Data Cache End-to-End Tests

Check that the running backend's data cache works with the real Sheet,
using GET /health/dashboard/cache, which reports when each worksheet was
last read:

- a second Overview request is served from the cache (no read times
  change);
- refresh=true reads every worksheet again (every read time moves on);
- a save marks only its own worksheet stale, and only that worksheet is
  read again on the next Overview request.

The first two only read the Sheet. The save test writes one Sleep row
dated 2099-01-01 and deletes it afterwards; the deletion is guarded so
only 2099 test rows can ever be removed.

Needs the backend running at BASE_URL. Live tests are opt-in: run with
pytest -m e2e (see CLAUDE.md).
"""


BASE_URL = "http://127.0.0.1:8000"

# The first request may wait for the cache to load all six worksheets.
TIMEOUT_SECONDS = 120

SOURCES = {"health", "sleep", "nutrition", "body", "workouts", "notifications"}


def get_summary(**params) -> None:

    response = requests.get(
        f"{BASE_URL}/health/dashboard/summary",
        params={"period": "week", **params},
        timeout=TIMEOUT_SECONDS,
    )

    assert response.status_code == 200, response.text


def get_cache_status() -> dict:

    response = requests.get(
        f"{BASE_URL}/health/dashboard/cache",
        timeout=TIMEOUT_SECONDS,
    )

    assert response.status_code == 200, response.text

    return response.json()


def read_times(status: dict) -> dict[str, datetime]:
    """
    Each worksheet's last read time, as a datetime so that times
    compare correctly.
    """

    return {
        source: datetime.fromisoformat(status[source]["read_at"])
        for source in status
    }


# Verify that after an Overview request every worksheet is loaded, and a
# second request (for another period and date) reads nothing.
def test_second_request_is_served_from_the_cache():

    get_summary()

    first = get_cache_status()

    assert set(first) == SOURCES
    assert all(first[source]["loaded"] for source in SOURCES)
    assert all(first[source]["rows"] >= 0 for source in SOURCES)

    get_summary(period="month", date="2023-05-15")

    assert read_times(get_cache_status()) == read_times(first)


# Verify that refresh=true reads every worksheet again.
def test_refresh_reads_every_worksheet_again():

    get_summary()

    before = read_times(get_cache_status())

    get_summary(refresh="true")

    after = read_times(get_cache_status())

    for source in SOURCES:
        assert after[source] > before[source], source


# Verify that saving a Sleep row marks only the sleep worksheet stale,
# and the next Overview request reads only that worksheet again.
def test_save_marks_only_its_worksheet_stale():

    get_summary()

    before = read_times(get_cache_status())

    try:
        response = requests.put(
            f"{BASE_URL}/health/sleep-metrics",
            json={
                "date": TEST_DATE,
                "total_sleep_duration_hr": 7.0,
                "source": TEST_SOURCE,
            },
            timeout=TIMEOUT_SECONDS,
        )

        assert response.status_code == 200, response.text

        status = get_cache_status()

        assert status["sleep"]["stale"] is True
        assert all(
            status[source]["stale"] is False
            for source in SOURCES - {"sleep"}
        )

        get_summary()

        after_status = get_cache_status()
        after = read_times(after_status)

        assert after_status["sleep"]["stale"] is False
        assert after["sleep"] > before["sleep"]

        for source in SOURCES - {"sleep"}:
            assert after[source] == before[source], source

    finally:
        delete_test_rows_from_google_sheets()

        # The test row was deleted directly in the Sheet, which the
        # cache cannot see; read it again so the cache matches the Sheet.
        get_summary(refresh="true")
