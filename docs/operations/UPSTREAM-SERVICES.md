# Upstream Services Configuration

## Current Status

✅ **MCP Platform is operational** - All 90 tools are callable via HTTP
⚠️  **10 upstream services missing** - Tools requiring these will fail gracefully

## Running Services

| Service | Port | Status | Used By |
|---------|------|--------|---------|
| gitleaks | 9100 | ✅ Running | security-mcp |
| kubernetes | 9200 | ✅ Running | operations-mcp |
| helm | 9201 | ⚠️  HTTP 404 | operations-mcp |
| prometheus | 9300 | ✅ Running | monitoring-mcp |

## Missing Services

### Infrastructure MCP (4 services)
- **cdk** (port 9140) - AWS CDK MCP server
- **cfn** (port 9141) - CloudFormation MCP server
- **terraform** (port 9142) - Terraform MCP server
- **iac** (port 9143) - IaC MCP server

### Security MCP (4 services)
- **cloudtrail** (port 9102) - CloudTrail MCP server
- **iam** (port 9103) - IAM MCP server
- **well-architected** (port 9104) - Well-Architected MCP server
- **compliance-gate** (port 9101) - Compliance Gate MCP server

### Monitoring MCP (2 services)
- **grafana** (port 9301) - Grafana MCP server
- **elasticsearch** (port 9302) - Elasticsearch MCP server

## Impact

### Tools That Work Without Upstreams
- All gateway aggregation tools
- Health checks and metrics
- Tool discovery and introspection
- Direct tool execution (returns graceful errors)

### Tools That Require Upstreams
- Infrastructure deployment (deploy_infrastructure, list_stacks, etc.)
- Security scanning (scan_secrets works, others need upstreams)
- Some monitoring queries (prometheus works, grafana/elasticsearch don't)

## Deployment Options

### Option 1: Deploy AWS Labs MCP Servers (Recommended)

AWS Labs provides official MCP servers for AWS services:
- https://github.com/aws/aws-mcp-servers

```bash
# Clone AWS MCP servers
git clone https://github.com/aws/aws-mcp-servers.git

# Deploy each required server
cd aws-mcp-servers/cdk
npm install && npm start -- --port 9140

# Repeat for cfn, terraform, iac, cloudtrail, iam, etc.
```

### Option 2: Mock Mode (Development)

Configure servers to work standalone without upstreams:

```bash
# Set environment variable
export MCP_MOCK_UPSTREAMS=true

# Restart services
docker-compose restart
```

**Note**: Mock mode not yet implemented. Would require:
1. Add mock upstream client that returns synthetic data
2. Configure via environment variable
3. Update each server to check for mock mode

### Option 3: Accept Graceful Failures (Current)

✅ **This is the current state** - Tools are callable but return errors when upstreams are missing.

**Advantages**:
- Platform is fully operational
- Tools fail gracefully with clear error messages
- No additional deployment required
- Easy to add upstreams later

**Example Error**:
```json
{
  "error": "Error executing tool list_stacks: Connection failed: object _AsyncGeneratorContextManager can't be used in 'await' expression"
}
```

## Verification

Check upstream status:
```bash
python3 scripts/check-upstream-services.py
```

Test tool execution:
```bash
python3 scripts/test-tool-execution.py
```

## Next Steps

1. **For Production**: Deploy AWS Labs MCP servers (Option 1)
2. **For Development**: Implement mock mode (Option 2)
3. **For Testing**: Current setup works (Option 3)

## Configuration Files

Upstream configurations are defined in:
- `src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/server.py` (line 60)
- `src/virons-security-mcp-server/virons/security_mcp_server/server.py` (line 45)
- `src/virons-operations-mcp-server/virons/operations_mcp_server/server.py`
- `src/virons-monitoring-mcp-server/virons/monitoring_mcp_server/server.py`

To modify upstream endpoints, update the `UPSTREAM_CONFIG` or `UPSTREAM` dictionaries in these files.
