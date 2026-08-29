from app.config import settings
from app.database.sheets_client import get_sheets_client
from app.modules.health.lab_schemas import (
    LabReport,
    LabMarkerDefinition,
    LabMarkerReferenceRange,
    LabMarkerInterpretation,
    LabResult,
)


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def get_lab_reports_worksheet():
    client = get_sheets_client()

    spreadsheet = client.open_by_key(
        settings.GOOGLE_SHEETS_SPREADSHEET_ID
    )

    return spreadsheet.worksheet(
        settings.LAB_REPORTS_WORKSHEET
    )

# =========================================================
# LAB REPORT
# =========================================================

# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

def create_lab_report(report: LabReport) -> LabReport:
    worksheet = get_lab_reports_worksheet()

    worksheet.append_row([
        report.report_key,
        report.report_date,
        report.collection_date,
        report.report_datetime,
        report.report_type,
        report.laboratory_name,
        report.file_name,
        report.notes,
    ])

    return report


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

def get_lab_report(report_key: str) -> LabReport | None:
    worksheet = get_lab_reports_worksheet()

    records = worksheet.get_all_records()

    for record in records:
        if record["Report_Key"] == report_key:
            return LabReport(
                report_key=record["Report_Key"],
                report_date=record["Report_Date"],
                collection_date=record["Collection_Date"],
                report_datetime=record["Report_DateTime"],
                report_type=record["Report_Type"],
                laboratory_name=record["Laboratory_Name"],
                file_name=record["File_Name"],
                notes=record["Notes"],
            )

    return None


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

def list_lab_reports() -> list[LabReport]:
    worksheet = get_lab_reports_worksheet()

    records = worksheet.get_all_records()

    reports = []

    for record in records:
        reports.append(
            LabReport(
                report_key=record["Report_Key"],
                report_date=record["Report_Date"],
                collection_date=record["Collection_Date"],
                report_datetime=record["Report_DateTime"],
                report_type=record["Report_Type"],
                laboratory_name=record["Laboratory_Name"],
                file_name=record["File_Name"],
                notes=record["Notes"],
            )
        )

    return reports


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

def update_lab_report(
    report_key: str,
    report: LabReport,
) -> LabReport | None:

    worksheet = get_lab_reports_worksheet()

    records = worksheet.get_all_records()

    for index, record in enumerate(records, start=2):

        if record["Report_Key"] == report_key:

            worksheet.update(
                range_name=f"B{index}:H{index}",
                values=[[
                    report.report_date,
                    report.collection_date,
                    report.report_datetime,
                    report.report_type,
                    report.laboratory_name,
                    report.file_name,
                    report.notes,
                ]],
            )

            # Return the report using the original Report_Key
            return report.model_copy(
                update={"report_key": report_key}
            )

    return None

# =========================================================
# LAB MARKER DEFINITIONS
# =========================================================


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def get_lab_marker_definitions_worksheet():
    client = get_sheets_client()

    spreadsheet = client.open_by_key(
        settings.GOOGLE_SHEETS_SPREADSHEET_ID
    )

    return spreadsheet.worksheet(
        settings.LAB_MARKER_DEFINITIONS_WORKSHEET
    )


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

def create_lab_marker_definition(
    definition: LabMarkerDefinition,
) -> LabMarkerDefinition:

    worksheet = get_lab_marker_definitions_worksheet()

    worksheet.append_row([
        definition.marker_key,
        definition.display_name,
        definition.category,
        definition.panel,
        definition.sample_type,
        definition.value_type,
        definition.default_unit,
        definition.is_active,
    ])

    return definition


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

