# Security MCP Server - Infrastructure Layer

## Overview

External integrations and technical implementations for security tools.

## Future Structure

```
infrastructure/
├── __init__.py
├── clients/
│   ├── gitleaks_client.py      # Gitleaks MCP client
│   ├── cloudtrail_client.py    # CloudTrail MCP client
│   ├── iam_client.py           # IAM MCP client
│   ├── well_architected_client.py
│   └── compliance_gate_client.py
├── repositories/
│   └── audit_repository.py     # Audit log persistence
└── adapters/
    └── mcp_adapter.py          # MCP protocol adapter
```

## Responsibilities

- Connect to upstream MCP servers
- Handle MCP protocol communication
- Retry logic and circuit breakers
- Audit log persistence

## Example Client

```python
class GitleaksClient:
    def __init__(self, host: str, port: int):
        self.base_url = f"http://{host}:{port}"
    
    async def scan(self, repo_path: str, scan_history: bool = False):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tools/scan",
                json={"path": repo_path, "history": scan_history}
            )
            return response.json()
```

## Upstreams

| Service | Port | Purpose |
|---------|------|---------|
| gitleaks | 9100 | Secret scanning |
| compliance-gate | 9101 | Compliance checks |
| cloudtrail | 9102 | Audit logs |
| iam | 9103 | IAM validation |
| well-architected | 9104 | Security best practices |

## Navigation

← [Core Implementation](../)
