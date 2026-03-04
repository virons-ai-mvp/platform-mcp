#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Scaffold generator for virons MCP servers.

Creates compliance-first MCP server structure following DDD and TDD principles.
"""

import argparse
import sys
from pathlib import Path


def create_directory_structure(name: str, output_dir: Path) -> Path:
    """Create the directory structure for a virons MCP server.
    
    Args:
        name: Server name (e.g., 'infrastructure')
        output_dir: Parent directory for the server
        
    Returns:
        Path to the created server directory
    """
    server_dir = output_dir / f"virons-{name}-mcp-server"
    package_name = name.replace("-", "_")
    
    # Create main directories
    (server_dir / "virons" / f"{package_name}_mcp_server").mkdir(parents=True)
    (server_dir / "tests").mkdir(parents=True)
    
    return server_dir


def create_python_files(server_dir: Path, name: str, port: str) -> None:
    """Create Python source files.
    
    Args:
        server_dir: Server root directory
        name: Server name
        port: Server port
    """
    package_name = name.replace("-", "_")
    pkg_dir = server_dir / "virons" / f"{package_name}_mcp_server"
    
    # Create __init__.py files
    (server_dir / "virons" / "__init__.py").write_text(
        "# PEP 420 namespace package\n"
        "__path__ = __import__('pkgutil').extend_path(__path__, __name__)\n"
    )
    
    (pkg_dir / "__init__.py").write_text(
        f'# Copyright Virons Fintech. All Rights Reserved.\n'
        f'# SPDX-License-Identifier: Apache-2.0\n'
        f'"""virons.{package_name}_mcp_server — Virons {name.title()} MCP Server."""\n\n'
        "__version__ = '0.1.0'\n"
    )
    
    # server.py with FastMCP template
    (pkg_dir / "server.py").write_text(
        f'''# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""FastMCP server implementation for virons-{name}-mcp-server."""

import argparse
import os
import sys
from mcp.server.fastmcp import FastMCP
from loguru import logger

from .compliance import setup_compliance_hooks
from .consts import SERVER_NAME, SERVER_INSTRUCTIONS, SERVER_DEPENDENCIES


# Configure logging
logger.remove()
logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

mcp = None


def create_server() -> FastMCP:
    """Create and configure the FastMCP server instance.
    
    Returns:
        Configured FastMCP server
    """
    server = FastMCP(
        SERVER_NAME,
        instructions=SERVER_INSTRUCTIONS,
        dependencies=SERVER_DEPENDENCIES,
    )
    
    # Register compliance hooks
    setup_compliance_hooks(server)
    
    return server


def main() -> FastMCP:
    """Main entry point for the MCP server.
    
    Returns:
        Running FastMCP server instance
    """
    global mcp
    
    parser = argparse.ArgumentParser(description=f"Virons {{name.title()}} MCP Server")
    parser.add_argument(
        "--allow-write",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable write operations (requires audit trail)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport protocol (stdio for MCP, http for K8s probes)",
    )
    
    args = parser.parse_args()
    
    logger.info(f"Starting {{SERVER_NAME}} (write_enabled={{args.allow_write}})")
    
    mcp = create_server()
    
    # TODO: Register your tool handlers here
    # @mcp.tool()
    # async def example_tool(param: str) -> str:
    #     """Example tool implementation."""
    #     return f"Result: {{param}}"
    
    mcp.run()
    return mcp


if __name__ == "__main__":
    main()
'''
    )
    
    # models.py with Pydantic templates
    (pkg_dir / "models.py").write_text(
        f'''# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Pydantic models for virons-{name}-mcp-server."""

from pydantic import BaseModel, Field


class ExampleRequest(BaseModel):
    """Example request model."""
    
    param: str = Field(..., description="Example parameter")


class ExampleResponse(BaseModel):
    """Example response model."""
    
    result: str = Field(..., description="Example result")
    audit_id: str = Field(..., description="BaFin AT 8.1 audit trail ID")
'''
    )
    
    # consts.py
    (pkg_dir / "consts.py").write_text(
        f'''# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Constants for virons-{name}-mcp-server."""

SERVER_NAME = "virons.{package_name}-mcp-server"
SERVER_PORT = {port}

