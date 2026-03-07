# Security MCP Server - Tests

## Overview

Test suite for security MCP server covering all layers.

## Structure

```
tests/
├── test_server.py           # Server integration tests
├── test_compliance.py       # Audit logging tests
├── test_tools.py            # Tool execution tests
├── application/             # Application layer tests
├── domain/                  # Domain layer tests
└── infrastructure/          # Infrastructure layer tests
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# Coverage
pytest tests/ --cov=virons.security_mcp_server --cov-report=html

# Specific layer
pytest tests/application/ -v
pytest tests/domain/ -v
pytest tests/infrastructure/ -v

# Single test
pytest tests/test_server.py::test_scan_secrets -v
```

## Test Categories

**Integration Tests** (test_server.py)
- API mode startup
- Tool execution end-to-end
- Health endpoints
- Metrics collection

**Unit Tests** (test_tools.py)
- Individual tool logic
- Input validation
- Error handling

**Compliance Tests** (test_compliance.py)
- Audit logging
- Write operations tracking
- Immutable audit trail

## Coverage Requirements

- Overall: >80%
- Critical paths: 100%
- Domain logic: >90%

## Navigation

← [Security MCP Server](..)
