# Claude Code Hooks for Genesis

## Purpose
Claude Code hooks that enforce Genesis workflows by blocking bypass commands at the assistant level.

## Required Claude Code Settings

Add these to your Claude Code settings to block Genesis bypass commands:

### Command Execution Hooks
```json
{
  "hooks": {
    "bash_command_pre": [
      // Git command blocks
      {
        "pattern": "^git\\s+worktree\\s+(add|create)",
        "action": "block",
        "message": "❌ Use 'genesis worktree create' instead for AI-safe sparse worktrees"
      },
      {
        "pattern": "^git\\s+commit",
        "action": "block",
        "message": "❌ Use 'genesis commit' for quality-assured commits. Direct git commits (including --no-verify) bypass all quality gates."
      },

      // Testing blocks - use make commands
      {
        "pattern": "^pytest\\s+(?!.*--co)",
        "action": "block",
        "message": "❌ Use 'make test' for running tests"
      },
      {
        "pattern": "^python\\s+-m\\s+pytest",
        "action": "block",
        "message": "❌ Use 'make test' or 'make test-unit' for testing"
      },

      // Formatting/linting blocks - use make or genesis
      {
        "pattern": "^ruff\\s+(?!.*--check)",
        "action": "block",
        "message": "❌ Use 'make lint' or 'genesis autofix' for linting"
      },
      {
        "pattern": "^black\\s+",
        "action": "block",
        "message": "❌ Use 'make format' or 'genesis autofix' for formatting"
      },
      {
        "pattern": "^prettier\\s+",
        "action": "block",
        "message": "❌ Use 'make format' for formatting"
      },
      {
        "pattern": "^pre-commit\\s+run",
        "action": "block",
        "message": "❌ Use 'genesis commit' which handles pre-commit internally"
      },

      // Dependency management blocks - use make
      {
        "pattern": "^poetry\\s+install(?!.*-e)",
        "action": "block",
        "message": "❌ Use 'make setup' or 'make install-dev' for dependencies"
      },
      {
        "pattern": "^pip\\s+install\\s+(?!-e)",
        "action": "block",
        "message": "❌ Use 'make setup' or 'make install-prod' for dependencies"
      },
      {
        "pattern": "^npm\\s+install",
        "action": "block",
        "message": "❌ Use 'make setup' for dependencies"
      },

      // Docker blocks - use genesis container
      {
        "pattern": "^docker\\s+build",
        "action": "block",
        "message": "❌ Use 'genesis container build' for building containers"
      },
      {
        "pattern": "^docker\\s+run\\s+(?!.*--rm.*alpine|.*--rm.*bash)",
        "action": "block",
        "message": "❌ Use 'genesis container run' for running containers"
      },
      {
        "pattern": "^docker\\s+exec",
        "action": "block",
        "message": "❌ Use 'genesis container shell' for container access"
      },
      {
        "pattern": "^docker-compose\\s+up",
        "action": "block",
        "message": "❌ Use 'genesis container run' for container orchestration"
      },

      // Build/clean blocks - use make
      {
        "pattern": "^rm\\s+-rf\\s+(build|dist|__pycache__|node_modules)",
        "action": "block",
        "message": "❌ Use 'make clean' for cleanup operations"
      },
      {
        "pattern": "^python\\s+setup\\.py\\s+build",
        "action": "block",
        "message": "❌ Use 'make build' for building the project"
      }
    ]
  }
}
```

## What Gets Blocked

### Command Execution (Claude Code hooks)

#### Git Operations
- `git worktree add/create` → Use `genesis worktree create`
- `git commit` (ALL forms including --no-verify) → Use `genesis commit`

#### Testing
- `pytest` or `python -m pytest` → Use `make test` or `make test-unit`

#### Formatting/Linting
- `ruff` → Use `make lint` or `genesis autofix`
- `black` → Use `make format` or `genesis autofix`
- `prettier` → Use `make format`
- `pre-commit run` → Use `genesis commit`

#### Dependency Management
- `poetry install` → Use `make setup` or `make install-dev`
- `pip install` → Use `make setup` or `make install-prod`
- `npm install` → Use `make setup`

#### Container Operations
- `docker build` → Use `genesis container build`
- `docker run` → Use `genesis container run`
- `docker exec` → Use `genesis container shell`
- `docker-compose up` → Use `genesis container run`

#### Cleanup
- `rm -rf build/dist/etc` → Use `make clean`

### Code Analysis (Git hooks)
These patterns are detected in committed code:
- TODOs, FIXMEs, HACKs → Resolve before committing
- Hardcoded values → Use environment variables
- Direct commits to main → Use feature branches

## Why Claude Code Hooks?

Claude Code hooks prevent the AI assistant from executing bypass commands, while git hooks analyze code being committed. They work together:

1. **Claude Code hooks** = Prevent execution of wrong commands
2. **Git hooks** = Analyze code quality before commit

## Configuration

The hooks configuration above should be added to your Claude Code settings. This ensures:
- Claude can't run `git worktree add` directly
- Claude must use `genesis` commands
- Quality gates are always enforced
