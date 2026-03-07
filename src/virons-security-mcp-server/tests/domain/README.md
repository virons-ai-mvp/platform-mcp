# Security MCP Server - Domain Tests

## Overview

Tests for domain entities, rules, and business logic.

## Test Files

```
domain/
├── __init__.py
├── test_entities.py         # Entity validation tests
├── test_secret_rules.py     # Secret detection rules
├── test_iam_rules.py        # IAM policy rules
└── test_risk_scoring.py     # Risk calculation tests
```

## Example Tests

```python
def test_secret_entity_validation():
    """Test Secret entity validates required fields."""
    secret = Secret(
        type="api_key",
        location="config.py:42",
        severity="high",
        confidence=0.95
    )
    assert secret.is_valid()
    assert secret.requires_remediation()

def test_iam_policy_risk_score():
    """Test IAM policy risk scoring."""
    policy = IAMPolicy(document={"Statement": [...]})
    score = policy.calculate_risk_score()
    assert 0 <= score <= 100
```

## Running

```bash
pytest tests/domain/ -v
```

## Navigation

← [Tests](../)
