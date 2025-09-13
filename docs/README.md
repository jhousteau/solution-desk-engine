# Solution Desk Engine Documentation

This directory contains all documentation for the Solution Desk Engine technical sales framework.

## Documentation Structure

<!-- auto-generated-start -->
```
docs
├── api/                        # API reference documentation
├── architecture/              # Architecture decisions and design
├── design/                    # Technical design documents
│   ├── Intelligent-Document-Selection-System.md
│   ├── migration.md
│   └── Technical-Sales-Solutioning-MVP-PRD.md
├── framework/                 # Framework documentation
│   ├── 11-phase-methodology.md
│   ├── AGENT-INSTRUCTIONS.md
│   ├── document-mappings.md
│   ├── intelligent-selection-algorithm.md
│   ├── README.md
│   ├── research-directory-recreation-guide.md
│   └── templates-organization-assessment.md
├── guides/                    # User guides and agent documentation
│   ├── agents/               # 26 specialized agent personas (complete library)
│   ├── 1-opportunity-setup.md
│   ├── agent-creation-best-practices.md
│   ├── agent-orchestration-architecture.md
│   └── agent-persona-template.md
├── templates/                 # Document templates and examples
│   ├── gcp_consumption_analysis.md
│   └── market_financial_analysis.md
├── working/                   # Active project work
└── README.md                  # This file
```
<!-- auto-generated-end -->

## Quick Links

### Framework Core
- [11-Phase Methodology](framework/11-phase-methodology.md) - Complete technical sales framework
- [Agent Orchestration Architecture](guides/agent-orchestration-architecture.md) - Dynamic team formation system
- [Opportunity Setup Guide](guides/1-opportunity-setup.md) - Project initialization process

### Agent Library (26 Specialists)
- [Agent Creation Best Practices](guides/agent-creation-best-practices.md) - Design guidelines
- [Agent Persona Template](guides/agent-persona-template.md) - Standardized template
- [Complete Agent Library](guides/agents/) - All 26 specialized agent personas

### Templates & Tools
- [GCP Cost Analysis Template](templates/gcp_consumption_analysis.md) - Advanced GCP pricing model
- [Market Analysis Template](templates/market_financial_analysis.md) - Financial projections framework
- [Intelligent Document Selection](design/Intelligent-Document-Selection-System.md) - Document management system

## Framework Status

**Current Implementation**: 11-Phase Technical Sales Framework with Agent Orchestration

**Key Features**:
- **26 Specialized Agents**: Complete domain expert library across all phases
- **Dynamic Team Formation**: Context-efficient 5-6 agent teams for optimal execution
- **11-Phase Methodology**: Comprehensive technical sales solutioning framework
- **Document Management**: Multi-format export and quality validation systems

**Quality Standards**:
- **Type Safety**: 100% MyPy compliance with strict typing
- **Test Coverage**: 75% minimum enforcement (configured in pyproject.toml)
- **Security**: Bandit + detect-secrets validation
- **Code Quality**: Black + Ruff + isort formatting

## Contributing to Documentation

When adding documentation:

1. Place API docs in the `api/` directory
2. Place user guides and tutorials in `guides/`
3. Place architecture decisions and design docs in `architecture/`
4. Use clear, descriptive filenames
5. Follow the existing documentation style

## Building Documentation

For projects that generate documentation:

```bash
# Build API documentation
make docs

# Serve docs locally
make serve-docs
```
