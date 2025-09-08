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

- Click framework for CLI commands
- Rich library for beautiful terminal output
- Poetry for dependency management
- Pytest with coverage reporting
- Pre-commit hooks for code quality
- Type checking with mypy

## Installation

### Prerequisites

- Python 3.11+
- Poetry

### Install from Source

```bash
# Clone and install
git clone <repository-url>
cd solution-desk-engine
poetry install
```

### Install as Package

```bash
pip install solution-desk-engine
```

## Usage

After installation, you can use the `solution-desk-engine` command:

```bash
# Show help
solution-desk-engine --help

# Say hello
solution-desk-engine hello
solution-desk-engine hello --name Alice --count 3

# Display styled messages
solution-desk-engine display "Welcome to solution-desk-engine!"
solution-desk-engine display "Success!" --style success
solution-desk-engine display "Warning!" --style warning

# Check status
solution-desk-engine status
```

## Available Commands

- `hello` - Say hello to someone
- `display` - Display text with styling options
- `status` - Show application status

## Development

```bash
# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run the CLI in development
poetry run solution-desk-engine --help

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov

# Format code
poetry run black src/ tests/
poetry run isort src/ tests/

# Type checking
poetry run mypy src/
```

## Building and Distribution

```bash
# Build the package
poetry build

# Publish to PyPI (if configured)
poetry publish
```

## Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run all quality checks
make quality
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the quality checks
6. Submit a pull request
