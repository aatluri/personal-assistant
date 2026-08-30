import hashlib

from app.modules.health.lab_schemas import (
    LabReport,
    LabReportCreate,
    LabResult,
)

from app.modules.health.lab_repository import (
    create_lab_report,
    get_lab_report,
    update_lab_report,
    create_lab_result,
    get_lab_result,
    update_lab_result,
)

from app.modules.health.lab_save_schemas import (
    LabReportSaveRequest,
    LabReportSaveResponse,
)


# ---------------------------------------------------------
# Generate Report Key
# ---------------------------------------------------------

def generate_report_key(
    report_date: str,
    file_name: str,
) -> str:
    """
    Generate a deterministic Report_Key using:

    - Report Date
    - SHA-256 hash of the filename

    Example:
        LAB_20250602_4d71c9a83f12
    """

    # Generate SHA-256 hash from the filename.
    file_hash = hashlib.sha256(
        file_name.encode("utf-8")
    ).hexdigest()[:12]

    # Convert 2025-06-02 -> 20250602.
    formatted_date = report_date.replace("-", "")

    return f"LAB_{formatted_date}_{file_hash}"


# ---------------------------------------------------------
# Create Lab Report
# ---------------------------------------------------------

def create_lab_report_record(
    report_data: LabReportCreate,
) -> LabReport:
    """
    Generate the Report_Key and calls the repository method to create the Lab Report.
    """

    report_key = generate_report_key(
        report_data.report_date,
        report_data.file_name,
    )

    report = LabReport(
        report_key=report_key,
        report_date=report_data.report_date,
        collection_date=report_data.collection_date,
        report_datetime=report_data.report_datetime,
        report_type=report_data.report_type,
        laboratory_name=report_data.laboratory_name,
        file_name=report_data.file_name,
        notes=report_data.notes,
    )

    return create_lab_report(report)



def save_lab_report(
    save_request: LabReportSaveRequest,
) -> LabReportSaveResponse:
    """
    Save a complete lab report and its non-empty marker results.

    This operation uses upsert behavior so that it is safe to retry
    if a previous save failed partway through.

    Flow:
    1. Generate the Report_Key.
    2. Create the Lab_Report if it does not exist.
       Otherwise, update the existing Lab_Report.
    3. Ignore empty marker values.
    4. For every non-empty marker:
       - Create the Lab_Result if it does not exist.
       - Update the Lab_Result if it already exists.
    5. Return the saved report and saved results.
    """

    # ---------------------------------------------------------
    # 1. Generate the Report_Key
    # ---------------------------------------------------------

    report_key = generate_report_key(
        save_request.report_date,
        save_request.file_name,
    )

    # ---------------------------------------------------------
    # 2. Build the Lab_Report record
    # ---------------------------------------------------------

    report = LabReport(
        report_key=report_key,
        report_date=save_request.report_date,
        collection_date=save_request.collection_date,
        report_datetime=save_request.report_datetime,
        report_type=save_request.report_type,
        laboratory_name=save_request.laboratory_name,
        file_name=save_request.file_name,
        notes=save_request.notes,
    )

    # ---------------------------------------------------------
    # 3. Upsert the Lab_Report
    # ---------------------------------------------------------

    existing_report = get_lab_report(
        report_key
    )

    if existing_report is None:
        saved_report = create_lab_report(
            report
        )
    else:
        saved_report = update_lab_report(
            report_key,
            report,
        )

    # ---------------------------------------------------------
    # 4. Save only non-empty marker results
    # ---------------------------------------------------------

    saved_results: list[LabResult] = []

    for result in save_request.results:

        # A result is considered empty when it has:
        # - no numerical value
        # - no meaningful text value
        #
        # Empty results are ignored and are not written
        # to Lab_Results.
        if (
            result.numerical_value is None
            and not result.text_value.strip()
        ):
            continue

        lab_result = LabResult(
            report_key=report_key,
            marker_key=result.marker_key,
            numerical_value=result.numerical_value,
            text_value=result.text_value,
            unit=result.unit,
        )

        # -----------------------------------------------------
        # 5. Upsert the Lab_Result
        # -----------------------------------------------------

        existing_result = get_lab_result(
            report_key,
            result.marker_key,
        )

        if existing_result is None:
            saved_result = create_lab_result(
                lab_result
            )
        else:
            saved_result = update_lab_result(
                report_key,
                result.marker_key,
                lab_result,
            )

        saved_results.append(
            saved_result
        )

    # ---------------------------------------------------------
    # 6. Return the completed save operation
    # ---------------------------------------------------------

    return LabReportSaveResponse(
        report=saved_report,
        results=saved_results,
    )