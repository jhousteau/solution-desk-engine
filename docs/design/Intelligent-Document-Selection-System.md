# Intelligent Document Selection System

## Core Concept

Given any source material and a target deliverable, intelligently select which documents to create, using source as input but always generating our own standardized versions.

## The Manual Process

1. **Analyze the source** - Extract all available information
2. **Understand the target** - Know what deliverable is needed
3. **Select necessary documents** - Choose which docs are needed for this path
4. **Generate each document** - Create our standard version, using source as input
5. **Produce target** - Assemble final deliverable from our documents

## Key Principle

We ALWAYS create our own documents to our standards. Source materials are inputs, not replacements.

**Critical Rule**: Source materials are raw ingredients. We always cook our own meal to our recipe, even if some ingredients are pre-prepared.

## The 11-Phase Framework Structure

```
opportunity/
├── 0-source/          # Given materials (POC, RFP, emails, etc.)
├── 1-research/        # Market analysis, industry patterns (~30 document types)
├── 2-requirements/    # Functional/non-functional requirements (~20 document types)
├── 3-analysis/        # Stakeholder, user analysis (~25 document types)
├── 4-business-case/   # ROI, value proposition (~15 document types)
├── 5-architecture/    # Technical design (~30 document types)
├── 6-solution-design/ # Detailed specifications (~35 document types)
├── 7-implementation-plan/ # Timeline, resources (~30 document types)
├── 8-proposal/        # Presentations, proposals (~20 document types)
├── 9-contract/        # Final deliverable (~15 document types)
└── 10-audit/          # Quality validation (~25 document types)
```

## Configuration System

### YAML-Driven Document Control

`research-documents-config.yaml`:
```yaml
documents_to_create:
  1-research:
    roi-patterns.md: true         # Generate this document
    implementation-patterns.md: true
    vendor-ecosystem.md: false    # Skip this document
  4-business-case:
    value-proposition.md: true
    roi-analysis.md: true
    benefits-realization.md: false
```

### Template System

`templates/` folder contains standardized templates:
- `gcp-consumption-analysis-template.md` - Cloud cost analysis
- `business-case-template.md` - ROI and value proposition
- `citation-standards.md` - Quality and sourcing standards
- `research-documents-config-template.yaml` - Master configuration
- `research-documents-status-template.yaml` - Progress tracking

## Selection Logic

### Document Selection Strategy

The system intelligently selects documents based on:

1. **Source Analysis** - What information exists in the source?
2. **Target Analysis** - What deliverable is needed?
3. **Gap Analysis** - What must be generated to bridge the gap?
4. **Path Optimization** - Minimum viable documentation set

### Selection Rules

**Always Generate Our Standards**:
- Source has requirements → Create OUR Requirements doc using their info
- Source mentions ROI → Create OUR Business Case doc with proper analysis
- Source has architecture → Create OUR Architecture doc to our standards
- Source lacks financials → Create Business Case with market research

**Example Logic**:
```
IF target = "Rapid POV SOW":
    MUST_HAVE = [roi-analysis, pov-specifications, implementation-timeline]
    CONDITIONAL = [market-analysis if missing, architecture if complex]
    SKIP = [detailed-personas, change-management, production-roadmap]
```

## Assets Harvested from Proven Framework

### 1. Core Framework Files
- `research-documents-config-template.yaml` - Master configuration (300+ documents)
- `research-documents-status-template.yaml` - Progress tracking
- `research-directory-recreation-guide.md` - Complete framework guide
- `AGENT-INSTRUCTIONS.md` - Quick start guide

### 2. Document Templates
- `gcp-consumption-analysis-template.md` - Cost analysis
- `cloud-budget-management-plan-template.md` - Budget planning
- `gcp-resource-allocation-plan-template.md` - Resource planning
- `citation-standards.md` - Quality standards

### 3. Best Practices Library
- `agentic-transformation-principles.md` - AI principles
- `quality-assurance-and-verification-protocols.md` - QA standards
- `gcp-consumption-calculation-guide.md` - GCP costing
- `daf-sow-preparation-plan.md` - SOW preparation

### 4. Export Infrastructure
- `export_docs.py` - Document conversion system
- `sow_template_processor.py` - SOW processing

## Example Workflow

### Source: Franchise Lease Management POC
### Target: $25K Rapid POV SOW

**Process**:

1. **Source Analysis**
   - POC has clear objectives (AI document search, 85% accuracy)
   - Business case mentioned but not detailed
   - Technical approach outlined
   - Timeline suggested (4-6 weeks)

2. **Target Requirements**
   - Rapid POV SOW needs: Prerequisites, Build tasks, Test criteria, Deliverables
   - Must demonstrate >10x ROI
   - Must fit 2-3 week timeline
   - Must include all SOW sections

3. **Document Selection** (~15-20 documents):
   ```yaml
   1-research:
     roi-patterns.md: true          # Prove >10x ROI
     critical-success-factors.md: true
   2-requirements:
     system-integration-analysis.md: true
   4-business-case:
     roi-analysis.md: true          # Critical for SOW
     value-proposition.md: true
   5-architecture:
     pov-architecture.md: true      # Build specifications
   7-implementation-plan:
     pov-implementation-timeline.md: true  # 2-3 weeks
     resource-allocation.md: true
   9-contract:
     rapid-pov-sow.md: true         # Final deliverable
   ```

4. **Generation Process**
   - Extract POC data as inputs
   - Generate each selected document using templates
   - Apply citation standards and QA protocols
   - Validate against target requirements

5. **Output**
   - Complete $25K Rapid POV SOW
   - All prerequisites defined
   - Build tasks specified
   - Success criteria established
   - Ready for signature

## Success Metrics

- **Efficiency**: Generate 15-20 documents instead of 300
- **Speed**: Complete process in <10 minutes
- **Quality**: Meet all template standards
- **Compliance**: Pass all validation gates
- **Utility**: Output requires minimal manual editing

## Quality Assurance

### Standards Applied
- Citation standards for all external data
- QA protocols for document validation
- Template compliance checking
- Target requirement verification

### Validation Gates
- Source analysis completeness
- Document selection appropriateness
- Template adherence
- Target deliverable completeness

## Implementation Notes

This system codifies the proven 11-phase methodology that successfully:
- Generated 73 documents for complex DAF engagement
- Discovered $57.7M - $97.4M opportunity (40-50x initial estimate)
- Achieved 35,467% - 114,200% ROI projection
- Completed full research-to-contract cycle

The intelligent selection ensures we maintain quality while optimizing for efficiency, generating only what's needed to successfully bridge from source to target deliverable.
