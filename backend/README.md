# Personal Assistant Backend

The backend is a FastAPI REST API, served under `/health`. It is the **only** part of the system
that reads or writes the Google Sheet, and it uses OpenAI (`gpt-5-mini`, set by
`LAB_EXTRACTION_MODEL` in `labs/lab_extraction_service.py`) to extract results from lab report PDFs.

Its clients are the frontend (http://localhost:5173, allowed through CORS; see
`CORS_ALLOWED_ORIGINS`) and the data importer.

---

## How a Request Flows

Example: `GET /health/nutrition-metrics/2026-10-08`

```text
Client (frontend or data importer)
   │
   ▼
app/modules/health/api.py
  get_nutrition_metric()                      ── validates the request and the response model
   │
   ▼
NutritionMetricsService
  (nutrition_metrics/nutrition_metrics_service.py)        ── business logic
   │
   ▼
NutritionMetricsGoogleSheetsRepository
  (nutrition_metrics/nutrition_metrics_google_sheets_repository.py)   ── Sheet reads and writes
   │
   ▼
app/database/sheets_client.py                 ── authenticated, cached spreadsheet client
   │
   ▼
Google Sheet: Nutrition_Metrics worksheet
   │
   ▼  (row converted into a NutritionMetrics model, from nutrition_metrics_schema.py)
   │
JSON response
```

What each layer does:

- **API (`api.py`):** defines the endpoints, validates requests and responses with Pydantic models,
  and returns the right HTTP status codes (for example `404` when a record does not exist).
- **Service (`*_service.py`):** business logic, such as the upsert: update the record if it exists,
  otherwise create it. It does not know how data is stored.
- **Repository (`*_google_sheets_repository.py`):** the only code that knows about Google Sheets. It
  converts worksheet rows into models and models into rows.
- **Schema (`*_schema.py`):** the Pydantic model shared by all layers.

Why the code is organised this way:

- **By feature, not by layer.** Each metric module has its own folder containing its schema, service
  and repository, so everything for one feature is in one place and new modules can be added without
  touching existing ones.
- **Separate layers.** Keeping API, business logic and data access apart makes each layer easy to
  test on its own.
- **Google Sheets is isolated in the repositories.** Moving to a real database later would mean
  replacing the repository layer, not rewriting the services or the API.

---

## Code Map

```text
backend/
├── app/
│   ├── main.py                  FastAPI app, CORS, root endpoint, includes the health router,
│   │                            loads the data cache at startup
│   ├── config.py                Settings loaded from .env (the `settings` object)
│   ├── data_cache.py            In-memory cache of whole worksheets for the dashboards
│   ├── database/
│   │   ├── sheet_formats.py     Date and date-time formats used in the Sheet (DATE_FORMAT, DATETIME_FORMAT)
│   │   └── sheets_client.py     Authenticated, cached Google Sheets client (retries when rate-limited)
│   ├── ai/
│   │   └── openai_client.py     OpenAI client used for lab PDF extraction
│   └── modules/health/
│       ├── api.py               Every /health endpoint (metrics, Overview and labs)
│       ├── dashboard/           The Overview page: goals, summary schema, DashboardService, and
│       │                        highlights.py (the highlight rules, in display order)
│       ├── body_measurements_metrics/  ┐
│       ├── health_metrics/             │  One folder per metric module, each with:
│       ├── heart_rate_notifications/   │    *_schema.py
│       ├── nutrition_metrics/          │    *_service.py
│       ├── sleep_metrics/              │    *_google_sheets_repository.py
│       ├── workout_metrics/            ┘
│       └── labs/                Lab reports, results and marker configuration
│                                (different pattern, see "Labs Module" below)
├── tools/                       Live connectivity checks (Google Sheets, OpenAI)
├── tests/                       One folder per module, plus helpers/test_data.py
├── requirements.txt
└── .env                         Local settings (not committed)
```

The **labs** module is organised differently: it uses module-level functions instead of service and
repository classes, and some endpoints in `api.py` call `lab_repository.py` directly.

---

## Modules and Endpoints

