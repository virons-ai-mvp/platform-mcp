# Virons Services Agent Directory

All specialized agents for the virons-services platform. Each agent loads its instructions from `.ai/agents/` and enforces TDD + compliance requirements.

## Quick Reference

```bash
# List all available agents
ls -1 .kiro/agents/*.json | xargs -n1 basename | sed 's/.json//'

# Invoke an agent (example)
kiro chat --agent testing-engineer
```

## Agent Catalog (16 agents)

### Backend Development (4)
- **go-backend-engineer** — Go 1.23 microservices (ingestion :9101-:9117, blockchain :9430-:9432, API :6001-:8002)
- **python-backend-engineer** — Python 3.12 services (forensic :9300-:9415, ML :9420-:9424)
- **api-engineer** — REST/WebSocket APIs, JWT auth, RFC 7807, 100% audit logging
- **frontend-engineer** — Next.js 15, investor dashboard (:6001), guided demo (:6002)

### ML & AI (1)
- **ml-engineer** — Bedrock (Nova Pro), SageMaker, model training/deployment, EU AI Act compliance

### Testing & Quality (1)
- **testing-engineer** — TDD-first, unit/integration/e2e, testcontainers, 95% coverage minimum

### Documentation (1)
- **documentation-engineer** — Technical docs, API docs, architecture diagrams, model cards

### Security & Compliance (2)
- **security-engineer** — IAM hardening, KMS, WAF, threat modeling, security audits
- **compliance-monitor** — BaFin MaRisk AT 8.1, GDPR Art 32, DORA Art 11, EU AI Act (read-only)

### Infrastructure & Operations (5)
- **devops-engineer** — CI/CD, GitHub Actions, ArgoCD, security scanning, image signing
- **kubernetes-engineer** — EKS 1.31, K8s manifests, Helm, KEDA, OPA policies
- **aws-architect** — Terraform, VPC, EKS, IAM design, Well-Architected reviews
- **disaster-recovery-agent** — DR planning, RTO ≤ 4h, RPO ≤ 1h, backup strategies
- **database-manager** — RDS PostgreSQL, ElastiCache Redis, pgvector, migrations

### FinTech & Cost (1)
- **finops-agent** — Cost optimization, budget gates, right-sizing (read-only)

### Repository Management (1)
- **repo-manager** — Monorepo structure, 42-service organization, code quality

## Agent Selection Guide

### By Task Type
| Task | Primary Agent | Supporting Agents |
|------|---------------|-------------------|
| New Go service | go-backend-engineer | testing-engineer, compliance-monitor |
| New Python service | python-backend-engineer | testing-engineer, compliance-monitor |
| API endpoint | api-engineer | testing-engineer, security-engineer |
| ML model | ml-engineer | testing-engineer, compliance-monitor |
| Frontend feature | frontend-engineer | testing-engineer |
| Infrastructure change | aws-architect | security-engineer, compliance-monitor |
| K8s deployment | kubernetes-engineer | devops-engineer |
| Security audit | security-engineer | compliance-monitor |
| Cost optimization | finops-agent | aws-architect, kubernetes-engineer |
| Documentation | documentation-engineer | — |

### By Namespace
| Namespace | Primary Agent | Port Range |
|-----------|---------------|------------|
| ingestion/ | go-backend-engineer | 9101-9117 |
| forensic/ | python-backend-engineer | 9300-9415 |
| ml/ | ml-engineer | 9420-9424 |
| blockchain/ | go-backend-engineer | 9430-9432 |
| api/ | api-engineer | 6001-8002 |

## Coordination Patterns

### Single Agent (Simple Tasks)
```
User: "Add health endpoint to beneish-calculator"
→ python-backend-engineer
```

### Sequential (Multi-Phase)
```
User: "Create new forensic service"
→ python-backend-engineer (scaffold)
→ testing-engineer (tests)
→ compliance-monitor (validate)
```

### Parallel (Independent Tasks)
```
User: "Update READMEs and add integration tests"
→ documentation-engineer (READMEs) || testing-engineer (tests)
```

### Compliance Gate (Always Required)
Add `compliance-monitor` for:
- Production changes
- Security/IAM changes
- New forensic/ML services
- Regulatory-sensitive code

## Agent Capabilities

### Read-Only Agents
- `compliance-monitor` — validation only, no modifications
- `finops-agent` — analysis only, no infrastructure changes

### High-Risk Agents (Extra Validation Required)
- `aws-architect` — infrastructure changes
- `security-engineer` — IAM/KMS changes
- `ml-engineer` — model deployment

### Always-Safe Agents
- `documentation-engineer` — docs only
- `testing-engineer` — tests only
- `repo-manager` — structure only

## Workflow Examples

### New Service Workflow
1. **Scaffold**: `go-backend-engineer` or `python-backend-engineer`
2. **Test**: `testing-engineer` — comprehensive test suite
3. **Document**: `documentation-engineer` — README, API docs
4. **Validate**: `compliance-monitor` — regulatory check
5. **Deploy**: `devops-engineer` — CI/CD pipeline

### Security Audit Workflow
1. **Threat Model**: `security-engineer`
2. **Compliance**: `compliance-monitor`
3. **Network**: `kubernetes-engineer` — NetworkPolicies
4. **Scanning**: `devops-engineer` — Trivy, CodeQL

### Performance Optimization Workflow
1. **Database**: `database-manager` — query optimization
2. **Resources**: `kubernetes-engineer` — HPA, resource limits
3. **Cost**: `finops-agent` — cost analysis
4. **Monitoring**: `devops-engineer` — CloudWatch, Prometheus

## References

- **Agent Definitions**: `.ai/agents/roles/`
- **Orchestration**: `.ai/agents/orchestration/agent-coordinator.md`
- **Workflows**: `.ai/agents/workflows/`
- **Safety Protocol**: `.ai/agents/orchestration/safety-protocol.md`
- **Coordination Guide**: `.kiro/steering/agents.md`

## Maintenance

To regenerate agent configurations:
```bash
python3 scripts/generate-kiro-agents.py
```

This reads `.ai/agents/roles/**/*.agent.md` and generates `.kiro/agents/*.json` files.
