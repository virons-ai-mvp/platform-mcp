#!/bin/bash
# Generate production-ready Dockerfiles for AWS Labs MCP servers
# Usage: ./scripts/generate-mcp-dockerfiles.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$PROJECT_ROOT/docker/Dockerfile.template"
AWSLABS_DIR="$PROJECT_ROOT/src/awslabs"

# MCP servers to generate Dockerfiles for
SERVERS=(
    "aws-network-mcp-server:9144:awslabs.aws_network_mcp_server.server"
    "postgres-mcp-server:9150:awslabs.postgres_mcp_server.server"
    "dynamodb-mcp-server:9180:awslabs.dynamodb_mcp_server.server"
    "cloudwatch-mcp-server:9190:awslabs.cloudwatch_mcp_server.server"
    "cloudtrail-mcp-server:9102:awslabs.cloudtrail_mcp_server.server"
)

generate_dockerfile() {
    local server_name=$1
    local port=$2
    local module=$3
    local server_dir="$AWSLABS_DIR/$server_name"
    local dockerfile="$server_dir/Dockerfile"

    # Extract script name from pyproject.toml
    local script_name=$(grep -A1 '\[project.scripts\]' "$server_dir/pyproject.toml" | grep '"' | cut -d'"' -f2)

    echo "Generating Dockerfile for $server_name (script: $script_name)..."

    cat > "$dockerfile" <<EOF
# Enterprise-Grade MCP Server: $server_name
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM python:3.13-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl \\
    ca-certificates \\
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Builder stage
FROM base AS builder
WORKDIR /build

# Copy server source
COPY . .

# Install dependencies
RUN uv sync --frozen --no-dev

# Runtime stage
FROM base AS runtime
WORKDIR /app/src/awslabs/$server_name

# Copy virtual environment from builder
COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build /app

# Create non-root user
RUN useradd -m -u 1000 mcp && \\
    chown -R mcp:mcp /app

# Switch to non-root user
USER mcp

# Environment variables
ENV PATH="/app/.venv/bin:\$PATH" \\
    PYTHONUNBUFFERED=1 \\
    PORT=$port \\
    LOG_LEVEL=INFO \\
    AWS_REGION=eu-central-1

# Expose port
EXPOSE $port

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \\
    CMD curl -f http://localhost:$port/health || exit 1

# Run server module directly
CMD ["python", "-m", "awslabs.${server_name//-/_}.server"]
EOF

    echo "✅ Created $dockerfile"
}

main() {
    echo "🚀 Generating Enterprise-Grade Dockerfiles for MCP Servers"
    echo "==========================================================="

    if [ ! -f "$TEMPLATE" ]; then
        echo "❌ Template not found: $TEMPLATE"
        exit 1
    fi

    for server_entry in "${SERVERS[@]}"; do
        IFS=':' read -r server_name port module <<< "$server_entry"

        if [ ! -d "$AWSLABS_DIR/$server_name" ]; then
            echo "⚠️  Server directory not found: $server_name (skipping)"
            continue
        fi

        generate_dockerfile "$server_name" "$port" "$module"
    done

    echo ""
    echo "✅ All Dockerfiles generated successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Review generated Dockerfiles"
    echo "2. Test build: docker build -t test src/awslabs/<server-name>"
    echo "3. Deploy: docker-compose -f docker-compose.core.yml up -d"
}

main "$@"
