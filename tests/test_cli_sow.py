"""Tests for SOW CLI commands."""

from unittest.mock import Mock, patch

from click.testing import CliRunner

from solution_desk_engine.cli import cli


class TestSOWCLI:
    """Test cases for SOW CLI commands."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("solution_desk_engine.cli.SOWGenerator")
    def test_sow_generate_command_success(self, mock_sow_generator) -> None:
        """Test successful SOW generation via CLI."""
        # Mock the SOW generator
        mock_generator = Mock()
        mock_generator.generate_sow.return_value = {
            "id": "generated_doc_id",
            "web_view_link": "https://docs.google.com/document/d/generated_doc_id/edit",
            "name": "Penske SOW - Test Project",
        }
        mock_sow_generator.return_value = mock_generator

        # Run the CLI command
        result = self.runner.invoke(
            cli,
            [
                "sow",
                "generate",
                "--template-id",
                "test_template_id",
                "--customer-name",
                "Penske",
                "--project-name",
                "Test Project",
                "--output-name",
                "Penske SOW - Test Project",
            ],
        )

        # Verify command succeeded
        assert result.exit_code == 0
        assert "SOW generated successfully!" in result.output
        assert "Penske SOW - Test Project" in result.output
        assert "generated_doc_id" in result.output

        # Verify SOW generator was called correctly
        mock_generator.generate_sow.assert_called_once()
        call_args = mock_generator.generate_sow.call_args
        assert call_args[1]["template_file_id"] == "test_template_id"
        assert call_args[1]["output_name"] == "Penske SOW - Test Project"

    @patch("solution_desk_engine.cli.SOWGenerator")
    def test_sow_validate_template_command_valid(self, mock_sow_generator) -> None:
        """Test template validation CLI command with valid template."""
        # Mock the SOW generator
        mock_generator = Mock()
        mock_generator.validate_template.return_value = True
        mock_generator.get_template_info.return_value = {
            "name": "SOW Template",
            "modifiedTime": "2025-01-01T00:00:00.000Z",
            "webViewLink": "https://docs.google.com/document/d/template_id/edit",
        }
        mock_sow_generator.return_value = mock_generator

        # Run the CLI command
        result = self.runner.invoke(
            cli, ["sow", "validate-template", "--template-id", "valid_template_id"]
        )

        # Verify command succeeded
        assert result.exit_code == 0
        assert "Template is valid!" in result.output
        assert "SOW Template" in result.output

    def test_sow_generate_missing_required_params(self) -> None:
        """Test SOW generate command with missing required parameters."""
        # Run command without required parameters
        result = self.runner.invoke(cli, ["sow", "generate"])

        # Verify command failed with helpful error
        assert result.exit_code != 0
        assert "Missing option" in result.output
