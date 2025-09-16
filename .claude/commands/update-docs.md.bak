---
name: update-docs
description: Update project documentation - extracts current state from code, updates READMEs, syncs command references, and maintains consistency
---

<role>
You are the documentation maintenance coordinator. Your responsibility: keep documentation files synchronized with the actual codebase while preserving manually written content.
</role>

<purpose>
This command automatically updates documentation from source code while preserving manual content. It analyzes your project structure and updates documentation based on common patterns.
</purpose>

<scope>
## Documentation Files to Discover and Update

The command will automatically discover and update documentation based on your project structure:

### **Component READMEs**
- Look for `README.md` files in subdirectories (src/, lib/, components/, modules/, etc.)
- Update with current command lists, API references, and usage examples

### **Main Documentation**
- `README.md` - Project overview and installation instructions
- `docs/README.md` - Documentation index (if exists)
- API documentation files in docs/ directory

### **Specialized Documentation**
- Script catalogs (`scripts/README.md`)
- Template documentation (`templates/README.md`)
- Configuration guides
- Architecture documentation (`docs/architecture/`)
- User guides (`docs/guides/`)

### **Protected Files (Never Auto-Update)**
- `CLAUDE.md` - AI context (manual only)
- `SECURITY.md` - Security policy (manual only)
- `LICENSE` - License file (manual only)
- Any files marked with `<!-- MANUAL-ONLY -->` comment
</scope>

<procedure>

## 1. **Scan Project Structure**
```bash
echo "📚 Scanning project documentation structure..."

# Find all markdown files (excluding common ignore patterns)
DOCS=$(find . -name "*.md" -type f \
  | grep -v ".venv\|venv\|node_modules\|.git\|.claude\|scratch\|__pycache__\|.next\|dist\|build" \
  | sort)

echo "Found $(echo "$DOCS" | wc -l) documentation files"

# Identify project type
PROJECT_TYPE="unknown"
[[ -f "package.json" ]] && PROJECT_TYPE="javascript"
[[ -f "pyproject.toml" || -f "setup.py" ]] && PROJECT_TYPE="python"
[[ -f "Cargo.toml" ]] && PROJECT_TYPE="rust"
[[ -f "go.mod" ]] && PROJECT_TYPE="go"
[[ -f "pom.xml" ]] && PROJECT_TYPE="java"

echo "Detected project type: $PROJECT_TYPE"
```

## 2. **Update Component READMEs**
For each directory with a README.md:

```python
import os
import subprocess
from pathlib import Path

def update_component_readme(component_path):
    """Update README.md for a component directory."""
    readme_path = component_path / "README.md"

    if not readme_path.exists():
        return

    print(f"📝 Updating {readme_path}")

    # Extract information based on project type
    commands = []
    api_docs = []
    scripts = []

    # For Python projects
    if any(Path(component_path).glob("*.py")):
        api_docs = extract_python_docstrings(component_path)
        commands = extract_cli_commands(component_path)

    # For JavaScript/TypeScript projects
    if any(Path(component_path).glob("*.js")) or any(Path(component_path).glob("*.ts")):
        api_docs = extract_js_exports(component_path)

    # For executable scripts
    scripts = list_executable_scripts(component_path)

    # Update README sections
    update_readme_section(readme_path, "## Commands", commands)
    update_readme_section(readme_path, "## API Reference", api_docs)
    update_readme_section(readme_path, "## Scripts", scripts)

# Process all component directories
for component_dir in find_component_directories():
    update_component_readme(Path(component_dir))
```

## 3. **Update Main README.md**
```python
# Extract project information
project_name = get_project_name()  # From package.json, pyproject.toml, etc.
version = get_project_version()
description = get_project_description()

# Update main README sections
update_readme_section("README.md", "## Installation", generate_install_instructions())
update_readme_section("README.md", "## Usage", extract_main_usage_examples())
update_readme_section("README.md", "## Commands", extract_cli_help())
update_readme_section("README.md", "## Components", list_project_components())

print(f"✅ Updated main README.md for {project_name} v{version}")
```

