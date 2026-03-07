# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM python:3.13-slim AS base
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

FROM base AS builder
WORKDIR /build
COPY src/virons-common /tmp/virons-common
COPY src/virons-infrastructure-mcp-server/pyproject.toml src/virons-infrastructure-mcp-server/README.md ./
COPY src/virons-infrastructure-mcp-server/virons ./virons
RUN uv venv && \
    uv pip install /tmp/virons-common && \
    uv pip install -e .

FROM base AS runtime
WORKDIR /app
COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build/virons ./virons
RUN useradd -m -u 1000 virons && chown -R virons:virons /app
USER virons
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PORT=9100
EXPOSE 9100
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:9100/health || exit 1
CMD ["python", "-m", "virons.infrastructure_mcp_server.server", "--transport", "api", "--port", "9100"]
