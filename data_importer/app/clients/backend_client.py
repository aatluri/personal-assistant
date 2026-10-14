import httpx

from app.config import settings


class BackendClient:
    """
    HTTP client for communicating with the Personal Assistant backend.
    """

    def __init__(self):
        self.base_url = settings.PERSONAL_ASSISTANT_API_URL.rstrip("/")

    def get_health_metrics(self, metric_date: str) -> dict | None:
        """
        Retrieve Health Metrics for a specific date.

        Returns the Health Metrics record if one exists.
        Returns None if no record exists for that date.
        """

        url = f"{self.base_url}/health/health-metrics/{metric_date}"

        response = httpx.get(
            url,
            timeout=10.0,
        )

        # The backend uses 404 when no Health Metrics record exists.
        if response.status_code == 404:
            return None

        # Raise an exception for unexpected HTTP errors.
        response.raise_for_status()

        return response.json()


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