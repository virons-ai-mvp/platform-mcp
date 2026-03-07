# Security MCP Server - Infrastructure Tests

## Overview

Tests for external integrations and technical implementations.

## Test Files

```
infrastructure/
├── __init__.py
├── test_gitleaks_client.py      # Gitleaks client tests
├── test_cloudtrail_client.py    # CloudTrail client tests
├── test_iam_client.py           # IAM client tests
├── test_audit_repository.py     # Audit persistence tests
└── test_mcp_adapter.py          # MCP protocol tests
```

## Example Tests

```python
@pytest.mark.asyncio
async def test_gitleaks_client_connection():
    """Test Gitleaks client connects to upstream."""
    client = GitleaksClient("localhost", 9100)
    health = await client.health_check()
    assert health["status"] == "healthy"

@pytest.mark.asyncio
async def test_gitleaks_client_retry():
    """Test client retries on failure."""
    client = GitleaksClient("localhost", 9100, max_retries=3)
    with pytest.raises(ConnectionError):
        await client.scan("/invalid/path")
    assert client.retry_count == 3
```

## Running

```bash
pytest tests/infrastructure/ -v

# With real upstreams
pytest tests/infrastructure/ -v --integration
```

## Navigation

← [Tests](../)
