import json
from io import BytesIO

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from app.config import settings


class GoogleDriveClient:
    """
    Client for communicating with Google Drive.
    """

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_SERVICE_ACCOUNT_FILE,
            scopes=[
                "https://www.googleapis.com/auth/drive",
            ],
        )

        self.service = build(
            "drive",
            "v3",
            credentials=credentials,
        )

    def list_files(
        self,
        folder_id: str,
    ) -> list[dict]:
        """
        Return all non-trashed files inside a Google Drive folder.
        """

        query = (
            f"'{folder_id}' in parents "
            "and trashed = false"
        )

        response = self.service.files().list(
            q=query,
            fields=(
                "files("
                "id, "
                "name, "
                "mimeType, "
                "createdTime, "
                "modifiedTime"
                ")"
            ),
            orderBy="modifiedTime",
        ).execute()

        return response.get("files", [])

    def read_json_file(
        self,
        file_id: str,
    ) -> dict:
        """
        Download a JSON file from Google Drive and return
        the parsed JSON data.
        """

        request = self.service.files().get_media(
            fileId=file_id,
        )

        file_buffer = BytesIO()

        downloader = MediaIoBaseDownload(
            file_buffer,
            request,
        )

        done = False

        while not done:
            _, done = downloader.next_chunk()

        file_buffer.seek(0)

        return json.load(file_buffer)

    def rename_file(
        self,
        file_id: str,
        new_name: str,
    ) -> dict:
        """
        Rename an existing Google Drive file.

        Renaming preserves the Google Drive file ID.
        """

        return self.service.files().update(
            fileId=file_id,
            body={
                "name": new_name,
            },
            fields="id, name",
        ).execute()

    def move_file(
        self,
        file_id: str,
        source_folder_id: str,
        destination_folder_id: str,
    ) -> dict:
        """
        Move an existing Google Drive file from one folder
        to another.

        Moving preserves the Google Drive file ID.
        """

        return self.service.files().update(
            fileId=file_id,
            addParents=destination_folder_id,
            removeParents=source_folder_id,
            fields="id, name, parents",
        ).execute()