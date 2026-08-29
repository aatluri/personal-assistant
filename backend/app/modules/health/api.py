"""
Health API

Exposes the Health module through REST endpoints.

Responsibilities:
- Receive HTTP requests from clients.
- Validate request and response models using Pydantic.
- Delegate business logic to the HealthService.
- Return HTTP responses.

The API layer should not contain business logic or access
Google Sheets directly.
"""

from fastapi import APIRouter
from datetime import date
from fastapi import HTTPException
from fastapi import status

from app.modules.health.schemas import DailyLog,BodyMeasurements
from app.modules.health.service import HealthService
from app.modules.health.lab_schemas import (
    LabReport,
    LabReportCreate,
    LabMarkerDefinition,
    LabMarkerInterpretation,
    LabMarkerReferenceRange,
    LabResult,
)
from app.modules.health.lab_repository import (
    get_lab_report,
    list_lab_reports,
    update_lab_report,
    create_lab_marker_definition,
    update_lab_marker_definition,
    get_lab_marker_definition,
    list_lab_marker_definitions,
    create_lab_marker_reference_range,
    get_lab_marker_reference_range,
    list_lab_marker_reference_ranges,
    update_lab_marker_reference_range,
    create_lab_marker_interpretation,
    get_lab_marker_interpretation,
    list_lab_marker_interpretations,
    update_lab_marker_interpretation,
    create_lab_result,
    get_lab_result,
    list_lab_results,
    update_lab_result,
)
from app.modules.health.lab_service import (
    create_lab_report_record,
)

from fastapi import UploadFile, File
import os
import tempfile

from app.modules.health.lab_extraction_schemas import (
    LabReportExtraction,
)

from app.modules.health.lab_extraction_service import (
    extract_lab_report,
)



# All endpoints defined in this router will begin with /health.
router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


# Create the Health service used by the API endpoints.
#
# The API layer does not communicate with Google Sheets directly.
# It calls the service layer, which then calls the repository.
health_service = HealthService()


@router.get("/status")
def get_health_status() -> dict[str, str]:
    """
    Verify that the Health module is available.

    This endpoint does not access Google Sheets.
    It is only a basic module health check.
    """
    return {
        "status": "ok",
        "module": "health",
    }


# -----------------------------------------------------------------------------
# Daily Log Endpoints
#
# Endpoints for creating, retrieving and updating Daily Logs.
# -----------------------------------------------------------------------------

@router.get("/daily-logs",response_model=list[DailyLog],)
def get_daily_logs() -> list[DailyLog]:
    """
    Return all Health Daily Log records.
    """
    return health_service.get_daily_logs()



@router.get("/daily-logs/{log_date}",response_model=DailyLog,)
def get_daily_log(log_date: date) -> DailyLog:
    """
    Retrieve the Daily Log for the specified date.

    Returns:
        - The matching DailyLog if found.
        - HTTP 404 if no record exists.
    """
    daily_log = health_service.get_daily_log(log_date)
    if daily_log is None:
        raise HTTPException(
            status_code=404,
            detail="Daily Log not found.",
        )
    return daily_log

@router.get("/latest",response_model=DailyLog,)


def get_latest_daily_log() -> DailyLog:
    """
    Return the most recent Daily Log.
    """

    latest_log = health_service.get_latest_daily_log()

    if latest_log is None:
        raise HTTPException(
            status_code=404,
            detail="No Daily Logs found.",
        )

    return latest_log

@router.post("/daily-logs",status_code=status.HTTP_201_CREATED,)
def create_daily_log(daily_log: DailyLog,) -> None:
    """
    Create a new Daily Log.
    """

    health_service.create_daily_log(daily_log)


@router.put("/daily-logs/{log_date}", response_model=DailyLog)
def update_daily_log(log_date: date,daily_log: DailyLog,) -> DailyLog:
    """
    Update an existing Daily Log or create one if it does not exist.

    The date in the URL must match the date contained in the request body.
    """

    if daily_log.date != log_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The URL date must match the Daily Log date.",
        )

    health_service.upsert_daily_log(
        log_date,
        daily_log,
    )

    return daily_log


# -----------------------------------------------------------------------------
# Body Measurements Endpoints
#
# Endpoints for creating, retrieving and updating Body Measurements.
# -----------------------------------------------------------------------------

@router.get( "/body-measurements",response_model=list[BodyMeasurements],)
def get_body_measurements():
    return health_service.get_body_measurements()


