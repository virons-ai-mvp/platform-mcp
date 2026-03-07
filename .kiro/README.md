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
├── commands/              ← slash commands
│   ├── new-tool.md
│   └── compliance-audit.md
├── steering/              ← always-loaded context
│   ├── project.md         ← MCP server catalog, compliance, quick commands
│   ├── context.md         ← auto-load manifest + on-demand index
│   └── compliance.md      ← regulatory requirements
└── workflows/             ← workflow definitions
    └── tool-development.md
```

## Agents

**All agents are defined at workspace level** in `../.kiro/agents/`.

Use `virons-agent` CLI to access the agent coordinator and specialized agents:

```bash
# Use workspace-level agent coordinator
kiro chat --agent virons-agent
```

Available workspace agents:
- `virons-agent` - Agent coordinator with routing and guardrails
- `python-backend-engineer` - Python development
- `devops-engineer` - Docker, Kubernetes, CI/CD
- `compliance-monitor` - BaFin, GDPR, DORA validation
- `aws-architect` - AWS infrastructure design
- `kubernetes-engineer` - Kubernetes operations
- And 10+ more specialized agents

See `../.kiro/agents/README.md` for complete agent catalog.
