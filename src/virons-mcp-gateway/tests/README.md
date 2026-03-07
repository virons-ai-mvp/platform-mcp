# MCP Gateway - Tests

## Overview

Test suite for gateway covering routing, discovery, and middleware.

## Structure

```
tests/
├── test_server.py           # Server integration tests
├── test_gateway.py          # Gateway routing tests
├── test_registry.py         # Service registry tests
├── test_middleware.py       # Middleware tests
└── test_discovery.py        # Tool discovery tests
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# Coverage
pytest tests/ --cov=virons.mcp_gateway --cov-report=html

# Specific test
pytest tests/test_gateway.py::test_execute_tool -v
```

## Test Categories

**Integration Tests** (test_server.py)
- Server startup
- Tool execution end-to-end
- Health endpoints
- Metrics collection

**Unit Tests** (test_gateway.py)
- Tool routing logic
- Error handling
- Backend communication

**Middleware Tests** (test_middleware.py)
- Rate limiting
- Correlation ID propagation
- Metrics collection

**Discovery Tests** (test_discovery.py)
- Tool discovery from backends
- Registry population
- Service mapping

## Coverage Requirements

- Overall: >80%
- Critical paths: 100%
- Routing logic: >95%

## Navigation

← [MCP Gateway](..)
