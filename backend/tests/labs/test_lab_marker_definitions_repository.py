from unittest.mock import MagicMock, patch

from app.modules.health.labs.lab_repository import (
    create_lab_marker_definition,
    get_lab_marker_definition,
    list_lab_marker_definitions,
    update_lab_marker_definition,
)
from app.modules.health.labs.lab_schemas import LabMarkerDefinition


TEST_DATETIME = "2026-10-21 10:30:00"


def test_create_lab_marker_definition():
    worksheet = MagicMock()

    definition = LabMarkerDefinition(
        marker_key="TEST_LDL",
        display_name="Test LDL Cholesterol",
        category="Cardiovascular",
        panel="Lipid Profile",
        sample_type="Serum",
        value_type="Numeric",
        default_unit="mg/dL",
        is_active=True,
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_marker_definitions_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = create_lab_marker_definition(definition)

    worksheet.append_row.assert_called_once_with([
        "TEST_LDL",
        "Test LDL Cholesterol",
        "Cardiovascular",
        "Lipid Profile",
        "Serum",
        "Numeric",
        "mg/dL",
        True,
        TEST_DATETIME,
    ])

    assert result.marker_key == "TEST_LDL"
    assert result.updated_datetime == TEST_DATETIME


def test_get_lab_marker_definition():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "TEST_LDL",
            "DisplayName": "Test LDL Cholesterol",
            "Category": "Cardiovascular",
            "Panel": "Lipid Profile",
            "Sample_Type": "Serum",
            "ValueType": "Numeric",
            "Default_Unit": "mg/dL",
            "Is_Active": True,
            "Updated_DateTime": TEST_DATETIME,
        }
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_definitions_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_marker_definition("TEST_LDL")

    assert result is not None
    assert result.marker_key == "TEST_LDL"
    assert result.display_name == "Test LDL Cholesterol"
    assert result.category == "Cardiovascular"
    assert result.panel == "Lipid Profile"
    assert result.sample_type == "Serum"
    assert result.value_type == "Numeric"
    assert result.default_unit == "mg/dL"
    assert result.is_active is True
    assert result.updated_datetime == TEST_DATETIME


def test_get_lab_marker_definition_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = []

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_definitions_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_marker_definition(
            "MARKER_DOES_NOT_EXIST"
        )

    assert result is None


def test_list_lab_marker_definitions():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "LDL_CHOLESTEROL",
            "DisplayName": "LDL Cholesterol",
            "Category": "Cardiovascular",
            "Panel": "Lipid Profile",
            "Sample_Type": "Serum",
            "ValueType": "Numeric",
            "Default_Unit": "mg/dL",
            "Is_Active": True,
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Marker_Key": "HDL_CHOLESTEROL",
            "DisplayName": "HDL Cholesterol",
            "Category": "Cardiovascular",
            "Panel": "Lipid Profile",
            "Sample_Type": "Serum",
            "ValueType": "Numeric",
            "Default_Unit": "mg/dL",
            "Is_Active": True,
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_definitions_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_marker_definitions()

    assert len(results) == 2
    assert results[0].marker_key == "LDL_CHOLESTEROL"
    assert results[1].marker_key == "HDL_CHOLESTEROL"


def test_update_lab_marker_definition():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "OTHER_MARKER",
        },
        {
            "Marker_Key": "TEST_LDL",
        },
    ]

    definition = LabMarkerDefinition(
        marker_key="THIS_KEY_SHOULD_NOT_BE_SAVED",
        display_name="Updated LDL Cholesterol",
        category="Updated Cardiovascular",
        panel="Updated Lipid Profile",
        sample_type="Plasma",
        value_type="Numeric",
        default_unit="mmol/L",
        is_active=False,
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_marker_definitions_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = update_lab_marker_definition(
            "TEST_LDL",
            definition,
        )

    assert result is not None

    # The matching record is the second data row.
    # Google Sheets row 1 is the header, so this is row 3.
    worksheet.update.assert_called_once_with(
        range_name="B3:I3",
        values=[[
            "Updated LDL Cholesterol",
            "Updated Cardiovascular",
            "Updated Lipid Profile",
            "Plasma",
            "Numeric",
            "mmol/L",
            False,
            TEST_DATETIME,
        ]],
    )

    # Marker_Key is immutable.
    assert result.marker_key == "TEST_LDL"
    assert result.display_name == "Updated LDL Cholesterol"
    assert result.updated_datetime == TEST_DATETIME


def test_update_lab_marker_definition_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "OTHER_MARKER",
        }
    ]

    definition = LabMarkerDefinition(
        marker_key="TEST_LDL",
        display_name="Test LDL",
        category="Cardiovascular",
        panel="Lipid Profile",
        sample_type="Serum",
        value_type="Numeric",
        default_unit="mg/dL",
        is_active=True,
    )

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_definitions_worksheet",
        return_value=worksheet,
    ):
        result = update_lab_marker_definition(
            "TEST_LDL",
            definition,
        )

    assert result is None
    worksheet.update.assert_not_called()