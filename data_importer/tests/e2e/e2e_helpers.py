"""
Helpers shared by the importer E2E tests.

The importer application never accesses the Google Sheet; it writes only
through the backend API. These helpers are the one exception, and exist
only so E2E tests can remove the test rows they create. They are used by
test code only.
"""

import json
from io import BytesIO

import pytest
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from app.clients.google_drive_client import GoogleDriveClient
from app.config import settings
from app.modules.health.constants import (
    FAILED_PREFIX,
    PROCESSED_PREFIX,
)


SHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


def assert_record_matches(
    expected: dict,
    actual: dict,
) -> None:
    """
    Verify that every expected field has the expected value in a record
    returned by the backend. Floats are compared to 2 decimal places.
    """

    for field, expected_value in expected.items():

        assert field in actual, (
            f"Field '{field}' missing from backend response."
        )

        if isinstance(expected_value, float):
            assert actual[field] == pytest.approx(
                expected_value,
                abs=0.01,
            ), (
                f"Mismatch for '{field}': expected "
                f"{expected_value!r}, got {actual[field]!r}"
            )
        else:
            assert actual[field] == expected_value, (
                f"Mismatch for '{field}': expected "
                f"{expected_value!r}, got {actual[field]!r}"
            )


class SharedFixture:
    """
    A permanent fixture file kept in a Drive incoming folder and shared
    by the archiver and importer E2E tests.

    Service accounts cannot create files in a personal Drive (they have
    no storage quota), so tests reuse a file the user uploaded once,
    renaming it temporarily instead of creating new files.

    Between test runs the file is called permanent_name (a TEST_ name,
    which the importer skips) and lives in the incoming folder.
    """

    def __init__(
        self,
        drive_client: GoogleDriveClient,
        incoming_folder_id: str,
        processed_folder_id: str,
        permanent_name: str,
        test_prefix: str,
        import_name: str,
    ):
        self.drive_client = drive_client
        self.incoming_folder_id = incoming_folder_id
        self.processed_folder_id = processed_folder_id
        self.permanent_name = permanent_name
        self.test_prefix = test_prefix
        self.import_name = import_name
        self.file_id = self._find_file_id()

    def _is_fixture_name(
        self,
        name: str,
    ) -> bool:
        """
        Recognise every name a test may have left the fixture under:
        its TEST_ name (with any date the archiver test used), the
        import name, and either of those with PROCESSED_ or FAILED_.
        """

        original_name = (
            name
            .removeprefix(PROCESSED_PREFIX)
            .removeprefix(FAILED_PREFIX)
        )

        return (
            original_name.startswith(self.test_prefix)
            or original_name == self.import_name
        )

    def _find_file_id(self) -> str:
        """
        Find the fixture in the incoming or processed folder.
        """

        matches = [
            file
            for folder_id in (
                self.incoming_folder_id,
                self.processed_folder_id,
            )
            for file in self.drive_client.list_files(folder_id)
            if self._is_fixture_name(file["name"])
        ]

        assert len(matches) == 1, (
            f"Expected exactly one fixture file {self.permanent_name!r} "
            "in the incoming folder (it may also be left under a "
            f"temporary name), found {[file['name'] for file in matches]}. "
            "Upload it once to the incoming folder if it is missing."
        )

        return matches[0]["id"]

    def restore(self) -> None:
        """
        Put the fixture back: in the incoming folder, under its
        permanent TEST_ name.
        """

        incoming_ids = {
            file["id"]
            for file in self.drive_client.list_files(
                self.incoming_folder_id
            )
        }

        if self.file_id not in incoming_ids:
            self.drive_client.move_file(
                file_id=self.file_id,
                source_folder_id=self.processed_folder_id,
                destination_folder_id=self.incoming_folder_id,
            )

        self.drive_client.rename_file(
            file_id=self.file_id,
            new_name=self.permanent_name,
        )

    def overwrite_content(
        self,
        data: dict,
    ) -> None:
        """
        Replace the fixture's content with data, so the Drive copy always
        matches the fixture committed in the repository.

        Updating a file the user owns is allowed even though creating
        one is not, because the file uses the user's storage.
        """

        media = MediaIoBaseUpload(
            BytesIO(json.dumps(data).encode("utf-8")),
            mimetype="application/json",
            resumable=False,
        )

        self.drive_client.service.files().update(
            fileId=self.file_id,
            media_body=media,
        ).execute()

    def rename_for_import(self) -> None:
        """
        Give the fixture a name the importer recognises.
        """

        self.drive_client.rename_file(
            file_id=self.file_id,
            new_name=self.import_name,
        )

    def current_name(self) -> str:
        """
        Return the fixture's current name in the incoming folder.
        """

        for file in self.drive_client.list_files(self.incoming_folder_id):
            if file["id"] == self.file_id:
                return file["name"]

        return ""


