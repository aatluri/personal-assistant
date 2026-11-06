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

    HEALTH_BODY_MEASUREMENTS_WORKSHEET: str

    LAB_REPORTS_WORKSHEET: str

    LAB_MARKER_DEFINITIONS_WORKSHEET: str

    LAB_MARKER_REFERENCE_RANGES_WORKSHEET: str

    LAB_MARKER_INTERPRETATIONS_WORKSHEET: str

    LAB_RESULTS_WORKSHEET: str

    HEALTH_WORKOUT_METRICS_WORKSHEET: str

    HEALTH_SLEEP_METRICS_WORKSHEET: str
    HEALTH_HEALTH_METRICS_WORKSHEET: str
    HEALTH_NUTRITION_METRICS_WORKSHEET: str
    HEALTH_HEART_RATE_NOTIFICATIONS_WORKSHEET: str

    OPENAI_API_KEY: str

    # Browser origins allowed to call the API (CORS): the frontend's
    # address. Optional; to change it, set a JSON list in .env, e.g.
    # CORS_ALLOWED_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]
    CORS_ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    # Print a line for every request to Google Sheets, e.g.
    # "Google Sheets: read Sleep_Metrics in 0.6s". Optional; set
    # LOG_GOOGLE_SHEETS_REQUESTS=false in .env before a long import,
    # which makes thousands of requests.
    LOG_GOOGLE_SHEETS_REQUESTS: bool = True

    model_config = SettingsConfigDict(

        env_file=".env",

        env_file_encoding="utf-8",

    )

settings = Settings()