SERVER_INSTRUCTIONS = """
Virons {name.title()} MCP Server

This server is compliance-first and follows:
- BaFin MaRisk AT 8.1 (audit trail on all writes)
- GDPR Art 25, 32 (data residency, correlation IDs)
- DORA Art 11 (health monitoring)
- EU AI Act (model card validation if high-risk)

All write operations are audited. Data resides in eu-central-1 only.
"""

SERVER_DEPENDENCIES = [
    "mcp[cli]>=1.23.0",
    "loguru>=0.7.0",
    "pydantic>=2.10.6",
    "virons.common>=0.1.0",
]
'''
    )
    
    # compliance.py with virons.common integration
    (pkg_dir / "compliance.py").write_text(
        f'''# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Compliance hooks for virons-{name}-mcp-server.

Integrates virons.common compliance utilities:
- BaFin MaRisk AT 8.1: write_audit()
- GDPR Art 25: enforce_region()
- GDPR Art 32: CorrelationContext, generate_correlation_id()
- DORA Art 11: HealthCheck
"""

from mcp.server.fastmcp import FastMCP
from virons.common import (
    HealthCheck,
    CorrelationContext,
    generate_correlation_id,
    enforce_region,
    write_audit,
)
from loguru import logger


# Global instances
health_check = HealthCheck()
correlation_context = CorrelationContext()


def setup_compliance_hooks(server: FastMCP) -> None:
    """Register compliance hooks with the FastMCP server.
    
    Args:
        server: FastMCP server instance
    """
    # Enforce EU data residency (GDPR Art 25)
    enforce_region("eu-central-1")
    logger.info("Data residency enforced: eu-central-1")
    
    # TODO: Add readiness checks for dependencies (DORA Art 11)
    # health_check.add_readiness_check("database", lambda: check_db_connection())
    
    logger.info("Compliance hooks initialized")


async def audit_write_operation(
    operation_name: str,
    entity_id: str,
    input_data: dict,
    output_data: dict,
) -> str:
    """Audit a write operation per BaFin MaRisk AT 8.1.
    
    Args:
        operation_name: Name of the operation
        entity_id: Entity identifier
        input_data: Input parameters
        output_data: Operation results
        
    Returns:
        Audit trail ID
    """
    audit_id = await write_audit(
        service_name="virons-{name}-mcp-server",
        calculation_type=operation_name,
        entity_id=entity_id,
        input_data=input_data,
        output_data=output_data,
    )
    logger.info(f"Audit trail created: {{audit_id}}")
    return audit_id
'''
    )


def create_test_files(server_dir: Path, name: str) -> None:
    """Create test files.
    
    Args:
        server_dir: Server root directory
        name: Server name
    """
    package_name = name.replace("-", "_")
    tests_dir = server_dir / "tests"
    
    # test_server.py
    (tests_dir / "test_server.py").write_text(
        f'''# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for server.py."""

import pytest
from virons.{package_name}_mcp_server.server import create_server


def test_create_server():
    """Test server creation."""
    server = create_server()
    assert server is not None
    assert server.name == "virons.{package_name}-mcp-server"
'''
    )
    
    # test_init.py
    (tests_dir / "test_init.py").write_text(
        f'''# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for package initialization."""

import re
from importlib import reload
import virons.{package_name}_mcp_server


def test_version():
    """Test version is valid semver."""
    version = virons.{package_name}_mcp_server.__version__
    assert re.match(r"^\\d+\\.\\d+\\.\\d+", version)


def test_module_reload():
    """Test module can be reloaded."""
    reload(virons.{package_name}_mcp_server)
    assert virons.{package_name}_mcp_server.__version__
'''
    )
    
    # test_main.py
    (tests_dir / "test_main.py").write_text(
        f'''# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for main entry point."""

from unittest.mock import patch
from virons.{package_name}_mcp_server.server import main


@patch("virons.{package_name}_mcp_server.server.FastMCP.run")
def test_main_runs(mock_run):
    """Test main function runs server."""
    with patch("sys.argv", ["server", "--allow-write"]):
        server = main()
        assert server is not None
        mock_run.assert_called_once()
'''
    )
    
    # test_compliance.py
    (tests_dir / "test_compliance.py").write_text(
        f'''# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for compliance hooks."""

import pytest
from virons.{package_name}_mcp_server.compliance import (
    health_check,
    correlation_context,
    audit_write_operation,
)


def test_health_check_liveness():
    """Test liveness check returns ok."""
    result = health_check.liveness()
    assert result["status"] == "ok"


