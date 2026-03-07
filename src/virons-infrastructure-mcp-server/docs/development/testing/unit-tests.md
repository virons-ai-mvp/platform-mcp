# Unit Testing Guide

**Version**: 1.0
**Last Updated**: 2026-03-07
**Target Coverage**: 88%+

## Overview

Guidelines for writing unit tests for the Virons Infrastructure MCP Server.

## Test Framework

### pytest
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=virons --cov-report=html

# Run specific test
pytest tests/domain/test_services.py::test_deploy_success

# Run with verbose output
pytest -v

# Run failed tests only
pytest --lf
```

## Test Structure

### File Organization
```
tests/
├── conftest.py              # Shared fixtures
├── domain/
│   ├── test_models.py
│   └── test_services.py
├── application/
│   └── test_use_cases.py
├── infrastructure/
│   ├── test_mcp_client.py
│   └── test_metrics.py
└── test_server.py
```

### Test Naming
```python
# Pattern: test_<function>_<scenario>_<expected>

def test_deploy_infrastructure_with_valid_params_returns_success():
    pass

def test_deploy_infrastructure_with_invalid_tool_raises_error():
    pass

def test_deploy_infrastructure_with_timeout_raises_timeout_error():
    pass
```

## Writing Tests

### Basic Test
```python
import pytest
from virons.infrastructure_mcp_server.domain.services import InfrastructureService

def test_deploy_infrastructure_success():
    """Test successful infrastructure deployment."""
    # Arrange
    service = InfrastructureService()
    stack_name = "test-stack"
    tool = "cdk"
    region = "eu-central-1"

    # Act
    result = service.deploy(stack_name, tool, region)

    # Assert
    assert result.status == "success"
    assert result.stack_name == stack_name
```

### Using Fixtures
```python
# conftest.py
import pytest
from virons.infrastructure_mcp_server.compliance_logging import ComplianceLogger
from virons.infrastructure_mcp_server.domain.services import InfrastructureService

@pytest.fixture
def compliance_logger():
    """Provide ComplianceLogger instance."""
    return ComplianceLogger()

@pytest.fixture
def infrastructure_service(compliance_logger):
    """Provide InfrastructureService instance."""
    return InfrastructureService(compliance_logger)

# test_services.py
def test_deploy(infrastructure_service):
    result = infrastructure_service.deploy("stack", "cdk", "eu-central-1")
    assert result.is_success()
```

### Parametrized Tests
```python
import pytest

@pytest.mark.parametrize("tool,expected", [
    ("cdk", True),
    ("terraform", True),
    ("cloudformation", True),
    ("invalid", False),
])
def test_validate_tool(tool, expected):
    """Test tool validation with various inputs."""
    result = validate_tool(tool)
    assert result == expected

@pytest.mark.parametrize("stack_name,tool,region", [
    ("vpc-stack", "cdk", "eu-central-1"),
    ("eks-cluster", "terraform", "us-east-1"),
    ("rds-instance", "cloudformation", "ap-southeast-1"),
])
def test_deploy_various_stacks(stack_name, tool, region, infrastructure_service):
    """Test deployment with various configurations."""
    result = infrastructure_service.deploy(stack_name, tool, region)
    assert result.is_success()
```

## Mocking

### Using unittest.mock
```python
from unittest.mock import Mock, patch, MagicMock

def test_deploy_with_mocked_client():
    """Test deployment with mocked MCP client."""
    # Mock the MCP client
    mock_client = Mock()
    mock_client.call_tool.return_value = {"status": "success"}

    service = InfrastructureService(client=mock_client)
    result = service.deploy("stack", "cdk", "eu-central-1")

    # Verify mock was called
    mock_client.call_tool.assert_called_once_with(
        "deploy",
        {"stack_name": "stack", "tool": "cdk", "region": "eu-central-1"}
    )
    assert result.is_success()
```

### Patching
```python
@patch('virons.infrastructure_mcp_server.infrastructure.mcp_client.MCPClient')
def test_deploy_with_patched_client(mock_client_class):
    """Test deployment with patched client class."""
    # Configure mock
    mock_instance = mock_client_class.return_value
    mock_instance.call_tool.return_value = {"status": "success"}

    service = InfrastructureService()
    result = service.deploy("stack", "cdk", "eu-central-1")

    assert result.is_success()
