# Solution Desk Engine Documentation

This directory contains all documentation for the Solution Desk Engine technical sales framework.

## Documentation Structure

<!-- auto-generated-start -->
```
docs
├── api                         # API reference documentation (placeholder)
├── architecture               # Architecture decisions and design (placeholder)
├── design/                    # Technical design documents
│   ├── migration.md          # Migration specifications and requirements
│   └── Technical-Sales-Solutioning-MVP-PRD.md  # Product Requirements Document
├── guides                     # User guides and tutorials (placeholder)
├── templates/                 # Document templates and examples
│   ├── gcp_consumption_analysis.md    # GCP cost modeling template
│   └── market_financial_analysis.md   # Market analysis template
└── README.md                  # This file
```
<!-- auto-generated-end -->

## Quick Links

- [Migration Guide](design/migration.md) - Asset migration from legacy systems
- [MVP Requirements](design/Technical-Sales-Solutioning-MVP-PRD.md) - Product specification
- [GCP Cost Analysis Template](templates/gcp_consumption_analysis.md) - Advanced GCP pricing model
- [Market Analysis Template](templates/market_financial_analysis.md) - Financial projections framework

## Framework Status

**Current Implementation**: Technical Sales Solutioning MVP with 3-phase methodology

**Quality Metrics**:
- **Test Coverage**: 93.86% (138 tests across 12 modules)
- **Type Safety**: 100% MyPy compliance
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
