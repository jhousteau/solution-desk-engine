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
- `poetry run pytest` - Run all tests (153 tests, 76.35% coverage)
- `poetry run pytest tests/specific_test.py` - Run a single test file
- `poetry run pytest -k test_name` - Run specific test by name
- `poetry run pytest --cov --cov-fail-under=80` - Coverage enforcement (80% minimum)

## Project Architecture

This is a **technical sales solutioning framework** built as a Python CLI application with Genesis integration. The framework implements a structured 3-phase methodology for cloud consulting engagements.

### Core Architecture Components

**Framework Core** (`src/solution_desk_engine/framework/`):
- `methodology.py` - 3-phase methodology (Analyze → Design → Package) with 14 document types
- `progress_tracker.py` - Real-time progress monitoring with JSON persistence

**Document Management** (`src/solution_desk_engine/`):
- `export/document_exporter.py` - Multi-format export (PDF, DOCX, HTML, Markdown) with Pandoc integration
- `quality/validator.py` - Document validation with citation enforcement and quality scoring
- `config/project_config.py` - YAML-based project configuration and settings

**CLI Interface** (`src/solution_desk_engine/cli.py`):
- Click-based commands with Rich terminal styling
- Entry point: `solution-desk-engine` command via poetry.scripts

### Technical Sales Methodology

The framework orchestrates a **3-phase workflow**:
1. **Phase 1 (Analyze)**: Requirements analysis, market research, stakeholder mapping (5 documents)
2. **Phase 2 (Design)**: Architecture design, business case, GCP consumption analysis (5 documents)
3. **Phase 3 (Package)**: Executive summaries, technical proposals, cost breakdowns (4 documents)

Each phase contains specific `DocumentType` enums mapped to templates with validation rules and export capabilities.

## Code Quality Standards

The project enforces strict code quality through pre-commit hooks:
- **MyPy**: 100% strict type checking compliance (all methods require type annotations)
- **Black** (line-length=88) for code formatting
- **Ruff** for linting with auto-fix
- **isort** for import sorting
- **Bandit** for security scanning
- **detect-secrets** for credential scanning with baseline file
- **Test Coverage**: 80% minimum enforced (currently 76.35% with 153 tests)

## Development Environment

- Python 3.11+ required
- Uses Poetry for virtual environment and dependency management
- Pre-commit hooks automatically run quality checks
- File organization is enforced via Genesis standards (scripts/check-file-organization.sh)

## Framework-Specific Development Notes

### Key Implementation Patterns
- **Dataclass + Enums**: All framework entities use `@dataclass` with typed enum properties
- **Progress Persistence**: JSON-based progress tracking in `.solution-desk-engine/progress.json`
- **Multi-Format Export**: Primary export via Pandoc with fallback strategies (weasyprint for PDF, python-docx for DOCX)
- **Validation Pipeline**: Citation enforcement for financial data, professional tone checking, structure validation

### Working with the Framework
- Document types are defined in `DocumentType` enum (14 total across 3 phases)
- Progress tracking uses `PhaseStatus.PENDING/IN_PROGRESS/COMPLETED` state machine
- Quality validation returns `ValidationResult` with 0-100 scoring and typed `ValidationIssue` list
- Export operations return `ExportResult` with success/failure status and detailed error messages

## Genesis Integration

This project uses Genesis CLI features:
- `make genesis-commit` - Smart commit with quality gates
- `make worktree-create NAME=feature-name` - Create AI-safe worktrees
- Genesis file organization checking is enforced via hooks
