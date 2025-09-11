# Solution Desk Engine

**AI-powered technical sales solutioning framework** for cloud consulting engagements.

Transform complex technical sales processes into structured, repeatable methodologies with automated document generation, quality validation, and progress tracking.

## Overview

Solution Desk Engine implements a streamlined **3-phase methodology** for technical sales solutioning:

1. **Analyze** - Requirements analysis, market research, and stakeholder mapping
2. **Design** - Architecture design, business case development, and solution specification
3. **Package** - Proposal creation, cost breakdown, and client presentation materials

Built on proven Genesis framework utilities for enterprise-grade reliability and maintainability.

## Core Features

### 📋 Methodology Framework
- **3-Phase Process**: Analyze → Design → Package workflow
- **14 Document Templates**: Comprehensive templates for all deliverables
- **Progress Tracking**: Real-time completion monitoring with phase status
- **Quality Validation**: Automated document quality scoring and citation enforcement

### 🎯 Specialized Components
- **GCP Consumption Analysis**: Advanced cost modeling with DAF qualification logic
- **Market & Financial Analysis**: Revenue projections and opportunity sizing
- **Architecture Design**: Technical solution specification and integration planning
- **Stakeholder Mapping**: Engagement planning and decision-maker identification

### 🚀 Export & Delivery
- **Multi-Format Export**: PDF, DOCX, HTML, and Markdown output
- **Professional Styling**: Enterprise-ready document formatting
- **Executive Summaries**: C-level presentation materials
- **Technical Proposals**: Detailed implementation specifications

### 🔧 Developer Experience
- **Type-Safe**: Full MyPy compliance with strict typing
- **CLI Interface**: Rich terminal experience with progress indicators
- **Configuration Management**: Project-specific settings and customization
- **Security Scanning**: Automated secret detection and security validation

## Installation

### Prerequisites

- Python 3.11+
- Poetry

### Install from Source

```bash
# Clone and install
git clone <repository-url>
cd solution-desk-engine
poetry install
```

### Install as Package

```bash
pip install solution-desk-engine
```

## Usage

After installation, you can use the `solution-desk-engine` command:

```bash
# Show help
solution-desk-engine --help

# Say hello
solution-desk-engine hello
solution-desk-engine hello --name Alice --count 3

# Display styled messages
solution-desk-engine display "Welcome to solution-desk-engine!"
solution-desk-engine display "Success!" --style success
solution-desk-engine display "Warning!" --style warning

# Check status
solution-desk-engine status
```

## Available Commands

<!-- auto-generated-start -->
```bash
solution-desk-engine --help
```

**Core Commands:**
- `hello` - Say hello to someone (with name and count options)
- `display` - Display text with rich styling options (success, warning, error styles)
- `status` - Show application status and version information

**Framework Commands:**
- `init-project` - Initialize new technical sales project
- `generate-docs` - Generate documents from templates
- `validate-quality` - Run quality validation on documents
- `export-deliverables` - Export documents to multiple formats
- `track-progress` - View project progress and completion status
<!-- auto-generated-end -->

## API Reference

<!-- auto-generated-start -->
### Core Framework Classes

**`TechnicalSalesMethodology`**
- Main framework orchestrating 3-phase solutioning process
- Methods: `get_phase()`, `get_documents_for_phase()`, `get_progress_summary()`
- Manages 14 document types across Analyze/Design/Package phases

**`ProgressTracker`**
- Real-time project progress monitoring and persistence
- Methods: `start_document()`, `complete_document()`, `display_progress()`
- JSON-based progress persistence with phase completion tracking

**`DocumentExporter`**
- Multi-format export engine (PDF, DOCX, HTML, Markdown)
- Methods: `export_document()`, `export_multiple_documents()`
- Pandoc integration with fallback export strategies

**`DocumentValidator`**
- Quality validation with citation enforcement
- Methods: `validate_document()`, `validate_multiple_documents()`
- Configurable quality scoring (0-100 scale)

**`ProjectConfiguration`**
- Project-specific settings and document management
- Methods: `load_config()`, `save_config()`, `get_enabled_documents()`
- YAML-based configuration with MVP defaults
<!-- auto-generated-end -->

## Development

```bash
# Install dependencies
make setup

# Run the CLI in development
make run-dev

# Run tests with coverage
make test-cov

# Run all quality checks (format, lint, typecheck)
make quality

# Format code
make format
```

### Quality Assurance

The project enforces strict quality standards:

```bash
# Type checking with MyPy
make typecheck

# Security scanning
poetry run bandit -r src/
poetry run detect-secrets scan --baseline .secrets.baseline

# Linting and formatting
poetry run ruff check src/ --fix
poetry run black src/ tests/
```

## Building and Distribution

```bash
# Build the package
poetry build

# Publish to PyPI (if configured)
poetry publish
```

## Testing

The project maintains **93.86% test coverage** with 138 comprehensive tests across 12 test modules:

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run all quality checks
make quality
```

### Test Suite Coverage

- **Framework Core**: TechnicalSalesMethodology, ProgressTracker
- **Export Engine**: Multi-format document export with fallback strategies
- **Quality Validation**: Document validation and citation enforcement
- **Configuration**: Project settings and YAML management
- **Integration**: End-to-end workflow testing
- **CLI Interface**: Command validation and rich output testing

## Framework Architecture

### Document Templates

The framework includes 14 comprehensive document templates:

**Phase 1: Analyze**
- Source Materials Collection
- Requirements Analysis
- Market & Financial Analysis
- System Integration Analysis
- Stakeholder Mapping

**Phase 2: Design**
- Business Case
- Architecture Overview
- GCP Consumption Analysis (with DAF qualification)
- Solution Design
- Implementation Plan

**Phase 3: Package**
- Executive Summary
- Technical Proposal
- Cost Breakdown
- Implementation Roadmap

### Quality Standards

- **Citation Enforcement**: All financial data must include citations
- **Professional Language**: Automated tone and style validation
- **Completeness Checking**: Template placeholder detection
- **Structure Validation**: Consistent document organization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run `make quality` to ensure all checks pass
6. Submit a pull request with clear description

### Code Standards

- **Type Safety**: Full MyPy compliance required
- **Security**: All subprocess calls must be annotated with `# nosec`
- **Documentation**: All public methods require docstrings
- **Testing**: Maintain >80% code coverage
