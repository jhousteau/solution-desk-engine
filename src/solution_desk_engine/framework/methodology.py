"""Three-phase methodology framework for technical sales solutioning."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class PhaseStatus(Enum):
    """Status of a methodology phase."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class DocumentType(Enum):
    """Types of documents in the framework."""

    # Phase 1: Analyze
    SOURCE_MATERIALS = "source_materials"
    REQUIREMENTS_ANALYSIS = "requirements_analysis"
    MARKET_FINANCIAL_ANALYSIS = "market_financial_analysis"
    SYSTEM_INTEGRATION_ANALYSIS = "system_integration_analysis"
    STAKEHOLDER_MAPPING = "stakeholder_mapping"

    # Phase 2: Design
    BUSINESS_CASE = "business_case"
    ARCHITECTURE_OVERVIEW = "architecture_overview"
    GCP_CONSUMPTION_ANALYSIS = "gcp_consumption_analysis"
    SOLUTION_DESIGN = "solution_design"
    IMPLEMENTATION_PLAN = "implementation_plan"

    # Phase 3: Package
    EXECUTIVE_SUMMARY = "executive_summary"
    TECHNICAL_PROPOSAL = "technical_proposal"
    COST_BREAKDOWN = "cost_breakdown"
    IMPLEMENTATION_ROADMAP = "implementation_roadmap"


@dataclass
class Document:
    """Represents a document in the methodology."""

    doc_type: DocumentType
    name: str
    description: str
    phase: int
    required: bool = True
    status: PhaseStatus = PhaseStatus.PENDING
    template_path: Optional[str] = None


@dataclass
class Phase:
    """Represents a methodology phase."""

    phase_number: int
    name: str
    description: str
    documents: List[Document]
    status: PhaseStatus = PhaseStatus.PENDING

    def __post_init__(self) -> None:
        if not hasattr(self, "documents"):
            self.documents = []


