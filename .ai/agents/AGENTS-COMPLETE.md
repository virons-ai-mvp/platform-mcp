# Platform-Services Agent Specialists — Complete

## ✅ All Agent Specialists Defined

### Backend Engineers (2)
1. **Python Backend Engineer** - forensic/, ml/ services
   - FastAPI, Pydantic, asyncio
   - BaFin AT 8.1 compliance (audit-first pattern)
   - ML gate enforcement
   - TDD with 95% coverage

2. **Go Backend Engineer** - ingestion/, blockchain/, api/ services
   - Go 1.23, Gin/Echo, goroutines
   - SHA-256 hashing (ingestion)
   - Async blockchain writes
   - 100% API audit logging

### Specialized Engineers (5)
3. **API Engineer** - REST/WebSocket APIs
   - RFC 7807 error format
   - JWT authentication, rate limiting
   - OpenAPI documentation
   - 100% request audit logging

4. **Frontend Engineer** - Next.js dashboards
   - Next.js 15, React 19, TypeScript
   - WCAG 2.1 AA accessibility
   - Real-time WebSocket updates
   - Core Web Vitals optimization

5. **Testing Engineer** - TDD enforcement
   - Test-first development
   - 95% coverage minimum
   - Unit/integration/E2E tests
   - Coverage analysis and reporting

6. **Documentation Engineer** - Compliance docs
   - Model cards (EU AI Act)
   - Architecture Decision Records (ADRs)
   - API documentation (OpenAPI)
   - Runbooks and playbooks

7. **ML Engineer** - ML/AI systems
   - Bedrock integration
   - IsolationForest ensemble
   - Model cards for high-risk AI
   - EU AI Act compliance

### Infrastructure & Operations (5)
8. **DevOps Engineer** - CI/CD pipelines
9. **Kubernetes Engineer** - EKS, ArgoCD
10. **Database Manager** - PostgreSQL, Redis
11. **AWS Architect** - AWS services
12. **Disaster Recovery** - DR planning

### Security & Compliance (2)
13. **Compliance Monitor** - BaFin, GDPR, DORA, EU AI Act
14. **Cyber Security** - Threat modeling, security review

### Financial Operations (2)
15. **FinOps Agent** - Cost optimization
16. **Repo Manager** - Service catalog governance

## Total: 16 Specialized Agents

## Agent Files Created

```
.ai/agents/roles/
├── backend/
│   ├── python-backend-engineer.agent.md ✅
│   └── go-backend-engineer.agent.md ✅
├── api/
│   └── api-engineer.agent.md ✅
├── frontend/
│   └── frontend-engineer.agent.md ✅
├── testing/
│   └── testing-engineer.agent.md ✅
├── documentation/
│   └── documentation-engineer.agent.md ✅
├── ml/
│   └── expert-ml-engineer.agent.md (existing)
├── devops/
│   └── expert-devops-engineer.agent.md (existing)
├── kubernetes/
│   └── expert-kubernetes-engineer.agent.md (existing)
├── database/
│   └── database-manager.agent.md (existing)
├── infrastructure/
│   ├── aws-architect.agent.md (existing)
│   └── disaster-recovery-agent.agent.md (existing)
├── security/
│   ├── compliance-monitor.agent.md (existing)
│   └── expert-cyber-security.agent.md (existing)
├── fintech/
│   └── finops-agent.agent.md (existing)
└── repo-manager/
    └── expert-repo-manager.agent.md (existing)
```

## Kiro CLI Agent Swap

All agents are now accessible via `/agent swap` in kiro-cli:

```bash
# Backend
/agent swap python-backend-engineer
/agent swap go-backend-engineer

# Specialized
/agent swap api-engineer
/agent swap frontend-engineer
/agent swap testing-engineer
/agent swap documentation-engineer
/agent swap expert-ml-engineer

# Infrastructure
/agent swap expert-devops-engineer
/agent swap expert-kubernetes-engineer
/agent swap database-manager
/agent swap aws-architect
/agent swap disaster-recovery-agent

# Security
/agent swap compliance-monitor
/agent swap expert-cyber-security

# Financial
/agent swap finops-agent
/agent swap expert-repo-manager
```

## Agent Selection Logic

Agents are automatically selected based on:

1. **File Path Detection**
   - `forensic/*.py` → Python Backend Engineer
   - `ingestion/*.go` → Go Backend Engineer
   - `api/rest-api/` → API Engineer
   - `api/investor-dashboard/` → Frontend Engineer

2. **Task Type Detection**
   - Testing tasks → Testing Engineer
   - Documentation tasks → Documentation Engineer
   - ML model work → ML Engineer
   - Compliance validation → Compliance Monitor

3. **Explicit User Request**
   - User runs `/agent swap <agent-name>`

## Key Features Per Agent

### Python Backend Engineer
- BaFin AT 8.1: `write_audit()` before `forensic_flags`
- ML gate: `gated_ml = ml_score if len(deterministic_flags) >= 1 else 0.0`
- Shared package: `from virons_common import write_audit, get_logger`

### Go Backend Engineer
- SHA-256 hashing for all ingested artifacts
- Async blockchain writes (never block)
- 100% API request audit logging

### API Engineer
- RFC 7807 error format
- Rate limiting per user/IP
- OpenAPI 3.0 documentation

### Frontend Engineer
- WCAG 2.1 AA accessibility
- Real-time WebSocket updates
- Core Web Vitals optimization

### Testing Engineer
- TDD enforcement (test-first)
- 95% coverage minimum
- Unit/integration/E2E/load tests

### Documentation Engineer
- Model cards for high-risk AI (EU AI Act)
- Architecture Decision Records (ADRs)
- Compliance documentation

## Next Steps

1. ✅ All 16 agents defined
2. ✅ Agent README updated
3. ✅ Kiro CLI agent swap ready
4. 🔄 Apply same structure to other repos:
   - platform-orchestrator-gateway
   - platform-mcp
   - platform-infrastructure
   - platform-ui

---

**Created**: 2026-03-07
**Status**: ✅ Complete
**Total Agents**: 16 specialists
