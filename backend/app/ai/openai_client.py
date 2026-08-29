from openai import OpenAI

from app.config import settings


def get_openai_client() -> OpenAI:
    """
    Create an authenticated OpenAI API client.
    """

    return OpenAI(
        api_key=settings.OPENAI_API_KEY,
    )