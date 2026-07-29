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

---

# Verify the Backend

Once the server is running, verify the following URLs:

| URL | Expected Result |
|------|-----------------|
| http://127.0.0.1:8000 | Personal Assistant API is running |
| http://127.0.0.1:8000/health/status | Health module status |
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
FastAPI API
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
Google Sheets Client
   │
   ▼
Google Sheets
```

## Layer Responsibilities

| Layer | Responsibility |
|--------|----------------|
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

---

## 🚧 Next Milestone

**Health Repository**

Goals:

- Build the Health repository.
- Read data from the Daily Log worksheet.
- Return typed Python models.
- Expose the data through a service layer.

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