# Agent Guardrails System

**Purpose**: Safety controls for AI agents working with virons-services
**Compliance**: BaFin MaRisk AT 8.1, GDPR Art 32, DORA Art 11, EU AI Act

## Core Files

| File | Purpose |
|---|---|
| `agent-restrictions.md` | What agents can/cannot do |
| `cost-guards.md` | Budget limits and cost controls |
| `orchestration/safety-protocol.md` | Risk assessment + approval workflow |
| `orchestration/agent-coordinator.md` | Agent routing and orchestration |
| `orchestration/service-agent-matrix.md` | 42-service → agent mapping |

## Decision Flow

```
Request → Agent Coordinator → Safety Protocol → Guardrail Check
    ↓
    ├─ LOW RISK    → Execute immediately
    ├─ MEDIUM RISK → Request approval → Execute
    ├─ HIGH RISK   → Full review + approval → Execute
    └─ CRITICAL    → Block + escalate
```

## Always Safe

- `kubectl get/describe/logs`
- AWS describe/list commands
- File reading, code analysis
- Running tests

## Always Requires Approval

- `kubectl apply` (any environment)
- Database migrations
- IAM/KMS changes
- Production deployments

## Always Blocked

- Hardcoded credentials
- Disabling encryption
- Resources outside eu-central-1
- Skipping `calculation_audit` before `forensic_flags`
- Deploying high-risk AI without model card

## Compliance Mapping

| Guardrail | BaFin AT 8.1 | GDPR Art 32 | DORA Art 11 | EU AI Act |
|---|---|---|---|---|
| agent-restrictions.md | ✓ | ✓ | ✓ | ✓ |
| cost-guards.md | ✓ | — | ✓ | — |
| safety-protocol.md | ✓ | ✓ | ✓ | ✓ |