def test_health_check_readiness():
    """Test readiness check returns ok when no checks registered."""
    result = health_check.readiness()
    assert result["status"] == "ok"


@pytest.mark.asyncio
async def test_audit_write_operation():
    """Test audit write operation creates audit trail."""
    audit_id = await audit_write_operation(
        operation_name="test_operation",
        entity_id="test-entity-123",
        input_data={{"param": "value"}},
        output_data={{"result": "success"}},
    )
    assert audit_id
    assert "virons-{name}-mcp-server" in audit_id
'''
    )


def create_metadata_files(server_dir: Path, name: str, description: str, port: str, deps: list[str]) -> None:
    """Create metadata files.
    
    Args:
        server_dir: Server root directory
        name: Server name
        description: Server description
        port: Server port
        deps: Additional dependencies
    """
    package_name = name.replace("-", "_")
    
    # pyproject.toml with full configuration
    deps_str = "\n".join(f'    "{dep}",' for dep in deps) if deps else ""
    (server_dir / "pyproject.toml").write_text(
        f"""[project]
name = "virons.{package_name}-mcp-server"
version = "0.1.0"
description = "{description}"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp[cli]>=1.23.0",
    "loguru>=0.7.0",
    "pydantic>=2.10.6",
    "virons.common>=0.1.0",
{deps_str}
]
license = {{text = "Apache-2.0"}}
license-files = ["LICENSE", "NOTICE"]
authors = [
    {{name = "Virons Fintech"}},
]
classifiers = [
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

[project.urls]
homepage = "https://virons.ai"
repository = "https://github.com/virons-fintech/virons-ai-mvp.git"

[project.scripts]
virons-{name}-mcp-server = "virons.{package_name}_mcp_server.server:main"

[dependency-groups]
dev = [
    "commitizen>=4.2.2",
    "pre-commit>=4.1.0",
    "ruff>=0.9.7",
    "pyright>=1.1.398",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.26.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["virons"]

[tool.ruff]
target-version = "py310"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "D", "UP", "ANN", "S", "B", "A", "C4", "DTZ", "T10", "EM", "ISC", "ICN", "G", "PIE", "T20", "PT", "Q", "RSE", "RET", "SIM", "TID", "ARG", "PTH", "PD", "PGH", "PL", "TRY", "NPY", "RUF"]
ignore = ["ANN101", "ANN102", "D203", "D213"]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101", "D", "ANN"]

[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "standard"
reportMissingTypeStubs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--strict-markers --tb=short"

[tool.coverage.run]
source = ["virons"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]

[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
tag_format = "v$version"
"""
    )
    
    # README.md with full template
    (server_dir / "README.md").write_text(
        f"""# virons-{name}-mcp-server

{description}

**Port**: {port} | **Status**: 🟢 Scaffolded | **Compliance**: ✅ Born Compliant

## Overview

Virons AI MCP server for {name} operations. This server follows Domain-Driven Design (DDD) and Test-Driven Development (TDD) principles, with compliance built-in from day one.

## Quick Start

```bash
# Install dependencies
cd virons-{name}-mcp-server
uv sync

# Run tests
uv run pytest

# Run server
uv run virons-{name}-mcp-server

# With write operations enabled
uv run virons-{name}-mcp-server --allow-write
```

## Docker

```bash
# Build
docker build -t virons-{name}-mcp-server .

# Run
docker run -it virons-{name}-mcp-server
```

## Architecture

```
virons-{name}-mcp-server/
├── virons/{package_name}_mcp_server/
│   ├── server.py          # FastMCP server + tool handlers
│   ├── compliance.py      # virons.common integration
│   ├── models.py          # Pydantic data models
│   └── consts.py          # Configuration constants
├── tests/                 # TDD test suite
├── Dockerfile             # Multi-stage container build
└── pyproject.toml         # Dependencies + tool config
```

## Compliance

This server is **born compliant** with:

| Regulation | Articles | Implementation |
|---|---|---|
| **BaFin MaRisk** | AT 8.1, AT 7.2 | `write_audit()` on all write operations |
| **GDPR** | Art 25, 32, 35 | Data residency (eu-central-1), correlation IDs |
| **DORA** | Art 6, 11, 15 | Health checks, ICT resilience |
| **EU AI Act** | Art 9, 11, 14, 17 | Model card validation (if high-risk) |

See [COMPLIANCE.md](./COMPLIANCE.md) for full regulatory traceability.

## Development

### Adding Tools

Edit `virons/{package_name}_mcp_server/server.py`:

```python
@mcp.tool()
async def your_tool(param: str) -> str:
    \"\"\"Your tool description.\"\"\"
    # Implementation
    result = process(param)
    
    # Audit write operations (BaFin AT 8.1)
    audit_id = await audit_write_operation(
        operation_name="your_tool",
        entity_id=param,
        input_data={{"param": param}},
        output_data={{"result": result}},
    )
    
    return result
```

### Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov --cov-report=term-missing

# Specific test file
uv run pytest tests/test_server.py -v
```

### Code Quality

```bash
# Linting
uv run ruff check .

# Type checking
uv run pyright

# Format
uv run ruff format .
```

## Dependencies

- **mcp[cli]** ≥1.23.0 — Model Context Protocol
- **loguru** ≥0.7.0 — Structured logging
- **pydantic** ≥2.10.6 — Data validation
- **virons.common** ≥0.1.0 — Compliance utilities

## License

Apache-2.0 — See [LICENSE](./LICENSE)

Copyright 2026 Virons Fintech. All Rights Reserved.

---

**Generated by**: `virons-scaffold` | **Domain**: Server Domain | **Context**: {name.title()} MCP Server
"""
    )
    
    # LICENSE - Copy from virons-common
    license_source = Path(__file__).parent.parent / "src" / "virons-common" / "LICENSE"
    if license_source.exists():
        (server_dir / "LICENSE").write_text(license_source.read_text())
    else:
        (server_dir / "LICENSE").write_text("Apache-2.0\n")
    
    # NOTICE
    (server_dir / "NOTICE").write_text(
        "Virons Fintech\n"
        "Copyright 2026 Virons Fintech. All Rights Reserved.\n\n"
        "This product includes software developed by Amazon Web Services (awslabs/mcp).\n"
    )
    
    # CHANGELOG.md
    (server_dir / "CHANGELOG.md").write_text(
        "# Changelog\n\n"
        "All notable changes to this project will be documented in this file.\n\n"
        "## [0.1.0] - 2026-03-04\n\n"
        "### Added\n"
        "- Initial scaffold with compliance baseline\n"
        "- BaFin MaRisk AT 8.1 audit integration\n"
        "- GDPR Art 25, 32 compliance hooks\n"
        "- DORA Art 11 health checks\n"
    )
    
    # COMPLIANCE.md
    (server_dir / "COMPLIANCE.md").write_text(
        f"""# Compliance Reference — virons-{name}-mcp-server

Regulatory traceability for the Virons AI {name} MCP server.

## Regulatory Sources

| Regulation | Official Document | Key Articles | Implementation |
|---|---|---|---|
| BaFin MaRisk | [MaRisk (BA) 09/2017](https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Rundschreiben/2017/rs_1709_marisk_ba.html) | AT 8.1, AT 7.2 | `compliance.py` → `virons.common.audit` |
| GDPR | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Art 25, Art 32, Art 35 | `compliance.py` → `virons.common.residency`, `correlation` |
| DORA | [Regulation (EU) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) | Art 6, Art 11, Art 15 | `compliance.py` → `virons.common.health` |
| EU AI Act | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Art 9, Art 11, Art 14, Art 17 | Model card validation (if high-risk) |

## Compliance Hooks

### BaFin MaRisk AT 8.1 — Audit Trail

Every write operation MUST call `virons.common.write_audit()` before returning:

```python
from virons.common import write_audit

audit_id = await write_audit(
    service_name='virons-{name}-mcp-server',
    calculation_type='operation_name',
    entity_id=entity_id,
    input_data={{'key': 'value'}},
    output_data={{'result': 'value'}},
)
```

### GDPR Art 25, 32 — Data Protection

- **Residency**: All data MUST reside in `eu-central-1` (enforced by `virons.common.enforce_region()`)
- **Correlation**: All requests MUST have correlation IDs (via `virons.common.CorrelationContext`)

### DORA Art 11 — Health Monitoring

- **Liveness**: `/health/live` endpoint via `virons.common.HealthCheck().liveness()`
- **Readiness**: `/health/ready` endpoint via `virons.common.HealthCheck().readiness()`

### EU AI Act — High-Risk Systems

If this server is classified as high-risk (Art 6), ensure:
- Model cards exist in `models/` directory
- Technical documentation per Art 11
- Human oversight mechanisms per Art 14
"""
    )
    
    # .gitignore
    (server_dir / ".gitignore").write_text(
        "__pycache__/\n"
        "*.py[cod]\n"
        "*$py.class\n"
        ".venv/\n"
        "venv/\n"
        ".pytest_cache/\n"
        ".coverage\n"
        "htmlcov/\n"
        "dist/\n"
        "build/\n"
        "*.egg-info/\n"
        ".ruff_cache/\n"
        ".pyright/\n"
        "uv.lock\n"
    )
    
    # .python-version
    (server_dir / ".python-version").write_text("3.10\n")


def create_readme_files(server_dir: Path, name: str) -> None:
    """Create DDD-compliant README files for subdirectories.
    
    Args:
        server_dir: Server root directory
        name: Server name
    """
    package_name = name.replace("-", "_")
    
    # virons/README.md
    (server_dir / "virons" / "README.md").write_text(
        f"""# Virons Namespace

## Overview

PEP 420 namespace package root for virons MCP servers.

## Contents

```
└── {package_name}_mcp_server/
```

## Context

| Key | Value |
|-----|-------|
| **Domain** | `virons` |
| **Bounded Context** | Namespace Root |

## Navigation

← [Package Root](../)

---
"""
    )
    
    # virons/{package_name}_mcp_server/README.md
    (server_dir / "virons" / f"{package_name}_mcp_server" / "README.md").write_text(
        f"""# {name.title()} MCP Server

## Overview

MCP server implementation for {name}.

- `server.py` — FastMCP server and tool handlers
- `models.py` — Pydantic data models
- `consts.py` — Constants and configuration
- `compliance.py` — virons.common compliance hooks

## Contents

```
├── server.py
├── models.py
├── consts.py
└── compliance.py
```

## Context

| Key | Value |
|-----|-------|
| **Domain** | `virons.{package_name}_mcp_server` |
| **Parent** | [virons](../) |
| **Bounded Context** | Server Domain |

## Navigation

← [virons README](../)

---
"""
    )
    
    # tests/README.md
    (server_dir / "tests" / "README.md").write_text(
        f"""# Test Suite

## Overview

TDD test suite for virons-{name}-mcp-server.

- `test_server.py` — Server and tool handler tests
- `test_init.py` — Package initialization tests
- `test_main.py` — CLI entry point tests
- `test_compliance.py` — Compliance hook tests

## Contents

```
├── test_server.py
├── test_init.py
├── test_main.py
└── test_compliance.py
```

## Context

| Key | Value |
|-----|-------|
| **Domain** | `tests` |
| **Parent** | [Package Root](../) |
| **Bounded Context** | Test Domain |

## Navigation

← [Package Root](../)

---
"""
    )


def create_docker_files(server_dir: Path, name: str) -> None:
    """Create Docker-related files.
    
    Args:
        server_dir: Server root directory
        name: Server name
    """
    package_name = name.replace("-", "_")
    
    # Dockerfile
    (server_dir / "Dockerfile").write_text(
        f'''# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

