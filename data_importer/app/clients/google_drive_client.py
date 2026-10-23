import json
from io import BytesIO

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

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

        files = []
        page_token = None

        while True:

            response = self.service.files().list(
                q=query,
                fields=(
                    "nextPageToken, "
                    "files("
                    "id, "
                    "name, "
                    "mimeType, "
                    "createdTime, "
                    "modifiedTime"
                    ")"
                ),
                orderBy="modifiedTime",
                pageSize=100,
                pageToken=page_token,
            ).execute()

            files.extend(
                response.get("files", [])
            )

            page_token = response.get(
                "nextPageToken"
            )

            if page_token is None:
                break

        return files

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


    def create_json_file(
        self,
        folder_id: str,
        file_name: str,
        data: dict,
    ) -> dict:
        """
        Create a JSON file inside a Google Drive folder.

        Primarily useful for integration and E2E tests.
        """

        file_content = json.dumps(
            data
        ).encode("utf-8")

        media = MediaIoBaseUpload(
            BytesIO(file_content),
            mimetype="application/json",
            resumable=False,
        )

        return self.service.files().create(
            body={
                "name": file_name,
                "parents": [folder_id],
            },
            media_body=media,
            fields="id, name, parents",
        ).execute()


    def delete_file(
        self,
        file_id: str,
    ) -> None:
        """
        Permanently delete a Google Drive file.
        """

        self.service.files().delete(
            fileId=file_id,
        ).execute()