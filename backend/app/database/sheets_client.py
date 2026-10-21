from functools import lru_cache

from google.oauth2.service_account import Credentials

import gspread

from app.config import settings


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


@lru_cache(maxsize=1)
def get_sheets_client() -> gspread.Client:
    """
    Create and return a shared authenticated Google Sheets client.

    The client is created once per application process and reused
    for subsequent Google Sheets operations.
    """

    credentials = Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    return gspread.authorize(credentials)


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