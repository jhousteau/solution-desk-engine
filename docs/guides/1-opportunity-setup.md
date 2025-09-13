# Opportunity Setup Guide

## Overview

This guide documents the complete process for setting up a new client opportunity within the solution-desk-engine framework. The process ensures consistent structure, proper document management, and efficient progression through the 11-phase methodology.

## Process Flow

### 1. Create Client Opportunity Structure

For each new opportunity, create a dedicated folder structure:

```
/opportunities/{client}/{opportunity}/
├── 0-source/
├── 1-research/
├── 2-requirements/
├── 3-analysis/
├── 4-business-case/
├── 5-architecture/
├── 6-solution-design/
├── 7-implementation-plan/
├── 8-proposal/
├── 9-contract/
├── 10-audit/
├── research-documents-config.yaml
└── research-documents-status.yaml
```

**Steps:**
1. Copy `/opportunities/example-client/` structure
2. Rename to `/opportunities/{client}/{opportunity}/`
3. Copy YAML templates to opportunity root

### 2. Document Conversion Requirements

#### Source Document Management
All source materials must be converted to markdown format and placed in the `0-source/` folder with **exact formatting preservation**.

**Critical Requirements:**
- No alterations except format conversion (.pdf → .md)
- Preserve all tables, numbering, legal language
- Maintain original structure and hierarchy
- Keep all financial details and pricing exactly as stated
- Preserve task lists, prerequisites, and deliverables

#### Naming Convention
- Use descriptive, hyphenated names
- Include document type and date when applicable
- Example: `google-sow-template-2025.md`, `franchise-lease-management-poc.md`

### 3. Target Document Analysis

#### Identify the Target Document
The target document represents the final deliverable (usually in phase 9-contract). Common targets:
- Statement of Work (SOW)
- Master Services Agreement
- Project Proposal
- Implementation Contract

#### Analysis Process
1. **Deep Analysis:** Identify all requirements, deliverables, and dependencies
2. **Deliverable Mapping:** Map each target requirement to supporting documentation
3. **Phase Dependencies:** Understand which phases feed into the target

### 4. Document Selection Methodology

#### Working Backwards Approach

Start from the target document (phase 9) and work backwards to identify only essential supporting documents:

**Phase 9 (Contract):** What documents are needed to complete the contract?
**Phase 8 (Proposal):** What's needed to support phase 9 deliverables?
**Phase 7 (Implementation):** What planning supports the proposal?
**...continue backwards to Phase 0**

#### Selection Criteria
- **Essential Only:** Select documents that directly contribute to the target
- **Linear Flow:** Create a logical progression from 0→10
- **No Over-Selection:** Avoid documents that don't support the target
- **No Under-Selection:** Don't miss critical supporting materials

#### Document Dependencies

Most phases build on each other:
- **0-source** → Provides raw materials for research
- **1-research** → Informs requirements gathering
- **2-requirements** → Feeds into analysis
- **3-analysis** → Supports business case development
- **4-business-case** → Justifies architecture decisions
- **5-architecture** → Enables solution design
- **6-solution-design** → Guides implementation planning
- **7-implementation-plan** → Supports proposal development
- **8-proposal** → Feeds into contract creation
- **9-contract** → Target deliverable
- **10-audit** → Validates completion

### 5. YAML Configuration Process

#### research-documents-config.yaml
1. Copy from `/templates/config/research-documents-config-template.yaml`
2. Update project metadata (name, description, client)
3. Set `create: true` for selected documents only
4. Set `create: false` for all others

#### research-documents-status.yaml
1. Copy from `/templates/config/research-documents-status-template.yaml`
2. Reset all `exists: false`
3. Update project name and metadata
4. Set completion percentages to 0%

### 6. Example: Google SOW Template Analysis

**Target Document:** Statement of Work for Google Cloud Workshops

**Required Deliverables:**
- Introduction Workshop ($10,000)
- Business Value Assessment ($20,000)
- Rapid POV ($25,000)

**Working Backwards - Essential Documents:**

**Phase 9 (Contract):**
- `statement-of-work.md` - Target document
- `deliverables-list.md` - Workshop deliverables
- `payment-schedule.md` - Pricing structure ($10K/$20K/$25K)

**Phase 8 (Proposal):**
- `executive-summary.md` - Executive overview
- `technical-overview.md` - Technical approach
- `pricing-proposal.md` - Commercial terms

**Phase 7 (Implementation):**
- `phase-1-pov-plan.md` - Rapid POV implementation
- `milestone-plan.md` - Workshop milestones

**Phase 6 (Solution Design):**
- `solution-design-overview.md` - Technical solution

**Phase 5 (Architecture):**
- `architecture-overview.md` - POC architecture
- `technology-stack.md` - Google Cloud services

**Phase 4 (Business Case):**
- `roi-analysis.md` - >10x ROI criteria
- `value-proposition.md` - Business value model

**Phase 3 (Analysis):**
- `stakeholder-map.md` - SPOC identification
- `current-state-analysis.md` - Customer discovery
- `gap-analysis.md` - Problem identification

**Phase 2 (Requirements):**
- `functional-requirements.md` - System capabilities
- `scope-definition.md` - POC boundaries

**Phase 1 (Research):**
- `problem-statement-research.md` - Customer pain points
- `solution-patterns.md` - Google Cloud solutions

**Phase 0 (Source):**
- `source-inventory.md` - Document catalog

### 7. Quality Gates

#### Document Conversion Verification
- [ ] All source documents converted to markdown
- [ ] Exact formatting preserved
- [ ] No content alterations
- [ ] Proper naming convention used

#### YAML Configuration Verification
- [ ] Only essential documents set to `create: true`
- [ ] No over-selection of documents
- [ ] Linear flow from 0→10 established
- [ ] Project metadata updated correctly

#### Structure Verification
- [ ] All 11 phase folders present
- [ ] YAML files in opportunity root
- [ ] Source documents in 0-source folder
- [ ] Folder naming follows convention

## Best Practices

1. **Always Work Backwards:** Start with the target and identify what's truly needed
2. **Preserve Original Formatting:** Never alter source documents during conversion
3. **Document Everything:** Maintain clear traceability from source to target
4. **Validate Dependencies:** Ensure each phase builds logically on previous phases
5. **Regular Reviews:** Periodically review document selection for completeness

## Common Pitfalls

- **Over-Selection:** Including too many documents that don't support the target
- **Under-Selection:** Missing critical supporting materials
- **Format Alterations:** Changing source document content during conversion
- **Poor Naming:** Using unclear or inconsistent naming conventions
- **Broken Dependencies:** Selecting documents without considering phase relationships

## Success Metrics

- Clear path from source materials (Phase 0) to target deliverable (Phase 9)
- All target requirements supported by appropriate documentation
- Efficient workflow with minimal unnecessary work
- High-quality deliverables that meet client expectations
