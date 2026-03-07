# Operations MCP Server - Infrastructure Tests

## Overview

Tests for external integrations and technical implementations.

## Test Files

```
infrastructure/
├── __init__.py
├── test_eks_client.py          # EKS client tests
├── test_lambda_client.py       # Lambda client tests
├── test_ecs_client.py          # ECS client tests
├── test_deployment_repository.py # Persistence tests
└── test_mcp_adapter.py         # MCP protocol tests
```

## Example Tests

```python
@pytest.mark.asyncio
async def test_eks_client_deploy():
    """Test EKS client deploys service."""
    client = EKSClient("localhost", 9105)
    result = await client.deploy("api", "api:v1.2.3", replicas=3)
    assert result["status"] == "success"

@pytest.mark.asyncio
async def test_eks_client_retry():
    """Test client retries on failure."""
    client = EKSClient("localhost", 9105, max_retries=3)
    with pytest.raises(ConnectionError):
        await client.deploy("invalid", "image:tag")
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
