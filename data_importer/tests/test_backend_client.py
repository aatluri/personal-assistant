from unittest.mock import Mock, patch

from app.clients.backend_client import BackendClient


@patch("app.clients.backend_client.httpx.put")
def test_update_health_metrics(mock_put):

    # Create the response that we want the mocked backend
    # request to return.
    mock_response = Mock()
    mock_response.json.return_value = {
        "date": "2026-10-12",
        "step_count": 4042,
        "source": "Health Auto Export",
    }

    mock_put.return_value = mock_response

    payload = {
        "date": "2026-10-12",
        "step_count": 4042,
        "source": "Health Auto Export",
    }

    client = BackendClient()

    result = client.update_health_metrics(payload)

    # Verify that the Data Importer called the correct backend endpoint
    # with the correct payload.
    mock_put.assert_called_once_with(
        f"{client.base_url}/health/health-metrics",
        json=payload,
        timeout=10.0,
    )

    # Verify that HTTP errors are checked.
    mock_response.raise_for_status.assert_called_once()

    # Verify that the backend response is returned to the caller.
    assert result == {
        "date": "2026-10-12",
        "step_count": 4042,
        "source": "Health Auto Export",
    }