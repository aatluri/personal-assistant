from unittest.mock import Mock, call, patch

import pytest
from gspread.exceptions import APIError

from app.database.sheets_client import (
    RETRY_WAIT_SECONDS,
    RetryingHTTPClient,
)


"""
RetryingHTTPClient Tests

gspread's real request and time.sleep are replaced with mocks, so these
tests never contact Google and never actually wait.
"""


BASE_REQUEST = "gspread.http_client.HTTPClient.request"
SLEEP = "app.database.sheets_client.time.sleep"


def api_error(code: int) -> APIError:
    """
    Build the APIError gspread raises for a Google API error response.
    """

    response = Mock()
    response.json.return_value = {
        "error": {
            "code": code,
            "message": "test error",
            "status": "TEST",
        }
    }

    return APIError(response)


def make_client() -> RetryingHTTPClient:
    """
    Create the client without real credentials; only request() is tested.
    """

    return RetryingHTTPClient.__new__(RetryingHTTPClient)


# Verify that a successful request is returned straight away.
def test_request_succeeds_without_waiting(capsys):

    with patch(BASE_REQUEST, return_value="response") as base_request, \
         patch(SLEEP) as sleep:

        result = make_client().request("get", "https://example.test")

    assert result == "response"
    base_request.assert_called_once()
    sleep.assert_not_called()
    assert capsys.readouterr().out == ""


# Verify that a rate-limited request prints a message, waits and retries.
def test_rate_limited_request_waits_and_retries(capsys):

    with patch(
        BASE_REQUEST,
        side_effect=[api_error(429), "response"],
    ) as base_request, patch(SLEEP) as sleep:

        result = make_client().request("get", "https://example.test")

    assert result == "response"
    assert base_request.call_count == 2
    sleep.assert_called_once_with(RETRY_WAIT_SECONDS[0])

    assert capsys.readouterr().out == (
        "Google Sheets rate limit reached; waiting 5s before retrying "
        "(attempt 1 of 4)...\n"
    )


# Verify that a temporary Google server error is also retried.
def test_server_error_waits_and_retries(capsys):

    with patch(
        BASE_REQUEST,
        side_effect=[api_error(503), "response"],
    ), patch(SLEEP):

        result = make_client().request("get", "https://example.test")

    assert result == "response"
    assert "Google Sheets temporary error (503)" in capsys.readouterr().out


# Verify that other errors (e.g. not found) are raised without waiting.
def test_other_errors_are_raised_immediately():

    with patch(
        BASE_REQUEST,
        side_effect=api_error(404),
    ) as base_request, patch(SLEEP) as sleep:

        with pytest.raises(APIError):
            make_client().request("get", "https://example.test")

    base_request.assert_called_once()
    sleep.assert_not_called()


# Verify that the error is raised once every retry has failed.
def test_raises_after_all_retries_fail(capsys):

    with patch(
        BASE_REQUEST,
        side_effect=api_error(429),
    ) as base_request, patch(SLEEP) as sleep:

        with pytest.raises(APIError):
            make_client().request("get", "https://example.test")

    # One try per wait, plus the final attempt.
    assert base_request.call_count == len(RETRY_WAIT_SECONDS) + 1

    assert sleep.call_args_list == [
        call(seconds) for seconds in RETRY_WAIT_SECONDS
    ]

    output = capsys.readouterr().out

    for attempt, seconds in enumerate(RETRY_WAIT_SECONDS, start=1):
        assert (
            f"waiting {seconds}s before retrying "
            f"(attempt {attempt} of {len(RETRY_WAIT_SECONDS)})"
        ) in output
