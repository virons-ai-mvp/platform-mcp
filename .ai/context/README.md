# .ai/ — Machine-Readable AI Context

This directory provides structured context for AI agents and tools.

## Structure

```
.ai/
├── context/
│   ├── repository.json     ← Full service registry, ports, compliance rules
│   └── README.md           ← This file
├── rules/
│   ├── repository-guidelines.md
│   ├── agent-restrictions.md
│   ├── cost-guards.md
│   ├── GUARDRAILS-README.md
│   ├── orchestration/
│   │   ├── agent-coordinator.md
│   │   ├── safety-protocol.md
│   │   └── service-agent-matrix.md
│   └── workflows/
│       ├── testing-workflows.md
│       ├── security-workflows.md
│       ├── deployment-workflows.md
│       ├── monitoring-workflows.md
│       ├── documentation-workflows.md
│       ├── pre-execution-checklist.md
│       ├── service-development.md
│       ├── inter-service-communication.md
│       └── database-migration.md
├── agents/
│   ├── go-backend.md
│   ├── python-backend.md
│   ├── ml-engineer.md
│   ├── devops.md
│   └── compliance.md
├── mcp/
│   └── mcp.json
└── tools/
    └── README.md
```

## Quick Reference

- All 42 services, ports, namespaces → `context/repository.json`
- Critical compliance rules → `context/repository.json#critical_rules`
- Agent selection → `rules/orchestration/service-agent-matrix.md`
- Cost limits → `rules/cost-guards.md`
