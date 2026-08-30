from pydantic import BaseModel

from app.modules.health.lab_schemas import (
    LabReport,
    LabResult,
)


class LabResultSave(BaseModel):
    """
    Represents a single lab marker value submitted by the UI
    as part of saving a lab report.

    report_key is intentionally not included because the backend
    generates the Report_Key when the report is saved.
    """

    # Existing Marker_Key from Lab_Marker_Definitions.
    marker_key: str

    # Numeric result, when applicable.
    numerical_value: float | None = None

    # Text result for non-numeric values such as
    # "Negative", "Nil", or "1 to 2".
    text_value: str = ""

    # Unit associated with the result.
    unit: str = ""


class LabReportSaveRequest(BaseModel):
    """
    Complete lab report submitted by the UI when the user
    clicks Save.

    Contains both report-level metadata and the marker values
    entered manually or populated through PDF extraction.
    """

    report_date: str
    collection_date: str = ""
    report_datetime: str = ""
    report_type: str = ""
    laboratory_name: str = ""
    file_name: str = ""
    notes: str = ""

    # The UI may send all marker fields.
    # Empty results will be ignored by the save service.
    results: list[LabResultSave]


class LabReportSaveResponse(BaseModel):
    """
    Represents the completed save operation.

    Returns the created Lab_Reports record together with
    the Lab_Results records that were actually saved.
    """

    report: LabReport
    results: list[LabResult]