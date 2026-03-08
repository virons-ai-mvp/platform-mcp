# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM python:3.13-slim AS base
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

FROM base AS builder
WORKDIR /build
COPY src/virons-common /tmp/virons-common
COPY src/virons-mcp-gateway/pyproject.toml src/virons-mcp-gateway/README.md ./
COPY src/virons-mcp-gateway/virons ./virons
RUN uv venv && \
    uv pip install /tmp/virons-common && \
    uv pip install -e . && \
    uv pip install mcp httpx pydantic

FROM base AS runtime
WORKDIR /app
COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build/virons ./virons

# Copy all orchestrator MCP servers
COPY src/virons-infrastructure-mcp /app/virons-infrastructure-mcp
COPY src/virons-forensic-mcp /app/virons-forensic-mcp
COPY src/virons-ml-mcp /app/virons-ml-mcp
COPY src/virons-blockchain-mcp /app/virons-blockchain-mcp
COPY src/virons-dev-mcp /app/virons-dev-mcp
COPY src/virons-api-mcp /app/virons-api-mcp
COPY src/virons-prompts-mcp /app/virons-prompts-mcp
COPY src/virons-compliance-mcp /app/virons-compliance-mcp
COPY src/virons-security-mcp /app/virons-security-mcp

# Copy awslabs MCP servers for orchestrators to invoke
COPY src/awslabs /app/awslabs

RUN useradd -m -u 1000 virons && chown -R virons:virons /app
USER virons
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PORT=9000
EXPOSE 9000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:9000/health || exit 1
CMD ["python", "-m", "virons.mcp_gateway.server"]
