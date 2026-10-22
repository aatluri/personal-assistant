from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from the .env file.
    """

    PERSONAL_ASSISTANT_API_URL: str
    GOOGLE_SERVICE_ACCOUNT_FILE: str
    HEALTH_METRICS_DRIVE_FOLDER_ID: str
    HEALTH_METRICS_PROCESSED_DRIVE_FOLDER_ID: str
    WORKOUT_METRICS_DRIVE_FOLDER_ID: str
    WORKOUT_METRICS_PROCESSED_DRIVE_FOLDER_ID: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()