from fastapi import APIRouter

# Create a router for the Health module.

# Think of this as a mini FastAPI application that will later

# be plugged into the main application.

router = APIRouter(

    # Every endpoint in this file will automatically start with /health

    # Example:

    # /status becomes /health/status

    prefix="/health",

    # Groups these endpoints together in the Swagger documentation.

    tags=["Health"],

)

# Test endpoint.

# This simply confirms that the Health module is working.

@router.get("/status")

def get_health_status():

    return {

        "status": "healthy",

        "module": "health"

    }