def get_lab_marker_definition(
    marker_key: str,
) -> LabMarkerDefinition | None:

    worksheet = get_lab_marker_definitions_worksheet()

    records = worksheet.get_all_records()

    for record in records:

        if record["Marker_Key"] == marker_key:

            return LabMarkerDefinition(
                marker_key=record["Marker_Key"],
                display_name=record["DisplayName"],
                category=record["Category"],
                panel=record["Panel"],
                sample_type=record["Sample_Type"],
                value_type=record["ValueType"],
                default_unit=record["Default_Unit"],
                is_active=record["Is_Active"],
            )

    return None


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

def list_lab_marker_definitions() -> list[LabMarkerDefinition]:

    worksheet = get_lab_marker_definitions_worksheet()

    records = worksheet.get_all_records()

    definitions = []

    for record in records:

        definitions.append(
            LabMarkerDefinition(
                marker_key=record["Marker_Key"],
                display_name=record["DisplayName"],
                category=record["Category"],
                panel=record["Panel"],
                sample_type=record["Sample_Type"],
                value_type=record["ValueType"],
                default_unit=record["Default_Unit"],
                is_active=record["Is_Active"],
            )
        )

    return definitions


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

def update_lab_marker_definition(
    marker_key: str,
    definition: LabMarkerDefinition,
) -> LabMarkerDefinition | None:

    worksheet = get_lab_marker_definitions_worksheet()

    records = worksheet.get_all_records()

    for index, record in enumerate(records, start=2):

        if record["Marker_Key"] == marker_key:

            worksheet.update(
                range_name=f"B{index}:H{index}",
                values=[[
                    definition.display_name,
                    definition.category,
                    definition.panel,
                    definition.sample_type,
                    definition.value_type,
                    definition.default_unit,
                    definition.is_active,
                ]],
            )

            return definition.model_copy(
                update={"marker_key": marker_key}
            )

    return None

# =========================================================
# LAB MARKER REFERENCE RANGES
# =========================================================


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def get_lab_marker_reference_ranges_worksheet():
    client = get_sheets_client()

    spreadsheet = client.open_by_key(
        settings.GOOGLE_SHEETS_SPREADSHEET_ID
    )

    return spreadsheet.worksheet(
        settings.LAB_MARKER_REFERENCE_RANGES_WORKSHEET
    )


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

def create_lab_marker_reference_range(
    reference_range: LabMarkerReferenceRange,
) -> LabMarkerReferenceRange:

    worksheet = get_lab_marker_reference_ranges_worksheet()

    worksheet.append_row([
        reference_range.marker_key,
        reference_range.gender,
        reference_range.min_age,
        reference_range.max_age,
        reference_range.lower_limit,
        reference_range.upper_limit,
        reference_range.unit,
        reference_range.source,
    ])

    return reference_range


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

def get_lab_marker_reference_range(
    marker_key: str,
    gender: str,
    min_age: int | None,
    max_age: int | None,
) -> LabMarkerReferenceRange | None:

    worksheet = get_lab_marker_reference_ranges_worksheet()

    records = worksheet.get_all_records()

    for record in records:

        if (
            record["Marker_Key"] == marker_key
            and record["Gender"] == gender
            and _optional_int(record["Min_Age"]) == min_age
            and _optional_int(record["Max_Age"]) == max_age
        ):
            return LabMarkerReferenceRange(
                marker_key=record["Marker_Key"],
                gender=record["Gender"],
                min_age=_optional_int(record["Min_Age"]),
                max_age=_optional_int(record["Max_Age"]),
                lower_limit=_optional_float(record["Lower_Limit"]),
                upper_limit=_optional_float(record["Upper_Limit"]),
                unit=record["Unit"],
                source=record["Source"],
            )

    return None


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

