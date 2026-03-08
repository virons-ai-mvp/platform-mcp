# Agent Coordinator

Orchestration layer for virons-services AI agents.

## Agent Roles

| Agent | Scope |
|---|---|
| `go-backend-engineer` | ingestion, blockchain, api (Go services) |
| `python-backend-engineer` | forensic, ml (Python services) |
| `ml-engineer` | ml namespace, EU AI Act compliance |
| `devops-engineer` | K8s manifests, Dockerfiles, EKS, IRSA |
| `compliance-validator` | BaFin/GDPR/DORA/EU AI Act audits |
| `security-auditor` | trivy, gosec, bandit, gitleaks |
| `service-scaffolder` | new service creation |

## Coordination Protocol

1. Receive request
2. Apply Safety Protocol (see `safety-protocol.md`)
3. Consult `service-agent-matrix.md` for agent selection
4. Delegate to appropriate agent(s)
5. Validate outputs
6. Return results

## Multi-Agent Tasks

| Task | Agents Involved |
|---|---|
| New forensic service | service-scaffolder + python-backend-engineer + compliance-validator |
| Production deployment | devops-engineer + security-auditor + compliance-validator |
| ML model update | ml-engineer + compliance-validator (EU AI Act) |
| Security incident | security-auditor + devops-engineer |

## Handoff Rules

- Always include `compliance-validator` for forensic/ml changes
- Always include `security-auditor` for production deployments
- `ml-engineer` owns all EU AI Act decisions — not overridable
