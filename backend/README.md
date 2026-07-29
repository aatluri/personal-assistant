# Personal Assistant Backend

## Overview

This backend powers the **Personal Assistant** application.

### Current Module

- Health Tracker

### Technology Stack

- Python
- FastAPI

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
│   └── modules/
│       └── health/
│           ├── api.py
│           ├── service.py
│           ├── repository.py
│           ├── schemas.py
│           └── __init__.py
│
├── credentials/
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
Database Client
   │
   ▼
Google Sheets (coming in Milestone 2)
```

## Layer Responsibilities

| Layer | Responsibility |
|--------|----------------|
| `api.py` | Defines REST API endpoints |
| `service.py` | Contains business logic |
| `repository.py` | Reads and writes data |
| `database/` | Communicates with external data sources (Google Sheets, databases, etc.) |

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
- Initial project pushed to GitHub

---

## 🚧 Next Milestone

**Google Sheets Integration**

Progress:

- ✅ Service account created
- ✅ Google Sheets API enabled
- ✅ Connection to Google Sheets verified
- ⬜ Build Google Sheets database client
- ⬜ Integrate with the repository layer

---

# Notes

Always activate the virtual environment before running the backend.

Whenever new Python packages are installed, update the requirements file:

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