# Code Style Guide

**Version**: 1.0
**Last Updated**: 2026-03-07
**Applies To**: All Python code in virons-infrastructure-mcp-server

## Overview

This guide defines coding standards for the Virons Infrastructure MCP Server following Domain-Driven Design (DDD) principles.

## Python Version

- **Required**: Python 3.11+
- **Type Hints**: Mandatory for all functions
- **Async**: Use async/await for I/O operations

## Code Formatting

### Black

```bash
# Format code
black virons/ tests/

# Check formatting
black --check virons/ tests/
```

**Configuration** (pyproject.toml):
```toml
[tool.black]
line-length = 100
target-version = ['py311']
```

### isort

```bash
# Sort imports
isort virons/ tests/

# Check imports
isort --check-only virons/ tests/
```

**Configuration** (pyproject.toml):
```toml
[tool.isort]
profile = "black"
line_length = 100
```

## Type Checking

### mypy

```bash
# Type check
mypy virons/

# Strict mode
mypy --strict virons/
```

**Configuration** (pyproject.toml):
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

## Linting

### ruff

```bash
# Lint code
ruff check virons/ tests/

# Fix auto-fixable issues
ruff check --fix virons/ tests/
```

**Configuration** (pyproject.toml):
```toml
[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "W", "B", "C90"]
```

## Naming Conventions

### Files and Modules
```python
# Snake case for files
compliance_logging.py
infrastructure_service.py

# Package names lowercase
virons/infrastructure_mcp_server/
```

### Classes
```python
# PascalCase for classes
class ComplianceLogger:
    pass

class InfrastructureService:
    pass

# Suffix for protocols/interfaces
class ToolProtocol(Protocol):
    pass
```

### Functions and Variables
```python
# Snake case for functions
def deploy_infrastructure(stack_name: str) -> DeployResult:
    pass

# Snake case for variables
user_id = "user-123"
stack_name = "virons-prod"

# Constants in UPPER_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
```

### Private Members
```python
class Service:
    def __init__(self):
        self._private_var = "internal"  # Single underscore
        self.__really_private = "very internal"  # Double underscore (rare)

    def _internal_method(self) -> None:  # Single underscore
        pass
```

## Type Hints

### Required for All Functions
```python
# Good
def deploy_infrastructure(
    stack_name: str,
    region: str,
    timeout: int = 300
) -> DeployResult:
    pass

# Bad - no type hints
def deploy_infrastructure(stack_name, region, timeout=300):
    pass
```

### Complex Types
```python
from typing import Dict, List, Optional, Union
from collections.abc import Sequence

# Use built-in generics (Python 3.11+)
def get_stacks(region: str) -> list[str]:
    pass

def get_config() -> dict[str, str | int]:
    pass

# Optional for nullable values
def find_stack(name: str) -> Optional[Stack]:
    pass

# Use Protocol for interfaces
from typing import Protocol

class ToolProtocol(Protocol):
    def execute(self, params: dict[str, str]) -> str:
        ...
```

## Docstrings

### Google Style
```python
def deploy_infrastructure(
    stack_name: str,
    tool: str,
    region: str,
    timeout: int = 300
) -> DeployResult:
    """Deploy infrastructure using specified IaC tool.

    Args:
        stack_name: Name of the infrastructure stack
        tool: IaC tool to use (cdk, terraform, cloudformation)
        region: AWS region for deployment
        timeout: Deployment timeout in seconds (default: 300)

    Returns:
        DeployResult containing status, outputs, and metadata

    Raises:
        DeploymentError: If deployment fails
        TimeoutError: If deployment exceeds timeout

    Example:
        >>> result = deploy_infrastructure("vpc-stack", "cdk", "eu-central-1")
        >>> print(result.status)
        'success'
    """
    pass
```

### Module Docstrings
```python
"""Infrastructure deployment service.

This module provides the core infrastructure deployment functionality
using multiple IaC tools (CDK, Terraform, CloudFormation).

Typical usage:
    service = InfrastructureService()
    result = await service.deploy("stack-name", "cdk", "eu-central-1")
"""
```

## DDD Architecture

### Layer Structure
```
virons/infrastructure_mcp_server/
├── domain/              # Business logic (pure Python)
│   ├── models.py       # Domain models
│   ├── services.py     # Domain services
│   └── exceptions.py   # Domain exceptions
├── application/         # Use cases
│   ├── deploy_use_case.py
│   └── destroy_use_case.py
├── infrastructure/      # External integrations
│   ├── mcp_client.py   # MCP protocol
│   ├── metrics.py      # Prometheus
│   └── health_server.py
└── server.py           # Entry point
```

### Domain Models
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)  # Immutable
class DeployResult:
    """Domain model for deployment result."""

    stack_name: str
    status: str
    outputs: dict[str, str]
    timestamp: datetime
    duration_ms: int

    def is_success(self) -> bool:
        """Check if deployment succeeded."""
        return self.status == "success"
```

### Domain Services
```python
class InfrastructureService:
    """Domain service for infrastructure operations."""

    def __init__(self, logger: ComplianceLogger):
        self._logger = logger

    async def deploy(
        self,
        stack_name: str,
        tool: str,
        region: str
    ) -> DeployResult:
        """Deploy infrastructure (domain logic)."""
        # Pure business logic, no external dependencies
        pass
