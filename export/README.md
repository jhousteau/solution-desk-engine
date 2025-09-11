# Export Directory

## Overview
Complete document generation and export infrastructure for converting opportunity documents to final deliverables in multiple formats.

## Structure

### Main Components
- **`export_docs.py`** - Main export orchestrator and CLI interface
- **`README-googledocs-setup.md`** - Google Docs API setup guide
- **`docx/`** - DOCX output directory
- **`_metadata/`** - Export metadata and settings

### `/scripts/`
Specialized conversion processors:
- **`branding_manager.py`** - Branding and styling management
- **`convert_to_docx.py`** - Microsoft Word document conversion
- **`convert_to_googledocs.py`** - Google Docs API export
- **`convert_to_pdf.py`** - PDF generation with styling
- **`sow_template_processor.py`** - Statement of Work processing

## Usage

### Command Line Interface
```bash
# Convert specific document to PDF
python export/export_docs.py pdf --file path/to/document.md --verbose

# Convert entire phase to DOCX
python export/export_docs.py docx --phase 4-business-case --verbose

# Export to Google Docs with index
python export/export_docs.py googledocs --verbose --create-index
```

### Available Formats
- **`pdf`** - High-quality PDF using weasyprint
- **`docx`** - Microsoft Word compatibility via python-docx
- **`googledocs`** - Google Docs API-based export with formatting

### Common Options
- **`--verbose`** - Show detailed processing information
- **`--file <path>`** - Convert specific file
- **`--phase <phase-name>`** - Convert entire phase
- **`--create-index`** - Generate document index

## Supported Features

### PDF Generation
- Professional styling and formatting
- Table of contents generation
- Custom branding integration
- High-quality typography using weasyprint

### DOCX Conversion
- Full Microsoft Word compatibility
- Template-based styling
- Table and image support
- Metadata preservation

### Google Docs Export
- Direct API integration
- Collaborative editing ready
- Formatted text preservation
- Automatic sharing capabilities

## Setup Requirements

### Dependencies
Install required packages via poetry:
```bash
poetry install
```

Key dependencies include:
- **weasyprint** - PDF generation
- **python-docx** - Word document processing
- **mistune** - Markdown parsing
- **google-api-python-client** - Google Docs integration

### Google Docs Setup
For Google Docs export, see `README-googledocs-setup.md` for complete API setup instructions.

## File Organization

Export outputs are organized by format:
```
export/
├── export_docs.py           # Main CLI
├── docx/                   # DOCX outputs
├── _metadata/              # Export settings
└── scripts/                # Format processors
    ├── branding_manager.py
    ├── convert_to_docx.py
    ├── convert_to_googledocs.py
    ├── convert_to_pdf.py
    └── sow_template_processor.py
```

## Integration

This export system integrates with:
- **Templates system** - Uses document templates
- **Opportunities workflow** - Exports from phase directories
- **Quality standards** - Applies citation and formatting rules
- **Branding system** - Consistent visual identity