class TechnicalSalesMethodology:
    """Three-phase technical sales solutioning methodology.

    Simplified from the original 11-phase framework to focus on:
    Phase 1: Analyze - Research, requirements, and stakeholder analysis
    Phase 2: Design - Architecture, business case, and solution design
    Phase 3: Package - Proposal creation and presentation materials
    """

    def __init__(self) -> None:
        self.phases = self._initialize_phases()
        self.documents = self._initialize_documents()

    def _initialize_phases(self) -> Dict[int, Phase]:
        """Initialize the three methodology phases."""
        return {
            1: Phase(
                phase_number=1,
                name="Analyze",
                description="Research, discovery, and requirements analysis",
                documents=[],
            ),
            2: Phase(
                phase_number=2,
                name="Design",
                description="Architecture design, business case, and solution specification",
                documents=[],
            ),
            3: Phase(
                phase_number=3,
                name="Package",
                description="Proposal creation and client presentation materials",
                documents=[],
            ),
        }

    def _initialize_documents(self) -> Dict[DocumentType, Document]:
        """Initialize document templates."""
        documents = {
            # Phase 1: Analyze
            DocumentType.SOURCE_MATERIALS: Document(
                doc_type=DocumentType.SOURCE_MATERIALS,
                name="Source Materials Collection",
                description="Original client materials, emails, and requirements",
                phase=1,
                template_path="templates/source_materials.md",
            ),
            DocumentType.REQUIREMENTS_ANALYSIS: Document(
                doc_type=DocumentType.REQUIREMENTS_ANALYSIS,
                name="Requirements Analysis",
                description="Functional and non-functional requirements with traceability",
                phase=1,
                template_path="templates/requirements_analysis.md",
            ),
            DocumentType.MARKET_FINANCIAL_ANALYSIS: Document(
                doc_type=DocumentType.MARKET_FINANCIAL_ANALYSIS,
                name="Market & Financial Analysis",
                description="Market sizing, financial projections, and revenue opportunity",
                phase=1,
                template_path="templates/market_financial_analysis.md",
            ),
            DocumentType.SYSTEM_INTEGRATION_ANALYSIS: Document(
                doc_type=DocumentType.SYSTEM_INTEGRATION_ANALYSIS,
                name="System Integration Analysis",
                description="Integration points, data flows, and system dependencies",
                phase=1,
                template_path="templates/system_integration_analysis.md",
            ),
            DocumentType.STAKEHOLDER_MAPPING: Document(
                doc_type=DocumentType.STAKEHOLDER_MAPPING,
                name="Stakeholder Mapping",
                description="Key stakeholders, roles, and engagement plan",
                phase=1,
                template_path="templates/stakeholder_mapping.md",
            ),
            # Phase 2: Design
            DocumentType.BUSINESS_CASE: Document(
                doc_type=DocumentType.BUSINESS_CASE,
                name="Business Case",
                description="ROI analysis and business justification",
                phase=2,
                template_path="templates/business_case.md",
            ),
            DocumentType.ARCHITECTURE_OVERVIEW: Document(
                doc_type=DocumentType.ARCHITECTURE_OVERVIEW,
                name="Architecture Overview",
                description="High-level technical architecture and design principles",
                phase=2,
                template_path="templates/architecture_overview.md",
            ),
            DocumentType.GCP_CONSUMPTION_ANALYSIS: Document(
                doc_type=DocumentType.GCP_CONSUMPTION_ANALYSIS,
                name="GCP Consumption Analysis",
                description="Detailed GCP cost modeling with optimization strategies",
                phase=2,
                template_path="templates/gcp_consumption_analysis.md",
            ),
            DocumentType.SOLUTION_DESIGN: Document(
                doc_type=DocumentType.SOLUTION_DESIGN,
                name="Solution Design",
                description="Detailed component specifications and integrations",
                phase=2,
                template_path="templates/solution_design.md",
            ),
            DocumentType.IMPLEMENTATION_PLAN: Document(
                doc_type=DocumentType.IMPLEMENTATION_PLAN,
                name="Implementation Plan",
                description="Execution roadmap and resource allocation",
                phase=2,
                template_path="templates/implementation_plan.md",
            ),
            # Phase 3: Package
            DocumentType.EXECUTIVE_SUMMARY: Document(
                doc_type=DocumentType.EXECUTIVE_SUMMARY,
                name="Executive Summary",
                description="High-level overview for executive stakeholders",
                phase=3,
                template_path="templates/executive_summary.md",
            ),
            DocumentType.TECHNICAL_PROPOSAL: Document(
                doc_type=DocumentType.TECHNICAL_PROPOSAL,
                name="Technical Proposal",
                description="Comprehensive technical proposal document",
                phase=3,
                template_path="templates/technical_proposal.md",
            ),
            DocumentType.COST_BREAKDOWN: Document(
                doc_type=DocumentType.COST_BREAKDOWN,
                name="Cost Breakdown",
                description="Detailed cost analysis and pricing breakdown",
                phase=3,
                template_path="templates/cost_breakdown.md",
            ),
            DocumentType.IMPLEMENTATION_ROADMAP: Document(
                doc_type=DocumentType.IMPLEMENTATION_ROADMAP,
                name="Implementation Roadmap",
                description="Visual timeline and milestone roadmap",
                phase=3,
                template_path="templates/implementation_roadmap.md",
            ),
        }

        # Associate documents with phases
        for doc in documents.values():
            self.phases[doc.phase].documents.append(doc)

        return documents

    def get_phase(self, phase_number: int) -> Optional[Phase]:
        """Get a specific phase by number."""
        return self.phases.get(phase_number)

    def get_documents_for_phase(self, phase_number: int) -> List[Document]:
        """Get all documents for a specific phase."""
        phase = self.get_phase(phase_number)
        return phase.documents if phase else []

    def get_document(self, doc_type: DocumentType) -> Optional[Document]:
        """Get a specific document by type."""
        return self.documents.get(doc_type)

    def get_next_phase(self) -> Optional[Phase]:
        """Get the next pending or in-progress phase."""
        for phase_num in [1, 2, 3]:
            phase = self.phases[phase_num]
            if phase.status != PhaseStatus.COMPLETED:
                return phase
        return None

    def is_phase_complete(self, phase_number: int) -> bool:
        """Check if a phase is complete."""
        phase = self.get_phase(phase_number)
        if not phase:
            return False

        # Phase is complete if all required documents are completed
        required_docs = [doc for doc in phase.documents if doc.required]
        completed_docs = [
            doc for doc in required_docs if doc.status == PhaseStatus.COMPLETED
        ]

        return len(required_docs) == len(completed_docs)

    def update_document_status(
        self, doc_type: DocumentType, status: PhaseStatus
    ) -> None:
        """Update the status of a document."""
        if doc_type in self.documents:
            self.documents[doc_type].status = status

            # Update phase status if all documents in phase are completed
            doc = self.documents[doc_type]
            if self.is_phase_complete(doc.phase):
                self.phases[doc.phase].status = PhaseStatus.COMPLETED

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get overall progress summary."""
        total_docs = len([doc for doc in self.documents.values() if doc.required])
        completed_docs = len(
            [
                doc
                for doc in self.documents.values()
                if doc.required and doc.status == PhaseStatus.COMPLETED
            ]
        )

        phase_progress = {}
        for phase_num, phase in self.phases.items():
            required_docs = [doc for doc in phase.documents if doc.required]
            completed_phase_docs = [
                doc for doc in required_docs if doc.status == PhaseStatus.COMPLETED
            ]
            phase_progress[phase_num] = {
                "name": phase.name,
                "status": phase.status.value,
                "completed_documents": len(completed_phase_docs),
                "total_documents": len(required_docs),
                "percentage": (
                    (len(completed_phase_docs) / len(required_docs) * 100)
                    if required_docs
                    else 0
                ),
            }

        next_phase = self.get_next_phase()
        return {
            "overall_percentage": (
                (completed_docs / total_docs * 100) if total_docs else 0
            ),
            "completed_documents": completed_docs,
            "total_documents": total_docs,
            "phases": phase_progress,
            "next_phase": next_phase.name if next_phase is not None else "All Complete",
        }