```

### pytest-mock
```python
def test_deploy_with_mocker(mocker, infrastructure_service):
    """Test deployment using pytest-mock."""
    # Mock method
    mock_call = mocker.patch.object(
        infrastructure_service,
        '_call_mcp_tool',
        return_value={"status": "success"}
    )

    result = infrastructure_service.deploy("stack", "cdk", "eu-central-1")

    assert result.is_success()
    mock_call.assert_called_once()
```

## Async Tests

### Testing Async Functions
```python
import pytest

@pytest.mark.asyncio
async def test_async_deploy():
    """Test async deployment."""
    service = InfrastructureService()
    result = await service.deploy_async("stack", "cdk", "eu-central-1")
    assert result.is_success()

@pytest.mark.asyncio
async def test_async_with_fixture(infrastructure_service):
    """Test async with fixture."""
    result = await infrastructure_service.deploy_async("stack", "cdk", "eu-central-1")
    assert result.is_success()
```

### Async Fixtures
```python
@pytest.fixture
async def async_client():
    """Provide async MCP client."""
    client = AsyncMCPClient()
    await client.connect()
    yield client
    await client.disconnect()

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    """Test with async fixture."""
    result = await async_client.call_tool("deploy", {})
    assert result["status"] == "success"
```

## Exception Testing

### Testing Exceptions
```python
import pytest
from virons.infrastructure_mcp_server.domain.exceptions import DeploymentError

def test_deploy_with_invalid_tool_raises_error():
    """Test that invalid tool raises DeploymentError."""
    service = InfrastructureService()

    with pytest.raises(DeploymentError) as exc_info:
        service.deploy("stack", "invalid-tool", "eu-central-1")

    assert "Invalid tool" in str(exc_info.value)

def test_deploy_timeout_raises_timeout_error():
    """Test that timeout raises TimeoutError."""
    service = InfrastructureService(timeout=1)

    with pytest.raises(TimeoutError):
        service.deploy("slow-stack", "cdk", "eu-central-1")
```

## Test Data

### Using Factories
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DeployResultFactory:
    """Factory for creating test DeployResult instances."""

    @staticmethod
    def create(
        stack_name: str = "test-stack",
        status: str = "success",
        outputs: dict[str, str] | None = None,
    ) -> DeployResult:
        return DeployResult(
            stack_name=stack_name,
            status=status,
            outputs=outputs or {},
            timestamp=datetime.utcnow(),
            duration_ms=1000,
        )

def test_with_factory():
    """Test using factory."""
    result = DeployResultFactory.create(status="failed")
    assert not result.is_success()
```

### Using Fixtures for Test Data
```python
@pytest.fixture
def sample_deploy_params():
    """Provide sample deployment parameters."""
    return {
        "stack_name": "test-stack",
        "tool": "cdk",
        "region": "eu-central-1",
        "timeout": 300,
    }

def test_with_sample_data(sample_deploy_params, infrastructure_service):
    """Test with sample data."""
    result = infrastructure_service.deploy(**sample_deploy_params)
    assert result.is_success()
```

## Coverage

### Measuring Coverage
```bash
# Run with coverage
pytest --cov=virons --cov-report=term-missing

# Generate HTML report
pytest --cov=virons --cov-report=html
open htmlcov/index.html

# Check coverage threshold
pytest --cov=virons --cov-fail-under=88
```

### Coverage Configuration
```toml
# pyproject.toml
[tool.coverage.run]
source = ["virons"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

## Best Practices

### AAA Pattern
```python
def test_deploy_infrastructure():
    """Test infrastructure deployment."""
    # Arrange - Set up test data and dependencies
    service = InfrastructureService()
    stack_name = "test-stack"

    # Act - Execute the function under test
    result = service.deploy(stack_name, "cdk", "eu-central-1")

    # Assert - Verify the results
    assert result.is_success()
    assert result.stack_name == stack_name
