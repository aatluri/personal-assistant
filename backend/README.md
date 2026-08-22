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

### 1. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 2. Activate the Virtual Environment

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

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

Application configuration is managed through `.env`.

Current configuration:

| Variable | Description |
|----------|-------------|
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path to the Google service account credentials |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | Google Spreadsheet ID |
| `HEALTH_DAILY_LOG_WORKSHEET` |  Daily_Log |

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