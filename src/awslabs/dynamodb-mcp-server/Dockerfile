# Enterprise-Grade MCP Server: dynamodb-mcp-server
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM python:3.13-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
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
WORKDIR /app/src/awslabs/dynamodb-mcp-server

# Copy virtual environment from builder
COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build /app

# Create non-root user
RUN useradd -m -u 1000 mcp && \
    chown -R mcp:mcp /app

# Switch to non-root user
USER mcp

# Environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PORT=9180 \
    LOG_LEVEL=INFO \
    AWS_REGION=eu-central-1

# Expose port
EXPOSE 9180

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:9180/health || exit 1

# Run server module directly
CMD ["python", "-m", "awslabs.dynamodb_mcp_server.server"]
