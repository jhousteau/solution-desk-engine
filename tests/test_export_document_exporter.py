"""Tests for the document export functionality."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from solution_desk_engine.export.document_exporter import (
    DocumentExporter,
    ExportFormat,
    ExportResult,
)


class TestExportFormat:
    """Test cases for ExportFormat enum."""

    def test_export_format_values(self):
        """Test that all expected export formats exist."""
        assert ExportFormat.MARKDOWN.value == "md"
        assert ExportFormat.PDF.value == "pdf"
        assert ExportFormat.DOCX.value == "docx"
        assert ExportFormat.HTML.value == "html"


class TestExportResult:
    """Test cases for ExportResult class."""

    def test_export_result_success(self):
        """Test creating successful export result."""
        output_path = Path("/test/output.pdf")
        result = ExportResult(success=True, output_path=output_path)

        assert result.success is True
        assert result.output_path == output_path
        assert result.error is None

    def test_export_result_failure(self):
        """Test creating failed export result."""
        error_msg = "Export failed"
        result = ExportResult(success=False, error=error_msg)

        assert result.success is False
        assert result.output_path is None
        assert result.error == error_msg


class TestDocumentExporter:
    """Test cases for DocumentExporter class."""

    def test_exporter_initialization_default(self):
        """Test DocumentExporter initialization with default output directory."""
        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter()

            assert exporter.output_dir == Path("output")

    def test_exporter_initialization_custom(self):
        """Test DocumentExporter initialization with custom output directory."""
        custom_dir = Path("/custom/output")
        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter(custom_dir)

            assert exporter.output_dir == custom_dir

    @patch("subprocess.run")
    @patch("pathlib.Path.exists", return_value=True)
    def test_export_to_pdf_success(self, mock_exists, mock_subprocess):
        """Test successful PDF export using pandoc."""
        mock_subprocess.return_value = MagicMock(returncode=0)

        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter()
            source_path = Path("test.md")

            result = exporter.export_document(source_path, ExportFormat.PDF)

            assert result.success is True
            assert result.output_path == exporter.output_dir / "test.pdf"
            assert result.error is None

            # Verify pandoc was called
            mock_subprocess.assert_called_once()

    @patch("subprocess.run")
    @patch("pathlib.Path.exists", return_value=True)
    def test_export_to_docx_success(self, mock_exists, mock_subprocess):
        """Test successful DOCX export using pandoc."""
        mock_subprocess.return_value = MagicMock(returncode=0)

        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter()
            source_path = Path("test.md")

            result = exporter.export_document(source_path, ExportFormat.DOCX)

            assert result.success is True
            assert result.output_path == exporter.output_dir / "test.docx"
            assert result.error is None

    @patch("pathlib.Path.exists", return_value=True)
    def test_export_to_html_success(self, mock_exists):
        """Test successful HTML export using markdown library."""
        mock_content = "# Test Document\n\nThis is test content."

        with (
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", mock_open(read_data=mock_content)),
        ):
            # Mock the markdown import within the method
            with patch("builtins.__import__") as mock_import:
                mock_markdown = MagicMock()
                mock_markdown.markdown.return_value = (
                    "<h1>Test Document</h1><p>This is test content.</p>"
                )

                def side_effect(name, *args, **kwargs):
                    if name == "markdown":
                        return mock_markdown
                    return __import__(name, *args, **kwargs)

                mock_import.side_effect = side_effect

                exporter = DocumentExporter()
                source_path = Path("test.md")

                result = exporter.export_document(source_path, ExportFormat.HTML)

                assert result.success is True
                assert result.output_path == exporter.output_dir / "test.html"
                assert result.error is None

    @patch("pathlib.Path.exists", return_value=True)
    def test_export_markdown_copy(self, mock_exists):
        """Test markdown export (simple copy operation)."""
        mock_content = "# Test Document\n\nThis is a test."

        with (
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", mock_open(read_data=mock_content)) as _mock_file,
            patch("shutil.copy2") as mock_copy,
        ):
            exporter = DocumentExporter()
            source_path = Path("test.md")

            result = exporter.export_document(source_path, ExportFormat.MARKDOWN)

            assert result.success is True
            assert result.output_path == exporter.output_dir / "test.md"
            mock_copy.assert_called_once()

    @patch("pathlib.Path.exists", return_value=False)
    def test_export_nonexistent_file(self, mock_exists):
        """Test export with non-existent source file."""
        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter()
            source_path = Path("nonexistent.md")

            result = exporter.export_document(source_path, ExportFormat.PDF)

            assert result.success is False
            assert "Source file not found" in result.error

    @patch("subprocess.run")
    @patch("pathlib.Path.exists", return_value=True)
    def test_export_subprocess_error(self, mock_exists, mock_subprocess):
        """Test export with subprocess error."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, "pandoc")

        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter()
            source_path = Path("test.md")

            # Mock the fallback imports to fail as well for clean error testing
            with patch(
                "builtins.__import__", side_effect=ImportError("No fallback available")
            ):
                result = exporter.export_document(source_path, ExportFormat.PDF)

                assert result.success is False
                assert "PDF export requires pandoc or weasyprint" in result.error

    @patch("subprocess.run")
    @patch("pathlib.Path.exists", return_value=True)
    def test_export_multiple_documents(self, mock_exists, mock_subprocess):
        """Test exporting multiple documents."""
        mock_subprocess.return_value = MagicMock(returncode=0)

        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter()
            source_paths = [Path("test1.md"), Path("test2.md")]

            # Test with single format (this is what the method actually supports)
            results = exporter.export_multiple_documents(source_paths, ExportFormat.PDF)

            assert len(results) == 2
            assert all(isinstance(result, ExportResult) for result in results.values())
            assert all(result.success for result in results.values())

    @patch("subprocess.run")
    @patch("pathlib.Path.exists", return_value=True)
    def test_export_with_custom_output_name(self, mock_exists, mock_subprocess):
        """Test export with custom output filename."""
        mock_subprocess.return_value = MagicMock(returncode=0)

        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter()
            source_path = Path("test.md")
            custom_name = "custom_output"

            result = exporter.export_document(
                source_path, ExportFormat.PDF, output_name=custom_name
            )

            assert result.success is True
            assert result.output_path == exporter.output_dir / f"{custom_name}.pdf"

    def test_get_export_summary(self):
        """Test generating export summary."""
        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter()

            # Create mock results
            results = {
                Path("test1.md"): ExportResult(
                    success=True, output_path=Path("output/test1.pdf")
                ),
                Path("test2.md"): ExportResult(success=False, error="Export failed"),
                Path("test3.md"): ExportResult(
                    success=True, output_path=Path("output/test3.html")
                ),
            }

            summary = exporter.get_export_summary(results)

            assert isinstance(summary, dict)
            assert "total_files" in summary
            assert "successful" in summary
            assert "failed" in summary
            assert "success_rate" in summary
            assert "output_files" in summary
            assert "errors" in summary

            assert summary["total_files"] == 3
            assert summary["successful"] == 2
            assert summary["failed"] == 1

    @patch("subprocess.run")
    @patch("pathlib.Path.exists", return_value=True)
    def test_pdf_export_with_fallback(self, mock_exists, mock_subprocess):
        """Test PDF export with fallback when pandoc fails."""
        # First call (pandoc) fails
        mock_subprocess.side_effect = [
            subprocess.CalledProcessError(1, "pandoc"),
            MagicMock(returncode=0),  # weasyprint fallback succeeds
        ]

        mock_markdown_content = "# Test\nContent"
        mock_html_content = "<h1>Test</h1><p>Content</p>"

        with (
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", mock_open(read_data=mock_markdown_content)),
        ):
            # Mock the imports within the method
            with patch("builtins.__import__") as mock_import:
                mock_markdown = MagicMock()
                mock_weasyprint = MagicMock()

                def side_effect(name, *args, **kwargs):
                    if name == "markdown":
                        return mock_markdown
                    elif name == "weasyprint":
                        return mock_weasyprint
                    return __import__(name, *args, **kwargs)

                mock_import.side_effect = side_effect

                mock_markdown.markdown.return_value = mock_html_content
                mock_html_doc = MagicMock()
                mock_weasyprint.HTML.return_value = mock_html_doc

                exporter = DocumentExporter()
                source_path = Path("test.md")

                result = exporter.export_document(source_path, ExportFormat.PDF)

                assert result.success is True

    @patch("subprocess.run")
    @patch("pathlib.Path.exists", return_value=True)
    def test_docx_export_with_fallback(self, mock_exists, mock_subprocess):
        """Test DOCX export with fallback when pandoc fails."""
        # Pandoc fails
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, "pandoc")

        mock_content = "# Test Document\n\nThis is test content."

        with (
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", mock_open(read_data=mock_content)),
        ):
            # Mock the imports within the method
            with patch("builtins.__import__") as mock_import:
                mock_docx = MagicMock()

                def side_effect(name, *args, **kwargs):
                    if name == "docx":
                        return mock_docx
                    return __import__(name, *args, **kwargs)

                mock_import.side_effect = side_effect

                mock_doc = MagicMock()
                mock_docx.Document.return_value = mock_doc

                exporter = DocumentExporter()
                source_path = Path("test.md")

                result = exporter.export_document(source_path, ExportFormat.DOCX)

                assert result.success is True
                mock_doc.save.assert_called_once()

    @patch("pathlib.Path.exists", return_value=True)
    def test_unsupported_format_error(self, mock_exists):
        """Test error handling for unsupported export format."""
        with patch("pathlib.Path.mkdir"):
            exporter = DocumentExporter()
            source_path = Path("test.md")

            # Create a mock unsupported format
            class UnsupportedFormat:
                value = "xyz"

            unsupported_format = UnsupportedFormat()

            result = exporter.export_document(source_path, unsupported_format)

            assert result.success is False
            assert "Unsupported format" in result.error

    def test_batch_export_summary(self):
        """Test batch export with mixed success/failure results."""
        with (
            patch("pathlib.Path.mkdir"),
            patch.object(DocumentExporter, "export_document") as mock_export,
        ):
            # Mock some successes and failures
            mock_export.side_effect = [
                ExportResult(success=True, output_path=Path("output/doc1.pdf")),
                ExportResult(success=False, error="Export failed"),
                ExportResult(success=True, output_path=Path("output/doc3.html")),
            ]

            exporter = DocumentExporter()
            source_paths = [Path("doc1.md"), Path("doc2.md"), Path("doc3.md")]

            results = exporter.export_multiple_documents(source_paths, ExportFormat.PDF)

            assert len(results) == 3

            # Count successes and failures
            successes = sum(1 for result in results.values() if result.success)
            failures = sum(1 for result in results.values() if not result.success)

            assert successes == 2
            assert failures == 1
