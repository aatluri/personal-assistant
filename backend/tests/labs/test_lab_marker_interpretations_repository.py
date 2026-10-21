from unittest.mock import MagicMock, patch

from app.modules.health.labs.lab_repository import (
    create_lab_marker_interpretation,
    get_lab_marker_interpretation,
    list_lab_marker_interpretations,
    update_lab_marker_interpretation,
)
from app.modules.health.labs.lab_schemas import LabMarkerInterpretation


TEST_DATETIME = "2026-10-21 10:30:00"


def test_create_lab_marker_interpretation():
    worksheet = MagicMock()

    interpretation = LabMarkerInterpretation(
        marker_key="TEST_LDL",
        label="Optimal",
        lower_limit=0,
        upper_limit=100,
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_marker_interpretations_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = create_lab_marker_interpretation(interpretation)

    worksheet.append_row.assert_called_once_with([
        "TEST_LDL",
        "Optimal",
        0,
        100,
        TEST_DATETIME,
    ])

    assert result.marker_key == "TEST_LDL"
    assert result.label == "Optimal"
    assert result.updated_datetime == TEST_DATETIME


def test_get_lab_marker_interpretation():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "TEST_LDL",
            "Label": "Optimal",
            "Lower_Limit": 0,
            "Upper_Limit": 100,
            "Updated_DateTime": TEST_DATETIME,
        }
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_interpretations_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_marker_interpretation(
            "TEST_LDL",
            "Optimal",
        )

    assert result is not None
    assert result.marker_key == "TEST_LDL"
    assert result.label == "Optimal"
    assert result.lower_limit == 0
    assert result.upper_limit == 100
    assert result.updated_datetime == TEST_DATETIME


def test_get_lab_marker_interpretation_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = []

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_interpretations_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_marker_interpretation(
            "MARKER_DOES_NOT_EXIST",
            "LABEL_DOES_NOT_EXIST",
        )

    assert result is None


def test_list_lab_marker_interpretations():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "LDL",
            "Label": "Optimal",
            "Lower_Limit": 0,
            "Upper_Limit": 100,
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Marker_Key": "LDL",
            "Label": "High",
            "Lower_Limit": 160,
            "Upper_Limit": "",
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_interpretations_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_marker_interpretations()

    assert len(results) == 2
    assert results[0].label == "Optimal"
    assert results[1].label == "High"
    assert results[1].upper_limit is None


def test_list_lab_marker_interpretations_filtered_by_marker():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "LDL",
            "Label": "Optimal",
            "Lower_Limit": 0,
            "Upper_Limit": 100,
            "Updated_DateTime": TEST_DATETIME,
        },
        {
            "Marker_Key": "HDL",
            "Label": "Low",
            "Lower_Limit": "",
            "Upper_Limit": 40,
            "Updated_DateTime": TEST_DATETIME,
        },
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_interpretations_worksheet",
        return_value=worksheet,
    ):
        results = list_lab_marker_interpretations("LDL")

    assert len(results) == 1
    assert results[0].marker_key == "LDL"
    assert results[0].label == "Optimal"


def test_interpretation_blank_limits_become_none():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "TEST_MARKER",
            "Label": "Detected",
            "Lower_Limit": "",
            "Upper_Limit": "",
            "Updated_DateTime": TEST_DATETIME,
        }
    ]

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_interpretations_worksheet",
        return_value=worksheet,
    ):
        result = get_lab_marker_interpretation(
            "TEST_MARKER",
            "Detected",
        )

    assert result is not None
    assert result.lower_limit is None
    assert result.upper_limit is None


def test_update_lab_marker_interpretation():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = [
        {
            "Marker_Key": "OTHER_MARKER",
            "Label": "Optimal",
        },
        {
            "Marker_Key": "TEST_LDL",
            "Label": "Optimal",
        },
    ]

    interpretation = LabMarkerInterpretation(
        marker_key="THIS_KEY_SHOULD_NOT_BE_SAVED",
        label="THIS_LABEL_SHOULD_NOT_BE_SAVED",
        lower_limit=10,
        upper_limit=90,
    )

    with (
        patch(
            "app.modules.health.labs.lab_repository."
            "get_lab_marker_interpretations_worksheet",
            return_value=worksheet,
        ),
        patch(
            "app.modules.health.labs.lab_repository."
            "get_current_datetime",
            return_value=TEST_DATETIME,
        ),
    ):
        result = update_lab_marker_interpretation(
            "TEST_LDL",
            "Optimal",
            interpretation,
        )

    assert result is not None

    worksheet.update.assert_called_once_with(
        range_name="C3:E3",
        values=[[
            10,
            90,
            TEST_DATETIME,
        ]],
    )

    # Composite key is immutable.
    assert result.marker_key == "TEST_LDL"
    assert result.label == "Optimal"
    assert result.updated_datetime == TEST_DATETIME


def test_update_lab_marker_interpretation_not_found():
    worksheet = MagicMock()

    worksheet.get_all_records.return_value = []

    interpretation = LabMarkerInterpretation(
        marker_key="TEST_LDL",
        label="Optimal",
        lower_limit=10,
        upper_limit=90,
    )

    with patch(
        "app.modules.health.labs.lab_repository."
        "get_lab_marker_interpretations_worksheet",
        return_value=worksheet,
    ):
        result = update_lab_marker_interpretation(
            "TEST_LDL",
            "Optimal",
            interpretation,
        )

    assert result is None
    worksheet.update.assert_not_called()