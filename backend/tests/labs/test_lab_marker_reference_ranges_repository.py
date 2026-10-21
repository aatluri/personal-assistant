from unittest.mock import MagicMock, patch

from app.modules.health.labs.lab_repository import (
    create_lab_marker_reference_range,
    get_lab_marker_reference_range,
    list_lab_marker_reference_ranges,
    update_lab_marker_reference_range,
)
from app.modules.health.labs.lab_schemas import LabMarkerReferenceRange


TEST_DATETIME = "2026-10-21 10:30:00"


def test_create_lab_marker_reference_range():
    worksheet = MagicMock()

    reference_range = LabMarkerReferenceRange(
        marker_key="TEST_LDL",
        gender="Male",
        min_age=18,
        max_age=65,
        lower_limit=0,
        upper_limit=130,
        unit="mg/dL",
        source="Repository Test",
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_marker_reference_ranges_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = create_lab_marker_reference_range(reference_range)

    worksheet.append_row.assert_called_once_with([
        "TEST_LDL",
        "Male",
        18,
        65,
        0,
        130,
        "mg/dL",
        "Repository Test",
        TEST_DATETIME,
    ])

    assert result.marker_key == "TEST_LDL"
    assert result.updated_datetime == TEST_DATETIME


def test_get_lab_marker_reference_range():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "TEST_LDL",
            "Gender": "Male",
            "Min_Age": 18,
            "Max_Age": 65,
            "Lower_Limit": 0,
            "Upper_Limit": 130,
            "Unit": "mg/dL",
            "Source": "Repository Test",
            "Updated_DateTime": TEST_DATETIME,
        }
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_reference_ranges_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_marker_reference_range(
            "TEST_LDL",
            "Male",
            18,
            65,
        )

    assert result is not None
    assert result.marker_key == "TEST_LDL"
    assert result.gender == "Male"
    assert result.min_age == 18
    assert result.max_age == 65
    assert result.lower_limit == 0
    assert result.upper_limit == 130
    assert result.unit == "mg/dL"
    assert result.source == "Repository Test"
    assert result.updated_datetime == TEST_DATETIME


def test_get_lab_marker_reference_range_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = []

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_reference_ranges_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_marker_reference_range(
            "MARKER_DOES_NOT_EXIST",
            "Male",
            18,
            65,
        )

    assert result is None


def test_list_lab_marker_reference_ranges():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "LDL",
            "Gender": "Male",
            "Min_Age": 18,
            "Max_Age": 65,
            "Lower_Limit": 0,
            "Upper_Limit": 130,
            "Unit": "mg/dL",
            "Source": "Test",
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Marker_Key": "HDL",
            "Gender": "Male",
            "Min_Age": 18,
            "Max_Age": 65,
            "Lower_Limit": 40,
            "Upper_Limit": "",
            "Unit": "mg/dL",
            "Source": "Test",
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_reference_ranges_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_marker_reference_ranges()

    assert len(results) == 2
    assert results[0].marker_key == "LDL"
    assert results[1].marker_key == "HDL"
    assert results[1].upper_limit is None


def test_list_lab_marker_reference_ranges_filtered_by_marker():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "LDL",
            "Gender": "Male",
            "Min_Age": 18,
            "Max_Age": 65,
            "Lower_Limit": 0,
            "Upper_Limit": 130,
            "Unit": "mg/dL",
            "Source": "Test",
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Marker_Key": "HDL",
            "Gender": "Male",
            "Min_Age": 18,
            "Max_Age": 65,
            "Lower_Limit": 40,
            "Upper_Limit": "",
            "Unit": "mg/dL",
            "Source": "Test",
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_reference_ranges_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_marker_reference_ranges("LDL")

    assert len(results) == 1
    assert results[0].marker_key == "LDL"


def test_reference_range_blank_numeric_values_become_none():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "TEST_OPTIONAL",
            "Gender": "All",
            "Min_Age": "",
            "Max_Age": "",
            "Lower_Limit": "",
            "Upper_Limit": "",
            "Unit": "mg/dL",
            "Source": "Test",
            "Updated_DateTime": TEST_DATETIME,
        }
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_reference_ranges_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_marker_reference_range(
            "TEST_OPTIONAL",
            "All",
            None,
            None,
        )

    assert result is not None
    assert result.min_age is None
    assert result.max_age is None
    assert result.lower_limit is None
    assert result.upper_limit is None


def test_update_lab_marker_reference_range():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "OTHER_MARKER",
            "Gender": "Male",
            "Min_Age": 18,
            "Max_Age": 65,
        },
        {
            "Marker_Key": "TEST_LDL",
            "Gender": "Male",
            "Min_Age": 18,
            "Max_Age": 65,
        },
    ]

    reference_range = LabMarkerReferenceRange(
        marker_key="THIS_KEY_SHOULD_NOT_BE_SAVED",
        gender="Female",
        min_age=20,
        max_age=70,
        lower_limit=10,
        upper_limit=120,
        unit="mmol/L",
        source="Updated Repository Test",
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_marker_reference_ranges_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = update_lab_marker_reference_range(
            "TEST_LDL",
            "Male",
            18,
            65,
            reference_range,
        )

    assert result is not None

    worksheet.update.assert_called_once_with(
        range_name="E3:I3",
        values=[[
            10,
            120,
            "mmol/L",
            "Updated Repository Test",
            TEST_DATETIME,
        ]],
    )

    # Composite key is immutable.
    assert result.marker_key == "TEST_LDL"
    assert result.gender == "Male"
    assert result.min_age == 18
    assert result.max_age == 65
    assert result.updated_datetime == TEST_DATETIME


def test_update_lab_marker_reference_range_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = []

    reference_range = LabMarkerReferenceRange(
        marker_key="TEST_LDL",
        gender="Male",
        min_age=18,
        max_age=65,
        lower_limit=10,
        upper_limit=120,
        unit="mg/dL",
        source="Test",
    )

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_reference_ranges_worksheet",
        return_value=worksheet,
    ):
        result = update_lab_marker_reference_range(
            "TEST_LDL",
            "Male",
            18,
            65,
            reference_range,
        )

    assert result is None
    worksheet.update.assert_not_called()