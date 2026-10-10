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
from datetime import date, datetime
from fastapi import HTTPException
from fastapi import status

from app.modules.health.schemas import (
    DailyLog,
    BodyMeasurements,
    WorkoutMetrics,
    SleepMetrics,
    HealthMetrics,
    NutritionMetrics
)
from app.modules.health.service import HealthService
from app.modules.health.lab_schemas import (
    LabReport,
    LabReportCreate,
    LabMarkerDefinition,
    LabMarkerInterpretation,
    LabMarkerReferenceRange,
    LabResult,
)
from app.modules.health.body_measurements_service import (
    BodyMeasurementsService,
)
from app.modules.health.sleep_metrics_service import (
    SleepMetricsService,
)
from app.modules.health.health_metrics_service import (
    HealthMetricsService,
)
from app.modules.health.nutrition_metrics_service import (
    NutritionMetricsService,
)

from app.modules.health.workout_metrics_service import (
    WorkoutMetricsService,
)

from app.modules.health.lab_save_schemas import (
    LabReportSaveRequest,
    LabReportSaveResponse,
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
    save_lab_report,
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


# Create the services used by the API endpoints.
#
# The API layer does not communicate with Google Sheets directly.
# It calls the service layer, which then calls the repository.

health_service = HealthService()

body_measurements_service = BodyMeasurementsService()

workout_metrics_service = WorkoutMetricsService()

sleep_metrics_service = SleepMetricsService()

health_metrics_service = HealthMetricsService()

nutrition_metrics_service = NutritionMetricsService()


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

@router.get( "/body-measurements",response_model=list[BodyMeasurements],tags=["BodyMeasurement Metrics"],)
def get_body_measurements():
    return body_measurements_service.get_body_measurements()


@router.get("/body-measurements/{measurement_date}",response_model=BodyMeasurements,tags=["BodyMeasurement Metrics"],)
def get_body_measurement(measurement_date: date,) -> BodyMeasurements:
    """
    Return the Body Measurements for a specific date.
    """

    body_measurement = body_measurements_service.get_body_measurement(
        measurement_date
    )

    if body_measurement is None:
        raise HTTPException(
            status_code=404,
            detail="Body Measurements not found.",
        )

    return body_measurement

@router.post("/body-measurements",status_code=status.HTTP_201_CREATED,tags=["BodyMeasurement Metrics"],)
def create_body_measurement(body_measurement: BodyMeasurements,) -> None:
    """
    Create a new Body Measurements record.
    """

    body_measurements_service.create_body_measurement(
        body_measurement
    )

@router.put(
    "/body-measurements",
    response_model=BodyMeasurements,
    tags=["BodyMeasurement Metrics"],
)
def update_body_measurement(
    body_measurement: BodyMeasurements,
) -> BodyMeasurements:
    """
    Update or create a Body Measurements record.

    The date contained in the request body is used
    to identify the record.
    """

    body_measurements_service.upsert_body_measurement(
        body_measurement.date,
        body_measurement,
    )

    return body_measurement

# -----------------------------------------------------------------------------
# Workout Metrics Endpoints
#
# Endpoints for creating, retrieving and updating Workout Metrics.
# -----------------------------------------------------------------------------

@router.get(
    "/workout-metrics",
    response_model=list[WorkoutMetrics],
    tags=["Workout Metrics"],
)
def get_workout_metrics(
    workout_date: date | None = None,
) -> list[WorkoutMetrics]:

    if workout_date is not None:
        return workout_metrics_service.get_workout_metrics_by_date(
            workout_date
        )

    return workout_metrics_service.get_workout_metrics()




@router.get(
    "/workout-metric",
    response_model=WorkoutMetrics,
    tags=["Workout Metrics"],
)
def get_workout_metric(
    workout_start_time: datetime,
) -> WorkoutMetrics:
    """
    Return the Workout Metrics record for the specified
    Workout Start Time.

    The Workout Start Time is supplied as a query parameter.
    """

    workout_metric = workout_metrics_service.get_workout_metric(
        workout_start_time
    )

    if workout_metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout Metrics not found.",
        )

    return workout_metric

@router.post(
    "/workout-metrics",
    status_code=status.HTTP_201_CREATED,
    tags=["Workout Metrics"],
)
def create_workout_metric(
    workout_metric: WorkoutMetrics,
) -> None:
    """
    Create a new Workout Metrics record.
    """

    workout_metrics_service.create_workout_metric(
        workout_metric
    )


@router.put(
    "/workout-metrics",
    response_model=WorkoutMetrics,
    tags=["Workout Metrics"],
)
def update_workout_metric(
    workout_metric: WorkoutMetrics,
) -> WorkoutMetrics:
    """
    Update or create a Workout Metrics record.

    The Workout Start Time contained in the request body
    is used to identify the record.
    """

    workout_metrics_service.upsert_workout_metric(
        workout_metric.workout_start_time,
        workout_metric,
    )

    return workout_metric

# -----------------------------------------------------------------------------
# Sleep Metrics Endpoints
#
# Endpoints for creating, retrieving and updating Sleep Metrics.
# -----------------------------------------------------------------------------

@router.get(
    "/sleep-metrics",
    response_model=list[SleepMetrics],
    tags=["Sleep Metrics"],
)
def get_sleep_metrics() -> list[SleepMetrics]:
    """
    Return all Sleep Metrics records.
    """

    return sleep_metrics_service.get_sleep_metrics()


