from fastapi import APIRouter

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


@router.get(
    "/daily-logs",
    response_model=list[DailyLog],
)
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