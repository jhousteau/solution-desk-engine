"""Simple progress tracker tests for coverage."""

from datetime import datetime

from solution_desk_engine.framework.methodology import DocumentType, PhaseStatus
from solution_desk_engine.framework.progress_tracker import (
    DocumentProgress,
    PhaseProgress,
    ProjectProgress,
)


class TestProgressSimple:
    """Simple progress tracker tests."""

    def test_document_progress_defaults(self):
        """Test DocumentProgress with default values."""
        doc_progress = DocumentProgress(DocumentType.BUSINESS_CASE)

        assert doc_progress.doc_type == DocumentType.BUSINESS_CASE
        assert doc_progress.status == PhaseStatus.PENDING
        assert doc_progress.created_at is None
        assert doc_progress.completed_at is None
        assert doc_progress.last_updated is None
        assert doc_progress.notes == ""

    def test_phase_progress_post_init(self):
        """Test PhaseProgress __post_init__ method."""
        # Test with documents provided
        phase_progress = PhaseProgress(1, "Test", {})
        assert phase_progress.documents == {}

        # Test post_init creates documents dict
        phase_progress = PhaseProgress(1, "Test", {})
        assert hasattr(phase_progress, "documents")

    def test_project_progress_post_init(self):
        """Test ProjectProgress __post_init__ method."""
        now = datetime.now()
        project_progress = ProjectProgress("Test", now, {})
        assert hasattr(project_progress, "phases")
        assert project_progress.phases == {}

    def test_project_progress_defaults(self):
        """Test ProjectProgress default values."""
        now = datetime.now()
        project_progress = ProjectProgress("Test Project", now, {})

        assert project_progress.project_name == "Test Project"
        assert project_progress.started_at == now
        assert project_progress.current_phase == 1
        assert project_progress.overall_status == PhaseStatus.PENDING
        assert project_progress.completion_percentage == 0.0

    def test_document_progress_with_all_fields(self):
        """Test DocumentProgress with all fields."""
        now = datetime.now()
        doc_progress = DocumentProgress(
            doc_type=DocumentType.BUSINESS_CASE,
            status=PhaseStatus.COMPLETED,
            created_at=now,
            completed_at=now,
            last_updated=now,
            notes="Test notes",
        )

        assert doc_progress.status == PhaseStatus.COMPLETED
        assert doc_progress.created_at == now
        assert doc_progress.completed_at == now
        assert doc_progress.last_updated == now
        assert doc_progress.notes == "Test notes"

    def test_phase_progress_with_all_fields(self):
        """Test PhaseProgress with all fields."""
        now = datetime.now()
        doc_dict = {
            DocumentType.BUSINESS_CASE: DocumentProgress(DocumentType.BUSINESS_CASE)
        }

        phase_progress = PhaseProgress(
            phase_number=2,
            name="Design Phase",
            documents=doc_dict,
            status=PhaseStatus.IN_PROGRESS,
            started_at=now,
            completed_at=None,
        )

        assert phase_progress.phase_number == 2
        assert phase_progress.name == "Design Phase"
        assert phase_progress.status == PhaseStatus.IN_PROGRESS
        assert phase_progress.started_at == now
        assert phase_progress.completed_at is None
        assert len(phase_progress.documents) == 1

    def test_project_progress_with_all_fields(self):
        """Test ProjectProgress with all fields."""
        now = datetime.now()
        phases_dict = {1: PhaseProgress(1, "Phase 1", {})}

        project_progress = ProjectProgress(
            project_name="Full Test Project",
            started_at=now,
            phases=phases_dict,
            current_phase=2,
            overall_status=PhaseStatus.IN_PROGRESS,
            completion_percentage=45.5,
        )

        assert project_progress.project_name == "Full Test Project"
        assert project_progress.current_phase == 2
        assert project_progress.overall_status == PhaseStatus.IN_PROGRESS
        assert project_progress.completion_percentage == 45.5
        assert len(project_progress.phases) == 1
