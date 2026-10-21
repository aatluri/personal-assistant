import hashlib
from unittest.mock import patch

from app.modules.health.labs.lab_schemas import (
    LabReport,
    LabResult,
)
from app.modules.health.labs.lab_save_schemas import (
    LabReportSaveRequest,
)
from app.modules.health.labs.lab_service import (
    generate_report_key,
    save_lab_report,
)


TEST_REPORT_DATE = "2026-08-30"
TEST_FILE_NAME = "test_lab_report.pdf"


def build_save_request() -> LabReportSaveRequest:
    return LabReportSaveRequest(
        report_date=TEST_REPORT_DATE,
        collection_date="2026-08-30",
        report_datetime="2026-08-30 09:30:00",
        report_type="Blood Work",
        laboratory_name="Test Laboratory",
        file_name=TEST_FILE_NAME,
        notes="Service test",
        results=[
            {
                "marker_key": "FASTING_GLUCOSE",
                "numerical_value": 101,
                "text_value": "",
                "unit": "mg/dL",
            },
            {
                "marker_key": "LDL_CHOLESTEROL",
                "numerical_value": 133,
                "text_value": "",
                "unit": "mg/dL",
            },
            {
                "marker_key": "STOOL_OCCULT_BLOOD",
                "numerical_value": None,
                "text_value": "Negative",
                "unit": "",
            },
        ],
    )


def test_generate_report_key():
    expected_hash = hashlib.sha256(
        TEST_FILE_NAME.encode("utf-8")
    ).hexdigest()[:12]

    expected_key = f"LAB_20260830_{expected_hash}"

    result = generate_report_key(
        TEST_REPORT_DATE,
        TEST_FILE_NAME,
    )

    assert result == expected_key
    assert len(result) == 25


def test_generate_report_key_is_deterministic():
    first_key = generate_report_key(
        TEST_REPORT_DATE,
        TEST_FILE_NAME,
    )

    second_key = generate_report_key(
        TEST_REPORT_DATE,
        TEST_FILE_NAME,
    )

    assert first_key == second_key


def test_generate_report_key_changes_when_filename_changes():
    first_key = generate_report_key(
        TEST_REPORT_DATE,
        "report_1.pdf",
    )

    second_key = generate_report_key(
        TEST_REPORT_DATE,
        "report_2.pdf",
    )

    assert first_key != second_key


def test_save_lab_report_creates_new_report_and_results():
    save_request = build_save_request()

    report_key = generate_report_key(
        TEST_REPORT_DATE,
        TEST_FILE_NAME,
    )

    with (
        patch(
            "app.modules.health.labs.lab_service.get_lab_report",
            return_value=None,
        ) as mock_get_report,
        patch(
            "app.modules.health.labs.lab_service.create_lab_report",
            side_effect=lambda report: report,
        ) as mock_create_report,
        patch(
            "app.modules.health.labs.lab_service.update_lab_report",
        ) as mock_update_report,
        patch(
            "app.modules.health.labs.lab_service.get_lab_result",
            return_value=None,
        ) as mock_get_result,
        patch(
            "app.modules.health.labs.lab_service.create_lab_result",
            side_effect=lambda result: result,
        ) as mock_create_result,
        patch(
            "app.modules.health.labs.lab_service.update_lab_result",
        ) as mock_update_result,
    ):
        response = save_lab_report(save_request)

    mock_get_report.assert_called_once_with(report_key)
    mock_create_report.assert_called_once()
    mock_update_report.assert_not_called()

    created_report = mock_create_report.call_args.args[0]

    assert created_report.report_key == report_key
    assert created_report.report_date == TEST_REPORT_DATE
    assert created_report.collection_date == "2026-08-30"
    assert created_report.report_type == "Blood Work"
    assert created_report.laboratory_name == "Test Laboratory"
    assert created_report.file_name == TEST_FILE_NAME

    assert mock_get_result.call_count == 3
    assert mock_create_result.call_count == 3
    assert mock_update_result.call_count == 0

    assert response.report.report_key == report_key
    assert len(response.results) == 3


def test_save_lab_report_updates_existing_report_and_results():
    save_request = build_save_request()

    report_key = generate_report_key(
        TEST_REPORT_DATE,
        TEST_FILE_NAME,
    )

    existing_report = LabReport(
        report_key=report_key,
        report_date=TEST_REPORT_DATE,
        collection_date="2026-08-30",
        report_datetime="2026-08-30 09:30:00",
        report_type="Blood Work",
        laboratory_name="Old Laboratory",
        file_name=TEST_FILE_NAME,
        notes="Old notes",
    )

    existing_result = LabResult(
        report_key=report_key,
        marker_key="FASTING_GLUCOSE",
        numerical_value=99,
        text_value="",
        unit="mg/dL",
    )

    with (
        patch(
            "app.modules.health.labs.lab_service.get_lab_report",
            return_value=existing_report,
        ),
        patch(
            "app.modules.health.labs.lab_service.create_lab_report",
        ) as mock_create_report,
        patch(
            "app.modules.health.labs.lab_service.update_lab_report",
            side_effect=lambda key, report: report,
        ) as mock_update_report,
        patch(
            "app.modules.health.labs.lab_service.get_lab_result",
            return_value=existing_result,
        ),
        patch(
            "app.modules.health.labs.lab_service.create_lab_result",
        ) as mock_create_result,
        patch(
            "app.modules.health.labs.lab_service.update_lab_result",
            side_effect=lambda report_key, marker_key, result: result,
        ) as mock_update_result,
    ):
        response = save_lab_report(save_request)

    mock_create_report.assert_not_called()
    mock_update_report.assert_called_once()

    updated_report_key, updated_report = (
        mock_update_report.call_args.args
    )

    assert updated_report_key == report_key
    assert updated_report.report_key == report_key
    assert updated_report.laboratory_name == "Test Laboratory"

    assert mock_create_result.call_count == 0
    assert mock_update_result.call_count == 3

    assert len(response.results) == 3


