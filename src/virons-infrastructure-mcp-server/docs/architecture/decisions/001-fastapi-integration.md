# ADR 001: FastAPI Integration for REST API

**Status**: Accepted
**Date**: 2026-03-07
**Deciders**: Platform Team
**Context**: Need REST API with interactive documentation

## Context and Problem Statement

The MCP server initially only supported stdio protocol for AI agents. We needed to add REST API support for:
- Human operators via web UI
- External system integration
- Interactive API documentation
- Easier testing and debugging

## Decision Drivers

- Need interactive API documentation (Swagger UI)
- Want to maintain MCP protocol support
- Require multi-protocol support (stdio, http, api)
- Must follow DDD architecture
- Need Pydantic validation
- Want OpenAPI schema generation

## Considered Options

1. **FastAPI** - Modern Python web framework
2. **Flask** - Lightweight web framework
3. **Django REST Framework** - Full-featured framework
4. **Extend MCP server** - Add HTTP to MCP

## Decision Outcome

Chosen option: **FastAPI**

### Positive Consequences

- ✅ Automatic OpenAPI/Swagger UI generation
- ✅ Built-in Pydantic validation
- ✅ Async/await support (matches MCP)
- ✅ High performance (ASGI)
- ✅ Type hints and IDE support
- ✅ Easy integration with existing code
- ✅ ReDoc alternative documentation

### Negative Consequences

- ➖ Additional dependency (fastapi + uvicorn)
- ➖ Slightly larger Docker image
- ➖ Need to maintain two API surfaces (MCP + REST)

## Implementation

### API Layer (`api.py`)
```python
from fastapi import FastAPI

app = FastAPI(
    title="Virons Infrastructure MCP Server",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)
```

### Multi-Protocol Support (`server.py`)
```python
parser.add_argument(
    "--transport",
    choices=["stdio", "http", "api"],
    default="stdio"
)

if args.transport == "api":
    uvicorn.run(app, host="0.0.0.0", port=args.port)
elif args.transport == "http":
    # Health checks only
elif args.transport == "stdio":
    # MCP protocol
```

### Pydantic Models
```python
class DeployRequest(BaseModel):
    tool: str
    stack_name: str
    template_path: Optional[str]
    parameters: Optional[Dict[str, Any]]
```

## Pros and Cons of the Options

### FastAPI
- ✅ Modern, async-first
- ✅ Automatic docs
- ✅ Pydantic integration
- ✅ High performance
- ➖ Newer framework

### Flask
- ✅ Mature, stable
- ✅ Large ecosystem
- ➖ No automatic docs
- ➖ Sync-first (WSGI)
- ➖ Manual validation

### Django REST Framework
- ✅ Full-featured
- ✅ Admin interface
- ➖ Heavy framework
- ➖ Overkill for our needs
- ➖ Sync-first

### Extend MCP
- ✅ No new dependencies
- ➖ No Swagger UI
- ➖ Manual HTTP handling
- ➖ Not standard REST

## Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Implementation PR](#) - Link to PR when available