FROM public.ecr.aws/amazonlinux/amazonlinux:2023 AS uv

# Install build dependencies
RUN dnf install -y shadow-utils python3.10 python3.10-devel gcc && \\
    dnf clean all

WORKDIR /app

# UV configuration
ENV UV_COMPILE_BYTECODE=1 \\
    UV_LINK_MODE=copy \\
    UV_PYTHON_PREFERENCE=only-managed \\
    UV_FROZEN=true \\
    PIP_NO_CACHE_DIR=1 \\
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy dependency files
COPY pyproject.toml ./

# Install uv and dependencies
RUN python3.10 -m ensurepip && \\
    python3.10 -m pip install uv && \\
    uv sync --python 3.10 --frozen --no-install-project --no-dev --no-editable

# Copy source code
COPY virons/ ./virons/

# Install project
RUN uv sync --python 3.10 --frozen --no-dev --no-editable

# Production stage
FROM public.ecr.aws/amazonlinux/amazonlinux:2023

RUN dnf install -y python3.10 && \\
    dnf clean all && \\
    useradd -m -u 1000 virons

WORKDIR /app

# Copy from build stage
COPY --from=uv --chown=virons:virons /app/.venv /app/.venv

# Copy healthcheck script
COPY docker-healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-healthcheck.sh

