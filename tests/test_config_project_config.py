"""Tests for the project configuration management functionality."""

from pathlib import Path
from unittest.mock import mock_open, patch

import yaml

from solution_desk_engine.config.project_config import (
    DocumentConfig,
    ProjectConfiguration,
    ProjectInfo,
)
from solution_desk_engine.framework.methodology import DocumentType


class TestProjectInfo:
    """Test cases for ProjectInfo class."""

    def test_project_info_creation(self):
        """Test creating ProjectInfo with required fields."""
        project_info = ProjectInfo(
            name="Test Project", description="A test project for validation"
        )

        assert project_info.name == "Test Project"
        assert project_info.description == "A test project for validation"
        assert project_info.client_name is None
        assert project_info.project_type is None

    def test_project_info_with_optional_fields(self):
        """Test ProjectInfo with all optional fields."""
        project_info = ProjectInfo(
            name="Test Project",
            description="A test project",
            client_name="Acme Corp",
            project_type="Technical Sales",
        )

        assert project_info.client_name == "Acme Corp"
        assert project_info.project_type == "Technical Sales"


class TestDocumentConfig:
    """Test cases for DocumentConfig class."""

    def test_document_config_creation(self):
        """Test creating DocumentConfig with required fields."""
        doc_config = DocumentConfig(
            enabled=True, description="Test document configuration"
        )

        assert doc_config.enabled is True
        assert doc_config.description == "Test document configuration"
        assert doc_config.template_path is None
        assert doc_config.priority == "normal"

    def test_document_config_with_optional_fields(self):
        """Test DocumentConfig with all optional fields."""
        doc_config = DocumentConfig(
            enabled=True,
            description="Test document",
            template_path="/path/to/template.md",
            priority="high",
        )

        assert doc_config.template_path == "/path/to/template.md"
        assert doc_config.priority == "high"


