# MCP Integration Plan - Virons AI MVP
**Date**: 2026-03-08
**Status**: DRAFT
**Architecture**: LangGraph Orchestrator + MCP Capability Islands + AWS EKS

## Executive Summary

Deploy 9 core MCP servers (capability islands) orchestrated by a LangGraph control-plane, delivering 70+ tools for Challenge Mode (≤90s), Retrospective Validator, and Grandmaster workflows with full compliance gates (BaFin, GDPR, DORA).

**Key Decisions**:
- **Orchestrator**: LangGraph (Python) + FastAPI wrapper
- **Compute**: AWS EKS (eu-central-1) with namespace isolation
- **Models**: Bedrock Nova Micro (batch NLP) + Nova Pro (Grandmaster)
- **Data**: RDS Postgres (audit/calc), ElastiCache Redis (cache), OpenSearch (artifacts), Neo4j Aura (graph)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│         LangGraph Orchestrator Gateway (OG) [:9000]              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Planner      │ │ Executor     │ │ Compliance   │            │
│  │ Agent        │ │ Agent        │ │ Gatekeeper   │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│  ┌──────────────────────────────────────────────────┐           │
│  │ Audit & Provenance Agent (correlationId)         │           │
│  └──────────────────────────────────────────────────┘           │
└────────────┬────────────────────────────────────────────────────┘
             │ mTLS + RBAC + NetworkPolicy
    ┌────────┼────────┬────────┬────────┬────────┬────────┬────────┐
    │        │        │        │        │        │        │        │
    ▼        ▼        ▼        ▼        ▼        ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Ingest  │ │Forensic│ │ML      │ │Block   │ │Prompts │ │Comp    │ │Sec     │ │Infra   │
│:9100   │ │:9300   │ │:9420   │ │:9430   │ │:9550   │ │:9560   │ │:9570   │ │:9500   │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
     │          │          │          │          │          │          │          │
     └──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
            ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
            │ RDS Postgres │  │ ElastiCache  │  │ OpenSearch   │
            │ (audit/calc) │  │ Redis (cache)│  │ (artifacts)  │
            └──────────────┘  └──────────────┘  └──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │ Neo4j Aura   │
            │ (graph)      │
            └──────────────┘
```

## Phase 1: Foundation (Week 1-2)

### 1.1 Orchestrator Gateway (OG) - LangGraph
**Location**: `src/orchestrator-gateway/`
**Stack**: Python 3.13 + LangGraph + FastAPI + Pydantic

**Components**:
```python
# src/orchestrator-gateway/agents/
planner.py          # DAG planning, pattern selection
executor.py         # Workflow execution, retries
compliance.py       # Policy enforcement, veto authority
audit.py            # Immutable audit log, correlationId

# src/orchestrator-gateway/workflows/
challenge_mode.py   # ≤90s workflow
retrospective.py    # Reproducibility workflow
grandmaster.py      # High-cost gated workflow

# src/orchestrator-gateway/api/
server.py           # FastAPI wrapper
schemas.py          # Pydantic models
```

**Acceptance Criteria**:
- [ ] All workflows emit correlationId
- [ ] Compliance agent can veto + create GitHub issue
- [ ] Audit events written to RDS with SHA-256 hashes
- [ ] Health check endpoint operational

### 1.2 Core Infrastructure (AWS EKS)
**Region**: eu-central-1 (Frankfurt)
**Namespace Strategy**: One namespace per MCP server

```hcl
# infra/terraform/modules/eks/
- VPC (public + private subnets)
- EKS cluster (1.28+)
- Node groups (t3.medium, autoscaling)
- NetworkPolicies (egress control)
- ALB Ingress Controller
- Cert-Manager (mTLS)
```

**Namespaces**:
- `orchestrator` - OG + control plane
- `mcp-ingestion` - Ingestion server (egress allowed)
- `mcp-forensic` - Forensic server (no egress)
- `mcp-ml` - ML server (Bedrock only)
- `mcp-blockchain` - Blockchain server
- `mcp-prompts` - Prompts server
- `mcp-compliance` - Compliance server (veto authority)
- `mcp-security` - Security server
- `mcp-infra` - Infrastructure server

### 1.3 Data Layer
```hcl
# infra/terraform/modules/data/
- RDS Aurora Postgres (Multi-AZ, eu-central-1)
  - Schema: audit_events, calculation_audit, evidence_chain
  - Extensions: pgcrypto (SHA-256)
- ElastiCache Redis (cluster mode)
  - Use: cache, idempotency, rate-limits
