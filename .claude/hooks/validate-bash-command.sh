#!/bin/bash
# PreToolUse hook to block bypass commands
# Exit code 0 = allow, Exit code 2 = block

set -euo pipefail

# Get the tool input from stdin
INPUT=$(cat)

# Extract the command from the Bash tool call
# Claude Code passes it as tool_input.command
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null || echo "")

if [[ -z "$COMMAND" ]]; then
    # Not a bash command, allow
    exit 0
fi

# Check for blocked git commands
if echo "$COMMAND" | grep -qE "^git\s+commit"; then
    echo "❌ Use 'genesis commit' for quality-assured commits. Direct git commits bypass all quality gates." >&2
    exit 2
fi

if echo "$COMMAND" | grep -qE "^git\s+worktree\s+(add|create|remove|prune|list)"; then
    echo "❌ Use 'genesis worktree' commands instead of direct git worktree operations" >&2
    echo "   - 'genesis worktree create' for AI-safe sparse worktrees" >&2
    echo "   - 'genesis worktree remove' for safe removal" >&2
    echo "   - 'genesis worktree list' to see existing worktrees" >&2
    exit 2
fi

# Block dangerous rm commands on worktrees
if echo "$COMMAND" | grep -qE "rm\s+.*(-rf|-fr).*worktrees"; then
    echo "❌ FORBIDDEN: Cannot delete worktrees directory directly. Use 'genesis worktree remove' for individual worktrees" >&2
    exit 2
fi

# Check for genesis clean command - ONLY block in SOLVE context
if echo "$COMMAND" | grep -qE "^genesis\s+clean"; then
    # Check multiple indicators of SOLVE context
    # 1. Check if we're in a solve-* directory (worktree or otherwise)
    if pwd | grep -qE "/(solve-[0-9]+|solve-[0-9]+-[a-z]+)($|/)"; then
        echo "❌ FORBIDDEN IN SOLVE: 'genesis clean' would destroy phase handoff files in .solve/ directory. The workspace must be preserved for VERIFY and ENHANCE phases." >&2
        exit 2
    fi

    # 2. Check if .solve directory exists (indicates active SOLVE pipeline)
    if [ -d ".solve" ] || [ -d "../.solve" ] || [ -d "../../.solve" ]; then
        echo "❌ FORBIDDEN: Active SOLVE pipeline detected (.solve directory present). Cannot clean during pipeline execution." >&2
        exit 2
    fi

    # 3. Check for SOLVE.md file (template file for agents)
    if [ -f "SOLVE.md" ] || [ -f "../SOLVE.md" ]; then
        echo "❌ FORBIDDEN: SOLVE.md detected. This appears to be a SOLVE workspace. Cleaning would break the pipeline." >&2
        exit 2
    fi

    # 4. Check for ISSUE.md file (another SOLVE indicator)
    if [ -f "ISSUE.md" ] && [ -f ".solve/context.md" ]; then
        echo "❌ FORBIDDEN: SOLVE pipeline files detected. Workspace must be preserved for phase handoffs." >&2
        exit 2
    fi
fi

# Check for blocked test commands
if echo "$COMMAND" | grep -qE "^pytest\s+(?!.*--co)"; then
    echo "❌ Use 'make test' for running tests" >&2
    exit 2
fi

# Check for blocked formatting commands
if echo "$COMMAND" | grep -qE "^(black|ruff|prettier)\s+"; then
    echo "❌ Use 'make format' or 'genesis autofix' for formatting" >&2
    exit 2
fi

# Check for blocked dependency commands
if echo "$COMMAND" | grep -qE "^(pip|poetry|npm)\s+install"; then
    echo "❌ Use 'make setup' for dependencies" >&2
    exit 2
fi

# Check for blocked docker commands
if echo "$COMMAND" | grep -qE "^docker\s+(build|run|exec)"; then
    echo "❌ Use 'genesis container' commands for Docker operations" >&2
    exit 2
fi

# Allow all other commands
exit 0
