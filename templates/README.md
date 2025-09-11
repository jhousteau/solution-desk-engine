# Templates Directory

## Structure

### `/config/`
YAML configuration templates:
- `research-documents-config-template.yaml` - Master document selection (300+ options)
- `research-documents-status-template.yaml` - Progress tracking template

### `/documents/`
Document templates for generation:
- `gcp-consumption-analysis-template.md` - Cloud cost analysis
- `cloud-budget-management-plan-template.md` - Budget planning
- `gcp-resource-allocation-plan-template.md` - Resource planning

### `/standards/`
Quality and citation standards:
- `citation-standards.md` - Sourcing and quality requirements

## Usage
1. Copy config templates to opportunity directory
2. Configure YAML flags for needed documents
3. Use document templates with intelligent generation
4. Apply standards for quality validation

## Template Variables
All templates use placeholders:
- `[CLIENT]` - Client company name
- `[PROJECT]` - Project name
- `[Amount]` - Financial figures
- `[URL]` - Source links

These are populated during document generation.
