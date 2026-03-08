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
ENV PORT=9500
ENV SECURITY_HEADERS="X-Content-Type-Options:nosniff,X-Frame-Options:DENY,X-XSS-Protection:1;mode=block"
ENV LOG_LEVEL=INFO
ENV COMPLIANCE_MODE=strict

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3   CMD curl -f http://localhost:${PORT}/health || exit 1
CMD ["python", "server.py"]
