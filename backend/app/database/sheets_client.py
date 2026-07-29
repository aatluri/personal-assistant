from google.oauth2.service_account import Credentials
from app.config import settings

import gspread


# Google Sheets API scope

SCOPES = [

    "https://www.googleapis.com/auth/spreadsheets"

]

def get_sheets_client() -> gspread.Client:

    """

    Creates and returns an authenticated Google Sheets client.

    Returns:

        gspread.Client: Authenticated Google Sheets client.

    """

    credentials = Credentials.from_service_account_file(

    settings.GOOGLE_SERVICE_ACCOUNT_FILE,

    scopes=SCOPES,

)
    return gspread.authorize(credentials)