```

### One Assertion Per Test
```python
# Good - focused test
def test_deploy_returns_success_status():
    result = service.deploy("stack", "cdk", "eu-central-1")
    assert result.status == "success"

def test_deploy_returns_correct_stack_name():
    result = service.deploy("stack", "cdk", "eu-central-1")
    assert result.stack_name == "stack"

# Acceptable - related assertions
def test_deploy_result_structure():
    result = service.deploy("stack", "cdk", "eu-central-1")
    assert result.status == "success"
    assert result.stack_name == "stack"
    assert isinstance(result.outputs, dict)
```

### Test Independence
```python
# Good - independent tests
def test_deploy_first_stack():
    result = service.deploy("stack-1", "cdk", "eu-central-1")
    assert result.is_success()

def test_deploy_second_stack():
    result = service.deploy("stack-2", "cdk", "eu-central-1")
    assert result.is_success()

# Bad - tests depend on each other
def test_deploy_and_destroy():
    deploy_result = service.deploy("stack", "cdk", "eu-central-1")
    destroy_result = service.destroy("stack", "cdk", "eu-central-1")
    # Second test depends on first
```

### Descriptive Test Names
```python
# Good - clear what's being tested
def test_deploy_infrastructure_with_valid_cdk_stack_returns_success():
    pass

def test_deploy_infrastructure_with_nonexistent_region_raises_error():
    pass

# Bad - unclear
def test_deploy():
    pass

def test_error():
    pass
```

## Common Patterns

### Testing Domain Models
```python
from virons.infrastructure_mcp_server.domain.models import DeployResult

def test_deploy_result_is_immutable():
    """Test that DeployResult is immutable."""
    result = DeployResult(
        stack_name="test",
        status="success",
        outputs={},
        timestamp=datetime.utcnow(),
        duration_ms=1000,
    )

    with pytest.raises(AttributeError):
        result.status = "failed"

def test_deploy_result_is_success():
    """Test is_success method."""
    success_result = DeployResult(status="success", ...)
    failed_result = DeployResult(status="failed", ...)

    assert success_result.is_success()
    assert not failed_result.is_success()
```

### Testing Services
```python
def test_infrastructure_service_deploy(mocker):
    """Test InfrastructureService.deploy."""
    # Mock dependencies
    mock_logger = mocker.Mock()
    mock_client = mocker.Mock()
    mock_client.call_tool.return_value = {"status": "success"}

    service = InfrastructureService(logger=mock_logger, client=mock_client)
    result = service.deploy("stack", "cdk", "eu-central-1")

    # Verify interactions
    mock_client.call_tool.assert_called_once()
    mock_logger.log_infrastructure_change.assert_called_once()
    assert result.is_success()
```

### Testing Compliance Logging
```python
def test_compliance_logging_on_deploy(mocker):
    """Test that deployment logs compliance entry."""
    mock_logger = mocker.Mock()
    service = InfrastructureService(logger=mock_logger)

    service.deploy("stack", "cdk", "eu-central-1")

    mock_logger.log_infrastructure_change.assert_called_once_with(
        action="deploy",
        details=mocker.ANY,
        user_id=mocker.ANY,
    )
```

## Running Tests

### Local Development
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=virons

# Run specific module
pytest tests/domain/

# Run specific test
pytest tests/domain/test_services.py::test_deploy_success

# Run with markers
pytest -m "not slow"

# Run in parallel
pytest -n auto
```

### CI/CD
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pytest --cov=virons --cov-fail-under=88
```

## Troubleshooting

### Slow Tests
```python
# Mark slow tests
@pytest.mark.slow
def test_slow_operation():
    pass

# Skip slow tests
pytest -m "not slow"
```

### Flaky Tests
```python
# Retry flaky tests
@pytest.mark.flaky(reruns=3)
def test_flaky_operation():
    pass
```

### Debugging Tests
```python
# Add breakpoint
def test_debug():
    result = service.deploy("stack", "cdk", "eu-central-1")
    breakpoint()  # Debugger will stop here
    assert result.is_success()

# Run with pdb
pytest --pdb
```

## References

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Code Style Guide](../contributing/code-style.md)
- [Integration Testing Guide](./integration-tests.md)

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
