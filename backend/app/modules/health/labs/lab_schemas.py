from pydantic import BaseModel

# ---------------------------------------------------------
# Lab Report Create - This is what the UI sends.
# ---------------------------------------------------------

class LabReportCreate(BaseModel):
    report_date: str
    collection_date: str
    report_datetime: str
    report_type: str
    laboratory_name: str
    file_name: str
    notes: str = ""


# ---------------------------------------------------------
# Lab Reports - This is once we create the report key
# ---------------------------------------------------------

class LabReport(BaseModel):
    report_key: str
    report_date: str
    collection_date: str
    report_datetime: str
    report_type: str
    laboratory_name: str
    file_name: str
    notes: str = ""

    # System-generated timestamp indicating when this record
    # was most recently created or updated by the backend.
    updated_datetime: str = ""


# ---------------------------------------------------------
# Lab Marker Definitions
# ---------------------------------------------------------

class LabMarkerDefinition(BaseModel):
    marker_key: str                         # Primary Key
    display_name: str
    category: str
    panel: str
    sample_type: str
    value_type: str
    default_unit: str
    is_active: bool

    # Backend-generated timestamp for the most recent change
    # made to this marker definition.
    updated_datetime: str = ""


# ---------------------------------------------------------
# Lab Marker Reference Ranges
# ---------------------------------------------------------

class LabMarkerReferenceRange(BaseModel):
    marker_key: str                         # Primary Key
    gender: str = ""                        # Primary Key
    min_age: int | None = None              # Primary Key
    max_age: int | None = None              # Primary Key
    lower_limit: float | None = None
    upper_limit: float | None = None
    unit: str
    source: str

    # Backend-generated timestamp for the most recent change
    # made to this reference range.
    updated_datetime: str = ""


# ---------------------------------------------------------
# Lab Marker Interpretations
# ---------------------------------------------------------

class LabMarkerInterpretation(BaseModel):
    marker_key: str                         # Primary Key
    label: str                              # Primary Key
    lower_limit: float | None = None
    upper_limit: float | None = None

    # Backend-generated timestamp for the most recent change
    # made to this interpretation.
    updated_datetime: str = ""


# ---------------------------------------------------------
# Lab Results
# ---------------------------------------------------------

class LabResult(BaseModel):
    report_key: str                         # Primary Key
    marker_key: str                         # Primary Key
    numerical_value: float | None = None
    text_value: str = ""
    unit: str = ""

    # Backend-generated timestamp indicating when this result
    # was most recently created or updated.
    updated_datetime: str = ""