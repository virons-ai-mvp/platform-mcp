# virons-infrastructure-mcp-server Implementation

**Status**: ✅ Scaffolded & Tested  
**Date**: 2026-03-05  
**Port**: 9140-9143  

## Overview

Infrastructure orchestrator MCP server that wraps official AWS MCP servers:
- **CDK** (9140) - AWS Cloud Development Kit
- **CloudFormation** (9141) - AWS CloudFormation
- **Terraform** (9142) - Terraform IaC
- **IaC** (9143) - Generic Infrastructure as Code

## Implementation Status

### ✅ Completed

1. **Scaffold Generated**
   - Package structure: `virons.infrastructure-mcp-server`
   - FastMCP server template
   - Compliance hooks (BaFin AT 8.1, GDPR, DORA)
   - Test suite (5 tests, all passing)

2. **Orchestrator Tools Implemented**
   - `deploy_infrastructure()` - Deploy stacks with audit trail
   - `list_stacks()` - List deployed stacks
   - `destroy_infrastructure()` - Destroy stacks with audit trail

3. **Compliance**
   - BaFin AT 8.1: Audit trail on all write operations
   - GDPR Art 25: EU data residency enforcement
   - DORA Art 11: Health check hooks

4. **Tests**
   ```bash
   ============================= 5 passed in 0.37s =============================
   ```

### 🚧 TODO

1. **Upstream MCP Integration**
   - Connect to official AWS MCP servers (CDK, CFN, Terraform, IaC)
   - Implement HTTP/stdio client for upstream calls
   - Add retry logic and error handling

2. **Helm Chart**
   - Create Kubernetes deployment manifests
   - Configure service mesh integration
   - Define IAM policies

3. **Documentation**
   - Architecture Decision Records (ADRs)
   - API documentation
   - Runbooks

## Tools

### deploy_infrastructure

Deploy infrastructure using CDK, CloudFormation, Terraform, or IaC.

**Parameters**:
- `tool`: IaC tool (cdk|cfn|terraform|iac)
- `stack_name`: Stack/deployment name
- `template_path`: Path to template/config
- `parameters`: Deployment parameters (optional)

**Returns**:
```json
{
  "status": "deployed",
  "stack_name": "my-stack",
  "tool": "cdk",
  "audit_id": "uuid"
}
```

### list_stacks

List deployed stacks for a given tool.

**Parameters**:
- `tool`: IaC tool (cdk|cfn|terraform|iac)

**Returns**:
```json
{
  "tool": "cdk",
  "stacks": []
}
```

### destroy_infrastructure

Destroy infrastructure with audit trail.

**Parameters**:
- `tool`: IaC tool (cdk|cfn|terraform|iac)
- `stack_name`: Stack name to destroy

**Returns**:
```json
{
  "status": "destroyed",
  "stack_name": "my-stack",
  "tool": "cdk",
  "audit_id": "uuid"
}
```

## Usage

### Local Development

```bash
# Install dependencies
cd src/virons-infrastructure-mcp-server
uv sync

# Run tests
uv run pytest -v

# Run server (stdio mode)
uv run virons-infrastructure-mcp-server

# Run server with write operations
uv run virons-infrastructure-mcp-server --allow-write

# Run server (HTTP mode for K8s)
uv run virons-infrastructure-mcp-server --transport http
```

### Docker

```bash
# Build
docker build -t virons-infrastructure-mcp-server .

# Run
docker run -it virons-infrastructure-mcp-server
```

## Architecture

```
virons-infrastructure-mcp-server (9140-9143)
├── Orchestrator Layer
│   ├── deploy_infrastructure()
│   ├── list_stacks()
│   └── destroy_infrastructure()
├── Compliance Layer
│   ├── audit_write_operation() (BaFin AT 8.1)
│   └── setup_compliance_hooks() (GDPR, DORA)
└── Upstream Layer (TODO)
    ├── cdk-mcp-server (9140)
    ├── cfn-mcp-server (9141)
    ├── terraform-mcp-server (9142)
    └── iac-mcp-server (9143)
```

## Compliance

| Regulation | Article | Implementation |
|---|---|---|
| BaFin MaRisk | AT 8.1 | `audit_write_operation()` on deploy/destroy |
| GDPR | Art 25, 32 | Data residency (eu-central-1) |
| DORA | Art 11 | Health check hooks |

## Next Steps

1. **Implement upstream MCP client** - Connect to official AWS MCP servers
2. **Create Helm chart** - Deploy to Kubernetes
3. **Add integration tests** - Test with real AWS MCP servers
4. **Document ADRs** - Architecture decisions
5. **Add monitoring** - Prometheus metrics, CloudWatch logs

---

**Generated**: 2026-03-05  
**Maintained By**: Virons Fintech Engineering Team
