# Operations MCP Server - Domain Tests

## Overview

Tests for domain entities, strategies, and business logic.

## Test Files

```
domain/
├── __init__.py
├── test_entities.py            # Entity validation tests
├── test_deployment_strategies.py # Strategy tests
└── test_deployment_manager.py  # Manager logic tests
```

## Example Tests

```python
def test_deployment_entity_validation():
    """Test Deployment entity validates required fields."""
    deployment = Deployment(
        service_name="api",
        platform="eks",
        image="api:v1.2.3",
        replicas=3,
        strategy="blue-green"
    )
    assert deployment.is_valid()
    assert deployment.requires_approval() == False

def test_blue_green_strategy():
    """Test blue-green deployment strategy."""
    strategy = BlueGreenStrategy()
    steps = strategy.plan_deployment(service="api", new_version="v2")
    assert len(steps) == 4  # deploy green, test, switch, cleanup blue
```

## Running

```bash
pytest tests/domain/ -v
```

## Navigation

← [Tests](../)
