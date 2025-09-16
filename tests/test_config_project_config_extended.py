"""Extended tests for project configuration management - covering missing methods."""

import tempfile
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import yaml

from solution_desk_engine.config.project_config import ProjectConfiguration, ProjectInfo


class TestProjectConfigurationLoadSave:
    """Test cases for load_config() and save_config() methods."""

    def test_load_config_valid_yaml(self) -> None:
        """Test loading configuration from a valid YAML file."""
        config_data = {
            "project_info": {
                "name": "Test Project",
                "description": "Test Description",
                "client_name": "Test Client",
                "project_type": "Technical Sales",
            },
            "documents": {},
            "settings": {
                "export_formats": ["pdf", "docx", "html"],
                "quality_standards": {
                    "require_citations": False,
                    "minimum_word_count": 50,
                },
            },
        }

        yaml_content = yaml.dump(config_data)

        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=yaml_content)):
                config = ProjectConfiguration(Path("test_config.yaml"))

                assert config.project_info is not None
                assert config.project_info.name == "Test Project"
                assert config.project_info.description == "Test Description"
                assert config.project_info.client_name == "Test Client"
                assert config.project_info.project_type == "Technical Sales"
                assert config.custom_settings["export_formats"] == [
                    "pdf",
                    "docx",
                    "html",
                ]
                assert (
                    config.custom_settings["quality_standards"]["require_citations"]
                    is False
                )

    def test_load_config_partial_yaml(self) -> None:
        """Test loading configuration with only partial data."""
        config_data = {
            "project_info": {
                "name": "Minimal Project",
                "description": "Minimal Description",
            },
        }

        yaml_content = yaml.dump(config_data)

        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=yaml_content)):
                config = ProjectConfiguration(Path("minimal_config.yaml"))

                assert config.project_info.name == "Minimal Project"
                assert config.project_info.client_name is None
                # Custom settings should be empty since we didn't provide them
                assert isinstance(config.custom_settings, dict)

    def test_load_config_invalid_yaml(self) -> None:
        """Test loading configuration from an invalid YAML file."""
        invalid_yaml = "invalid: yaml: content: [unclosed"

        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=invalid_yaml)):
                with patch("builtins.print") as mock_print:
                    config = ProjectConfiguration(Path("invalid_config.yaml"))

                    # Should fall back to default config
                    assert config.project_info.name == "Technical Sales Solution"
                    # Warning should be printed
                    mock_print.assert_called_once()
                    assert (
                        "Warning: Failed to load config" in mock_print.call_args[0][0]
                    )

    def test_load_config_file_not_found(self) -> None:
        """Test loading configuration when file doesn't exist after check."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open", side_effect=FileNotFoundError):
                with patch("builtins.print") as mock_print:
                    config = ProjectConfiguration(Path("missing_config.yaml"))

                    # Should fall back to default config
                    assert config.project_info.name == "Technical Sales Solution"
                    mock_print.assert_called_once()

    def test_save_config_complete(self) -> None:
        """Test saving complete configuration to YAML file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            config_path = Path(f.name)

        try:
            with patch("pathlib.Path.exists", return_value=False):
                config = ProjectConfiguration(config_path)
                config.project_info = ProjectInfo(
                    name="Save Test Project",
                    description="Testing save functionality",
                    client_name="Test Client",
                    project_type="Technical Sales",
                )
                config.custom_settings = {
                    "export_formats": ["pdf"],
                    "custom_value": 42,
                }

                # Keep document configs empty since the current implementation
                # expects DocumentType enum which is temporarily disabled
                config.document_configs = {}

                config.save_config()

                # Read back the saved file
                with open(config_path, "r") as f:
                    saved_data = yaml.safe_load(f)

                assert saved_data["project_info"]["name"] == "Save Test Project"
                assert saved_data["project_info"]["client_name"] == "Test Client"
                assert saved_data["settings"]["export_formats"] == ["pdf"]
                assert saved_data["settings"]["custom_value"] == 42
                assert saved_data["documents"] == {}

        finally:
            config_path.unlink(missing_ok=True)

    def test_save_config_no_project_info(self) -> None:
        """Test that save_config does nothing when project_info is None."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            config_path = Path(f.name)

        try:
            with patch("pathlib.Path.exists", return_value=False):
                config = ProjectConfiguration(config_path)
                config.project_info = None  # Explicitly set to None

                config.save_config()

                # File should not be created
                assert not config_path.exists()

        finally:
            config_path.unlink(missing_ok=True)

    def test_save_config_with_exception(self) -> None:
        """Test save_config handles write exceptions gracefully."""
        config = ProjectConfiguration(Path("/invalid/path/config.yaml"))
        config.project_info = ProjectInfo("Test", "Test Description")

        # Should not raise exception
        with patch("builtins.open", side_effect=PermissionError):
            with pytest.raises(PermissionError):
                config.save_config()


class TestProjectConfigurationSettings:
    """Test cases for get_setting() and set_setting() methods."""

    def test_get_setting_simple(self) -> None:
        """Test getting a simple setting value."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()
            config.custom_settings = {"test_key": "test_value"}

            assert config.get_setting("test_key") == "test_value"
            assert config.get_setting("missing_key") is None
            assert config.get_setting("missing_key", "default") == "default"

    def test_get_setting_nested(self) -> None:
        """Test getting nested setting values with dot notation."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()
            config.custom_settings = {
                "level1": {"level2": {"level3": "deep_value"}, "other": "other_value"}
            }

            assert config.get_setting("level1.level2.level3") == "deep_value"
            assert config.get_setting("level1.other") == "other_value"
            assert config.get_setting("level1.missing") is None
            assert config.get_setting("level1.missing.deep") is None

    def test_get_setting_default_values(self) -> None:
        """Test getting settings from default configuration."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            assert config.get_setting("export_formats") == ["pdf", "docx"]
            assert config.get_setting("quality_standards.require_citations") is True
            assert config.get_setting("quality_standards.minimum_word_count") == 100
            assert config.get_setting("templates.use_professional_styling") is True

    def test_set_setting_simple(self) -> None:
        """Test setting a simple value."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            config.set_setting("new_key", "new_value")
            assert config.custom_settings["new_key"] == "new_value"

            config.set_setting("existing_key", "updated_value")
            assert config.custom_settings["existing_key"] == "updated_value"

    def test_set_setting_nested_existing(self) -> None:
        """Test setting nested values in existing structure."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Modify existing nested setting
            config.set_setting("quality_standards.require_citations", False)
            assert (
                config.custom_settings["quality_standards"]["require_citations"]
                is False
            )

            # Add new key to existing nested dict
            config.set_setting("quality_standards.new_rule", "strict")
            assert config.custom_settings["quality_standards"]["new_rule"] == "strict"

    def test_set_setting_nested_new(self) -> None:
        """Test creating new nested structure with dot notation."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Create entirely new nested structure
            config.set_setting("new.nested.path", "value")
            assert config.custom_settings["new"]["nested"]["path"] == "value"

            # Add another value at intermediate level
            config.set_setting("new.nested.sibling", "sibling_value")
            assert config.custom_settings["new"]["nested"]["sibling"] == "sibling_value"
            assert config.custom_settings["new"]["nested"]["path"] == "value"

    def test_set_setting_complex_types(self) -> None:
        """Test setting complex data types."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Set list
            config.set_setting("formats", ["pdf", "docx", "html"])
            assert config.custom_settings["formats"] == ["pdf", "docx", "html"]

            # Set dict
            config.set_setting("metadata", {"author": "Test", "version": "1.0"})
            assert config.custom_settings["metadata"]["author"] == "Test"

            # Set boolean
            config.set_setting("flags.enabled", True)
            assert config.custom_settings["flags"]["enabled"] is True


