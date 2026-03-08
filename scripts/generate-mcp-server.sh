#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: ./scripts/generate-mcp-server.sh <server-name> <port>"
  echo "Example: ./scripts/generate-mcp-server.sh infrastructure 9100"
  exit 1
fi

NAME=$1
PORT=$2
DIR="src/virons-${NAME}-mcp"

echo "Creating MCP server: virons-${NAME}-mcp on port ${PORT}"

mkdir -p "${DIR}/tools"

# server.py
cat > "${DIR}/server.py" << 'EOF'
"""Virons {NAME} MCP Server"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("virons-{NAME}-mcp")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="example_tool",
            description="Example tool - replace with actual tools",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "Example parameter"}
                },
                "required": ["param"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "example_tool":
        return [TextContent(type="text", text=f"Result: {arguments.get('param')}")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
EOF

sed -i '' "s/{NAME}/${NAME}/g" "${DIR}/server.py"

# pyproject.toml
cat > "${DIR}/pyproject.toml" << EOF
[project]
name = "virons-${NAME}-mcp"
version = "0.1.0"
description = "Virons ${NAME} MCP Server"
requires-python = ">=3.13"
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
EOF

# Dockerfile
cat > "${DIR}/Dockerfile" << EOF
FROM python:3.13-slim AS base
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

FROM base AS builder
WORKDIR /build
COPY pyproject.toml .
COPY server.py .
COPY tools/ tools/
RUN uv pip install --system -e .

FROM base AS runtime
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY --from=builder /build /app
RUN useradd -m -u 10001 mcp && chown -R mcp:mcp /app
USER mcp
ENV PORT=${PORT}
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:\${PORT}/health || exit 1
CMD ["python", "-m", "mcp", "run", "server.py"]
EOF

# tools/__init__.py
cat > "${DIR}/tools/__init__.py" << 'EOF'
"""Tool implementations"""
EOF

# README.md
cat > "${DIR}/README.md" << EOF
# Virons ${NAME} MCP Server

Port: ${PORT}

## Tools

- \`example_tool\` - Example tool (replace with actual tools)

## Usage

\`\`\`bash
# Run locally
python server.py

# Build Docker image
docker build -t virons-${NAME}-mcp .

# Run container
docker run -p ${PORT}:${PORT} virons-${NAME}-mcp
\`\`\`
EOF

echo "✅ Created ${DIR}"
echo "Next steps:"
echo "  1. Edit ${DIR}/server.py to add actual tools"
echo "  2. Implement tools in ${DIR}/tools/"
echo "  3. Update ${DIR}/README.md with tool documentation"
