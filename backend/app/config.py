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

    model_config = SettingsConfigDict(

        env_file=".env",

        env_file_encoding="utf-8",

    )

settings = Settings()