# MCP Server Deployment Plan
**Date**: 2026-03-08
**Status**: ACTIVE
**Goal**: Deploy 9 MCP servers in platform-mcp, connect to existing orchestrator-gateway

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  platform-orchestrator-gateway (EXISTING - NO CHANGES)      │
│  - LangGraph workflows                                       │
│  - FastAPI server :3100                                      │
│  - Postgres checkpointer                                     │
└────────────┬────────────────────────────────────────────────┘
             │ HTTP
             ▼
┌─────────────────────────────────────────────────────────────┐
│  virons-mcp-gateway :9000 (EXISTING - OPERATIONAL)          │
│  - Tool routing                                              │
│  - Circuit breakers                                          │
│  - Metrics                                                   │
└────────────┬────────────────────────────────────────────────┘
             │ HTTP
    ┌────────┼────────┬────────┬────────┬────────┬────────┐
    ▼        ▼        ▼        ▼        ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Infra   │ │Forensic│ │ML      │ │Block   │ │Prompts │ │Comp    │
│:9100   │ │:9300   │ │:9420   │ │:9430   │ │:9550   │ │:9560   │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
┌────────┐ ┌────────┐ ┌────────┐
│Sec     │ │Dev     │ │API     │
│:9570   │ │:9500   │ │:9540   │
└────────┘ └────────┘ └────────┘
```

## Current Status

### ✅ Operational (2 components)
- **orchestrator-gateway** - Separate repo, needs config update only
- **virons-mcp-gateway** - Running at :9000, healthy

### ❌ Missing (9 MCP servers)
All need to be built in `platform-mcp/src/`:

1. **virons-infrastructure-mcp** (:9100) - AWS/EKS operations
2. **virons-forensic-mcp** (:9300) - Deterministic rules + calculation audit
3. **virons-ml-mcp** (:9420) - Bedrock Nova models
4. **virons-blockchain-mcp** (:9430) - Evidence ledger
5. **virons-prompts-mcp** (:9550) - Template library
6. **virons-compliance-mcp** (:9560) - Policy enforcement
7. **virons-security-mcp** (:9570) - Posture assessment
8. **virons-dev-mcp** (:9500) - Git/DevOps
9. **virons-api-mcp** (:9540) - REST/GraphQL proxy

## Deployment Strategy

### Phase 1: Core Servers (Week 1)
**Priority**: Challenge Mode critical path

#### 1. Infrastructure MCP (:9100)
```python
# src/virons-infrastructure-mcp/server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("virons-infrastructure-mcp")

@server.list_tools()
async def list_tools():
    return [
        {"name": "list_accounts", "description": "List AWS accounts"},
        {"name": "list_ec2", "description": "List EC2 instances"},
        {"name": "get_costs", "description": "Get cost analysis"}
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "list_accounts":
        # AWS Organizations API
        return {"accounts": [...]}
```

**Tools**: `list_accounts`, `list_ec2`, `get_costs`, `validate_cloudformation`, `deploy_stack`, `eks_ops`

#### 2. Forensic MCP (:9300)
```python
# src/virons-forensic-mcp/server.py
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "run_deterministic_rules":
        # Beneish M-Score, Altman Z-Score
        return {"flags": [...], "scores": {...}}
    elif name == "calculation_audit":
        # SHA-256 hash of inputs + outputs
        return {"audit_hash": "...", "inputs_hash": "..."}
```

**Tools**: `run_deterministic_rules`, `calculation_audit`, `neo4j_query`, `extract_evidence`

#### 3. ML MCP (:9420)
```python
# src/virons-ml-mcp/server.py
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='eu-central-1')

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "phase_classify":
        # Nova Micro for batch NLP
        response = bedrock.invoke_model(
            modelId='amazon.nova-micro-v1:0',
            body=json.dumps({"prompt": arguments["text"]})
        )
        return {"phase": "...", "confidence": 0.85}
    elif name == "grandmaster_invoke":
        # Nova Pro for structured output (cost-gated)
        response = bedrock.invoke_model(
            modelId='amazon.nova-pro-v1:0',
            body=json.dumps({"prompt": arguments["prompt"]})
        )
        return {"scenarios": [...]}
```

**Tools**: `phase_classify`, `anomaly_detect`, `grandmaster_invoke`, `eval_model`

### Phase 2: Compliance & Security (Week 2)

#### 4. Compliance MCP (:9560)
```python
# src/virons-compliance-mcp/server.py
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "check_gdpr":
        # GDPR Art 32 residency check
        return {"compliant": True, "region": "eu-central-1"}
    elif name == "check_bafin":
        # BaFin MaRisk AT 8.1 audit trail
        return {"compliant": True, "gaps": []}
```

**Tools**: `check_gdpr`, `check_dora`, `check_bafin`, `policy_enforce`, `create_issue`

#### 5. Security MCP (:9570)
```python
# src/virons-security-mcp/server.py
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "assess_posture":
        # AWS Config + SecurityHub
        return {"score": 85, "findings": [...]}
