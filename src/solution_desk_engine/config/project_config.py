"""Project configuration management for technical sales solutioning."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

# from ..framework.methodology import DocumentType  # TODO: Re-enable when methodology is reimplemented


@dataclass
class ProjectInfo:
    """Basic project information."""

    name: str
    description: str
    client_name: Optional[str] = None
    project_type: Optional[str] = None


@dataclass
class DocumentConfig:
    """Configuration for a specific document."""

    enabled: bool
    description: str
    template_path: Optional[str] = None
    priority: str = "normal"  # high, normal, low


class ProjectConfiguration:
    """Manages project configuration for technical sales solutioning."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize project configuration.

        Args:
            config_path: Path to configuration YAML file
        """
        self.config_path = config_path or Path("project_config.yaml")
        self.project_info: Optional[ProjectInfo] = None
        self.document_configs: Dict[
            str, DocumentConfig
        ] = {}  # TODO: Change back to DocumentType when reimplemented
        self.custom_settings: Dict[str, Any] = {}

        # Load configuration if file exists
        if self.config_path.exists():
            self.load_config()
        else:
            self._initialize_default_config()

    def _initialize_default_config(self) -> None:
        """Initialize with default MVP configuration."""
        self.project_info = ProjectInfo(
            name="Technical Sales Solution",
            description="AI-powered technical sales solutioning project",
        )

        # TODO: Re-enable when DocumentType enum is reimplemented
        self.document_configs = {}

        self.custom_settings = {
            "export_formats": ["pdf", "docx"],
            "quality_standards": {
                "require_citations": True,
                "minimum_word_count": 100,
                "require_references_section": True,
            },
            "templates": {
                "use_professional_styling": True,
                "include_branding": False,
                "generate_toc": True,
            },
        }

    def load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            # Load project info
            if "project_info" in config_data:
                self.project_info = ProjectInfo(**config_data["project_info"])

            # Load document configurations
            if "documents" in config_data:
                self._load_document_configs(config_data["documents"])

            # Load custom settings
            if "settings" in config_data:
                self.custom_settings.update(config_data["settings"])

        except Exception as e:
            print(f"Warning: Failed to load config from {self.config_path}: {e}")
            self._initialize_default_config()

    def save_config(self) -> None:
        """Save current configuration to YAML file."""
        if not self.project_info:
            return

        config_data = {
            "project_info": {
                "name": self.project_info.name,
                "description": self.project_info.description,
                "client_name": self.project_info.client_name,
                "project_type": self.project_info.project_type,
            },
            "documents": {
                doc_type.value: {
                    "enabled": config.enabled,
                    "description": config.description,
                    "template_path": config.template_path,
                    "priority": config.priority,
                }
                for doc_type, config in self.document_configs.items()
            },
            "settings": self.custom_settings,
        }

        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)

    def _load_document_configs(self, documents_config: Dict[str, Any]) -> None:
        """Load document configurations from config data."""
        # TODO: Re-enable when DocumentType enum is reimplemented
        pass

    # TODO: Re-enable when DocumentType enum is reimplemented
    # def is_document_enabled(self, doc_type: DocumentType) -> bool:
    #     """Check if a document type is enabled."""
    #     return self.document_configs.get(doc_type, DocumentConfig(False, "")).enabled

    # def get_enabled_documents(self) -> List[DocumentType]:
    #     """Get list of enabled document types."""
    #     return [
    #         doc_type
    #         for doc_type, config in self.document_configs.items()
    #         if config.enabled
    #     ]

    # def get_high_priority_documents(self) -> List[DocumentType]:
    #     """Get list of high-priority documents."""
    #     return [
    #         doc_type
    #         for doc_type, config in self.document_configs.items()
    #         if config.enabled and config.priority == "high"
    #     ]

    # def get_documents_for_phase(self, phase_number: int) -> List[DocumentType]:
    #     """Get enabled documents for a specific phase."""
    #     from ..framework.methodology import TechnicalSalesMethodology

    #     methodology = TechnicalSalesMethodology()
    #     phase_docs = methodology.get_documents_for_phase(phase_number)

    #     return [
    #         doc.doc_type for doc in phase_docs if self.is_document_enabled(doc.doc_type)
    #     ]

    # def enable_document(
    #     self, doc_type: DocumentType, description: str = "", priority: str = "normal"
    # ) -> None:
    #     """Enable a document type."""
    #     if doc_type not in self.document_configs:
    #         self.document_configs[doc_type] = DocumentConfig(
    #             enabled=True, description=description, priority=priority
    #         )
    #     else:
    #         self.document_configs[doc_type].enabled = True

    # def disable_document(self, doc_type: DocumentType) -> None:
    #     """Disable a document type."""
    #     if doc_type in self.document_configs:
    #         self.document_configs[doc_type].enabled = False

    def update_project_info(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        client_name: Optional[str] = None,
        project_type: Optional[str] = None,
    ) -> None:
        """Update project information."""
        if not self.project_info:
            self.project_info = ProjectInfo("", "")

        if name is not None:
            self.project_info.name = name
        if description is not None:
            self.project_info.description = description
        if client_name is not None:
            self.project_info.client_name = client_name
        if project_type is not None:
            self.project_info.project_type = project_type

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a custom setting value."""
        keys = key.split(".")
        value = self.custom_settings

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set_setting(self, key: str, value: Any) -> None:
        """Set a custom setting value."""
        keys = key.split(".")
        setting = self.custom_settings

        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in setting:
                setting[k] = {}
            setting = setting[k]

        # Set the final value
        setting[keys[-1]] = value

    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration."""
        enabled_docs = len(self.get_enabled_documents())
        total_docs = len(self.document_configs)
        high_priority = len(self.get_high_priority_documents())

        return {
            "project_name": self.project_info.name if self.project_info else "Unknown",
            "client_name": self.project_info.client_name if self.project_info else None,
            "total_documents": total_docs,
            "enabled_documents": enabled_docs,
            "high_priority_documents": high_priority,
            "completion_percentage": 0,  # Will be updated by progress tracker
            "phases": {
                "phase_1": len(self.get_documents_for_phase(1)),
                "phase_2": len(self.get_documents_for_phase(2)),
                "phase_3": len(self.get_documents_for_phase(3)),
            },
            "export_formats": self.get_setting("export_formats", ["pdf"]),
            "quality_checks_enabled": self.get_setting(
                "quality_standards.require_citations", True
            ),
        }
