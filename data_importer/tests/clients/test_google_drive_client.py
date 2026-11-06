from unittest.mock import Mock, patch

import pytest

from app.clients.google_drive_client import (
    DRIVE_RETRIES,
    GoogleDriveClient,
)


"""
Google Drive Client Tests

The Drive service is mocked, so these tests never reach Google Drive.
They check that the requests that are safe to repeat (list, download,
rename, move) ask Google's client library to retry temporary errors,
and that creating a file does not.
"""


CLIENT = "app.clients.google_drive_client"


@pytest.fixture
def drive_client():
    """
    A GoogleDriveClient whose credentials and Drive service are mocks.
    """

    with patch(f"{CLIENT}.service_account.Credentials.from_service_account_file"), \
            patch(f"{CLIENT}.build") as mock_build:

        mock_build.return_value = Mock()

        yield GoogleDriveClient()


# Verify that every page of a folder listing is retried on temporary errors.
def test_list_files_retries_every_page(drive_client):

    list_request = drive_client.service.files.return_value.list.return_value

    list_request.execute.side_effect = [
        {"files": [{"id": "file-1"}], "nextPageToken": "page-2"},
        {"files": [{"id": "file-2"}]},
    ]

    files = drive_client.list_files("folder-123")

    assert files == [{"id": "file-1"}, {"id": "file-2"}]

    assert list_request.execute.call_count == 2

    for execute_call in list_request.execute.call_args_list:
        assert execute_call.kwargs == {"num_retries": DRIVE_RETRIES}


# Verify that downloading a file is retried on temporary errors.
def test_read_json_file_retries_download(drive_client):

    downloader = Mock()
    downloader.next_chunk.return_value = (None, True)

    def fake_downloader(file_buffer, request):
        file_buffer.write(b'{"data": {"metrics": []}}')
        return downloader

    with patch(f"{CLIENT}.MediaIoBaseDownload", side_effect=fake_downloader):
        data = drive_client.read_json_file("file-123")

    assert data == {"data": {"metrics": []}}

    downloader.next_chunk.assert_called_once_with(
        num_retries=DRIVE_RETRIES
    )


# Verify that renaming a file is retried on temporary errors.
def test_rename_file_retries(drive_client):

    update_request = drive_client.service.files.return_value.update.return_value

    drive_client.rename_file("file-123", "PROCESSED_HealthMetrics-2026-11-05.json")

    update_request.execute.assert_called_once_with(
        num_retries=DRIVE_RETRIES
    )


# Verify that moving a file is retried on temporary errors.
def test_move_file_retries(drive_client):

    update_request = drive_client.service.files.return_value.update.return_value

    drive_client.move_file("file-123", "incoming-folder", "processed-folder")

    update_request.execute.assert_called_once_with(
        num_retries=DRIVE_RETRIES
    )


# Verify that creating a file is not retried, because a retry after a
# lost response could create a duplicate file.
def test_create_json_file_is_not_retried(drive_client):

    create_request = drive_client.service.files.return_value.create.return_value

    drive_client.create_json_file("folder-123", "TEST_file.json", {"a": 1})

    create_request.execute.assert_called_once_with()
