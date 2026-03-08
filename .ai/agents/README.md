# Agent Index — platform-services

All agents scoped to this repo's role: **42 microservices across 5 namespaces (ingestion, forensic, ml, blockchain, api)**.

## Backend Engineers

| Agent | File | Trigger |
|-------|------|---------|
| Python Backend Engineer | `roles/backend/python-backend-engineer.agent.md` | forensic/, ml/ services |
| Go Backend Engineer | `roles/backend/go-backend-engineer.agent.md` | ingestion/, blockchain/, api/ services |

## Specialized Engineers

| Agent | File | Trigger |
|-------|------|---------|
| API Engineer | `roles/api/api-engineer.agent.md` | REST/WebSocket APIs, authentication |
| Frontend Engineer | `roles/frontend/frontend-engineer.agent.md` | Next.js dashboards, UI components |
| Testing Engineer | `roles/testing/testing-engineer.agent.md` | TDD enforcement, coverage, test strategy |
| Documentation Engineer | `roles/documentation/documentation-engineer.agent.md` | Model cards, ADRs, compliance docs |
| ML Engineer | `roles/ml/expert-ml-engineer.agent.md` | Bedrock, IsolationForest, model cards |

## Infrastructure & Operations

| Agent | File | Trigger |
|-------|------|---------|
| DevOps Engineer | `roles/devops/expert-devops-engineer.agent.md` | CI/CD, GitHub Actions, deployments |
| Kubernetes Engineer | `roles/kubernetes/expert-kubernetes-engineer.agent.md` | EKS, ArgoCD, K8s manifests |
| Database Manager | `roles/database/database-manager.agent.md` | PostgreSQL, Redis, migrations |
| AWS Architect | `roles/infrastructure/aws-architect.agent.md` | AWS services, architecture |
| Disaster Recovery | `roles/infrastructure/disaster-recovery-agent.agent.md` | DR planning, RTO/RPO |

## Security & Compliance

| Agent | File | Trigger |
|-------|------|---------|
| Compliance Monitor | `roles/security/compliance-monitor.agent.md` | BaFin, GDPR, DORA, EU AI Act |
| Cyber Security | `roles/security/expert-cyber-security.agent.md` | Threat modeling, security review |

## Financial Operations

| Agent | File | Trigger |
|-------|------|---------|
| FinOps Agent | `roles/fintech/finops-agent.agent.md` | Cost optimization, budget gates |
| Repo Manager | `roles/repo-manager/expert-repo-manager.agent.md` | Repo governance, service catalog |

## Orchestration

- `orchestration/agent-coordinator.md` — how agents are selected and coordinated
- `orchestration/safety-protocol.md` — risk assessment, approval gates

## Guardrails (always active)

- `agent-restrictions.md` — what agents can/cannot do
- `cost-guards.md` — budget limits per environment
- `GUARDRAILS-README.md` — comprehensive guardrails documentation

## Workflows

| Workflow | File |
|----------|------|
| Service Development | `workflows/service-development.md` |
| Testing | `workflows/testing-workflows.md` |
| Security | `workflows/security-workflows.md` |
| Deployment | `workflows/deployment-workflows.md` |
| Monitoring | `workflows/monitoring-workflows.md` |
| Documentation | `workflows/documentation-workflows.md` |
| Database Migration | `workflows/database-migration.md` |
| Inter-Service Communication | `workflows/inter-service-communication.md` |
| Pre-execution Checklist | `workflows/pre-execution-checklist.md` |

## Agent Selection Guide

### When to use which agent:

**Backend Development:**
- Python services (forensic, ml) → Python Backend Engineer
- Go services (ingestion, blockchain, api) → Go Backend Engineer

**API Work:**
- REST/WebSocket endpoints → API Engineer
- Authentication, rate limiting → API Engineer

**Frontend Work:**
- Dashboard UI → Frontend Engineer
- React components → Frontend Engineer

**Testing:**
- TDD enforcement → Testing Engineer
- Coverage analysis → Testing Engineer
- Test strategy → Testing Engineer

**Documentation:**
- Model cards → Documentation Engineer
- ADRs → Documentation Engineer
- Compliance docs → Documentation Engineer

**ML/AI:**
- Bedrock integration → ML Engineer
- Model training → ML Engineer
- EU AI Act compliance → ML Engineer + Compliance Monitor

**Infrastructure:**
- K8s manifests → Kubernetes Engineer
- CI/CD pipelines → DevOps Engineer
- AWS resources → AWS Architect

**Security:**
- Compliance validation → Compliance Monitor
- Security review → Cyber Security
- Threat modeling → Cyber Security

**Operations:**
- Cost optimization → FinOps Agent
- Database work → Database Manager
- DR planning → Disaster Recovery

## Quick Commands

```bash
# List all agents
ls -la .ai/agents/roles/*/

# Search for agent by keyword
grep -r "keyword" .ai/agents/roles/

# View agent details
cat .ai/agents/roles/backend/python-backend-engineer.agent.md
```

## Agent Swap in Kiro CLI

All agents are available via `/agent swap` command in kiro-cli:

```bash
# Swap to Python backend engineer
/agent swap python-backend-engineer

# Swap to testing engineer
/agent swap testing-engineer

# Swap to compliance monitor
/agent swap compliance-monitor
```

Agents are automatically selected based on:
1. File path (namespace detection)
2. Task type (testing, documentation, etc.)
3. Explicit user request
