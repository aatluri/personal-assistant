from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    """

    Application configuration.

    Values are loaded from the .env file.

.env
   │
   ▼
app/config.py
   │
   ▼
settings
   │
   ├──────────────► sheets_client.py
   │
   ├──────────────► repositories
   │
   ├──────────────► services
   │
   └──────────────► future modules

    """

    GOOGLE_SERVICE_ACCOUNT_FILE: str

    GOOGLE_SHEETS_SPREADSHEET_ID: str

    HEALTH_DAILY_LOG_WORKSHEET: str

    HEALTH_BODY_MEASUREMENTS_WORKSHEET: str

    LAB_REPORTS_WORKSHEET: str

    LAB_MARKER_DEFINITIONS_WORKSHEET: str

    LAB_MARKER_REFERENCE_RANGES_WORKSHEET: str

    LAB_MARKER_INTERPRETATIONS_WORKSHEET: str

    LAB_RESULTS_WORKSHEET: str

    model_config = SettingsConfigDict(

        env_file=".env",

        env_file_encoding="utf-8",

    )

settings = Settings()