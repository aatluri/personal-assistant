# ADR 002 – Google Sheets Access

## Status

Accepted

---

## Context

The application needs to connect to a specific Google Spreadsheet that stores the user's health data.

Initially, the spreadsheet was accessed using:

```python
client.open("Health Tracker Database")
```

This required enabling the Google Drive API because the library searches Google Drive for the spreadsheet by name.

---

## Decision

The application will access the spreadsheet using its Spreadsheet ID.

```python
client.open_by_key(SPREADSHEET_ID)
```

The Spreadsheet ID will be stored in the application's configuration (`.env`).

---

## Rationale

- Does not require the Google Drive API.
- Uses only the Google Sheets API.
- Follows the principle of least privilege.
- More reliable if the spreadsheet is renamed.
- Faster because no Drive search is required.
- Easier to configure across environments.

---

## Consequences

- The spreadsheet ID must be configured before the application starts.
- Renaming the spreadsheet will not affect the application.
- Future Google Sheets integrations should always use `open_by_key()`.