def list_lab_marker_reference_ranges(
    marker_key: str | None = None,
) -> list[LabMarkerReferenceRange]:

    worksheet = get_lab_marker_reference_ranges_worksheet()

    records = worksheet.get_all_records()

    reference_ranges = []

    for record in records:

        # If a Marker_Key was supplied, only return
        # reference ranges belonging to that marker.
        if (
            marker_key is not None
            and record["Marker_Key"] != marker_key
        ):
            continue

        reference_ranges.append(
            LabMarkerReferenceRange(
                marker_key=record["Marker_Key"],
                gender=record["Gender"],
                min_age=_optional_int(record["Min_Age"]),
                max_age=_optional_int(record["Max_Age"]),
                lower_limit=_optional_float(record["Lower_Limit"]),
                upper_limit=_optional_float(record["Upper_Limit"]),
                unit=record["Unit"],
                source=record["Source"],
            )
        )

    return reference_ranges


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

def update_lab_marker_reference_range(
    marker_key: str,
    gender: str,
    min_age: int | None,
    max_age: int | None,
    reference_range: LabMarkerReferenceRange,
) -> LabMarkerReferenceRange | None:

    worksheet = get_lab_marker_reference_ranges_worksheet()

    records = worksheet.get_all_records()

    for index, record in enumerate(records, start=2):

        if (
            record["Marker_Key"] == marker_key
            and record["Gender"] == gender
            and _optional_int(record["Min_Age"]) == min_age
            and _optional_int(record["Max_Age"]) == max_age
        ):

            # Only update Lower_Limit, Upper_Limit, Unit and Source.
            # The fields making up the unique key are immutable.
            worksheet.update(
                range_name=f"E{index}:H{index}",
                values=[[
                    reference_range.lower_limit,
                    reference_range.upper_limit,
                    reference_range.unit,
                    reference_range.source,
                ]],
            )

            return reference_range.model_copy(
                update={
                    "marker_key": marker_key,
                    "gender": gender,
                    "min_age": min_age,
                    "max_age": max_age,
                }
            )

    return None


# ---------------------------------------------------------
# Conversion Helpers
# _optional_int() and _optional_float() are necessary because Google Sheets returns blank cells as "",
# while our Pydantic model expects None for missing numeric values.
# ---------------------------------------------------------

def _optional_int(value) -> int | None:

    if value == "" or value is None:
        return None

    return int(value)


def _optional_float(value) -> float | None:

    if value == "" or value is None:
        return None

    return float(value)

# =========================================================
# LAB MARKER INTERPRETATIONS
# =========================================================


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def get_lab_marker_interpretations_worksheet():
    client = get_sheets_client()

    spreadsheet = client.open_by_key(
        settings.GOOGLE_SHEETS_SPREADSHEET_ID
    )

    return spreadsheet.worksheet(
        settings.LAB_MARKER_INTERPRETATIONS_WORKSHEET
    )


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

def create_lab_marker_interpretation(
    interpretation: LabMarkerInterpretation,
) -> LabMarkerInterpretation:

    worksheet = get_lab_marker_interpretations_worksheet()

    worksheet.append_row([
        interpretation.marker_key,
        interpretation.label,
        interpretation.lower_limit,
        interpretation.upper_limit,
    ])

    return interpretation


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

def get_lab_marker_interpretation(
    marker_key: str,
    label: str,
) -> LabMarkerInterpretation | None:

    worksheet = get_lab_marker_interpretations_worksheet()

    records = worksheet.get_all_records()

    for record in records:

        if (
            record["Marker_Key"] == marker_key
            and record["Label"] == label
        ):
            return LabMarkerInterpretation(
                marker_key=record["Marker_Key"],
                label=record["Label"],
                lower_limit=_optional_float(
                    record["Lower_Limit"]
                ),
                upper_limit=_optional_float(
                    record["Upper_Limit"]
                ),
            )

    return None


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

def list_lab_marker_interpretations(
    marker_key: str | None = None,
) -> list[LabMarkerInterpretation]:

    worksheet = get_lab_marker_interpretations_worksheet()

    records = worksheet.get_all_records()

    interpretations = []

    for record in records:

        # If Marker_Key was supplied, only return
        # interpretations belonging to that marker.
        if (
            marker_key is not None
            and record["Marker_Key"] != marker_key
        ):
            continue

        interpretations.append(
            LabMarkerInterpretation(
                marker_key=record["Marker_Key"],
                label=record["Label"],
                lower_limit=_optional_float(
                    record["Lower_Limit"]
                ),
                upper_limit=_optional_float(
                    record["Upper_Limit"]
                ),
            )
        )

    return interpretations


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

