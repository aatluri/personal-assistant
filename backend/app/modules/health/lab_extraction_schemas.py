from pydantic import BaseModel


class ExtractedLabResult(BaseModel):
    """
    Represents a single lab result extracted from the uploaded PDF
    that was successfully mapped to one of our existing lab markers.

    This is temporary extraction data returned to the UI.
    It is NOT written directly to the Lab_Results worksheet.

    The user can review/edit the extracted value in the UI before
    the final save operation takes place.
    """
    marker_key: str
    reported_name: str
    numerical_value: float | None = None
    text_value: str = ""
    unit: str = ""


class UnmappedLabResult(BaseModel):
    """
    Represents a result that was successfully extracted from the PDF
    but could NOT be confidently mapped to an existing Marker_Key.

    Keeping unmapped results is important because we do not want the
    AI to guess or invent Marker_Keys just to force every result into
    our existing Lab_Marker_Definitions.

    These results can later be reviewed and, if appropriate, a new
    marker definition can be added to the system.
    """
    reported_name: str
    numerical_value: float | None = None
    text_value: str = ""
    unit: str = ""


class LabReportExtraction(BaseModel):
    """
    Represents the complete structured response produced after
    extracting an uploaded lab report PDF.

    The extraction contains two types of information:

    1. Report-level metadata
       - report date
       - collection date
       - laboratory name
       - etc.

    2. Individual lab results
       - successfully mapped results
       - unmapped results

    This model represents the output of the PDF extraction process.

    IMPORTANT:
    Creating this object does NOT save anything to Google Sheets.

    The API returns this object to the frontend, where the extracted
    information is used to populate the lab report screen. The user
    can then review/edit the information before saving it.
    """
    report_date: str
    collection_date: str = ""
    report_datetime: str = ""
    report_type: str = ""
    laboratory_name: str = ""
    file_name: str

    results: list[ExtractedLabResult]
    unmapped_results: list[UnmappedLabResult]