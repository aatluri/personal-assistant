import json
from pathlib import Path
from unittest.mock import Mock

from app.modules.health.importers.body_measurements_metrics_importer import (
    build_body_measurements_metrics_payload,
    import_body_measurements_metrics,
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


def test_build_body_measurements_metrics_payload():

    export_data = load_test_health_json()

    payload = build_body_measurements_metrics_payload(export_data)

    assert payload is not None

    # Verify the record-level fields.
    assert payload["date"] == "2026-10-12"
    assert payload["source"] == "Health Auto Export"

    # Verify the exact Body Measurements extracted from
    # the real Health Auto Export file.
    assert payload["weight_kg"] == 177.5647316252014 * 0.45359237
    assert payload["body_mass_index"] == 27.224851608276367
    assert payload["body_fat_percent"] == 26.147844314575195


def test_build_body_measurements_metrics_payload_with_no_body_measurements_data():

    export_data = {
        "data": {
            "metrics": []
        }
    }

    payload = build_body_measurements_metrics_payload(export_data)

    assert payload is None


def test_import_body_measurements_metrics():

    export_data = load_test_health_json()

    backend_client = Mock()

    backend_client.update_body_measurements.return_value = {
        "date": "2026-10-12",
        "source": "Health Auto Export",
    }

    result = import_body_measurements_metrics(
        export_data,
        backend_client,
    )

    # One Body Measurements record should have been sent
    # to the backend.
    backend_client.update_body_measurements.assert_called_once()

    payload_sent = (
        backend_client
        .update_body_measurements
        .call_args
        .args[0]
    )

    assert payload_sent["date"] == "2026-10-12"
    assert payload_sent["source"] == "Health Auto Export"
    assert payload_sent["weight_kg"] is not None
    assert payload_sent["body_mass_index"] is not None
    assert payload_sent["body_fat_percent"] is not None

    # Verify that the importer returns the backend response.
    assert result == {
        "date": "2026-10-12",
        "source": "Health Auto Export",
    }


def test_import_body_measurements_metrics_with_no_body_measurements_data():

    export_data = {
        "data": {
            "metrics": []
        }
    }

    backend_client = Mock()

    result = import_body_measurements_metrics(
        export_data,
        backend_client,
    )

    # No backend request should be made when there is
    # no Body Measurements data.
    backend_client.update_body_measurements.assert_not_called()

    assert result is None