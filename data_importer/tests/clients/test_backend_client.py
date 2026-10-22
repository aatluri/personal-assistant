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

@patch("app.clients.backend_client.httpx.put")
def test_update_nutrition_metrics(mock_put):

    # Create the response that we want the mocked backend
    # request to return.
    mock_response = Mock()
    mock_response.json.return_value = {
        "date": "2026-10-12",
        "dietary_energy_kcal": 1750.5,
        "protein_g": 112.4,
        "carbohydrates_g": 180.2,
        "fiber_g": 28.5,
        "sugar_g": 32.1,
        "total_fat_g": 62.3,
        "saturated_fat_g": 18.4,
        "polyunsaturated_fat_g": 10.2,
        "monounsaturated_fat_g": 22.6,
        "water_fl_oz_us": 101.4,
        "cholesterol_mg": 210.0,
        "source": "Health Auto Export",
    }

    mock_put.return_value = mock_response

    payload = {
        "date": "2026-10-12",
        "dietary_energy_kcal": 1750.5,
        "protein_g": 112.4,
        "carbohydrates_g": 180.2,
        "fiber_g": 28.5,
        "sugar_g": 32.1,
        "total_fat_g": 62.3,
        "saturated_fat_g": 18.4,
        "polyunsaturated_fat_g": 10.2,
        "monounsaturated_fat_g": 22.6,
        "water_fl_oz_us": 101.4,
        "cholesterol_mg": 210.0,
        "source": "Health Auto Export",
    }

    client = BackendClient()

    result = client.update_nutrition_metrics(payload)

    # Verify that the Data Importer called the correct backend endpoint
    # with the correct payload.
    mock_put.assert_called_once_with(
        f"{client.base_url}/health/nutrition-metrics",
        json=payload,
        timeout=10.0,
    )

    # Verify that HTTP errors are checked.
    mock_response.raise_for_status.assert_called_once()

    # Verify that the backend response is returned to the caller.
    assert result == mock_response.json.return_value


@patch("app.clients.backend_client.httpx.put")
def test_update_sleep_metrics(mock_put):

    # Create the response that we want the mocked backend
    # request to return.
    mock_response = Mock()
    mock_response.json.return_value = {
        "date": "2026-10-12",
        "sleep_start_time": "2026-10-11T23:30:00+05:30",
        "sleep_end_time": "2026-10-12T07:00:00+05:30",
        "total_sleep_duration_hr": 7.5,
        "core_sleep_hr": 4.2,
        "rem_sleep_hr": 1.6,
        "deep_sleep_hr": 1.2,
        "awake_hr": 0.5,
        "source": "Health Auto Export",
    }

    mock_put.return_value = mock_response

    payload = {
        "date": "2026-10-12",
        "sleep_start_time": "2026-10-11T23:30:00+05:30",
        "sleep_end_time": "2026-10-12T07:00:00+05:30",
        "total_sleep_duration_hr": 7.5,
        "core_sleep_hr": 4.2,
        "rem_sleep_hr": 1.6,
        "deep_sleep_hr": 1.2,
        "awake_hr": 0.5,
        "source": "Health Auto Export",
    }

    client = BackendClient()

    result = client.update_sleep_metrics(payload)

    # Verify that the Data Importer called the correct backend endpoint
    # with the correct payload.
    mock_put.assert_called_once_with(
        f"{client.base_url}/health/sleep-metrics",
        json=payload,
        timeout=10.0,
    )

    # Verify that HTTP errors are checked.
    mock_response.raise_for_status.assert_called_once()

    # Verify that the backend response is returned to the caller.
    assert result == mock_response.json.return_value

@patch("app.clients.backend_client.httpx.put")
def test_update_workout_metrics(mock_put):

    # Create the response that we want the mocked backend
    # request to return.
    mock_response = Mock()
    mock_response.json.return_value = {
        "date": "2026-07-02",
        "workout_type": "Outdoor Run",
        "workout_start_time": "2026-07-02T15:40:44+05:30",
        "workout_end_time": "2026-07-02T16:14:24+05:30",
        "workout_duration": "0:33:40",
        "total_energy_kcal": 425.44,
        "active_energy_kcal": 365.25,
        "max_heart_rate_bpm": 170,
        "avg_heart_rate_bpm": 153.77,
        "distance_mi": 3.14,
        "avg_speed_mph": 5.59,
    }

    mock_put.return_value = mock_response

    payload = {
        "date": "2026-07-02",
        "workout_type": "Outdoor Run",
        "workout_start_time": "2026-07-02T15:40:44+05:30",
        "workout_end_time": "2026-07-02T16:14:24+05:30",
        "workout_duration": "0:33:40",
        "total_energy_kcal": 425.44,
        "active_energy_kcal": 365.25,
        "max_heart_rate_bpm": 170,
        "avg_heart_rate_bpm": 153.77,
        "distance_mi": 3.14,
        "avg_speed_mph": 5.59,
    }

    client = BackendClient()

    result = client.update_workout_metrics(payload)

    # Verify that the Data Importer called the correct backend endpoint
    # with the correct payload.
    mock_put.assert_called_once_with(
        f"{client.base_url}/health/workout-metrics",
        json=payload,
        timeout=10.0,
    )

    # Verify that HTTP errors are checked.
    mock_response.raise_for_status.assert_called_once()

    # Verify that the backend response is returned to the caller.
    assert result == mock_response.json.return_value