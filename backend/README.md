# Personal Assistant Backend

## Overview

This backend powers the Personal Assistant application.

Current Module:
- Health Tracker

Technology Stack:
- Python
- FastAPI

---

## Prerequisites

- Python 3.10+
- pip

---

## First Time Setup

### 1. Create a virtual environment

python3 -m venv .venv

### 2. Activate the virtual environment

macOS/Linux

source .venv/bin/activate

Windows

.venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

---

## Running the Backend

Activate the virtual environment

source .venv/bin/activate

Start the development server

fastapi dev app/main.py

---

## API Documentation

Swagger UI

http://127.0.0.1:8000/docs

Root Endpoint

http://127.0.0.1:8000

Health Endpoint

http://127.0.0.1:8000/health/status

---

## Project Structure

app/
    main.py
    config.py
    database/
    modules/
        health/

---

## Current Status

✅ FastAPI project created

✅ Health module added

✅ Health router registered

⬜ Google Sheets connection

⬜ Daily Log API

⬜ Body Measurements API

⬜ Bloodwork API

---

## Notes

Always activate the virtual environment before running the project.

If new packages are installed, update requirements.txt using:

pip freeze > requirements.txt