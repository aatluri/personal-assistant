from datetime import date
from unittest.mock import patch

from app.modules.health.orchestrators.file_lifecycle import (
    is_still_updating,
    name_after_import,
)


"""
File Lifecycle Tests

Today is fixed to Saturday, November 7, 2026, so "today" and
"yesterday" are Nov 7 and Nov 6.
"""


TODAY = "app.modules.health.orchestrators.file_lifecycle.today"


# Verify that today's and yesterday's files may still be updated, and
# older or future-dated ones (such as the live tests' 2099 fixtures)
# cannot.
def test_is_still_updating_for_today_and_yesterday_only():

    with patch(TODAY, return_value=date(2026, 11, 7)):
        assert is_still_updating(date(2026, 11, 7)) is True
        assert is_still_updating(date(2026, 11, 6)) is True
        assert is_still_updating(date(2026, 11, 5)) is False
        assert is_still_updating(date(2022, 1, 1)) is False
        assert is_still_updating(date(2026, 11, 8)) is False
        assert is_still_updating(date(2099, 2, 1)) is False


# Verify that a file that may still be updated keeps its plain name, and
# an older one is marked as processed.
def test_name_after_import():

    with patch(TODAY, return_value=date(2026, 11, 7)):
        assert name_after_import(
            "HealthMetrics-2026-11-06.json", date(2026, 11, 6)
        ) == "HealthMetrics-2026-11-06.json"

        assert name_after_import(
            "HealthMetrics-2026-11-05.json", date(2026, 11, 5)
        ) == "PROCESSED_HealthMetrics-2026-11-05.json"
