import time
from functools import lru_cache
from http import HTTPStatus

from google.oauth2.service_account import Credentials

import gspread
from gspread.exceptions import APIError
from gspread.http_client import HTTPClient

from app.config import settings


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

# Seconds to wait before each retry when Google Sheets rejects a request
# because of its per-minute rate limit (or a temporary server error).
# About 75 seconds in total, enough for the per-minute quota to reset.
RETRY_WAIT_SECONDS = [5, 10, 20, 40]


class RetryingHTTPClient(HTTPClient):
    """
    gspread HTTP client that waits and retries when Google Sheets is
    temporarily unavailable, instead of failing straight away.

    Google Sheets allows a limited number of requests per minute. Bulk
    work, such as importing many records at once, can exceed it, and the
    API then answers 429 (Too Many Requests). This client prints a
    message, waits, and tries again. If every retry fails, the original
    error is raised as before.
    """

    def request(self, *args, **kwargs):

        for attempt, wait_seconds in enumerate(RETRY_WAIT_SECONDS, start=1):

            try:
                return super().request(*args, **kwargs)

            except APIError as error:

                is_rate_limited = error.code == HTTPStatus.TOO_MANY_REQUESTS
                is_server_error = error.code >= HTTPStatus.INTERNAL_SERVER_ERROR

                if not (is_rate_limited or is_server_error):
                    raise

                reason = (
                    "Google Sheets rate limit reached"
                    if is_rate_limited
                    else f"Google Sheets temporary error ({error.code})"
                )

                print(
                    f"{reason}; waiting {wait_seconds}s before retrying "
                    f"(attempt {attempt} of {len(RETRY_WAIT_SECONDS)})...",
                    flush=True,
                )

                time.sleep(wait_seconds)

        # Final attempt: any error now propagates to the caller.
        return super().request(*args, **kwargs)


@lru_cache(maxsize=1)
def get_sheets_client() -> gspread.Client:
    """
    Create and return a shared authenticated Google Sheets client.

    The client is created once per application process and reused
    for subsequent Google Sheets operations. It uses RetryingHTTPClient,
    so rate-limited requests wait and retry instead of failing.
    """

    credentials = Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    return gspread.authorize(
        credentials,
        http_client=RetryingHTTPClient,
    )


@lru_cache(maxsize=1)
def get_spreadsheet() -> gspread.Spreadsheet:
    """
    Open and return the application's Google Spreadsheet.

    The spreadsheet is opened once per application process and
    reused by all repositories.
    """

    client = get_sheets_client()

    return client.open_by_key(
        settings.GOOGLE_SHEETS_SPREADSHEET_ID
    )