from datetime import date, datetime
import pytest
import requests

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.importers.body_measurements_metrics_importer import (
    build_body_measurements_metrics_payload,
)
from app.modules.health.importers.health_metrics_importer import (
    build_health_metrics_payload,
)
from app.modules.health.importers.nutrition_metrics_importer import (
    build_nutrition_metrics_payload,
)
from app.modules.health.importers.sleep_metrics_importer import (
    build_sleep_metrics_payload,
)


DATA_IMPORTER_BASE_URL = "http://127.0.0.1:8001"
BACKEND_BASE_URL = "http://127.0.0.1:8000"

FAILED_PREFIX = "FAILED_"
PROCESSED_PREFIX = "PROCESSED_"
FILE_PREFIX = "HealthMetrics-"
FILE_SUFFIX = ".json"


def get_health_metrics_file_date(
    file_name: str,
) -> date | None:
    """
    Extract the date from an unprocessed Health Metrics filename.
    """

    if (
        file_name.startswith(FAILED_PREFIX)
        or file_name.startswith(PROCESSED_PREFIX)
    ):
        return None

    if not (
        file_name.startswith(FILE_PREFIX)
        and file_name.endswith(FILE_SUFFIX)
    ):
        return None

    date_text = file_name[
        len(FILE_PREFIX):-len(FILE_SUFFIX)
    ]

    try:
        return datetime.strptime(
            date_text,
            "%Y-%m-%d",
        ).date()

    except ValueError:
        return None


def get_latest_health_metrics_file(
    drive_client: GoogleDriveClient,
) -> dict:
    """
    Return the newest unprocessed Health Metrics file
    from the configured incoming Google Drive folder.
    """

    files = drive_client.list_files(
        settings.HEALTH_METRICS_DRIVE_FOLDER_ID
    )

    valid_files = []

    for file in files:
        print(file["name"])
        file_date = get_health_metrics_file_date(
            file["name"]
        )

        if file_date is not None:
            valid_files.append(
                (
                    file_date,
                    file,
                )
            )

    assert valid_files, (
        "No unprocessed Health Metrics files found "
        "in the incoming Google Drive folder."
    )

    valid_files.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return valid_files[0][1]


def assert_payload_matches_record(
    expected: dict,
    actual: dict,
) -> None:
    """
    Verify that every expected payload field matches
    the value returned by the backend.
    """

    for field, expected_value in expected.items():

        assert field in actual, (
            f"Field '{field}' missing from backend response."
        )

        actual_value = actual[field]

        if isinstance(expected_value, float):
            assert actual_value == pytest.approx(
                expected_value,
                abs=0.01,
            ), (
                f"Mismatch for '{field}': "
                f"expected {expected_value!r}, "
                f"got {actual_value!r}"
            )
        else:
            assert actual_value == expected_value, (
                f"Mismatch for '{field}': "
                f"expected {expected_value!r}, "
                f"got {actual_value!r}"
            )


