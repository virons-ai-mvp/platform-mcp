# Integration Testing Guide

**Version**: 1.0
**Last Updated**: 2026-03-07

## Overview

Guidelines for writing integration tests that verify the Virons Infrastructure MCP Server works correctly with external systems.

## Test Scope

### What to Test
- MCP protocol communication
- Upstream MCP server integration (CDK, Terraform, CloudFormation)
- Database operations (RDS)
- S3 audit log storage
- Kubernetes deployment
- FastAPI endpoints

### What Not to Test
- External service internals (tested by their owners)
- Third-party library behavior (trust their tests)

## Test Structure

### File Organization
```
tests/integration/
├── conftest.py              # Integration fixtures
├── test_mcp_protocol.py     # MCP communication
├── test_upstream_servers.py # CDK, Terraform, CFN servers
├── test_database.py         # RDS operations
├── test_s3_storage.py       # S3 audit logs
├── test_api_endpoints.py    # FastAPI routes
└── test_end_to_end.py       # Full workflows
```

## Environment Setup

### Test Environment
```bash
# Set test environment
export ENVIRONMENT=test
export AWS_REGION=eu-central-1
export DB_HOST=test-db.local
export S3_BUCKET=virons-test-audit-logs

# Start test dependencies
docker-compose -f docker-compose.test.yml up -d
```

### Docker Compose for Tests
```yaml
# docker-compose.test.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: virons_test
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    ports:
      - "5432:5432"

  localstack:
    image: localstack/localstack
    environment:
      SERVICES: s3,rds
    ports:
      - "4566:4566"

  cdk-server:
    image: virons/cdk-mcp-server:latest
    ports:
      - "9140:9140"
```

## MCP Protocol Tests

### Test MCP Communication
```python
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@pytest.mark.integration
@pytest.mark.asyncio
async def test_mcp_list_tools():
    """Test listing available MCP tools."""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "virons.infrastructure_mcp_server.server", "--transport", "stdio"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            assert len(tools.tools) > 0
            tool_names = [tool.name for tool in tools.tools]
            assert "deploy_infrastructure" in tool_names
            assert "destroy_infrastructure" in tool_names

@pytest.mark.integration
@pytest.mark.asyncio
async def test_mcp_call_tool():
    """Test calling MCP tool."""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "virons.infrastructure_mcp_server.server", "--transport", "stdio"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_infrastructure_info",
                arguments={}
            )

            assert result.content
            assert "available_tools" in result.content[0].text
```

## Upstream Server Tests

### Test CDK Server Integration
```python
import pytest
import httpx

@pytest.mark.integration
@pytest.mark.asyncio
async def test_cdk_server_deploy():
    """Test deployment via CDK MCP server."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://cdk-server:9140/call-tool",
            json={
                "tool": "deploy",
                "params": {
                    "stack_name": "test-vpc",
                    "region": "eu-central-1",
                }
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

@pytest.mark.integration
@pytest.mark.asyncio
async def test_terraform_server_deploy():
    """Test deployment via Terraform MCP server."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://terraform-server:9142/call-tool",
            json={
                "tool": "apply",
                "params": {
                    "workspace": "test",
                    "region": "eu-central-1",
                }
            }
        )

        assert response.status_code == 200
```

## Database Tests

### Test RDS Operations
```python
import pytest
import asyncpg

@pytest.fixture
async def db_connection():
    """Provide database connection."""
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="test",
        password="test",
        database="virons_test",
    )
    yield conn
    await conn.close()

@pytest.mark.integration
@pytest.mark.asyncio
async def test_audit_log_write(db_connection):
    """Test writing audit log to database."""
    await db_connection.execute("""
        INSERT INTO audit_logs (timestamp, action, user_id, details)
        VALUES ($1, $2, $3, $4)
    """, "2026-03-07T10:00:00Z", "deploy", "user-123", '{"stack": "test"}')

    result = await db_connection.fetchrow(
        "SELECT * FROM audit_logs WHERE user_id = $1",
        "user-123"
    )

    assert result["action"] == "deploy"
    assert result["user_id"] == "user-123"

@pytest.mark.integration
@pytest.mark.asyncio
async def test_audit_log_retention(db_connection):
    """Test audit log retention policy."""
    # Insert old log
    await db_connection.execute("""
        INSERT INTO audit_logs (timestamp, action, user_id, details)
        VALUES ($1, $2, $3, $4)
    """, "2016-03-07T10:00:00Z", "deploy", "user-old", '{}')

    # Verify it exists (10-year retention)
    result = await db_connection.fetchrow(
        "SELECT * FROM audit_logs WHERE user_id = $1",
        "user-old"
    )

    assert result is not None
```

## S3 Storage Tests

### Test S3 Audit Logs
```python
import pytest
import boto3
from moto import mock_s3

@pytest.fixture
def s3_client():
    """Provide mocked S3 client."""
    with mock_s3():
        client = boto3.client("s3", region_name="eu-central-1")
        client.create_bucket(
            Bucket="virons-test-audit-logs",
            CreateBucketConfiguration={"LocationConstraint": "eu-central-1"}
        )
        yield client

@pytest.mark.integration
def test_s3_audit_log_upload(s3_client):
    """Test uploading audit log to S3."""
    s3_client.put_object(
        Bucket="virons-test-audit-logs",
        Key="2026/03/07/audit-log.json",
        Body='{"action": "deploy", "user_id": "user-123"}'
    )

    response = s3_client.get_object(
        Bucket="virons-test-audit-logs",
        Key="2026/03/07/audit-log.json"
    )

    content = response["Body"].read().decode()
    assert "deploy" in content

@pytest.mark.integration
def test_s3_versioning_enabled(s3_client):
    """Test S3 versioning is enabled."""
    s3_client.put_bucket_versioning(
        Bucket="virons-test-audit-logs",
        VersioningConfiguration={"Status": "Enabled"}
    )

    response = s3_client.get_bucket_versioning(
        Bucket="virons-test-audit-logs"
    )

    assert response["Status"] == "Enabled"
```

