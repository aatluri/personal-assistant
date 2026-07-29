from google.oauth2.service_account import Credentials
import gspread

# Path to the service account credentials
SERVICE_ACCOUNT_FILE = "backend/credentials/service_account.json"

# Google Sheets API scope
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# Authenticate
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES,
)

client = gspread.authorize(credentials)

# Open the spreadsheet by name
spreadsheet = client.open_by_key(

    "1yAf4kP1GoH8jwfsAyTkiRrrDk8fajNyl3dc_rUmAN9E"

)


print(f"Connected successfully!")
print(f"Spreadsheet Title: {spreadsheet.title}")

print("\nWorksheets:")

for worksheet in spreadsheet.worksheets():
    print(f"- {worksheet.title}")