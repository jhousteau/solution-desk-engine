# solution-desk-engine

A solution-desk-engine project created with Genesis


## Genesis Shared Utilities

This project uses `shared-core`, the same battle-tested utilities that power Genesis itself:

- **Configuration Management**: `ConfigLoader` for YAML/env config with validation
- **Logging**: Structured logging with `get_logger()`
- **Error Handling**: Comprehensive error context with `create_error_context()`
- **Resilience**: Retry logic with exponential backoff via `@retry` decorator
- **Health Checks**: Production-ready health monitoring with `HealthCheck`
- **Environment**: Type-safe env vars with `get_required_env()` and `get_optional_env()`

These utilities are proven in production and follow Genesis best practices.

## Features

- FastAPI framework with automatic OpenAPI documentation
- Poetry for dependency management
- Pytest with async support and coverage reporting
- Pre-commit hooks with comprehensive code quality checks
- Type checking with mypy
- Code formatting with black and isort
- Advanced linting with ruff and flake8
- Security scanning with bandit and gitleaks
- Code quality analysis with pylint
- Environment management with direnv
- AI safety file count enforcement

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry
- direnv (required for automatic .envrc loading)

### Setup direnv (required)

```bash
# macOS
brew install direnv

# Ubuntu/Debian
sudo apt-get install direnv

# Add to your shell (add to ~/.bashrc or ~/.zshrc)
eval "$(direnv hook bash)"  # for bash
eval "$(direnv hook zsh)"   # for zsh

# Allow .envrc in this project
direnv allow
```

### Installation

✅ **Already configured!** Genesis bootstrap has set up everything for you:
- Poetry dependencies installed
- Pre-commit hooks configured
- Development environment ready

If you need to reinstall dependencies:
```bash
poetry install
poetry run pre-commit install
```

### Development

```bash
# Run the development server
poetry run uvicorn solution_desk_engine.main:app --reload
# or use make
make run

# Run tests
poetry run pytest
# or use make
make test

# Run tests with coverage
poetry run pytest --cov
# or use make
make test-cov

# Format code
poetry run black src/ tests/
poetry run isort src/ tests/
# or use make
make format

# Type checking
poetry run mypy src/
# or use make
make typecheck
```

### API Documentation

Once the server is running, you can access:
- API Documentation: http://localhost:8000/docs
- Alternative API Documentation: http://localhost:8000/redoc

### API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Production Deployment

```bash
# Install production dependencies
poetry install --only=main

# Run with Gunicorn (production WSGI server)
poetry run gunicorn solution_desk_engine.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run tests in watch mode
make test-watch
```

## Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type check
make typecheck

# Security scanning
make security

# Run all quality checks
make quality
```

## Build and Cleanup

```bash
# Build the package
make build

# Clean build artifacts
make clean
```

## Available Commands

```bash
# See all available make targets
make help
```

## Security

This project includes comprehensive security scanning:

- **Bandit**: Python security linter
- **Gitleaks**: Secret detection
- **Pre-commit hooks**: Prevent security issues from being committed

## AI-Safe Development with Worktrees

This project is Genesis-enabled with AI safety patterns built-in. For complex features or large codebases, use AI-safe worktrees to maintain optimal development experience:

### Creating Worktrees

```bash
# Using Genesis CLI directly
genesis worktree create my-feature --focus src/

# Using make (recommended)
make worktree-create NAME=my-feature FOCUS=src/

# Focus on multiple paths
genesis worktree create auth-system --focus src/auth --focus tests/auth

# Create with custom file limit
genesis worktree create large-feature --focus src/ --max-files 50
```

### Working in Worktrees

```bash
# List all worktrees
make worktree-list

# Switch to your worktree
cd worktrees/my-feature

# Work normally - all Genesis commands available
make test
make lint
make genesis-commit MSG="add new feature"

# Return to main project
cd ../..
```

### Removing Worktrees

```bash
# Clean up when done
make worktree-remove NAME=my-feature

# Or use Genesis directly
genesis worktree remove my-feature
```

### Genesis CLI Integration

Full Genesis CLI integration with smart commit and project health monitoring:

```bash
# Smart commit with quality gates
genesis commit -m "your message"
# or via make
make genesis-commit MSG="your message"

# Check project health
genesis status
# or via make
make genesis-status

# Clean workspace
genesis clean
# or via make
make genesis-clean
```

### Why Use Worktrees?

- **AI Optimal**: Keep file count under 30 for best AI assistant performance
- **Focus**: Work on specific features without distraction
- **Safety**: Changes isolated until ready to merge
- **Speed**: Faster operations on smaller working sets

## AI Safety Features

This project enforces AI safety patterns automatically:
- ✅ **File count limits**: Maximum 30 files per worktree for optimal AI interaction
- ✅ **Automatic validation**: File count warnings in development environment
- ✅ **Smart worktrees**: Genesis automatically creates properly scoped worktrees
- ✅ **Quality gates**: All commits go through Genesis smart-commit validation
