from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from app.data_cache import CACHE_DURATION, DataCache


"""
DataCache Tests

The sources are mock functions and the clock is controlled by the
tests, so nothing reaches Google Sheets and no test actually waits.
"""


START = datetime(2026, 11, 5, 12, 0)


class Clock:
    """
    A clock the tests can move forward.
    """

    def __init__(self, now: datetime):
        self.now = now

    def __call__(self) -> datetime:
        return self.now


def make_cache(clock=None):
    """
    Build a DataCache with two sources. Returns the cache and the mock
    functions that read each source, so tests can count reads.
    """

    loaders = {
        "sleep": Mock(return_value=["sleep rows"]),
        "workouts": Mock(return_value=["workout rows"]),
    }

    cache = DataCache(loaders=loaders, now=clock or Clock(START))

    return cache, loaders


def read_counts(loaders) -> dict[str, int]:
    return {source: loader.call_count for source, loader in loaders.items()}


# Verify that a source is read once and then served from the cache.
def test_get_reads_a_source_once():

    cache, loaders = make_cache()

    assert cache.get("sleep") == ["sleep rows"]
    assert cache.get("sleep") == ["sleep rows"]

    assert read_counts(loaders) == {"sleep": 1, "workouts": 0}


# Verify that a source is read again once CACHE_DURATION has passed,
# but not before.
def test_get_reads_again_after_cache_duration():

    clock = Clock(START)
    cache, loaders = make_cache(clock)

    cache.get("sleep")

    clock.now = START + CACHE_DURATION - timedelta(seconds=1)
    cache.get("sleep")

    assert loaders["sleep"].call_count == 1

    clock.now = START + CACHE_DURATION
    cache.get("sleep")

    assert loaders["sleep"].call_count == 2


# Verify that a stale source is read again on its own, and only when it
# is next needed.
def test_mark_stale_reloads_only_that_source_when_next_needed():

    cache, loaders = make_cache()

    cache.get("sleep")
    cache.get("workouts")

    cache.mark_stale("sleep")

    # Marking does not read anything yet.
    assert read_counts(loaders) == {"sleep": 1, "workouts": 1}

    cache.get("sleep")
    cache.get("workouts")

    assert read_counts(loaders) == {"sleep": 2, "workouts": 1}


# Verify that unknown source names are rejected, so a typo in a save
# endpoint does not go unnoticed.
def test_unknown_sources_are_rejected():

    cache, _ = make_cache()

    with pytest.raises(ValueError):
        cache.mark_stale("steps")

    with pytest.raises(ValueError):
        cache.get("steps")


# Verify that refresh reads every source again, even within
# CACHE_DURATION.
def test_refresh_reloads_every_source():

    cache, loaders = make_cache()

    cache.get("sleep")
    cache.refresh()

    assert read_counts(loaders) == {"sleep": 2, "workouts": 1}

    cache.get("sleep")
    cache.get("workouts")

    assert read_counts(loaders) == {"sleep": 2, "workouts": 1}


# Verify that load_all fills the cache, so later gets read nothing.
def test_load_all_fills_the_cache():

    cache, loaders = make_cache()

    cache.load_all()
    cache.get("sleep")
    cache.get("workouts")

    assert read_counts(loaders) == {"sleep": 1, "workouts": 1}


# Verify that a failed load_all does not raise, and the next get reads
# the source again.
def test_failed_load_all_does_not_raise_and_next_get_retries():

    cache, loaders = make_cache()

    loaders["sleep"].side_effect = [
        RuntimeError("Sheets unavailable"),
        ["sleep rows"],
    ]

    cache.load_all()

    assert cache.get("sleep") == ["sleep rows"]
    assert loaders["sleep"].call_count == 2
