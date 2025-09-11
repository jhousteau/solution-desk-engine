"""Simple export tests for coverage."""

from pathlib import Path
from unittest.mock import patch

from solution_desk_engine.export.document_exporter import (
    DocumentExporter,
    ExportFormat,
    ExportResult,
)


class TestExportSimple:
    """Simple export tests for coverage."""

    def test_export_result_success_creation(self):
        """Test creating successful ExportResult."""
        result = ExportResult(success=True, output_path=Path("test.pdf"))
        assert result.success is True
        assert result.output_path == Path("test.pdf")
        assert result.error is None

    def test_export_result_failure_creation(self):
        """Test creating failed ExportResult."""
        result = ExportResult(success=False, error="Test error")
        assert result.success is False
        assert result.output_path is None
        assert result.error == "Test error"

    def test_export_result_minimal(self):
        """Test ExportResult with minimal parameters."""
        result = ExportResult(success=True)
        assert result.success is True
        assert result.output_path is None
        assert result.error is None

    def test_document_exporter_output_dir_creation(self):
        """Test DocumentExporter output directory setup."""
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            exporter = DocumentExporter()
            assert exporter.output_dir == Path("output")
            mock_mkdir.assert_called_once_with(exist_ok=True)

    def test_document_exporter_custom_output_dir(self):
        """Test DocumentExporter with custom output directory."""
        custom_dir = Path("/custom/path")
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            exporter = DocumentExporter(custom_dir)
            assert exporter.output_dir == custom_dir
            mock_mkdir.assert_called_once_with(exist_ok=True)

    def test_export_format_enum_values(self):
        """Test ExportFormat enum values."""
        assert ExportFormat.MARKDOWN.value == "md"
        assert ExportFormat.PDF.value == "pdf"
        assert ExportFormat.DOCX.value == "docx"
        assert ExportFormat.HTML.value == "html"

    def test_export_format_iteration(self):
        """Test iterating over ExportFormat."""
        formats = list(ExportFormat)
        assert len(formats) == 4
        assert ExportFormat.MARKDOWN in formats
        assert ExportFormat.PDF in formats
        assert ExportFormat.DOCX in formats
        assert ExportFormat.HTML in formats
