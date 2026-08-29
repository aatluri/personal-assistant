import hashlib

from app.modules.health.lab_schemas import (
    LabReport,
    LabReportCreate,
)

from app.modules.health.lab_repository import (
    create_lab_report,
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