All endpoints are prefixed with `/health`. Swagger UI at http://127.0.0.1:8000/docs lists them all.

| Module | Endpoints | Worksheet setting | Records |
|---|---|---|---|
| Body Measurements | `GET /body-measurements`, `GET /body-measurements/{measurement_date}`, `POST`, `PUT` | `HEALTH_BODY_MEASUREMENTS_WORKSHEET` | One per date |
| Health Metrics | `GET /health-metrics`, `GET /health-metrics/{metric_date}`, `POST`, `PUT` | `HEALTH_HEALTH_METRICS_WORKSHEET` | One per date |
| Nutrition Metrics | `GET /nutrition-metrics`, `GET /nutrition-metrics/{metric_date}`, `POST`, `PUT` | `HEALTH_NUTRITION_METRICS_WORKSHEET` | One per date |
| Sleep Metrics | `GET /sleep-metrics`, `GET /sleep-metrics/{metric_date}`, `POST`, `PUT` | `HEALTH_SLEEP_METRICS_WORKSHEET` | One per date |
| Workout Metrics | `GET /workout-metrics?workout_date=`, `GET /workout-metric?workout_start_time=`, `POST`, `PUT` | `HEALTH_WORKOUT_METRICS_WORKSHEET` | One per workout, matched by start time |
| Heart Rate Notifications | `GET /heart-rate-notifications?notification_date=`, `GET /heart-rate-notification?start_time=`, `POST`, `PUT` | `HEALTH_HEART_RATE_NOTIFICATIONS_WORKSHEET` | One per notification, matched by start time. `readings` is the heart rate values as text, e.g. `"39, 40, 39"` |
| Labs | Lab reports, lab results, marker definitions, reference ranges, interpretations, `POST /lab-reports/extract`, `POST /lab-reports/save` | `LAB_*_WORKSHEET` settings | See [Labs Module](#labs-module) |
| Overview | `GET /dashboard/summary?period=day\|week\|month&date=YYYY-MM-DD&refresh=true` (`date` defaults to today; `refresh` is optional), `GET /dashboard/cache` (the cache's state) | Reads the six metric worksheets through the data cache | Read-only. See [Overview and the Data Cache](#overview-and-the-data-cache) |

Also: `GET /` (API is running) and `GET /health/status` (health module status).

For the metric modules, `POST` creates a record and `PUT` creates or updates one (an upsert). The
frontend and the data importer both use `PUT`.

---

## Overview and the Data Cache

`GET /health/dashboard/summary` returns everything the Overview page shows for a day, a week
(Monday to Sunday) or a calendar month. The rules (averages over days with data, comparisons,
coverage, body trends) are in `modules/health/dashboard/dashboard_service.py`; the design is in
[`docs/dashboard/overview-design.md`](../docs/dashboard/overview-design.md).

Each request needs all six metric worksheets, so they are kept in memory by `DataCache`
(`app/data_cache.py`), created once in `api.py`:

- **Startup:** `main.py` loads the cache in a background thread, so the backend starts straight
  away. If loading fails, it prints a message and the first Overview request loads it.
- **Saves:** every metric `POST` and `PUT` marks its worksheet as stale after a successful save,
  so the next Overview request reads that worksheet again. Imports save through these endpoints,
  so they show straight away.
- **Expiry:** each worksheet is read again after 12 hours (`CACHE_DURATION`).
- **Refresh:** `refresh=true` reads every worksheet again, for edits made directly in Google Sheets.

**Checking that it works:**

- The backend's terminal shows every read of a worksheet and why it happened, e.g.
  `Data cache: read sleep (610 rows) in 0.8s (marked stale by a save)`. The reasons are `startup`,
  `refresh`, `marked stale by a save`, `older than 12h` and `not loaded yet`. Using the cache prints
  nothing.
- Loading at startup and refreshing are bracketed by a line before and after, e.g.
  `Data cache: loading all 6 sources at startup...` and
  `Data cache: loaded all 6 sources in 3.8s (startup)`, or
  `Data cache: could not load at startup; it will load on the next request. (...)`.
- Clicking around the Overview prints no `Google Sheets: ...` lines (see
  [Rules Shared by the Metric Modules](#rules-shared-by-the-metric-modules)): its data comes from
  the cache.
- `GET /health/dashboard/cache` reports, for each worksheet, whether it is loaded, its row count,
  when it was read, when it expires and whether it is stale. It returns no health data and never
  reads the Sheet.

Only the dashboards use the cache; the log pages always read the Sheet. The cache lives inside the
backend process, so run the backend as **a single process** (one worker). With several workers or
copies, each would have its own cache, and a save would only mark one of them stale.

---

## Rules Shared by the Metric Modules

These apply to all six metric repositories (including Heart Rate Notifications):

- **`PUT` is a partial update.** When a record already exists, only fields with a value overwrite it.
  A field sent as `null` keeps its existing value, so a field cannot be cleared through the API.
- **`POST` appends a new row without checking for duplicates.** Use `PUT` unless you are sure the
  record does not exist.
- **Dates are stored in the Sheet as `"%B %d, %Y"`** (for example `"October 08, 2026"`), and date-times as
  `"%B %d, %Y %H:%M:%S"`. Both formats are defined once, in `app/database/sheet_formats.py`.
- **The last column is `Updated_DateTime`,** set to the time of each write.
- **Reads use header names; writes use column positions.** Each repository writes a whole row with a
  hardcoded range (for example `A:N` for Nutrition Metrics). Adding, removing or reordering
  worksheet columns therefore requires a matching code change.
- **Only repositories touch the Sheet.** Google Sheets access lives only in the
  `*_google_sheets_repository.py` files, `labs/lab_repository.py` and `database/sheets_client.py`.
- **Rate limits are retried, not failed.** Google Sheets allows a limited number of requests per
  minute, which bulk imports can exceed. `RetryingHTTPClient` in `database/sheets_client.py` then
  prints a message in the backend's terminal (for example `Google Sheets rate limit reached;
  waiting 10s before retrying (attempt 2 of 4)...`), waits and retries: 5, 10, 20 and 40 seconds,
  about 75 seconds in total. Temporary Google server errors (5xx) are retried the same way; other
  errors are raised immediately.
- **Every Google Sheets request is logged.** `RetryingHTTPClient` also prints one line per request
  that succeeds, naming the worksheet, e.g. `Google Sheets: read Workout_Metrics in 0.6s` or
  `Google Sheets: write Sleep_Metrics in 0.4s` (`read spreadsheet details` is gspread looking up a
  worksheet). Every repository, the labs code and the data cache use this client, so this shows
  each time the backend actually calls Google. A long import makes thousands of requests: set
  `LOG_GOOGLE_SHEETS_REQUESTS=false` in `.env` first.

### Missing Sleep and Workout Durations

Health Auto Export sometimes reports a sleep total or workout duration of `0` even though the start
and end times are known. When a sleep record's `total_sleep_duration_hr` or a workout's
`workout_duration_min` is sent as `0` or empty, the service (`SleepMetricsService`,
`WorkoutMetricsService`) applies this rule before saving:

1. **A real stored value (> 0) is kept.** The incoming `0` or empty value never overwrites it.
2. **Otherwise the duration is calculated** from the start and end times (sent, or else stored) when
   the span is plausible: 1 to 16 hours for sleep (in hours, 2 decimals), 1 minute to 24 hours for
   a workout (in whole minutes). A calculated sleep total is the time between start and end, so it
   includes any time awake.
3. **Otherwise the value is saved exactly as sent**, so an implausible span keeps its `0`.

A real incoming value is always saved as sent. Existing rows saved before this rule are not changed.

---

## Setup

### Prerequisites

- Python 3.10+
- pip

### First Time Setup

From the repository root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

When you install a new package, update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

### Configuration

Settings are loaded from `backend/.env` by `app/config.py` and are available throughout the backend
as `settings`. All of the following are required, except `CORS_ALLOWED_ORIGINS` and
`LOG_GOOGLE_SHEETS_REQUESTS`:

| Variable | Purpose |
|---|---|
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path to the Google service account JSON, e.g. `credentials/service_account.json` |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | The spreadsheet ID, found in the Google Sheet's URL |
| `HEALTH_BODY_MEASUREMENTS_WORKSHEET` | Worksheet name for Body Measurements |
| `HEALTH_HEALTH_METRICS_WORKSHEET` | Worksheet name for Health Metrics |
| `HEALTH_NUTRITION_METRICS_WORKSHEET` | Worksheet name for Nutrition Metrics |
| `HEALTH_SLEEP_METRICS_WORKSHEET` | Worksheet name for Sleep Metrics |
| `HEALTH_WORKOUT_METRICS_WORKSHEET` | Worksheet name for Workout Metrics |
| `HEALTH_HEART_RATE_NOTIFICATIONS_WORKSHEET` | Worksheet name for Heart Rate Notifications (`HR_Rate_Notifications`) |
| `LAB_REPORTS_WORKSHEET` | Worksheet name for lab reports |
| `LAB_RESULTS_WORKSHEET` | Worksheet name for lab results |
| `LAB_MARKER_DEFINITIONS_WORKSHEET` | Worksheet name for lab marker definitions |
| `LAB_MARKER_REFERENCE_RANGES_WORKSHEET` | Worksheet name for lab marker reference ranges |
| `LAB_MARKER_INTERPRETATIONS_WORKSHEET` | Worksheet name for lab marker interpretations |
| `OPENAI_API_KEY` | OpenAI API key, used for lab PDF extraction |
| `CORS_ALLOWED_ORIGINS` | **Optional.** Browser origins allowed to call the API (the frontend's address). Defaults to `["http://localhost:5173"]`; set a JSON list to change it, e.g. `["http://localhost:5173","http://127.0.0.1:5173"]` |
| `LOG_GOOGLE_SHEETS_REQUESTS` | **Optional.** Print a line for every Google Sheets request (see "Every Google Sheets request is logged"). Defaults to `true`; set `false` before a long import |

Create `.env` using the variable names in the table above. If one is missing, the backend fails at
startup with an error naming it. `.env` and the credentials file are ignored by git.

**Why the spreadsheet is opened by ID:** `database/sheets_client.py` uses
`open_by_key(GOOGLE_SHEETS_SPREADSHEET_ID)` rather than opening the spreadsheet by name. Opening by
name searches Google Drive, which needs the Drive API and wider permissions. Opening by ID needs only
the Google Sheets permission (the `spreadsheets` scope), keeps working if the spreadsheet is renamed,
and skips the Drive search. Do not switch it back to `client.open("<name>")`.

### Run the Backend

```bash
fastapi dev app/main.py
```

`fastapi dev` restarts the backend whenever a file under `backend/` changes. During a long import,
start it with `fastapi dev app/main.py --no-reload` instead, so code changes do not restart it
mid-import (a restart makes the file being imported fail; it is retried on the next run).

Then check:

| URL | Expected result |
|---|---|
| http://127.0.0.1:8000 | Personal Assistant API is running |
| http://127.0.0.1:8000/health/status | Health module status |
| http://127.0.0.1:8000/health/nutrition-metrics | All Nutrition Metrics records |
| http://127.0.0.1:8000/docs | Swagger UI with every endpoint |

### Connectivity Tools

The scripts in `tools/` check the live connections. They use the real Google Sheet and the real
OpenAI API, so only run them when you mean to:

```bash
python -m tools.test_google_sheets      # Google Sheets connection
python -m tools.test_openai_config      # OpenAI configuration
python -m tools.test_openai_client      # OpenAI API call
```

---

## Testing

The backend is tested at multiple levels. Each level focuses on a different part of the application.

#### Repository Tests

Repository tests verify that the repository correctly reads from and writes to the data source.

Example:
- `get_nutrition_metrics()` returns all Nutrition Metrics records.
- `update_body_measurement()` updates the correct worksheet row.

#### Repository Helper Tests

Repository helper tests verify the internal helper methods used to convert data between Google Sheets and the application's models.

Example:
- `_row_to_nutrition_metrics()` converts a worksheet row into a `NutritionMetrics` object.
- `_nutrition_metric_to_row()` converts a `NutritionMetrics` object into a worksheet row.

#### Service Tests

Service tests verify the application's business logic and ensure that the Service layer correctly interacts with the Repository layer.

Example:
- `NutritionMetricsService.get_nutrition_metrics()` returns all Nutrition Metrics from the repository.
- `NutritionMetricsService.upsert_nutrition_metric()` updates the existing record, or creates one if none exists.

#### API Tests

API tests verify the FastAPI endpoints by sending HTTP requests and validating the responses.

Example:
- `GET /health/nutrition-metrics` returns a list of Nutrition Metrics.
- `POST /health/nutrition-metrics` creates a new Nutrition Metrics record and returns the correct status code.

### Running Tests Safely

**Live tests are opt-in.** Tests in files ending in `_e2e.py` are marked `e2e` by
`tests/conftest.py` and skipped by default (`pytest.ini` sets `addopts = -m "not e2e"`). These are
the end-to-end tests, which read and write the real Google Sheet through a running backend,
`tests/dashboard/test_dashboard_e2e.py`, which only reads it (the Overview endpoint, checking rules
that hold for any data), `tests/dashboard/test_data_cache_e2e.py`, which checks the cache through
`GET /health/dashboard/cache` (it reads, and its save test writes and deletes one 2099 Sleep row),
and `tests/labs/test_lab_extraction_e2e.py`, which reads the live Sheet and calls OpenAI.

The end-to-end tests create rows with clearly fake values (the year 2099, keys starting with
`TEST_`, file names starting with `api_test_`) and delete them afterwards. Before deleting
anything, each cleanup calls a guard from `tests/helpers/e2e_guards.py`, which stops the test if
the value it would match on is not one of these test values, so a mistake in a test can never
delete real rows.

Run the mocked tests from `backend/`. The fake credentials are an extra safety net: any call that is
not mocked fails instead of reaching a real service.

```bash
GOOGLE_SERVICE_ACCOUNT_FILE=/nonexistent/offline.json OPENAI_API_KEY=offline-invalid-key \
  .venv/bin/python -m pytest -q -p no:cacheprovider
```

Run a single file or test with the same environment variables:

```bash
GOOGLE_SERVICE_ACCOUNT_FILE=/nonexistent/offline.json OPENAI_API_KEY=offline-invalid-key \
  .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/nutrition_metrics/test_nutrition_metrics_google_sheets_repository.py::test_get_nutrition_metrics
```

Add `-v` for detailed output.

To run live tests deliberately (with the backend running, and the real `.env` credentials):

```bash
.venv/bin/python -m pytest -m e2e                                   # all live tests
.venv/bin/python -m pytest -m e2e tests/nutrition_metrics/          # live tests in one folder
```

Passing an `_e2e.py` file path without `-m e2e` runs nothing, because its tests are deselected.

---

## Adding a New Field to an Existing Metric

Example: adding a column to Nutrition Metrics.

1. **Google Sheet**
   - Add the new column to the worksheet.

2. **Schema** (`nutrition_metrics/nutrition_metrics_schema.py`)
   - Add the new field to the Pydantic model.

3. **Repository** (`nutrition_metrics/nutrition_metrics_google_sheets_repository.py`)
   - Update `_row_to_nutrition_metrics()` to read the new column by its header name.
   - Update `_nutrition_metric_to_row()` to write the new column in the correct position.
   - Update the hardcoded update range (for example `A:N`) to include the new column.

4. **API and Service**
   - No changes are needed if the endpoints already use the updated schema.
   - Verify the new field appears in Swagger and in API responses.

5. **Configuration**
   - No changes unless the field needs new configuration.

6. **Testing**
   - Update `tests/helpers/test_data.py` so fake worksheet rows and generated models include the
     new field.
   - Update the repository helper tests:
     - `_row_to_nutrition_metrics()` reads the new field correctly.
     - `_nutrition_metric_to_row()` writes the new field in the correct position.
   - Update the repository tests to check the new field is returned.
   - Run the module's tests first, then the full safe test suite.

7. **Other parts and docs**
   - Update the frontend and the data importer if they use the field.
   - Update any README that describes the affected fields.

## Renaming a Column in a Worksheet

1. **Google Sheet**
   - Rename the column.

2. **Repository**
   - Update the header name used in `_row_to_<entity>()`. Writes use column positions, so they do
     not need to change unless the column also moves.

3. **Testing**
   - Update the header name in `tests/helpers/test_data.py`.
   - Verify GET still returns the correct data, and PUT still writes to the correct column.

## Adding a New Metric Module (New Worksheet)

1. **Google Sheet**
   - Create the new worksheet, with `Date` first and `Updated_DateTime` last, like the other
     metric worksheets.

2. **Configuration**
   - Add a worksheet setting to `.env` and the matching field in `app/config.py`.

3. **Module folder** (`app/modules/health/<name>/`), following an existing metric module:
   - `<name>_schema.py`: the Pydantic model.
   - `<name>_google_sheets_repository.py`: get the worksheet; read all records and one record;
     create and update records; convert rows to models and back.
   - `<name>_service.py`: get, create and upsert, delegating to the repository.

4. **API** (`app/modules/health/api.py`)
   - Add `GET`, `POST` and `PUT` endpoints, plus a tag in `tags_metadata` in `app/main.py`.
   - Add a loader for the worksheet to `data_cache`, and call `data_cache.mark_stale("<source>")`
     in the `POST` and `PUT` endpoints after the save, so the dashboards see changes.
   - Add the new save routes to `SAVE_ROUTES` in `tests/dashboard/test_dashboard_api.py`. A test
     fails for any metric save route that is not listed there.

5. **Testing**
   - Add `tests/<name>/` with repository, service and API tests, using `tests/helpers/test_data.py`.
   - End-to-end tests use the real Sheet: add them only deliberately, in a file ending in
     `_e2e.py`, so they are skipped by default. Use 2099 dates or `TEST_` keys for test data, and
     call the matching guard from `tests/helpers/e2e_guards.py` at the start of the cleanup.

6. **Docs**
   - Add the module to the [Modules and Endpoints](#modules-and-endpoints) table above.

---

# Labs Module

The Labs module follows a different code pattern from the metric modules: module-level functions in
`lab_service.py`, `lab_extraction_service.py` and `lab_repository.py` instead of service and
repository classes, and some endpoints in `api.py` call `lab_repository.py` directly.

## Lab Module Overview

The Lab module stores bloodwork and other laboratory results and provides the configuration data required to identify and interpret those results.

The module uses five main entities:

| Entity | Purpose | How Data Is Added |
|---|---|---|
| `Lab_Reports` | Stores one record for each laboratory report | Created when a user saves a manually entered or PDF-extracted report |
| `Lab_Results` | Stores the individual marker results belonging to a laboratory report | Created when a user saves a manually entered or PDF-extracted report |
| `Lab_Marker_Definitions` | Stores the master list of laboratory markers supported by the application | Managed through the Lab administration UI |
| `Lab_Marker_Reference_Ranges` | Stores reference ranges for markers based on factors such as gender and age | Managed through the Lab administration UI |
| `Lab_Marker_Interpretations` | Stores interpretation ranges and labels used to interpret marker values | Managed through the Lab administration UI |

### Two Types of Lab Data

The five entities are divided into two broad groups.

#### 1. Lab Configuration / Master Data

The following entities define the laboratory markers understood by the application and how their values should be interpreted:

```text
Lab_Marker_Definitions
Lab_Marker_Reference_Ranges
Lab_Marker_Interpretations
```

This data is maintained through the Lab administration UI. It is not created when a laboratory report is uploaded or saved.

##### `Lab_Marker_Definitions`

Defines the laboratory markers supported by the application.

Examples include:

```text
LDL Cholesterol
HDL Cholesterol
Fasting Glucose
Vitamin D
Vitamin B12
```

Each definition provides a canonical `Marker_Key` and supporting metadata such as the display name, category, panel, default unit, and active status. The canonical key allows results from different laboratories, which may use different reported names, to refer to the same marker consistently.

`Lab_Marker_Definitions` is also used during PDF extraction. Active marker definitions are supplied to the extraction process so that reported test names can be mapped to existing `Marker_Key` values. The extraction process never invents new marker keys; tests that cannot be mapped confidently are returned as unmapped results.

##### `Lab_Marker_Reference_Ranges`

Defines the expected or normal reference ranges for laboratory markers.

Reference ranges may vary according to factors such as:

- Gender
- Minimum age
- Maximum age
- Unit
- Laboratory or source

This data allows the application to select an applicable reference range and determine whether a result is below, within, or above that range.

Each reference-range record belongs to a marker definition through its `Marker_Key`.

##### `Lab_Marker_Interpretations`

Defines application-level interpretation bands and labels for marker values.

Examples include:

```text
Low
Optimal
Normal
Borderline High
High
Deficient
Insufficient
```

Interpretations can be used to present a more meaningful description of a value than a simple in-range or out-of-range status. Each interpretation record belongs to a marker definition through its `Marker_Key`.

Reference ranges and interpretations serve different purposes:

- A reference range describes the expected range supplied by a laboratory or configured source.
- An interpretation assigns a descriptive application label to a value or value range.

#### 2. Actual Laboratory Report Data

The following entities contain reports saved by the user and the individual results within those reports:

```text
Lab_Reports
Lab_Results
```

These records are created only when the user saves a report. A report may be entered manually or populated from a PDF extraction for review before saving.

##### `Lab_Reports`

Stores one parent record for each saved laboratory report.

A report record contains report-level information such as:

- Report identifier
- Report date
- Collection date
- Report date and time
- Report type
- Laboratory name
- Source file name
- Other report-level metadata

`Lab_Reports` does not store the individual test values. Those values are stored in `Lab_Results`.

##### `Lab_Results`

Stores the individual test or marker results that belong to a saved laboratory report.

Each result is linked to:

- One report through its report identifier
- One supported marker through its `Marker_Key`

A result can store information such as:

- The test name as reported by the laboratory
- A numerical value
- A text value for non-numeric results
- The reported unit
- Other result-level metadata

Numeric results are stored separately from text results. For example, `95` may be stored as a numerical value, while values such as `Negative`, `Nil`, or `1 to 2` may be stored as text.

### Entity Relationships

The main relationships are:

```text
Lab_Reports
    └── Lab_Results

Lab_Marker_Definitions
    ├── Lab_Results
    ├── Lab_Marker_Reference_Ranges
    └── Lab_Marker_Interpretations
```

In practical terms:

- One `Lab_Reports` record can have many `Lab_Results` records.
- Each `Lab_Results` record belongs to one `Lab_Reports` record.
- Each mapped `Lab_Results` record refers to one `Lab_Marker_Definitions` record through `Marker_Key`.
- One `Lab_Marker_Definitions` record can have many `Lab_Results` records across different reports.
- One `Lab_Marker_Definitions` record can have multiple `Lab_Marker_Reference_Ranges` records.
- One `Lab_Marker_Definitions` record can have multiple `Lab_Marker_Interpretations` records.

### Google Sheets Worksheets

The entities are stored in the following Google Sheets worksheets:

| Entity | Worksheet Name |
|---|---|
| `Lab_Reports` | `Lab_Reports` |
| `Lab_Results` | `Lab_Results` |
| `Lab_Marker_Definitions` | `Lab_Marker_Definitions` |
| `Lab_Marker_Reference_Ranges` | `Lab_Marker_Reference_Ranges` |
| `Lab_Marker_Interpretations` | `Lab_Marker_Interpretations` |

### PDF Extraction and Saving Scope

PDF extraction and report saving mainly concern `Lab_Reports` and `Lab_Results`:

- PDF extraction reads report metadata and individual test results from an uploaded file.
- Extraction returns structured data to the UI but does not save it to Google Sheets.
- The user can review and edit the extracted data before saving.
- Saving creates one `Lab_Reports` record and the associated `Lab_Results` records.

`Lab_Marker_Definitions` also participates in extraction, but only as existing master data used to map reported test names to supported `Marker_Key` values. Uploading or saving a report does not create or modify marker definitions, reference ranges, or interpretations.




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