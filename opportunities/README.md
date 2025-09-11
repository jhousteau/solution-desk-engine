# Opportunities Directory

## Structure
All opportunities are organized as:
```
opportunities/
├── {client-name}/
│   └── {opportunity-name}/
│       ├── research-documents-config.yaml
│       ├── research-documents-status.yaml
│       ├── 0-source/         # Original client materials
│       ├── 1-research/       # Market analysis, patterns
│       ├── 2-requirements/   # Requirements analysis
│       ├── 3-analysis/       # Stakeholder analysis
│       ├── 4-business-case/  # ROI, value proposition
│       ├── 5-architecture/   # Technical design
│       ├── 6-solution-design/# Detailed specifications
│       ├── 7-implementation-plan/ # Timeline, resources
│       ├── 8-proposal/       # Presentations
│       ├── 9-contract/       # Final deliverable
│       └── 10-audit/         # Quality validation
```

## Workflow
1. Create client directory: `opportunities/{client}/`
2. Create opportunity directory: `opportunities/{client}/{opportunity}/`
3. Copy YAML configs from templates
4. Create 11-phase directory structure (0-10)
5. Place source materials in `0-source/`
6. Configure YAML to select needed documents
7. Generate selected documents using intelligent selection
8. Export final deliverable from `9-contract/`

## Example
See `opportunities/example-client/franchise-lease-management/` for complete structure.
