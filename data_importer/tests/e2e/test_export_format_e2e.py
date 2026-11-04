import warnings
from datetime import datetime

import pytest

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.constants import (
    FAILED_PREFIX,
    PROCESSED_PREFIX,
)
from app.modules.health.mappings.body_measurements_metrics_mapping import (
    BODY_MEASUREMENTS_METRICS_MAPPING,
)
from app.modules.health.mappings.health_metrics_mapping import (
    HEALTH_METRICS_MAPPING,
)
from app.modules.health.mappings.nutrition_metrics_mapping import (
    NUTRITION_METRICS_MAPPING,
)
from app.modules.health.mappings.sleep_metrics_mapping import (
    SLEEP_METRICS_MAPPING,
)
from app.modules.health.orchestrators.health_metrics_orchestrator import (
    get_health_metrics_file_date,
)
from app.modules.health.orchestrators.workout_metrics_orchestrator import (
    get_workout_metrics_file_date,
)


"""
Export Format Check (read-only E2E)

Checks that Health Auto Export's real files still have the format the
importer's mappings assume: metric names, value fields, date formats and,
most importantly, units. If the app changes a unit (for example water from
US fl oz to ml), the importer's conversions would silently store wrong
values; this test fails instead.

It reads the most recent real exports from Google Drive and NEVER imports,
renames or writes anything.

When Health Auto Export changes its format deliberately, update the
mappings and conversions first, then the expectations below.
"""


RECENT_FILE_COUNT = 7

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S %z"

HEALTH_MAPPINGS = [
    HEALTH_METRICS_MAPPING,
    NUTRITION_METRICS_MAPPING,
    SLEEP_METRICS_MAPPING,
    BODY_MEASUREMENTS_METRICS_MAPPING,
]

# The unit each Health Auto Export metric is expected to use. The
# importer's conversions depend on these (dietary_water → ml,
# weight_body_mass → kg), so a change here means wrong stored values.
EXPECTED_UNITS = {
    "step_count": "count",
    "active_energy": "kcal",
    "basal_energy_burned": "kcal",
    "blood_oxygen_saturation": "%",
    "heart_rate": "count/min",
    "heart_rate_variability": "ms",
    "physical_effort": "kcal/hr·kg",
    "respiratory_rate": "count/min",
    "resting_heart_rate": "count/min",
    "flights_climbed": "count",
    "dietary_energy": "kcal",
    "protein": "g",
    "carbohydrates": "g",
    "fiber": "g",
    "dietary_sugar": "g",
    "total_fat": "g",
    "saturated_fat": "g",
    "polyunsaturated_fat": "g",
    "monounsaturated_fat": "g",
    "dietary_water": "fl_oz_us",
    "cholesterol": "mg",
    "sleep_analysis": "hr",
    "weight_body_mass": "lb",
    "body_mass_index": "count",
    "body_fat_percentage": "%",
}

# Mapped metrics that are not recorded every day, so they may be missing
# from the recent files. When one without an EXPECTED_UNITS entry
# appears, its unit is reported as a warning so it can be added there.
OPTIONAL_METRICS = {
    "atrial_fibrillation_burden",
    "breathing_disturbances",
    "cardio_recovery",
    "flights_climbed",
}

# Fields read by the workout mapping, as paths into each workout, with
# the unit expected where the export labels one.
REQUIRED_WORKOUT_FIELDS = {
    ("name",): None,
    ("start",): None,
    ("end",): None,
    ("duration",): None,          # seconds; not labelled in the export
    ("totalEnergy", "qty"): "kcal",
    ("activeEnergyBurned", "qty"): "kcal",
    ("heartRate", "max", "qty"): "count/min",
    ("heartRate", "avg", "qty"): "count/min",
}

# Only outdoor workouts have these.
OPTIONAL_WORKOUT_FIELDS = {
    ("distance", "qty"): "mi",
    ("activities", 0, "metrics", "speed", "qty"): "m/s",
}


def read_recent_exports(
    drive_client: GoogleDriveClient,
    folder_id: str,
    get_file_date,
) -> list[tuple[str, dict]]:
    """
    Read the most recent real export files from a Drive folder, newest
    first. PROCESSED_ and FAILED_ files count, because they are real
    exports; TEST_ and other unrecognised files are ignored. Read-only.
    """

    dated_files = []

    for file in drive_client.list_files(folder_id):

        original_name = (
            file["name"]
            .removeprefix(PROCESSED_PREFIX)
            .removeprefix(FAILED_PREFIX)
        )

        file_date = get_file_date(original_name)

        if file_date is not None:
            dated_files.append((file_date, file))

    dated_files.sort(key=lambda item: item[0], reverse=True)

    return [
        (file["name"], drive_client.read_json_file(file["id"]))
        for _, file in dated_files[:RECENT_FILE_COUNT]
    ]


