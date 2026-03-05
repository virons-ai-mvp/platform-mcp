# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM public.ecr.aws/amazonlinux/amazonlinux:2023 AS uv

# Install build dependencies
RUN dnf install -y shadow-utils python3.10 python3.10-devel gcc && \
    dnf clean all

WORKDIR /app

# UV configuration
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_FROZEN=true \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy dependency files
COPY pyproject.toml ./

# Install uv and dependencies
RUN python3.10 -m ensurepip && \
    python3.10 -m pip install uv && \
    uv sync --python 3.10 --frozen --no-install-project --no-dev --no-editable

# Copy source code
COPY virons/ ./virons/

# Install project
RUN uv sync --python 3.10 --frozen --no-dev --no-editable

# Production stage
FROM public.ecr.aws/amazonlinux/amazonlinux:2023

RUN dnf install -y python3.10 && \
    dnf clean all && \
    useradd -m -u 1000 virons

WORKDIR /app

# Copy from build stage
COPY --from=uv --chown=virons:virons /app/.venv /app/.venv

# Copy healthcheck script
COPY docker-healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-healthcheck.sh

USER virons

ENV PATH="/app/.venv/bin:$PATH"

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/docker-healthcheck.sh"]

ENTRYPOINT ["virons-infrastructure-mcp-server"]
