"""Progress tracking for technical sales solutioning methodology."""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console  # type: ignore
from rich.table import Table  # type: ignore

from .methodology import DocumentType, PhaseStatus, TechnicalSalesMethodology

console = Console()


@dataclass
class DocumentProgress:
    """Progress tracking for a single document."""

    doc_type: DocumentType
    status: PhaseStatus = PhaseStatus.PENDING
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    word_count: int = 0
    quality_score: float = 0.0
    last_updated: Optional[datetime] = None
    notes: str = ""


@dataclass
class PhaseProgress:
    """Progress tracking for a methodology phase."""

    phase_number: int
    name: str
    documents: Dict[DocumentType, DocumentProgress]
    status: PhaseStatus = PhaseStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not hasattr(self, "documents"):
            self.documents = {}


@dataclass
class ProjectProgress:
    """Overall project progress tracking."""

    project_name: str
    started_at: datetime
    phases: Dict[int, PhaseProgress]
    current_phase: int = 1
    overall_status: PhaseStatus = PhaseStatus.PENDING
    completion_percentage: float = 0.0

    def __post_init__(self) -> None:
        if not hasattr(self, "phases"):
            self.phases = {}


class ProgressTracker:
    """Tracks progress through the technical sales methodology."""

    def __init__(self, project_name: str, progress_file: Optional[Path] = None):
        """Initialize progress tracker.

        Args:
            project_name: Name of the project being tracked
            progress_file: Path to progress tracking JSON file
        """
        self.project_name = project_name
        self.progress_file = progress_file or Path("project_progress.json")
        self.methodology = TechnicalSalesMethodology()
        self.project_progress: Optional[ProjectProgress] = None

        # Load existing progress or initialize new
        if self.progress_file.exists():
            self.load_progress()
        else:
            self.initialize_progress()

    def initialize_progress(self) -> None:
        """Initialize progress tracking for a new project."""
        self.project_progress = ProjectProgress(
            project_name=self.project_name, started_at=datetime.now(), phases={}
        )

        # Initialize phases
        for phase_num, phase in self.methodology.phases.items():
            phase_progress = PhaseProgress(
                phase_number=phase_num, name=phase.name, documents={}
            )

            # Initialize documents for this phase
            for document in phase.documents:
                doc_progress = DocumentProgress(doc_type=document.doc_type)
                phase_progress.documents[document.doc_type] = doc_progress

            self.project_progress.phases[phase_num] = phase_progress

        self.save_progress()

    def load_progress(self) -> None:
        """Load progress from JSON file."""
        try:
            with open(self.progress_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Parse dates and enums
            started_at = datetime.fromisoformat(data["started_at"])
            overall_status = PhaseStatus(data.get("overall_status", "pending"))

            # Initialize project progress
            self.project_progress = ProjectProgress(
                project_name=data["project_name"],
                started_at=started_at,
                phases={},
                current_phase=data.get("current_phase", 1),
                overall_status=overall_status,
                completion_percentage=data.get("completion_percentage", 0.0),
            )

            # Load phases
            for phase_num, phase_data in data.get("phases", {}).items():
                phase_progress = PhaseProgress(
                    phase_number=int(phase_num),
                    name=phase_data["name"],
                    documents={},
                    status=PhaseStatus(phase_data.get("status", "pending")),
                    started_at=(
                        datetime.fromisoformat(phase_data["started_at"])
                        if phase_data.get("started_at")
                        else None
                    ),
                    completed_at=(
                        datetime.fromisoformat(phase_data["completed_at"])
                        if phase_data.get("completed_at")
                        else None
                    ),
                )

                # Load documents
                for doc_type_str, doc_data in phase_data.get("documents", {}).items():
                    doc_type = DocumentType(doc_type_str)
                    doc_progress = DocumentProgress(
                        doc_type=doc_type,
                        status=PhaseStatus(doc_data.get("status", "pending")),
                        created_at=(
                            datetime.fromisoformat(doc_data["created_at"])
                            if doc_data.get("created_at")
                            else None
                        ),
                        completed_at=(
                            datetime.fromisoformat(doc_data["completed_at"])
                            if doc_data.get("completed_at")
                            else None
                        ),
                        word_count=doc_data.get("word_count", 0),
                        quality_score=doc_data.get("quality_score", 0.0),
                        last_updated=(
                            datetime.fromisoformat(doc_data["last_updated"])
                            if doc_data.get("last_updated")
                            else None
                        ),
                        notes=doc_data.get("notes", ""),
                    )
                    phase_progress.documents[doc_type] = doc_progress

                self.project_progress.phases[int(phase_num)] = phase_progress

        except Exception as e:
            console.print(
                f"Warning: Failed to load progress from {self.progress_file}: {e}"
            )
            self.initialize_progress()

    def save_progress(self) -> None:
        """Save current progress to JSON file."""
        if not self.project_progress:
            return

        # Convert to serializable format
        data: Dict[str, Any] = {
            "project_name": self.project_progress.project_name,
            "started_at": self.project_progress.started_at.isoformat(),
            "current_phase": self.project_progress.current_phase,
            "overall_status": self.project_progress.overall_status.value,
            "completion_percentage": self.project_progress.completion_percentage,
            "phases": {},
        }

        for phase_num, phase_progress in self.project_progress.phases.items():
            phase_data: Dict[str, Any] = {
                "name": phase_progress.name,
                "status": phase_progress.status.value,
                "started_at": (
                    phase_progress.started_at.isoformat()
                    if phase_progress.started_at
                    else None
                ),
                "completed_at": (
                    phase_progress.completed_at.isoformat()
                    if phase_progress.completed_at
                    else None
                ),
                "documents": {},
            }

            for doc_type, doc_progress in phase_progress.documents.items():
                doc_data: Dict[str, Any] = {
                    "status": doc_progress.status.value,
                    "created_at": (
                        doc_progress.created_at.isoformat()
                        if doc_progress.created_at
                        else None
                    ),
                    "completed_at": (
                        doc_progress.completed_at.isoformat()
                        if doc_progress.completed_at
                        else None
                    ),
                    "word_count": doc_progress.word_count,
                    "quality_score": doc_progress.quality_score,
                    "last_updated": (
                        doc_progress.last_updated.isoformat()
                        if doc_progress.last_updated
                        else None
                    ),
                    "notes": doc_progress.notes,
                }
                phase_data["documents"][doc_type.value] = doc_data

            data["phases"][str(phase_num)] = phase_data

        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def start_document(self, doc_type: DocumentType) -> bool:
        """Mark a document as started.

        Args:
            doc_type: Type of document being started

        Returns:
            True if successfully started, False otherwise
        """
        if not self.project_progress:
            return False

        # Find which phase this document belongs to
        phase_num = None
        for phase in self.methodology.phases.values():
            if any(doc.doc_type == doc_type for doc in phase.documents):
                phase_num = phase.phase_number
                break

        if phase_num is None:
            console.print(f"Warning: Unknown document type {doc_type}")
            return False

        # Update document progress
        phase_progress = self.project_progress.phases[phase_num]
        if doc_type in phase_progress.documents:
            doc_progress = phase_progress.documents[doc_type]
            doc_progress.status = PhaseStatus.IN_PROGRESS
            doc_progress.created_at = datetime.now()
            doc_progress.last_updated = datetime.now()

            # Start phase if this is first document
            if phase_progress.status == PhaseStatus.PENDING:
                phase_progress.status = PhaseStatus.IN_PROGRESS
                phase_progress.started_at = datetime.now()

            self.save_progress()
            console.print(f"Started working on {doc_type.value}")
            return True

        return False

    def complete_document(
        self,
        doc_type: DocumentType,
        word_count: int = 0,
        quality_score: float = 0.0,
        notes: str = "",
    ) -> bool:
        """Mark a document as completed.

        Args:
            doc_type: Type of document completed
            word_count: Word count of the completed document
            quality_score: Quality score from validation (0-100)
            notes: Additional notes about the document

        Returns:
            True if successfully completed, False otherwise
        """
        if not self.project_progress:
            return False

        # Find which phase this document belongs to
        phase_num = None
        for phase in self.methodology.phases.values():
            if any(doc.doc_type == doc_type for doc in phase.documents):
                phase_num = phase.phase_number
                break

        if phase_num is None:
            return False

        # Update document progress
        phase_progress = self.project_progress.phases[phase_num]
        if doc_type in phase_progress.documents:
            doc_progress = phase_progress.documents[doc_type]
            doc_progress.status = PhaseStatus.COMPLETED
            doc_progress.completed_at = datetime.now()
            doc_progress.last_updated = datetime.now()
            doc_progress.word_count = word_count
            doc_progress.quality_score = quality_score
            doc_progress.notes = notes

            # Check if phase is complete
            all_completed = all(
                doc.status == PhaseStatus.COMPLETED
                for doc in phase_progress.documents.values()
            )

            if all_completed:
                phase_progress.status = PhaseStatus.COMPLETED
                phase_progress.completed_at = datetime.now()
                console.print(f"Phase {phase_num} ({phase_progress.name}) completed!")

                # Update current phase
                next_phase = phase_num + 1
                if next_phase <= 3:
                    self.project_progress.current_phase = next_phase
                else:
                    self.project_progress.overall_status = PhaseStatus.COMPLETED
                    console.print("🎉 Project methodology completed!")

            # Update overall completion percentage
            self._update_completion_percentage()

            self.save_progress()
            console.print(f"Completed {doc_type.value}")
            return True

        return False

    def _update_completion_percentage(self) -> None:
        """Update overall completion percentage."""
        if not self.project_progress:
            return

        total_docs = 0
        completed_docs = 0

        for phase_progress in self.project_progress.phases.values():
            total_docs += len(phase_progress.documents)
            completed_docs += sum(
                1
                for doc in phase_progress.documents.values()
                if doc.status == PhaseStatus.COMPLETED
            )

        if total_docs > 0:
            self.project_progress.completion_percentage = (
                completed_docs / total_docs
            ) * 100

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get comprehensive progress summary."""
        if not self.project_progress:
            return {}

        summary: Dict[str, Any] = {
            "project_name": self.project_progress.project_name,
            "started_at": self.project_progress.started_at.isoformat(),
            "current_phase": self.project_progress.current_phase,
            "overall_status": self.project_progress.overall_status.value,
            "completion_percentage": round(
                self.project_progress.completion_percentage, 1
            ),
            "phases": {},
            "next_actions": self._get_next_actions(),
        }

        for phase_num, phase_progress in self.project_progress.phases.items():
            completed_docs = sum(
                1
                for doc in phase_progress.documents.values()
                if doc.status == PhaseStatus.COMPLETED
            )
            total_docs = len(phase_progress.documents)

            summary["phases"][phase_num] = {
                "name": phase_progress.name,
                "status": phase_progress.status.value,
                "started_at": (
                    phase_progress.started_at.isoformat()
                    if phase_progress.started_at
                    else None
                ),
                "completed_at": (
                    phase_progress.completed_at.isoformat()
                    if phase_progress.completed_at
                    else None
                ),
                "completed_documents": completed_docs,
                "total_documents": total_docs,
                "percentage": (completed_docs / total_docs * 100) if total_docs else 0,
            }

        return summary

    def _get_next_actions(self) -> List[str]:
        """Get list of recommended next actions."""
        if not self.project_progress:
            return []

        actions = []

        # Find next pending documents in current phase
        current_phase = self.project_progress.phases.get(
            self.project_progress.current_phase
        )
        if current_phase:
            pending_docs = [
                doc_type.value
                for doc_type, doc in current_phase.documents.items()
                if doc.status == PhaseStatus.PENDING
            ]

            if pending_docs:
                actions.extend([f"Start working on {doc}" for doc in pending_docs[:3]])

            # Check for in-progress documents
            in_progress = [
                doc_type.value
                for doc_type, doc in current_phase.documents.items()
                if doc.status == PhaseStatus.IN_PROGRESS
            ]

            if in_progress:
                actions.extend([f"Complete {doc}" for doc in in_progress])

        return actions[:5]  # Limit to top 5 actions

    def display_progress(self) -> None:
        """Display progress in a formatted table."""
        if not self.project_progress:
            console.print("No progress data available")
            return

        table = Table(title=f"Progress: {self.project_progress.project_name}")
        table.add_column("Phase", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Documents", justify="right")
        table.add_column("Progress", justify="right")

        for phase_num in [1, 2, 3]:
            if phase_num in self.project_progress.phases:
                phase = self.project_progress.phases[phase_num]
                completed = sum(
                    1
                    for doc in phase.documents.values()
                    if doc.status == PhaseStatus.COMPLETED
                )
                total = len(phase.documents)
                percentage = (completed / total * 100) if total else 0

                status_emoji = {
                    PhaseStatus.PENDING: "⏸️",
                    PhaseStatus.IN_PROGRESS: "🔄",
                    PhaseStatus.COMPLETED: "✅",
                }

                table.add_row(
                    f"{phase_num}. {phase.name}",
                    f"{status_emoji[phase.status]} {phase.status.value}",
                    f"{completed}/{total}",
                    f"{percentage:.0f}%",
                )

        console.print(table)

        # Show next actions
        next_actions = self._get_next_actions()
        if next_actions:
            console.print("\n📋 Next Actions:")
            for i, action in enumerate(next_actions, 1):
                console.print(f"  {i}. {action}")

        # Show overall progress
        console.print(
            f"\n🎯 Overall Progress: {self.project_progress.completion_percentage:.1f}% Complete"
        )

    def get_document_status(self, doc_type: DocumentType) -> Optional[DocumentProgress]:
        """Get status of a specific document."""
        if not self.project_progress:
            return None

        for phase_progress in self.project_progress.phases.values():
            if doc_type in phase_progress.documents:
                return phase_progress.documents[doc_type]

        return None
