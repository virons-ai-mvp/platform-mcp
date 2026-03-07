# Security MCP Server - Application Layer

## Overview

Use cases and orchestration logic for security operations. Currently minimal - tools are registered directly in server.py.

## Future Structure

```
application/
├── __init__.py
├── scan_service.py      # Secret scanning orchestration
├── audit_service.py     # CloudTrail audit queries
├── iam_service.py       # IAM policy validation
└── gate_service.py      # Compliance gate execution
```

## Responsibilities

- Coordinate calls to multiple upstream servers
- Aggregate results from different security tools
- Apply business rules (e.g., severity thresholds)
- Handle retries and error recovery

## Example Pattern

```python
class ScanService:
    def __init__(self, gitleaks_client, compliance_client):
        self.gitleaks = gitleaks_client
        self.compliance = compliance_client
    
    async def scan_repository(self, repo_path: str) -> ScanResult:
        # 1. Scan with Gitleaks
        secrets = await self.gitleaks.scan(repo_path)
        
        # 2. Check compliance rules
        violations = await self.compliance.check(secrets)
        
        # 3. Aggregate results
        return ScanResult(secrets=secrets, violations=violations)
```

## Navigation

← [Core Implementation](../)
