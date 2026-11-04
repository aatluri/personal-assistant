# Data Importer

The data importer reads the daily JSON exports that the **Health Auto Export** iOS app writes to
Google Drive (through its automation), converts them into the payloads the backend expects, and
sends them to the backend REST API.

It never touches the Google Sheet. All writes go through the backend.

---

## How It Works

```text
Health Auto Export (automation)
        │
        ▼
Google Drive incoming folder
  HealthMetrics-YYYY-MM-DD.json
  WorkoutMetrics-YYYY-MM-DD.json
        │
        ▼
PUT /health/import/...  (called manually)
        │
        ▼
orchestrator ──► importer + mapping (one per metric) ──► BackendClient ──► backend PUT /health/...
        │
        └── renames the file in Drive:
              PROCESSED_<name>  on success
              FAILED_<name>     on failure (retried next run)

POST /health/archive  (called manually)
        └── moves PROCESSED_ files older than N days to the processed folder
```

---

## Code Map

| Path | Role |
|---|---|
| `app/main.py` | **Start here.** FastAPI endpoints for importing and archiving. |
| `app/modules/health/orchestrators/` | Per-file loop: list files in Drive, run the importers, rename each file `PROCESSED_` or `FAILED_`. |
| `app/modules/health/importers/` | One importer per metric. Turns the export JSON into a backend payload and sends it. |
| `app/modules/health/mappings/` | For each backend field: the source metric name, which value to read, and any type or unit conversion. |
| `app/modules/health/archivers/file_archiver.py` | Moves old `PROCESSED_` files into the processed folder. |
| `app/modules/health/constants.py` | The `PROCESSED_` and `FAILED_` file prefixes. |
| `app/clients/google_drive_client.py` | Lists, reads, renames and moves files in Google Drive. |
| `app/clients/backend_client.py` | Sends payloads to the backend API. |
| `app/config.py` | Settings loaded from `.env`. |
| `scripts/import_historical_health_metrics.py` | One-off script for importing a large backlog of Health Metrics files. |
| `tests/` | Unit tests (mocked) and `tests/e2e/` (live services). |

---

## What Gets Imported

| File | Importers | Backend endpoint(s) | Records |
|---|---|---|---|
| `HealthMetrics-YYYY-MM-DD.json` | health, nutrition, sleep, body measurements | `PUT /health/health-metrics`, `/health/nutrition-metrics`, `/health/sleep-metrics`, `/health/body-measurements` | One record per date for each metric |
| `WorkoutMetrics-YYYY-MM-DD.json` | workouts | `PUT /health/workout-metrics` | One record per workout; the backend matches existing workouts by start time |

Every payload is sent with `source: "Health Auto Export"`.

A metric that is missing from a file is normal. That importer simply sends nothing, and the file is
not treated as failed.

---

## File Lifecycle

- **Filenames:** only `HealthMetrics-YYYY-MM-DD.json` and `WorkoutMetrics-YYYY-MM-DD.json` are
  recognised. Files are processed **oldest first**, using the date in the filename.
- **`PROCESSED_` files** are skipped. Imported files stay in the incoming folder with this prefix
  until they are archived.
- **`FAILED_` files** are retried on every run. On success the `FAILED_` prefix is replaced with
  `PROCESSED_`.
- **A file fails as a whole.** If any one of its imports fails (for example sleep), the file is
  renamed `FAILED_`. Imports from that file that already succeeded are **not** rolled back.
  Retrying is safe because the backend updates the existing record instead of creating a duplicate.
- **Archiving** only happens when `POST /health/archive` is called. A file is moved when the date in
  its filename is older than `DATA_IMPORTER_ARCHIVE_AFTER_DAYS` (default 30), regardless of when it
  was processed.
- **`TEST_` files** are skipped by the historical import script only. The regular import endpoints
  do not skip them.

---

## Unit and Type Conversions

Everything is stored in metric units, and conversions happen here, not in the backend.

| Backend field | Conversion | Defined in |
|---|---|---|
| `water_ml` | US fl oz → ml | nutrition mapping (`fl_oz_us_to_ml`) |
| `weight_kg` | lb → kg | body measurements mapping (`lb_to_kg`) |
| `workout_duration_min` | seconds → whole minutes | workout importer code |
| `distance_km` | miles → km | workout importer code |
| `avg_speed_kmph` | m/s → km/h | workout importer code |

Rounding:

- **Health and nutrition** values are rounded to whole numbers (`value_type: "int"`).
- **Body measurements** are kept as decimals (`value_type: "float"`).
- **Sleep and workout** numbers are rounded to 2 decimal places.

