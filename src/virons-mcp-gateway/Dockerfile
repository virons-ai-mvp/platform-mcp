# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM python:3.13-slim AS builder

WORKDIR /build

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY src/virons-infrastructure-mcp-server/pyproject.toml src/virons-infrastructure-mcp-server/README.md ./
COPY src/virons-infrastructure-mcp-server/virons ./virons
COPY src/virons-infrastructure-mcp-server/scripts ./scripts

# Copy virons.common
COPY src/virons-common /tmp/virons-common

# Create venv and install dependencies
RUN uv venv && \
    uv pip install /tmp/virons-common && \
    uv pip install -e .

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /build/.venv /app/.venv

# Copy application code
COPY --from=builder /build/virons ./virons

# Create non-root user
RUN useradd -m -u 1000 virons && \
    chown -R virons:virons /app

USER virons

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health/live')"

CMD ["python", "-m", "virons.infrastructure_mcp_server.server", "--transport", "http"]