```

## Error Handling

### Custom Exceptions
```python
class InfrastructureError(Exception):
    """Base exception for infrastructure operations."""
    pass

class DeploymentError(InfrastructureError):
    """Raised when deployment fails."""
    pass

class ValidationError(InfrastructureError):
    """Raised when validation fails."""
    pass
```

### Exception Handling
```python
# Good - specific exceptions
try:
    result = await deploy_infrastructure(stack_name, tool, region)
except DeploymentError as e:
    logger.error(f"Deployment failed: {e}")
    raise
except TimeoutError:
    logger.error("Deployment timed out")
    raise DeploymentError("Timeout exceeded")

# Bad - bare except
try:
    result = deploy_infrastructure(stack_name, tool, region)
except:  # Don't do this
    pass
```

## Async/Await

### Use for I/O Operations
```python
# Good - async for I/O
async def deploy_infrastructure(stack_name: str) -> DeployResult:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
    return DeployResult(...)

# Bad - blocking I/O
def deploy_infrastructure(stack_name: str) -> DeployResult:
    response = requests.post(url, json=data)  # Blocks
    return DeployResult(...)
```

### Async Context Managers
```python
class MCPClient:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

# Usage
async with MCPClient() as client:
    result = await client.call_tool("deploy", params)
```

## Logging

### Structured Logging
```python
import structlog

logger = structlog.get_logger()

# Good - structured
logger.info(
    "deployment_started",
    stack_name=stack_name,
    tool=tool,
    region=region,
    user_id=user_id
)

# Bad - string formatting
logger.info(f"Deploying {stack_name} with {tool} in {region}")
```

### Compliance Logging
```python
from virons.infrastructure_mcp_server.compliance_logging import ComplianceLogger

logger = ComplianceLogger()

# Always log infrastructure changes
logger.log_infrastructure_change(
    action="deploy",
    details={"stack": stack_name, "tool": tool},
    user_id=user_id
)
```

## Testing

### Test File Naming
```python
# Test files mirror source structure
virons/infrastructure_mcp_server/domain/services.py
tests/domain/test_services.py
```

### Test Function Naming
```python
# Descriptive test names
def test_deploy_infrastructure_success():
    pass

def test_deploy_infrastructure_with_invalid_tool_raises_error():
    pass

def test_deploy_infrastructure_timeout_raises_timeout_error():
    pass
```

### Fixtures
```python
import pytest

@pytest.fixture
def infrastructure_service():
    """Provide InfrastructureService instance."""
    logger = ComplianceLogger()
    return InfrastructureService(logger)

def test_deploy(infrastructure_service):
    result = infrastructure_service.deploy("stack", "cdk", "eu-central-1")
    assert result.is_success()
```

## Code Organization

### Imports
```python
# Standard library
import asyncio
import logging
from datetime import datetime
from typing import Optional

# Third-party
import httpx
import structlog
from fastapi import FastAPI

# Local
from virons.infrastructure_mcp_server.domain.models import DeployResult
from virons.infrastructure_mcp_server.domain.services import InfrastructureService
```

### Class Organization
```python
class InfrastructureService:
    """Service for infrastructure operations."""

    # 1. Class variables
    DEFAULT_TIMEOUT = 300

    # 2. __init__
    def __init__(self, logger: ComplianceLogger):
        self._logger = logger

    # 3. Public methods
    async def deploy(self, stack_name: str) -> DeployResult:
        pass

    async def destroy(self, stack_name: str) -> DestroyResult:
        pass

    # 4. Private methods
    def _validate_stack_name(self, name: str) -> None:
        pass

    # 5. Properties
    @property
    def is_ready(self) -> bool:
        return True
```

## Security

### No Secrets in Code
```python
# Good - from environment
import os
api_key = os.getenv("API_KEY")

# Bad - hardcoded
api_key = "sk-1234567890"  # Never do this
```

### Input Validation
```python
def deploy_infrastructure(stack_name: str, tool: str) -> DeployResult:
    # Validate inputs
    if not stack_name or not stack_name.strip():
        raise ValidationError("Stack name required")

    if tool not in ["cdk", "terraform", "cloudformation"]:
        raise ValidationError(f"Invalid tool: {tool}")

    # Proceed with deployment
    pass
```

## Performance

### Use Generators
```python
# Good - generator (memory efficient)
def get_all_stacks() -> Iterator[Stack]:
    for stack in query_stacks():
        yield stack

# Bad - list (loads all in memory)
def get_all_stacks() -> list[Stack]:
    return [stack for stack in query_stacks()]
```

### Avoid Premature Optimization
```python
# Good - clear and simple
def calculate_score(values: list[float]) -> float:
    return sum(values) / len(values)

# Bad - premature optimization
def calculate_score(values: list[float]) -> float:
    # Complex optimization that's hard to read
    pass
```

## Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.1
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
```

## Code Review Checklist

- [ ] Type hints on all functions
- [ ] Docstrings for public functions
- [ ] Tests for new functionality
- [ ] No hardcoded secrets
- [ ] Input validation
- [ ] Error handling
- [ ] Compliance logging (if infrastructure change)
- [ ] Black formatted
- [ ] isort sorted
- [ ] mypy passes
- [ ] ruff passes

## References

- [PEP 8](https://peps.python.org/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black Documentation](https://black.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
