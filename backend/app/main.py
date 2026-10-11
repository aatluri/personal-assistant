from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

tags_metadata = [
    {
        "name": "Daily Log Metrics",
        "description": "Daily health summary records.",
    },
    {
        "name": "BodyMeasurement Metrics",
        "description": "Body weight and measurement records.",
    },
    {
        "name": "Workout Metrics",
        "description": "Workout and exercise metrics.",
    },
    {
        "name": "Sleep Metrics",
        "description": "Sleep duration and sleep stage metrics.",
    },
    {
        "name": "Health Metrics",
        "description": "General health and activity metrics.",
    },
    {
        "name": "Nutrition Metrics",
        "description": "Daily nutrition and dietary metrics.",
    },
    {
        "name": "Lab Reports",
        "description": "Blood test and laboratory reports.",
    },
    {
        "name": "Lab Marker Definitions",
        "description": "Definitions of laboratory markers.",
    },
    {
        "name": "Lab Marker Reference Ranges",
        "description": "Reference ranges for laboratory markers.",
    },
    {
        "name": "Lab Marker Interpretations",
        "description": "Interpretation rules for laboratory markers.",
    },
    {
        "name": "Lab Results",
        "description": "Individual laboratory test results.",
    },
    {
        "name": "API Health",
        "description": "General Health module endpoints.",
    },
]


# Create the main FastAPI application.

# There is only ONE FastAPI app for the entire project.

app = FastAPI(
    title="Personal Assistant API",
    description="Backend API for the Personal Assistant application.",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
