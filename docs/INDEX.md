# Platform MCP Documentation Index

## Quick Links

### Getting Started
- [README](../README.md) - Project overview and quick start
- [Quickstart Guide](getting-started/QUICKSTART.md)

### Architecture (Domain Design)
- [Design Guidelines](architecture/design-guidelines.md) - DDD principles and patterns
- [MCP Server Standard](architecture/mcp-server-standard.md) - Gateway pattern for all servers
- [MCP Servers Overview](architecture/mcp-servers-overview.md) - All 90 tools catalog
- [MCP Server Script Implementation](architecture/mcp-server-script-implementation.md)
- [DDD Architecture](architecture/ddd/README.md)
- [Architecture Decisions](architecture/decisions/)
- [AWS MCP Audit](architecture/aws-mcp-audit/)

### Operations (Infrastructure)
- [Deployment Guide](operations/deployment.md)
- [Docker Optimization](operations/docker-optimization.md)
- [Runbooks](operations/runbooks/)

### Development
- [Developer Guide](development/developer-guide.md)
- [Coding Tips](development/coding-tips.md)
- [Contributing](development/contributing.md)

### Governance
- [Code of Conduct](governance/code-of-conduct.md)

### Compliance
- [BaFin Compliance](compliance/bafin/)
- [DORA Compliance](compliance/dora/)
- [GDPR Compliance](compliance/gdpr/)

### Security
- [MCP Security Policies](security/MCP-SECURITY-POLICIES.md)

### Reference
- [AWS MCP Audit Summary](reference/aws-mcp-audit-summary.md)
- [Docs Mirror Checklist](reference/docs-mirror-checklist.md)

## Documentation Structure (DDD)

```
docs/
├── architecture/          # Domain models, technical design
│   ├── design-guidelines.md
│   ├── mcp-server-standard.md
│   ├── mcp-servers-overview.md
│   ├── ddd/
│   ├── decisions/
│   └── aws-mcp-audit/
├── operations/           # Infrastructure, deployment
│   ├── deployment.md
│   ├── docker-optimization.md
│   └── runbooks/
├── development/          # Contributing, coding
│   ├── developer-guide.md
│   ├── coding-tips.md
│   └── contributing.md
├── governance/           # Policies, conduct
│   └── code-of-conduct.md
├── compliance/           # Regulatory requirements
│   ├── bafin/
│   ├── dora/
│   └── gdpr/
├── security/            # Security policies
└── reference/           # Audits, checklists
    ├── aws-mcp-audit-summary.md
    └── docs-mirror-checklist.md
```
