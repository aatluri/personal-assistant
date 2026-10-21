from unittest.mock import MagicMock, patch

from app.modules.health.labs.lab_repository import (
    create_lab_report,
    get_lab_report,
    list_lab_reports,
    update_lab_report,
)
from app.modules.health.labs.lab_schemas import LabReport


TEST_DATETIME = "2026-10-21 10:30:00"


def test_create_lab_report():
    worksheet = MagicMock()

    report = LabReport(
        report_key="TEST_REPORT_001",
        report_date="2026-08-28",
        collection_date="2026-08-28",
        report_datetime="2026-08-28 09:30:00",
        report_type="Blood Work",
        laboratory_name="Test Laboratory",
        file_name="test_report.pdf",
        notes="Repository test",
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_reports_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = create_lab_report(report)

    worksheet.append_row.assert_called_once_with([
        "TEST_REPORT_001",
        "2026-08-28",
        "2026-08-28",
        "2026-08-28 09:30:00",
        "Blood Work",
        "Test Laboratory",
        "test_report.pdf",
        "Repository test",
        TEST_DATETIME,
    ])

    assert result.report_key == "TEST_REPORT_001"
    assert result.updated_datetime == TEST_DATETIME


def test_get_lab_report():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "TEST_REPORT_001",
            "Report_Date": "2026-08-28",
            "Collection_Date": "2026-08-28",
            "Report_DateTime": "2026-08-28 09:30:00",
            "Report_Type": "Blood Work",
            "Laboratory_Name": "Test Laboratory",
            "File_Name": "test_report.pdf",
            "Notes": "Repository test",
            "Updated_DateTime": TEST_DATETIME,
        }
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_reports_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_report("TEST_REPORT_001")

    assert result is not None
    assert result.report_key == "TEST_REPORT_001"
    assert str(result.report_date) == "2026-08-28"
    assert str(result.collection_date) == "2026-08-28"
    assert result.report_type == "Blood Work"
    assert result.laboratory_name == "Test Laboratory"
    assert result.file_name == "test_report.pdf"
    assert result.notes == "Repository test"
    assert result.updated_datetime == TEST_DATETIME


def test_get_lab_report_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = []

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_reports_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_report(
            "REPORT_DOES_NOT_EXIST"
        )

    assert result is None


def test_list_lab_reports():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "REPORT_001",
            "Report_Date": "2026-08-28",
            "Collection_Date": "2026-08-28",
            "Report_DateTime": "2026-08-28 09:30:00",
            "Report_Type": "Blood Work",
            "Laboratory_Name": "Laboratory A",
            "File_Name": "report_1.pdf",
            "Notes": "First report",
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Report_Key": "REPORT_002",
            "Report_Date": "2026-09-15",
            "Collection_Date": "2026-09-15",
            "Report_DateTime": "2026-09-15 08:00:00",
            "Report_Type": "Blood Work",
            "Laboratory_Name": "Laboratory B",
            "File_Name": "report_2.pdf",
            "Notes": "Second report",
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_reports_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_reports()

    assert len(results) == 2

    assert results[0].report_key == "REPORT_001"
    assert results[0].laboratory_name == "Laboratory A"

    assert results[1].report_key == "REPORT_002"
    assert results[1].laboratory_name == "Laboratory B"


def test_update_lab_report():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "OTHER_REPORT",
        },
        {
            "Report_Key": "TEST_REPORT_001",
        },
    ]

    report = LabReport(
        report_key="THIS_KEY_SHOULD_NOT_BE_SAVED",
        report_date="2026-09-01",
        collection_date="2026-09-01",
        report_datetime="2026-09-01 10:00:00",
        report_type="Updated Blood Work",
        laboratory_name="Updated Laboratory",
        file_name="updated_report.pdf",
        notes="Updated repository test",
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_reports_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = update_lab_report(
            "TEST_REPORT_001",
            report,
        )

    assert result is not None

    # TEST_REPORT_001 is the second data row.
    # Row 1 contains headers, so it is Google Sheets row 3.
    worksheet.update.assert_called_once_with(
        range_name="B3:I3",
        values=[[
            "2026-09-01",
            "2026-09-01",
            "2026-09-01 10:00:00",
            "Updated Blood Work",
            "Updated Laboratory",
            "updated_report.pdf",
            "Updated repository test",
            TEST_DATETIME,
        ]],
    )

    # Report_Key is immutable.
    assert result.report_key == "TEST_REPORT_001"
    assert result.report_type == "Updated Blood Work"
    assert result.laboratory_name == "Updated Laboratory"
    assert result.updated_datetime == TEST_DATETIME


def test_update_lab_report_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Report_Key": "OTHER_REPORT",
        }
    ]

    report = LabReport(
        report_key="TEST_REPORT_001",
        report_date="2026-08-28",
        collection_date="2026-08-28",
        report_datetime="2026-08-28 09:30:00",
        report_type="Blood Work",
        laboratory_name="Test Laboratory",
        file_name="test_report.pdf",
        notes="Repository test",
    )

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_reports_worksheet",
        return_value=worksheet,
    ):
        result = update_lab_report(
            "TEST_REPORT_001",
            report,
        )

    assert result is None
    worksheet.update.assert_not_called()