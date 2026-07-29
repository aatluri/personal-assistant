# ADR 001 – Project Structure

## Status

Accepted

---

## Context

The Personal Assistant application is expected to grow over time and include multiple independent modules, such as:

- Health
- Email
- Workout
- Nutrition
- Calendar
- Tasks

The project should remain easy to navigate and maintain as new modules are added.

---

## Decision

The project will use a feature-based architecture.

```
personal-assistant/
│
├── backend/
│   ├── app/
│   │   ├── modules/
│   │   ├── database/
│   │   ├── core/
│   │   ├── utils/
│   │   └── main.py
│   ├── credentials/
│   ├── tests/
│   └── README.md
│
├── frontend/
├── docs/
├── scripts/
└── infrastructure/
```

Within each backend module:

```
modules/
    health/
        api.py
        service.py
        repository.py
        schemas.py
```

---

## Rationale

- Groups code by business feature rather than technical layer.
- Keeps each module self-contained.
- Makes it easier to add new modules without affecting existing ones.
- Separates API, business logic, and data access responsibilities.
- Supports future migration from Google Sheets to a database with minimal changes.
- Scales well as the application grows.

---

## Consequences

### Advantages

- Clear separation of responsibilities.
- Easy to locate related code.
- Simple to test individual modules.
- New modules follow a consistent structure.

### Trade-offs

- Some files (such as `service.py` and `repository.py`) may initially contain very little code.
- There is slightly more boilerplate compared to a small prototype.

---

## Alternatives Considered

### Single `services/` folder

Rejected because business logic becomes spread across unrelated files as the application grows.

### Layer-first structure

Example:

```
controllers/
services/
repositories/
models/
```

Rejected because code for one feature becomes scattered across multiple folders, making navigation harder.

---

## Notes

This structure should remain the default for all future modules unless there is a compelling architectural reason to change it.