"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner

from solution_desk_engine.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    """Create CLI test runner."""
    return CliRunner()


def test_cli_help(runner: CliRunner) -> None:
    """Test CLI help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Technical Sales Solutioning Framework" in result.output


def test_status_command(runner: CliRunner) -> None:
    """Test status command."""
    result = runner.invoke(cli, ["status"])
    assert result.exit_code == 0
    assert "solution-desk-engine Framework" in result.output
    assert "11-Phase Technical Sales Methodology" in result.output


def test_invalid_command(runner: CliRunner) -> None:
    """Test invalid command returns error."""
    result = runner.invoke(cli, ["invalid"])
    assert result.exit_code != 0


# TODO: Add tests for new framework commands when implemented
# def test_create_command(runner: CliRunner) -> None:
# def test_analyze_command(runner: CliRunner) -> None:
# def test_generate_command(runner: CliRunner) -> None:
