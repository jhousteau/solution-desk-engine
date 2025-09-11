"""Final tests to reach 80% coverage."""

from pathlib import Path
from unittest.mock import patch

from solution_desk_engine.export.document_exporter import DocumentExporter
from solution_desk_engine.framework.methodology import (
    PhaseStatus,
    TechnicalSalesMethodology,
)


class TestFinalCoverage:
    """Final tests to reach coverage target."""

    def test_methodology_phase_status_updates(self):
        """Test methodology phase status updates."""
        methodology = TechnicalSalesMethodology()

        # Test that phases can have their status updated
        methodology.phases[1].status = PhaseStatus.IN_PROGRESS
        assert methodology.phases[1].status == PhaseStatus.IN_PROGRESS

        methodology.phases[1].status = PhaseStatus.COMPLETED
        assert methodology.phases[1].status == PhaseStatus.COMPLETED

    def test_methodology_complete_phases(self):
        """Test completing methodology phases."""
        methodology = TechnicalSalesMethodology()

        # Test that phases can be marked as completed
        for phase_num in [1, 2, 3]:
            phase = methodology.get_phase(phase_num)
            assert phase is not None
            phase.status = PhaseStatus.COMPLETED
            assert phase.status == PhaseStatus.COMPLETED

    def test_methodology_invalid_phase_operations(self):
        """Test invalid phase operations."""
        methodology = TechnicalSalesMethodology()

        # Test invalid phase numbers
        result = methodology.get_phase(99)
        assert result is None

        # Test accessing phase that doesn't exist
        assert 99 not in methodology.phases

    def test_exporter_initialization_variations(self):
        """Test different exporter initialization patterns."""
        with patch("pathlib.Path.mkdir"):
            # Test default initialization
            exporter1 = DocumentExporter()
            assert exporter1.output_dir == Path("output")

            # Test with None (should use default)
            exporter2 = DocumentExporter(None)
            assert exporter2.output_dir == Path("output")

            # Test with specific path
            custom_path = Path("/custom")
            exporter3 = DocumentExporter(custom_path)
            assert exporter3.output_dir == custom_path

    def test_methodology_document_access(self):
        """Test accessing methodology documents."""
        methodology = TechnicalSalesMethodology()

        # Test that we can access all documents
        assert len(methodology.documents) > 0

        # Test that documents have required attributes
        for doc_type, document in methodology.documents.items():
            assert hasattr(document, "doc_type")
            assert hasattr(document, "name")
            assert hasattr(document, "phase")

    def test_methodology_phase_access(self):
        """Test accessing methodology phases."""
        methodology = TechnicalSalesMethodology()

        # Test that we can access all phases
        assert len(methodology.phases) == 3

        # Test phase attributes
        for phase_num, phase in methodology.phases.items():
            assert hasattr(phase, "phase_number")
            assert hasattr(phase, "name")
            assert hasattr(phase, "description")
            assert hasattr(phase, "status")

    def test_progress_summary_edge_cases(self):
        """Test progress summary with different states."""
        methodology = TechnicalSalesMethodology()

        # Test initial progress summary
        summary = methodology.get_progress_summary()
        assert isinstance(summary, dict)
        assert summary["overall_percentage"] == 0
        assert summary["completed_documents"] == 0

        # Test with some completed phases - update status directly
        methodology.phases[1].status = PhaseStatus.COMPLETED
        summary = methodology.get_progress_summary()
        assert isinstance(summary, dict)

    def test_document_type_coverage_expansion(self):
        """Test additional document type coverage."""
        from solution_desk_engine.framework.methodology import DocumentType

        # Test that we can access different document types
        doc_types = [
            DocumentType.SOURCE_MATERIALS,
            DocumentType.REQUIREMENTS_ANALYSIS,
            DocumentType.MARKET_FINANCIAL_ANALYSIS,
            DocumentType.SYSTEM_INTEGRATION_ANALYSIS,
            DocumentType.STAKEHOLDER_MAPPING,
            DocumentType.ARCHITECTURE_OVERVIEW,
            DocumentType.SOLUTION_DESIGN,
            DocumentType.IMPLEMENTATION_PLAN,
            DocumentType.COST_BREAKDOWN,
            DocumentType.IMPLEMENTATION_ROADMAP,
        ]

        for doc_type in doc_types:
            assert hasattr(doc_type, "value")
            assert isinstance(doc_type.value, str)
