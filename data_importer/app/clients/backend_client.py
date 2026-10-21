import httpx

from app.config import settings


class BackendClient:
    """
    HTTP client for communicating with the Personal Assistant backend.
    """

    def __init__(self):
        self.base_url = settings.PERSONAL_ASSISTANT_API_URL.rstrip("/")


    def update_health_metrics(self, payload: dict) -> dict:
        """
        Send a Health Metrics record to the Personal Assistant backend.

        The backend is responsible for persisting the record.
        The Data Importer does not interact with Google Sheets directly.
        """

        url = f"{self.base_url}/health/health-metrics"

        response = httpx.put(
            url,
            json=payload,
            timeout=10.0,
        )

        if response.status_code != 200:
            print("Payload sent:", payload)
            print("Backend response:", response.text)


        # Raise an exception if the backend returns an unsuccessful
        # HTTP status code.
        response.raise_for_status()

        return response.json()

    def update_nutrition_metrics(self, payload: dict) -> dict:
        """
        Send a Nutrition Metrics record to the Personal Assistant backend.

        The backend is responsible for persisting the record.
        The Data Importer does not interact with Google Sheets directly.
        """

        url = f"{self.base_url}/health/nutrition-metrics"

        response = httpx.put(
            url,
            json=payload,
            timeout=10.0,
        )

        if response.status_code != 200:
            print("Payload sent:", payload)
            print("Backend response:", response.text)

        # Raise an exception if the backend returns an unsuccessful
        # HTTP status code.
        response.raise_for_status()

        return response.json()


    def update_sleep_metrics(self, payload: dict) -> dict:
        """
        Send a Sleep Metrics record to the Personal Assistant backend.

        The backend is responsible for persisting the record.
        The Data Importer does not interact with Google Sheets directly.
        """
        url = f"{self.base_url}/health/sleep-metrics"

        response = httpx.put(
            url,
            json=payload,
            timeout=10.0,
        )

        if response.status_code != 200:
            print("Payload sent:", payload)
            print("Backend response:", response.text)

        response.raise_for_status()

        return response.json()