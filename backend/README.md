# Personal Assistant Backend

## Overview

This backend powers the **Personal Assistant** application.

### Technology Stack

- Python
- FastAPI
- Google Sheets
- Pydantic Settings

---

### Prerequisites

- Python 3.10+
- pip

---

## First Time Setup

### Clone the Git Repository

Clone the project to your local machine.

```bash
git clone <repository-url>
```

### Navigate to the Backend Folder

Move into the backend folder before installing dependencies or running the application.

```bash
cd personal-assistant/backend
```

### Create a Virtual Environment

```bash
python3 -m venv .venv
```

### Activate the Virtual Environment

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file from `.env.example` and populate the required values.

Example:

```env
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service_account.json (Download this from the google dev account)
GOOGLE_SHEETS_SPREADSHEET_ID=YOUR_SPREADSHEET_ID (Its alphanumeric and You will find it in the google sheet url)
```

---

### Start the FastAPI Development Server

```bash
fastapi dev app/main.py
```

---

### Test the Google Sheets Connection

From the `backend` directory:

```bash
python -m tools.test_google_sheets
```

### Test the Health Repository

From the `backend` directory:

```bash
python -m tools.test_health_repository
```

### Test the Health Service

From the `backend` directory:

```bash
python -m tools.test_health_service
```

---

### Verify the Backend

Once the server is running, verify the following URLs:

| URL | Expected Result |
|------|-----------------|
| http://127.0.0.1:8000 | Personal Assistant API is running |
| http://127.0.0.1:8000/health/status | Health module status |
| http://127.0.0.1:8000/health/daily-logs | Returns all Daily Logs |
| http://127.0.0.1:8000/health/latest | Returns the latest Daily Log |
| http://127.0.0.1:8000/docs | Swagger API documentation |
and so on

---

# Project Structure

```text
backend/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database/
│   │   └── sheets_client.py
│   ├── modules/
│   │   └── health/
│   │       ├── api.py
│   │       ├── service.py
│   │       ├── repository.py
│   │       ├── schemas.py
│   │       └── __init__.py
│   └── utils/
│
├── credentials/
├── tools/
├── tests/
├── requirements.txt
├── .env
├── .env.example
└── README.md
```

---

# Architecture

The backend follows a layered architecture.

```text
Client
   │
   ▼
FastAPI API (api.py)
   │
   ▼
HealthService(service.py)
   │
   ▼
HealthRepository(repository.py)
   │
   ▼
Google Sheets Client
   │
   ▼
Google Sheets
```

## Request Flow

Example request:

```http
GET /health/daily-logs/2026-08-21
```

The request follows the flow below:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
api.py
(get_daily_log)
   │
   ├────► schemas.py
   │       (Response Model)
   │
   ▼
service.py
(get_daily_log)
   │
   ▼
repository.py
(get_daily_log)
   │
   ▼
Google Sheets Client
   │
   ▼
Daily_Log Worksheet
   │
   ▼
repository.py
(_row_to_daily_log)
   │
   ├────► schemas.py
   │       (Creates DailyLog object)
   │
   ▼
service.py
   │
   ▼
api.py
   │
   ▼
FastAPI
(Response Validation & Serialization)
   │
   ▼