Timestamps (sleep and workout start/end times) are converted to ISO 8601. The record date comes from
the source data's timestamp, not from the filename.

---

## Running It

The backend must be running on port 8000 first. Then, from `data_importer/`:

```bash
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uvicorn app.main:app --reload --port 8001
```

> **Warning:** importing writes to the real Google Sheet (through the backend) and renames files in
> the real Google Drive folders. Archiving moves real Drive files.

The endpoints are called manually, either from Swagger UI at http://127.0.0.1:8001/docs or with
`curl`:

```bash
# Check the service is running
curl http://127.0.0.1:8001/health

# Import every waiting Health Metrics file (including FAILED_ retries)
curl -X PUT http://127.0.0.1:8001/health/import/health-metrics

# Import one specific file
curl -X PUT "http://127.0.0.1:8001/health/import/health-metrics?file_name=HealthMetrics-2026-10-12.json"

# Import every waiting Workout Metrics file
curl -X PUT http://127.0.0.1:8001/health/import/workout-metrics

# Archive PROCESSED_ files older than DATA_IMPORTER_ARCHIVE_AFTER_DAYS
curl -X POST http://127.0.0.1:8001/health/archive
```

Each import returns the number of files processed and the backend's response for each metric.

---

## Historical Import Script

`scripts/import_historical_health_metrics.py` imports a large backlog of **Health Metrics** files
(not workouts), oldest first. It reuses the same orchestrator as the import endpoint, one file at a
time.

```bash
# from data_importer/, with .venv activated
python -m scripts.import_historical_health_metrics
```

- Processes unprocessed and `FAILED_` files; skips `PROCESSED_` and `TEST_` files.
- Limits are constants at the top of the script (edit the file to change them):
  - `MAX_FILES = 500`: maximum files per run.
  - `BATCH_SIZE = 15` and `BATCH_DELAY_SECONDS = 60`: pause for a minute after every 15 files to
    stay within Google Sheets API quotas.

The same real-data warning applies.

---

## Configuration

Settings are loaded from `data_importer/.env` by `app/config.py`. Create `.env` using the variable
names in the table below; if a required one is missing, the importer fails at startup with an error
naming it.

| Variable | Purpose |
|---|---|
| `PERSONAL_ASSISTANT_API_URL` | Backend base URL, normally `http://127.0.0.1:8000` |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path to the Google service account JSON, e.g. `credentials/service_account.json` |
| `HEALTH_METRICS_DRIVE_FOLDER_ID` | Drive folder where Health Metrics files arrive |
| `HEALTH_METRICS_PROCESSED_DRIVE_FOLDER_ID` | Drive folder where archived Health Metrics files are moved |
| `WORKOUT_METRICS_DRIVE_FOLDER_ID` | Drive folder where Workout Metrics files arrive |
| `WORKOUT_METRICS_PROCESSED_DRIVE_FOLDER_ID` | Drive folder where archived Workout Metrics files are moved |
| `DATA_IMPORTER_ARCHIVE_AFTER_DAYS` | Age in days before a processed file is archived (default `30`) |

`.env` and `credentials/` are ignored by git.

---

## Testing

Safe, mocked tests (from `data_importer/`). The fake values make any unmocked call fail instead of
reaching Google Drive or the backend:

```bash
GOOGLE_SERVICE_ACCOUNT_FILE=/nonexistent/offline.json PERSONAL_ASSISTANT_API_URL=http://127.0.0.1:9 \
  .venv/bin/python -m pytest tests -q -p no:cacheprovider --ignore=tests/e2e
```

These cover the importers, orchestrators, archiver and backend client, using the sample exports in
`tests/test_data/`.

> **Warning:** `tests/e2e/` uses live services. These tests read real Drive files, create and delete
> `TEST_*` files in Drive, and write to the real Sheet through the backend. Run them only
> deliberately.

---

## Adding a New Metric Field

1. **Backend first.** The field must already exist in the backend schema and Sheet.
2. **Add a mapping entry** in the matching file under `app/modules/health/mappings/`, with
   `source_name` (the Health Auto Export metric), `value_field` (usually `qty`), and any
   `value_type` or `conversion`.
3. **New kind of conversion?** Add its code to the importer, since importers only apply the
   conversions they already know about.
4. **Update the tests:** the importer test and, if needed, the sample export in `tests/test_data/`.
5. **Run the safe tests** above.

---

## Rules

- **Never write to the Google Sheet directly.** Always go through `BackendClient`.
- **Unit conversions belong here,** not in the backend. Everything the backend stores is metric.
- **Missing metrics are normal.** A file without, say, sleep data still imports successfully.
