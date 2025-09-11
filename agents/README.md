# Agents Directory

## Overview
This directory contains the intelligent agents that power the document selection and generation system.

## Structure

### `/analyzers/`
Agents that analyze source materials:
- Source analyzer: Extracts information from client materials
- Gap analyzer: Identifies what's missing between source and target
- ROI analyzer: Calculates business value metrics

### `/generators/`
Agents that generate documents:
- Document generator: Creates standardized documents from templates
- Content generator: Populates templates with analyzed data
- Contract generator: Assembles final deliverables

### `/validators/`
Agents that validate quality:
- Citation validator: Ensures proper sourcing
- Quality validator: Checks against standards
- Completeness validator: Verifies all requirements met

## Implementation
Agents will be implemented using the agentic transformation principles from the best-practices directory.
