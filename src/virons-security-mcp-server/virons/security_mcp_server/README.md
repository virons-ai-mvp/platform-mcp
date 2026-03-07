# Security MCP Server - Core Implementation

## Overview

Security orchestration layer coordinating 5 upstream MCP servers for comprehensive security analysis.

## Structure

```
security_mcp_server/
├── application/       # Use cases (future: orchestration logic)
├── domain/           # Business logic (future: security rules)
├── infrastructure/   # External integrations (future: upstream clients)
├── server.py         # FastMCP server (stdio/http/api modes)
├── compliance.py     # Audit logging
├── consts.py         # Constants
├── models.py         # Data models
└── tool_metadata.py  # Tool enrichment with examples
```

## Key Files

**server.py** - Main entry point
- FastMCP server with 4 tools
- API mode: FastAPI + Swagger + /tools endpoint
- Middleware: correlation ID, Prometheus metrics
- Health endpoints: /health, /ready, /metrics

**tool_metadata.py** - Tool enrichment
- Real examples for each tool
- Category: security
- Input/output schemas

**compliance.py** - Audit trail
- write_audit() for all write operations
- Immutable audit logs

## Tools

```python
@server.tool()
async def scan_secrets(repository_path: str, scan_history: bool = False)
  # Scan repository for secrets using Gitleaks

@server.tool()
async def audit_cloudtrail(start_time: str, end_time: str, event_name: str = None)
  # Query CloudTrail audit logs

@server.tool()
async def check_iam_policy(policy_document: dict, resource_type: str)
  # Validate IAM policy against security best practices

@server.tool()
async def run_compliance_gate(artifact_path: str, gate_type: str)
  # Run compliance gate checks (pre-commit/pre-deploy/post-deploy)
```

## Upstreams

```python
UPSTREAM = {
    "cloudtrail": {"host": "localhost", "port": 9102},
    "iam": {"host": "localhost", "port": 9103},
    "well-architected": {"host": "localhost", "port": 9104},
    "gitleaks": {"host": "localhost", "port": 9100},
    "compliance-gate": {"host": "localhost", "port": 9101},
}
```

## Navigation

← [Security MCP Server](../..)  
→ [Application Layer](application/)  
→ [Domain Layer](domain/)  
→ [Infrastructure Layer](infrastructure/)
