import json
from pathlib import Path
from unittest.mock import Mock

from app.modules.health.importers.workout_metrics_importer import (
    build_workout_metrics_payloads,
    import_workout_metrics,
)


def load_test_workout_json() -> dict:

    json_path = (
        Path(__file__).parent.parent
        / "test_data"
        / "WorkoutMetrics-2026-07-02.json"
    )

    assert json_path.exists(), f"Test JSON not found: {json_path}"

    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)


def test_build_workout_metrics_payloads():

    export_data = load_test_workout_json()

    payloads = build_workout_metrics_payloads(export_data)

    # The test file contains two workouts.
    assert len(payloads) == 2

    hiit = payloads[0]
    outdoor_run = payloads[1]

    # Validate the HIIT workout.
    assert hiit["date"] == "2026-07-02"
    assert hiit["workout_type"] == "High Intensity Interval Training"
    assert hiit["workout_start_time"] == "2026-07-02T16:35:58+05:30"
    assert hiit["workout_end_time"] == "2026-07-02T17:17:11+05:30"
    assert hiit["workout_duration"] == "0:41:13"
    assert hiit["total_energy_kcal"] == 470.24
    assert hiit["active_energy_kcal"] == 394.33
    assert hiit["max_heart_rate_bpm"] == 165
    assert hiit["avg_heart_rate_bpm"] == 137.25
    assert hiit["distance_km"] is None
    assert hiit["avg_speed_mph"] is None

    # Validate the Outdoor Run.
    assert outdoor_run["date"] == "2026-07-02"
    assert outdoor_run["workout_type"] == "Outdoor Run"
    assert outdoor_run["workout_start_time"] == "2026-07-02T15:40:44+05:30"
    assert outdoor_run["workout_end_time"] == "2026-07-02T16:14:24+05:30"
    assert outdoor_run["workout_duration"] == "0:33:40"
    assert outdoor_run["total_energy_kcal"] == 425.44
    assert outdoor_run["active_energy_kcal"] == 365.25
    assert outdoor_run["max_heart_rate_bpm"] == 170
    assert outdoor_run["avg_heart_rate_bpm"] == 153.77
    assert outdoor_run["distance_km"] == 3.14
    assert outdoor_run["avg_speed_mph"] == 5.59


def test_build_workout_metrics_payloads_with_no_workouts():

    export_data = {
        "data": {
            "workouts": []
        }
    }

    payloads = build_workout_metrics_payloads(export_data)

    assert payloads == []


def test_import_workout_metrics():

    export_data = load_test_workout_json()

    backend_client = Mock()

    backend_client.update_workout_metrics.side_effect = [
        {"status": "updated", "workout": "HIIT"},
        {"status": "updated", "workout": "Outdoor Run"},
    ]

    results = import_workout_metrics(
        export_data,
        backend_client,
    )

    # Both workouts should have been sent to the backend.
    assert backend_client.update_workout_metrics.call_count == 2

    # Validate the first payload sent to the backend.
    first_payload = (
        backend_client
        .update_workout_metrics
        .call_args_list[0]
        .args[0]
    )

    assert first_payload["workout_type"] == "High Intensity Interval Training"
    assert first_payload["workout_start_time"] == "2026-07-02T16:35:58+05:30"

    # Validate the second payload sent to the backend.
    second_payload = (
        backend_client
        .update_workout_metrics
        .call_args_list[1]
        .args[0]
    )

    assert second_payload["workout_type"] == "Outdoor Run"
    assert second_payload["workout_start_time"] == "2026-07-02T15:40:44+05:30"
    assert second_payload["distance_mi"] == 3.14
    assert second_payload["avg_speed_mph"] == 5.59

    # Verify that the importer returns the backend responses.
    assert results == [
        {"status": "updated", "workout": "HIIT"},
        {"status": "updated", "workout": "Outdoor Run"},
    ]


def test_import_workout_metrics_with_no_workouts():

    export_data = {
        "data": {
            "workouts": []
        }
    }

    backend_client = Mock()

    results = import_workout_metrics(
        export_data,
        backend_client,
    )

    # No backend request should be made when there are no workouts.
    backend_client.update_workout_metrics.assert_not_called()

    assert results == []