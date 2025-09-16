# Proof of Concept Scope Document
## Franchise Lease Management System - Google Cloud AI Platform

**Version:** 2.0
**Date:** September 2025
**Duration:** 4-6 weeks
**Environment:** Capgemini GCP Innovation Lab - Customer Sandbox
**Purpose:** Demonstrate AI-powered lease analysis and conversational insights across 50 franchise lease documents

---

## 1. POC Objectives

### 1.1 Primary Goals
- Upload and analyze 50 franchise lease documents on Google Cloud Platform
- Demonstrate conversational search and analysis across the entire lease portfolio
- Extract and analyze 5 critical data elements with specialized AI processing
- Provide rent forecasting with graduated escalation calculations
- Enable natural language insights and comparative analysis across properties
- Establish Google Cloud architecture foundation for enterprise deployment

### 1.2 Success Criteria
- Process all 50 lease documents with Google Cloud Document AI
- Extract 5 key data elements with 90%+ accuracy:
  - Exclusion language clauses
  - Commencement dates
  - Rent rates and schedules
  - Graduated rent forecasting calculations
  - Expiration dates
- Enable conversational queries: "Show me leases with territorial exclusions"
- Generate rent forecasting projections for lease portfolio
- Reduce lease analysis time from days to minutes
- Demonstrate portfolio-wide comparative insights

---

## 2. POC Scope

### 2.1 In Scope - Core Features

#### 2.1.1 Google Cloud Document Processing Pipeline
**What We'll Build:**
- Google Cloud Storage bucket for 50 franchise lease documents
- Document AI OCR processing for text extraction
- Vertex AI custom models for specialized data extraction
- BigQuery warehouse for structured lease data
- Vector embeddings for semantic search capabilities
- Cloud Functions for processing orchestration

**What We'll Demonstrate:**
- Scalable document processing on Google Cloud
- Enterprise-grade OCR and AI extraction
- Cloud-native architecture for lease management

#### 2.1.2 Conversational Lease Analysis (Showcase Feature)
**What We'll Build:**
- Natural language conversational interface powered by Vertex AI
- Semantic search across all 50 lease documents using vector embeddings
- Portfolio-wide analytical queries:
  - "Show me all leases with exclusive territory clauses"
  - "Which properties have rent escalations above 3% annually?"
  - "Find leases expiring in 2026 with renewal options"
  - "Compare exclusion restrictions across all franchise locations"
- Contextual follow-up conversations
- Visual analytics and comparative insights

**What We'll Demonstrate:**
- Conversational lease portfolio analysis
- AI-powered insights across document collection
- Complex multi-document pattern recognition

#### 2.1.3 Specialized 5-Element Data Extraction
**What We'll Build:**
- **Exclusion Language Analysis**: AI-powered extraction and categorization of restrictive clauses, territorial exclusions, and use limitations
- **Commencement Date Extraction**: Precise date parsing with validation across multiple date formats and legal terminology
- **Rent Rate & Schedule Processing**: Comprehensive extraction of base rent, escalation clauses, and payment schedules
- **Graduated Rent Forecasting Engine**: Automated calculation of future rent projections based on escalation language (percentage increases, CPI adjustments, fixed step-ups)
- **Expiration Date Analytics**: Lease term analysis with renewal option identification and critical date mapping
- Confidence scoring and validation workflows
- Structured data output for BigQuery analytics

**What We'll Demonstrate:**
- Specialized AI models for complex lease language
- Automated financial forecasting and projections
- Portfolio-wide pattern analysis and insights

#### 2.1.4 Portfolio Analytics & Forecasting Dashboard
**What We'll Build:**
- Interactive rent forecasting visualizations across all 50 properties
- Portfolio-wide lease expiration timeline with renewal analysis
- Exclusion clause comparison matrix across franchise locations
- Financial projection models with graduated escalation scenarios
- Comparative analytics: rent rates, terms, and restrictions by location
- BigQuery-powered reporting with real-time insights

**What We'll Demonstrate:**
- Strategic lease portfolio management
- Data-driven renewal and expansion decisions
- Financial forecasting for franchise growth planning

#### 2.1.5 Intelligent Alerts & Insights
**What We'll Build:**
- Cloud Functions-based notification system
- Proactive alerts for rent escalations and lease expirations
- Portfolio anomaly detection (unusual exclusion clauses, rent terms)
- Automated insights: "3 leases have exclusive territory conflicts"
- Configurable notification preferences via Cloud Scheduler
- Integration-ready for email/Slack notifications

**What We'll Demonstrate:**
- Proactive lease portfolio monitoring
- AI-powered anomaly and pattern detection
- Automated business intelligence insights

### 2.2 Out of Scope - Not in POC

**Document Management:**
- Version control and amendment tracking
- Complex folder hierarchies
- Bulk upload capabilities
- Non-PDF file formats
- Document-level security

**Advanced Features:**
- Mobile applications
- Team collaboration features
- Task management
- User roles and permissions (single user POC)
- Accounting system integrations

