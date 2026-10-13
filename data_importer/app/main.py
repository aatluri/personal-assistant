from fastapi import FastAPI


# Create the FastAPI application.
app = FastAPI(
    title="Personal Assistant - Data Importer",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    """
    Simple health-check endpoint.

    This lets us verify that the Data Importer service
    is running and responding to HTTP requests.
    """
    return {"status": "ok"}