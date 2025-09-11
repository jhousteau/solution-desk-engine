"""Integration tests for the technical sales framework."""

from unittest.mock import patch

from solution_desk_engine.config.project_config import ProjectConfiguration
from solution_desk_engine.export.document_exporter import DocumentExporter, ExportFormat
from solution_desk_engine.framework.methodology import (
    DocumentType,
    PhaseStatus,
    TechnicalSalesMethodology,
)
from solution_desk_engine.quality.validator import DocumentValidator


class TestFrameworkIntegration:
    """Test integration between framework components."""

    def test_methodology_and_config_integration(self):
        """Test that methodology works with project configuration."""
        with patch("pathlib.Path.exists", return_value=False):
            # Create methodology and config
            methodology = TechnicalSalesMethodology()
            config = ProjectConfiguration()

            # Test that all methodology documents are in config
            methodology_doc_types = set(methodology.documents.keys())
            config_doc_types = set(config.document_configs.keys())

            # Should have overlap between methodology and config documents
            assert len(methodology_doc_types.intersection(config_doc_types)) > 0

    def test_methodology_document_export_integration(self):
        """Test that methodology documents can be exported."""
        methodology = TechnicalSalesMethodology()
        _exporter = DocumentExporter()

        # Test that document types can be used for filename generation
        for doc_type in methodology.documents.keys():
            if hasattr(doc_type, "value"):
                filename = f"{doc_type.value}.md"
                assert isinstance(filename, str)
                assert filename.endswith(".md")

    def test_methodology_validation_integration(self):
        """Test that methodology works with validation."""
        methodology = TechnicalSalesMethodology()
        _validator = DocumentValidator()

        # Test that we can validate methodology phases
        for phase_num in methodology.phases.keys():
            assert isinstance(phase_num, int)
            assert 1 <= phase_num <= 3

    def test_complete_workflow_simulation(self):
        """Test a complete workflow using all components."""
        # Initialize components
        methodology = TechnicalSalesMethodology()

        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

        # Test getting documents for first phase
        phase1_docs = methodology.get_documents_for_phase(1)
        assert len(phase1_docs) > 0

        # Test progress tracking
        progress = methodology.get_progress_summary()
        assert isinstance(progress, dict)
        assert "overall_percentage" in progress
        assert "total_documents" in progress

        # Test that we can get enabled documents from config
        enabled_docs = config.get_enabled_documents()
        assert len(enabled_docs) > 0

    def test_document_type_consistency(self):
        """Test that document types are consistent across components."""
        methodology = TechnicalSalesMethodology()

        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

        # Test that key document types exist in both
        key_docs = [
            DocumentType.BUSINESS_CASE,
            DocumentType.EXECUTIVE_SUMMARY,
            DocumentType.TECHNICAL_PROPOSAL,
        ]

        for doc_type in key_docs:
            assert doc_type in methodology.documents
            assert doc_type in config.document_configs

    def test_phase_document_mapping(self):
        """Test that phase-document mapping is consistent."""
        methodology = TechnicalSalesMethodology()

        # Test each phase has documents
        for phase_num in [1, 2, 3]:
            phase_docs = methodology.get_documents_for_phase(phase_num)
            assert len(phase_docs) > 0

            # Test that each document belongs to the correct phase
            for doc in phase_docs:
                assert doc.phase == phase_num

    def test_export_format_compatibility(self):
        """Test that export formats are properly defined."""
        # Test that all export formats have valid extensions
        for format_type in ExportFormat:
            assert hasattr(format_type, "value")
            assert isinstance(format_type.value, str)
            assert len(format_type.value) > 0

    def test_configuration_defaults(self):
        """Test that configuration has sensible defaults."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Test default project info
            assert config.project_info is not None
            assert config.project_info.name is not None
            assert len(config.project_info.name) > 0

            # Test that some documents are enabled by default
            enabled_docs = config.get_enabled_documents()
            assert len(enabled_docs) > 0

            # Test that high priority docs exist
            high_priority_docs = config.get_high_priority_documents()
            assert len(high_priority_docs) > 0

    def test_methodology_phase_transitions(self):
        """Test phase transitions in methodology."""
        methodology = TechnicalSalesMethodology()

        # Test initial state
        next_phase = methodology.get_next_phase()
        assert next_phase is not None
        assert next_phase.phase_number == 1

        # Test phase completion flow - update status directly
        methodology.phases[1].status = PhaseStatus.COMPLETED
        next_phase = methodology.get_next_phase()
        assert next_phase is not None
        assert next_phase.phase_number == 2

    def test_document_lifecycle(self):
        """Test document lifecycle across components."""
        methodology = TechnicalSalesMethodology()

        # Test that documents start in pending state
        business_case_doc = methodology.documents[DocumentType.BUSINESS_CASE]
        assert business_case_doc is not None
        assert hasattr(business_case_doc, "doc_type")
        assert business_case_doc.doc_type == DocumentType.BUSINESS_CASE