@router.get("/body-measurements/{measurement_date}",response_model=BodyMeasurements,)
def get_body_measurement(measurement_date: date,) -> BodyMeasurements:
    """
    Return the Body Measurements for a specific date.
    """

    body_measurement = health_service.get_body_measurement(
        measurement_date
    )

    if body_measurement is None:
        raise HTTPException(
            status_code=404,
            detail="Body Measurements not found.",
        )

    return body_measurement

@router.post("/body-measurements",status_code=status.HTTP_201_CREATED,)
def create_body_measurement(body_measurement: BodyMeasurements,) -> None:
    """
    Create a new Body Measurements record.
    """

    health_service.create_body_measurement(
        body_measurement
    )

@router.put("/body-measurements/{measurement_date}",response_model=BodyMeasurements,)
def update_body_measurement(
    measurement_date: date,
    body_measurement: BodyMeasurements,
) -> BodyMeasurements:
    """
    Update or create the Body Measurements for the specified date.
    """

    if body_measurement.date != measurement_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The URL date must match the Body Measurements date.",
        )

    health_service.upsert_body_measurement(
        measurement_date,
        body_measurement,
    )

    return body_measurement

# =========================================================
# LAB REPORTS
# =========================================================


# ---------------------------------------------------------
# Create
# This calls the service create method to generate the key
# That method calls the repository method to create the record in the database.
# ---------------------------------------------------------

@router.post(
    "/lab-reports",
    response_model=LabReport,
    status_code=status.HTTP_201_CREATED,
)
def create_lab_report_endpoint(
    report: LabReportCreate,
):
    return create_lab_report_record(report)


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

@router.get(
    "/lab-reports/{report_key}",
    response_model=LabReport,
)
def get_lab_report_endpoint(
    report_key: str,
):
    report = get_lab_report(report_key)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab report not found",
        )

    return report


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

@router.get(
    "/lab-reports",
    response_model=list[LabReport],
)
def list_lab_reports_endpoint():
    return list_lab_reports()


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

@router.put(
    "/lab-reports/{report_key}",
    response_model=LabReport,
)
def update_lab_report_endpoint(
    report_key: str,
    report: LabReport,
):
    updated_report = update_lab_report(
        report_key,
        report,
    )

    if updated_report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab report not found",
        )

    return updated_report


# =========================================================
# LAB MARKER DEFINITIONS
# =========================================================


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

@router.post(
    "/lab-marker-definitions",
    response_model=LabMarkerDefinition,
    status_code=status.HTTP_201_CREATED,
)
def create_lab_marker_definition_endpoint(
    definition: LabMarkerDefinition,
):
    return create_lab_marker_definition(definition)


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

@router.get(
    "/lab-marker-definitions/{marker_key}",
    response_model=LabMarkerDefinition,
)
def get_lab_marker_definition_endpoint(
    marker_key: str,
):
    definition = get_lab_marker_definition(marker_key)

    if definition is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab marker definition not found",
        )

    return definition


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

@router.get(
    "/lab-marker-definitions",
    response_model=list[LabMarkerDefinition],
)
def list_lab_marker_definitions_endpoint():
    return list_lab_marker_definitions()


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

@router.put(
    "/lab-marker-definitions/{marker_key}",
    response_model=LabMarkerDefinition,
)
def update_lab_marker_definition_endpoint(
    marker_key: str,
    definition: LabMarkerDefinition,
):
    updated_definition = update_lab_marker_definition(
        marker_key,
        definition,
    )

    if updated_definition is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab marker definition not found",
        )

    return updated_definition

# =========================================================
# LAB MARKER REFERENCE RANGES
# =========================================================


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

@router.post(
    "/lab-marker-reference-ranges",
    response_model=LabMarkerReferenceRange,
    status_code=status.HTTP_201_CREATED,
)
def create_lab_marker_reference_range_endpoint(
    reference_range: LabMarkerReferenceRange,
):
    return create_lab_marker_reference_range(
        reference_range
    )


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

@router.get(
    "/lab-marker-reference-ranges/{marker_key}",
    response_model=LabMarkerReferenceRange,
)
def get_lab_marker_reference_range_endpoint(
    marker_key: str,
    gender: str,
    min_age: int | None = None,
    max_age: int | None = None,
):
    reference_range = get_lab_marker_reference_range(
        marker_key,
        gender,
        min_age,
        max_age,
    )

    if reference_range is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab marker reference range not found",
        )

    return reference_range


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

@router.get(
    "/lab-marker-reference-ranges",
    response_model=list[LabMarkerReferenceRange],
)
def list_lab_marker_reference_ranges_endpoint(
    marker_key: str | None = None,
):
    return list_lab_marker_reference_ranges(
        marker_key
    )


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

