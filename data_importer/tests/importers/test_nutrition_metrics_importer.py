import json
from pathlib import Path
from unittest.mock import Mock

from app.modules.health.importers.nutrition_metrics_importer import (
    build_nutrition_metrics_payload,
    import_nutrition_metrics,
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


def test_build_nutrition_metrics_payload():

    export_data = load_test_health_json()

    payload = build_nutrition_metrics_payload(export_data)

    assert payload is not None

    # Verify the record-level fields.
    assert payload["date"] == "2026-10-12"
    assert payload["source"] == "Health Auto Export"

    # Verify the exact Nutrition Metrics extracted from
    # the real Health Auto Export file.
    assert payload["dietary_energy_kcal"] == 1903
    assert payload["protein_g"] == 111
    assert payload["carbohydrates_g"] == 129
    assert payload["fiber_g"] == 21
    assert payload["sugar_g"] == 22
    assert payload["total_fat_g"] == 106
    assert payload["saturated_fat_g"] == 32
    assert payload["polyunsaturated_fat_g"] == 17
    assert payload["monounsaturated_fat_g"] == 32
    assert payload["water_fl_oz_us"] == 120
    assert payload["cholesterol_mg"] == 700

def test_build_nutrition_metrics_payload_with_no_nutrition_data():

    export_data = {
        "data": {
            "metrics": []
        }
    }

    payload = build_nutrition_metrics_payload(export_data)

    assert payload is None


def test_import_nutrition_metrics():

    export_data = load_test_health_json()

    backend_client = Mock()

    backend_client.update_nutrition_metrics.return_value = {
        "date": "2026-10-12",
        "source": "Health Auto Export",
    }

    result = import_nutrition_metrics(
        export_data,
        backend_client,
    )

    # One Nutrition Metrics record should have been sent
    # to the backend.
    backend_client.update_nutrition_metrics.assert_called_once()

    payload_sent = (
        backend_client
        .update_nutrition_metrics
        .call_args
        .args[0]
    )

    assert payload_sent["date"] == "2026-10-12"
    assert payload_sent["source"] == "Health Auto Export"
    assert payload_sent["dietary_energy_kcal"] is not None
    assert payload_sent["protein_g"] is not None

    # Verify that the importer returns the backend response.
    assert result == {
        "date": "2026-10-12",
        "source": "Health Auto Export",
    }


def test_import_nutrition_metrics_with_no_nutrition_data():

    export_data = {
        "data": {
            "metrics": []
        }
    }

    backend_client = Mock()

    result = import_nutrition_metrics(
        export_data,
        backend_client,
    )

    # No backend request should be made when there is
    # no Nutrition Metrics data.
    backend_client.update_nutrition_metrics.assert_not_called()

    assert result is None