def delete_test_rows_from_google_sheets(
    sheet_date: str,
) -> None:
    """
    Delete every row whose Date column equals sheet_date, in every
    worksheet that has a Date column.

    Only dates in 2099 are allowed, so this can never delete real data.
    Requires GOOGLE_SHEETS_SPREADSHEET_ID in data_importer/.env, and the
    importer's service account needs edit access to the spreadsheet.
    """

    if not sheet_date.endswith("2099"):
        raise ValueError(
            f"Refusing to delete rows for {sheet_date!r}: "
            "only 2099 test dates may be deleted."
        )

    assert settings.GOOGLE_SHEETS_SPREADSHEET_ID, (
        "GOOGLE_SHEETS_SPREADSHEET_ID must be set in data_importer/.env "
        "to run the importer E2E tests."
    )

    credentials = Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SHEETS_SCOPES,
    )

    spreadsheets = build(
        "sheets",
        "v4",
        credentials=credentials,
        cache_discovery=False,
    ).spreadsheets()

    spreadsheet_id = settings.GOOGLE_SHEETS_SPREADSHEET_ID

    metadata = spreadsheets.get(
        spreadsheetId=spreadsheet_id,
        fields="sheets.properties(sheetId,title)",
    ).execute()

    delete_requests = []

    for sheet in metadata["sheets"]:

        sheet_id = sheet["properties"]["sheetId"]
        title = sheet["properties"]["title"]

        rows = spreadsheets.values().get(
            spreadsheetId=spreadsheet_id,
            range=f"'{title}'",
        ).execute().get("values", [])

        if not rows or "Date" not in rows[0]:
            continue

        date_column = rows[0].index("Date")

        matching_row_indexes = [
            index
            for index, row in enumerate(rows)
            if index > 0
            and len(row) > date_column
            and row[date_column] == sheet_date
        ]

        # Delete bottom-to-top so earlier deletions do not shift the
        # positions of rows still to be deleted.
        for index in reversed(matching_row_indexes):
            delete_requests.append(
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": sheet_id,
                            "dimension": "ROWS",
                            "startIndex": index,
                            "endIndex": index + 1,
                        }
                    }
                }
            )

    if delete_requests:
        spreadsheets.batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": delete_requests},
        ).execute()


# The permanent fixture files shared by the archiver and importer E2E
# tests, one per incoming folder. Between runs each has its TEST_ name;
# the importer tests temporarily rename it to the import name.
HEALTH_FIXTURE_PERMANENT_NAME = "TEST_HealthMetrics-2099-01-01.json"
HEALTH_FIXTURE_TEST_PREFIX = "TEST_HealthMetrics-"
HEALTH_FIXTURE_IMPORT_NAME = "HealthMetrics-2099-02-01.json"

WORKOUT_FIXTURE_PERMANENT_NAME = "TEST_WorkoutMetrics-2099-01-01.json"
WORKOUT_FIXTURE_TEST_PREFIX = "TEST_WorkoutMetrics-"
WORKOUT_FIXTURE_IMPORT_NAME = "WorkoutMetrics-2099-02-01.json"


def health_metrics_fixture(
    drive_client: GoogleDriveClient,
) -> SharedFixture:
    """
    Find the shared Health Metrics fixture file in Drive.
    """

    return SharedFixture(
        drive_client=drive_client,
        incoming_folder_id=settings.HEALTH_METRICS_DRIVE_FOLDER_ID,
        processed_folder_id=(
            settings.HEALTH_METRICS_PROCESSED_DRIVE_FOLDER_ID
        ),
        permanent_name=HEALTH_FIXTURE_PERMANENT_NAME,
        test_prefix=HEALTH_FIXTURE_TEST_PREFIX,
        import_name=HEALTH_FIXTURE_IMPORT_NAME,
    )


def workout_metrics_fixture(
    drive_client: GoogleDriveClient,
) -> SharedFixture:
    """
    Find the shared Workout Metrics fixture file in Drive.
    """

    return SharedFixture(
        drive_client=drive_client,
        incoming_folder_id=settings.WORKOUT_METRICS_DRIVE_FOLDER_ID,
        processed_folder_id=(
            settings.WORKOUT_METRICS_PROCESSED_DRIVE_FOLDER_ID
        ),
        permanent_name=WORKOUT_FIXTURE_PERMANENT_NAME,
        test_prefix=WORKOUT_FIXTURE_TEST_PREFIX,
        import_name=WORKOUT_FIXTURE_IMPORT_NAME,
    )