## 4. **Update Script Catalogs**
```bash
if [[ -d "scripts" ]]; then
    echo "📜 Updating script documentation..."

    # Generate script list with descriptions
    (
        echo "# Scripts"
        echo ""
        echo "Available scripts in this project:"
        echo ""

        for script in scripts/*; do
            if [[ -x "$script" ]]; then
                name=$(basename "$script")
                # Try to get help text or description
                help_text=$("$script" --help 2>/dev/null | head -n 1 ||
                           grep -m 1 "^# " "$script" 2>/dev/null | sed 's/^# //' ||
                           echo "Script: $name")
                echo "- **$name**: $help_text"
            fi
        done
    ) > /tmp/script-catalog.md

    update_readme_section "scripts/README.md" "## Available Scripts" "/tmp/script-catalog.md"
fi
```

## 5. **Update API Documentation**
```python
def update_api_docs():
    """Update API documentation based on project type."""

    # For Python projects - extract from docstrings
    if project_type == "python":
        modules = find_python_modules()
        for module in modules:
            api_doc = extract_python_api(module)
            if api_doc:
                doc_path = f"docs/api/{module.stem}.md"
                write_api_documentation(doc_path, api_doc)

    # For JavaScript/TypeScript - extract from JSDoc comments
    elif project_type == "javascript":
        update_js_api_docs()

    # For other languages - look for documented interfaces
    else:
        scan_for_documented_interfaces()

update_api_docs()
print("✅ API documentation updated")
```

## 6. **Update Configuration Documentation**
```python
# Look for configuration files and update their documentation
config_files = find_config_files()  # .env.example, config.yml, etc.

for config_file in config_files:
    if should_document_config(config_file):
        doc_path = f"docs/configuration/{Path(config_file).stem}.md"
        generate_config_documentation(config_file, doc_path)

print(f"✅ Updated documentation for {len(config_files)} configuration files")
```

## 7. **Verify Documentation Links**
```bash
echo "🔗 Checking documentation links..."

# Find all markdown files and check internal links
find . -name "*.md" -type f | while read -r file; do
    # Extract relative links and check if files exist
    grep -o '\](\.\/[^)]*\.md)' "$file" 2>/dev/null | while read -r link; do
        target=$(echo "$link" | sed 's/](.\/\(.*\))/\1/')
        if [[ ! -f "$(dirname "$file")/$target" ]]; then
            echo "⚠️  Broken link in $file: $target"
        fi
    done
done
```

## 8. **Generate Documentation Index**
```python
def generate_doc_index():
    """Generate a comprehensive documentation index."""

    all_docs = find_all_markdown_files()

    # Group by category
    categories = {
        "Getting Started": [],
        "API Reference": [],
        "Guides": [],
        "Configuration": [],
        "Components": [],
        "Architecture": []
    }

    for doc in all_docs:
        category = categorize_documentation(doc)
        if category in categories:
            categories[category].append(doc)

    # Generate index
    index_content = generate_index_markdown(categories)

    # Write to docs/README.md or create index
    if Path("docs").exists():
        write_file("docs/README.md", index_content)
    else:
        append_to_main_readme("## Documentation Index", index_content)

generate_doc_index()
print("✅ Documentation index generated")
```

</procedure>

<approach>
## Documentation Update Strategy

1. **Preserve Manual Content**: Never overwrite manually written sections unless they're clearly marked as auto-generated
2. **Extract from Source**: Pull current information directly from code, configs, and help text
3. **Follow Conventions**: Use consistent formatting and section structure across all docs
4. **Validate Links**: Ensure all internal links work and external links are accessible
5. **Version Awareness**: Update version references consistently across all documentation

## Protected Patterns
- Files with `<!-- MANUAL-ONLY -->` comment
- Sections between `<!-- MANUAL START -->` and `<!-- MANUAL END -->`
- CLAUDE.md, SECURITY.md, LICENSE files
- Any file marked as protected in project settings
</approach>

<examples>
## Example Usage Patterns

### For a Python CLI Project:
- Updates `README.md` with current CLI commands from `--help`
- Extracts API docs from docstrings in `src/` directory
- Updates component READMEs in subdirectories
- Catalogs scripts in `scripts/` directory

### For a JavaScript Library:
- Extracts API from exported functions and JSDoc
- Updates usage examples from test files
- Documents configuration options
- Updates build and deployment instructions

### For a Multi-Component Project:
- Discovers all components with README.md files
- Updates each component's documentation independently
- Maintains consistent structure across components
- Links components in main documentation index
</examples>
