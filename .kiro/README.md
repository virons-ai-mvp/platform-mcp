# platform-mcp Kiro Configuration

Kiro steering and settings for the platform-mcp multi-service MCP platform with 90 tools.

## Structure

```
.kiro/
├── README.md              ← this file
├── SECURITY-POLICY.md     ← Kiro security and permissions
├── CONFIGURATION-SUMMARY.md   ← project configuration overview
├── CONFIGURATION-REFERENCE.md ← detailed settings reference
├── settings.json          ← project settings
├── agents/                ← specialized agent configurations
│   ├── virons-python-engineer.json
│   ├── virons-mcp-specialist.json
│   ├── virons-compliance-validator.json
│   └── virons-devops.json
├── commands/              ← slash commands
│   ├── new-tool.md
│   └── compliance-audit.md
├── skills/                ← reusable skills
│   ├── tool-generator/
│   ├── compliance-check/
│   └── security-validation/
├── steering/              ← always-loaded context
│   ├── project.md         ← MCP server catalog, compliance, quick commands
│   ├── context.md         ← auto-load manifest + on-demand index
│   └── compliance.md      ← regulatory requirements
├── workflows/             ← workflow definitions
│   └── tool-development.md
├── domains/               ← domain-specific context
│   └── mcp-tools.md
└── tests/                 ← test configurations
    └── README.md
```

## Steering Files

**project.md** is always loaded at session start. Keep it under 150 lines.
It contains the full MCP server catalog, tool counts, compliance coordinates, and critical rules.

**context.md** defines what else gets auto-loaded and what loads on-demand.
Total auto-load budget: ~10KB. Leave 190KB for task context.

**compliance.md** contains all regulatory requirements (BaFin, GDPR, DORA, EU AI Act).

## Commands

Slash commands for common operations:
- `/new-tool [server] [name] [category]` — scaffold new MCP tool
- `/compliance-audit [server|all]` — run compliance checks

## Skills

Reusable skills for common tasks:
- **tool-generator** — scaffold new MCP tools with proper structure
- **compliance-check** — validate BaFin/GDPR/DORA/EU AI Act compliance
- **security-validation** — run security scans and validation

## Agents

Specialized agents for different tasks:
- **virons-python-engineer** — Python development and testing
- **virons-mcp-specialist** — MCP server development and tool creation
- **virons-compliance-validator** — Compliance validation and auditing
- **virons-devops** — Deployment, Docker, Kubernetes operations

## Settings

See `settings.json` for complete project configuration including:
- AWS/Kubernetes settings
- Compliance frameworks
- Testing requirements
- Security policies
- MCP server configurations
- Monitoring and deployment settings
