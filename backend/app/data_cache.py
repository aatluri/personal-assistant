from collections.abc import Callable
from datetime import datetime, timedelta
import threading
import time

from pydantic import BaseModel


# How long a source stays in the cache before it is read again. Saves
# through the API mark the affected source as stale sooner, and the
# Overview page's Refresh button reloads everything.
CACHE_DURATION = timedelta(hours=12)


class CacheSourceStatus(BaseModel):
    """
    The state of one cached source, for checking that the cache works.
    Contains no data, only counts and times.
    """

    loaded: bool
    rows: int | None = None
    read_at: datetime | None = None
    expires_at: datetime | None = None

    # True after a save, until the source is read again.
    stale: bool = False


class DataCache:
    """
    An in-memory cache of whole data sources, such as every row of a
    worksheet, for pages that need a lot of data at once (the Overview
    page needs all six health metric worksheets on every request).

    Each source has a name and a function that reads it, normally a
    service method, so the cache never talks to Google Sheets itself:

        DataCache(loaders={"sleep": sleep_metrics_service.get_sleep_metrics})

    A source is read again when it is older than CACHE_DURATION, after
    mark_stale(), or on refresh(). Only pages that read through the
    cache use it; the log pages always read the Sheet, because they are
    used for editing and must show what is actually stored.
    """

    def __init__(
        self,
        loaders: dict[str, Callable[[], list]],
        now: Callable[[], datetime] = datetime.now,
    ):
        """
        The clock is passed in, so tests can move time forward.
        """

        self._loaders = loaders
        self._now = now

        # source -> (time it was read, rows)
        self._cache: dict[str, tuple[datetime, list]] = {}
        self._stale: set[str] = set()

        # One read at a time: a request that arrives while the cache is
        # loading waits for that load instead of starting another.
        self._lock = threading.Lock()


    def get(self, source: str) -> list:
        """
        Return a source's rows from the cache, reading it only if it is
        missing, stale or older than CACHE_DURATION.
        """

        self._check_source(source)

        with self._lock:
            entry = self._cache.get(source)

            # Why the source must be read again, if it must.
            if entry is None:
                reason = "not loaded yet"
            elif source in self._stale:
                reason = "marked stale by a save"
            elif self._now() - entry[0] >= CACHE_DURATION:
                reason = "older than 12h"
            else:
                reason = None

            if reason is not None:
                entry = self._load(source, reason)

            return entry[1]


    def mark_stale(self, source: str) -> None:
        """
        Mark one source as out of date after a save. It is read again
        the next time it is needed, not now, so a long import does not
        read the Sheet after every save.
        """

        self._check_source(source)

        with self._lock:
            self._stale.add(source)


    def refresh(self) -> None:
        """
        Read every source again, even if cached (the Refresh button).
        """

        count = len(self._loaders)

        print(f"Data cache: refreshing all {count} sources...")

        seconds = self._load_every_source("refresh")

        print(f"Data cache: refreshed all {count} sources in {seconds:.1f}s")


    def load_all(self) -> None:
        """
        Fill the cache with every source.

        Called in the background when the backend starts. A failure is
        printed, not raised, so the backend keeps running; the next
        request tries again.
        """

        count = len(self._loaders)

        print(f"Data cache: loading all {count} sources at startup...")

        try:
            seconds = self._load_every_source("startup")

        except Exception as error:
            print(
                "Data cache: could not load at startup; it will load "
                f"on the next request. ({error})"
            )
            return

        print(
            f"Data cache: loaded all {count} sources in {seconds:.1f}s "
            "(startup)"
        )


    def _load_every_source(self, reason: str) -> float:
        """
        Read every source, holding the lock throughout so requests wait
        for the whole load. Returns how long it took, in seconds.
        """

        started = time.monotonic()

        with self._lock:
            for source in self._loaders:
                self._load(source, reason)

        return time.monotonic() - started


    def status(self) -> dict[str, CacheSourceStatus]:
        """
        Report each source's state: whether it is loaded, how many
        rows, when it was read, when it expires, and whether it is
        stale. Used to check that the cache is working.
        """

        with self._lock:
            report = {}

            for source in self._loaders:
                entry = self._cache.get(source)

                if entry is None:
                    report[source] = CacheSourceStatus(
                        loaded=False,
                        stale=source in self._stale,
                    )
                    continue

                read_at, rows = entry

                report[source] = CacheSourceStatus(
                    loaded=True,
                    rows=len(rows),
                    read_at=read_at,
                    expires_at=read_at + CACHE_DURATION,
                    stale=source in self._stale,
                )

            return report


    def _check_source(self, source: str) -> None:
        """
        Reject unknown source names, so a typo is an error instead of a
        source that is silently never refreshed.
        """

        if source not in self._loaders:
            raise ValueError(f"Unknown data cache source: {source}")


    def _load(self, source: str, reason: str) -> tuple[datetime, list]:
        """
        Read one source into the cache. The caller holds the lock.

        Prints a line for every read, with the reason, so the backend's
        terminal shows when and why the Sheet is actually read (startup,
        refresh, marked stale by a save, older than 12h, not loaded
        yet). Using the cache prints nothing.
        """

        started = time.monotonic()

        rows = self._loaders[source]()

        print(
            f"Data cache: read {source} ({len(rows)} rows) "
            f"in {time.monotonic() - started:.1f}s ({reason})"
        )

        entry = (self._now(), rows)

        self._cache[source] = entry
        self._stale.discard(source)

        return entry
