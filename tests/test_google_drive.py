"""Tests for Google Drive integration."""

import os
from unittest.mock import Mock, mock_open, patch

import pytest

from solution_desk_engine.integrations.google_drive import GoogleDriveClient


class TestGoogleDriveClient:
    """Test cases for GoogleDriveClient."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.client = GoogleDriveClient()

    def test_default_paths(self) -> None:
        """Test default credential and token paths."""
        expected_creds = os.path.expanduser(
            "~/.solution-desk-engine/google_credentials.json"
        )
        expected_token = os.path.expanduser("~/.solution-desk-engine/google_token.json")

        assert self.client.credentials_path == expected_creds
        assert self.client.token_path == expected_token

    def test_custom_paths(self) -> None:
        """Test custom credential and token paths."""
        custom_creds = "/custom/creds.json"
        custom_token = "/custom/token.json"

        client = GoogleDriveClient(
            credentials_path=custom_creds, token_path=custom_token
        )

        assert client.credentials_path == custom_creds
        assert client.token_path == custom_token

    @patch("solution_desk_engine.integrations.google_drive.build")
    @patch(
        "solution_desk_engine.integrations.google_drive.Credentials.from_authorized_user_file"
    )
    @patch("os.path.exists")
    def test_authentication_with_existing_token(
        self, mock_exists, mock_from_file, mock_build
    ) -> None:
        """Test authentication with existing valid token."""
        # Mock existing token file
        mock_exists.return_value = True

        # Mock valid credentials
        mock_creds = Mock()
        mock_creds.valid = True
        mock_from_file.return_value = mock_creds

        # Test authentication
        self.client._get_service()

        mock_from_file.assert_called_once()
        mock_build.assert_called_once_with("drive", "v3", credentials=mock_creds)

    @patch("solution_desk_engine.integrations.google_drive.MediaIoBaseDownload")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_doc_as_docx(self, mock_file, mock_download) -> None:
        """Test downloading Google Doc as DOCX."""
        # Mock the service
        mock_service = Mock()
        mock_request = Mock()
        mock_service.files().export_media.return_value = mock_request
        self.client._service = mock_service

        # Mock downloader
        mock_downloader = Mock()
        mock_downloader.next_chunk.side_effect = [(None, False), (None, True)]
        mock_download.return_value = mock_downloader

        # Test download
        self.client.download_doc_as_docx("test_file_id", "/tmp/test.docx")

        # Verify API call
        mock_service.files().export_media.assert_called_once_with(
            fileId="test_file_id",
            mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

        # Verify download process
        mock_download.assert_called_once()
        assert mock_downloader.next_chunk.call_count == 2

    @patch("solution_desk_engine.integrations.google_drive.MediaFileUpload")
    @patch("os.path.exists")
    def test_upload_docx_as_google_doc(self, mock_exists, mock_media_upload) -> None:
        """Test uploading DOCX as Google Doc."""
        mock_exists.return_value = True

        # Mock the service
        mock_service = Mock()
        mock_file_result = {
            "id": "new_doc_id",
            "webViewLink": "https://docs.google.com/document/d/new_doc_id/edit",
            "name": "Test SOW",
        }
        mock_service.files().create().execute.return_value = mock_file_result
        self.client._service = mock_service

        # Mock media upload
        mock_media = Mock()
        mock_media_upload.return_value = mock_media

        # Test upload
        result = self.client.upload_docx_as_google_doc("/tmp/test.docx", "Test SOW")

        # Verify result
        assert result["id"] == "new_doc_id"
        assert (
            result["web_view_link"]
            == "https://docs.google.com/document/d/new_doc_id/edit"
        )
        assert result["name"] == "Test SOW"

        # Verify API call - check the actual call with parameters
        create_calls = [
            call
            for call in mock_service.files().create.call_args_list
            if len(call.args) > 0 or len(call.kwargs) > 0
        ]
        assert len(create_calls) == 1
        call_args = create_calls[0]
        assert (
            call_args[1]["body"]["mimeType"] == "application/vnd.google-apps.document"
        )
        assert call_args[1]["body"]["name"] == "Test SOW"

    def test_upload_nonexistent_file_raises_error(self) -> None:
        """Test that uploading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            self.client.upload_docx_as_google_doc("/nonexistent/file.docx", "Test SOW")

    def test_get_file_info(self) -> None:
        """Test getting file information."""
        # Mock the service
        mock_service = Mock()
        mock_file_info = {
            "id": "test_id",
            "name": "Test Document",
            "mimeType": "application/vnd.google-apps.document",
        }
        mock_service.files().get().execute.return_value = mock_file_info
        self.client._service = mock_service

        # Test get file info
        result = self.client.get_file_info("test_id")

        assert result == mock_file_info
        # Check that the get method was called with correct parameters
        get_calls = [
            call
            for call in mock_service.files().get.call_args_list
            if len(call.args) > 0 or len(call.kwargs) > 0
        ]
        assert len(get_calls) == 1
        call_args = get_calls[0]
        assert call_args.kwargs["fileId"] == "test_id"
        assert (
            call_args.kwargs["fields"]
            == "id,name,mimeType,createdTime,modifiedTime,webViewLink"
        )

    def test_list_files_in_folder(self) -> None:
        """Test listing files in a folder."""
        # Mock the service
        mock_service = Mock()
        mock_files = {
            "files": [
                {"id": "file1", "name": "Document 1"},
                {"id": "file2", "name": "Document 2"},
            ]
        }
        mock_service.files().list().execute.return_value = mock_files
        self.client._service = mock_service

        # Test list files
        result = self.client.list_files_in_folder("folder_id")

        assert len(result) == 2
        assert result[0]["id"] == "file1"
        assert result[1]["id"] == "file2"

        # Check that the list method was called with correct parameters
        list_calls = [
            call
            for call in mock_service.files().list.call_args_list
            if len(call.args) > 0 or len(call.kwargs) > 0
        ]
        assert len(list_calls) == 1
        call_args = list_calls[0]
        assert call_args.kwargs["q"] == "'folder_id' in parents and trashed=false"
        assert (
            call_args.kwargs["fields"]
            == "files(id,name,mimeType,createdTime,modifiedTime,webViewLink)"
        )
