from fastapi import APIRouter
from datetime import date
from fastapi import HTTPException
from fastapi import status

from app.modules.health.schemas import DailyLog
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


@router.get("/daily-logs",response_model=list[DailyLog],)
def get_daily_logs() -> list[DailyLog]:
    """
    Return all Health Daily Log records.

    Request flow:

        API
        ↓
        HealthService
        ↓
        HealthRepository
        ↓
        Google Sheets

    FastAPI uses the DailyLog response model to validate and serialize
    the returned objects into JSON.
    """
    return health_service.get_daily_logs()

@router.get("/daily-logs/{log_date}",response_model=DailyLog,)
def get_daily_log(log_date: date) -> DailyLog:
    """
    Return the Daily Log for a specific date.
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


@router.put("/daily-logs/{log_date}",response_model=DailyLog,)
def update_daily_log(log_date: date,daily_log: DailyLog,) -> DailyLog:
    """
    Update the Daily Log for the specified date.
    """

    if daily_log.date != log_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The URL date must match the Daily Log date.",
        )

    updated = health_service.update_daily_log(
        log_date,
        daily_log,
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily Log not found.",
        )

    return daily_log

