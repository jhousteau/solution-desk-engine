"""Test configuration and fixtures."""

import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    """Load environment variables from .envrc for tests."""
    # Find the project root (.envrc should be there)
    project_root = Path(__file__).parent.parent
    envrc_path = project_root / ".envrc"

    if envrc_path.exists():
        # Parse .envrc file and set environment variables
        with open(envrc_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("export ") and "=" in line:
                    # Remove 'export ' prefix and parse KEY=VALUE
                    var_assignment = line[7:]  # Remove 'export '
                    if "=" in var_assignment:
                        key, value = var_assignment.split("=", 1)
                        # Remove quotes if present
                        value = value.strip("\"'")
                        os.environ[key] = value