def update_lab_marker_interpretation(
    marker_key: str,
    label: str,
    interpretation: LabMarkerInterpretation,
) -> LabMarkerInterpretation | None:

    worksheet = get_lab_marker_interpretations_worksheet()

    records = worksheet.get_all_records()

    for index, record in enumerate(records, start=2):

        if (
            record["Marker_Key"] == marker_key
            and record["Label"] == label
        ):

            # Marker_Key and Label form the unique key.
            # Therefore only the limits can be updated.
            worksheet.update(
                range_name=f"C{index}:D{index}",
                values=[[
                    interpretation.lower_limit,
                    interpretation.upper_limit,
                ]],
            )

            return interpretation.model_copy(
                update={
                    "marker_key": marker_key,
                    "label": label,
                }
            )

    return None


# =========================================================
# LAB RESULTS
# =========================================================


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def get_lab_results_worksheet():
    client = get_sheets_client()

    spreadsheet = client.open_by_key(
        settings.GOOGLE_SHEETS_SPREADSHEET_ID
    )

    return spreadsheet.worksheet(
        settings.LAB_RESULTS_WORKSHEET
    )


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

def create_lab_result(
    result: LabResult,
) -> LabResult:

    worksheet = get_lab_results_worksheet()

    worksheet.append_row([
        result.report_key,
        result.marker_key,
        result.numerical_value,
        result.text_value,
        result.unit,
    ])

    return result


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

def get_lab_result(
    report_key: str,
    marker_key: str,
) -> LabResult | None:

    worksheet = get_lab_results_worksheet()

    records = worksheet.get_all_records()

    for record in records:

        if (
            record["Report_Key"] == report_key
            and record["Marker_Key"] == marker_key
        ):
            return LabResult(
                report_key=record["Report_Key"],
                marker_key=record["Marker_Key"],
                numerical_value=_optional_float(
                    record["Numerical_Value"]
                ),
                text_value=record["Text_Value"],
                unit=record["Unit"],
            )

    return None


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

def list_lab_results(
    report_key: str | None = None,
    marker_key: str | None = None,
) -> list[LabResult]:

    worksheet = get_lab_results_worksheet()

    records = worksheet.get_all_records()

    results = []

    for record in records:

        # Filter by Report_Key if supplied.
        if (
            report_key is not None
            and record["Report_Key"] != report_key
        ):
            continue

        # Filter by Marker_Key if supplied.
        if (
            marker_key is not None
            and record["Marker_Key"] != marker_key
        ):
            continue

        results.append(
            LabResult(
                report_key=record["Report_Key"],
                marker_key=record["Marker_Key"],
                numerical_value=_optional_float(
                    record["Numerical_Value"]
                ),
                text_value=record["Text_Value"],
                unit=record["Unit"],
            )
        )

    return results


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

def update_lab_result(
    report_key: str,
    marker_key: str,
    result: LabResult,
) -> LabResult | None:

    worksheet = get_lab_results_worksheet()

    records = worksheet.get_all_records()

    for index, record in enumerate(records, start=2):

        if (
            record["Report_Key"] == report_key
            and record["Marker_Key"] == marker_key
        ):

            # Report_Key and Marker_Key form the unique key.
            # Therefore only the result values and unit
            # can be updated.
            worksheet.update(
                range_name=f"C{index}:E{index}",
                values=[[
                    result.numerical_value,
                    result.text_value,
                    result.unit,
                ]],
            )

            return result.model_copy(
                update={
                    "report_key": report_key,
                    "marker_key": marker_key,
                }
            )

    return None