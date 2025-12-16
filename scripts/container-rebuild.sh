#!/bin/bash
# Genesis Container Rebuild Script
# Complete container rebuild workflow: clean, sync, rebuild, and enter shell
set -euo pipefail

echo "🔄 Starting complete container rebuild workflow..."

# Change to project root directory (parent of scripts/)
cd "$(dirname "$0")/.."

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]] && [[ ! -f "package.json" ]] && [[ ! -f "go.mod" ]] && [[ ! -f "Cargo.toml" ]]; then
    echo "❌ Error: Not in project root directory (no project file found)"
    echo "   Current directory: $(pwd)"
    exit 1
fi

# Check if Genesis CLI is available
if ! command -v genesis >/dev/null 2>&1 && ! poetry run genesis --version >/dev/null 2>&1 && ! npm run genesis --version >/dev/null 2>&1; then
    echo "❌ Error: Genesis CLI not available"
    echo "   Please run 'source .envrc' and ensure Genesis is installed"
    exit 1
fi

# Determine the command to use based on project type
GENESIS_CMD="genesis"
if ! command -v genesis >/dev/null 2>&1; then
    if [[ -f "pyproject.toml" ]]; then
        GENESIS_CMD="poetry run genesis"
    elif [[ -f "package.json" ]]; then
        GENESIS_CMD="npm run genesis"
    else
        echo "❌ Error: Cannot determine how to run Genesis CLI"
        exit 1
    fi
fi

echo "🧹 Step 1/6: Cleaning build artifacts..."
make clean

echo "🔄 Step 2/6: Syncing project files with templates..."
$GENESIS_CMD sync

echo "🗑️  Step 3/6: Removing existing container..."
$GENESIS_CMD container remove || {
    echo "⚠️  No existing container to remove (this is normal on first run)"
}

echo "🔨 Step 4/6: Building fresh container image..."
$GENESIS_CMD container build

echo "🚀 Step 5/6: Starting container in detached mode..."
$GENESIS_CMD container run

echo "🐚 Step 6/6: Opening interactive shell in container..."
echo ""
echo "🎉 Container rebuild complete! Opening shell..."
echo "   Type 'exit' to leave the container shell"
echo ""

# Open shell (this will be interactive)
$GENESIS_CMD container shell