class TestProjectConfigurationMethods:
    """Test other uncovered methods in ProjectConfiguration."""

    def test_get_setting_with_non_dict_parent(self) -> None:
        """Test get_setting when parent is not a dict."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()
            config.custom_settings = {
                "scalar": "value",
                "list": [1, 2, 3],
            }

            # Trying to access nested key on scalar returns default
            assert config.get_setting("scalar.nested") is None
            assert config.get_setting("scalar.nested", "default") == "default"

            # Trying to access nested key on list returns default
            assert config.get_setting("list.nested") is None

    def test_update_project_info_from_none(self) -> None:
        """Test update_project_info when project_info is initially None."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()
            config.project_info = None  # Explicitly set to None

            config.update_project_info(
                name="Created Project",
                description="Created from None",
            )

            assert config.project_info is not None
            assert config.project_info.name == "Created Project"
            assert config.project_info.description == "Created from None"

    def test_update_project_info_partial(self) -> None:
        """Test partial updates to project_info."""
        with patch("pathlib.Path.exists", return_value=False):
            config = ProjectConfiguration()

            # Update only name
            config.update_project_info(name="New Name")
            assert config.project_info.name == "New Name"
            assert (
                config.project_info.description
                == "AI-powered technical sales solutioning project"
            )

            # Update only client_name
            config.update_project_info(client_name="New Client")
            assert config.project_info.name == "New Name"
            assert config.project_info.client_name == "New Client"

            # Update project_type
            config.update_project_info(project_type="POC")
            assert config.project_info.project_type == "POC"
