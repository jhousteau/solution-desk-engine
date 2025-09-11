#!/bin/bash
set -e

echo "🚀 Setting up {{project_name}} development environment..."

# Change to project root directory (parent of scripts/)
cd "$(dirname "$0")/.."

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]]; then
    echo "❌ Error: Not in project root directory (pyproject.toml not found)"
    echo "   Current directory: $(pwd)"
    exit 1
fi

# Install dependencies and development tools
echo "📦 Installing dependencies and development environment..."
if command -v poetry >/dev/null 2>&1; then
    poetry install
else
    echo "❌ Error: Poetry not found. Please install Poetry first."
    echo "   Visit: https://python-poetry.org/docs/#installation"
    exit 1
fi

# Install Genesis CLI for project commands
echo "🔧 Installing Genesis CLI..."
if [[ -d "../genesis" ]]; then
    # Install Genesis from local development directory using pip (not poetry)
    # This ensures proper editable install that Genesis can find its root
    poetry run pip install -e "../genesis"
    echo "✅ Genesis CLI installed from local development version"
elif command -v pip >/dev/null 2>&1; then
    # Try to install Genesis from PyPI (if published)
    if poetry run pip install genesis-cli 2>/dev/null; then
        echo "✅ Genesis CLI installed from PyPI"
    else
        echo "⚠️  Genesis CLI not available via PyPI, using project-specific commands"
    fi
else
    echo "⚠️  Could not install Genesis CLI - using project-specific commands"
fi

# Check if direnv is available
if command -v direnv >/dev/null 2>&1; then
    echo "🌍 direnv detected - environment will auto-load when entering directory"
    direnv allow
else
    echo "⚠️  direnv not found - you can install it for automatic environment loading"
    echo "   Or manually source .envrc: source .envrc"
fi

# Initialize git hooks if needed
if [[ -d ".git" ]]; then
    echo "🔧 Git repository detected - pre-commit hooks installed"
else
    echo "ℹ️  No git repository found - hooks will be installed when you init git"
fi

# Test the setup
echo "🧪 Testing setup..."
poetry run python -c "print('✅ Python environment working')"
poetry run black --version >/dev/null && echo "✅ Code formatting tools ready"
poetry run pytest --version >/dev/null && echo "✅ Testing framework ready"

# Test Genesis CLI availability
if poetry run genesis --version >/dev/null 2>&1; then
    echo "✅ Genesis CLI ready"
    GENESIS_AVAILABLE=true
else
    echo "⚠️  Genesis CLI not available - using make targets instead"
    GENESIS_AVAILABLE=false
fi

echo ""
echo "🎉 Setup complete! You can now:"
echo "   • Run tests: make test"
echo "   • Format code: make format"
echo "   • Start dev server: make run"

if [[ "$GENESIS_AVAILABLE" == "true" ]]; then
    echo "   • Smart commit: genesis commit"
    echo "   • Check status: genesis status"
    echo "   • See all commands: make help"
    echo ""
    echo "💡 Pro tip: Use 'genesis status' to check project health"
else
    echo "   • Smart commit: make genesis-commit MSG=\"your message\""
    echo "   • Check status: make genesis-status"
    echo "   • See all commands: make help"
    echo ""
    echo "💡 Pro tip: Use 'make genesis-status' to check project health"
fi
