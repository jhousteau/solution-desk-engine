# Solution Desk Engine

**AI-powered technical sales solutioning framework** for cloud consulting engagements.

Transform complex technical sales processes into structured, repeatable methodologies with automated document generation, quality validation, and progress tracking.

## Overview

Solution Desk Engine implements a comprehensive **11-phase methodology** for technical sales solutioning:

**Foundation Phase**: Project setup and requirements gathering
**Analysis Phase**: Deep dive into technical and business requirements
**Design Phase**: Solution architecture and technical design
**Validation Phase**: Proof of concept and technical validation
**Costing Phase**: Financial modeling and pricing analysis
**Proposal Phase**: Comprehensive proposal development
**Presentation Phase**: Executive and technical presentations
**Negotiation Phase**: Contract and commercial discussions
**Implementation Phase**: Solution deployment planning
**Delivery Phase**: Project execution and delivery
**Closure Phase**: Project wrap-up and lessons learned

Built on proven Genesis framework utilities for enterprise-grade reliability and maintainability.

## Core Features

### 📋 Methodology Framework
- **11-Phase Process**: Comprehensive foundation to closure workflow
- **Agent Orchestration**: 26 specialized agents with dynamic team formation
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
# Show help
solution-desk-engine --help

# Show framework status and version
solution-desk-engine status

# SOW generation commands
solution-desk-engine sow generate           # Generate SOW from Google Docs template
solution-desk-engine sow validate-template  # Validate Google Docs template
```

**Core Commands:**
- `status` - Show framework status and version information
- `sow generate` - Generate SOW document from Google Docs template
- `sow validate-template` - Validate Google Docs template for SOW generation

**Framework Features:**
- 11-Phase methodology for cloud consulting engagements
- Google Drive integration for document generation
- SOW generator with template validation
- Comprehensive agent orchestration system with 26 specialized agents
<!-- auto-generated-end -->

## API Reference

<!-- auto-generated-start -->
### Core Framework Components

**Technical Sales Framework**
- 11-phase methodology for cloud consulting engagements
- Comprehensive document templates and validation systems
- Progress tracking and quality assurance automation
- Multi-format export capabilities (PDF, DOCX, HTML, Markdown)

**Agent Orchestration System**
- 26 specialized agents covering all phases of technical sales
- Dynamic team formation with 5-6 agent teams for optimal task execution
- Context-efficient orchestration preventing decision paralysis
- Professional system prompts with domain expertise

**Document Management**
- `DocumentExporter`: Multi-format export with Pandoc integration
- `DocumentValidator`: Quality validation with citation enforcement
- `ProjectConfiguration`: YAML-based project settings and configuration
- Template system supporting comprehensive technical sales methodology

**Development Tools**
- Poetry-based dependency management
- Comprehensive testing suite with coverage enforcement
- Pre-commit hooks with quality gates (Black, Ruff, MyPy, Bandit)
- Docker containerization for consistent deployment
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

The project maintains comprehensive test coverage with quality enforcement:

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