```

**Tools**: `assess_posture`, `list_findings`, `iam_check`, `incident_ops`

### Phase 3: Supporting Services (Week 3)

#### 6. Blockchain MCP (:9430)
```python
# src/virons-blockchain-mcp/server.py
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "seal_evidence":
        # Merkle tree in Postgres
        return {"ledger_entry_id": "...", "merkle_root": "..."}
```

**Tools**: `seal_evidence`, `verify_seal`, `get_merkle_proof`

#### 7. Prompts MCP (:9550)
**Tools**: `search_prompts`, `get_prompt`, `chain_prompts`, `version_prompt`

#### 8. Dev MCP (:9500)
**Tools**: `list_repos`, `get_pr_diff`, `create_pr`, `run_code_analysis`, `trigger_build`

#### 9. API MCP (:9540)
**Tools**: `call_rest_api`, `graphql_query`, `soap_call`, `oauth_token`, `cache_get_set`

## MCP Server Template

```
src/virons-{name}-mcp/
├── server.py              # MCP server implementation
├── tools/                 # Tool implementations
│   ├── __init__.py
│   └── {tool_name}.py
├── Dockerfile             # Enterprise-grade build
├── pyproject.toml         # Dependencies
└── README.md
```

### Dockerfile Template
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install -e .
COPY . .
USER 10001
HEALTHCHECK CMD python -c "import httpx; httpx.get('http://localhost:${PORT}/health')"
CMD ["python", "-m", "mcp", "run", "server.py"]
```

### pyproject.toml Template
```toml
[project]
name = "virons-{name}-mcp"
version = "0.1.0"
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0"
]
```

## Gateway Registration

### Update gateway config
```yaml
# platform-mcp/config/servers.yaml
servers:
  - name: infrastructure
    url: http://virons-infrastructure-mcp:9100
    tools: [list_accounts, list_ec2, get_costs, ...]
  - name: forensic
    url: http://virons-forensic-mcp:9300
    tools: [run_deterministic_rules, calculation_audit, ...]
  - name: ml
    url: http://virons-ml-mcp:9420
    tools: [phase_classify, anomaly_detect, grandmaster_invoke, ...]
```

### Gateway auto-discovery
Gateway already implements tool routing - just add servers to config.

## Orchestrator Configuration

### Update orchestrator-gateway config
```json
// platform-orchestrator-gateway/config/gateway.json
{
  "gateway_url": "http://virons-mcp-gateway.virons-mcp.svc.cluster.local:9000",
  "timeout": 30,
  "retry_attempts": 3
}
```

### Update server registry
```yaml
# platform-orchestrator-gateway/config/registry/servers.yaml
servers:
  - name: infrastructure
    url: http://virons-mcp-gateway:9000
    namespace: mcp-infrastructure
    tools: [list_accounts, list_ec2, ...]
```

**Note**: Orchestrator calls gateway, gateway routes to servers. No direct orchestrator→server calls.

## Deployment Commands

```bash
# Build all MCP servers
cd platform-mcp
docker-compose -f docker-compose.core.yml build

# Deploy to Kubernetes
helm upgrade --install virons-mcp ./helm

# Verify all servers healthy
kubectl get pods -n virons-mcp
kubectl logs -n virons-mcp virons-infrastructure-mcp

# Test gateway routing
curl http://localhost:9000/tools

# Update orchestrator config
cd ../platform-orchestrator-gateway
# Edit config/gateway.json
# Edit config/registry/servers.yaml

# Test end-to-end
curl -X POST http://localhost:3100/orchestrate \
  -d '{"workflow": "challenge_mode", "company_id": "test-corp"}'
```

## Testing Strategy

### Unit Tests (per server)
```python
# tests/test_infrastructure_mcp.py
async def test_list_accounts():
    result = await call_tool("list_accounts", {})
    assert "accounts" in result
```

### Integration Tests (gateway)
```python
# tests/test_gateway_routing.py
async def test_routes_to_infrastructure():
    response = await gateway.call_tool("list_accounts", {})
    assert response.status_code == 200
```

### E2E Tests (orchestrator)
```python
# tests/test_challenge_mode_e2e.py
async def test_challenge_mode_workflow():
    result = await orchestrator.run_workflow("challenge_mode", {"company_id": "test"})
    assert result["status"] == "completed"
    assert "dossier" in result
```

## Success Criteria

- [ ] 9/9 MCP servers deployed and healthy
- [ ] Gateway routes to all servers
- [ ] Orchestrator connects to gateway
- [ ] Challenge Mode workflow completes end-to-end
- [ ] All tools accessible via gateway
- [ ] Audit trail complete
- [ ] Compliance gates operational

## Timeline

- **Week 1**: Infrastructure, Forensic, ML servers (Challenge Mode critical path)
- **Week 2**: Compliance, Security servers
- **Week 3**: Blockchain, Prompts, Dev, API servers
- **Week 4**: Integration testing + documentation

**Total**: 4 weeks to full deployment

## Next Steps

1. Create MCP server template/generator script
2. Build Infrastructure MCP (highest priority)
3. Build Forensic MCP
4. Build ML MCP
5. Test Challenge Mode workflow
6. Continue with remaining servers
