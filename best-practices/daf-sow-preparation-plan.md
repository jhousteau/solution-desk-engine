# DAF SOW Preparation Plan - [CLIENT] [PROJECT]

## Overview
This plan guides the creation of a Google Deal Acceleration Fund (DAF) Statement of Work for the [CLIENT] [PROJECT] POV, following 2025 DAF requirements.

## Prerequisites Check
- [ ] Confirm customer name: **[CLIENT]**
- [ ] Confirm partner name: **Capgemini**
- [ ] Confirm project name: **F&I AI Assistant Proof of Concept**
- [ ] Confirm engagement type: **Pilot/Proof of Concept**
- [ ] Confirm funding amount: **$50,000 USD**
- [ ] Confirm timeline: **8 weeks**
- [ ] Confirm effective date: **[7+ business days from submission]**

## Document Preparation Steps

### Phase 1: Information Gathering
**Files to Read:**
- `/opportunity/0-source/content/client-auto-f-n-i-agent-pov.md` - Core POV requirements
- `/opportunity/0-source/content/sales-finance-process-deal-flow.md` - Business process
- `/opportunity/1-research/14-market-financial-analysis.md` - Financial data
- `/opportunity/5-architecture/2-pov-architecture.md` - Technical architecture

**Key Information to Extract:**
1. Business case metrics (60,000 cash customers, $1.2M-$3.6M revenue)
2. Technical architecture (3-agent system, Vertex AI Agent Engine)
3. Success criteria (60%+ attachment rate, <2 sec response)
4. Deliverables (Chat UI, Agent system, Report)

### Phase 2: SOW Section Completion

#### Section 1: Cover Page
**Template Location:** Lines 28-40 of `c-daf-psf-sow-template-y25.md`
**Required Changes:**
- Replace `[PARTNER NAME]` with `Capgemini`
- Replace `[CUSTOMER NAME]` with `[CLIENT]`
- Replace `[Google Cloud Workload Implementation]` with `F&I AI Assistant Proof of Concept`
- Add current date
- Add author name

#### Section 2: Executive Summary
**Template Location:** Lines 130-142
**Required Content:**
- Business value: Transform F&I engagement for 60,000 annual cash customers
- Technical outcome: Multi-agent AI system using Vertex AI Agent Engine
- ROI projection: 24:1 ($1.2M revenue vs $50K investment)
- Implementation: 8-week POV in [CLIENT]'s Google Cloud environment

**Key Phrases to Include:**
```markdown
Capgemini offers [CLIENT] support in implementing an AI-powered F&I Assistant
to transform how cash customers engage with finance and insurance products. This proof of
concept will demonstrate a multi-agent system capable of generating $1.2M-$3.6M in annual
revenue from currently unserved cash customers.
```

#### Section 3: Requirements and Solution
**Template Location:** Section 2 (Lines 144-150)
**Required Elements:**
1. **Architecture Diagram** (MANDATORY)
   - Source: `/opportunity/5-architecture/2-pov-architecture.md`
   - Include: 3-agent system, Vertex AI Agent Engine, Cloud Run, Firestore
   - Format: Mermaid diagram converted to image

2. **Business Requirements:**
   - Engage 60,000 annual cash customers
   - Increase F&I attachment from <5% to 10-30%
   - Handle objections with personalized recommendations

3. **Technical Requirements:**
   - Multi-agent orchestration
   - Real-time pricing calculations
   - Conversation management
   - Synthetic data integration

#### Section 4: Activities and Deliverables
**Template Location:** Section 3
**Structure:**
```markdown
### Phase 1: Design & Setup (Weeks 1-2)
- Activity: Architecture design and environment setup
- Activity: Synthetic data preparation
- Deliverable: Approved architecture document

### Phase 2: Agent Development (Weeks 3-5)
- Activity: Master Agent implementation
- Activity: Recommendation Agent development
- Activity: Calculator Agent creation
- Deliverable: Functional multi-agent system

### Phase 3: Integration & Testing (Weeks 6-7)
- Activity: UI integration
- Activity: End-to-end testing
- Deliverable: Working POV with chat interface

### Phase 4: Validation & Documentation (Week 8)
- Activity: Stakeholder demos
- Activity: Performance validation
- Deliverable: Final report and recommendations
```

#### Section 5: Timeline
**Template Location:** Section 3.7
**Format:**
```markdown
| Week | Phase | Activities | Deliverables |
|------|-------|------------|--------------|
| 1-2 | Design & Setup | Architecture, Environment, Data | Architecture Document |
| 3-5 | Development | Agent Implementation | Multi-agent System |
| 6-7 | Integration | UI, Testing | Working POV |
| 8 | Validation | Demos, Documentation | Final Report |
```

#### Section 6: Roles & Responsibilities
**Template Location:** Section 5
**RACI Matrix Required:**
```markdown
| Task | Capgemini | [CLIENT] | Google |
|------|-----------|---------|---------|
| Project Management | R,A | C,I | I |
| Architecture Design | R,A | C,I | C |
| Agent Development | R,A | I | - |
| Data Preparation | R,A | C,I | - |
| Testing & Validation | R | A,C | I |
| Business Case Validation | C | R,A | I |
```