## API Endpoint Tests

### Test FastAPI Routes
```python
import pytest
from fastapi.testclient import TestClient
from virons.infrastructure_mcp_server.api import app

@pytest.fixture
def client():
    """Provide FastAPI test client."""
    return TestClient(app)

@pytest.mark.integration
def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

@pytest.mark.integration
def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "mcp_tool_duration_seconds" in response.text

@pytest.mark.integration
def test_deploy_endpoint(client):
    """Test deploy endpoint."""
    response = client.post(
        "/api/deploy",
        json={
            "stack_name": "test-stack",
            "tool": "cdk",
            "region": "eu-central-1",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

@pytest.mark.integration
def test_swagger_ui(client):
    """Test Swagger UI is accessible."""
    response = client.get("/api/docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower()
```

## End-to-End Tests

### Test Complete Workflow
```python
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.slow
async def test_deploy_and_destroy_workflow():
    """Test complete deploy and destroy workflow."""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "virons.infrastructure_mcp_server.server", "--transport", "stdio"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Deploy infrastructure
            deploy_result = await session.call_tool(
                "deploy_infrastructure",
                arguments={
                    "stack_name": "test-e2e-stack",
                    "tool": "cdk",
                    "region": "eu-central-1",
                }
            )

            assert "success" in deploy_result.content[0].text

            # List stacks
            list_result = await session.call_tool(
                "list_stacks",
                arguments={"tool": "cdk", "region": "eu-central-1"}
            )

            assert "test-e2e-stack" in list_result.content[0].text

            # Destroy infrastructure
            destroy_result = await session.call_tool(
                "destroy_infrastructure",
                arguments={
                    "stack_name": "test-e2e-stack",
                    "tool": "cdk",
                    "region": "eu-central-1",
                }
            )

            assert "success" in destroy_result.content[0].text
```

## Test Fixtures

### Shared Integration Fixtures
```python
# tests/integration/conftest.py
import pytest
import asyncio
import boto3
from moto import mock_s3, mock_rds

@pytest.fixture(scope="session")
def event_loop():
    """Provide event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def aws_credentials():
    """Provide mocked AWS credentials."""
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

@pytest.fixture
def s3_bucket(aws_credentials):
    """Provide S3 bucket for testing."""
    with mock_s3():
        client = boto3.client("s3", region_name="eu-central-1")
        client.create_bucket(
            Bucket="virons-test-audit-logs",
            CreateBucketConfiguration={"LocationConstraint": "eu-central-1"}
        )
        yield client
```

## Running Integration Tests

### Local Development
```bash
# Start test dependencies
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/ -m integration

# Run with coverage
pytest tests/integration/ -m integration --cov=virons

# Run specific test
pytest tests/integration/test_mcp_protocol.py::test_mcp_list_tools

# Stop test dependencies
docker-compose -f docker-compose.test.yml down
```

### CI/CD
```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests
on: [push, pull_request]
jobs:
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: virons_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pytest tests/integration/ -m integration
```

## Best Practices

### Test Isolation
```python
# Good - clean up after test
@pytest.mark.integration
async def test_with_cleanup(db_connection):
    await db_connection.execute("INSERT INTO audit_logs ...")

    # Test logic

    # Cleanup
    await db_connection.execute("DELETE FROM audit_logs WHERE ...")

# Better - use fixtures for cleanup
@pytest.fixture
async def clean_database(db_connection):
    yield
    await db_connection.execute("TRUNCATE audit_logs")
```

### Test Data Management
```python
# Use factories for test data
class AuditLogFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            "timestamp": "2026-03-07T10:00:00Z",
            "action": "deploy",
            "user_id": "test-user",
            "details": "{}",
        }
        return {**defaults, **kwargs}

@pytest.mark.integration
async def test_with_factory(db_connection):
    log_data = AuditLogFactory.create(action="destroy")
    await db_connection.execute("INSERT INTO audit_logs ...", **log_data)
```

### Retry Flaky Tests
```python
@pytest.mark.integration
@pytest.mark.flaky(reruns=3, reruns_delay=2)
async def test_external_service():
    """Test that may be flaky due to network."""
    response = await client.get("http://external-service/api")
    assert response.status_code == 200
```

## Troubleshooting

### Connection Issues
```bash
# Check services are running
docker-compose -f docker-compose.test.yml ps

# Check logs
docker-compose -f docker-compose.test.yml logs postgres

# Restart services
docker-compose -f docker-compose.test.yml restart
```

### Slow Tests
```python
# Mark slow tests
@pytest.mark.integration
@pytest.mark.slow
async def test_slow_operation():
    pass

# Skip slow tests in development
pytest tests/integration/ -m "integration and not slow"
```

## References

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [moto (AWS Mocking)](https://docs.getmoto.org/)
- [Unit Testing Guide](./unit-tests.md)

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
