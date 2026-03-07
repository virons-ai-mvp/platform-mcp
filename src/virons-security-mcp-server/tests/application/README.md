# Security MCP Server - Application Tests

## Overview

Tests for application layer use cases and orchestration.

## Test Files

```
application/
├── __init__.py
├── test_scan_service.py      # Secret scanning tests
├── test_audit_service.py     # Audit query tests
├── test_iam_service.py       # IAM validation tests
└── test_gate_service.py      # Compliance gate tests
```

## Example Tests

```python
@pytest.mark.asyncio
async def test_scan_service_aggregates_results():
    """Test that scan service aggregates Gitleaks + compliance results."""
    service = ScanService(mock_gitleaks, mock_compliance)
    result = await service.scan_repository("/path/to/repo")
    
    assert result.secrets_found > 0
    assert result.violations_count > 0
    assert result.risk_score is not None
```

## Running

```bash
pytest tests/application/ -v
```

## Navigation

← [Tests](../)
