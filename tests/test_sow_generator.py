"""Tests for SOW generator."""

from unittest.mock import Mock, patch

import pytest

from solution_desk_engine.sow.sow_generator import SOWContext, SOWGenerator


class TestSOWContext:
    """Test cases for SOWContext."""

    def test_context_creation(self) -> None:
        """Test SOW context creation with required fields."""
        context = SOWContext(
            customer_name="Penske", project_name="Franchise Lease Management"
        )

        assert context.customer_name == "Penske"
        assert context.project_name == "Franchise Lease Management"
        assert context.contractor_name == "Capgemini"  # Default value

    def test_context_to_dict(self) -> None:
        """Test converting context to dictionary."""
        context = SOWContext(
            customer_name="Penske",
            project_name="Franchise Lease Management",
            contractor_poc_name="John Doe",
            contractor_poc_email="john.doe@capgemini.com",
        )

        context_dict = context.to_dict()

        assert context_dict["customer_name"] == "Penske"
        assert context_dict["project_name"] == "Franchise Lease Management"
        assert context_dict["contractor_poc_name"] == "John Doe"
        assert context_dict["contractor_poc_email"] == "john.doe@capgemini.com"

    def test_create_context_from_config(self) -> None:
        """Test creating context from configuration dictionary."""
        config = {
            "customer_name": "Penske",
            "project_name": "Franchise Lease Management",
            "contractor_poc_name": "Jane Smith",
            "max_total_cost": "$500,000",
        }

        context = SOWGenerator.create_context_from_config(config)

        assert context.customer_name == "Penske"
        assert context.project_name == "Franchise Lease Management"
        assert context.contractor_poc_name == "Jane Smith"
        assert context.max_total_cost == "$500,000"
        assert context.contractor_name == "Capgemini"  # Default


class TestSOWGenerator:
    """Test cases for SOWGenerator."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_google_drive = Mock()
        self.generator = SOWGenerator(google_drive_client=self.mock_google_drive)

    def test_initialization_with_default_client(self) -> None:
        """Test generator initialization with default Google Drive client."""
        generator = SOWGenerator()
        assert generator.google_drive is not None

    def test_initialization_with_custom_client(self) -> None:
        """Test generator initialization with custom Google Drive client."""
        assert self.generator.google_drive == self.mock_google_drive

    @patch("solution_desk_engine.sow.sow_generator.DocxTemplate")
    @patch("tempfile.TemporaryDirectory")
    def test_generate_sow_success(self, mock_temp_dir, mock_docx_template) -> None:
        """Test successful SOW generation."""
        # Mock temporary directory
        mock_temp_dir.return_value.__enter__.return_value = "/tmp/test"

        # Mock DocxTemplate
        mock_template = Mock()
        mock_docx_template.return_value = mock_template

        # Mock Google Drive operations
        expected_result = {
            "id": "generated_doc_id",
            "web_view_link": "https://docs.google.com/document/d/generated_doc_id/edit",
            "name": "Penske SOW - Franchise Lease Management",
        }
        self.mock_google_drive.upload_docx_as_google_doc.return_value = expected_result

        # Create test context
        context = SOWContext(
            customer_name="Penske", project_name="Franchise Lease Management"
        )

        # Test SOW generation
        result = self.generator.generate_sow(
            template_file_id="template_id",
            context=context,
            output_name="Penske SOW - Franchise Lease Management",
        )

        # Verify Google Drive operations
        self.mock_google_drive.download_doc_as_docx.assert_called_once()
        self.mock_google_drive.upload_docx_as_google_doc.assert_called_once()

        # Verify template processing
        mock_template.render.assert_called_once_with(context.to_dict())
        mock_template.save.assert_called_once()

        # Verify result
        assert result == expected_result

    @patch("solution_desk_engine.sow.sow_generator.DocxTemplate")
    def test_process_template_success(self, mock_docx_template) -> None:
        """Test successful template processing."""
        mock_template = Mock()
        mock_docx_template.return_value = mock_template

        context = SOWContext(
            customer_name="Penske", project_name="Franchise Lease Management"
        )

        # Test template processing
        self.generator._process_template(
            "/tmp/template.docx", context, "/tmp/output.docx"
        )

        # Verify template operations
        mock_docx_template.assert_called_once_with("/tmp/template.docx")
        mock_template.render.assert_called_once_with(context.to_dict())
        mock_template.save.assert_called_once_with("/tmp/output.docx")

    def test_get_template_info(self) -> None:
        """Test getting template information."""
        expected_info = {
            "id": "template_id",
            "name": "SOW Template",
            "mimeType": "application/vnd.google-apps.document",
        }
        self.mock_google_drive.get_file_info.return_value = expected_info

        result = self.generator.get_template_info("template_id")

        assert result == expected_info
        self.mock_google_drive.get_file_info.assert_called_once_with("template_id")

    def test_validate_template_valid(self) -> None:
        """Test validating a valid Google Docs template."""
        self.mock_google_drive.get_file_info.return_value = {
            "mimeType": "application/vnd.google-apps.document"
        }

        result = self.generator.validate_template("template_id")

        assert result is True
        self.mock_google_drive.get_file_info.assert_called_once_with("template_id")

    def test_validate_template_invalid_mime_type(self) -> None:
        """Test validating template with invalid MIME type."""
        self.mock_google_drive.get_file_info.return_value = {
            "mimeType": "application/pdf"
        }

        result = self.generator.validate_template("template_id")

        assert result is False

    def test_validate_template_error(self) -> None:
        """Test validating template when API call fails."""
        self.mock_google_drive.get_file_info.side_effect = Exception("API Error")

        result = self.generator.validate_template("template_id")

        assert result is False

    def test_generate_sow_with_folder_id(self) -> None:
        """Test SOW generation with output folder specified."""
        with (
            patch("tempfile.TemporaryDirectory"),
            patch("solution_desk_engine.sow.sow_generator.DocxTemplate"),
        ):
            expected_result = {"id": "doc_id", "web_view_link": "link", "name": "name"}
            self.mock_google_drive.upload_docx_as_google_doc.return_value = (
                expected_result
            )

            context = SOWContext("Customer", "Project")

            self.generator.generate_sow(
                template_file_id="template_id",
                context=context,
                output_name="Test SOW",
                output_folder_id="folder_id",
            )

            # Verify folder ID was passed to upload
            self.mock_google_drive.upload_docx_as_google_doc.assert_called_once()
            call_args = self.mock_google_drive.upload_docx_as_google_doc.call_args
            assert call_args[0][2] == "folder_id"  # output_folder_id parameter

    @patch("solution_desk_engine.sow.sow_generator.DocxTemplate")
    def test_process_template_error(self, mock_docx_template) -> None:
        """Test template processing with error."""
        mock_docx_template.side_effect = Exception("Template error")

        context = SOWContext("Customer", "Project")

        with pytest.raises(Exception, match="Failed to process template"):
            self.generator._process_template(
                "/tmp/template.docx", context, "/tmp/output.docx"
            )
