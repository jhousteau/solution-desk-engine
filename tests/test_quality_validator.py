"""Tests for the document quality validation functionality."""

from pathlib import Path
from unittest.mock import mock_open, patch

from solution_desk_engine.quality.validator import (
    DocumentValidator,
    ValidationIssue,
    ValidationResult,
    ValidationSeverity,
)


class TestValidationSeverity:
    """Test cases for ValidationSeverity enum."""

    def test_validation_severity_values(self):
        """Test that all expected severity levels exist."""
        assert ValidationSeverity.ERROR.value == "error"
        assert ValidationSeverity.WARNING.value == "warning"
        assert ValidationSeverity.INFO.value == "info"


class TestValidationIssue:
    """Test cases for ValidationIssue class."""

    def test_validation_issue_creation(self):
        """Test creating ValidationIssue with proper attributes."""
        issue = ValidationIssue(
            severity=ValidationSeverity.ERROR,
            message="Missing citation for financial data",
            line_number=42,
            suggestion="Add citation in format [Source: Company Annual Report 2023]",
        )

        assert issue.severity == ValidationSeverity.ERROR
        assert issue.message == "Missing citation for financial data"
        assert issue.line_number == 42
        assert (
            issue.suggestion
            == "Add citation in format [Source: Company Annual Report 2023]"
        )

    def test_validation_issue_optional_fields(self):
        """Test ValidationIssue with optional fields."""
        issue = ValidationIssue(
            severity=ValidationSeverity.INFO, message="Possible spelling error"
        )

        assert issue.line_number is None
        assert issue.suggestion is None


class TestValidationResult:
    """Test cases for ValidationResult class."""

    def test_validation_result_creation(self):
        """Test creating ValidationResult with proper attributes."""
        document_path = Path("test.md")
        issues = [ValidationIssue(ValidationSeverity.WARNING, "Test warning")]

        result = ValidationResult(
            document_path=document_path, issues=issues, score=75.5
        )

        assert result.document_path == document_path
        assert len(result.issues) == 1
        assert result.score == 75.5

    def test_validation_result_properties(self):
        """Test ValidationResult computed properties."""
        document_path = Path("test.md")

        # Test with errors
        issues_with_errors = [
            ValidationIssue(ValidationSeverity.ERROR, "Error message"),
            ValidationIssue(ValidationSeverity.WARNING, "Warning message"),
        ]
        result_with_errors = ValidationResult(document_path, issues_with_errors, 60.0)

        assert result_with_errors.has_errors is True
        assert result_with_errors.has_warnings is True
        assert result_with_errors.is_valid is False

        # Test without errors
        issues_without_errors = [
            ValidationIssue(ValidationSeverity.WARNING, "Warning only")
        ]
        result_without_errors = ValidationResult(
            document_path, issues_without_errors, 85.0
        )

        assert result_without_errors.has_errors is False
        assert result_without_errors.has_warnings is True
        assert result_without_errors.is_valid is True  # No errors means valid

        # Test clean document
        clean_result = ValidationResult(document_path, [], 100.0)
        assert clean_result.has_errors is False
        assert clean_result.has_warnings is False
        assert clean_result.is_valid is True


