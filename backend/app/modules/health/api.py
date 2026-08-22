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

from app.modules.health.schemas import DailyLog
from app.modules.health.schemas import BodyMeasurements
from app.modules.health.service import HealthService



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
