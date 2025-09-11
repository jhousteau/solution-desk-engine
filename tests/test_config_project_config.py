"""Tests for the project configuration management functionality."""

from pathlib import Path
from unittest.mock import patch

from solution_desk_engine.config.project_config import (
    DocumentConfig,
    ProjectConfiguration,
    ProjectInfo,
)

# from solution_desk_engine.framework.methodology import DocumentType  # TODO: Re-enable when methodology is reimplemented


class TestProjectInfo:
    """Test cases for ProjectInfo class."""

    def test_project_info_creation(self) -> None:
        """Test creating ProjectInfo with required fields."""
        project_info = ProjectInfo(
            name="Test Project", description="A test project for validation"
        )

        assert project_info.name == "Test Project"
        assert project_info.description == "A test project for validation"
        assert project_info.client_name is None
        assert project_info.project_type is None

    def test_project_info_with_optional_fields(self) -> None:
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

    def test_document_config_creation(self) -> None:
        """Test creating DocumentConfig with required fields."""
        doc_config = DocumentConfig(
            enabled=True, description="Test document configuration"
        )

        assert doc_config.enabled is True
        assert doc_config.description == "Test document configuration"
        assert doc_config.template_path is None
        assert doc_config.priority == "normal"

    def test_document_config_with_optional_fields(self) -> None:
        """Test DocumentConfig with optional fields."""
        doc_config = DocumentConfig(
            enabled=False,
            description="Test document",
            template_path="templates/test.md",
            priority="high",
        )

        assert doc_config.enabled is False
        assert doc_config.template_path == "templates/test.md"
        assert doc_config.priority == "high"


class TestProjectConfiguration:
    """Test cases for ProjectConfiguration class."""

    def test_project_configuration_initialization_no_file(self) -> None:
        """Test ProjectConfiguration when no config file exists."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration(Path("test_config.yaml"))

            # Test that default initialization works
            assert config.project_info is not None
            assert config.project_info.name == "Technical Sales Solution"
            assert isinstance(config.document_configs, dict)
            assert isinstance(config.custom_settings, dict)

    def test_project_configuration_custom_settings(self) -> None:
        """Test custom settings management."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration(Path("test.yaml"))

            # Test that default custom settings exist
            assert "export_formats" in config.custom_settings
            assert "quality_standards" in config.custom_settings
            assert "templates" in config.custom_settings

            # Test updating custom settings directly
            config.custom_settings["new_setting"] = "test_value"
            assert config.custom_settings["new_setting"] == "test_value"

    def test_update_project_info(self) -> None:
        """Test updating project information."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration(Path("test.yaml"))

            config.update_project_info(
                name="New Project Name",
                description="Updated description",
                client_name="Test Client",
            )

            assert config.project_info.name == "New Project Name"
            assert config.project_info.description == "Updated description"
            assert config.project_info.client_name == "Test Client"

    def test_basic_configuration_properties(self) -> None:
        """Test basic configuration properties."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration(Path("test.yaml"))

            # Test that basic properties are accessible
            assert config.project_info is not None
            assert config.custom_settings is not None
            assert config.document_configs is not None
            assert config.project_info.name == "Technical Sales Solution"


# TODO: Re-enable when DocumentType enum is reimplemented
# The following tests depend on the DocumentType enum and methodology framework
# that was removed during the framework refactoring. These will be restored
# when the new 11-phase methodology is implemented.
#
# class TestProjectConfigurationDocumentTypes:
#     def test_is_document_enabled(self) -> None:
#     def test_get_enabled_documents(self) -> None:
#     def test_get_high_priority_documents(self) -> None:
#     def test_get_documents_for_phase(self) -> None:
#     def test_enable_document(self) -> None:
#     def test_disable_document(self) -> None:
