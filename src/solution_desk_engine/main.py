"""Main FastAPI application."""

from fastapi import FastAPI
from pydantic import BaseModel

# Use Genesis shared utilities for dogfooding - same utilities Genesis uses internally
from shared_core.env import get_optional_env
from shared_core import get_logger, HealthCheck
from shared_core.health import HealthStatus

# Initialize logger
logger = get_logger(__name__)

# Configuration loaded with fail-fast behavior using shared_core utilities
SERVICE_NAME = get_optional_env("SERVICE_NAME", "solution-desk-engine")
SERVICE_VERSION = get_optional_env("SERVICE_VERSION", "0.1.0")
LOG_LEVEL = get_optional_env("LOG_LEVEL", "info")

app = FastAPI(
    title=SERVICE_NAME,
    description="A solution-desk-engine project created with Genesis",
    version=SERVICE_VERSION
)

# Initialize health checker for monitoring
health_checker = HealthCheck()

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    service: str
    version: str
    checks: list[dict]

class MessageResponse(BaseModel):
    """Generic message response model."""
    message: str

@app.get("/")
async def root() -> MessageResponse:
    """Root endpoint returning welcome message."""
    logger.info(f"Root endpoint accessed for {SERVICE_NAME}")
    return MessageResponse(message=f"Welcome to {SERVICE_NAME}!")

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint with detailed status."""
    # Run health checks using shared_core
    checks = health_checker.run_all_checks()
    overall_status = health_checker.get_overall_status()

    return HealthResponse(
        status="healthy" if overall_status == HealthStatus.HEALTHY else "unhealthy",
        service=SERVICE_NAME,
        version=SERVICE_VERSION,
        checks=[{"name": c.name, "status": c.status.value, "message": c.message} for c in checks]
    )

if __name__ == "__main__":
    import uvicorn

    # Get server configuration with fail-fast behavior
    host = get_optional_env("SERVER_HOST", "127.0.0.1")
    port = int(get_optional_env("SERVER_PORT", "8000"))

    logger.info(f"Starting {SERVICE_NAME} on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
