# Google Docs Conversion Setup Guide

This guide shows you how to set up and use the `convert_to_googledocs.py` script to convert your markdown documents to Google Docs.

## Prerequisites

1. **Python Dependencies**
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

2. **Existing Scripts**
   - `convert_to_docx.py` must be in the same directory
   - All dependencies for DOCX conversion must be installed

## Google API Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Name it something like "[CLIENT] Documentation Converter"

### Step 2: Enable APIs

1. In Google Cloud Console, go to **APIs & Services > Library**
2. Enable these APIs:
   - **Google Docs API**
   - **Google Drive API**

### Step 3: Create Credentials

1. Go to **APIs & Services > Credentials**
2. Click **+ CREATE CREDENTIALS > OAuth client ID**
3. If prompted, configure OAuth consent screen:
   - Choose "External" for user type
   - Fill in app name: "[CLIENT] Doc Converter"
   - Add your email as developer contact
   - Save and continue through scopes and test users
4. Create OAuth client ID:
   - Application type: **Desktop application**
   - Name: "[CLIENT] Doc Converter"
5. Download the JSON file
6. Save it as `credentials/credentials.json` in your project directory

### Step 4: Directory Structure

Create this structure in your project:
```
your-project/
├── convert_to_googledocs.py
├── convert_to_docx.py
├── credentials/
│   └── credentials.json        # Downloaded from Google Cloud
└── opportunity/                # Your markdown files
    ├── 1-research/
    ├── 2-requirements/
    └── ...
```

## Usage

### Basic Conversion

Convert all markdown files to Google Docs:
```bash
python convert_to_googledocs.py --verbose
```

### Process Specific Phase

Convert only specific phase:
```bash
python convert_to_googledocs.py --phase 9-contract --verbose
```

### Process Single File

Convert single file:
```bash
python convert_to_googledocs.py --file opportunity/1-research/5-solution-patterns.md --verbose
```

### Create Master Index

Generate a master index document with links to all created docs:
```bash
python convert_to_googledocs.py --verbose --create-index
```

## First Run Authentication

1. Run the script for the first time
2. It will open your browser for Google authentication
3. Sign in with your Google account
4. Grant permissions to the application
5. The script will save authentication tokens for future use

## Features

### Automatic Organization
- Creates folder structure in Google Drive: "[CLIENT] F&I Documentation"
- Organizes documents by phase (Research & Discovery, Requirements Analysis, etc.)
- Maintains document titles with phase prefixes

### Document Conversion
- Uses your existing DOCX conversion logic
- Uploads DOCX files to Google Drive
- Automatically converts to Google Docs format
- Preserves formatting and styling

### Metadata Tracking
- Logs all conversions with Google Doc links
- Creates JSON index files with document metadata
- Tracks failed conversions for troubleshooting

### Master Index
- Optional master index document
- Contains links to all generated documents
- Organized by phase for easy navigation

## Output

### Google Drive Structure
```
[CLIENT] F&I Documentation/
├── Research & Discovery/
│   └── [1-RESEARCH] Solution Patterns
├── Requirements Analysis/
│   └── [2-REQUIREMENTS] Functional Requirements
└── Contract Documents/
    └── [9-CONTRACT] Statement of Work
```

### Local Metadata
```
output_googledocs/
└── _metadata/
    ├── googledocs-conversion-log.json    # Full conversion log
    ├── googledocs-index.json             # Document index
    └── failed-conversions.json           # Error tracking
```

## Troubleshooting

### Common Issues

**"Credentials file not found"**
- Ensure `credentials/credentials.json` exists
- Check the file path in the error message

**"API not enabled"**
- Enable Google Docs API and Google Drive API in Google Cloud Console

**"Authentication failed"**
- Delete `credentials/token.json` and re-authenticate
- Check your Google Cloud project settings

**"Rate limit exceeded"**
- Reduce parallel workers: `--parallel 1`
- Add delays between uploads if needed

### Rate Limits

Google APIs have rate limits:
- **Default parallel workers**: 2 (reduced from 4 for API limits)
- **Quota limits**: 300 requests per minute per user
- **Daily limits**: 20,000 requests per day

## Security Notes

- Keep `credentials/credentials.json` secure
- Add `credentials/` to your `.gitignore`
- The `token.json` file contains your access tokens
- Only grant necessary permissions during OAuth flow

## Command Line Options

```bash
python convert_to_googledocs.py [OPTIONS]

Options:
  --credentials PATH    Path to credentials file (default: credentials/credentials.json)
  --phase PHASE        Process only specific phase (e.g., 9-contract)
  --file FILE          Process only specific file
  --parallel N         Number of parallel conversions (default: 2)
  --verbose, -v        Verbose output
  --create-index       Create master index document with links
  --help              Show help message
```

## Example Output

```bash
$ python convert_to_googledocs.py --verbose --create-index

Converting [CLIENT] F&I documentation to Google Docs...
Parallel workers: 2
Google API services initialized successfully
Processing all phases...
Found existing folder: [CLIENT] F&I Documentation
Created new folder: Research & Discovery
Successfully uploaded: [1-RESEARCH] Solution Patterns (ID: 1a2b3c4d5e6f...)
Successfully uploaded: [2-REQUIREMENTS] Functional Requirements (ID: 2b3c4d5e6f7g...)
Creating master index document...
Created master index: https://docs.google.com/document/d/INDEX_DOC_ID/edit

Conversion Results:
Total files: 15
Successful: 15
Failed: 0

Created 15 Google Docs:
  - [1-RESEARCH] Solution Patterns: https://docs.google.com/document/d/DOC_ID_1/edit
  - [2-REQUIREMENTS] Functional Requirements: https://docs.google.com/document/d/DOC_ID_2/edit
  ...

Master Index: https://docs.google.com/document/d/INDEX_DOC_ID/edit

Metadata saved to: output_googledocs/_metadata
```
