"""Tests for the main entry point."""

from unittest.mock import patch

from solution_desk_engine import main


class TestMain:
    """Test cases for main module."""

    @patch("solution_desk_engine.main.cli")
    def test_main_calls_cli(self, mock_cli):
        """Test that main() calls the CLI function."""
        main.main()
        mock_cli.assert_called_once()

    def test_main_exists(self):
        """Test that main function exists and is callable."""
        assert callable(main.main)
