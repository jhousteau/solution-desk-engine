# Genesis Developer Guide

**Version:** 1.7.2
**Last Updated:** 2025-10-12

## What is Genesis?

Genesis is a lean development toolkit that enforces AI-safe project practices, quality gates, and automated workflows. It provides CLI commands for testing, formatting, smart commits, and worktree management while keeping your codebase focused and maintainable.

**Core Principles:**
- AI safety through file count limits and sparse worktrees
- Quality gates before every commit
- Minimal complexity, maximum value
- Template-driven project consistency

## Installation

Install the latest Genesis CLI from GitHub releases:

```bash
# Using curl (recommended)
curl -sSL https://raw.githubusercontent.com/jhousteau/genesis/main/.genesis/scripts/setup/install-genesis.sh | bash

# Or if you have a Makefile with install-latest target
make install-latest
```

Verify installation:
```bash
genesis --version
# Genesis CLI v1.7.2
```

## Quick Start

### 1. Initialize Your Project

If starting a new project:
```bash
genesis bootstrap my-project --type python-api
cd my-project
```

If adding Genesis to existing project:
```bash
cd my-existing-project
genesis init
genesis setup
```

### 2. Your First Commit

```bash
# Make some changes
echo "# My Project" > README.md

# Test and format
genesis test
genesis format

# Smart commit with quality gates
genesis commit -m "feat: initial commit"
```

### 3. Keep Templates Updated

```bash
# Sync latest templates from Genesis
genesis sync

# Check project health
genesis status
```

## CLI Commands Reference

All commands support both `-h` and `--help` for detailed usage.

### Development Commands

**`genesis setup`**
Run initial project setup - installs dependencies and configures environment.
```bash
genesis setup
```

**`genesis test [args...]`**
Run tests with pytest. Pass additional pytest flags as needed.
```bash
genesis test                    # Run all tests
genesis test -k test_specific   # Run specific test
genesis test -v --tb=short      # Verbose with short traceback
genesis test -h                 # Show help
```

**`genesis format`**
Format code with black and ruff (respects .gitignore).
```bash
genesis format
```

**`genesis lint`**
Lint code with ruff (respects .gitignore).
```bash
genesis lint
```

**`genesis typecheck`**
Type check with mypy (checks source directories).
```bash
genesis typecheck
```

**`genesis quality`**
Run all quality checks: format + lint + typecheck.
```bash
genesis quality
```

### Workflow Commands

**`genesis commit`**
Smart commit with quality gates and pre-commit hooks.
```bash
genesis commit -m "feat: add user authentication"
genesis commit -m "fix: resolve login bug" -d "Details about the fix"
genesis commit --help
```

**`genesis status`**
Check Genesis project health and component status.
```bash
genesis status
genesis status -v    # Verbose output
```

**`genesis clean`**
Clean workspace - removes old worktrees and build artifacts.
```bash
genesis clean --all          # Clean everything
genesis clean --worktrees    # Just worktrees
genesis clean --artifacts    # Just build artifacts
```

**`genesis sync`**
Update project support files from Genesis templates.
```bash
genesis sync                 # Sync with confirmation
genesis sync --preview       # Preview changes
genesis sync --force         # Force overwrite
genesis sync --dry-run       # Show what would change
```

**`genesis autofix`**
Run autofix (formatting, linting) without committing.
```bash
genesis autofix
genesis autofix --dry-run
genesis autofix --stages 3
```

### Worktree Management (AI-Safe Development)

**`genesis worktree create`**
Create AI-safe sparse worktree focused on specific paths.
```bash
genesis worktree create feature-name --focus src/
genesis worktree create bugfix --focus src/auth/ tests/auth/
genesis worktree create docs --focus docs/ --max-files 30
```

**`genesis worktree list`**
List existing worktrees.
```bash
genesis worktree list
```

**`genesis worktree info`**
Show information about a specific worktree.
```bash
genesis worktree info feature-name
```

**`genesis worktree remove`**
Remove a worktree by name.
```bash
genesis worktree remove feature-name
```

### Git Workflow Helpers

**`genesis branch`**
Manage Git branches.
```bash
genesis branch list              # List branches
genesis branch list --all        # List all (including remote)
genesis branch create feat-x     # Create branch
genesis branch create feat-x -s  # Create and switch
genesis branch delete old-feat   # Delete branch
```

**`genesis checkout`**
Switch to a different branch or restore files.
```bash
genesis checkout main
genesis checkout -f develop  # Force checkout
```

**`genesis pull`**
Pull updates from remote repository.
```bash
genesis pull
genesis pull --rebase
```

**`genesis reset`**
Reset current branch to a specific commit.
```bash
genesis reset HEAD~1          # Soft reset (default)
genesis reset HEAD~1 --mixed  # Mixed reset
genesis reset HEAD~1 --hard --confirm-hard  # Hard reset (requires confirmation)
```

### Advanced Commands

**`genesis container`**
Manage Docker containers using docker-compose.
```bash
genesis container build      # Build image
genesis container run        # Start container
genesis container shell      # Open shell
genesis container logs       # View logs
genesis container stop       # Stop container
```

