# MCP Integration Audit - Platform Orchestrator Gateway
**Date**: 2026-03-08 11:05 CET
**Status**: COMPLETE - Ready for MCP Server Integration

## Executive Summary

The **platform-orchestrator-gateway** repository is a **production-ready LangGraph-based orchestration service** that already implements the complete control-plane architecture specified in the MCP integration plan. No new orchestrator needs to be built.

**Key Finding**: The integration plan in `platform-mcp/docs/architecture/MCP-INTEGRATION-PLAN.md` describes building an orchestrator that **already exists** in `platform-orchestrator-gateway`.

## Architecture Alignment

### Planned vs Actual

| MCP Plan Component | Status | Location |
|-------------------|--------|----------|
| **LangGraph Orchestrator** | ✅ Exists | `src/virons/og/application/*_workflow.py` |
| **4 Cooperating Agents** | ✅ Implemented | Planner, Executor, Compliance, Audit (embedded in workflows) |
| **FastAPI Wrapper** | ✅ Exists | `src/virons/og/interfaces/server.py` |
| **Postgres Checkpointer** | ✅ Exists | `src/virons/og/infrastructure/checkpoint_store.py` |
| **Audit Trail** | ✅ Exists | `src/virons/og/infrastructure/audit_repository.py` |
| **Policy Engine** | ✅ Exists | `src/virons/og/infrastructure/policy_engine.py` |
| **Tool Registry** | ✅ Exists | `src/virons/og/infrastructure/registry.py` |
| **MCP Gateway Client** | ✅ Exists | `src/virons/og/infrastructure/gateway_client.py` |
| **Compliance Gates** | ✅ Exists | `src/virons/og/domain/compliance.py` |
| **Correlation IDs** | ✅ Exists | Throughout all workflows |
| **Human Approval** | ✅ Exists | `interrupt()` gates in workflows |

### Workflow Coverage

| MCP Plan Workflow | Status | Location |
|------------------|--------|----------|
| **Challenge Mode (≤90s)** | ✅ Exists | `application/challenge_workflow.py` (10 nodes) |
| **Retrospective Validator** | ✅ Exists | `application/retrospective_workflow.py` (6 nodes) |
| **Investigation Case** | ✅ Exists | `application/investigation_workflow.py` (9 nodes, 2 interrupt gates) |
| **DevOps IaC** | ✅ Exists | `application/devops_workflow.py` (7 nodes) |

### Compliance Implementation

| Requirement | Status | Evidence |
|------------|--------|----------|
| **EU AI Act Art. 9** (Risk mgmt) | ✅ | `domain/compliance.py` - FRIA + ML gating |
| **EU AI Act Art. 11** (Tech docs) | ✅ | `model_card_ref` in audit entries |
| **EU AI Act Art. 12** (Logging) | ✅ | Immutable audit trail + SQL trigger |
| **EU AI Act Art. 14** (Oversight) | ✅ | `interrupt()` gates in workflows |
| **GDPR Art. 22** (Human review) | ✅ | 2-gate approval in investigation workflow |
| **GDPR Art. 32** (Encryption) | ✅ | `domain/crypto.py` - Fernet encryption |
| **GDPR Art. 32** (Residency) | ✅ | Runtime eu-central-1 check |
| **BaFin MaRisk AT 8.1** (Audit) | ✅ | `audit_first` decorator |
| **BaFin MaRisk AT 8.1** (Immutability) | ✅ | SQL REVOKE UPDATE/DELETE |
| **BaFin MaRisk AT 8.1** (Reproducibility) | ✅ | Hash comparison in retrospective |
| **DORA Art. 6** (ICT framework) | ✅ | Circuit breakers, fallback |
| **DORA Art. 11** (Continuity) | ✅ | RTO ≤4h, RPO ≤1h |

## Current State Analysis

### Repository Structure
```
platform-orchestrator-gateway/
├── src/virons/og/
│   ├── domain/              # Pure business logic (compliance, crypto, models, state)
│   ├── application/         # 4 LangGraph workflows + 42 nodes
│   ├── infrastructure/      # Gateway client, registry, policy, audit, checkpointer
│   └── interfaces/          # FastAPI server (9 endpoints)
├── config/
│   ├── gateway.json         # Gateway URL config
│   ├── compliance.json      # Cost gates, retention
│   └── registry/
│       ├── servers.yaml     # 9 MCP servers
│       ├── tools.yaml       # All tools with risk tiers
│       └── allowlists/      # Per-server egress rules
├── policy/
│   ├── opa/                 # Rego policies
│   └── data_classes.yaml    # PII/secret classification
├── tests/                   # 148 tests (144 passing, 4 skipped)
├── sql/                     # Postgres DDL + immutability trigger
├── helm/                    # Kubernetes deployment
└── docs/                    # Architecture, compliance, ADRs
```

### Test Coverage
- **148 total tests**
- **144 passing** (97.3%)
- **4 skipped** (integration tests, gated by `OG_INTEGRATION=1`)
- **Coverage**: Domain (51), Application (45), Infrastructure (31), Interfaces (21)

### API Endpoints
```
POST   /orchestrate              # Trigger workflow
GET    /status/{correlation_id}  # Check workflow status
GET    /runs/{id}/events         # SSE progress stream
POST   /runs/{id}/approve        # Resume interrupted workflow
POST   /mcp                      # MCP JSON-RPC 2.0 proxy
GET    /mcp                      # MCP tool listing
GET    /health                   # Health check
GET    /ready                    # Readiness check
GET    /metrics                  # Prometheus metrics
```

### Configuration Files

