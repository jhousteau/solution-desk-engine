"""Quality validation for technical sales documents."""

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console  # type: ignore

console = Console()


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """A validation issue found in a document."""

    severity: ValidationSeverity
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of document validation."""

    document_path: Path
    issues: List[ValidationIssue]
    score: float  # 0-100 quality score

    @property
    def has_errors(self) -> bool:
        return any(issue.severity == ValidationSeverity.ERROR for issue in self.issues)

    @property
    def has_warnings(self) -> bool:
        return any(
            issue.severity == ValidationSeverity.WARNING for issue in self.issues
        )

    @property
    def is_valid(self) -> bool:
        return not self.has_errors


class DocumentValidator:
    """Validates technical sales documents for quality and completeness."""

    def __init__(self) -> None:
        """Initialize the document validator."""
        self.citation_patterns = [
            r"\[[\w\s\d\-,\.]+\]",  # [Source Name, Date]
            r"¹²³⁴⁵⁶⁷⁸⁹",  # Superscript numbers
            r"\(\d{4}\)",  # (Year)
            r"Retrieved from",  # Citation endings
        ]

        self.financial_keywords = [
            "revenue",
            "profit",
            "income",
            "sales",
            "cost",
            "margin",
            "growth",
            "percentage",
            "billion",
            "million",
            "dollar",
        ]

        self.quality_checks = [
            self._check_citations,
            self._check_financial_data_citations,
            self._check_structure,
            self._check_completeness,
            self._check_professional_language,
            self._check_technical_accuracy,
        ]

    def validate_document(self, document_path: Path) -> ValidationResult:
        """Validate a single document for quality and completeness.

        Args:
            document_path: Path to the markdown document

        Returns:
            ValidationResult with issues and quality score
        """
        if not document_path.exists():
            return ValidationResult(
                document_path=document_path,
                issues=[
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message=f"Document not found: {document_path}",
                    )
                ],
                score=0.0,
            )

        try:
            with open(document_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return ValidationResult(
                document_path=document_path,
                issues=[
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message=f"Failed to read document: {str(e)}",
                    )
                ],
                score=0.0,
            )

        issues = []
        lines = content.split("\n")

        # Run all quality checks
        for check in self.quality_checks:
            check_issues = check(content, lines, document_path)
            issues.extend(check_issues)

        # Calculate quality score
        score = self._calculate_quality_score(issues, content)

        return ValidationResult(document_path=document_path, issues=issues, score=score)

    def _check_citations(
        self, content: str, lines: List[str], doc_path: Path
    ) -> List[ValidationIssue]:
        """Check for proper citations throughout the document."""
        issues = []

        # Check for References section
        if (
            "references" not in content.lower()
            and "bibliography" not in content.lower()
        ):
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="No References section found",
                    suggestion="Add a References section at the end of the document",
                )
            )

        # Check for citation patterns
        citation_found = False
        for pattern in self.citation_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                citation_found = True
                break

        if not citation_found and len(content) > 1000:  # Only for substantial documents
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="No citation patterns found in document",
                    suggestion="Add proper citations using footnotes or reference format",
                )
            )

        return issues

    def _check_financial_data_citations(
        self, content: str, lines: List[str], doc_path: Path
    ) -> List[ValidationIssue]:
        """Check that financial data has proper citations."""
        issues = []

        for i, line in enumerate(lines, 1):
            line_lower = line.lower()

            # Check for financial data without citations
            has_financial_keyword = any(
                keyword in line_lower for keyword in self.financial_keywords
            )
            has_specific_number = re.search(r"\$[\d,]+|\d+%|\d+\.\d+%", line)

            if has_financial_keyword and has_specific_number:
                # Check if line has citation
                has_citation = any(
                    re.search(pattern, line, re.IGNORECASE)
                    for pattern in self.citation_patterns
                )

                if not has_citation:
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.ERROR,
                            message="Financial data without citation",
                            line_number=i,
                            suggestion="Add citation for financial data using footnote or reference",
                        )
                    )

        return issues

    def _check_structure(
        self, content: str, lines: List[str], doc_path: Path
    ) -> List[ValidationIssue]:
        """Check document structure and organization."""
        issues = []

        # Check for title
        if not content.startswith("#"):
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="Document should start with a title (# heading)",
                    suggestion="Add a title at the beginning of the document",
                )
            )

        # Check for section headers
        headers = [line for line in lines if line.startswith("#")]
        if len(headers) < 3:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="Document has very few sections",
                    suggestion="Consider organizing content into clear sections with headers",
                )
            )

        # Check for consistent header levels
        header_levels = [len(h.split()[0]) for h in headers if h.strip()]
        if header_levels and max(header_levels) - min(header_levels) > 3:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message="Inconsistent header levels",
                    suggestion="Use consistent header hierarchy (# ## ### etc.)",
                )
            )

        return issues

    def _check_completeness(
        self, content: str, lines: List[str], doc_path: Path
    ) -> List[ValidationIssue]:
        """Check document completeness."""
        issues = []

        # Check for placeholder content
        placeholders = re.findall(r"\[[\w_]+\]", content)
        if placeholders:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Found {len(placeholders)} placeholder(s) that need completion: {', '.join(set(placeholders[:5]))}",
                    suggestion="Replace all placeholders with actual content",
                )
            )

        # Check minimum content length
        word_count = len(content.split())
        if word_count < 100:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message=f"Document is very short ({word_count} words)",
                    suggestion="Consider adding more detailed content",
                )
            )

        # Check for TODO items
        todos = [
            line for line in lines if "TODO" in line.upper() or "FIXME" in line.upper()
        ]
        if todos:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message=f"Found {len(todos)} TODO/FIXME item(s)",
                    suggestion="Complete all TODO and FIXME items",
                )
            )

        return issues

    def _check_professional_language(
        self, content: str, lines: List[str], doc_path: Path
    ) -> List[ValidationIssue]:
        """Check for professional language and tone."""
        issues = []

        # Check for informal language
        informal_words = ["gonna", "wanna", "kinda", "yeah", "ok", "cool", "awesome"]
        found_informal = [word for word in informal_words if word in content.lower()]

        if found_informal:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    message=f"Informal language found: {', '.join(found_informal)}",
                    suggestion="Use professional language throughout the document",
                )
            )

        # Check for proper capitalization in headers
        for i, line in enumerate(lines, 1):
            if line.startswith("#"):
                title = line.lstrip("#").strip()
                if title and not title[0].isupper():
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.WARNING,
                            message="Header should start with capital letter",
                            line_number=i,
                            suggestion="Capitalize the first word of headers",
                        )
                    )

        return issues

    def _check_technical_accuracy(
        self, content: str, lines: List[str], doc_path: Path
    ) -> List[ValidationIssue]:
        """Check for technical accuracy and consistency."""
        issues = []

        # Check for consistent terminology
        # This is a simplified check - could be expanded with domain-specific dictionaries

        # Check for broken URLs
        url_pattern = r"https?://[^\s)]+"
        urls = re.findall(url_pattern, content)

        for url in urls:
            if "example.com" in url or "[URL]" in url or url.endswith("..."):
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        message=f"Placeholder URL found: {url}",
                        suggestion="Replace with actual URL",
                    )
                )

        return issues

    def _calculate_quality_score(
        self, issues: List[ValidationIssue], content: str
    ) -> float:
        """Calculate overall quality score (0-100)."""
        base_score = 100.0

        # Deduct points for issues
        for issue in issues:
            if issue.severity == ValidationSeverity.ERROR:
                base_score -= 15.0
            elif issue.severity == ValidationSeverity.WARNING:
                base_score -= 5.0
            else:  # INFO
                base_score -= 1.0

        # Bonus points for good practices
        word_count = len(content.split())
        if word_count > 500:
            base_score += 2.0

        # Check for good citation practices
        if any(pattern in content for pattern in ["Retrieved from", "References", "¹"]):
            base_score += 3.0

        # Check for structured content
        if content.count("\n## ") > 2:  # Multiple sections
            base_score += 2.0

        return max(0.0, min(100.0, base_score))

    def validate_multiple_documents(
        self, document_paths: List[Path]
    ) -> Dict[Path, ValidationResult]:
        """Validate multiple documents.

        Args:
            document_paths: List of document paths to validate

        Returns:
            Dictionary mapping paths to validation results
        """
        results = {}

        for doc_path in document_paths:
            console.print(f"Validating {doc_path.name}...")
            result = self.validate_document(doc_path)
            results[doc_path] = result

            if result.has_errors:
                console.print(
                    f"✗ {doc_path.name}: {len([i for i in result.issues if i.severity == ValidationSeverity.ERROR])} errors",
                    style="red",
                )
            elif result.has_warnings:
                console.print(
                    f"⚠ {doc_path.name}: {len([i for i in result.issues if i.severity == ValidationSeverity.WARNING])} warnings",
                    style="yellow",
                )
            else:
                console.print(f"✓ {doc_path.name}: No issues", style="green")

        return results

    def generate_validation_report(
        self, results: Dict[Path, ValidationResult]
    ) -> Dict[str, Any]:
        """Generate a comprehensive validation report.

        Args:
            results: Dictionary of validation results

        Returns:
            Summary report dictionary
        """
        total_docs = len(results)
        error_docs = sum(1 for result in results.values() if result.has_errors)
        warning_docs = sum(1 for result in results.values() if result.has_warnings)
        clean_docs = total_docs - error_docs - warning_docs

        avg_score = (
            sum(result.score for result in results.values()) / total_docs
            if total_docs
            else 0
        )

        return {
            "summary": {
                "total_documents": total_docs,
                "documents_with_errors": error_docs,
                "documents_with_warnings": warning_docs,
                "clean_documents": clean_docs,
                "average_quality_score": round(avg_score, 1),
            },
            "document_scores": {
                str(path): result.score for path, result in results.items()
            },
            "top_issues": self._get_top_issues(results),
            "recommendations": self._generate_recommendations(results),
        }

    def _get_top_issues(
        self, results: Dict[Path, ValidationResult]
    ) -> List[Dict[str, Any]]:
        """Get the most common validation issues."""
        issue_counts: Dict[str, int] = {}

        for result in results.values():
            for issue in result.issues:
                key = f"{issue.severity.value}: {issue.message.split('.')[0]}"  # Use first sentence
                issue_counts[key] = issue_counts.get(key, 0) + 1

        # Sort by frequency
        sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)

        return [{"issue": issue, "count": count} for issue, count in sorted_issues[:10]]

    def _generate_recommendations(
        self, results: Dict[Path, ValidationResult]
    ) -> List[str]:
        """Generate improvement recommendations based on validation results."""
        recommendations = []

        # Check for common patterns
        total_docs = len(results)
        citation_issues = sum(
            1
            for result in results.values()
            if any("citation" in issue.message.lower() for issue in result.issues)
        )

        if citation_issues > total_docs * 0.3:
            recommendations.append(
                "Implement consistent citation standards across all documents"
            )

        structure_issues = sum(
            1
            for result in results.values()
            if any(
                "structure" in issue.message.lower()
                or "header" in issue.message.lower()
                for issue in result.issues
            )
        )

        if structure_issues > total_docs * 0.3:
            recommendations.append("Improve document structure and organization")

        placeholder_issues = sum(
            1
            for result in results.values()
            if any("placeholder" in issue.message.lower() for issue in result.issues)
        )

        if placeholder_issues > 0:
            recommendations.append(
                "Complete all placeholder content before document finalization"
            )

        return recommendations
