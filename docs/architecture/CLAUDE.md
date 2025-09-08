# solution-desk-engine Architecture Context

This directory contains system architecture, design patterns, and technical constraints for development work.

## System Architecture

### Technology Stack
- **Framework**: FastAPI (Python 3.11+)
- **Server**: Uvicorn (ASGI)
- **Testing**: Pytest with async support
- **Configuration**: Environment variables (fail-fast loading)
- **Documentation**: Automatic OpenAPI generation

### Service Boundaries
Define what this service owns vs external dependencies:
- **Owns**: Business logic, data validation, API contracts
- **External**: Authentication, databases, message queues, file storage

## Design Patterns & Principles

### Required Patterns
- **Dependency Injection**: Use FastAPI's dependency system
- **Configuration Management**: Environment variables with clear error messages
- **Error Handling**: Structured responses, proper HTTP status codes
- **Validation**: Pydantic models for all inputs/outputs

### Forbidden Patterns
- **Hardcoded Values**: No embedded URLs, ports, or connection strings
- **Silent Failures**: Always fail fast with clear error messages
- **Global State**: Avoid module-level mutable state
- **Tight Coupling**: Services should be independently testable

## API Design Standards

### REST Conventions
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Follow RESTful resource naming
- Return consistent response formats
- Include proper status codes

### Data Models
```python
# ✅ REQUIRED - Explicit validation
class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)

# ❌ FORBIDDEN - Vague or missing validation
class UserData(BaseModel):
    data: dict
```

## Security Architecture

### Authentication & Authorization
Document your security model as it develops:
- API key validation
- JWT token handling
- Role-based access control

### Data Protection
- Input sanitization requirements
- Output filtering rules
- Sensitive data handling

## Performance Requirements

### Response Time Targets
- Health checks: < 100ms
- Simple operations: < 500ms
- Complex operations: < 2s

### Resource Constraints
- Memory usage per request: < 50MB
- Concurrent connections: 100+
- Request throughput: 1000+ req/sec

## Development Constraints

### Code Organization
```
src/solution-desk-engine/
├── main.py          # FastAPI app and configuration
├── models/          # Pydantic data models
├── routers/         # API route handlers
├── services/        # Business logic
└── dependencies/    # FastAPI dependencies
```

### Testing Requirements
- Unit tests for all business logic
- Integration tests for API endpoints
- 80%+ code coverage required
- All tests must be deterministic

---

**Context for AI Assistants**: Follow these patterns and constraints when implementing features. When adding new functionality, maintain consistency with existing code structure and security requirements.
