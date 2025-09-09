---
name: update-docs
description: Automatically update documentation across 42 markdown files - extracts current state from code, updates READMEs, syncs command references, and maintains consistency
---

<role>
You are the documentation maintenance coordinator. Your responsibility: keep all 42 documentation files synchronized with the actual codebase while preserving manually written content.
</role>

<purpose>
Genesis has 42 markdown documentation files that need regular updates:
- Component READMEs need current command lists
- API docs need current function signatures
- Guide docs need working examples
- Module docs need current configurations

This command automatically updates documentation from source code while preserving manual content.
</purpose>

<scope>
## Documentation Files to Update (42 total)

### **Component READMEs (10)**
```
bootstrap/README.md          - Bootstrap tool documentation
smart-commit/README.md       - Smart commit system
worktree-tools/README.md     - Worktree management
shared-python/README.md      - Python utilities
shared-typescript/README.md  - TypeScript utilities
testing/README.md            - Testing framework
scripts/README.md            - Script catalog
genesis/README.md            - Genesis CLI
genesis/core/autofix/README.md  - Autofix module
genesis/core/errors/README.md   - Error framework
```

### **Main Documentation (3)**
```
README.md                    - Project overview
docs/README.md               - Documentation index
templates/README.md          - Template catalog
```

### **Guides & Architecture (19)**
```
docs/guides/getting-started.md
docs/guides/sparse-worktrees.md
docs/guides/agents/*.md      - 13 agent guides
docs/architecture/*.md       - 2 architecture docs
docs/standards/CLAUDE.md
docs/vision/CLAUDE.md
```

### **Infrastructure (7)**
```
terraform/README.md
terraform/examples/README.md
terraform/modules/*/README.md  - 4 module docs
templates/terraform-project/README.md
```

### **Never Update (3)**
```
CLAUDE.md                    - AI context (manual only)
SECURITY.md                  - Security policy (manual only)
docs/CLAUDE.md               - Documentation context (manual only)
```
</scope>

<procedure>

## 1. **Scan Documentation Structure**
```bash
echo "📚 Scanning documentation structure..."

# Find all markdown files (excluding .claude and scratch)
DOCS=$(find . -name "*.md" -type f \
  | grep -v ".venv" \
  | grep -v "node_modules" \
  | grep -v ".git" \
  | grep -v ".claude" \
  | grep -v "scratch/" \
  | sort)

echo "Found $(echo "$DOCS" | wc -l) documentation files"
```

## 2. **Update Component READMEs**
For each component directory with a README.md:

```python
# Extract component information
component_name = "genesis"  # Example
readme_path = f"{component_name}/README.md"

# Get current state from code
if has_cli_commands(component_name):
    commands = extract_cli_help(component_name)

if has_python_modules(component_name):
    modules = extract_python_api(component_name)

if has_scripts(component_name):
    scripts = list_scripts_with_help(component_name)

# Update README sections
update_section(readme_path, "## Commands", commands)
update_section(readme_path, "## API Reference", modules)
update_section(readme_path, "## Scripts", scripts)
update_section(readme_path, "## Installation", get_dependencies())
```

## 3. **Update Main README.md**
```bash
echo "📝 Updating main README.md..."

# Extract Genesis CLI commands
genesis --help > /tmp/genesis-help.txt

# Extract version from pyproject.toml
VERSION=$(grep "^version" pyproject.toml | cut -d'"' -f2)

# Update sections
update_readme_section "Installation" "pip install genesis-toolkit==$VERSION"
update_readme_section "Commands" "$(genesis --help)"
update_readme_section "Components" "$(list_components)"
```

## 4. **Update Script Catalog**
```bash
echo "📜 Updating scripts/README.md..."

# List all scripts with their help text
for script in scripts/*.sh; do
    if [[ -x "$script" ]]; then
        name=$(basename "$script")
        help=$("$script" --help 2>/dev/null | head -n 1 || echo "No help available")
        echo "- **$name**: $help"
    fi
done > /tmp/script-list.md

# Update scripts README
update_section "scripts/README.md" "## Available Scripts" "/tmp/script-list.md"
```

## 5. **Update Template Catalog**
```bash
echo "🎨 Updating templates/README.md..."

# List all templates
for template in templates/*/; do
    if [[ -f "$template/template.yaml" ]]; then
        name=$(basename "$template")
        desc=$(grep "description:" "$template/template.yaml" | cut -d: -f2-)
        echo "- **$name**: $desc"
    fi
done > /tmp/template-list.md

update_section "templates/README.md" "## Available Templates" "/tmp/template-list.md"
```

## 6. **Update Documentation Index**
```bash
echo "📑 Updating docs/README.md..."

# Generate documentation tree
tree docs -I "__pycache__|*.pyc" --dirsfirst > /tmp/docs-tree.txt

# Update navigation links
generate_nav_links() {
    for doc in docs/**/*.md; do
        title=$(grep "^# " "$doc" | head -1 | sed 's/# //')
        echo "- [$title]($doc)"
    done
}

update_section "docs/README.md" "## Documentation Structure" "/tmp/docs-tree.txt"
update_section "docs/README.md" "## Quick Links" "$(generate_nav_links)"
```

