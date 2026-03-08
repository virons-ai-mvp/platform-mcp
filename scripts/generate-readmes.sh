#!/bin/bash
# Generate missing README.md files from template

set -e

TEMPLATE="src/virons-infrastructure-mcp-server/docs/reference/virons-readme-template.md"
SERVERS=("infrastructure" "security" "operations" "monitoring")

# Root READMEs
for server in "${SERVERS[@]}"; do
  target="src/virons-${server}-mcp-server/README.md"
  if [ ! -f "$target" ]; then
    echo "Creating $target"
    server_cap=$(echo "$server" | sed 's/^./\U&/')
    sed "s/\[Service Name\]/${server_cap} MCP Server/g" "$TEMPLATE" > "$target"
  fi
done

# virons/ layer READMEs
for server in "${SERVERS[@]}"; do
  target="src/virons-${server}-mcp-server/virons/${server}_mcp_server/README.md"
  if [ ! -f "$target" ]; then
    echo "Creating $target"
    server_cap=$(echo "$server" | sed 's/^./\U&/')
    cat > "$target" << EOFVIRONS
# ${server_cap} MCP Server - Core Implementation

## Overview
Core implementation of the ${server} MCP server following DDD architecture.

## Structure
${server}_mcp_server/
├── application/    # Use cases & orchestration
├── domain/         # Business logic & entities
├── infrastructure/ # External integrations
├── server.py       # Entry point
├── compliance.py   # Audit logging
└── models.py       # Data models

## Key Files
- server.py - FastMCP server with API/stdio modes
- tool_metadata.py - Tool enrichment with examples
- compliance.py - Audit trail implementation

## Navigation
← [${server_cap} MCP Server](../..)
EOFVIRONS
  fi
done

# tests/ READMEs
for server in "${SERVERS[@]}"; do
  target="src/virons-${server}-mcp-server/tests/README.md"
  if [ ! -f "$target" ]; then
    echo "Creating $target"
    server_cap=$(echo "$server" | sed 's/^./\U&/')
    cat > "$target" << EOFTESTS
# ${server_cap} MCP Server - Tests

## Overview
Test suite for ${server} MCP server.

## Structure
tests/
├── test_server.py       # Server integration tests
├── test_compliance.py   # Audit logging tests
└── test_tools.py        # Tool execution tests

## Running Tests
# All tests
pytest tests/ -v

# Coverage
pytest tests/ --cov=virons.${server}_mcp_server --cov-report=html

## Navigation
← [${server_cap} MCP Server](..)
EOFTESTS
  fi
done

# scripts/ READMEs
for server in "${SERVERS[@]}"; do
  if [ "$server" = "infrastructure" ]; then
    continue  # Already has scripts/
  fi
  
  mkdir -p "src/virons-${server}-mcp-server/scripts"
  target="src/virons-${server}-mcp-server/scripts/README.md"
  if [ ! -f "$target" ]; then
    echo "Creating $target"
    server_cap=$(echo "$server" | sed 's/^./\U&/')
    cat > "$target" << EOFSCRIPT
# ${server_cap} MCP Server - Scripts

## Overview
Operational scripts for ${server} MCP server.

## Available Scripts
- start-api.sh - Start API server locally
- run-tests.sh - Run test suite
- healthcheck.sh - Health check script

## Navigation
← [${server_cap} MCP Server](..)
EOFSCRIPT
  fi
done

# Gateway
target="src/virons-mcp-gateway/README.md"
if [ ! -f "$target" ]; then
  echo "Creating $target"
  cat > "$target" << EOFGATEWAY
# Virons MCP Gateway

## Overview
Central gateway aggregating 90 tools from 4 backend MCP servers.

## Architecture
graph TB
  Client[MCP Client] --> Gateway[Gateway :9000]
  Gateway --> Infra[Infrastructure :9100<br/>78 tools]
  Gateway --> Sec[Security :9500<br/>4 tools]
  Gateway --> Ops[Operations :9510<br/>4 tools]
  Gateway --> Mon[Monitoring :9520<br/>4 tools]

## Key Features
- Dynamic tool discovery from backends
- Correlation ID propagation
- Prometheus metrics
- Rate limiting
- Health-based dependencies

## Usage
# List all tools
curl http://localhost:9000/tools | jq

# Execute tool
curl -X POST http://localhost:9000/tools/deploy_infrastructure \\
  -H "Authorization: Bearer token" \\
  -d '{"tool": "terraform", "stack_name": "test"}'

## Navigation
← [Platform MCP](../..)
EOFGATEWAY
fi

echo "✅ README generation complete"