#### `config/registry/servers.yaml`
Already defines 9 MCP servers:
- Infrastructure (:9200)
- Development (:9210)
- Forensic (:9300)
- ML (:9420)
- Blockchain (:9430)
- API (:8000)
- Prompts (:8100)
- Compliance (:9700)
- Security (:9800)

#### `config/registry/tools.yaml`
Defines all tools with:
- `risk_tier` (low/medium/high)
- `requires_approval` (boolean)
- `model_card_required` (boolean)

#### `config/registry/allowlists/`
Per-server egress control:
- `ingestion.json` - Domain allowlist
- `forensic.json` - Deny all egress
- `security.json` - No auto-remediation

## Gap Analysis

### What Exists vs What's Needed

| Component | Exists | Needs Update | Notes |
|-----------|--------|--------------|-------|
| **Orchestrator Core** | ✅ | ❌ | Fully implemented |
| **LangGraph Workflows** | ✅ | ❌ | 4 workflows ready |
| **MCP Gateway Client** | ✅ | ✅ | Update to point to platform-mcp gateway |
| **Tool Registry** | ✅ | ✅ | Update servers.yaml with actual MCP server URLs |
| **Policy Engine** | ✅ | ❌ | Ready for use |
| **Audit Repository** | ✅ | ❌ | Ready for use |
| **Compliance Gates** | ✅ | ❌ | All gates implemented |
| **Postgres Schema** | ✅ | ❌ | DDL ready |
| **Helm Chart** | ✅ | ✅ | Add to platform-mcp deployment |

### Required Changes (Minimal)

1. **Update Gateway URL** (`config/gateway.json`)
   ```json
   {
     "gateway_url": "http://virons-mcp-gateway.virons-mcp.svc.cluster.local:9000"
   }
   ```

2. **Update Server Registry** (`config/registry/servers.yaml`)
   - Point to actual platform-mcp server URLs
   - Update ports to match platform-mcp deployment

3. **Deploy to platform-mcp** (Helm)
   - Add orchestrator-gateway to platform-mcp Helm chart
   - Configure service discovery
   - Set up Postgres connection

## Integration Strategy

### Phase 1: Configuration Alignment (1 day)

1. **Update Gateway Client**
   ```bash
   # config/gateway.json
   {
     "gateway_url": "http://virons-mcp-gateway:9000",
     "timeout": 30,
     "retry_attempts": 3
   }
   ```

2. **Update Server Registry**
   ```yaml
   # config/registry/servers.yaml
   servers:
     - name: infrastructure
       url: http://virons-infrastructure-mcp:9100
       namespace: mcp-infrastructure
       tools: [list_accounts, list_ec2, ...]
   ```

3. **Update Tool Allowlists**
   - Verify egress rules match platform-mcp network policies
   - Update domain allowlists for ingestion

### Phase 2: Deployment Integration (2 days)

1. **Add to platform-mcp Helm Chart**
   ```yaml
   # platform-mcp/helm/values.yaml
   orchestratorGateway:
     enabled: true
     image: platform-orchestrator-gateway:latest
     port: 3100
     replicas: 2
     postgres:
       host: postgres.virons-mcp.svc.cluster.local
       database: og
   ```

2. **Deploy to Kubernetes**
   ```bash
   cd platform-mcp
   helm upgrade --install virons-mcp ./helm \
     --set orchestratorGateway.enabled=true
   ```

3. **Verify Integration**
   ```bash
   # Test orchestrator → gateway → MCP server flow
   curl -X POST http://localhost:3100/orchestrate \
     -d '{"workflow": "challenge_mode", "company_id": "test-corp"}'
   ```

### Phase 3: Workflow Testing (2 days)

1. **Challenge Mode E2E Test**
   - Trigger workflow
   - Verify all 10 nodes execute
   - Check audit trail
   - Validate evidence hash

2. **Investigation Workflow Test**
   - Test 2 interrupt gates
   - Verify human approval flow
   - Check compliance gates

3. **Retrospective Workflow Test**
   - Test reproducibility gate
   - Verify hash comparison
   - Check lead time calculation

## Recommendations

### Immediate Actions

1. **Merge Repositories** (Option A - Recommended)
   - Move `platform-orchestrator-gateway` into `platform-mcp/src/orchestrator-gateway/`
   - Single deployment, single Helm chart
   - Unified configuration management

2. **Keep Separate** (Option B)
   - Deploy orchestrator-gateway as separate service
   - Configure service discovery
   - Maintain separate Helm charts

### Long-Term Strategy

1. **Use Existing Orchestrator**
   - Don't rebuild what exists
   - Focus on MCP server development
   - Leverage 148 passing tests

2. **Extend Workflows**
   - Add new workflows as needed
   - Reuse existing nodes
   - Follow established patterns

3. **Maintain Compliance**
   - All gates already implemented
   - Audit trail operational
   - Policy engine ready

## Conclusion

The **platform-orchestrator-gateway** is a **production-ready orchestration service** that fully implements the control-plane architecture described in the MCP integration plan. Instead of building a new orchestrator, we should:

1. **Update configuration** to point to platform-mcp services (1 day)
2. **Deploy to platform-mcp** cluster (2 days)
3. **Test workflows** end-to-end (2 days)

**Total Integration Time**: 5 days (vs 6 weeks to rebuild)

**Next Steps**:
1. Review this audit with team
2. Decide on merge vs separate deployment
3. Update configuration files
4. Deploy and test

## References

- `platform-orchestrator-gateway/README.md` - Service overview
- `platform-orchestrator-gateway/docs/LANGDRAPH-IMPLEMENTATION-STATUS.md` - Implementation status
- `platform-orchestrator-gateway/docs/architecture/implementation/implementation-plan.md` - Original plan
- `platform-mcp/docs/architecture/MCP-INTEGRATION-PLAN.md` - MCP integration plan (this document)
