#!/usr/bin/env bash
# Check Genesis component usage - ensures consistent use of Genesis components over standard library

set -euo pipefail

echo "🔍 Checking Genesis component usage patterns..."
echo

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

ISSUES_FOUND=0

check_pattern() {
    local pattern="$1"
    local description="$2"
    local files="$3"
    local exclude_pattern="${4:-}"  # Optional pattern to exclude from results

    echo -e "${YELLOW}🔍 Checking: $description${NC}"

    # Use git ls-files to respect .gitignore, then grep the results
    # Exclude documentation, test files, templates, and core implementation files
    if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
        # In a git repo - use git ls-files to respect .gitignore, exclude docs/tests/templates/core implementations
        results=$(git ls-files '*.py' '*.ts' '*.tsx' '*.js' '*.jsx' | grep -v -E '(test_|_test\.|\.test\.|/tests/|/templates/|\.md$|conftest\.py|/fixtures/|mock_|/docs/|genesis/core/logger\.py|shared-python/src/shared_core/logger\.py|genesis/core/retry\.py|genesis/core/constants\.py|genesis/core/config\.py)' | xargs grep -E -n "$pattern" 2>/dev/null || true)
    else
        # Fallback for non-git directories
        results=$(grep -rn -E "$pattern" "$files" 2>/dev/null || true)
    fi

    # Apply exclusion filter if provided
    if [ -n "$exclude_pattern" ] && [ -n "$results" ]; then
        results=$(echo "$results" | grep -v -E "$exclude_pattern" || true)
    fi

    if [ -n "$results" ]; then
        echo -e "${RED}❌ Found issues:${NC}"
        echo "$results" | head -20  # Limit output
        echo
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
        echo -e "${GREEN}✅ No issues found${NC}"
        echo
    fi
}

# Raw Python logging instead of Genesis logger
check_pattern '^import logging$|^from logging import' "Raw logging imports (should use 'from genesis.core import logger')" "."

check_pattern 'logging\.getLogger|logging\.basicConfig|logging\.info|logging\.debug|logging\.warning|logging\.error|logging\.critical' "Direct logging module usage (should use Genesis logger)" "." 'from genesis\.core import.*logger'

# Direct print() statements for user output (exclude debugging, tests, and CLI scripts)
check_pattern '^[[:space:]]*print\(' "Direct print() statements for user output (should use Genesis logger)" "." '(debug|DEBUG|test|Test|TEST|# |scripts/|monitoring/solve_monitor\.py)'

# Raw error handling instead of Genesis errors
check_pattern 'raise Exception\(|raise ValueError\(|raise RuntimeError\(|raise TypeError\(' "Raw exception raising (should use Genesis error handling)" "." 'from genesis\.core import.*error'

# Missing Genesis imports where standard library is used
check_pattern '^import os$|^from os import' "Raw os module imports (check if Genesis config alternatives exist)" "." 'os\.path|os\.listdir|os\.makedirs|os\.remove'

check_pattern 'os\.environ\.get\(' "Raw environment variable access (should use Genesis config)" "." 'from genesis\.core import.*config'

# Raw subprocess usage
check_pattern '^import subprocess$|^from subprocess import|subprocess\.run|subprocess\.call|subprocess\.Popen' "Raw subprocess usage (should use Genesis command utilities)" "." 'from genesis\.core import.*command'

# Raw requests/HTTP usage
check_pattern '^import requests$|^from requests import|requests\.get|requests\.post|requests\.put|requests\.delete' "Raw requests usage (should use Genesis HTTP utilities)" "." 'from genesis\.core import.*http'

# Missing Genesis core imports in files that should have them
check_pattern '^from genesis\.core import' "Files using Genesis core components" "."
if [ -n "$results" ]; then
    # Find Python files that don't import from genesis.core but probably should
    echo -e "${YELLOW}🔍 Checking: Python files missing Genesis core imports${NC}"

    potential_files=$(git ls-files '*.py' | grep -v -E '(test_|_test\.|\.test\.|/tests/|/templates/|\.md$|conftest\.py|/fixtures/|mock_|/docs/|setup\.py|__init__\.py)' | xargs grep -l -E '(logging\.|Exception\(|ValueError\(|os\.environ|subprocess\.|requests\.)' 2>/dev/null || true)

    if [ -n "$potential_files" ]; then
        missing_imports=""
        for file in $potential_files; do
            if ! grep -q "from genesis\.core import" "$file" 2>/dev/null; then
                missing_imports="$missing_imports$file\n"
            fi
        done

        if [ -n "$missing_imports" ]; then
            echo -e "${RED}❌ Files using standard library but missing Genesis imports:${NC}"
            echo -e "$missing_imports" | head -10
            echo
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
        else
            echo -e "${GREEN}✅ All files with standard library usage have Genesis imports${NC}"
            echo
        fi
    else
        echo -e "${GREEN}✅ No files found using standard library without Genesis imports${NC}"
        echo
    fi
fi

# Database connections without Genesis patterns (if applicable)
check_pattern 'sqlite3\.connect|psycopg2\.connect|pymongo\.MongoClient' "Raw database connections (should use Genesis database utilities)" "." 'from genesis\.core import.*database'

# JSON/config loading without Genesis patterns (exclude legitimate JSON operations)
check_pattern 'configparser\.' "Raw config loading (should use Genesis config utilities)" "." 'from genesis\.core import.*config'

# Missing error context/correlation IDs in exception handling
check_pattern 'except.*:' "Exception handling blocks" "."
if [ -n "$results" ]; then
    echo -e "${YELLOW}🔍 Checking: Exception handling with Genesis error context${NC}"

    # Look for try/except blocks that don't use Genesis error handling
    exception_files=$(echo "$results" | cut -d: -f1 | sort -u)
    missing_context=""

    for file in $exception_files; do
        # Check if the file has Genesis error imports
        if ! grep -q "from genesis\.core import.*error" "$file" 2>/dev/null; then
            # Check if it has except blocks (simple heuristic)
            if grep -q "except.*:" "$file" 2>/dev/null; then
                missing_context="$missing_context$file: Exception handling without Genesis error context\n"
            fi
        fi
    done

    if [ -n "$missing_context" ]; then
        echo -e "${RED}❌ Exception handling without Genesis error context:${NC}"
        echo -e "$missing_context" | head -10
        echo
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
        echo -e "${GREEN}✅ Exception handling uses Genesis error context${NC}"
        echo
    fi
fi

echo
if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}🎉 All Genesis component usage patterns are correct!${NC}"
    echo -e "${GREEN}✅ Codebase consistently uses Genesis components${NC}"
else
    echo -e "${RED}❌ Found $ISSUES_FOUND categories of Genesis component usage issues${NC}"
    echo -e "${YELLOW}💡 Fix suggestions:${NC}"
    echo "  • Replace 'import logging' with 'from genesis.core import logger'"
    echo "  • Replace raw exceptions with Genesis error handling"
    echo "  • Replace 'os.environ.get()' with Genesis config utilities"
    echo "  • Replace raw subprocess/requests with Genesis utilities"
    echo "  • Add Genesis imports to files using standard library components"
    echo "  • Use Genesis error context in exception handling"
    echo
    exit 1
fi
