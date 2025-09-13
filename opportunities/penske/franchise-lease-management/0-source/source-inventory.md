# Source Document Inventory
**Project:** Penske Franchise Lease Management POC
**Phase:** 0-source
**Date:** September 12, 2025

## Executive Summary

This inventory catalogs two primary source documents that establish the foundation for the Penske Franchise Lease Management POC. The POC document defines requirements and success criteria, while the Google SOW template provides the delivery framework. Together, these documents enable mapping from customer needs to structured workshop deliverables.

---

## Document Analysis

### Document 1: franchise-lease-management-poc.md

**Document Type:** Proof of Concept Scope Document
**Version:** 1.0
**Purpose:** Define POC boundaries, objectives, and technical approach for AI-powered franchise lease management

#### Key Sections Breakdown:

**1. POC Objectives (Section 1.1)**
- Demonstrate AI-powered document search across lease portfolios
- Prove automated extraction of critical dates and key terms
- Show immediate time savings in document retrieval
- Validate user experience for non-technical franchise operators
- Establish technical architecture foundation

**2. Success Criteria (Section 1.2)**
- Process 25-50 actual lease documents
- Achieve 85%+ automated extraction accuracy for critical dates
- Answer natural language queries with 90%+ accuracy
- Reduce document search time from hours to seconds
- Achieve positive feedback from 3-5 test users

**3. Core Features (Section 2.1)**

*Document Management:*
- Single-tenant repository supporting 25-50 documents
- PDF upload capability (up to 25MB per file)
- Simple folder structure (Location → Document Type)
- Basic metadata tagging and document preview

*AI-Powered Search (Showcase Feature):*
- Natural language search interface
- Full-text search across all documents
- Pre-defined smart queries for common lease questions
- Search result highlighting and session history

*Automated Data Extraction:*
- Extract lease dates, rent amounts, renewal options
- Extract notice requirements, parties, and addresses
- Confidence scoring and manual override capability

*Critical Date Dashboard:*
- Calendar view of upcoming dates
- 90-day obligation list with urgency indicators
- Visual timeline of lease expirations

*Basic Notifications:*
- Email alerts for critical dates
- Configurable lead times (30, 60, 90, 180 days)
- Daily digest options

**4. Technical Approach (Section 3)**
- Frontend: React-based web application
- Backend: Node.js/Python API server
- Database: PostgreSQL for structured data
- Storage: AWS S3 or Google Cloud Storage
- AI/Search: OpenAI API for natural language processing
- PDF Processing: Apache PDFBox or similar

**5. User Scenarios with Time Savings**
- New Lease Onboarding: 2-4 hours → 2 minutes
- Renewal Decision Research: 1-2 hours → 30 seconds
- CAM Audit Preparation: 8-16 hours → 5 minutes

**6. Deliverables Framework**
- Working prototype with live demo environment
- Performance metrics and accuracy assessments
- User feedback summary and ROI projections
- Technical feasibility assessment and implementation roadmap

---

### Document 2: google-sow-template-2025.md

**Document Type:** Statement of Work Template
**Purpose:** Contractual framework for Google Cloud Workshop delivery
**End Date:** December 31, 2025

#### Service Structure Analysis:

**Service Categories (Section 4.1A)**
The SOW supports 8 use case categories:
1. Infrastructure Modernization
2. Databases
3. App Modernization
4. Data Analytics
5. Security
6. Artificial Intelligence (Predictive AI, Gen AI with RAG, Media, External/Internal Search, CCAI Services)
7. Industry Solutions

**Three Service Types:**

**1. Introduction Workshop ($10,000)**
- Remote or on-site delivery
- Prerequisites: SPOC identification, stakeholder alignment, documentation review
- Discovery: Technical pain-points, business outcomes, use case identification
- Demonstration: Google Cloud overview and solution capabilities
- Architecture: High-level future state design
- Deliverables: Solution documentation and post-engagement feedback

**2. Business Value Assessment ($20,000)**
- Builds on Introduction Workshop
- Prerequisites: Business and technical stakeholder involvement
- Assessment: Current state processes, systems, and gap analysis
- Business Value: ROI modeling and value proposition development
- Deliverables: Prioritized use cases, technical architecture, business case

**3. Rapid POV ($25,000)**
- Prerequisites: Success criteria definition and next steps planning
- Build: Lower-level environment solution implementation
- Test: Solution validation against success criteria
- Demo: Customer demonstration and production alignment
- Deliverables: Technical architecture and demonstration documentation