**`genesis environment`**
Manage multi-environment configuration.
```bash
genesis environment current      # Show current environment
genesis environment switch prod  # Switch to production
genesis environment config KEY   # Show config value
```

**`genesis init`**
Initialize Genesis sync configuration for current project.
```bash
genesis init
genesis init --type python-api --name my-project
```

**`genesis migrate`**
Migrate existing Genesis project to new format.
```bash
genesis migrate
genesis migrate --dry-run
```

**`genesis bootstrap`**
Create new project with Genesis patterns.
```bash
genesis bootstrap my-project --type python-api
genesis bootstrap my-cli --type cli-tool
genesis bootstrap my-service --type typescript-service
```

## Common Workflows

### Daily Development Loop

```bash
# 1. Start your work
cd my-project

# 2. Make changes to code
vim src/main.py

# 3. Test your changes
genesis test

# 4. Format and lint
genesis format
genesis lint

# 5. Commit with quality gates
genesis commit -m "feat: add new feature"

# 6. Push to remote
git push
```

### Before Creating a Pull Request

```bash
# 1. Run full quality check
genesis quality

# 2. Sync latest templates
genesis sync

# 3. Check project health
genesis status

# 4. Ensure all tests pass
genesis test

# 5. Create PR (if gh CLI installed)
gh pr create --title "Feature: XYZ" --body "Description..."
```

### Working on Large Feature (AI-Safe)

```bash
# 1. Create focused worktree
genesis worktree create new-feature --focus src/feature/ tests/feature/

# 2. Switch to worktree directory
cd ../worktrees/new-feature

# 3. Develop with reduced file count (AI-safe)
genesis test
genesis commit -m "feat: implement feature component"

# 4. When done, switch back and remove worktree
cd ../../my-project
genesis worktree remove new-feature
```

### Fixing Bugs

```bash
# 1. Create worktree for bug fix
genesis worktree create bugfix-123 --focus src/problematic_module.py tests/test_module.py

# 2. Fix the bug in worktree
cd ../worktrees/bugfix-123
vim src/problematic_module.py

# 3. Test the fix
genesis test -k test_problematic

# 4. Commit from worktree
genesis commit -m "fix: resolve issue #123"

# 5. Return to main and clean up
cd ../../my-project
genesis worktree remove bugfix-123
```

### Updating Dependencies

```bash
# 1. Update dependencies
poetry update

# 2. Test everything still works
genesis test

# 3. Run quality checks
genesis quality

# 4. Commit the lock file
genesis commit -m "chore: update dependencies"
```

## AI Safety

Genesis enforces AI safety through file count limits and sparse worktrees.

### File Count Limits

**Default Limits:**
- `AI_MAX_FILES=60` - Max files per component
- `MAX_PROJECT_FILES=1000` - Max total project files
- `WORKTREE_MAX_FILES=80` - Max files in worktrees

**When file counts exceed limits:**
1. Genesis warns you during operations
2. Use worktrees to isolate work
3. Focus on specific components

### Using Worktrees for AI Safety

Worktrees create isolated copies with only necessary files:

```bash
# Create focused worktree (only includes specified paths)
genesis worktree create feature --focus src/auth/ tests/auth/

# Work in AI-safe environment
cd ../worktrees/feature
# Now only ~30 files visible instead of 500+

# AI assistants work better with fewer files
genesis commit -m "feat: update auth logic"
```

### AI Safety Enforcement

Genesis automatically:
- ✅ Counts files on sync operations
- ✅ Warns when approaching limits
- ✅ Suggests worktrees for large projects
- ✅ Enforces limits in CI/CD (if configured)

## Project Structure

Genesis projects follow this structure:

```
my-project/
├── .genesis/              # Genesis configuration and scripts
│   ├── manifest.yml       # Template sync configuration
│   ├── hooks/            # Git hooks
│   ├── scripts/          # Setup and utility scripts
│   └── releases.json     # Genesis version tracking
├── .claude/              # Claude Code configuration
│   ├── agents/           # AI agent configurations
│   ├── commands/         # Custom slash commands
│   └── settings.json     # Claude settings
├── src/                  # Source code
├── tests/                # Test files
├── .envrc                # Environment variables (direnv)
├── CLAUDE.md             # AI assistant instructions
├── README.md             # Project documentation
├── pyproject.toml        # Python project configuration
└── Dockerfile            # Container configuration
```

## Configuration

### Environment Variables (.envrc)

Key variables clients should configure:

```bash
# Project identification
export PROJECT_NAME="my-project"
export PROJECT_MODE="development"  # or production

# AI Safety
export AI_SAFETY_MODE="enforced"
export AI_MAX_FILES="60"
export MAX_PROJECT_FILES="1000"

# Logging
export LOG_LEVEL="info"  # debug, info, warning, error
export LOG_JSON="false"

# AutoFix
export AUTOFIX_MAX_ITERATIONS="3"
export AUTOFIX_MAX_RUNS="5"

# Container
export COMPOSE_PROJECT_NAME="my-project"
```

### Genesis Manifest (.genesis/manifest.yml)

Controls which files Genesis syncs from templates:

```yaml
shared_files:
  - path: .genesis/hooks/post-commit
    source_hash: sha256:...
    sync: always
    description: Git post-commit hook

  - path: CLAUDE.md
    source_hash: sha256:...
    sync: never  # User customizable
    description: AI assistant instructions
```

**Sync Policies:**
- `always` - Always overwrite during sync
- `never` - Created once, never updated (user customizable)
- `if_unchanged` - Only sync if file hasn't been modified

### Claude Code Settings (.claude/settings.json)

Configure AI assistant behavior:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@uplight/mcp-context7-server"]
    }
  }
}
```

## Troubleshooting

### Command Not Found: genesis

**Problem:** `genesis: command not found`

**Solutions:**
```bash
# 1. Install Genesis
curl -sSL https://raw.githubusercontent.com/jhousteau/genesis/main/.genesis/scripts/setup/install-genesis.sh | bash

# 2. Activate virtual environment (if using .venv)
source .venv/bin/activate

# 3. Ensure .venv/bin is in PATH
export PATH="$PWD/.venv/bin:$PATH"
```

### Tests Failing After Sync

**Problem:** Tests fail after running `genesis sync`

**Solution:**
```bash
# 1. Check what changed
genesis sync --preview

# 2. Review changes to test files
git diff tests/

# 3. Update tests if needed
genesis test -v

# 4. Revert problematic syncs
git checkout -- problematic-file.py
```

### File Count Warnings

**Problem:** "⚠️ WARNING: 573 files detected - consider using sparse worktree"

**Solution:**
```bash
# Use worktrees for focused development
genesis worktree create feature --focus src/specific_module/

# Or adjust limits in .envrc
export AI_MAX_FILES="100"  # Increase if needed
```

### Import Errors After Sync

**Problem:** `ModuleNotFoundError` after syncing templates

**Solution:**
```bash
# 1. Reinstall dependencies
genesis setup

# 2. Or just poetry install
poetry install

# 3. Verify imports work
genesis test
```

### Docker Container Issues

**Problem:** Container commands fail

**Solution:**
```bash
# 1. Check Docker is running
docker ps

# 2. Validate docker-compose.yml
docker compose config

# 3. Rebuild container
genesis container build

# 4. Check logs
genesis container logs
```

### Quality Checks Failing

**Problem:** `genesis commit` blocked by quality checks

**Solution:**
```bash
# 1. Run checks individually
genesis format      # Format code
genesis lint        # Check for issues
genesis typecheck   # Verify types

# 2. Fix issues
genesis autofix

# 3. Or run quality to see all issues
genesis quality

# 4. Commit after fixes
genesis commit -m "fix: address quality issues"
```

### Worktree Creation Fails

**Problem:** `genesis worktree create` fails

**Solution:**
```bash
# 1. Check available space
df -h

# 2. Remove old worktrees
genesis worktree list
genesis worktree remove old-feature

# 3. Clean up
genesis clean --worktrees

# 4. Try again with smaller scope
genesis worktree create feature --focus src/small_module/
```

## Best Practices

### Commits
- ✅ Use `genesis commit` instead of `git commit` (quality gates)
- ✅ Write clear commit messages following conventional commits
- ✅ Run `genesis test` before committing
- ❌ Don't skip quality checks with `--no-verify`

### Testing
- ✅ Run `genesis test` frequently during development
- ✅ Use `-k` flag to run specific tests during iteration
- ✅ Run full `genesis quality` before PR
- ❌ Don't commit failing tests

### File Organization
- ✅ Keep projects under 1000 files
- ✅ Use worktrees for large features
- ✅ Respect AI safety limits
- ❌ Don't add unnecessary files to git

### Templates
- ✅ Run `genesis sync` regularly to get updates
- ✅ Review changes before accepting
- ✅ Customize "never" sync files freely
- ❌ Don't modify "always" sync files (they'll be overwritten)

### Worktrees
- ✅ Use focused worktrees for large features
- ✅ Remove worktrees when done
- ✅ Keep worktrees under 80 files
- ❌ Don't create worktrees for small changes

## Getting Help

**Command Help:**
```bash
genesis --help           # List all commands
genesis <command> -h     # Command-specific help
genesis <command> --help # Detailed help
```

**Check Status:**
```bash
genesis status          # Project health
genesis status -v       # Verbose output
genesis --version       # Genesis version
```

**Resources:**
- GitHub: https://github.com/jhousteau/genesis
- Issues: https://github.com/jhousteau/genesis/issues
- Discussions: https://github.com/jhousteau/genesis/discussions

## Version History

**v1.7.2 (Current)**
- Added: `genesis setup`, `test`, `format`, `lint`, `typecheck`, `quality` commands
- Improved: Worktree management with file count limits
- Fixed: Manifest sync with hash-based change detection

**v1.7.x**
- Added: Container management commands
- Added: Environment configuration commands
- Improved: Smart commit with autofix integration

**v1.6.x**
- Added: Worktree commands for AI-safe development
- Added: Template sync system with manifest
- Improved: Bootstrap templates

---

**Last Updated:** 2025-10-12
**Genesis Version:** 1.7.2
**Maintainer:** Genesis Team