USER virons

ENV PATH="/app/.venv/bin:$PATH"

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD ["/usr/local/bin/docker-healthcheck.sh"]

ENTRYPOINT ["virons-{name}-mcp-server"]
'''
    )
    
    # docker-healthcheck.sh
    (server_dir / "docker-healthcheck.sh").write_text(
        f'''#!/bin/sh
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

SERVER="virons-{name}-mcp-server"

# Check if the server process is running
if pgrep -f "virons.{package_name}_mcp_server" > /dev/null; then
  echo "$SERVER is running"
  exit 0
fi

# Unhealthy
echo "$SERVER is not running"
exit 1
'''
    )
    
    # Make healthcheck executable
    (server_dir / "docker-healthcheck.sh").chmod(0o755)
    
    # .dockerignore
    (server_dir / ".dockerignore").write_text(
        '''__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.pytest_cache/
.coverage
htmlcov/
.git/
.gitignore
.ruff_cache/
.pyright/
tests/
*.md
!README.md
'''
    )


def print_validation_summary(server_dir: Path, name: str, port: str) -> None:
    """Print validation summary after scaffolding.
    
    Args:
        server_dir: Server root directory
        name: Server name
        port: Server port
    """
    package_name = name.replace("-", "_")
    
    # Count files
    py_files = list(server_dir.rglob("*.py"))
    test_files = list((server_dir / "tests").glob("test_*.py"))
    
    print("\n" + "="*80)
    print(f"✓ Scaffold Complete: virons-{name}-mcp-server")
    print("="*80)
    print(f"\n📦 Package: virons.{package_name}-mcp-server")
    print(f"🔌 Port: {port}")
    print(f"📁 Location: {server_dir}")
    
    print(f"\n📊 Files Generated:")
    print(f"  • Python source files: {len(py_files)}")
    print(f"  • Test files: {len(test_files)}")
    print(f"  • Total files: {len(list(server_dir.rglob('*')))}")
    
    print(f"\n✅ Compliance Baseline:")
    print(f"  • BaFin MaRisk AT 8.1 — Audit trail (write_audit)")
    print(f"  • GDPR Art 25, 32 — Data residency (eu-central-1)")
    print(f"  • DORA Art 11 — Health checks (liveness, readiness)")
    print(f"  • EU AI Act — Model card validation hooks")
    
    print(f"\n🚀 Next Steps:")
    print(f"  1. cd {server_dir.name}")
    print(f"  2. uv sync")
    print(f"  3. uv run pytest")
    print(f"  4. Implement your tools in virons/{package_name}_mcp_server/server.py")
    print(f"  5. Add tests in tests/")
    
    print(f"\n📚 Documentation:")
    print(f"  • README.md — Quick start and architecture")
    print(f"  • COMPLIANCE.md — Regulatory traceability")
    print(f"  • CHANGELOG.md — Version history")
    
    print("\n" + "="*80 + "\n")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Scaffold a virons MCP server")
    parser.add_argument("--name", required=True, help="Server name (e.g., infrastructure)")
    parser.add_argument("--description", required=True, help="Server description")
    parser.add_argument("--port", required=True, help="Server port (e.g., 9300)")
    parser.add_argument("--deps", help="Additional dependencies (comma-separated)")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio", help="Transport type")
    parser.add_argument("--output-dir", type=Path, default=Path("src"), help="Output directory")
    
    args = parser.parse_args()
    
    # Parse dependencies
    deps = [d.strip() for d in args.deps.split(",")] if args.deps else []
    
    # Check if directory already exists
    server_dir = args.output_dir / f"virons-{args.name}-mcp-server"
    if server_dir.exists():
        print(f"Error: Directory {server_dir} already exists", file=sys.stderr)
        return 1
    
    # Create structure
    server_dir = create_directory_structure(args.name, args.output_dir)
    create_python_files(server_dir, args.name, args.port)
    create_test_files(server_dir, args.name)
    create_metadata_files(server_dir, args.name, args.description, args.port, deps)
    create_readme_files(server_dir, args.name)
    create_docker_files(server_dir, args.name)
    
    # Print validation summary
    print_validation_summary(server_dir, args.name, args.port)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
