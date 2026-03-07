# Operations MCP Server - Application Tests

## Overview

Tests for application layer use cases and orchestration.

## Test Files

```
application/
├── __init__.py
├── test_deploy_service.py      # Deployment tests
├── test_rollback_service.py    # Rollback tests
├── test_scale_service.py       # Scaling tests
└── test_status_service.py      # Status aggregation tests
```

## Example Tests

```python
@pytest.mark.asyncio
async def test_deploy_service_orchestrates_platforms():
    """Test that deploy service coordinates multiple platforms."""
    service = DeployService(mock_eks, mock_ecs, mock_lambda)
    result = await service.deploy("eks", "api", "api:v1.2.3")
    
    assert result.status == "completed"
    assert result.health_status == "healthy"
    assert result.replicas == 3
```

## Running

```bash
pytest tests/application/ -v
```

## Navigation

← [Tests](../)
