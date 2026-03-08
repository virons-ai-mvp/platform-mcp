#!/bin/bash
# Extract metadata from MCP server for README generation

set -e

SERVER=$1
if [ -z "$SERVER" ]; then
  echo "Usage: $0 <server-name>"
  echo "Example: $0 security"
  exit 1
fi

SERVER_DIR="src/virons-${SERVER}-mcp-server"
if [ ! -d "$SERVER_DIR" ]; then
  echo "Error: $SERVER_DIR not found"
  exit 1
fi

echo "=== Extracting metadata for ${SERVER} MCP server ==="

# Port
PORT=$(grep -A5 "virons-${SERVER}-mcp:" docker-compose.yml | grep -E '"\d+:\d+"' | sed -E 's/.*"[0-9]+:([0-9]+)".*/\1/')
echo "Port: $PORT"

# Tools from tool_metadata.py
if [ -f "$SERVER_DIR/virons/${SERVER}_mcp_server/tool_metadata.py" ]; then
  TOOLS=$(grep 'if name ==' "$SERVER_DIR/virons/${SERVER}_mcp_server/tool_metadata.py" | wc -l | tr -d ' ')
  echo "Tools: $TOOLS"
  echo "Tool list:"
  grep 'if name ==' "$SERVER_DIR/virons/${SERVER}_mcp_server/tool_metadata.py" | sed -E 's/.*name == "([^"]+)".*/  - \1/'
fi

# Upstreams
if [ -f "$SERVER_DIR/virons/${SERVER}_mcp_server/server.py" ]; then
  echo "Upstreams:"
  grep -A10 "^UPSTREAM = {" "$SERVER_DIR/virons/${SERVER}_mcp_server/server.py" | grep '"' | sed -E 's/.*"([^"]+)".*/  - \1/' | grep -v "host\|port"
fi

# Dependencies
if [ -f "$SERVER_DIR/pyproject.toml" ]; then
  echo "Key dependencies:"
  grep -A20 "^dependencies = \[" "$SERVER_DIR/pyproject.toml" | grep '"' | sed -E 's/.*"([^">=]+).*/  - \1/' | head -6
fi

# DDD layers
echo "DDD structure:"
if [ -d "$SERVER_DIR/virons/${SERVER}_mcp_server/application" ]; then
  echo "  ✓ application/"
else
  echo "  ✗ application/ (missing)"
fi
if [ -d "$SERVER_DIR/virons/${SERVER}_mcp_server/domain" ]; then
  echo "  ✓ domain/"
else
  echo "  ✗ domain/ (missing)"
fi
if [ -d "$SERVER_DIR/virons/${SERVER}_mcp_server/infrastructure" ]; then
  echo "  ✓ infrastructure/"
else
  echo "  ✗ infrastructure/ (missing)"
fi

echo "=== Metadata extraction complete ==="
