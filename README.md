# Personal Assistant

A single-user, local-only application for logging and reviewing personal health data: nutrition,
sleep, workouts, body measurements, general health metrics and lab results.

A Google Sheet is the application's data store.

---

## How It Fits Together

```text
Health Auto Export JSON files ──► Google Drive folders
                                       │
                                       ▼
                           data_importer (FastAPI :8001)
                                       │  HTTP only
                                       ▼
frontend (React :5173) ──────► backend (FastAPI :8000) ──► Google Sheet
                                       │
                                       └──► OpenAI (lab PDF extraction)
```

- **Two ways data gets in:** the user enters it manually in the frontend, or the data importer
  reads exported JSON files from Google Drive.
- **The backend is the only part that touches the Google Sheet.** The frontend and the data importer
  both go through the backend's REST API.
- **Lab reports** are sent to the backend as PDFs, which uses OpenAI to extract the results before
  they are saved.

---

## The Parts

| Folder | Purpose | Technology | Runs on |
|---|---|---|---|
| [`frontend/`](frontend/README.md) | User interface for viewing and logging data | React, TypeScript, Vite | http://localhost:5173 |
| [`backend/`](backend/README.md) | REST API, business logic and all Google Sheets access | Python, FastAPI, Pydantic | http://127.0.0.1:8000 (Swagger UI at `/docs`) |
| [`data_importer/`](data_importer/README.md) | Imports exported health and workout files from Google Drive into the backend | Python, FastAPI | http://127.0.0.1:8001 |
| [`docs/`](docs/README.md) | Architecture decision records and UI design notes | Markdown | — |

The data importer exposes two import endpoints:

- `PUT /health/import/health-metrics`: Health Metrics export files, each of which can contain
  health, nutrition, sleep and body measurement data
- `PUT /health/import/workout-metrics`: Workout Metrics export files

---

## Quick Start

First-time setup (virtual environments, dependencies, `.env` files and credentials) is described in
the [backend](backend/README.md) and [frontend](frontend/README.md) READMEs.

Start each part in its own terminal. The backend and the data importer each have their own virtual
environment (`.venv`), which must be activated first.

```bash
# backend/
source .venv/bin/activate        # Windows: .venv\Scripts\activate
fastapi dev app/main.py

# frontend/
npm run dev

# data_importer/ (only needed when importing files)
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uvicorn app.main:app --reload --port 8001
```

The data importer reaches the backend through `PERSONAL_ASSISTANT_API_URL` in its `.env`, which
should point at `http://127.0.0.1:8000`.

---

## What Exists Today

- **Frontend pages:** Nutrition Metrics, Sleep Metrics, Health Metrics, Body Measurements and
  Workout Metrics, each for viewing and logging one date at a time.
- **Labs:** backend endpoints for lab configuration, PDF extraction and saving reports exist, but
  there is no frontend for them yet.
- **Placeholders:** Dashboard, History and Settings pages.

---

## Key Rules

- **The Google Sheet is real data and acts as the database.** The code depends on its worksheet
  names and column positions, so any structural change to the Sheet must be made together with a
  code change.
- **Sheet access lives in one layer.** Only the `*_google_sheets_repository.py` files,
  `labs/lab_repository.py` and `database/sheets_client.py` in the backend read or write the Sheet.
- **The data importer converts units.** Everything is stored in metric units (kg, km, ml, kcal),
  and the importer writes only through the backend API.
- **Dates are local time (IST).** Dates are stored in the Sheet in the form `"October 08, 2026"`.
- **Saving a metric record is a partial update.** Fields sent as empty keep their existing value in
  the Sheet; they are not cleared.

---

## Testing Safely

Some tests and scripts write to the real Google Sheet, touch Google Drive or call OpenAI. In
particular, **plain `pytest` and the `*_e2e.py` tests hit live services.**

Use the safe, mocked test commands listed in [`CLAUDE.md`](CLAUDE.md#safe-test-commands-mockedlocal-only).
They set fake credentials, so any call that is not mocked fails instead of reaching a real service.

---

## Documentation Map

| Document | What it covers |
|---|---|
| [`frontend/README.md`](frontend/README.md) | Frontend setup, page load and save flow, styling, adding fields and pages, testing |
| [`backend/README.md`](backend/README.md) | Backend setup, architecture, request flow, adding fields and worksheets, testing, Labs module |
| [`data_importer/README.md`](data_importer/README.md) | Import flow, file lifecycle, unit conversions, running imports, configuration, testing |
| [`docs/README.md`](docs/README.md) | Architecture decision records (ADRs) |
| [`docs/ui/`](docs/ui/) | UI design principles, components and styling guidelines |
| [`CLAUDE.md`](CLAUDE.md) | Working rules for this repository, including safe test commands |
