# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Essential Commands
- `make setup` - Install dependencies and set up development environment (includes pre-commit hooks)
- `make test` - Run tests
- `make test-cov` - Run tests with coverage reporting
- `make quality` - Run all quality checks (format, lint, typecheck)
- `make run-dev` - Run the CLI in development mode

### Quality Assurance
- `make format` - Format code with black and isort
- `make typecheck` - Type check with mypy
- `poetry run ruff check src/ tests/ --fix` - Lint and auto-fix with ruff

### Testing
- `poetry run pytest` - Run all tests
- `poetry run pytest tests/specific_test.py` - Run a single test file
- `poetry run pytest -k test_name` - Run specific test by name

## Project Architecture

This is a Python CLI application built with the Genesis framework, using:

- **CLI Framework**: Click for command-line interface (src/solution_desk_engine/cli.py)
- **Output**: Rich library for terminal styling and formatting
- **Package Management**: Poetry for dependency management
- **Entry Point**: `solution-desk-engine` command via poetry.scripts

### Core Structure
- `src/solution_desk_engine/` - Main application code
  - `main.py` - Entry point that delegates to CLI
  - `cli.py` - All CLI commands and Click configuration
- `tests/` - Test files using pytest
- `docs/` - Documentation files

### Available CLI Commands
- `hello` - Greeting command with name and count options
- `display` - Display styled messages with different style options
- `status` - Show application status and version info

## Code Quality Standards

The project enforces strict code quality through pre-commit hooks:
- **Black** (line-length=88) for code formatting
- **Ruff** for linting with auto-fix
- **mypy** with strict type checking
- **isort** for import sorting
- **Bandit** for security scanning

## Development Environment

- Python 3.11+ required
- Uses Poetry for virtual environment and dependency management
- Pre-commit hooks automatically run quality checks
- File organization is enforced via Genesis standards (scripts/check-file-organization.sh)

## Genesis Integration

This project uses Genesis CLI features:
- `make genesis-commit` - Smart commit with quality gates
- `make worktree-create NAME=feature-name` - Create AI-safe worktrees
- Genesis file organization checking is enforced via hooks
