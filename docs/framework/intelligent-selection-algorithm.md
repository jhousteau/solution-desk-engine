# Intelligent Document Selection Algorithm

## Core Concept

The intelligent selection algorithm is the brain of the solution-desk-engine framework. It analyzes source materials and target requirements to determine the minimum viable set of documents needed to create a professional deliverable.

## Algorithm Overview

```
Source Analysis → Gap Analysis → Document Selection → Generation Control
```

## Phase 1: Source Analysis

### Information Extraction
Parse all materials in `0-source/` to extract:

**Business Information**:
- Company size and industry vertical
- Revenue figures and financial data
- Market position and competitive landscape
- Current technology stack and systems
- Business objectives and success metrics

**Technical Information**:
- Existing architecture and infrastructure
- Integration requirements and constraints
- Performance and scalability requirements
- Security and compliance needs
- Data sources and volumes

**Project Information**:
- Timeline and budget constraints
- Resource availability and skill sets
- Risk factors and constraints
- Stakeholder structure and decision makers
- Success criteria and acceptance requirements

### Source Quality Assessment
Rate source completeness on key dimensions:

```yaml
source_assessment:
  business_case_info: 0-100%    # ROI data, market sizing, value prop
  technical_requirements: 0-100% # Functional/non-functional specs
  stakeholder_context: 0-100%   # Decision makers, users, influencers
  financial_data: 0-100%        # Budget, current costs, ROI targets
  timeline_constraints: 0-100%   # Go-live dates, milestone requirements
  integration_needs: 0-100%     # Existing systems, data flows
```

## Phase 2: Target Analysis

### Deliverable Requirements
For each target deliverable type, define required information:

**Google DAF SOW Requirements**:
```yaml
required_sections:
  executive_summary:
    - business_value_statement: REQUIRED
    - roi_projection: REQUIRED (must be quantified)
    - technical_approach: REQUIRED
    - timeline_summary: REQUIRED

  technical_approach:
    - architecture_overview: REQUIRED
    - gcp_services_used: REQUIRED
    - integration_points: CONDITIONAL (if existing systems)
    - security_approach: REQUIRED

  business_case:
    - cost_analysis: REQUIRED (detailed)
    - benefits_quantification: REQUIRED
    - implementation_timeline: REQUIRED
    - success_metrics: REQUIRED

  implementation_details:
    - resource_requirements: REQUIRED
    - milestone_schedule: REQUIRED
    - risk_mitigation: CONDITIONAL (if high-risk project)
    - testing_approach: REQUIRED
```

**Enterprise RFP Response Requirements**:
```yaml
required_sections:
  company_overview:
    - partner_qualifications: REQUIRED
    - relevant_experience: REQUIRED
    - team_credentials: REQUIRED

  technical_solution:
    - detailed_architecture: REQUIRED
    - scalability_approach: REQUIRED
    - security_framework: REQUIRED
    - integration_strategy: REQUIRED

  implementation_approach:
    - project_methodology: REQUIRED
    - timeline_and_milestones: REQUIRED
    - change_management: CONDITIONAL (if >100 users)
    - testing_and_qa: REQUIRED
```

## Phase 3: Gap Analysis

### Information Gap Detection
Compare source completeness against target requirements:

```python
def detect_gaps(source_assessment, target_requirements):
    gaps = {}

    for section, requirements in target_requirements.items():
        gaps[section] = {}

        for requirement, priority in requirements.items():
            source_score = source_assessment.get(requirement, 0)

            if priority == "REQUIRED" and source_score < 70:
                gaps[section][requirement] = {
                    "severity": "HIGH",
                    "source_score": source_score,
                    "documents_needed": get_documents_for_requirement(requirement)
                }
            elif priority == "CONDITIONAL":
                # Check conditions and assess if needed
                if check_condition(requirement) and source_score < 70:
                    gaps[section][requirement] = {
                        "severity": "MEDIUM",
                        "source_score": source_score,
                        "documents_needed": get_documents_for_requirement(requirement)
                    }
```

### Document Mapping
Map information gaps to specific documents that can fill them:

```yaml
gap_to_document_mapping:
  roi_projection:
    primary: "4-business-case/roi-analysis.md"
    supporting:
      - "1-research/market-financial-analysis.md"
      - "4-business-case/benefits-realization.md"

  architecture_overview:
    primary: "5-architecture/solution-architecture.md"
    supporting:
      - "5-architecture/integration-architecture.md"
      - "5-architecture/security-architecture.md"

  gcp_services_used:
    primary: "5-architecture/gcp-services-analysis.md"
    supporting:
      - "7-implementation-plan/gcp-resource-allocation.md"
      - "4-business-case/gcp-cost-analysis.md"
```

