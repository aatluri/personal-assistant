from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from the .env file.
    """

    # Base URL of the Personal Assistant backend API.
    PERSONAL_ASSISTANT_API_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# Single settings instance that can be imported throughout the application.
settings = Settings()