class TestProjectConfiguration:
    """Test cases for ProjectConfiguration class."""

    def test_project_configuration_initialization_no_file(self):
        """Test ProjectConfiguration initialization when config file doesn't exist."""
        config_path = Path("nonexistent_config.yaml")

        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration(config_path)

            assert config.config_path == config_path
            assert config.project_info is not None
            assert config.project_info.name == "Technical Sales Solution"
            assert len(config.document_configs) == 14  # MVP has 14 document types
            assert isinstance(config.custom_settings, dict)

    def test_project_configuration_default_documents(self):
        """Test that default MVP documents are properly configured."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Check that key document types are enabled
            essential_docs = [
                DocumentType.SOURCE_MATERIALS,
                DocumentType.REQUIREMENTS_ANALYSIS,
                DocumentType.BUSINESS_CASE,
                DocumentType.GCP_CONSUMPTION_ANALYSIS,
                DocumentType.EXECUTIVE_SUMMARY,
                DocumentType.TECHNICAL_PROPOSAL,
            ]

            for doc_type in essential_docs:
                assert doc_type in config.document_configs
                assert config.document_configs[doc_type].enabled is True

    def test_project_configuration_load_existing_file(self):
        """Test ProjectConfiguration loading from existing YAML file."""
        mock_config_data = {
            "project_info": {
                "name": "Loaded Project",
                "description": "Loaded from file",
                "client_name": "Test Client",
            },
            "documents": {
                "business_case": {
                    "enabled": True,
                    "description": "Business case document",
                    "priority": "high",
                }
            },
            "settings": {
                "export_formats": ["pdf", "html"],
                "quality_standards": {"require_citations": False},
            },
        }

        mock_yaml_content = yaml.dump(mock_config_data)

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=mock_yaml_content)),
        ):
            config = ProjectConfiguration(Path("test_config.yaml"))

            assert config.project_info.name == "Loaded Project"
            assert config.project_info.client_name == "Test Client"
            assert DocumentType.BUSINESS_CASE in config.document_configs
            assert config.custom_settings["export_formats"] == ["pdf", "html"]

    def test_save_config(self):
        """Test saving configuration to YAML file."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            with (
                patch("builtins.open", mock_open()) as mock_file,
                patch("yaml.dump") as mock_yaml_dump,
            ):
                config.save_config()

                # Verify file was opened for writing
                mock_file.assert_called_once()
                # Verify yaml.dump was called
                mock_yaml_dump.assert_called_once()

    def test_save_config_no_project_info(self):
        """Test saving configuration when project_info is None."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()
            config.project_info = None

            with patch("builtins.open", mock_open()) as mock_file:
                config.save_config()

                # Should return early and not try to write
                mock_file.assert_not_called()

    def test_is_document_enabled(self):
        """Test checking if document is enabled."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Test enabled document
            assert config.is_document_enabled(DocumentType.BUSINESS_CASE) is True

            # Test disabled document (modify config)
            config.document_configs[DocumentType.BUSINESS_CASE].enabled = False
            assert config.is_document_enabled(DocumentType.BUSINESS_CASE) is False

            # Test non-existent document type
            config.document_configs.clear()
            assert config.is_document_enabled(DocumentType.BUSINESS_CASE) is False

    def test_get_enabled_documents(self):
        """Test getting list of enabled documents."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            enabled_docs = config.get_enabled_documents()

            assert isinstance(enabled_docs, list)
            assert len(enabled_docs) > 0
            assert all(isinstance(doc_type, DocumentType) for doc_type in enabled_docs)

            # All should be enabled in default MVP config
            for doc_type in enabled_docs:
                assert config.document_configs[doc_type].enabled is True

    def test_get_high_priority_documents(self):
        """Test getting list of high-priority documents."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            high_priority_docs = config.get_high_priority_documents()

            assert isinstance(high_priority_docs, list)
            assert len(high_priority_docs) > 0

            # Verify all returned documents have high priority
            for doc_type in high_priority_docs:
                assert config.document_configs[doc_type].priority == "high"
                assert config.document_configs[doc_type].enabled is True

    def test_get_documents_for_phase(self):
        """Test getting enabled documents for specific phase."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Test phase 1 documents
            phase1_docs = config.get_documents_for_phase(1)
            assert isinstance(phase1_docs, list)
            assert len(phase1_docs) > 0

            # Test phase 2 documents
            phase2_docs = config.get_documents_for_phase(2)
            assert isinstance(phase2_docs, list)
            assert len(phase2_docs) > 0

            # Test phase 3 documents
            phase3_docs = config.get_documents_for_phase(3)
            assert isinstance(phase3_docs, list)
            assert len(phase3_docs) > 0

    def test_enable_document(self):
        """Test enabling a document type."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Test enabling existing document
            config.document_configs[DocumentType.BUSINESS_CASE].enabled = False
            config.enable_document(
                DocumentType.BUSINESS_CASE, "Updated description", "high"
            )

            assert config.document_configs[DocumentType.BUSINESS_CASE].enabled is True

            # Test enabling non-existent document (should create new config)
            config.document_configs.clear()
            config.enable_document(
                DocumentType.BUSINESS_CASE, "New description", "normal"
            )

            assert DocumentType.BUSINESS_CASE in config.document_configs
            assert config.document_configs[DocumentType.BUSINESS_CASE].enabled is True
            assert (
                config.document_configs[DocumentType.BUSINESS_CASE].description
                == "New description"
            )

    def test_disable_document(self):
        """Test disabling a document type."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Ensure document is enabled first
            assert config.document_configs[DocumentType.BUSINESS_CASE].enabled is True

            # Disable it
            config.disable_document(DocumentType.BUSINESS_CASE)
            assert config.document_configs[DocumentType.BUSINESS_CASE].enabled is False

            # Test disabling non-existent document (should not crash)
            config.document_configs.clear()
            config.disable_document(
                DocumentType.BUSINESS_CASE
            )  # Should not raise error

    def test_update_project_info(self):
        """Test updating project information."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Update existing project info
            config.update_project_info(
                name="Updated Name",
                description="Updated Description",
                client_name="New Client",
                project_type="Updated Type",
            )

            assert config.project_info.name == "Updated Name"
            assert config.project_info.description == "Updated Description"
            assert config.project_info.client_name == "New Client"
            assert config.project_info.project_type == "Updated Type"

            # Test partial update
            config.update_project_info(name="Partially Updated")
            assert config.project_info.name == "Partially Updated"
            assert (
                config.project_info.description == "Updated Description"
            )  # Should remain

    def test_update_project_info_none(self):
        """Test updating project info when it's None."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()
            config.project_info = None

            config.update_project_info(name="New Name", description="New Description")

            assert config.project_info is not None
            assert config.project_info.name == "New Name"
            assert config.project_info.description == "New Description"

    def test_get_setting(self):
        """Test getting custom setting values."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Test getting existing setting
            export_formats = config.get_setting("export_formats")
            assert export_formats == ["pdf", "docx"]

            # Test getting nested setting
            require_citations = config.get_setting(
                "quality_standards.require_citations"
            )
            assert require_citations is True

            # Test getting non-existent setting with default
            non_existent = config.get_setting("non_existent_setting", "default_value")
            assert non_existent == "default_value"

            # Test getting non-existent setting without default
            non_existent_no_default = config.get_setting("non_existent_setting")
            assert non_existent_no_default is None

    def test_set_setting(self):
        """Test setting custom setting values."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Test setting top-level setting
            config.set_setting("new_setting", "new_value")
            assert config.get_setting("new_setting") == "new_value"

            # Test setting nested setting
            config.set_setting("nested.setting", "nested_value")
            assert config.get_setting("nested.setting") == "nested_value"

            # Test overwriting existing setting
            config.set_setting("export_formats", ["html", "markdown"])
            assert config.get_setting("export_formats") == ["html", "markdown"]

    def test_get_config_summary(self):
        """Test getting configuration summary."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            summary = config.get_config_summary()

            assert isinstance(summary, dict)
            assert "project_name" in summary
            assert "client_name" in summary
            assert "total_documents" in summary
            assert "enabled_documents" in summary
            assert "high_priority_documents" in summary
            assert "completion_percentage" in summary
            assert "phases" in summary
            assert "export_formats" in summary
            assert "quality_checks_enabled" in summary

            # Verify values
            assert summary["project_name"] == "Technical Sales Solution"
            assert summary["total_documents"] > 0
            assert summary["enabled_documents"] > 0
            assert isinstance(summary["phases"], dict)

    def test_load_document_configs(self):
        """Test loading document configurations from config data."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Test loading valid document config
            documents_config = {
                "business_case": {
                    "enabled": True,
                    "description": "Business case document",
                    "template_path": "/path/to/template.md",
                    "priority": "high",
                },
                "invalid_document_type": {
                    "enabled": True,
                    "description": "This should be ignored",
                },
            }

            # Clear existing configs to test loading
            config.document_configs.clear()
            config._load_document_configs(documents_config)

            # Should have loaded valid document type
            assert DocumentType.BUSINESS_CASE in config.document_configs
            assert config.document_configs[DocumentType.BUSINESS_CASE].enabled is True
            assert (
                config.document_configs[DocumentType.BUSINESS_CASE].description
                == "Business case document"
            )
            assert (
                config.document_configs[DocumentType.BUSINESS_CASE].template_path
                == "/path/to/template.md"
            )
            assert (
                config.document_configs[DocumentType.BUSINESS_CASE].priority == "high"
            )

            # Should not have loaded invalid document type
            assert len(config.document_configs) == 1

    def test_load_config_exception_handling(self):
        """Test load_config with file read exceptions."""
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("builtins.open", side_effect=IOError("File read error")),
        ):
            # Should fall back to default config without crashing
            config = ProjectConfiguration(Path("problematic_config.yaml"))

            # Should have default project info
            assert config.project_info.name == "Technical Sales Solution"
            assert len(config.document_configs) == 14

    def test_load_config_invalid_yaml(self):
        """Test load_config with invalid YAML content."""
        invalid_yaml = "invalid: yaml: content: ["

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=invalid_yaml)),
        ):
            # Should fall back to default config without crashing
            config = ProjectConfiguration(Path("invalid_config.yaml"))

            # Should have default project info
            assert config.project_info.name == "Technical Sales Solution"
