from datetime import datetime

from app.clients.backend_client import BackendClient
from app.modules.health.mappings.sleep_metrics_mapping import (
    SLEEP_METRICS_MAPPING,
)


def build_sleep_metrics_payload(
    export_data: dict,
) -> dict | None:
    """
    Transform Health Auto Export JSON into the payload expected
    by the Personal Assistant Sleep Metrics API.

    Returns None if the export contains no Sleep Metrics data.
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

    # Go through every backend Sleep Metrics field defined
    # in our mapping.
    for backend_field, mapping in SLEEP_METRICS_MAPPING.items():

        source_name = mapping["source_name"]
        value_field = mapping["value_field"]

        # Find the corresponding Health Auto Export metric.
        source_metric = metrics_by_name.get(source_name)

        # Sleep Analysis may not exist in every export.
        if source_metric is None:
            payload[backend_field] = None
            continue

        metric_data = source_metric.get("data", [])

        # The metric may exist but contain no data.
        if not metric_data:
            payload[backend_field] = None
            continue

        # Health Auto Export provides the daily sleep data
        # inside the sleep_analysis record.
        data_record = metric_data[0]

        # Extract the required sleep value.
        value = data_record.get(value_field)

        # Convert Health Auto Export timestamps into ISO 8601 format.
        if backend_field in {
            "sleep_start_time",
            "sleep_end_time",
        } and value is not None:

            parsed_datetime = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S %z",
            )

            value = parsed_datetime.isoformat()

        # Round sleep duration values to 2 decimal places.
        if isinstance(value, (int, float)):
            value = round(value, 2)

        payload[backend_field] = value

        # Determine the record date from the sleep analysis record.
        if record_date is None:

            source_date = data_record.get("date")

            if source_date:
                parsed_date = datetime.strptime(
                    source_date,
                    "%Y-%m-%d %H:%M:%S %z",
                )

                record_date = parsed_date.date().isoformat()

    # If there is no Sleep data in this export,
    # there is nothing to import.
    #
    # Missing sleep data is valid and should not cause
    # the entire Health Auto Export file to fail.
    if record_date is None:
        return None

    # Add fields that do not come from the mapping.
    payload["date"] = record_date
    payload["source"] = "Health Auto Export"

    return payload


def import_sleep_metrics(
    export_data: dict,
    backend_client: BackendClient,
) -> dict | None:
    """
    Import Sleep Metrics into the Personal Assistant backend.

    If the export contains no Sleep Metrics data,
    nothing is imported.
    """

    # Convert the Health Auto Export JSON into the format
    # expected by the Personal Assistant backend.
    payload = build_sleep_metrics_payload(export_data)

    # No Sleep Metrics data exists in this export.
    # This is not considered an error.
    if payload is None:
        return None

    # Send the Sleep Metrics record to the backend.
    #
    # The backend is responsible for persistence.
    # The Data Importer does not write directly to Google Sheets.
    return backend_client.update_sleep_metrics(payload)