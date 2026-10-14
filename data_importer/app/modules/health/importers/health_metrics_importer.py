from datetime import datetime

from app.clients.backend_client import BackendClient
from app.modules.health.mappings.health_metrics_mapping import (
    HEALTH_METRICS_MAPPING,
)


def build_health_metrics_payload(export_data: dict) -> dict:
    """
    Transform Health Auto Export JSON into the payload expected
    by the Personal Assistant Health Metrics API.
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

    # Go through every backend Health Metrics field defined
    # in our mapping.
    for backend_field, mapping in HEALTH_METRICS_MAPPING.items():

        source_name = mapping["source_name"]
        value_field = mapping["value_field"]

        # Find the corresponding Health Auto Export metric.
        source_metric = metrics_by_name.get(source_name)

        # Some Health Metrics may not exist in every export.
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

        # Extract the required value.
        #
        # Most metrics use "qty".
        # Heart Rate uses fields such as "Min" and "Max".
        # The mapping determines which field to use.

        # Extract the value from the Health Auto Export record.
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

    # A Health Metrics record must always have a date.
    if record_date is None:
        raise ValueError(
            "Unable to determine Health Metrics date from export data."
        )

    # Add fields that do not come from the mapping.
    payload["date"] = record_date
    payload["source"] = "Health Auto Export"

    return payload


def import_health_metrics(
    export_data: dict,
    backend_client: BackendClient,
) -> dict:
    """
    Import Health Metrics into the Personal Assistant backend.
    """

    # Convert the Health Auto Export JSON into the format
    # expected by the Personal Assistant backend.
    payload = build_health_metrics_payload(export_data)

    # Send the Health Metrics record to the backend.
    #
    # The backend is responsible for persistence.
    # The Data Importer does not write directly to Google Sheets.
    return backend_client.update_health_metrics(payload)