# Docs Mirror Checklist

**Date**: 2026-03-05  
**Task**: Mirror platform-infrastructure/docs to platform-mcp/docs

## ✅ Completed

- [x] Created directory structure matching platform-infrastructure
- [x] Created main docs/README.md with MCP-specific content
- [x] Created placeholder READMEs in all subdirectories
- [x] Adapted content for MCP server context

## 📁 Directory Structure Created

```
docs/
├── README.md
├── architecture/
│   ├── ddd/
│   ├── decisions/
│   ├── diagrams/
│   ├── governance/
│   └── implementation/
├── compliance/
│   ├── audits/
│   ├── bafin/
│   ├── dora/
│   ├── evidence/
│   ├── gdpr/
│   ├── policies/
│   ├── references/
│   └── reports/
├── development/
│   ├── contributing/
│   ├── tdd/
│   └── testing/
├── getting-started/
├── governance/
├── infrastructure/
│   ├── ai/
│   ├── eks/
│   ├── foundation/
│   ├── governance/
│   ├── modules/
│   └── status/
├── operations/
│   ├── procedures/
│   ├── process/
│   └── runbooks/
├── reference/
│   ├── aws-mcp/
│   └── style-guides/
└── security/
```

## 📝 Files Created

- [x] `docs/README.md` - Main documentation index
- [x] `docs/architecture/README.md` + subdirectories
- [x] `docs/compliance/README.md` + subdirectories (BaFin, GDPR, DORA)
- [x] `docs/development/README.md` + subdirectories
- [x] `docs/getting-started/README.md`
- [x] `docs/governance/README.md`
- [x] `docs/infrastructure/README.md` + subdirectories
- [x] `docs/operations/README.md` + subdirectories
- [x] `docs/reference/README.md` + subdirectories
- [x] `docs/security/README.md`

## 🎯 Next Steps

- [x] Populate architecture/ddd/ with MCP bounded contexts
- [x] Create ADRs in architecture/decisions/ (ADR-001: Port Allocation)
- [x] Document MCP servers in getting-started/ (QUICKSTART.md)
- [x] Add compliance evidence for BaFin AT 8.1, DORA Art 11
- [x] Create runbooks for secrets-rotation, MCP server outage
- [x] Add security policies for MCP server access
- [x] Add GDPR Art 25/32 compliance docs
- [x] **AWS MCP Server Integration Audit** ⭐ NEW
  - [x] Server catalog (67 AWS MCP servers)
  - [x] Scoring framework (compliance/operational/platform/development)
  - [x] Server scores (Tier 1: 33, Tier 2: 25, Tier 3: 8)
  - [x] Context mapping (10 bounded contexts, 9100-9199)
  - [x] ADR-002: AWS MCP Integration decision
  - [x] Integration backlog (Phase 2/3 roadmap)
  - [x] Implementation checklist (execution plan)
- [ ] Document Kind cluster setup in infrastructure/foundation/
- [ ] Create style guides in reference/style-guides/
- [ ] Create architecture diagrams in architecture/diagrams/
- [ ] Add contributing guide in development/contributing/

## 🔗 References

- Source: `platform-infrastructure/docs`
- Target: `platform-mcp/docs`
- Compliance: BaFin AT 8.1, GDPR Art 25/32, DORA Art 11
