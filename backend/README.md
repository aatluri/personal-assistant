Personal Assistant Backend

Overview

This backend powers the Personal Assistant application.

Current module:

* Health Tracker

Technology Stack:

* Python
* FastAPI

⸻

Prerequisites

* Python 3.10+
* pip

⸻

First Time Setup

1. Create a virtual environment

python3 -m venv .venv

2. Activate the virtual environment

macOS / Linux

source .venv/bin/activate

Windows

.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

⸻

Running the Backend

Activate the virtual environment

source .venv/bin/activate

Start the FastAPI development server

fastapi dev app/main.py

⸻

Verify the Backend

Open the following URLs:

URL	Expected Result
http://127.0.0.1:8000	Personal Assistant API is running
http://127.0.0.1:8000/health/status	Health module status
http://127.0.0.1:8000/docs	Swagger API documentation

⸻

Project Structure

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
│           └── schemas.py
│
├── credentials/
├── tests/
├── requirements.txt
├── .env
└── README.md

⸻

Architecture

The backend follows a layered architecture.

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
Google Sheets (currently pending)

Responsibilities:

* api.py → Defines REST API endpoints.
* service.py → Contains business logic.
* repository.py → Reads/writes data.
* database/ → Handles communication with external data sources.

⸻

Current Status

✅ Completed

* Project structure created
* FastAPI configured
* Health module created
* Swagger documentation working
* Git repository created
* GitHub repository connected
* Initial commit pushed

🚧 Next Milestone

Google Sheets Integration

⸻

Notes

Always activate the virtual environment before running the backend.

Whenever new Python packages are installed:

pip freeze > requirements.txt

After making code changes:

git status
git add .
git commit -m "Meaningful commit message"
git push