**Key Requirements Across All Services:**
- >10x ROI criteria mandatory
- Stage 0/1 opportunity classification
- Google approval required before commitment
- Solution tagging required

#### Payment Structure:
- Introduction Workshop: $10,000
- Business Value Assessment: $20,000
- Rapid POV: $25,000
- Maximum total cost cap with tax inclusion
- One service type per customer limitation

---

## Critical Mappings and Alignments

### POC → Introduction Workshop Alignment

**Discovery Tasks Mapping:**
- POC pain points (manual processes, scattered files) → Workshop discovery of technical challenges
- POC business outcomes (time savings, efficiency) → Workshop business outcome identification
- POC use cases (search, extraction, dashboard) → Workshop use case prioritization

**Demonstration Requirements:**
- POC technical approach → Workshop Google Cloud capabilities demo
- POC AI-powered search → Workshop AI/ML services demonstration
- POC architecture → Workshop future state architecture design

### POC → Business Value Assessment Alignment

**Value Proposition Mapping:**
- POC time savings metrics → BVA ROI calculation framework
- New lease onboarding (2-4 hrs → 2 min) → 98% efficiency improvement
- Document search (hours → seconds) → Massive productivity gains
- CAM audit prep (8-16 hrs → 5 min) → 95% time reduction

**Business Case Elements:**
- POC success criteria (85% accuracy, 90% query success) → BVA performance targets
- POC user feedback targets → BVA adoption metrics
- POC technical architecture → BVA implementation roadmap

### POC → Rapid POV Alignment

**Build Requirements:**
- POC core features → POV solution components
- POC technical stack → POV implementation approach
- POC 25-50 document capacity → POV scale parameters

**Success Criteria Translation:**
- POC extraction accuracy (85%) → POV validation metrics
- POC query accuracy (90%) → POV performance benchmarks
- POC user satisfaction → POV customer acceptance criteria

---

## Key Insights for Phase Planning

### 1. **Clear Value Proposition Established**
- POC provides quantifiable time savings that exceed >10x ROI requirement
- Three user scenarios demonstrate concrete business impact
- Technical feasibility validated through defined architecture

### 2. **Google Cloud Alignment Opportunities**
- AI/ML services (OpenAI → Vertex AI migration path)
- Storage services (S3 → Google Cloud Storage)
- Database services (PostgreSQL → Cloud SQL)
- Search capabilities (custom → Vertex AI Search)

### 3. **Workshop Progression Path**
- Introduction Workshop: Demonstrate POC concept alignment with Google Cloud
- Business Value Assessment: Quantify time savings as ROI model
- Rapid POV: Implement core POC features using Google Cloud services

### 4. **Risk Mitigation Factors**
- POC scope is well-defined and achievable
- Technical approach is proven and scalable
- Success metrics are measurable and realistic
- User scenarios provide clear validation criteria

---

## Dependencies for Subsequent Phases

### Phase 1 (Research) Requirements:
- **Problem Statement Research:** POC pain points and manual processes
- **Solution Patterns Research:** Google Cloud AI/ML architecture patterns

### Phase 2 (Requirements) Requirements:
- **Scope Definition:** POC in/out of scope boundaries
- **Functional Requirements:** POC core features and capabilities

### Phase 3 (Analysis) Requirements:
- **Stakeholder Map:** SOW SPOC requirements and POC user personas
- **Current State Analysis:** POC current process documentation
- **Gap Analysis:** Manual vs. automated process comparison

### Phase 4 (Business Case) Requirements:
- **ROI Analysis:** POC time savings quantification
- **Value Proposition:** POC business impact modeling

### Phase 5 (Architecture) Requirements:
- **Architecture Overview:** POC technical approach translated to Google Cloud
- **Technology Stack:** Google Cloud services mapping

---

## Quality Gates and Validation

### Completeness Checklist:
- [x] POC objectives clearly defined
- [x] Success criteria quantified
- [x] Technical approach documented
- [x] SOW service types understood
- [x] Pricing structure confirmed
- [x] Alignment mappings established

### Traceability Requirements:
- All Phase 1+ documents must reference source materials
- POC requirements must map to specific SOW deliverables
- Business case must trace to POC value propositions
- Technical design must align with POC architecture

### Success Validation:
- Final SOW must deliver POC objectives through Google Cloud Workshop framework
- All POC success criteria must be achievable through workshop deliverables
- ROI calculations must exceed >10x requirement using POC metrics

---

**Document Status:** Complete
**Next Phase:** 1-research (problem-statement-research.md, solution-patterns.md)
**Approval:** Ready for Phase 1 initiation
