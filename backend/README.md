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

---

## Notes

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



## Lab Report PDF Extraction

The Health module supports extracting structured lab results from uploaded PDF reports.

### Endpoint

`POST /health/lab-reports/extract`

The endpoint accepts a PDF lab report and returns extracted report metadata and marker results.

**Extraction does not save any data to Google Sheets.** The returned data is intended to populate the UI so the user can review or edit the values before saving.

### How It Works

1. The user uploads a lab report PDF.
2. FastAPI receives the PDF and creates a temporary local file.
3. The backend loads all active markers from `Lab_Marker_Definitions`.
4. A compact list of marker definitions is prepared containing:
   - `marker_key`
   - `display_name`
   - `category`
   - `panel`
   - `default_unit`
5. The PDF and marker definitions are sent to OpenAI.
6. OpenAI extracts:
   - Report metadata
   - All laboratory test results found in the PDF
7. Each extracted test is mapped to an existing `Marker_Key`.
8. A `Marker_Key` is only used when the test can be confidently mapped to one of the supplied marker definitions. New marker keys are never invented.
9. Tests that cannot be confidently mapped are returned separately in `unmapped_results`.
10. The structured extraction is returned to the UI.
11. The temporary PDF is deleted.
12. The user can review or edit the populated values before saving them.

### Extraction Response

The response contains:

- `report_date`
- `collection_date`
- `report_datetime`
- `report_type`
- `laboratory_name`
- `file_name`
- `results`
- `unmapped_results`

Each mapped result contains:

- `marker_key`
- `reported_name`
- `numerical_value`
- `text_value`
- `unit`

Numeric results are stored in `numerical_value`. Non-numeric results such as `Negative`, `Nil`, or `1 to 2` are returned in `text_value`.

Dates are normalized during extraction:

- Dates: `YYYY-MM-DD`
- Date/time values: `YYYY-MM-DD HH:MM:SS`

Units are preserved exactly as reported by the laboratory and are not converted.

### Flow

PDF Upload
→ FastAPI `/lab-reports/extract`
→ Load active `Lab_Marker_Definitions`
→ OpenAI extraction and Marker_Key mapping
→ Structured response
→ UI fields populated
→ User reviews/edits
→ Save


## Lab Report Save Flow

The Lab Report Save endpoint saves the reviewed lab report data from the frontend into the `Lab_Reports` and `Lab_Results` worksheets.

### Endpoint

`POST /health/lab-reports/save`

### Overall Flow

```text
Lab Marker Screen
        ↓
User manually enters values
        OR
Uploads PDF → values are extracted and populated
        ↓
User reviews / edits the values
        ↓
User clicks Save
        ↓
POST /health/lab-reports/save
        ↓
Backend generates Report_Key
        ↓
Save / Update Lab_Reports
        ↓
Save / Update non-empty Lab_Results
```

### Request

The frontend sends the report metadata together with the current marker values.

Example:

```json
{
  "report_date": "2025-06-02",
  "collection_date": "2025-06-02",
  "report_datetime": "2025-06-02 13:56:54",
  "report_type": "",
  "laboratory_name": "VIJAYA MEDICAL CENTRE",
  "file_name": "Blood work Adarsh 20250602.pdf",
  "notes": "",
  "results": [
    {
      "marker_key": "FASTING_GLUCOSE",
      "numerical_value": 101,
      "text_value": "",
      "unit": "mg/dL"
    },
    {
      "marker_key": "STOOL_OCCULT_BLOOD",
      "numerical_value": null,
      "text_value": "Negative",
      "unit": ""
    }
  ]
}
```

The frontend does **not** generate or send the `Report_Key`.

### Report_Key Generation

The backend generates the `Report_Key` using:

```text
LAB_<ReportDate YYYYMMDD>_<first 12 characters of SHA-256(filename)>
```

For example:

```text
LAB_20250602_4d71c9a83f12
```

Using the same report date and file name therefore generates the same `Report_Key`.

### Saving Lab_Reports

The backend checks whether the generated `Report_Key` already exists.

```text
Report exists?
    │
    ├── No  → Create Lab_Reports row
    │
    └── Yes → Update existing Lab_Reports row
```

This makes the save operation retry-safe and prevents another report row from being created when the same report is saved again.

### Saving Lab_Results

The backend processes each marker result sent by the frontend.

A result is saved only when it contains either:

- a `numerical_value`, or
- a non-empty `text_value`

Completely empty marker results are ignored.

For each non-empty result, the unique key is:

```text
Report_Key + Marker_Key
```

The backend checks whether that result already exists.

```text
Result exists?
    │
    ├── No  → Create Lab_Results row
    │
    └── Yes → Update existing Lab_Results row
```

This means the user can save the same report again after correcting values without creating duplicate measurements.

### Updated_DateTime

`Updated_DateTime` is system-generated by the backend.

The frontend does not supply this value.

Format:

```text
YYYY-MM-DD HH:MM:SS
```

When a report or result is created, the backend sets `Updated_DateTime`.

When an existing report or result is updated, the backend replaces it with the new update time.

### Save Response

The endpoint returns the saved report together with all non-empty results that were saved or updated.

### Important Distinction: Extract vs Save

PDF extraction and saving are separate operations.

```text
POST /health/lab-reports/extract
        ↓
Extract data from PDF
        ↓
Return data to frontend
        ↓
Nothing saved


POST /health/lab-reports/save
        ↓
Save reviewed frontend data
        ↓
Lab_Reports + Lab_Results updated
```

This separation allows the user to review and correct AI-extracted values before anything is permanently stored.