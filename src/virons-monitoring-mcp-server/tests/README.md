# Monitoring MCP Server - Tests

## Overview

Test suite for monitoring MCP server covering all layers.

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
pytest tests/ -v
pytest tests/ --cov=virons.monitoring_mcp_server --cov-report=html
```

## Navigation

← [Monitoring MCP Server](..)
