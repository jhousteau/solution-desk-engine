# Agent Instructions for Research Framework

## Quick Start Guide

This repository contains a systematic research framework for conducting complex technical projects. Follow these instructions to use it effectively.

## 1. Framework Overview

The framework consists of 11 phases (0-10) that progress sequentially:
- **0-source**: Original client materials
- **1-research**: Research and discovery
- **2-requirements**: Requirements analysis
- **3-analysis**: Stakeholder analysis
- **4-business-case**: Business justification
- **5-architecture**: Technical design
- **6-solution-design**: Detailed specifications
- **7-implementation-plan**: Execution roadmap
- **8-proposal**: Client presentations
- **9-contract**: Legal documents
- **10-audit**: Quality assurance

## 2. Getting Started

### Step 1: Review Configuration Files
```bash
# Check which documents are enabled
cat research-documents-config.yaml

# Check current progress
cat research-documents-status.yaml
```

### Step 2: Review CLAUDE.md
Read `CLAUDE.md` for detailed framework principles and best practices.

### Step 3: Check Existing Work
```bash
# See what's already been done
ls -la research/
```

## 3. Working on a Phase

### For Each Phase:
1. **Check the phase directory**: `ls research/[phase-number]-[name]/`
2. **Review existing documents**: Use Read tool on existing files
3. **Check config for required documents**: Look at `research-documents-config.yaml`
4. **Create missing documents**: Only if `create: true` in config
5. **Update status**: Mark completed in `research-documents-status.yaml`

### Document Creation Process:
1. **Always base on source materials** in `0-source/`
2. **Extract only explicit requirements** - no assumptions
3. **Document assumptions separately** if you must make any
4. **Maintain traceability** to source documents
5. **Follow templates** in existing documents
6. **Use numbered prefixes** - Name documents with logical order prefixes (1-, 2-, 3-) to aid user navigation
7. **Prioritize system integration analysis** - Create comprehensive system-integration-analysis.md early in requirements phase
8. **Capture market/financial data early** - Create market-financial-analysis.md in research phase with proper citations

## 4. Key Commands

### Check Phase Status:
```bash
# See what exists in a phase
ls -la research/3-analysis/

# Count documents in a phase
ls research/3-analysis/*.md | wc -l
```

### Read Source Materials:
```bash
# Always start with source materials
cat research/0-source/README.md
```

### Update Configuration:
- Use Edit tool on `research-documents-config.yaml` to enable/disable documents
- Use Edit tool on `research-documents-status.yaml` to track progress

## 5. Quality Checks

Before moving to next phase:
- ✓ All enabled documents created
- ✓ All documents reference source materials
- ✓ Status YAML updated
- ✓ No unexplained assumptions
- ✓ Clear traceability maintained

## 6. Common Tasks

### Creating a New Document:
1. Check if enabled in config: `create: true`
2. Use the description field for guidance
3. Reference source materials
4. Follow existing document patterns
5. Update status when complete

### Reviewing Progress:
1. Check `research-documents-status.yaml`
2. Look at `overall_statistics` section
3. Review `directory_statistics` for each phase
4. Check `next_priorities` for what to do next

## 7. Important Rules

1. **Sequential Development**: Complete phases in order
2. **Source-Based**: Everything traces to source materials
3. **No Assumptions**: Document explicitly or ask user
4. **Config-Driven**: Only create documents marked `create: true`
5. **Status Tracking**: Always update status YAML

## 8. Getting Help

- **Framework Details**: See `research-directory-recreation-guide.md`
- **Best Practices**: See `CLAUDE.md`
- **Templates**: Check `templates/` directory
- **Examples**: Look at completed documents in phases 0-4

## Remember

This framework ensures systematic, traceable, and comprehensive project documentation. Follow it carefully to deliver high-quality results.