- OpenSearch (3 nodes)
  - Use: artifact search, audit search
- Neo4j Aura (free tier → paid)
  - Use: person-network graph
```

## Phase 2: MCP Servers (Week 3-4)

### 2.1 Priority 1: Critical Path (Challenge Mode)

#### Ingestion MCP (:9100)
**Tools**: `fetch`, `brave_search`, `apify_scrape`, `store_artifact`, `emit_event`
**Boundaries**:
- Egress allowlist (public corporate sources only)
- EU residency enforcement (S3 eu-central-1)
- Idempotency (SHA-256 in Redis)
**Audit**: `artifact_hash`, `source_url`, `s3_uri`, `index_id`, `event_id`

#### Forensic MCP (:9300)
**Tools**: `run_deterministic_rules`, `calculation_audit`, `neo4j_query`, `extract_evidence`
**Boundaries**:
- No egress (reads from artifact store only)
- Schema validation (Pydantic)
**Audit**: `rule_id`, `inputs_hash`, `calc_hash`, `evidence_refs[]`

#### ML MCP (:9420)
**Tools**: `phase_classify`, `anomaly_detect`, `grandmaster_invoke`, `eval_model`
**Boundaries**:
- Cost gate (Nova Pro only if Phase-3 confidence > threshold)
- High-risk gating (human approval)
**Audit**: `model_id`, `model_card_ref`, `prompt_hash`, `output_hash`, `eval_run_id`
**Models**:
- Nova Micro: `amazon.nova-micro-v1:0` (batch NLP, $0.035/1M tokens)
- Nova Pro: `amazon.nova-pro-v1:0` (Grandmaster, $0.80/1M tokens)

### 2.2 Priority 2: Compliance & Security

#### Compliance MCP (:9560)
**Tools**: `check_gdpr`, `check_dora`, `check_bafin`, `policy_enforce`, `create_issue`
**Boundaries**:
- Veto authority (can block workflows)
- Auto-creates GitHub issues
**Audit**: `policy_id`, `violation`, `remediation_ticket`

#### Security MCP (:9570)
**Tools**: `assess_posture`, `list_findings`, `iam_check`, `incident_ops`
**Boundaries**:
- Can suspend workflows
- No auto-remediation (pre-approved runbooks only)
**Audit**: `incident_id`, `severity`, `containment_action`

### 2.3 Priority 3: Supporting Services

#### Blockchain MCP (:9430)
**Tools**: `seal_evidence`, `verify_seal`, `get_merkle_proof`
**Boundaries**: Async-only, replayable
**Audit**: `ledger_entry_id`, `merkle_root`, `timestamp_proof`

#### Prompts MCP (:9550)
**Tools**: `search_prompts`, `get_prompt`, `chain_prompts`, `version_prompt`
**Boundaries**: Read-only in prod, GitHub promotion workflow
**Audit**: `prompt_version`, `ab_bucket`, `scorecard_metrics`

#### Infrastructure MCP (:9500)
**Tools**: `list_accounts`, `list_ec2`, `get_costs`, `deploy_stack`, `eks_ops`
**Boundaries**: Production actions require approval
**Audit**: `deploy_id`, `terraform_plan_hash`, `approval_ref`

## Phase 3: Workflows (Week 5)

### 3.1 Challenge Mode (≤90s)
```python
# src/orchestrator-gateway/workflows/challenge_mode.py
async def challenge_mode_workflow(company: str, correlation_id: str):
    # 1. Resolve entity (parallel: LEI, OpenCorporates, Wikipedia)
    entity = await planner.resolve_entity(company)

    # 2. Ingest snapshot (parallel: filings, news, social)
    artifacts = await executor.parallel([
        ingestion.fetch_filings(entity),
        ingestion.brave_search(entity),
        ingestion.apify_scrape(entity)
    ])

    # 3. Deterministic forensics (parallel: all rules)
    forensics = await executor.parallel([
        forensic.run_rules(artifacts),
        forensic.calculation_audit(artifacts)
    ])

    # 4. Phase classify (ML gate)
    phase = await ml.phase_classify(forensics)

    # 5. Risk fuse (compliance gate)
    await compliance.check_gates(phase, forensics)

    # 6. Seal evidence (async)
    executor.background(blockchain.seal_evidence(forensics))

    # 7. Generate dossier
    dossier = await generate_dossier(entity, forensics, phase)

    # 8. Audit checkpoint
    await audit.write_event(correlation_id, dossier)

    return dossier
