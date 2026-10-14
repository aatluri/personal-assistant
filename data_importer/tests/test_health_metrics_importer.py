import json
from pathlib import Path

from data_importer.app.modules.health.importers.health_metrics_importer import (
    build_health_metrics_payload,
)


def test_build_health_metrics_payload():

    # Load a real Health Auto Export file so the test verifies
    # our importer against the actual JSON structure we receive.
    fixture_path = (
        Path(__file__).parent
        / "helpers"
        / "HealthMetrics-2026-10-12.json"
    )

    with fixture_path.open() as file:
        export_data = json.load(file)

    payload = build_health_metrics_payload(export_data)

    # Verify the record-level fields.
    assert payload["date"] == "2026-10-12"
    assert payload["source"] == "Health Auto Export"

    # Verify Health Metrics extracted from the export.
    assert payload["step_count"] == 4042
    assert payload["active_energy_kcal"] == 301.96316587905153
    assert payload["resting_energy_kcal"] == 1845.3776789350886

    assert payload["blood_oxygen_saturation_percent"] == 95.83333333333333

    assert payload["heart_rate_min_bpm"] == 37
    assert payload["heart_rate_max_bpm"] == 107
    assert payload["heart_rate_variability_ms"] == 75.16665205307112

    assert payload["physical_effort_kcal_hr_kg"] == 3.3663265449660167
    assert payload["respiratory_rate_bpm"] == 17.040816326530614
    assert payload["resting_heart_rate_bpm"] == 43

    # These metrics are not present in this particular export,
    # so the importer should return None rather than fail.
    assert payload["atrial_fibrillation_burden_percent"] is None
    assert payload["breathing_disturbances_count"] is None
    assert payload["cardio_recovery_bpm"] is None
    assert payload["flights_climbed"] is None