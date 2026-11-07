"""
When an imported file is marked as processed.

Health Auto Export rewrites the files for today and yesterday on every
export, updating the same file in Google Drive. So data added late, such
as nutrition logged the next day or a second export the same evening,
ends up in a file that was already imported.

Such a file keeps its plain name after a successful import, so every run
imports it again. Once it is REIMPORT_DAYS days old it can no longer
change: it is imported one last time and renamed PROCESSED_.

Importing a file again is safe: the backend updates or creates each
record by its date (or a workout's or notification's start time), so
nothing is duplicated, and a blank value never overwrites a stored one.
"""

from datetime import date, timedelta

from app.modules.health.constants import PROCESSED_PREFIX, REIMPORT_DAYS


def today() -> date:
    """
    Today's local date. A function of its own, so tests can fix it.
    """

    return date.today()


def is_still_updating(file_date: date) -> bool:
    """
    True for files Health Auto Export may still update: today's and
    yesterday's. Anything else, older or dated in the future (such as the
    2099 fixtures used by the live tests), cannot change and is marked as
    processed after its import.
    """

    current = today()

    return current - timedelta(days=REIMPORT_DAYS) < file_date <= current


def name_after_import(original_name: str, file_date: date) -> str:
    """
    The name a file gets after a successful import: its plain name while
    it may still be updated (so the next run imports it again), and
    PROCESSED_<name> once it can no longer change.

    original_name is the file's name without any FAILED_ prefix.
    """

    if is_still_updating(file_date):
        return original_name

    return f"{PROCESSED_PREFIX}{original_name}"