#### Section 7: Success Criteria
**Template Location:** Part of Section 3
**Measurable Criteria:**
1. Working multi-agent system in Google Cloud
2. 60%+ F&I product recommendation acceptance in demos
3. <2 second response time for recommendations
4. Successful handling of 5+ objection scenarios
5. Positive stakeholder feedback (80%+ approval)
6. Clear path to production implementation

#### Section 8: Pricing
**Template Location:** Section 6
**Required Elements:**
```markdown
| Component | Cost | Paid By |
|-----------|------|---------|
| Professional Services | $50,000 | Google Cloud (DAF)* |
| Google Cloud Consumption | TBD | [CLIENT] |
| Partner Co-investment | $0 | Capgemini |
| Customer Investment | $0 | [CLIENT] |

*Subject to formal DAF approval by Google Cloud
```

#### Section 9: Business Case Appendix
**NOT shared with customer**
**Required Content:**
1. **ROI Calculation:**
   - Investment: $50,000
   - Year 1 Revenue: $1,200,000 (conservative)
   - ROI: 24:1
   - Payback: <2 months

2. **ARR Projection:**
   - Year 1: $250,000 (infrastructure + licenses)
   - Year 2: $500,000 (expansion)
   - Year 3: $1,000,000 (full production)

3. **Strategic Impact:**
   - First-mover advantage in AI-powered F&I
   - Competitive differentiation
   - Foundation for multi-channel expansion

### Phase 3: Document Assembly

#### Step 1: Create Base Document
```bash
# Copy template
cp opportunity/0-source/google/c-daf-psf-sow-template-y25.md opportunity/9-contract/client-daf-sow-draft.md

# Remove all [DELETE] sections
# Remove all -ToBeDeleted- content
# Replace all [ToBeChanged] markers
```

#### Step 2: Insert Architecture Diagram
1. Extract Mermaid diagram from `/opportunity/5-architecture/2-pov-architecture.md`
2. Convert to PNG using Mermaid CLI or online tool
3. Insert in Section 2.1

#### Step 3: Validate Against Checklist
**Use:** `opportunity/0-source/google/c-daf-psf-sow-checklist-y25-daf-sow-checklist.md`
- [ ] Cover page complete
- [ ] Executive summary includes business value
- [ ] Architecture diagram present
- [ ] Activities and deliverables itemized
- [ ] Timeline with future dates
- [ ] RACI matrix included
- [ ] Success criteria measurable
- [ ] Pricing shows all parties
- [ ] ROI justification >20:1

### Phase 4: Review and Submission

#### Internal Review
1. Technical accuracy check
2. Financial calculations verification
3. Compliance with DAF requirements
4. Legal/contract terms review

#### Submission Process
1. Convert to Google Docs format
2. Set sharing permissions (comment enabled)
3. Send to appropriate regional approver:
   - NORTHAM: psfapproversNORTHAM@google.com
4. Include Fair Market Value template

## Critical Success Factors

### Must-Have Elements
1. **Architecture diagram** - Visual proof of workload
2. **Fixed price** - $50,000 total
3. **Measurable success criteria** - Quantifiable outcomes
4. **20:1 ROI justification** - Clear business case
5. **Future dates** - No retroactive funding

### Common Pitfalls to Avoid
- Don't mention specific CCAI/Agent Assist requirements (not needed for 2025)
- Don't include Google roles in RACI matrix
- Don't share ROI appendix with customer
- Don't sign before Google approval
- Don't use time/effort caps in activities

## Quick Reference Commands

### File Locations
```bash
# Templates
TEMPLATE="opportunity/0-source/google/c-daf-psf-sow-template-y25.md"
CHECKLIST="opportunity/0-source/google/c-daf-psf-sow-checklist-y25-daf-sow-checklist.md"
OVERVIEW="opportunity/0-source/google/c-daf-psf-sow-checklist-y25-partner-funds-overview.md"

# Source Documents
POV_SPEC="opportunity/0-source/content/client-auto-f-n-i-agent-pov.md"
PROCESS="opportunity/0-source/content/sales-finance-process-deal-flow.md"
FINANCE="opportunity/1-research/14-market-financial-analysis.md"
ARCHITECTURE="opportunity/5-architecture/2-pov-architecture.md"

# Output
OUTPUT="opportunity/9-contract/client-daf-sow-draft.md"
```

### Text Replacements
```bash
# Key replacements for template
[PARTNER NAME] → Capgemini
[CUSTOMER NAME] → [CLIENT]
[WORKLOAD] → F&I AI Assistant
[STARTING_DATE] → [TBD - 7+ days from submission]
[PARTNER_COUNTRY] → United States
[CUSTOMER_COUNTRY] → United States
[PARTNER_TENANT/CUSTOMER_ORGANIZATION] → [CLIENT] Google Cloud Organization
```

## Next Steps
1. Begin Phase 1: Information Gathering
2. Create draft using template
3. Insert architecture diagram
4. Complete all sections per checklist
5. Review and validate
6. Submit for approval

---
*This plan is optimized for Claude Code to efficiently process and execute each step with clear file paths and specific instructions.*