```

**Gates**:
- Cost gate: Nova Pro only if `phase.confidence > 0.7` or `staleness > 7d`
- Compliance gate: GDPR/DORA/BaFin checks before narrative
- Audit gate: 100% captured before response

### 3.2 Retrospective Validator
```python
# src/orchestrator-gateway/workflows/retrospective.py
async def retrospective_workflow(case_id: str, correlation_id: str):
    # 1. Load frozen case
    frozen = await load_frozen_case(case_id)

    # 2. Re-run all rules
    results = await forensic.run_rules(frozen.artifacts)

    # 3. Compute lead time
    lead_time = await compute_lead_time(frozen, results)

    # 4. Reproducibility gate
    assert results.hashes == frozen.hashes, "Non-deterministic"

    # 5. Generate report
    report = await generate_report(frozen, results, lead_time)

    # 6. Seal
    await blockchain.seal_evidence(report)

    return report
```

**Gates**:
- Reproducibility: Same inputs → same outputs
- CalculationAudit BEFORE forensic flags

### 3.3 Grandmaster Run (Expensive)
```python
# src/orchestrator-gateway/workflows/grandmaster.py
async def grandmaster_workflow(entity: str, correlation_id: str):
    # 1. Preflight (cost/risk gate)
    cost_estimate = await ml.estimate_cost(entity)
    if cost_estimate > THRESHOLD:
        await compliance.request_approval(cost_estimate)

    # 2. Fetch KB analogues
    analogues = await prompts.search_prompts(entity)

    # 3. Run structured output model (Nova Pro)
    scenarios = await ml.grandmaster_invoke(entity, analogues)

    # 4. Validate structured output
    await compliance.validate_output(scenarios)

    # 5. Store scenarios
    await store_scenarios(scenarios)

    # 6. Set watches
    await set_watches(entity, scenarios)

    return scenarios
```

**Gates**:
- Cost ceiling: `$X per run`
- Human approval: `risk > threshold`
- Structured output validation

## Phase 4: Compliance & Security (Week 6)

### 4.1 RBAC (3 Layers)
```yaml
# OG Policy Engine
orchestrator:
  - role: planner
    permissions: [read_workflows, write_plans]
  - role: executor
    permissions: [call_mcp_tools, write_audit]
  - role: compliance
    permissions: [veto_workflows, create_issues]

# MCP Server Policy
mcp_servers:
  ingestion:
    - role: fetcher
      permissions: [egress_allowlist, write_s3]
  forensic:
    - role: analyzer
      permissions: [read_artifacts, write_findings]

# Service-Level Policy
services:
  challenge_mode:
    - role: user
      permissions: [invoke_workflow, read_dossier]