**Analytics & Reporting:**
- Financial analytics and calculations
- ASC 842 compliance features
- Custom report builders
- Data export capabilities
- CAM reconciliation tools

**Enterprise Features:**
- Multi-tenant architecture
- API access
- Audit trails
- Two-factor authentication
- Backup and recovery

---

## 3. Technical Approach

### 3.1 Google Cloud Architecture (Capgemini Innovation Lab Sandbox)
- **Project Environment:** Dedicated GCP project within Capgemini Innovation Lab
- **Document Storage:** Google Cloud Storage bucket with 50 franchise lease PDFs
- **Document Processing:** Document AI for OCR and text extraction
- **AI/ML Platform:** Vertex AI for custom extraction models and embeddings
- **Data Warehouse:** BigQuery dataset for structured lease data and analytics
- **Search & Conversation:** Vertex AI Search with vector embeddings
- **Compute:** Cloud Functions for processing orchestration
- **Frontend:** Cloud Run container with React application for demonstrations
- **Security:** IAM roles and sandbox isolation for customer data protection
- **Monitoring:** Cloud Logging and Monitoring for POC performance tracking

### 3.2 Key Technologies to Validate
- **Hybrid PDF Processing**: Document AI OCR for both traditional text-based PDFs and image-scanned lease documents
- **Mixed Content Extraction**: Handling varying quality from clean text to scanned image pages
- Vertex AI custom models for 5-element extraction across different PDF formats
- Vector embedding quality for conversational search on mixed text sources
- Rent forecasting algorithm accuracy with graduated escalations from both text and OCR sources
- BigQuery performance for portfolio analytics queries
- End-to-end processing latency for 50-document corpus with mixed PDF types

---

## 4. POC Deliverables

### 4.1 Working Prototype (Innovation Lab Deployment)
- **Sandbox Environment:** Secure GCP project within Capgemini Innovation Lab
- **Web Application:** Cloud Run deployment accessible via browser for live demonstrations
- **Data Security:** Customer lease documents processed in isolated sandbox environment
- **Demo Dataset:** 50 franchise lease documents (anonymized/sanitized for demonstration)
- **Access Control:** Restricted access for POC stakeholders and demonstration purposes
- **Documentation:** Technical architecture guide and user demonstration scripts

### 4.2 Demonstrations
- **Demo 1: Hybrid PDF Processing**
  - Upload text-based and scanned image lease PDFs
  - Document AI OCR processing showcase
  - 5-element data extraction from mixed formats
  - Time: 7 minutes

- **Demo 2: Conversational Lease Analysis**
  - Natural language portfolio queries across 50 leases
  - "Show me all territorial exclusions" conversations
  - Cross-document pattern recognition and insights
  - Time: 10 minutes

- **Demo 3: Rent Forecasting & Portfolio Analytics**
  - Graduated rent projection calculations
  - Portfolio comparison and analytics dashboard
  - Financial forecasting with escalation scenarios
  - Time: 8 minutes

### 4.3 Analysis & Reports
- **Document Processing Performance**: OCR accuracy rates for text vs. scanned PDFs in sandbox environment
- **5-Element Extraction Analysis**: Precision metrics for exclusion language, dates, rent rates, forecasting, and terms
- **Conversational Search Effectiveness**: Query response accuracy and relevance scoring
- **Portfolio Analytics Validation**: Forecasting model accuracy and comparative insights
- **Innovation Lab Infrastructure Assessment**: GCP service utilization and performance metrics
- **Security & Compliance Report**: Data handling and sandbox isolation validation
- **Production Deployment Roadmap**: Migration path from Innovation Lab to enterprise environment
- **Cost Analysis**: Sandbox resource consumption and enterprise scalability projections
- **ROI Assessment**: Demonstrated time savings and business value quantification

---

## 5. User Scenarios for POC

### 5.1 Scenario 1: Portfolio-Wide Exclusion Analysis
**Current Process:** Days of manual review across 50 lease files
**POC Demo:** Minutes with conversational analysis
- User asks: "Show me all territorial exclusion clauses across our franchise locations"
- System analyzes all 50 leases and returns categorized exclusions
- Comparative analysis highlights conflicting or unusual restrictions
- Visual map showing territorial conflicts and opportunities

### 5.2 Scenario 2: Rent Forecasting for Budget Planning
**Current Process:** Manual spreadsheet calculations taking 8-16 hours
**POC Demo:** Instant automated forecasting
- System processes graduated rent escalations from all 50 leases
- Generates 5-year rent projection across entire portfolio
- Identifies locations with unusual escalation terms
- Provides budget planning insights for franchise growth

### 5.3 Scenario 3: Lease Expiration & Renewal Strategy
**Current Process:** 4-6 hours gathering expiration data
**POC Demo:** Conversational renewal analysis
- User asks: "Which leases expire in 2026 and have favorable renewal terms?"
- System provides instant analysis with renewal option details
- Cross-references rent rates and exclusion clauses for strategic decisions
- Generates renewal prioritization recommendations
