from datetime import datetime

from app.clients.backend_client import BackendClient
from app.modules.health.mappings.workout_metrics_mapping import (
    WORKOUT_METRICS_MAPPING,
)


def build_workout_metrics_payloads(
    export_data: dict,
) -> list[dict]:
    """
    Transform Health Auto Export JSON into the payloads expected
    by the Personal Assistant Workout Metrics API.

    One payload is created for each workout.
    """

    workouts = export_data.get("data", {}).get("workouts", [])

    payloads = []

    for workout in workouts:

        payload = {}

        for backend_field, mapping in WORKOUT_METRICS_MAPPING.items():

            source_field = mapping["source_field"]

            value = workout.get(source_field)

            # Move through any nested fields defined in the mapping.
            for mapping_field in (
                "value_field",
                "nested_value_field",
                "final_value_field",
            ):
                nested_field = mapping.get(mapping_field)

                if nested_field is None:
                    continue

                if isinstance(value, list):
                    # For fields such as activities, use the first
                    # recorded workout activity.
                    if not value:
                        value = None
                        break

                    value = value[0]

                if not isinstance(value, dict):
                    value = None
                    break

                value = value.get(nested_field)

            # Convert Health Auto Export timestamps into ISO 8601.
            if backend_field in {
                "workout_start_time",
                "workout_end_time",
            } and value is not None:

                parsed_datetime = datetime.strptime(
                    value,
                    "%Y-%m-%d %H:%M:%S %z",
                )

                value = parsed_datetime.isoformat()

            # Health Auto Export provides workout duration in seconds.
            # Convert it to whole minutes.
            if (
                backend_field == "workout_duration_min"
                and value is not None
            ):
                value = int(round(value / 60))

            # Health Auto Export provides distance in miles
            # Convert it to km because the current backend
            # Distance field is in km
            if (
                backend_field == "distance_km"
                and value is not None
            ):
                value = value * 1.609344
            # Health Auto Export provides average speed in metres per second.
            # Convert it to km per hour because the current backend
            # Workout Metrics field is avg_speed_kmph.
            if (
                backend_field == "avg_speed_kmph"
                and value is not None
            ):
                value = value * 3.6

            # Round numeric workout values to 2 decimal places.
            if (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
            ):
                value = round(value, 2)
            payload[backend_field] = value

        # Derive the workout date from its start time.
        start_time = workout.get("start")

        if start_time is None:
            continue

        parsed_start_time = datetime.strptime(
            start_time,
            "%Y-%m-%d %H:%M:%S %z",
        )

        payload["date"] = parsed_start_time.date().isoformat()
        payload["source"] = "Health Auto Export"

        payloads.append(payload)

    return payloads


def import_workout_metrics(
    export_data: dict,
    backend_client: BackendClient,
) -> list[dict]:
    """
    Import Workout Metrics into the Personal Assistant backend.

    Each workout is imported as a separate Workout Metrics record.
    """

    payloads = build_workout_metrics_payloads(export_data)

    results = []

    for payload in payloads:

        result = backend_client.update_workout_metrics(payload)

        results.append(result)

    return results