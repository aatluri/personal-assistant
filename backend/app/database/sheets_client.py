import time
from functools import lru_cache
from http import HTTPStatus
from urllib.parse import unquote

from google.oauth2.service_account import Credentials

import gspread
from gspread.exceptions import APIError
from gspread.http_client import HTTPClient
from gspread.urls import SPREADSHEETS_API_V4_BASE_URL

from app.config import settings


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

# Seconds to wait before each retry when Google Sheets rejects a request
# because of its per-minute rate limit (or a temporary server error).
# About 75 seconds in total, enough for the per-minute quota to reset.
RETRY_WAIT_SECONDS = [5, 10, 20, 40]


def describe_request(method: str, endpoint: str) -> str:
    """
    Describe a Google Sheets request in a few words for the log, e.g.
    "read Sleep_Metrics" or "write Workout_Metrics". The spreadsheet ID
    and cell ranges are left out.

    gspread's URLs look like (see gspread/urls.py):
        .../spreadsheets/<id>                     spreadsheet details
        .../spreadsheets/<id>:batchUpdate         structure, e.g. deleting rows
        .../spreadsheets/<id>/values/<range>      one range (":append" or
                                                  ":clear" may follow)
        .../spreadsheets/<id>/values:batchGet     several ranges
    The range is URL-encoded, e.g. 'Sleep_Metrics'!A3:J3 becomes
    %27Sleep_Metrics%27%21A3%3AJ3, so a literal ":" only ever starts a
    suffix such as ":append".
    """

    action = "read" if method.lower() == "get" else "write"
    prefix = SPREADSHEETS_API_V4_BASE_URL + "/"

    if not endpoint.startswith(prefix):
        return f"{method.upper()} {endpoint.split('?')[0]}"

    path = endpoint[len(prefix):].split("?")[0]
    spreadsheet, _, rest = path.partition("/")

    if rest.startswith("values/"):
        encoded_range = rest[len("values/"):].split(":")[0]
        worksheet = unquote(encoded_range).split("!")[0].strip("'")
        return f"{action} {worksheet}"

    if rest.startswith("values:"):
        return f"{action} several ranges"

    if spreadsheet.endswith(":batchUpdate"):
        return "change the spreadsheet structure"

    return f"{action} spreadsheet details"


class RetryingHTTPClient(HTTPClient):
    """
    gspread HTTP client that waits and retries when Google Sheets is
    temporarily unavailable, instead of failing straight away, and logs
    every request.

    Google Sheets allows a limited number of requests per minute. Bulk
    work, such as importing many records at once, can exceed it, and the
    API then answers 429 (Too Many Requests). This client prints a
    message, waits, and tries again. If every retry fails, the original
    error is raised as before.

    Every repository, the data cache and the labs code use this client,
    so logging here shows every time the backend actually calls Google
    Sheets (unless LOG_GOOGLE_SHEETS_REQUESTS is turned off).
    """

    def request(self, method, endpoint, *args, **kwargs):

        started = time.monotonic()

        response = self._request_with_retries(
            method, endpoint, *args, **kwargs
        )

        if settings.LOG_GOOGLE_SHEETS_REQUESTS:
            print(
                f"Google Sheets: {describe_request(method, endpoint)} "
                f"in {time.monotonic() - started:.1f}s",
                flush=True,
            )

        return response


    def _request_with_retries(self, *args, **kwargs):

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