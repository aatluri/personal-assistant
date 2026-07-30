from fastapi import FastAPI

# Import the Health module's router.
# As we add more modules (Email, Workout, Nutrition),
# we'll import their routers here as well.
#Each module owns its own endpoints, while main.py simply brings them all together into a single FastAPI application.
# This is one of the cleanest patterns for larger FastAPI projects.
# main.py
 #   │
 #   ├── Health Router
 #   ├── Email Router
 #   ├── Workout Router#
 #   └── Nutrition Router

from app.modules.health.api import router as health_router

# Create the main FastAPI application.

# There is only ONE FastAPI app for the entire project.

app = FastAPI(
    title="Personal Assistant API",
    description="Backend API for the Personal Assistant application.",
    version="0.1.0",
)


# Simple root endpoint.
# Used to verify that the API is running.

@app.get("/")
def root():
    return {

        "message": "Personal Assistant API is running"

    }

# Register the Health module with the main application.
# This makes all routes defined in health/api.py available.

app.include_router(health_router)