## Phase 4: Document Selection

### Selection Rules

**Rule 1: Always Generate Primary Documents**
```yaml
if gap.severity == "HIGH":
  select_document(gap.primary_document)
  for doc in gap.supporting_documents:
    if source_assessment[doc.required_info] < 50:
      select_document(doc)
```

**Rule 2: Conditional Selection Based on Project Characteristics**
```yaml
project_characteristics:
  enterprise_scale: user_count > 100
  complex_integration: existing_systems_count > 5
  regulated_industry: industry in [healthcare, financial, government]
  tight_timeline: project_duration < 12_weeks

conditional_documents:
  if enterprise_scale:
    select: ["3-analysis/change-management.md", "3-analysis/user-adoption.md"]

  if complex_integration:
    select: ["2-requirements/integration-requirements.md", "5-architecture/data-architecture.md"]

  if regulated_industry:
    select: ["2-requirements/compliance-requirements.md", "5-architecture/security-architecture.md"]
```

**Rule 3: Optimization for Document Count**
Prefer documents that address multiple gaps:

```python
def optimize_selection(selected_documents, gaps):
    # Calculate coverage score for each document
    coverage_scores = {}
    for doc in selected_documents:
        coverage_scores[doc] = calculate_gap_coverage(doc, gaps)

    # Remove redundant documents
    optimized = []
    remaining_gaps = gaps.copy()

    # Sort by coverage score and select highest impact documents
    for doc in sorted(selected_documents, key=lambda x: coverage_scores[x], reverse=True):
        if has_uncovered_gaps(doc, remaining_gaps):
            optimized.append(doc)
            remaining_gaps = remove_covered_gaps(doc, remaining_gaps)

    return optimized
```

## Phase 5: Generation Control

### YAML Configuration Output
The selection algorithm generates a project-specific configuration:

```yaml
# Generated: opportunities/[client]/[project]/research-documents-config.yaml
documents_to_create:
  1-research:
    market-financial-analysis.md: true    # HIGH priority gap: financial_data
    roi-patterns.md: true                 # HIGH priority gap: roi_benchmarks
    implementation-patterns.md: false     # Source has sufficient info

  2-requirements:
    functional-requirements.md: true      # HIGH priority gap: technical_specs
    integration-requirements.md: true     # CONDITIONAL: complex_integration = true
    compliance-requirements.md: false     # CONDITIONAL: regulated_industry = false

  4-business-case:
    roi-analysis.md: true                # HIGH priority gap: roi_projection
    cost-benefit-analysis.md: true       # HIGH priority gap: cost_analysis
    benefits-realization.md: false       # Source has adequate benefits info
```

### Selection Metadata
Track selection reasoning for audit and optimization:

```yaml
selection_metadata:
  algorithm_version: "v1.0"
  analysis_timestamp: "2024-01-15T10:30:00Z"
  source_assessment_scores:
    business_case_info: 45
    technical_requirements: 70
    financial_data: 30

  gap_analysis_summary:
    high_priority_gaps: 5
    medium_priority_gaps: 3
    documents_selected: 12
    documents_skipped: 18

  selection_reasoning:
    "1-research/market-financial-analysis.md": "HIGH gap: financial_data (30% complete)"
    "2-requirements/integration-requirements.md": "CONDITIONAL: complex_integration=true (6 existing systems)"
    "4-business-case/benefits-realization.md": "SKIPPED: source has 85% coverage"
```

## Quality Validation

### Selection Review Process
1. **Completeness Check**: Verify all HIGH priority gaps are addressed
2. **Redundancy Check**: Ensure no unnecessary document overlap
3. **Feasibility Check**: Validate selected documents can be completed with available information
4. **Optimization Check**: Confirm minimum viable set for target deliverable

### Human Override Capability
Allow manual adjustment of algorithm selections:

```yaml
manual_overrides:
  force_include:
    - "3-analysis/stakeholder-mapping.md"  # Reason: Complex org structure discovered

  force_exclude:
    - "5-architecture/detailed-design.md"  # Reason: POV scope too limited

  priority_adjustments:
    "1-research/competitive-analysis.md": "HIGH"  # Reason: Competitive bid situation
```

## Algorithm Evolution

### Learning and Improvement
- Track success rates of different document combinations
- Analyze which selections lead to successful deliverables
- Incorporate feedback from delivery teams
- Refine gap detection and document mapping based on outcomes

### Version Control
- Algorithm versions tied to framework releases
- Backward compatibility with previous configurations
- Clear migration path for algorithm updates
- Audit trail of all selection decisions

This algorithm ensures that every opportunity gets the right documents—no more, no less—while maintaining the quality and completeness needed for successful deliverables.
