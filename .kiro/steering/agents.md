# Agent Coordination Guide

Reference for selecting and coordinating specialized agents in virons-services.

## Agent Selection Matrix

### Backend Development
| Task | Agent | Tools |
|------|-------|-------|
| Go services (ingestion, blockchain, API) | `go-backend-engineer` | read, write, shell, grep, glob |
| Python services (forensic, ML) | `python-backend-engineer` | read, write, shell, grep, glob |
| REST/WebSocket APIs | `api-engineer` | read, write, shell, grep, glob |
| Next.js frontend | `frontend-engineer` | read, write, shell, grep, glob |

### ML & AI
| Task | Agent | Tools |
|------|-------|-------|
| Bedrock, SageMaker, model ops | `ml-engineer` | read, write, shell, grep, glob |

### Testing & Quality
| Task | Agent | Tools |
|------|-------|-------|
| TDD, unit/integration tests, coverage | `testing-engineer` | read, write, shell, grep, glob |

### Documentation
| Task | Agent | Tools |
|------|-------|-------|
| Technical docs, API docs, diagrams | `documentation-engineer` | read, write, grep, glob |

### Security & Compliance
| Task | Agent | Tools |
|------|-------|-------|
| IAM, KMS, WAF, threat modeling | `security-engineer` | read, write, shell, grep, glob |
| BaFin, GDPR, DORA, EU AI Act | `compliance-monitor` | read, grep, glob |

### Infrastructure & Operations
| Task | Agent | Tools |
|------|-------|-------|
| CI/CD, GitHub Actions, ArgoCD | `devops-engineer` | read, write, shell, grep, glob |
| EKS, K8s manifests, Helm | `kubernetes-engineer` | read, write, shell, grep, glob |
| Terraform, VPC, IAM design | `aws-architect` | read, write, shell, grep, glob |
| DR planning, RTO/RPO | `disaster-recovery-agent` | read, write, shell, grep, glob |
| RDS, ElastiCache, migrations | `database-manager` | read, write, shell, grep, glob |

### FinTech & Cost
| Task | Agent | Tools |
|------|-------|-------|
| Cost optimization, budget gates | `finops-agent` | read, grep, glob |

### Repository Management
| Task | Agent | Tools |
|------|-------|-------|
| Monorepo structure, organization | `repo-manager` | read, write, grep, glob |

## Coordination Patterns

### Single Agent
Simple tasks with clear scope:
```
User: "Add health endpoint to beneish-calculator"
→ python-backend-engineer
```

### Sequential Agents
Tasks requiring multiple phases:
```
User: "Create new forensic service"
→ python-backend-engineer (scaffold)
→ testing-engineer (add tests)
→ compliance-monitor (validate)
```

### Parallel Agents
Independent tasks that can run simultaneously:
```
User: "Update all service READMEs and add integration tests"
→ documentation-engineer (READMEs)
→ testing-engineer (tests)
```

### Compliance Gate
Always add compliance-monitor for:
- Production changes
- Security/IAM changes
- New forensic/ML services
- Regulatory-sensitive code

## Quick Reference

**Read-only agents** (no write access):
- `compliance-monitor`
- `finops-agent`

**High-risk agents** (require extra validation):
- `aws-architect` (infrastructure changes)
- `security-engineer` (IAM/KMS changes)
- `ml-engineer` (model deployment)

**Always-safe agents**:
- `documentation-engineer`
- `testing-engineer`
- `repo-manager`

## Example Workflows

### New Service
1. `go-backend-engineer` or `python-backend-engineer` — scaffold
2. `testing-engineer` — add comprehensive tests
3. `documentation-engineer` — write docs
4. `compliance-monitor` — validate compliance
5. `devops-engineer` — add CI/CD

### Security Audit
1. `security-engineer` — threat modeling
2. `compliance-monitor` — regulatory check
3. `kubernetes-engineer` — network policies
4. `devops-engineer` — security scanning

### Performance Optimization
1. `database-manager` — query optimization
2. `kubernetes-engineer` — resource tuning
3. `finops-agent` — cost analysis
4. `devops-engineer` — monitoring setup

## References

- Full agent definitions: `.ai/agents/roles/`
- Orchestration logic: `.ai/agents/orchestration/agent-coordinator.md`
- Workflows: `.ai/agents/workflows/`
- Safety protocol: `.ai/agents/orchestration/safety-protocol.md`
