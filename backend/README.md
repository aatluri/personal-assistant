# Personal Assistant Backend

## Overview

This backend powers the **Personal Assistant** application.

### Current Module

- Health Tracker

### Technology Stack

- Python
- FastAPI
- Google Sheets
- Pydantic Settings

---

# Prerequisites

- Python 3.10+
- pip

---

# First Time Setup

## 1. Create a Virtual Environment

```bash
python3 -m venv .venv
```

## 2. Activate the Virtual Environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file from `.env.example` and populate the required values.

Example:

```env
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service_account.json
GOOGLE_SHEETS_SPREADSHEET_ID=YOUR_SPREADSHEET_ID
```

---

# Running the Backend

## Activate the Virtual Environment

```bash
source .venv/bin/activate
```

## Start the FastAPI Development Server

```bash
fastapi dev app/main.py
```

---

# Development Utilities

## Test the Google Sheets Connection

From the `backend` directory:

```bash
python -m tools.test_google_sheets
```

## Test the Health Repository

From the `backend` directory:

```bash
python -m tools.test_health_repository
```

## Test the Health Service

From the `backend` directory:

```bash
python -m tools.test_health_service
```

---

# Verify the Backend

Once the server is running, verify the following URLs:

| URL | Expected Result |
|------|-----------------|
| http://127.0.0.1:8000 | Personal Assistant API is running |
| http://127.0.0.1:8000/health/status | Health module status |
| http://127.0.0.1:8000/health/daily-logs | Returns all Daily Logs |
| http://127.0.0.1:8000/health/latest | Returns the latest Daily Log |
| http://127.0.0.1:8000/docs | Swagger API documentation |

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

## Example Request

Assume a client sends the following HTTP request:

```http

GET /health/daily-logs

```

The request flows through the backend as follows.

### 1. FastAPI receives the request

File:

```text

app/modules/health/api.py

```

FastAPI matches the request to:

```python

get_daily_logs()

```

This function is responsible for:

- Receiving the HTTP request.

- Calling the service layer.

- Returning the response to the client.

```text

Client

    │

GET /health/daily-logs

    │

    ▼

api.py

get_daily_logs()

```

---

### 2. API calls the Service

The API executes:

```python

health_service.get_daily_logs()

```

File:

```text

app/modules/health/service.py

```

Method called:

```python

HealthService.get_daily_logs()

```

The service layer contains the application's business logic.

Currently this method simply retrieves all Daily Log records.

In the future it may:

- Filter records

- Calculate statistics

- Validate business rules

- Combine data from multiple repositories

```text

api.py

    │

    ▼

HealthService.get_daily_logs()

```

---

### 3. Service calls the Repository

The service executes:

```python
self._repository.get_daily_logs()
```
File:
```text
app/modules/health/repository.py
```

Method called:
```python
HealthRepository.get_daily_logs()
```
The repository is responsible only for accessing data.
It:
- Connects to Google Sheets
- Reads worksheet rows
- Converts each row into a `DailyLog` object
- Returns a list of `DailyLog` objects

```text
HealthService
    │
    ▼
HealthRepository.get_daily_logs()
```

---

### 4. Repository calls the Google Sheets Client
The repository executes:
```python
get_sheets_client()
```
File:
```text
app/database/sheets_client.py
```

This function:
- Authenticates using the service account
- Creates the Google Sheets client
- Returns the authenticated client
The repository then opens the spreadsheet and worksheet before reading all rows.

```text
HealthRepository
    │
    ▼
get_sheets_client()
    │
    ▼
Google Sheets

```

---

### 5. Data flows back up the layers

Once the worksheet has been read:
- The repository returns a list of `DailyLog` objects.
- The service receives those objects and returns them unchanged.
- The API receives the objects.
- FastAPI automatically converts them into JSON.
- The JSON response is returned to the client.

```text
Google Sheets
    │
    ▼
List[DailyLog]
    │
    ▼
HealthRepository
    │
    ▼
HealthService
    │
    ▼
FastAPI
    │
    ▼
JSON Response
    │
    ▼
Client
```

---

## Complete Method Call Sequence

```text
Client
↓
GET /health/daily-logs
↓
api.py
get_daily_logs()
↓
service.py
HealthService.get_daily_logs()
↓
repository.py
HealthRepository.get_daily_logs()
↓
database/sheets_client.py
get_sheets_client()
↓
Google Sheets
↓
repository.py
_row_to_daily_log()
↓
List[DailyLog]
↓
service.py
HealthService.get_daily_logs()
↓
api.py
get_daily_logs()
↓
JSON Response
↓
Client

```

## Layer Responsibilities

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
# Current Status

## ✅ Completed

- Project structure created
- FastAPI configured
- Health module created
- Health router registered
- Swagger documentation verified
- Git repository initialized
- GitHub repository connected
- Configuration management implemented
- Google Sheets client implemented
- Google Sheets connectivity verified
- `DailyLog` domain model implemented
- Health repository implemented
- Google Sheets to `DailyLog` mapping implemented
- Health service implemented
- Health REST API implemented
- CRUD endpoints implemented
    - GET /health/status
    - GET /health/daily-logs
    - GET /health/daily-logs/{date}
    - GET /health/latest
    - POST /health/daily-logs
    - PUT /health/daily-logs/{date}
- Repository and service test utilities created
- Repository refactored to reuse worksheet access
- End-to-end Health module flow verified

---

## 🚧 Next Milestone

**Health API Layer**

### Goals

- Implement REST API endpoints for the Health module.
- Connect the API layer to the Health service.
- Return `DailyLog` data through FastAPI.
- Verify all endpoints using Swagger UI.
- Establish the pattern for future modules (Workout, Nutrition, Email).
---

# Documentation

Additional project documentation is available in:

- `docs/development-log.md`
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