def test_save_lab_report_skips_empty_results():
    save_request = LabReportSaveRequest(
        report_date=TEST_REPORT_DATE,
        collection_date="2026-08-30",
        report_datetime="2026-08-30 09:30:00",
        report_type="Blood Work",
        laboratory_name="Test Laboratory",
        file_name=TEST_FILE_NAME,
        notes="Service test",
        results=[
            {
                "marker_key": "FASTING_GLUCOSE",
                "numerical_value": 101,
                "text_value": "",
                "unit": "mg/dL",
            },
            {
                "marker_key": "EMPTY_RESULT",
                "numerical_value": None,
                "text_value": "",
                "unit": "",
            },
            {
                "marker_key": "WHITESPACE_RESULT",
                "numerical_value": None,
                "text_value": "   ",
                "unit": "",
            },
        ],
    )

    with (
        patch(
            "app.modules.health.labs.lab_service.get_lab_report",
            return_value=None,
        ),
        patch(
            "app.modules.health.labs.lab_service.create_lab_report",
            side_effect=lambda report: report,
        ),
        patch(
            "app.modules.health.labs.lab_service.get_lab_result",
            return_value=None,
        ) as mock_get_result,
        patch(
            "app.modules.health.labs.lab_service.create_lab_result",
            side_effect=lambda result: result,
        ) as mock_create_result,
    ):
        response = save_lab_report(save_request)

    # Only FASTING_GLUCOSE should reach the repository.
    mock_get_result.assert_called_once()
    mock_create_result.assert_called_once()

    saved_result = mock_create_result.call_args.args[0]

    assert saved_result.marker_key == "FASTING_GLUCOSE"
    assert saved_result.numerical_value == 101

    assert len(response.results) == 1
    assert response.results[0].marker_key == "FASTING_GLUCOSE"


def test_save_lab_report_accepts_text_only_result():
    save_request = LabReportSaveRequest(
        report_date=TEST_REPORT_DATE,
        collection_date="2026-08-30",
        report_datetime="2026-08-30 09:30:00",
        report_type="Blood Work",
        laboratory_name="Test Laboratory",
        file_name=TEST_FILE_NAME,
        notes="Service test",
        results=[
            {
                "marker_key": "STOOL_OCCULT_BLOOD",
                "numerical_value": None,
                "text_value": "Negative",
                "unit": "",
            }
        ],
    )

    with (
        patch(
            "app.modules.health.labs.lab_service.get_lab_report",
            return_value=None,
        ),
        patch(
            "app.modules.health.labs.lab_service.create_lab_report",
            side_effect=lambda report: report,
        ),
        patch(
            "app.modules.health.labs.lab_service.get_lab_result",
            return_value=None,
        ),
        patch(
            "app.modules.health.labs.lab_service.create_lab_result",
            side_effect=lambda result: result,
        ) as mock_create_result,
    ):
        response = save_lab_report(save_request)

    mock_create_result.assert_called_once()

    saved_result = mock_create_result.call_args.args[0]

    assert saved_result.marker_key == "STOOL_OCCULT_BLOOD"
    assert saved_result.numerical_value is None
    assert saved_result.text_value == "Negative"

    assert len(response.results) == 1


def test_save_lab_report_accepts_zero_as_numeric_result():
    save_request = LabReportSaveRequest(
        report_date=TEST_REPORT_DATE,
        collection_date="2026-08-30",
        report_datetime="2026-08-30 09:30:00",
        report_type="Blood Work",
        laboratory_name="Test Laboratory",
        file_name=TEST_FILE_NAME,
        notes="Service test",
        results=[
            {
                "marker_key": "ZERO_RESULT",
                "numerical_value": 0,
                "text_value": "",
                "unit": "mg/dL",
            }
        ],
    )

    with (
        patch(
            "app.modules.health.labs.lab_service.get_lab_report",
            return_value=None,
        ),
        patch(
            "app.modules.health.labs.lab_service.create_lab_report",
            side_effect=lambda report: report,
        ),
        patch(
            "app.modules.health.labs.lab_service.get_lab_result",
            return_value=None,
        ),
        patch(
            "app.modules.health.labs.lab_service.create_lab_result",
            side_effect=lambda result: result,
        ) as mock_create_result,
    ):
        response = save_lab_report(save_request)

    mock_create_result.assert_called_once()

    saved_result = mock_create_result.call_args.args[0]

    assert saved_result.numerical_value == 0
    assert len(response.results) == 1