```

### 4.2 Audit Event Schema
```json
{
  "correlationId": "chal_20260308_abc123",
  "taskId": "ingest_filing_with_validation",
  "actor": {
    "type": "agent",
    "name": "orchestrator-gateway"
  },
  "tool": {
    "mcpServer": "ingestion:9100",
    "toolName": "fetch"
  },
  "inputsHash": "sha256:...",
  "outputsHash": "sha256:...",
  "artifacts": [
    {
      "hash": "sha256:...",
      "s3Uri": "s3://virons-artifacts-eu-central-1/..."
    }
  ],
  "policy": {
    "decision": "allow",
    "rules": ["EU_RESIDENCY_OK", "PUBLIC_DATA_OK"]
  },
  "timestamps": {
    "startedAt": "2026-03-08T10:00:00Z",
    "endedAt": "2026-03-08T10:00:05Z"
  }
}
```

### 4.3 Compliance Controls
- **RBAC**: Short-lived scoped credentials per MCP server
- **Audit Log**: Append-only, 7-year retention, RDS Postgres
- **Egress Control**: Ingestion only, allowlisted proxy
- **Human Approval**: Risk threshold triggers pause + approval log

## Deployment Strategy

### Build Order
1. **Week 1**: OG skeleton + EKS cluster + RDS/Redis
2. **Week 2**: Ingestion + Forensic + ML MCP servers
3. **Week 3**: Compliance + Security MCP servers
4. **Week 4**: Blockchain + Prompts + Infra MCP servers
5. **Week 5**: Challenge Mode + Retrospective workflows
6. **Week 6**: Grandmaster workflow + compliance gates

### Acceptance Criteria (MVP)
- [ ] 9/9 MCP servers healthy
- [ ] Challenge Mode completes in ≤90s
- [ ] Every workflow replayable (frozen artifacts → same hashes)
- [ ] 100% correlation coverage (every log line has correlationId)
- [ ] Compliance veto works (blocks workflow + creates GitHub issue)
- [ ] Failure is graceful (degrades to cache + flags staleness)
- [ ] 70+ tools operational
- [ ] Gateway aggregates all tools
- [ ] Health checks passing
- [ ] Audit log complete

### Success Metrics
- **Latency**: P99 < 200ms per tool call
- **Availability**: 99.95% uptime
- **Cost**: Nova Micro for 80% of calls, Nova Pro for 20%
- **Compliance**: 100% audit coverage, 0 veto failures
- **Reproducibility**: 100% hash match on retrospective runs

## Repository Structure

```
platform-mcp/
├── src/
│   ├── orchestrator-gateway/       # LangGraph OG
│   │   ├── agents/                 # Planner, Executor, Compliance, Audit
│   │   ├── workflows/              # Challenge, Retrospective, Grandmaster
│   │   ├── api/                    # FastAPI wrapper
│   │   └── Dockerfile
│   ├── mcp-servers/
│   │   ├── ingestion/              # :9100
│   │   ├── forensic/               # :9300
│   │   ├── ml/                     # :9420
│   │   ├── blockchain/             # :9430
│   │   ├── prompts/                # :9550
│   │   ├── compliance/             # :9560
│   │   ├── security/               # :9570
│   │   └── infrastructure/         # :9500
├── infra/
│   ├── terraform/
│   │   ├── modules/
│   │   │   ├── eks/
│   │   │   ├── data/
│   │   │   └── networking/
│   │   └── environments/
│   │       ├── dev/
│   │       └── prod/
│   └── helm/
│       ├── orchestrator-gateway/
│       └── mcp-servers/
├── docs/
│   ├── architecture/
│   │   ├── MCP-INTEGRATION-PLAN.md (this file)
│   │   ├── mcp-servers-overview.md
│   │   └── agentic-ai-plan.md
│   └── operations/
│       ├── DEPLOYMENT-GUIDE.md
│       └── RUNBOOK.md
└── scripts/
    ├── deploy-orchestrator.sh
    ├── deploy-mcp-servers.sh
    └── verify-integration.sh
```

## Implementation Status

### ✅ Complete
- **Orchestrator Gateway**: Exists in `platform-orchestrator-gateway` repo (148 tests passing)
- **MCP Gateway**: Operational at :9000 in `platform-mcp`
- **LangGraph Workflows**: 4 workflows implemented (Challenge Mode, Investigation, Retrospective, DevOps)
- **Compliance Gates**: All EU AI Act, GDPR, BaFin, DORA controls implemented
- **Audit Trail**: Immutable Postgres-backed audit log operational

### 🚧 In Progress
- **MCP Servers**: 0/9 deployed (see MCP-DEPLOYMENT-PLAN.md)
- **Gateway Configuration**: Needs update to point orchestrator → gateway

### 📋 Next Steps

1. **Week 1**: Build Infrastructure + Forensic + ML MCP servers (Challenge Mode critical path)
2. **Week 2**: Build Compliance + Security MCP servers
3. **Week 3**: Build Blockchain + Prompts + Dev + API MCP servers
4. **Week 4**: Integration testing + E2E validation

**See**: `docs/architecture/MCP-DEPLOYMENT-PLAN.md` for detailed implementation plan.

## Configuration Updates Required

### Orchestrator Gateway
```json
// platform-orchestrator-gateway/config/gateway.json
{
  "gateway_url": "http://virons-mcp-gateway.virons-mcp.svc.cluster.local:9000"
}
```

### MCP Gateway
```yaml
# platform-mcp/config/servers.yaml
servers:
  - name: infrastructure
    url: http://virons-infrastructure-mcp:9100
  - name: forensic
    url: http://virons-forensic-mcp:9300
  # ... (7 more servers)
```

## Open Questions

1. **Neo4j**: Self-hosted in VPC or Neo4j Aura for MVP? → **Aura free tier for MVP**
2. **Cost Threshold**: What's the $ ceiling for Grandmaster runs requiring approval? → **$10 per run**
3. **Risk Threshold**: What confidence score triggers human approval? → **>0.7 confidence**

## References

- `docs/architecture/mcp-servers-overview.md` - Tool catalog
- `docs/architecture/agentic-ai-plan.md` - Orchestration patterns
- `docs/operations/MCP-STATUS-REPORT.md` - Current deployment status
- AWS Bedrock Nova models: https://aws.amazon.com/bedrock/nova/
- LangGraph: https://langchain-ai.github.io/langgraph/