JSON Response
```

## Layer Responsibilities

- `FastAPI`
  - Receives the HTTP request.
  - Routes the request to the correct API endpoint.
  - Validates and serializes the response using the Pydantic schema.

- `api.py`
  - Receives the HTTP request.
  - Validates the request and response.
  - Calls the Service layer.

- `service.py`
  - Implements the business logic.
  - Coordinates the Repository layer.

- `repository.py`
  - Reads and writes data to Google Sheets.
  - Converts worksheet rows into Pydantic models.

- `schemas.py`
  - Defines the Pydantic models used throughout the application.
  - Used by the Repository when creating domain objects.
  - Used by FastAPI to validate and serialize API responses.

- `sheets_client.py`
  - Creates the authenticated Google Sheets client used by the Repository.


| Layer | Responsibility |
|--------|----------------|
| `schemas.py` | Defines domain models independent of the data source |
| `api.py` | Defines REST API endpoints |
| `service.py` | Contains business logic |
| `repository.py` | Reads and writes application data |
| `database/sheets_client.py` | Creates authenticated Google Sheets client |
| `config.py` | Loads application configuration from `.env` |

---

# Configuration

Application configuration is managed through the `.env` file.

The `.env` file contains environment-specific settings such as:

- Google Sheets connection details
- Google service account credentials
- Worksheet names
- Other application configuration

The application loads these values through `app/config.py`, making them available throughout the backend via the `settings` object.

---

## Adding a New Field to the backend data store

When a new field is added to an existing data store, update the following components:

1. **Data Store**
   - Add the new column to the datastore.

2. **schemas.py**
   - Add the new field to the corresponding Pydantic model.

3. **repository.py**
   - Update `_row_to_<entity>()` to read the new column.
   - Update `_<entity>_to_row()` to write the new column.

4. **API**
   - No changes required if the existing endpoints already return the updated schema.

5. **Service**
   - No changes required unless business logic for the new field is needed.

6. **Configuration**
   - No changes required unless the new field requires additional configuration.

7. **Testing**
   - Verify the GET endpoint returns the new field.
   - Verify the POST/PUT endpoint correctly persists the new field.



## Renaming a Column in the Backend datastore

When a worksheet column is renamed, update the following components:

1. **Google Sheet**
   - Rename the column.

2. **repository.py**
   - Update the column name in `_row_to_<entity>()`.

3. **Testing**
   - Verify the GET endpoint still returns the correct data.
   - Verify the POST/PUT endpoint continues to read and write the correct column.



## Adding a New Worksheet / Entity

When a new worksheet (for example, `BodyMeasurements`) is added to the Google Spreadsheet, the following backend changes are required:

1. **Google Sheet**
   - Create the new worksheet.

2. **Configuration**
   - Add a new worksheet setting to `.env`.
   - Add the corresponding setting in `app/config.py`.

3. **schemas.py**
   - Create a new Pydantic model for the new entity.

4. **repository.py**
   - Add a method to retrieve the worksheet.
   - Add methods to read records.
   - Add methods to retrieve a single record.
   - Add methods to create and update records.
   - Add methods to convert worksheet rows to Pydantic models and vice versa.

5. **service.py**
   - Add methods that expose the Repository functionality.

6. **api.py**
   - Add the required CRUD endpoints.
   - Expose the new Pydantic model through the API.

7. **Testing**
   - Verify all GET, POST and PUT endpoints.
   - Verify data is correctly read from and written to the new worksheet.

---

# Documentation

Additional project documentation is available in:

- `docs/decisions/`

---

# Notes

Always activate the virtual environment before running the backend.

Whenever new Python packages are installed:

```bash
pip freeze > requirements.txt
```

Typical Git workflow:

```bash
git status
git add .
git commit -m "Meaningful commit message"
git push
```


## Testing

The backend is tested at multiple levels. Each level focuses on a different part of the application.

#### Repository Tests

Repository tests verify that the repository correctly reads from and writes to the data source.

Example:
- `get_daily_logs()` returns all Daily Log records.
- `update_body_measurement()` updates the correct worksheet row.

#### Repository Helper Tests

Repository helper tests verify the internal helper methods used to convert data between Google Sheets and the application's models.

Example:
- `_row_to_daily_log()` converts a worksheet row into a `DailyLog` object.
- `_daily_log_to_row()` converts a `DailyLog` object into a worksheet row.

#### Service Tests

Service tests verify the application's business logic and ensure that the Service layer correctly interacts with the Repository layer.

Example:
- `HealthService.get_daily_logs()` returns all Daily Logs from the repository.
- `HealthService.create_daily_log()` delegates the save operation to the repository.

#### API Tests

API tests verify the FastAPI endpoints by sending HTTP requests and validating the responses.

Example:
- `GET /health/daily-logs` returns a list of Daily Logs.
- `POST /health/daily-logs` creates a new Daily Log and returns the correct status code.

### Running Tests

Run all backend tests:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/repository/test_health_repository.py
```

Run a specific test method:

```bash
pytest tests/repository/test_health_repository.py::test_get_daily_logs
```

Run all tests with detailed output:

```bash
pytest -v
```