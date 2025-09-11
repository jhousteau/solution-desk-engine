#!/bin/bash
# Genesis File Organization Check
# Ensures proper project structure and prevents file clutter

set -euo pipefail

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Project root (should be current directory for bootstrapped projects)
PROJECT_ROOT="$(pwd)"

# Function to log messages
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}" >&2
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" >&2
}

log_error() {
    echo -e "${RED}❌ $1${NC}" >&2
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}" >&2
}

# Check for misplaced files in root directory
check_root_clutter() {
    local violations=0

    # Allowed files in root
    local allowed_root_files=(
        "README.md" "CLAUDE.md" "CHANGELOG.md" "LICENSE" "SECURITY.md"
        "Makefile" "pyproject.toml" "package.json" "requirements.txt"
        ".gitignore" ".envrc" ".env.example" ".python-version"
        "Dockerfile" "docker-compose.yml" "docker-compose.yaml"
        "main.tf" "variables.tf" "outputs.tf" "versions.tf"
    )

    # Allowed directories in root
    local allowed_root_dirs=(
        "src" "tests" "docs" "scripts" "config" "scratch"
        ".git" ".github" ".vscode" ".devcontainer" ".claude"
        ".venv" "venv" "__pycache__" ".pytest_cache" ".mypy_cache"
        "build" "dist" "htmlcov" "node_modules" ".next"
    )

    # Check for disallowed files in root
    for file in "$PROJECT_ROOT"/*; do
        if [[ ! -e "$file" ]]; then continue; fi

        filename=$(basename "$file")

        if [[ -f "$file" ]]; then
            # Check if file is allowed
            local allowed=false
            for allowed_file in "${allowed_root_files[@]}"; do
                if [[ "$filename" == "$allowed_file" ]]; then
                    allowed=true
                    break
                fi
            done

            # Special patterns
            if [[ "$filename" =~ ^\.env ]]; then allowed=true; fi
            if [[ "$filename" =~ \.md$ ]] && [[ "$filename" =~ ^(README|CHANGELOG|CONTRIBUTING|SECURITY|LICENSE)$ ]]; then allowed=true; fi

            if [[ "$allowed" == "false" ]]; then
                log_error "File '$filename' should not be in root directory"

                # Suggest proper location
                case "$filename" in
                    *.py) log_info "  → Move to: src/" ;;
                    *.sh) log_info "  → Move to: scripts/" ;;
                    *.md) log_info "  → Move to: docs/" ;;
                    *.json|*.yaml|*.yml|*.toml)
                        if [[ ! "$filename" =~ ^(package\.json|pyproject\.toml|docker-compose\.ya?ml)$ ]]; then
                            log_info "  → Move to: config/"
                        fi
                        ;;
                    test_*.py|*_test.py|conftest.py) log_info "  → Move to: tests/" ;;
                    *) log_info "  → Consider organizing into appropriate subdirectory" ;;
                esac

                violations=$((violations + 1))
            fi

        elif [[ -d "$file" ]]; then
            # Check if directory is allowed
            local allowed=false
            for allowed_dir in "${allowed_root_dirs[@]}"; do
                if [[ "$filename" == "$allowed_dir" ]]; then
                    allowed=true
                    break
                fi
            done

            if [[ "$allowed" == "false" ]]; then
                log_error "Directory '$filename' may not follow Genesis structure"
                log_info "  → Standard directories: src/, tests/, docs/, scripts/, config/"
                violations=$((violations + 1))
            fi
        fi
    done

    return $violations
}

# Check src/ directory structure
check_src_structure() {
    local violations=0

    if [[ ! -d "$PROJECT_ROOT/src" ]]; then
        log_warning "No src/ directory found - this is unusual for Python projects"
        return 0
    fi

    # Check for Python files in wrong locations
    find "$PROJECT_ROOT" -name "*.py" -not -path "*/src/*" -not -path "*/tests/*" -not -path "*/.venv/*" -not -path "*/venv/*" -not -path "*/__pycache__/*" -not -path "*/.pytest_cache/*" | while read -r pyfile; do
        if [[ "$pyfile" =~ (setup\.py|conftest\.py)$ ]]; then
            continue  # These are allowed in root
        fi

        log_error "Python file outside src/: $(realpath --relative-to="$PROJECT_ROOT" "$pyfile")"
        log_info "  → Move to: src/"
        violations=$((violations + 1))
    done

    return $violations
}

# Check for test files in wrong locations
check_test_structure() {
    local violations=0

    # Find test files outside tests/
    find "$PROJECT_ROOT" -name "test_*.py" -o -name "*_test.py" | grep -v "/tests/" | while read -r testfile; do
        log_error "Test file outside tests/: $(realpath --relative-to="$PROJECT_ROOT" "$testfile")"
        log_info "  → Move to: tests/"
        violations=$((violations + 1))
    done

    return $violations
}

# Check for script files in wrong locations
check_script_structure() {
    local violations=0

    # Find shell scripts outside scripts/
    find "$PROJECT_ROOT" -name "*.sh" -not -path "*/scripts/*" -not -path "*/.git/*" -not -path "*/.venv/*" -not -path "*/venv/*" -not -path "*/.claude/*" | while read -r scriptfile; do
        log_error "Shell script outside scripts/: $(realpath --relative-to="$PROJECT_ROOT" "$scriptfile")"
        log_info "  → Move to: scripts/"
        violations=$((violations + 1))
    done

    return $violations
}

# Main execution
main() {
    log_info "Checking Genesis project file organization..."

    local total_violations=0

    # Run all checks
    check_root_clutter
    total_violations=$((total_violations + $?))

    check_src_structure
    total_violations=$((total_violations + $?))

    check_test_structure
    total_violations=$((total_violations + $?))

    check_script_structure
    total_violations=$((total_violations + $?))

    # Report results
    if [[ $total_violations -eq 0 ]]; then
        log_success "File organization follows Genesis standards"
        exit 0
    else
        log_error "Found $total_violations file organization violations"
        log_info "Run 'make clean' to fix common issues automatically"
        exit 1
    fi
}

# Only run main if script is executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