def test_health_metrics_importer_e2e():

    drive_client = GoogleDriveClient()

    # ---------------------------------------------------------
    # 1. FIND THE LATEST UNPROCESSED HEALTH AUTO EXPORT FILE
    # ---------------------------------------------------------

    file = get_latest_health_metrics_file(
        drive_client
    )

    file_id = file["id"]
    file_name = file["name"]

    print(
        f"Testing Health Metrics import with: "
        f"{file_name}"
    )

    # ---------------------------------------------------------
    # 2. READ THE REAL JSON FILE
    # ---------------------------------------------------------

    export_data = drive_client.read_json_file(
        file_id
    )

    assert export_data is not None

    assert "data" in export_data
    assert "metrics" in export_data["data"]

    # ---------------------------------------------------------
    # 3. BUILD THE EXPECTED BACKEND PAYLOADS
    # ---------------------------------------------------------

    expected_health = build_health_metrics_payload(
        export_data
    )

    expected_nutrition = build_nutrition_metrics_payload(
        export_data
    )

    expected_sleep = build_sleep_metrics_payload(
        export_data
    )

    expected_body_measurements = (
        build_body_measurements_metrics_payload(
            export_data
        )
    )

    assert expected_health is not None, (
        f"{file_name} contains no Health Metrics data."
    )

    # ---------------------------------------------------------
    # 4. RUN THE DATA IMPORTER
    # ---------------------------------------------------------

    response = requests.put(
        f"{DATA_IMPORTER_BASE_URL}"
        f"/health/import/health-metrics",
        params={
            "file_name": file_name,
        },
        timeout=30,
    )

    assert response.status_code == 200, response.text

    import_result = response.json()

    assert import_result["status"] == "success"

    assert import_result["files_processed"] == 1

    assert len(import_result["results"]) == 1

    file_result = import_result["results"][0]

    assert file_result["file_name"] == file_name

    # ---------------------------------------------------------
    # 5. VERIFY IMPORTER RESULT
    # ---------------------------------------------------------

    assert (
        file_result["health_metrics"]
        is not None
    )

    if expected_nutrition is None:

        assert (
            file_result["nutrition_metrics"]
            is None
        )

    else:

        assert (
            file_result["nutrition_metrics"]
            is not None
        )

    if expected_sleep is None:

        assert (
            file_result["sleep_metrics"]
            is None
        )

    else:

        assert (
            file_result["sleep_metrics"]
            is not None
        )

    if expected_body_measurements is None:

        assert (
            file_result["body_measurements_metrics"]
            is None
        )

    else:

        assert (
            file_result["body_measurements_metrics"]
            is not None
        )

    # ---------------------------------------------------------
    # 6. VERIFY HEALTH METRICS THROUGH BACKEND
    # ---------------------------------------------------------

    health_date = expected_health["date"]

    response = requests.get(
        f"{BACKEND_BASE_URL}"
        f"/health/health-metrics/{health_date}",
        timeout=10,
    )

    assert response.status_code == 200, response.text

    actual_health = response.json()

    assert_payload_matches_record(
        expected_health,
        actual_health,
    )

    # ---------------------------------------------------------
    # 7. VERIFY NUTRITION METRICS THROUGH BACKEND
    # ---------------------------------------------------------

    if expected_nutrition is not None:

        nutrition_date = expected_nutrition["date"]

        response = requests.get(
            f"{BACKEND_BASE_URL}"
            f"/health/nutrition-metrics/{nutrition_date}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        actual_nutrition = response.json()

        assert_payload_matches_record(
            expected_nutrition,
            actual_nutrition,
        )

    # ---------------------------------------------------------
    # 8. VERIFY SLEEP METRICS THROUGH BACKEND
    # ---------------------------------------------------------

    if expected_sleep is not None:

        sleep_date = expected_sleep["date"]

        response = requests.get(
            f"{BACKEND_BASE_URL}"
            f"/health/sleep-metrics/{sleep_date}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        actual_sleep = response.json()

        # Google Sheets stores Sleep timestamps without
        # timezone information.
        expected_sleep["sleep_start_time"] = (
            datetime.fromisoformat(
                expected_sleep["sleep_start_time"]
            )
            .replace(tzinfo=None)
            .isoformat()
        )

        expected_sleep["sleep_end_time"] = (
            datetime.fromisoformat(
                expected_sleep["sleep_end_time"]
            )
            .replace(tzinfo=None)
            .isoformat()
        )

        assert_payload_matches_record(
            expected_sleep,
            actual_sleep,
        )

    # ---------------------------------------------------------
    # 9. VERIFY BODY MEASUREMENTS THROUGH BACKEND
    # ---------------------------------------------------------

    if expected_body_measurements is not None:

        body_measurements_date = (
            expected_body_measurements["date"]
        )

        response = requests.get(
            f"{BACKEND_BASE_URL}"
            f"/health/body-measurements/"
            f"{body_measurements_date}",
            timeout=10,
        )

        assert response.status_code == 200, response.text

        actual_body_measurements = response.json()

        assert_payload_matches_record(
            expected_body_measurements,
            actual_body_measurements,
        )

    # ---------------------------------------------------------
    # 10. VERIFY FILE WAS MARKED AS PROCESSED
    # ---------------------------------------------------------

    files = drive_client.list_files(
        settings.HEALTH_METRICS_DRIVE_FOLDER_ID
    )

    processed_file_name = (
        f"{PROCESSED_PREFIX}{file_name}"
    )

    processed_file = next(
        (
            file
            for file in files
            if (
                file["id"] == file_id
                and file["name"] == processed_file_name
            )
        ),
        None,
    )

    assert processed_file is not None, (
        f"Expected file '{processed_file_name}' "
        f"was not found after processing."
    )