def parses_as_timestamp(value) -> bool:
    try:
        datetime.strptime(value, TIMESTAMP_FORMAT)
        return True
    except (TypeError, ValueError):
        return False


def get_path(data, path):
    """
    Follow a path of keys and list indexes; return None if any step is
    missing.
    """

    for step in path:
        try:
            data = data[step]
        except (KeyError, IndexError, TypeError):
            return None

    return data


def unit_for_path(workout: dict, path: tuple):
    """
    Return the unit label next to a value, e.g. the "units" beside
    totalEnergy.qty.
    """

    return get_path(workout, path[:-1] + ("units",))


def test_health_export_format_e2e():

    exports = read_recent_exports(
        GoogleDriveClient(),
        settings.HEALTH_METRICS_DRIVE_FOLDER_ID,
        get_health_metrics_file_date,
    )

    if not exports:
        pytest.skip("No Health Metrics exports found in Drive.")

    # Each mapped metric with the value fields the mappings read from it.
    value_fields_by_metric = {}

    for mapping in HEALTH_MAPPINGS:
        for field_mapping in mapping.values():
            value_fields_by_metric.setdefault(
                field_mapping["source_name"], set()
            ).add(field_mapping["value_field"])

    problems = []
    seen_metrics = set()

    for file_name, export_data in exports:

        metrics_by_name = {
            metric["name"]: metric
            for metric in export_data["data"]["metrics"]
        }

        for metric_name, value_fields in value_fields_by_metric.items():

            metric = metrics_by_name.get(metric_name)

            if metric is None or not metric.get("data"):
                continue

            seen_metrics.add(metric_name)

            units = metric.get("units")
            expected_units = EXPECTED_UNITS.get(metric_name)

            if expected_units is None:
                warnings.warn(
                    f"{metric_name} appeared in {file_name} with units "
                    f"{units!r}; add it to EXPECTED_UNITS."
                )
            elif units != expected_units:
                problems.append(
                    f"{file_name}: {metric_name} units changed from "
                    f"{expected_units!r} to {units!r}"
                )

            record = metric["data"][0]

            for value_field in sorted(value_fields):
                if value_field not in record:
                    problems.append(
                        f"{file_name}: {metric_name} data record has no "
                        f"{value_field!r} field"
                    )

            if not parses_as_timestamp(record.get("date")):
                problems.append(
                    f"{file_name}: {metric_name} date "
                    f"{record.get('date')!r} does not match "
                    f"{TIMESTAMP_FORMAT}"
                )

    for metric_name in sorted(value_fields_by_metric):
        if (
            metric_name not in seen_metrics
            and metric_name not in OPTIONAL_METRICS
        ):
            problems.append(
                f"{metric_name} not found in any of the last "
                f"{len(exports)} Health Metrics exports"
            )

    assert not problems, (
        "Health Auto Export format no longer matches the mappings:\n  "
        + "\n  ".join(problems)
    )


def test_workout_export_format_e2e():

    exports = read_recent_exports(
        GoogleDriveClient(),
        settings.WORKOUT_METRICS_DRIVE_FOLDER_ID,
        get_workout_metrics_file_date,
    )

    workouts = [
        (file_name, workout)
        for file_name, export_data in exports
        for workout in export_data["data"]["workouts"]
    ]

    if not workouts:
        pytest.skip("No workouts found in recent Workout Metrics exports.")

    problems = []

    for file_name, workout in workouts:

        label = f"{file_name}: workout {workout.get('name')!r}"

        for path, expected_units in REQUIRED_WORKOUT_FIELDS.items():

            if get_path(workout, path) is None:
                problems.append(f"{label} has no {'.'.join(map(str, path))}")

            elif expected_units is not None:
                units = unit_for_path(workout, path)

                if units != expected_units:
                    problems.append(
                        f"{label}: {'.'.join(map(str, path))} units "
                        f"changed from {expected_units!r} to {units!r}"
                    )

        for path, expected_units in OPTIONAL_WORKOUT_FIELDS.items():

            if get_path(workout, path) is None:
                continue

            units = unit_for_path(workout, path)

            if units != expected_units:
                problems.append(
                    f"{label}: {'.'.join(map(str, path))} units "
                    f"changed from {expected_units!r} to {units!r}"
                )

        for field in ("start", "end"):
            if not parses_as_timestamp(workout.get(field)):
                problems.append(
                    f"{label}: {field} {workout.get(field)!r} does not "
                    f"match {TIMESTAMP_FORMAT}"
                )

    assert not problems, (
        "Health Auto Export workout format no longer matches the "
        "mapping:\n  " + "\n  ".join(problems)
    )
