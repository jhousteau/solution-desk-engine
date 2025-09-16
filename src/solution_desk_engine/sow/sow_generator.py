"""SOW document generator using Google Docs templates."""

import os
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, Optional

from docxtpl import DocxTemplate  # type: ignore

from ..integrations.google_drive import GoogleDriveClient


@dataclass
class SOWContext:
    """Context data for SOW template rendering."""

    customer_name: str
    project_name: str
    contractor_name: str = "Capgemini"
    contractor_poc_name: str = ""
    contractor_poc_email: str = ""
    google_poc_name: str = ""
    google_poc_email: str = ""
    sow_end_date: str = "December 31, 2025"
    max_total_cost: str = ""
    special_terms: str = "N/A"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for template rendering."""
        return {
            "customer_name": self.customer_name,
            "project_name": self.project_name,
            "contractor_name": self.contractor_name,
            "contractor_poc_name": self.contractor_poc_name,
            "contractor_poc_email": self.contractor_poc_email,
            "google_poc_name": self.google_poc_name,
            "google_poc_email": self.google_poc_email,
            "sow_end_date": self.sow_end_date,
            "max_total_cost": self.max_total_cost,
            "special_terms": self.special_terms,
        }


class SOWGenerator:
    """Generate customized SOW documents from Google Docs templates."""

    def __init__(self, google_drive_client: Optional[GoogleDriveClient] = None) -> None:
        """Initialize SOW generator.

        Args:
            google_drive_client: Optional Google Drive client instance
        """
        self.google_drive = google_drive_client or GoogleDriveClient()

    def generate_sow(
        self,
        template_file_id: str,
        context: SOWContext,
        output_name: str,
        output_folder_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate SOW document from Google Docs template.

        Args:
            template_file_id: Google Drive file ID of the SOW template
            context: SOW context data for template rendering
            output_name: Name for the generated SOW document
            output_folder_id: Optional Google Drive folder ID for output

        Returns:
            Dictionary containing generated document info (ID, link, name)

        Raises:
            Exception: If SOW generation fails
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "template.docx")
            output_path = os.path.join(temp_dir, "generated_sow.docx")

            try:
                # 1. Download template from Google Drive as DOCX
                self.google_drive.download_doc_as_docx(template_file_id, template_path)

                # 2. Process template with context data
                self._process_template(template_path, context, output_path)

                # 3. Upload processed document back to Google Drive
                result = self.google_drive.upload_docx_as_google_doc(
                    output_path, output_name, output_folder_id
                )

                return result

            except Exception as error:
                raise Exception(f"Failed to generate SOW: {error}")

    def _process_template(
        self, template_path: str, context: SOWContext, output_path: str
    ) -> None:
        """Process DOCX template with context data.

        Args:
            template_path: Path to template DOCX file
            context: SOW context data
            output_path: Path for processed DOCX file

        Raises:
            Exception: If template processing fails
        """
        try:
            # Load template
            doc = DocxTemplate(template_path)

            # Render with context data
            doc.render(context.to_dict())

            # Save processed document
            doc.save(output_path)

        except Exception as error:
            raise Exception(f"Failed to process template: {error}")

    def get_template_info(self, template_file_id: str) -> Dict[str, Any]:
        """Get information about a SOW template.

        Args:
            template_file_id: Google Drive file ID of the template

        Returns:
            Dictionary containing template metadata
        """
        return self.google_drive.get_file_info(template_file_id)

    def validate_template(self, template_file_id: str) -> bool:
        """Validate that a template file exists and is accessible.

        Args:
            template_file_id: Google Drive file ID of the template

        Returns:
            True if template is valid and accessible
        """
        try:
            file_info = self.google_drive.get_file_info(template_file_id)
            # Check if it's a Google Doc
            return file_info.get("mimeType") == "application/vnd.google-apps.document"
        except Exception:
            return False

    @staticmethod
    def create_context_from_config(config: Dict[str, Any]) -> SOWContext:
        """Create SOW context from configuration dictionary.

        Args:
            config: Configuration dictionary with SOW parameters

        Returns:
            SOWContext instance
        """
        return SOWContext(
            customer_name=config.get("customer_name", ""),
            project_name=config.get("project_name", ""),
            contractor_name=config.get("contractor_name", "Capgemini"),
            contractor_poc_name=config.get("contractor_poc_name", ""),
            contractor_poc_email=config.get("contractor_poc_email", ""),
            google_poc_name=config.get("google_poc_name", ""),
            google_poc_email=config.get("google_poc_email", ""),
            sow_end_date=config.get("sow_end_date", "December 31, 2025"),
            max_total_cost=config.get("max_total_cost", ""),
            special_terms=config.get("special_terms", "N/A"),
        )