class TestDocumentValidator:
    """Test cases for DocumentValidator class."""

    def test_validator_initialization_defaults(self):
        """Test DocumentValidator initialization with default settings."""
        validator = DocumentValidator()

        assert hasattr(validator, "citation_patterns")

    @patch("pathlib.Path.exists", return_value=False)
    def test_validate_document_file_not_found(self, mock_exists):
        """Test validation with non-existent file."""
        validator = DocumentValidator()

        result = validator.validate_document(Path("nonexistent.md"))

        assert isinstance(result, ValidationResult)
        assert result.document_path == Path("nonexistent.md")
        assert result.score == 0.0
        assert len(result.issues) > 0
        assert result.has_errors is True

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="# Test Document\n\nThis is a test document with sufficient content to meet word count requirements and proper structure.",
    )
    @patch("pathlib.Path.exists", return_value=True)
    def test_validate_document_success(self, mock_exists, mock_file):
        """Test successful document validation."""
        validator = DocumentValidator()

        result = validator.validate_document(Path("test.md"))

        assert isinstance(result, ValidationResult)
        assert result.document_path == Path("test.md")
        assert result.score >= 0
        assert result.score <= 100

    @patch(
        "builtins.open", new_callable=mock_open, read_data="# Test\n\nShort content."
    )
    @patch("pathlib.Path.exists", return_value=True)
    def test_validate_document_with_content(self, mock_exists, mock_file):
        """Test validation with actual content."""
        validator = DocumentValidator()

        result = validator.validate_document(Path("test.md"))

        assert isinstance(result, ValidationResult)
        assert result.document_path == Path("test.md")
        # Should have some score even for short content
        assert 0 <= result.score <= 100

    def test_validate_multiple_documents(self):
        """Test validating multiple documents."""
        validator = DocumentValidator()

        mock_content = "# Test Document\n\nThis is test content."

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=mock_content)),
        ):
            file_paths = [Path("test1.md"), Path("test2.md")]
            results = validator.validate_multiple_documents(file_paths)

            assert len(results) == 2
            assert all(
                isinstance(result, ValidationResult) for result in results.values()
            )
            assert all(path in results for path in file_paths)

    def test_check_structure(self):
        """Test document structure checking."""
        validator = DocumentValidator()

        # Test good structure
        good_content = "# Title\n\n## Section\n\nContent here."
        lines = good_content.split("\n")
        doc_path = Path("test.md")
        good_issues = validator._check_structure(good_content, lines, doc_path)
        assert isinstance(good_issues, list)

        # Test poor structure
        poor_content = "No title or headers just text."
        lines = poor_content.split("\n")
        poor_issues = validator._check_structure(poor_content, lines, doc_path)
        assert isinstance(poor_issues, list)

    def test_check_citations(self):
        """Test citation checking functionality."""
        validator = DocumentValidator()

        # Test content with citations
        content_with_citations = "Revenue was $1M [Source: Annual Report]. Growth is 15% [Source: Market Study]."
        lines = content_with_citations.split("\n")
        doc_path = Path("test.md")
        citation_issues = validator._check_citations(
            content_with_citations, lines, doc_path
        )
        assert isinstance(citation_issues, list)

        # Test content without citations
        content_without_citations = (
            "Revenue was $1M. Growth is 15%. No sources provided."
        )
        lines = content_without_citations.split("\n")
        no_citation_issues = validator._check_citations(
            content_without_citations, lines, doc_path
        )
        assert isinstance(no_citation_issues, list)

    def test_check_professional_tone(self):
        """Test professional tone checking."""
        validator = DocumentValidator()

        # Test professional content
        professional_content = "The analysis demonstrates significant market opportunity through comprehensive evaluation."
        lines = professional_content.split("\n")
        doc_path = Path("test.md")
        professional_issues = validator._check_professional_language(
            professional_content, lines, doc_path
        )
        assert isinstance(professional_issues, list)

        # Test unprofessional content
        unprofessional_content = (
            "This is totally awesome!!! We should definitely do this ASAP."
        )
        lines = unprofessional_content.split("\n")
        unprofessional_issues = validator._check_professional_language(
            unprofessional_content, lines, doc_path
        )
        assert isinstance(unprofessional_issues, list)

    def test_calculate_quality_score(self):
        """Test quality score calculation."""
        validator = DocumentValidator()

        # Test with no issues
        no_issues = []
        test_content = "This is test content for quality scoring."
        high_score = validator._calculate_quality_score(no_issues, test_content)
        assert 80 <= high_score <= 100

        # Test with some issues
        some_issues = [
            ValidationIssue(ValidationSeverity.WARNING, "Minor issue"),
            ValidationIssue(ValidationSeverity.INFO, "Suggestion"),
        ]
        medium_score = validator._calculate_quality_score(some_issues, test_content)
        assert 0 <= medium_score <= 100

        # Test with errors
        error_issues = [
            ValidationIssue(ValidationSeverity.ERROR, "Critical issue"),
            ValidationIssue(ValidationSeverity.WARNING, "Warning"),
        ]
        low_score = validator._calculate_quality_score(error_issues, test_content)
        assert 0 <= low_score <= 100

    def test_validate_document_exception_handling(self):
        """Test validation with file read exceptions."""
        validator = DocumentValidator()

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("builtins.open", side_effect=IOError("File read error")),
        ):
            result = validator.validate_document(Path("problematic.md"))

            assert isinstance(result, ValidationResult)
            assert result.has_errors is True
            assert result.score == 0.0