@router.put(
    "/lab-marker-reference-ranges/{marker_key}",
    response_model=LabMarkerReferenceRange,
)
def update_lab_marker_reference_range_endpoint(
    marker_key: str,
    reference_range: LabMarkerReferenceRange,
    gender: str,
    min_age: int | None = None,
    max_age: int | None = None,
):
    updated_reference_range = (
        update_lab_marker_reference_range(
            marker_key,
            gender,
            min_age,
            max_age,
            reference_range,
        )
    )

    if updated_reference_range is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab marker reference range not found",
        )

    return updated_reference_range


# =========================================================
# LAB MARKER INTERPRETATIONS
# =========================================================


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

@router.post(
    "/lab-marker-interpretations",
    response_model=LabMarkerInterpretation,
    status_code=status.HTTP_201_CREATED,
)
def create_lab_marker_interpretation_endpoint(
    interpretation: LabMarkerInterpretation,
):
    return create_lab_marker_interpretation(
        interpretation
    )


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

@router.get(
    "/lab-marker-interpretations/{marker_key}",
    response_model=LabMarkerInterpretation,
)
def get_lab_marker_interpretation_endpoint(
    marker_key: str,
    label: str,
):
    interpretation = get_lab_marker_interpretation(
        marker_key,
        label,
    )

    if interpretation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab marker interpretation not found",
        )

    return interpretation


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

@router.get(
    "/lab-marker-interpretations",
    response_model=list[LabMarkerInterpretation],
)
def list_lab_marker_interpretations_endpoint(
    marker_key: str | None = None,
):
    return list_lab_marker_interpretations(
        marker_key
    )


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

@router.put(
    "/lab-marker-interpretations/{marker_key}",
    response_model=LabMarkerInterpretation,
)
def update_lab_marker_interpretation_endpoint(
    marker_key: str,
    interpretation: LabMarkerInterpretation,
    label: str,
):
    updated_interpretation = (
        update_lab_marker_interpretation(
            marker_key,
            label,
            interpretation,
        )
    )

    if updated_interpretation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab marker interpretation not found",
        )

    return updated_interpretation


# =========================================================
# LAB RESULTS
# =========================================================


# ---------------------------------------------------------
# Create
# ---------------------------------------------------------

@router.post(
    "/lab-results",
    response_model=LabResult,
    status_code=status.HTTP_201_CREATED,
)
def create_lab_result_endpoint(
    result: LabResult,
):
    return create_lab_result(result)


# ---------------------------------------------------------
# Get
# ---------------------------------------------------------

@router.get(
    "/lab-results/{report_key}",
    response_model=LabResult,
)
def get_lab_result_endpoint(
    report_key: str,
    marker_key: str,
):
    result = get_lab_result(
        report_key,
        marker_key,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab result not found",
        )

    return result


# ---------------------------------------------------------
# List
# ---------------------------------------------------------

@router.get(
    "/lab-results",
    response_model=list[LabResult],
)
def list_lab_results_endpoint(
    report_key: str | None = None,
    marker_key: str | None = None,
):
    return list_lab_results(
        report_key,
        marker_key,
    )


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------

@router.put(
    "/lab-results/{report_key}",
    response_model=LabResult,
)
def update_lab_result_endpoint(
    report_key: str,
    result: LabResult,
    marker_key: str,
):
    updated_result = update_lab_result(
        report_key,
        marker_key,
        result,
    )

    if updated_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab result not found",
        )

    return updated_result


# ---------------------------------------------------------
# Extract Lab Report PDF
# ---------------------------------------------------------

@router.post(
    "/lab-reports/extract",
    response_model=LabReportExtraction,
)
async def extract_lab_report_endpoint(
    file: UploadFile = File(...),
):
    """
    Extract lab report metadata and results from an uploaded PDF.

    This endpoint does not save anything to Google Sheets.
    It only returns extracted data for the UI to review.
    """

    # Only allow PDF files.
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    temp_file_path = None

    try:
        # Create a temporary PDF file.
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp_file:

            temp_file_path = temp_file.name

            # Read the uploaded PDF and write it temporarily.
            file_content = await file.read()
            temp_file.write(file_content)

        # Extract the report.
        extraction = extract_lab_report(
            file_path=temp_file_path,
            file_name=file.filename or "lab_report.pdf",
        )

        return extraction

    finally:
        # Always remove the temporary PDF,
        # even if extraction fails.
        if (
            temp_file_path
            and os.path.exists(temp_file_path)
        ):
            os.remove(temp_file_path)