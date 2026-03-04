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


def create_python_files(server_dir: Path, name: str) -> None:
    """Create Python source files.
    
    Args:
        server_dir: Server root directory
        name: Server name
    """
    package_name = name.replace("-", "_")
    pkg_dir = server_dir / "virons" / f"{package_name}_mcp_server"
    
    # Create __init__.py files
    (server_dir / "virons" / "__init__.py").write_text(
        "# PEP 420 namespace package\n"
        "__path__ = __import__('pkgutil').extend_path(__path__, __name__)\n"
    )
    
    (pkg_dir / "__init__.py").write_text(
        f'"""virons.{package_name}_mcp_server — Virons {name.title()} MCP Server."""\n\n'
        "__version__ = '0.1.0'\n"
    )
    
    # Create placeholder files
    (pkg_dir / "server.py").write_text("# Server implementation\n")
    (pkg_dir / "models.py").write_text("# Pydantic models\n")
    (pkg_dir / "consts.py").write_text("# Constants\n")
    (pkg_dir / "compliance.py").write_text("# Compliance hooks\n")


def create_test_files(server_dir: Path) -> None:
    """Create test files.
    
    Args:
        server_dir: Server root directory
    """
    tests_dir = server_dir / "tests"
    
    for test_file in ["test_server.py", "test_init.py", "test_main.py", "test_compliance.py"]:
        (tests_dir / test_file).write_text(f"# Tests for {test_file[5:-3]}\n")


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
    
    # README.md
    (server_dir / "README.md").write_text(
        f"# virons-{name}-mcp-server\n\n{description}\n\n"
        f"**Port**: {port}\n\n"
        f"## Compliance\n\n"
        f"This server is born compliant with:\n"
        f"- BaFin MaRisk AT 8.1 (audit trail)\n"
        f"- GDPR Art 25, 32 (data protection, security)\n"
        f"- DORA Art 11 (ICT resilience)\n"
        f"- EU AI Act Art 9, 11, 14, 17 (high-risk AI systems)\n\n"
        f"See [COMPLIANCE.md](./COMPLIANCE.md) for regulatory traceability.\n"
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
    create_python_files(server_dir, args.name)
    create_test_files(server_dir)
    create_metadata_files(server_dir, args.name, args.description, args.port, deps)
    create_readme_files(server_dir, args.name)
    
    print(f"✓ Created virons-{args.name}-mcp-server at {server_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
