"""Google Drive API integration for SOW document management."""

import io
import os
from typing import Any, Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload  # type: ignore

# Scopes required for Google Drive API access
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class GoogleDriveClient:
    """Google Drive API client for downloading and uploading documents."""

    def __init__(
        self, credentials_path: Optional[str] = None, token_path: Optional[str] = None
    ) -> None:
        """Initialize Google Drive client.

        Args:
            credentials_path: Path to OAuth2 credentials JSON file
            token_path: Path to store/load user token
        """
        self.credentials_path = credentials_path or self._get_default_credentials_path()
        self.token_path = token_path or self._get_default_token_path()
        self._service = None

    def _get_default_credentials_path(self) -> str:
        """Get default path for Google OAuth2 credentials."""
        return os.path.expanduser("~/.solution-desk-engine/google_credentials.json")

    def _get_default_token_path(self) -> str:
        """Get default path for Google OAuth2 token."""
        return os.path.expanduser("~/.solution-desk-engine/google_token.json")

    def _authenticate(self) -> Credentials:
        """Authenticate with Google Drive API using OAuth2.

        Returns:
            Google OAuth2 credentials

        Raises:
            FileNotFoundError: If credentials file not found
            Exception: If authentication fails
        """
        creds = None

        # Load existing token if available
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # If no valid credentials, initiate OAuth2 flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Google OAuth2 credentials not found at {self.credentials_path}. "
                        "Please download credentials from Google Cloud Console and place them at this location."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return creds  # type: ignore

    def _get_service(self) -> Any:
        """Get authenticated Google Drive service instance."""
        if self._service is None:
            creds = self._authenticate()
            self._service = build("drive", "v3", credentials=creds)
        return self._service

    def download_doc_as_docx(self, file_id: str, output_path: str) -> None:
        """Download Google Doc as DOCX file.

        Args:
            file_id: Google Drive file ID
            output_path: Local path to save DOCX file

        Raises:
            HttpError: If Google Drive API request fails
            IOError: If file write fails
        """
        try:
            service = self._get_service()

            # Export Google Doc as DOCX
            request = service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

            # Download file
            with io.FileIO(output_path, "wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()

        except HttpError as error:
            raise HttpError(f"Failed to download Google Doc {file_id}: {error}")
        except Exception as error:
            raise IOError(f"Failed to save file to {output_path}: {error}")

    def upload_docx_as_google_doc(
        self, docx_path: str, name: str, folder_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload DOCX file as Google Doc.

        Args:
            docx_path: Path to DOCX file to upload
            name: Name for the new Google Doc
            folder_id: Optional Google Drive folder ID to upload to

        Returns:
            Dictionary containing file ID and web view link

        Raises:
            FileNotFoundError: If DOCX file not found
            HttpError: If Google Drive API request fails
        """
        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"DOCX file not found: {docx_path}")

        try:
            service = self._get_service()

            # File metadata
            file_metadata = {
                "name": name,
                "mimeType": "application/vnd.google-apps.document",  # Convert to Google Doc
            }

            # Add to folder if specified
            if folder_id:
                file_metadata["parents"] = [folder_id]  # type: ignore

            # Upload file
            media = MediaFileUpload(
                docx_path,
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

            file = (
                service.files()
                .create(
                    body=file_metadata, media_body=media, fields="id,webViewLink,name"
                )
                .execute()
            )

            return {
                "id": file.get("id"),
                "web_view_link": file.get("webViewLink"),
                "name": file.get("name"),
            }

        except HttpError as error:
            raise HttpError(f"Failed to upload DOCX as Google Doc: {error}")

    def get_file_info(self, file_id: str) -> Dict[str, Any]:
        """Get file information from Google Drive.

        Args:
            file_id: Google Drive file ID

        Returns:
            Dictionary containing file metadata

        Raises:
            HttpError: If Google Drive API request fails
        """
        try:
            service = self._get_service()

            file_info = (
                service.files()
                .get(
                    fileId=file_id,
                    fields="id,name,mimeType,createdTime,modifiedTime,webViewLink",
                )
                .execute()
            )

            return file_info  # type: ignore

        except HttpError as error:
            raise HttpError(f"Failed to get file info for {file_id}: {error}")

    def list_files_in_folder(self, folder_id: str) -> list[Dict[str, Any]]:
        """List files in a Google Drive folder.

        Args:
            folder_id: Google Drive folder ID

        Returns:
            List of file dictionaries

        Raises:
            HttpError: If Google Drive API request fails
        """
        try:
            service = self._get_service()

            results = (
                service.files()
                .list(
                    q=f"'{folder_id}' in parents and trashed=false",
                    fields="files(id,name,mimeType,createdTime,modifiedTime,webViewLink)",
                )
                .execute()
            )

            return results.get("files", [])  # type: ignore

        except HttpError as error:
            raise HttpError(f"Failed to list files in folder {folder_id}: {error}")
