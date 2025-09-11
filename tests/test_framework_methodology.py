"""Tests for the technical sales methodology framework."""

from solution_desk_engine.framework.methodology import (
    Document,
    DocumentType,
    Phase,
    PhaseStatus,
    TechnicalSalesMethodology,
)


class TestTechnicalSalesMethodology:
    """Test cases for TechnicalSalesMethodology class."""

    def test_initialization(self):
        """Test methodology initialization with default phases."""
        methodology = TechnicalSalesMethodology()

        assert len(methodology.phases) == 3
        assert 1 in methodology.phases
        assert 2 in methodology.phases
        assert 3 in methodology.phases

        # Test phase names
        assert methodology.phases[1].name == "Analyze"
        assert methodology.phases[2].name == "Design"
        assert methodology.phases[3].name == "Package"

    def test_phase_creation(self):
        """Test individual phase creation and properties."""
        methodology = TechnicalSalesMethodology()
        phase = methodology.phases[1]

        assert isinstance(phase, Phase)
        assert phase.phase_number == 1
        assert phase.name == "Analyze"
        assert phase.description == "Research, discovery, and requirements analysis"
        assert phase.status == PhaseStatus.PENDING
        assert isinstance(phase.documents, list)

    def test_document_initialization(self):
        """Test document template initialization."""
        methodology = TechnicalSalesMethodology()

        # Check that documents are properly initialized
        assert len(methodology.documents) == 14

        # Test specific document types exist
        expected_docs = [
            DocumentType.SOURCE_MATERIALS,
            DocumentType.REQUIREMENTS_ANALYSIS,
            DocumentType.BUSINESS_CASE,
            DocumentType.GCP_CONSUMPTION_ANALYSIS,
            DocumentType.EXECUTIVE_SUMMARY,
            DocumentType.TECHNICAL_PROPOSAL,
        ]

        for doc_type in expected_docs:
            assert doc_type in methodology.documents

    def test_get_phase(self):
        """Test getting specific phases."""
        methodology = TechnicalSalesMethodology()

        phase1 = methodology.get_phase(1)
        assert phase1.name == "Analyze"

        phase2 = methodology.get_phase(2)
        assert phase2.name == "Design"

        phase3 = methodology.get_phase(3)
        assert phase3.name == "Package"

        # Test invalid phase number
        invalid_phase = methodology.get_phase(99)
        assert invalid_phase is None

    def test_get_documents_for_phase(self):
        """Test getting documents for specific phases."""
        methodology = TechnicalSalesMethodology()

        # Test phase 1 documents
        phase1_docs = methodology.get_documents_for_phase(1)
        assert len(phase1_docs) > 0

        # Verify all returned documents are Document instances
        for doc in phase1_docs:
            assert isinstance(doc, Document)

        # Test phase 2 documents
        phase2_docs = methodology.get_documents_for_phase(2)
        assert len(phase2_docs) > 0

        # Test phase 3 documents
        phase3_docs = methodology.get_documents_for_phase(3)
        assert len(phase3_docs) > 0

        # Test invalid phase
        invalid_docs = methodology.get_documents_for_phase(99)
        assert invalid_docs == []

    def test_get_next_phase(self):
        """Test getting the next incomplete phase."""
        methodology = TechnicalSalesMethodology()

        # Initially, all phases are pending, so next should be phase 1
        next_phase = methodology.get_next_phase()
        assert next_phase.phase_number == 1

        # Complete phase 1
        methodology.phases[1].status = PhaseStatus.COMPLETED
        next_phase = methodology.get_next_phase()
        assert next_phase.phase_number == 2

        # Complete phase 2
        methodology.phases[2].status = PhaseStatus.COMPLETED
        next_phase = methodology.get_next_phase()
        assert next_phase.phase_number == 3

        # Complete all phases
        methodology.phases[3].status = PhaseStatus.COMPLETED
        next_phase = methodology.get_next_phase()
        assert next_phase is None

    def test_get_progress_summary(self):
        """Test getting progress summary."""
        methodology = TechnicalSalesMethodology()

        summary = methodology.get_progress_summary()

        assert isinstance(summary, dict)
        assert "overall_percentage" in summary
        assert "completed_documents" in summary
        assert "total_documents" in summary
        assert "phases" in summary
        assert "next_phase" in summary

        # Initially, no documents completed
        assert summary["completed_documents"] == 0
        assert summary["total_documents"] > 0
        assert summary["overall_percentage"] == 0

        # Test with some completed phases
        methodology.phases[1].status = PhaseStatus.COMPLETED
        summary = methodology.get_progress_summary()
        assert isinstance(summary["phases"], dict)


class TestPhase:
    """Test cases for Phase class."""

    def test_phase_creation(self):
        """Test creating a phase with proper attributes."""
        documents = []
        phase = Phase(
            phase_number=1,
            name="Test Phase",
            description="Test description",
            documents=documents,
        )

        assert phase.phase_number == 1
        assert phase.name == "Test Phase"
        assert phase.description == "Test description"
        assert phase.status == PhaseStatus.PENDING
        assert phase.documents == documents


class TestDocument:
    """Test cases for Document class."""

    def test_document_creation(self):
        """Test creating a document with proper attributes."""
        doc = Document(
            doc_type=DocumentType.BUSINESS_CASE,
            name="Test Business Case",
            description="Test description",
            phase=2,
        )

        assert doc.doc_type == DocumentType.BUSINESS_CASE
        assert doc.name == "Test Business Case"
        assert doc.description == "Test description"
        assert doc.phase == 2
        assert doc.status == PhaseStatus.PENDING

    def test_document_optional_fields(self):
        """Test document creation with optional fields."""
        doc = Document(
            doc_type=DocumentType.BUSINESS_CASE,
            name="Test Business Case",
            description="Test description",
            phase=2,
            template_path="/path/to/template.md",
        )

        assert doc.template_path == "/path/to/template.md"


class TestDocumentType:
    """Test cases for DocumentType enum."""

    def test_document_type_values(self):
        """Test that all expected document types exist."""
        expected_types = [
            "source_materials",
            "requirements_analysis",
            "market_financial_analysis",
            "system_integration_analysis",
            "stakeholder_mapping",
            "business_case",
            "architecture_overview",
            "gcp_consumption_analysis",
            "solution_design",
            "implementation_plan",
            "executive_summary",
            "technical_proposal",
            "cost_breakdown",
            "implementation_roadmap",
        ]

        for expected in expected_types:
            # Test that we can create enum from string value
            doc_type = DocumentType(expected)
            assert doc_type.value == expected


class TestPhaseStatus:
    """Test cases for PhaseStatus enum."""

    def test_phase_status_values(self):
        """Test that all expected phase statuses exist."""
        assert PhaseStatus.PENDING.value == "pending"
        assert PhaseStatus.IN_PROGRESS.value == "in_progress"
        assert PhaseStatus.COMPLETED.value == "completed"
