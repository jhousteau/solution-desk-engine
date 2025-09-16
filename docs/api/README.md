# API Reference

## Core Framework Components

### Document Export (`export.document_exporter`)

**DocumentExporter**: Multi-format document export system
- `ExportFormat`: Enum for supported formats (MARKDOWN, PDF, DOCX, HTML)
- `ExportResult`: Result wrapper for export operations
- Export methods for various output formats with fallback strategies

### SOW Generation (`sow.sow_generator`)

**SOWGenerator**: Statement of Work document generator
- `SOWContext`: Data class for SOW template rendering context
- Google Docs template integration via DocxTemplate
- Support for customer, project, and contractor information

**SOWContext Fields:**
- `customer_name`: Client company name
- `project_name`: Project identifier
- `contractor_name`: Default "Capgemini"
- `contractor_poc_name/email`: Contractor point of contact
- `google_poc_name/email`: Google Cloud contact information
- `sow_end_date`: Project end date (default: "December 31, 2025")
- `max_total_cost`: Maximum project cost
- `special_terms`: Additional contract terms

### Google Drive Integration (`integrations.google_drive`)

**GoogleDriveClient**: Google Drive API client for document management
- OAuth2 authentication flow with credentials management
- Document download and upload capabilities
- File sharing and permission management
- Support for Google Docs template processing

**Key Methods:**
- `authenticate()`: Handle OAuth2 authentication flow
- `download_file()`: Download files from Google Drive
- `upload_file()`: Upload files to Google Drive
- `share_file()`: Manage file sharing permissions

### Quality Validation (`quality.validator`)

**DocumentValidator**: Document quality assurance system
- Citation enforcement for financial data
- Professional tone and style validation
- Template completeness checking
- Structure and formatting validation

### Project Configuration (`config.project_config`)

**ProjectConfiguration**: YAML-based project settings management
- Project metadata and configuration storage
- Phase-specific settings and preferences
- Template selection and customization options

## CLI Interface (`cli.py`)

**Main Commands:**
- `status`: Show framework status and version information
- `sow generate`: Generate SOW document from Google Docs template
- `sow validate-template`: Validate Google Docs template structure

## Usage Examples

### SOW Generation
```python
from solution_desk_engine.sow.sow_generator import SOWGenerator, SOWContext

# Create context
context = SOWContext(
    customer_name="Example Corp",
    project_name="Cloud Migration",
    contractor_poc_name="John Doe",
    contractor_poc_email="john.doe@capgemini.com"
)

# Generate SOW
generator = SOWGenerator()
result = generator.generate_from_template(template_id, context)
```

### Document Export
```python
from solution_desk_engine.export.document_exporter import DocumentExporter, ExportFormat

exporter = DocumentExporter()
result = exporter.export(
    input_path="document.md",
    output_format=ExportFormat.PDF,
    output_path="output.pdf"
)
```

### Google Drive Integration
```python
from solution_desk_engine.integrations.google_drive import GoogleDriveClient

client = GoogleDriveClient()
client.authenticate()
file_content = client.download_file(file_id)
```

## Framework Architecture

The API follows a modular architecture with clear separation of concerns:

1. **Core Framework** (`framework/`): 11-phase methodology implementation
2. **Document Management**: Export, validation, and quality assurance
3. **Integrations**: External service connections (Google Drive, etc.)
4. **CLI Interface**: User-facing commands and interactions
5. **Configuration**: Project-specific settings and customization

All components follow strict typing with MyPy compliance and comprehensive error handling.
