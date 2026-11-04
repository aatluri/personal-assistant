# CLAUDE.md

Operating rules for working on this repository. Architecture, setup, and step-by-step
checklists (adding a field, page, or worksheet) live in `backend/README.md`,
`frontend/README.md`, and `docs/` — read those rather than duplicating them here.

Rules marked *(current)* reflect decisions for the current phase and are expected to be revisited.

## Safety: real data and paid services

- The Google Sheet configured in `backend/.env` is **real data**, unless the user explicitly says otherwise.
- **Ask first** before running anything that writes to the Sheet, touches Google Drive, or calls OpenAI
  or any other paid/external API. This includes:
  - any `*_e2e.py` test, i.e. anything run with `pytest -m e2e` (backend and `data_importer/tests/e2e/`;
    includes `backend/tests/labs/test_lab_extraction_e2e.py`, which reads the live Sheet and calls OpenAI)
  - `backend/tools/*` scripts
  - data importer endpoints and `data_importer/scripts/import_historical_health_metrics.py`
  - starting the backend to exercise write paths manually or through the UI
- **Google Sheet structure** *(current)*: never change it automatically. If a feature needs a new
  worksheet, column, range, or other structural change, explain exactly what must change and why,
  and wait for approval. Repositories depend on column positions and hardcoded ranges, so code and
  Sheet must change together.
- The lab PDFs in `backend/tests/labs/test_data/` contain real personal data. Do not move, remove,
  or rewrite them, and do not modify Git history. *(current — to be handled separately)*

## Safe test commands (mocked/local only)

These run without touching the Sheet, Drive, OpenAI, or the backend. The overridden environment
variables are a safety net: any call that is not mocked fails instead of reaching a real service.

```bash
# backend/
GOOGLE_SERVICE_ACCOUNT_FILE=/nonexistent/offline.json OPENAI_API_KEY=offline-invalid-key \
  .venv/bin/python -m pytest -q -p no:cacheprovider

# data_importer/
GOOGLE_SERVICE_ACCOUNT_FILE=/nonexistent/offline.json PERSONAL_ASSISTANT_API_URL=http://127.0.0.1:9 \
  .venv/bin/python -m pytest -q -p no:cacheprovider

# frontend/
npm run test:run
npm run lint
```

- Live tests are opt-in: tests in files ending in `_e2e.py` are marked `e2e` by `tests/conftest.py`
  and deselected by `pytest.ini` (`addopts = -m "not e2e"`). They run only with `pytest -m e2e`,
  which needs approval first (see Safety above).
- Do not run `npm run test:coverage` unless asked; it rewrites the committed `frontend/coverage/` files.
- New tests that touch real external services must go in a file ending in `_e2e.py`, so they stay
  out of the default run.

## Test execution workflow *(current)*

- Reading and inspecting existing tests is always allowed.
- When implementing a feature or fix, write new tests or modify existing tests as appropriate.
- After making code or test changes, **before running any tests** (including the safe commands
  above), show the user:
  1. which implementation files changed
  2. which tests were added or modified
  3. what those tests are intended to verify
  4. the exact test command(s) proposed

  Then wait for approval before running them.
- Do not modify existing tests merely to make an implementation pass. Existing tests represent
  expected behaviour unless a behaviour change has been explicitly decided.
- This approval step is temporary; safe mocked/local tests may later be allowed to run automatically.

## Git

- Do not commit unless asked. Never commit to `main` — create a feature branch first.
- Never push without explicit approval.

## Architecture rules

- Application and business logic must not depend on Google Sheets. Sheets access belongs only in
  `*_google_sheets_repository.py` / `labs/lab_repository.py` and `app/database/sheets_client.py`.
- Keep a clean repository abstraction, but do not prematurely generalise or optimise it for a future
  database migration.
- New backend code follows the API → Service → Repository separation used by the metric modules
  (service and repository classes). Do not refactor the existing labs module (module-level functions,
  API calling the repository directly) merely for consistency unless explicitly decided.
- The data importer writes only through the backend HTTP API (`BackendClient`), never to the Sheet directly.
- Frontend: pages own state, section components update their slice of it, and only `src/api/*`
  calls `fetch`.

## Conventions

- Time: assume IST/local time. Preserve current storage formats (e.g. Sheet dates as `"%B %d, %Y"`,
  timezone stripped from datetimes) unless a change is explicitly decided.
- Units: metric (kg, km, ml, kcal). Conversions happen in the importer.
- Code clarity: code should be educational and easy to understand, so the user can understand and
  maintain the application without the code becoming unnecessarily verbose.
  - Add docstrings to public or non-obvious functions and classes.
  - Add high-level comments where they explain important flows, business rules, architectural
    decisions, or non-obvious reasoning.
  - Do not add comments or docstrings that merely restate obvious code.
- Documentation consistency: After making code, architecture, API, configuration, setup, workflow,
  or behavior changes, check whether any README or other project documentation affected by the
  change is now inaccurate or incomplete. Update relevant documentation as part of the same change.
  Do not modify documentation when the change has no impact on it. Do not fix unrelated stale
  docs — mention them instead.

## Scope

- Single-user and local-only *(current)*. Do not add authentication, deployment infrastructure,
  or related complexity unless explicitly decided.
- Keep current providers, models, and import formats (OpenAI `gpt-5-mini` for lab extraction; the
  existing Health/Workout JSON export format for the importer) unless explicitly decided.

## Known state — do not "fix" unasked

- `npm run lint` reports pre-existing errors in `src/api/workoutMetrics.ts` and
  `src/components/Button.tsx`.
- **Labs frontend** is not built yet (backend endpoints exist). Do not start it until asked.
- Dashboard, History, and Settings pages are placeholders.
