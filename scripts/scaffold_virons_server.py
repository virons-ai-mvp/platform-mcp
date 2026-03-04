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
    
    # pyproject.toml
    deps_str = "\n".join(f'    "{dep}",' for dep in deps) if deps else ""
    (server_dir / "pyproject.toml").write_text(
        f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "virons.{package_name}-mcp-server"
version = "0.1.0"
description = "{description}"
dependencies = [
    "mcp[cli]>=1.23.0",
    "loguru>=0.7.0",
    "pydantic>=2.0.0",
    "virons.common>=0.1.0",
{deps_str}
]

[project.scripts]
virons-{name}-mcp-server = "virons.{package_name}_mcp_server.server:main"
"""
    )
    
    # README.md
    (server_dir / "README.md").write_text(
        f"# virons-{name}-mcp-server\n\n{description}\n\nPort: {port}\n"
    )
    
    # LICENSE
    (server_dir / "LICENSE").write_text("Apache-2.0\n")
    
    # NOTICE
    (server_dir / "NOTICE").write_text(
        "Virons Fintech\n"
        "Copyright 2026 Virons Fintech. All Rights Reserved.\n\n"
        "This product includes software developed by Amazon Web Services (awslabs/mcp).\n"
    )
    
    # CHANGELOG.md
    (server_dir / "CHANGELOG.md").write_text("# Changelog\n\n## [0.1.0] - 2026-03-04\n- Initial release\n")
    
    # COMPLIANCE.md
    (server_dir / "COMPLIANCE.md").write_text("# Compliance\n\nRegulatory traceability documentation.\n")
    
    # .gitignore
    (server_dir / ".gitignore").write_text("__pycache__/\n*.py[cod]\n.venv/\n.pytest_cache/\n.coverage\n")
    
    # .python-version
    (server_dir / ".python-version").write_text("3.10\n")


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
    
    print(f"✓ Created virons-{args.name}-mcp-server at {server_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
