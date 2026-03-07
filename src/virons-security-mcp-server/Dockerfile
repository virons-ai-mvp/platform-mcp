# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM python:3.13-slim AS builder
WORKDIR /build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY src/virons-common /tmp/virons-common
COPY src/virons-security-mcp-server/pyproject.toml src/virons-security-mcp-server/README.md ./
COPY src/virons-security-mcp-server/virons ./virons
RUN uv venv && \
    uv pip install /tmp/virons-common && \
    uv pip install -e .

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build/virons ./virons
RUN useradd -m -u 1000 virons && chown -R virons:virons /app
USER virons
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PORT=9500
EXPOSE 9500
CMD ["python", "-m", "virons.security_mcp_server.server", "--transport", "http"]