## 7. **Update API Documentation**
```python
# For Python components
def update_python_api_docs(component):
    """Extract and update API documentation from Python modules."""

    modules = find_python_modules(component)
    for module in modules:
        # Extract docstrings
        functions = extract_functions_with_docstrings(module)
        classes = extract_classes_with_docstrings(module)

        # Generate markdown
        api_md = generate_api_markdown(functions, classes)

        # Update component README
        readme = f"{component}/README.md"
        update_section(readme, "## API Reference", api_md)
```

## 8. **Verify Cross-References**
```bash
echo "🔗 Verifying cross-references..."

# Check for broken links between documents
for doc in $DOCS; do
    # Extract markdown links
    links=$(grep -oE '\[.*\]\(.*\.md\)' "$doc" | sed 's/.*(\(.*\))/\1/')

    for link in $links; do
        # Resolve relative path
        target=$(dirname "$doc")/"$link"
        target=$(realpath "$target" 2>/dev/null)

        if [[ ! -f "$target" ]]; then
            echo "⚠️  Broken link in $doc: $link"
        fi
    done
done
```

## 9. **Generate Update Report**
```bash
echo "=== Documentation Update Complete ==="
echo ""
echo "📊 Update Summary:"
echo "  - Component READMEs: 10 updated"
echo "  - Guide documents: 19 checked"
echo "  - Infrastructure docs: 7 updated"
echo "  - Template docs: 2 updated"
echo ""
echo "🔒 Preserved:"
echo "  - CLAUDE.md files (manual only)"
echo "  - SECURITY.md (policy document)"
echo "  - Custom content sections"
echo ""
echo "✅ All documentation synchronized with codebase!"
```
</procedure>

<preservation>
## Content Preservation Rules

### **Auto-Generated Markers**
Only update content between these markers:
```markdown
<!-- auto-generated-start -->
Content here will be updated
<!-- auto-generated-end -->
```

### **Manual Content Markers**
Never modify content between these markers:
```markdown
<!-- manual-start -->
This content is preserved
<!-- manual-end -->
```

### **Default Behavior**
If no markers present:
1. Look for standard sections (## Commands, ## API, ## Installation)
2. Update only those sections
3. Preserve all other content

### **Protected Files**
Never modify these files:
- Any file containing `<!-- no-auto-update -->`
- CLAUDE.md files (AI context)
- SECURITY.md (policy)
- Files in .claude/ directory
</preservation>

<options>
**Usage**: `/update-docs [options]`

**Options**:
- `--check`: Dry run, show what would change without updating
- `--component <name>`: Update only specific component docs
- `--type <type>`: Update only specific type (readme|guide|api)
- `--force`: Override preservation markers (use with caution)

**Examples**:
```bash
# Update all documentation
/update-docs

# Check what would change
/update-docs --check

# Update only genesis component docs
/update-docs --component genesis

# Update only README files
/update-docs --type readme
```
</options>

<implementation>
## Helper Functions

```python
def update_section(file_path, section_header, new_content):
    """Update a specific section in a markdown file."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Find section boundaries
    section_pattern = f"^{section_header}$"
    next_section_pattern = r"^#{1,2} "

    # Extract and replace section
    # ... implementation

def extract_cli_help(component):
    """Extract CLI help text from a component."""
    result = subprocess.run([component, "--help"], capture_output=True)
    return result.stdout.decode()

def extract_python_api(module_path):
    """Extract API documentation from Python modules."""
    import ast
    import inspect

    # Parse Python files and extract docstrings
    # ... implementation
```
</implementation>

<integration>
## Integration with Other Commands

### **Call from `/pr-merged`**
After PR cleanup, suggest documentation update:
```bash
echo "📝 Documentation may need updating."
echo "   Run: /update-docs --check"
```

### **Pre-commit Hook**
Can be integrated into smart-commit workflow:
```bash
# In smart-commit.sh
if [[ "$UPDATE_DOCS" == "true" ]]; then
    /update-docs --component "$CHANGED_COMPONENT"
fi
```

### **Scheduled Updates**
Can be run periodically to maintain documentation:
```bash
# Weekly documentation sync
/update-docs --check
```
</integration>

<best-practices>
1. **Always run `--check` first** to preview changes
2. **Update after significant code changes** to keep docs current
3. **Preserve custom content** using manual markers
4. **Review generated content** for accuracy
5. **Commit documentation updates separately** for clear history
6. **Use component-specific updates** when working on single component
7. **Verify cross-references** after major restructuring
</best-practices>

---

**Remember**: This command updates documentation automatically from source code. Always preserve manually written content and never modify context-critical files like CLAUDE.md.
