import json
from pathlib import Path
from unittest.mock import Mock

from app.modules.health.importers.sleep_metrics_importer import (
    build_sleep_metrics_payload,
    import_sleep_metrics,
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


def test_build_sleep_metrics_payload():

    export_data = load_test_health_json()

    payload = build_sleep_metrics_payload(export_data)

    assert payload is not None

    # Verify the record-level fields.
    assert payload["date"] == "2026-10-12"
    assert payload["source"] == "Health Auto Export"

    # Verify the exact Sleep Metrics extracted from
    # the real Health Auto Export file.
    assert payload["sleep_start_time"] == "2026-10-11T23:59:40+05:30"
    assert payload["sleep_end_time"] == "2026-10-12T07:24:32+05:30"

    assert payload["total_sleep_duration_hr"] == 7.23
    assert payload["core_sleep_hr"] == 4.10
    assert payload["rem_sleep_hr"] == 2.23
    assert payload["deep_sleep_hr"] == 0.90
    assert payload["awake_hr"] == 0.18


def test_build_sleep_metrics_payload_with_no_sleep_data():

    export_data = {
        "data": {
            "metrics": []
        }
    }

    payload = build_sleep_metrics_payload(export_data)

    assert payload is None


def test_import_sleep_metrics():

    export_data = load_test_health_json()

    backend_client = Mock()

    backend_client.update_sleep_metrics.return_value = {
        "date": "2026-10-12",
        "source": "Health Auto Export",
    }

    result = import_sleep_metrics(
        export_data,
        backend_client,
    )

    # One Sleep Metrics record should have been sent to the backend.
    backend_client.update_sleep_metrics.assert_called_once()

    payload_sent = (
        backend_client
        .update_sleep_metrics
        .call_args
        .args[0]
    )

    assert payload_sent["date"] == "2026-10-12"
    assert payload_sent["source"] == "Health Auto Export"
    assert payload_sent["sleep_start_time"] is not None
    assert payload_sent["sleep_end_time"] is not None

    # Verify that the importer returns the backend response.
    assert result == {
        "date": "2026-10-12",
        "source": "Health Auto Export",
    }


def test_import_sleep_metrics_with_no_sleep_data():

    export_data = {
        "data": {
            "metrics": []
        }
    }

    backend_client = Mock()

    result = import_sleep_metrics(
        export_data,
        backend_client,
    )

    # No backend request should be made when there is
    # no Sleep Metrics data.
    backend_client.update_sleep_metrics.assert_not_called()

    assert result is None