# AWS Labs Integration - Quick Reference

## Status: ✅ COMPLETE

### Services Running
```bash
docker-compose ps
# All 5 services healthy
# Infrastructure: 78 tools + 9 AWS Labs tools
```

### Test Connection
```bash
docker exec virons-infrastructure-mcp python -c "
import asyncio
from virons.common import MCPClient

async def test():
    client = MCPClient(
        command='/app/.venv/bin/python',
        args=['-m', 'awslabs.aws_iac_mcp_server.server'],
        server_name='iac'
    )
    await client.connect()
    tools = await client.list_tools()
    print(f'{len(tools)} tools available')
    await client.disconnect()

asyncio.run(test())
"
```

### AWS Labs Tools (9 total)

**Validation**:
- `validate_cloudformation_template`
- `check_cloudformation_template_compliance`

**Troubleshooting**:
- `troubleshoot_cloudformation_deployment`
- `get_cloudformation_pre_deploy_validation_instructions`

**Documentation**:
- `search_cdk_documentation`
- `search_cloudformation_documentation`
- `search_cdk_samples_and_constructs`
- `cdk_best_practices`
- `read_iac_documentation_page`

### Configuration

**Infrastructure MCP** (`server.py:60-66`):
```python
UPSTREAM_CONFIG = {
    "iac": {
        "command": "/app/.venv/bin/python",
        "args": ["-m", "awslabs.aws_iac_mcp_server.server"],
        "description": "AWS IaC MCP Server"
    }
}
```

**Security MCP** (`server.py:45-60`):
```python
UPSTREAM = {
    "cloudtrail": {...},
    "iam": {...},
    "well_architected": {...}
}
```

**Monitoring MCP** (`server.py:45-50`):
```python
UPSTREAM = {
    "cloudwatch": {...}
}
```

### Usage in Code

```python
from virons.common import UpstreamRegistry

# Initialize (once per server)
registry = UpstreamRegistry(UPSTREAM_CONFIG)

# Get client (cached)
client = await registry.get_client("iac")

# Call tool
result = await client.call_tool(
    "validate_cloudformation_template",
    {"template_content": "..."}
)

# Cleanup (on shutdown)
await registry.close_all()
```

### Key Files

- `virons-common/virons/common/mcp_client.py` - STDIO client
- `virons-common/virons/common/upstream_registry.py` - Connection registry
- `virons-infrastructure-mcp-server/Dockerfile` - AWS Labs packages
- `virons-infrastructure-mcp-server/server.py` - Upstream config

### Troubleshooting

**Check logs**:
```bash
docker logs virons-infrastructure-mcp | tail -50
```

**Verify packages**:
```bash
docker exec virons-infrastructure-mcp uv pip list | grep awslabs
```

**Test manually**:
```bash
docker exec virons-infrastructure-mcp /app/.venv/bin/python \
  -m awslabs.aws_iac_mcp_server.server --help
```

### Documentation

- [Complete Integration Guide](./AWSLABS-INTEGRATION-COMPLETE.md)
- [Original Action Plan](./AWSLABS-ACTION-PLAN.md)
- [MCP Client API](../../src/virons-common/virons/common/mcp_client.py)

---

**Integration Method**: Subprocess STDIO (MCP-native)
**Status**: Production Ready ✅
**Date**: 2026-03-08
