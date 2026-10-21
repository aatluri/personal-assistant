from datetime import datetime

from app.clients.backend_client import BackendClient
from app.modules.health.mappings.nutrition_metrics_mapping import (
    NUTRITION_METRICS_MAPPING,
)


def build_nutrition_metrics_payload(
    export_data: dict,
) -> dict | None:
    """
    Transform Health Auto Export JSON into the payload expected
    by the Personal Assistant Nutrition Metrics API.

    Returns None if the export contains no Nutrition Metrics data.
    """

    # Get all metrics from the Health Auto Export JSON.
    metrics = export_data["data"]["metrics"]

    # Create a lookup dictionary using the metric name.
    # This means we do not depend on the order of metrics in the JSON.
    metrics_by_name = {
        metric["name"]: metric
        for metric in metrics
    }

    payload = {}
    record_date = None

    # Go through every backend Nutrition Metrics field defined
    # in our mapping.
    for backend_field, mapping in NUTRITION_METRICS_MAPPING.items():

        source_name = mapping["source_name"]
        value_field = mapping["value_field"]

        # Find the corresponding Health Auto Export metric.
        source_metric = metrics_by_name.get(source_name)

        # Some Nutrition Metrics may not exist in every export.
        if source_metric is None:
            payload[backend_field] = None
            continue

        metric_data = source_metric.get("data", [])

        # The metric may exist but contain no data.
        if not metric_data:
            payload[backend_field] = None
            continue

        # Health Auto Export currently provides one aggregated
        # daily record for these metrics.
        data_record = metric_data[0]

        # Extract the value using the field defined in the mapping.
        value = data_record.get(value_field)

        # Apply any type conversion defined in the mapping.
        value_type = mapping.get("value_type")

        if value is not None and value_type == "int":
            value = int(round(value))

        payload[backend_field] = value

        # Determine the date from the first available metric
        # containing a date.
        if record_date is None:

            source_date = data_record.get("date")

            if source_date:
                parsed_date = datetime.strptime(
                    source_date,
                    "%Y-%m-%d %H:%M:%S %z",
                )

                record_date = parsed_date.date().isoformat()

    # If none of the Nutrition Metrics in our mapping contained
    # data, there is nothing to import for this file.
    #
    # Missing nutrition data is valid and should not cause
    # the entire Health Auto Export file to fail.
    if record_date is None:
        return None

    # Add fields that do not come from the mapping.
    payload["date"] = record_date
    payload["source"] = "Health Auto Export"

    return payload


def import_nutrition_metrics(
    export_data: dict,
    backend_client: BackendClient,
) -> dict | None:
    """
    Import Nutrition Metrics into the Personal Assistant backend.

    If the export contains no Nutrition Metrics data,
    nothing is imported.
    """

    # Convert the Health Auto Export JSON into the format
    # expected by the Personal Assistant backend.
    payload = build_nutrition_metrics_payload(export_data)

    # No Nutrition Metrics data exists in this export.
    # This is not considered an error.
    if payload is None:
        return None

    # Send the Nutrition Metrics record to the backend.
    #
    # The backend is responsible for persistence.
    # The Data Importer does not write directly to Google Sheets.
    return backend_client.update_nutrition_metrics(payload)