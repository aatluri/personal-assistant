from unittest.mock import MagicMock, patch

from app.modules.health.labs.lab_repository import (
    create_lab_result,
    get_lab_result,
    list_lab_results,
    update_lab_result,
)
from app.modules.health.labs.lab_schemas import LabResult


TEST_DATETIME = "2026-10-21 10:30:00"


def test_create_lab_result():
    worksheet = MagicMock()

    lab_result = LabResult(
        report_key="TEST_REPORT_001",
        marker_key="TEST_LDL",
        numerical_value=110,
        text_value="",
        unit="mg/dL",
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_results_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = create_lab_result(lab_result)

    worksheet.append_row.assert_called_once_with([
        "TEST_REPORT_001",
        "TEST_LDL",
        110,
        "",
        "mg/dL",
        TEST_DATETIME,
    ])

    assert result.report_key == "TEST_REPORT_001"
    assert result.marker_key == "TEST_LDL"
    assert result.updated_datetime == TEST_DATETIME


def test_get_numeric_lab_result():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "TEST_REPORT_001",
            "Marker_Key": "TEST_LDL",
            "Numerical_Value": 110,
            "Text_Value": "",
            "Unit": "mg/dL",
            "Updated_DateTime": TEST_DATETIME,
        }
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_results_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_result(
            "TEST_REPORT_001",
            "TEST_LDL",
        )

    assert result is not None
    assert result.report_key == "TEST_REPORT_001"
    assert result.marker_key == "TEST_LDL"
    assert result.numerical_value == 110
    assert result.text_value == ""
    assert result.unit == "mg/dL"
    assert result.updated_datetime == TEST_DATETIME


def test_get_text_lab_result():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "TEST_REPORT_001",
            "Marker_Key": "HBSAG",
            "Numerical_Value": "",
            "Text_Value": "Negative",
            "Unit": "",
            "Updated_DateTime": TEST_DATETIME,
        }
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_results_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_result(
            "TEST_REPORT_001",
            "HBSAG",
        )

    assert result is not None
    assert result.numerical_value is None
    assert result.text_value == "Negative"
    assert result.unit == ""


def test_get_lab_result_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = []

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_results_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_result(
            "REPORT_DOES_NOT_EXIST",
            "MARKER_DOES_NOT_EXIST",
        )

    assert result is None


def test_list_lab_results():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "REPORT_001",
            "Marker_Key": "LDL",
            "Numerical_Value": 110,
            "Text_Value": "",
            "Unit": "mg/dL",
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Report_Key": "REPORT_002",
            "Marker_Key": "HBSAG",
            "Numerical_Value": "",
            "Text_Value": "Negative",
            "Unit": "",
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_results_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_results()

    assert len(results) == 2
    assert results[0].marker_key == "LDL"
    assert results[0].numerical_value == 110

    assert results[1].marker_key == "HBSAG"
    assert results[1].numerical_value is None
    assert results[1].text_value == "Negative"


def test_list_lab_results_filtered_by_report_key():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "REPORT_001",
            "Marker_Key": "LDL",
            "Numerical_Value": 110,
            "Text_Value": "",
            "Unit": "mg/dL",
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Report_Key": "REPORT_002",
            "Marker_Key": "LDL",
            "Numerical_Value": 120,
            "Text_Value": "",
            "Unit": "mg/dL",
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_results_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_results(
            report_key="REPORT_001"
        )

    assert len(results) == 1
    assert results[0].report_key == "REPORT_001"


def test_list_lab_results_filtered_by_marker_key():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "REPORT_001",
            "Marker_Key": "LDL",
            "Numerical_Value": 110,
            "Text_Value": "",
            "Unit": "mg/dL",
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Report_Key": "REPORT_001",
            "Marker_Key": "HDL",
            "Numerical_Value": 50,
            "Text_Value": "",
            "Unit": "mg/dL",
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_results_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_results(
            marker_key="LDL"
        )

    assert len(results) == 1
    assert results[0].marker_key == "LDL"


def test_list_lab_results_filtered_by_report_and_marker():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "REPORT_001",
            "Marker_Key": "LDL",
            "Numerical_Value": 110,
            "Text_Value": "",
            "Unit": "mg/dL",
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Report_Key": "REPORT_002",
            "Marker_Key": "LDL",
            "Numerical_Value": 120,
            "Text_Value": "",
            "Unit": "mg/dL",
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_results_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_results(
            report_key="REPORT_001",
            marker_key="LDL",
        )

    assert len(results) == 1
    assert results[0].report_key == "REPORT_001"
    assert results[0].marker_key == "LDL"


def test_update_lab_result():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "OTHER_REPORT",
            "Marker_Key": "TEST_LDL",
        },
        {
            "Report_Key": "TEST_REPORT_001",
            "Marker_Key": "TEST_LDL",
        },
    ]

    lab_result = LabResult(
        report_key="THIS_REPORT_KEY_SHOULD_NOT_BE_SAVED",
        marker_key="THIS_MARKER_KEY_SHOULD_NOT_BE_SAVED",
        numerical_value=125,
        text_value="",
        unit="mmol/L",
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_results_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = update_lab_result(
            "TEST_REPORT_001",
            "TEST_LDL",
            lab_result,
        )

    assert result is not None

    worksheet.update.assert_called_once_with(
        range_name="C3:F3",
        values=[[
            125,
            "",
            "mmol/L",
            TEST_DATETIME,
        ]],
    )

    # Composite key is immutable.
    assert result.report_key == "TEST_REPORT_001"
    assert result.marker_key == "TEST_LDL"
    assert result.numerical_value == 125
    assert result.updated_datetime == TEST_DATETIME


def test_update_lab_result_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = []

    lab_result = LabResult(
        report_key="TEST_REPORT_001",
        marker_key="TEST_LDL",
        numerical_value=125,
        text_value="",
        unit="mg/dL",
    )

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_results_worksheet",
        return_value=worksheet,
    ):
        result = update_lab_result(
            "TEST_REPORT_001",
            "TEST_LDL",
            lab_result,
        )

    assert result is None
    worksheet.update.assert_not_called()