@router.get(
    "/sleep-metrics/{metric_date}",
    response_model=SleepMetrics,
    tags=["Sleep Metrics"],
)
def get_sleep_metric(
    metric_date: date,
) -> SleepMetrics:
    """
    Return the Sleep Metrics for a specific date.
    """

    sleep_metric = sleep_metrics_service.get_sleep_metric(
        metric_date
    )

    if sleep_metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sleep Metrics not found.",
        )

    return sleep_metric


@router.post(
    "/sleep-metrics",
    status_code=status.HTTP_201_CREATED,
    tags=["Sleep Metrics"],
)
def create_sleep_metric(
    sleep_metric: SleepMetrics,
) -> None:
    """
    Create a new Sleep Metrics record.
    """

    sleep_metrics_service.create_sleep_metric(
        sleep_metric
    )


@router.put(
    "/sleep-metrics",
    response_model=SleepMetrics,
    tags=["Sleep Metrics"],
)
def update_sleep_metric(
    sleep_metric: SleepMetrics,
) -> SleepMetrics:
    """
    Update or create a Sleep Metrics record.

    The date contained in the request body is used
    to identify the record.
    """

    sleep_metrics_service.upsert_sleep_metric(
        sleep_metric.date,
        sleep_metric,
    )

    return sleep_metric


# -----------------------------------------------------------------------------
# Health Metrics Endpoints
#
# Endpoints for creating, retrieving and updating Health Metrics.
# -----------------------------------------------------------------------------

@router.get(
    "/health-metrics",
    response_model=list[HealthMetrics],
    tags=["Health Metrics"],
)
def get_health_metrics() -> list[HealthMetrics]:
    """
    Return all Health Metrics records.
    """

    return health_metrics_service.get_health_metrics()


@router.get(
    "/health-metrics/{metric_date}",
    response_model=HealthMetrics,
    tags=["Health Metrics"],
)
def get_health_metric(
    metric_date: date,
) -> HealthMetrics:
    """
    Return the Health Metrics for a specific date.
    """

    health_metric = health_metrics_service.get_health_metric(
        metric_date
    )

    if health_metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health Metrics not found.",
        )

    return health_metric


@router.post(
    "/health-metrics",
    status_code=status.HTTP_201_CREATED,
    tags=["Health Metrics"],
)
def create_health_metric(
    health_metric: HealthMetrics,
) -> None:
    """
    Create a new Health Metrics record.
    """

    health_metrics_service.create_health_metric(
        health_metric
    )


@router.put(
    "/health-metrics",
    response_model=HealthMetrics,
    tags=["Health Metrics"],
)
def update_health_metric(
    health_metric: HealthMetrics,
) -> HealthMetrics:
    """
    Update or create a Health Metrics record.

    The date contained in the request body is used
    to identify the record.
    """

    health_metrics_service.upsert_health_metric(
        health_metric.date,
        health_metric,
    )

    return health_metric


# -----------------------------------------------------------------------------
# Nutrition Metrics Endpoints
#
# Endpoints for creating, retrieving and updating Nutrition Metrics.
# -----------------------------------------------------------------------------

@router.get(
    "/nutrition-metrics",
    response_model=list[NutritionMetrics],
    tags=["Nutrition Metrics"],
)
def get_nutrition_metrics() -> list[NutritionMetrics]:
    """
    Return all Nutrition Metrics records.
    """

    return nutrition_metrics_service.get_nutrition_metrics()


@router.get(
    "/nutrition-metrics/{metric_date}",
    response_model=NutritionMetrics,
    tags=["Nutrition Metrics"],
)
def get_nutrition_metric(
    metric_date: date,
) -> NutritionMetrics:
    """
    Return the Nutrition Metrics for a specific date.
    """

    nutrition_metric = nutrition_metrics_service.get_nutrition_metric(
        metric_date
    )

    if nutrition_metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nutrition Metrics not found.",
        )

    return nutrition_metric


@router.post(
    "/nutrition-metrics",
    status_code=status.HTTP_201_CREATED,
    tags=["Nutrition Metrics"],
)
def create_nutrition_metric(
    nutrition_metric: NutritionMetrics,
) -> None:
    """
    Create a new Nutrition Metrics record.
    """

    nutrition_metrics_service.create_nutrition_metric(
        nutrition_metric
    )


@router.put(
    "/nutrition-metrics",
    response_model=NutritionMetrics,
    tags=["Nutrition Metrics"],
)
def update_nutrition_metric(
    nutrition_metric: NutritionMetrics,
) -> NutritionMetrics:
    """
    Update or create a Nutrition Metrics record.

    The date contained in the request body is used
    to identify the record.
    """

    nutrition_metrics_service.upsert_nutrition_metric(
        nutrition_metric.date,
        nutrition_metric,
    )

    return nutrition_metric
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


@router.post(
    "/lab-reports/save",
    response_model=LabReportSaveResponse,
)
def save_lab_report_endpoint(
    save_request: LabReportSaveRequest,
):
    """
    Save a complete lab report and its marker results.

    The frontend sends:
    - Lab report metadata
    - All marker values currently entered in the UI

    The service layer:
    - Generates the Report_Key
    - Creates or updates the Lab_Reports record
    - Ignores empty marker results
    - Creates or updates non-empty Lab_Results
    """

    return save_lab_report(save_request)