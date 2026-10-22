import json
from pathlib import Path
from unittest.mock import Mock

from app.modules.health.importers.health_metrics_importer import (
    build_health_metrics_payload,
    import_health_metrics,
)


def load_test_health_json() -> dict:

    fixture_path = (
        Path(__file__).parent.parent
        / "test_data"
        / "HealthMetrics-2026-10-12.json"
    )

    assert fixture_path.exists(), f"Test JSON not found: {fixture_path}"

    with fixture_path.open(encoding="utf-8") as file:
        return json.load(file)


def test_build_health_metrics_payload():

    export_data = load_test_health_json()

    payload = build_health_metrics_payload(export_data)

    assert payload is not None

    # Verify the record-level fields.
    assert payload["date"] == "2026-10-12"
    assert payload["source"] == "Health Auto Export"

    # Verify the exact Health Metrics extracted from
    # the real Health Auto Export file.
    assert payload["step_count"] == 4042
    assert payload["active_energy_kcal"] == 302
    assert payload["resting_energy_kcal"] == 1845

    assert payload["blood_oxygen_saturation_percent"] == 96

    assert payload["heart_rate_min_bpm"] == 37
    assert payload["heart_rate_max_bpm"] == 107
    assert payload["heart_rate_variability_ms"] == 75

    assert payload["physical_effort_kcal_hr_kg"] == 3
    assert payload["respiratory_rate_bpm"] == 17
    assert payload["resting_heart_rate_bpm"] == 43

    # These mapped Health Metrics are not present
    # in this particular export.
    assert payload["atrial_fibrillation_burden_percent"] is None
    assert payload["breathing_disturbances_count"] is None
    assert payload["cardio_recovery_bpm"] is None
    assert payload["flights_climbed"] is None

def test_build_health_metrics_payload_with_no_health_metrics():

    export_data = {
        "data": {
            "metrics": []
        }
    }

    payload = build_health_metrics_payload(export_data)

    assert payload is None


def test_import_health_metrics():

    export_data = load_test_health_json()

    backend_client = Mock()

    backend_client.update_health_metrics.return_value = {
        "date": "2026-10-12",
        "step_count": 4042,
        "source": "Health Auto Export",
    }

    result = import_health_metrics(
        export_data,
        backend_client,
    )

    # One Health Metrics record should have been sent to the backend.
    backend_client.update_health_metrics.assert_called_once()

    payload_sent = (
        backend_client
        .update_health_metrics
        .call_args
        .args[0]
    )

    # Verify important fields sent to the backend.
    assert payload_sent["date"] == "2026-10-12"
    assert payload_sent["step_count"] == 4042
    assert payload_sent["heart_rate_min_bpm"] == 37
    assert payload_sent["heart_rate_max_bpm"] == 107
    assert payload_sent["source"] == "Health Auto Export"

    # Verify that the importer returns the backend response.
    assert result == {
        "date": "2026-10-12",
        "step_count": 4042,
        "source": "Health Auto Export",
    }


def test_import_health_metrics_with_no_health_metrics():

    export_data = {
        "data": {
            "metrics": []
        }
    }

    backend_client = Mock()

    result = import_health_metrics(
        export_data,
        backend_client,
    )

    # No backend request should be made when there is
    # no Health Metrics data.
    backend_client.update_health_metrics.assert_not_called()

    assert result is None