from app.database.sheets_client import get_sheets_client
from app.config import settings


client = get_sheets_client()

spreadsheet = client.open_by_key(
    settings.GOOGLE_SHEETS_SPREADSHEET_ID
)

print(f"Connected to: {spreadsheet.title}")

for sheet in spreadsheet.worksheets():

    print(sheet.title)


