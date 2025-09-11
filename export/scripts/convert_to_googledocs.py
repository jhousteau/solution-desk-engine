#!/usr/bin/env python3
"""
Google Docs Conversion Script for [CLIENT] F&I Documentation
Converts markdown files to Google Docs by first creating DOCX files and uploading to Google Drive.
Extends convert_to_docx.py functionality with Google Drive integration.
"""

import argparse
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import the existing DOCX processor
try:
    from convert_to_docx import COLORS, OPPORTUNITY_DIR, PHASES
    from convert_to_docx import DocumentProcessor as DocxProcessor
except ImportError:
    print(
        "Error: convert_to_docx.py not found. Ensure it exists in the same directory."
    )
    sys.exit(1)

# Google API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print("Error: Google API libraries not installed.")
    print(
        "Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client"
    )
    sys.exit(1)

# Configuration
OUTPUT_DIR = Path("../googledocs")
CREDENTIALS_DIR = Path("../../credentials")
METADATA_DIR = Path("../_metadata")

# Google API scopes
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.file",
]


class GoogleDocsProcessor(DocxProcessor):
    """Extends DocumentProcessor to create Google Docs via DOCX upload."""

    def __init__(self, output_dir: Path, credentials_path: Path, verbose: bool = False):
        super().__init__(output_dir, verbose)
        self.credentials_path = credentials_path
        self.temp_dir = Path(tempfile.mkdtemp())
        self.service = None
        self.drive_service = None
        self.created_docs = []
        self.folder_cache = {}

        # Setup Google API services
        self._setup_google_services()

    def _setup_google_services(self) -> None:
        """Authenticate and setup Google API services."""
        try:
            creds = self._authenticate()
            self.service = build("docs", "v1", credentials=creds)
            self.drive_service = build("drive", "v3", credentials=creds)
            self.logger.info("Google API services initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to setup Google services: {e}")
            raise

    def _authenticate(self) -> Credentials:
        """Handle Google API authentication."""
        creds = None
        token_file = self.credentials_path.parent / "token.json"

        # Load existing token if available
        if token_file.exists():
            creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(token_file, "w") as token:
                token.write(creds.to_json())

        return creds

    def _create_or_get_folder(self, folder_name: str, parent_id: str = None) -> str:
        """Create or get Google Drive folder with branded naming."""
        # Use branded folder names from branding manager
        folder_structure = self.branding.create_google_drive_folder_structure()
        branded_name = folder_structure.get("phases", {}).get(folder_name, folder_name)

        cache_key = f"{parent_id}:{branded_name}"
        if cache_key in self.folder_cache:
            return self.folder_cache[cache_key]

        try:
            # Search for existing folder
            query = f"name='{branded_name}' and mimeType='application/vnd.google-apps.folder'"
            if parent_id:
                query += f" and '{parent_id}' in parents"

            results = self.drive_service.files().list(q=query).execute()
            items = results.get("files", [])

            if items:
                folder_id = items[0]["id"]
                self.logger.info(f"Found existing folder: {branded_name}")
            else:
                # Create new folder
                folder_metadata = {
                    "name": branded_name,
                    "mimeType": "application/vnd.google-apps.folder",
                }
                if parent_id:
                    folder_metadata["parents"] = [parent_id]

                folder = (
                    self.drive_service.files().create(body=folder_metadata).execute()
                )
                folder_id = folder.get("id")
                self.logger.info(f"Created new folder: {branded_name}")

            self.folder_cache[cache_key] = folder_id
            return folder_id

        except HttpError as e:
            self.logger.error(f"Error creating/getting folder {branded_name}: {e}")
            return None

    def _upload_docx_as_google_doc(
        self, docx_path: Path, title: str, folder_id: str = None
    ) -> Optional[str]:
        """Upload DOCX file to Google Drive and convert to Google Docs."""
        try:
            # File metadata
            file_metadata = {
                "name": title,
                "mimeType": "application/vnd.google-apps.document",  # Convert to Google Doc
            }

            if folder_id:
                file_metadata["parents"] = [folder_id]

            # Upload file
            media = MediaFileUpload(
                str(docx_path),
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                resumable=True,
            )

            file = (
                self.drive_service.files()
                .create(
                    body=file_metadata, media_body=media, fields="id,name,webViewLink"
                )
                .execute()
            )

            doc_id = file.get("id")
            web_link = file.get("webViewLink")

            self.logger.info(f"Successfully uploaded: {title} (ID: {doc_id})")

            return {"id": doc_id, "name": file.get("name"), "link": web_link}

        except HttpError as e:
            self.logger.error(f"Error uploading {docx_path}: {e}")
            return None

    def convert_file(self, input_path: Path, output_path: Path) -> bool:
        """Convert markdown file to Google Doc via DOCX."""
        try:
            # Create temporary DOCX file
            temp_docx = self.temp_dir / f"{input_path.stem}.docx"

            # Use parent class to create DOCX
            success = super().convert_file(input_path, temp_docx)
            if not success:
                return False

            # Extract metadata for naming
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
            metadata = self.extract_metadata(content, input_path)

            # Determine folder structure using branding manager
            phase = self.get_phase_from_path(input_path)
            folder_structure = self.branding.create_google_drive_folder_structure()
            root_folder_id = self._create_or_get_folder(folder_structure["root"])

            folder_id = root_folder_id
            if phase:
                folder_id = self._create_or_get_folder(phase, root_folder_id)

            # Create branded title
            title = metadata.get("title", input_path.stem.replace("-", " ").title())
            brand_metadata = self.branding.get_brand_metadata(title, phase)
            if phase:
                title = f"[{phase.upper()}] {brand_metadata['title']}"
            else:
                title = brand_metadata["title"]

            # Upload to Google Drive as Google Doc
            doc_info = self._upload_docx_as_google_doc(temp_docx, title, folder_id)

            if doc_info:
                # Log success with Google Doc info
                self.conversion_log.append(
                    {
                        "input": str(input_path),
                        "output": f"Google Doc: {doc_info['link']}",
                        "google_doc_id": doc_info["id"],
                        "google_doc_name": doc_info["name"],
                        "google_doc_link": doc_info["link"],
                        "status": "success",
                        "metadata": metadata,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                self.created_docs.append(doc_info)

                # Clean up temp file
                temp_docx.unlink()

                if self.verbose:
                    self.logger.info(f"Created Google Doc: {title}")
                    self.logger.info(f"Link: {doc_info['link']}")

                return True
            else:
                return False

        except Exception as e:
            self.logger.error(f"Error converting {input_path}: {e}")
            self.failed_conversions.append(
                {
                    "input": str(input_path),
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            )
            return False

    def create_master_index_doc(self) -> Optional[str]:
        """Create a master index Google Doc with links to all created documents."""
        if not self.created_docs:
            return None

        try:
            # Create index document
            index_title = f"[CLIENT] F&I Documentation Index - {datetime.now().strftime('%Y-%m-%d')}"
            doc_body = {"title": index_title}
            doc = self.service.documents().create(body=doc_body).execute()
            doc_id = doc.get("documentId")

            # Build content
            content_lines = [
                f"# {index_title}\n",
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
                f"Total Documents: {len(self.created_docs)}\n\n",
            ]

            # Group by phase
            phase_groups = {}
            for doc in self.created_docs:
                # Extract phase from name
                name = doc["name"]
                if name.startswith("[") and "]" in name:
                    phase = name.split("]")[0][1:]
                    if phase not in phase_groups:
                        phase_groups[phase] = []
                    phase_groups[phase].append(doc)
                else:
                    if "OTHER" not in phase_groups:
                        phase_groups["OTHER"] = []
                    phase_groups["OTHER"].append(doc)

            # Add sections for each phase
            for phase, docs in sorted(phase_groups.items()):
                phase_name = PHASES.get(phase.lower(), {}).get("name", phase)
                content_lines.append(f"## {phase_name}\n\n")

                for doc in docs:
                    content_lines.append(f"- [{doc['name']}]({doc['link']})\n")

                content_lines.append("\n")

            # Insert content
            content = "".join(content_lines)
            requests = [{"insertText": {"location": {"index": 1}, "text": content}}]

            self.service.documents().batchUpdate(
                documentId=doc_id, body={"requests": requests}
            ).execute()

            # Move to branded root folder
            folder_structure = self.branding.create_google_drive_folder_structure()
            root_folder_id = self._create_or_get_folder(folder_structure["root"])
            if root_folder_id:
                self.drive_service.files().update(
                    fileId=doc_id, addParents=root_folder_id, removeParents="root"
                ).execute()

            # Get web link
            file_info = (
                self.drive_service.files()
                .get(fileId=doc_id, fields="webViewLink")
                .execute()
            )

            self.logger.info(f"Created master index: {file_info['webViewLink']}")
            return file_info["webViewLink"]

        except Exception as e:
            self.logger.error(f"Error creating master index: {e}")
            return None

    def save_metadata(self) -> None:
        """Save conversion metadata including Google Doc links."""
        # Ensure metadata directory exists
        METADATA_DIR.mkdir(parents=True, exist_ok=True)

        # Save conversion log with Google Doc info
        log_file = METADATA_DIR / "googledocs-conversion-log.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(self.conversion_log, f, indent=2, ensure_ascii=False)

        # Save failed conversions
        if self.failed_conversions:
            failed_file = METADATA_DIR / "failed-conversions.json"
            with open(failed_file, "w", encoding="utf-8") as f:
                json.dump(self.failed_conversions, f, indent=2, ensure_ascii=False)

        # Create Google Docs index
        index = {
            "conversion_date": datetime.now().isoformat(),
            "total_files": len(self.conversion_log),
            "successful_conversions": len(self.conversion_log),
            "failed_conversions": len(self.failed_conversions),
            "google_docs": self.created_docs,
            "phases": {},
        }

        # Group by phase
        for log_entry in self.conversion_log:
            input_path = Path(log_entry["input"])
            phase = self.get_phase_from_path(input_path)
            if phase:
                if phase not in index["phases"]:
                    index["phases"][phase] = []
                index["phases"][phase].append(
                    {
                        "title": log_entry["metadata"]["title"],
                        "input": log_entry["input"],
                        "google_doc_link": log_entry.get("google_doc_link", ""),
                        "google_doc_id": log_entry.get("google_doc_id", ""),
                    }
                )

        index_file = METADATA_DIR / "googledocs-index.json"
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def cleanup(self):
        """Clean up temporary files."""
        try:
            import shutil

            shutil.rmtree(self.temp_dir)
        except Exception as e:
            self.logger.warning(f"Could not clean up temp directory: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Convert [CLIENT] F&I documentation to Google Docs"
    )
    parser.add_argument(
        "--credentials",
        default="credentials/credentials.json",
        help="Path to Google API credentials file",
    )
    parser.add_argument(
        "--phase", help="Process only specific phase (e.g., 9-contract)"
    )
    parser.add_argument("--file", help="Process only specific file")
    parser.add_argument(
        "--parallel",
        type=int,
        default=2,
        help="Number of parallel conversions (reduced for API limits)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--create-index", action="store_true", help="Create master index document"
    )

    args = parser.parse_args()

    # Setup paths
    base_dir = Path.cwd()
    opportunity_dir = base_dir / OPPORTUNITY_DIR
    output_dir = base_dir / OUTPUT_DIR
    credentials_path = base_dir / args.credentials

    # Check if opportunity directory exists
    if not opportunity_dir.exists():
        print(f"Error: {opportunity_dir} directory not found")
        sys.exit(1)

    # Check credentials file
    if not credentials_path.exists():
        print(f"Error: Credentials file not found: {credentials_path}")
        print(
            "Please download Google API credentials and save as credentials/credentials.json"
        )
        print("See: https://developers.google.com/docs/api/quickstart/python")
        sys.exit(1)

    # Create processor
    try:
        processor = GoogleDocsProcessor(output_dir, credentials_path, args.verbose)
    except Exception as e:
        print(f"Error initializing Google Docs processor: {e}")
        sys.exit(1)

    print("Converting [CLIENT] F&I documentation to Google Docs...")
    print(f"Parallel workers: {args.parallel}")

    try:
        # Process specific file, phase, or all
        if args.file:
            file_path = Path(args.file)
            if not file_path.exists():
                print(f"Error: File not found: {file_path}")
                sys.exit(1)

            print(f"Processing file: {file_path}")
            success = processor.convert_file(file_path, Path("dummy"))
            results = {
                "total": 1,
                "successful": 1 if success else 0,
                "failed": 0 if success else 1,
            }
        elif args.phase:
            phase_dir = opportunity_dir / args.phase
            if not phase_dir.exists():
                print(f"Error: Phase directory not found: {phase_dir}")
                sys.exit(1)

            print(f"Processing phase: {args.phase}")
            results = processor.process_directory(phase_dir, args.parallel)
        else:
            print("Processing all phases...")
            results = processor.process_directory(opportunity_dir, args.parallel)

        # Create master index if requested
        index_link = None
        if args.create_index and processor.created_docs:
            print("Creating master index document...")
            index_link = processor.create_master_index_doc()

        # Save metadata
        processor.save_metadata()

        # Print results
        print("\nConversion Results:")
        print(f"Total files: {results['total']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")

        if results["successful"] > 0:
            print(f"\nCreated {len(processor.created_docs)} Google Docs:")
            for doc in processor.created_docs:
                print(f"  - {doc['name']}: {doc['link']}")

        if index_link:
            print(f"\nMaster Index: {index_link}")

        if results["failed"] > 0:
            print(
                f"\nFailed conversions logged to: {METADATA_DIR / 'failed-conversions.json'}"
            )

        print(f"\nMetadata saved to: {METADATA_DIR}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error during processing: {e}")
        sys.exit(1)
    finally:
        processor.cleanup()


if __name__ == "__main__":
    main()
