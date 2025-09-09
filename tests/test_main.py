"""Tests for main application."""

import os
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

from solution_desk_engine.main import app
from shared_core.env import get_optional_env, get_required_env

client = TestClient(app)

def test_root_endpoint() -> None:
    """Test the root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to solution-desk-engine!"

def test_health_check() -> None:
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "solution-desk-engine"
    assert data["version"] == "0.1.0"

@pytest.mark.asyncio
async def test_root_endpoint_async() -> None:
    """Test root endpoint using async client."""
    from httpx import AsyncClient
    import httpx

    async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "Welcome to solution-desk-engine" in data["message"]

def test_get_required_env_success() -> None:
    """Test get_required_env returns value when environment variable is set."""
    with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
        result = get_required_env("TEST_VAR")
        assert result == "test_value"

def test_get_required_env_missing() -> None:
    """Test get_required_env raises ValueError when environment variable is missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Required environment variable 'TEST_VAR' is not set"):
            get_required_env("TEST_VAR")

def test_main_execution_code_paths() -> None:
    """Test the code paths in the main execution block."""

    # Test the environment variable retrieval logic used in main block
    with patch.dict(os.environ, {"SERVER_HOST": "0.0.0.0", "SERVER_PORT": "9000"}):
        host = get_optional_env("SERVER_HOST", "127.0.0.1")
        port = int(get_optional_env("SERVER_PORT", "8000"))

        assert host == "0.0.0.0"
        assert port == 9000

    # Test with default values (empty environment)
    with patch.dict(os.environ, {}, clear=True):
        host = get_optional_env("SERVER_HOST", "127.0.0.1")
        port = int(get_optional_env("SERVER_PORT", "8000"))

        assert host == "127.0.0.1"
        assert port == 8000
