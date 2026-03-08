# platform-services Kiro Configuration

Kiro configuration for 42 microservices for forensic analysis, ML, blockchain, and API.

## Structure

```
.kiro/
├── README.md              ← this file
├── settings.json          ← repo-specific settings (inherits workspace)
├── commands/              ← repo-specific slash commands
├── steering/              ← repo-specific context (auto-loaded)
│   ├── project.md         ← project overview, quick commands
│   └── context.md         ← auto-load manifest
└── workflows/             ← repo-specific workflows
```

## Agents

**All agents are defined at workspace level** in `../.kiro/agents/`.

Use `virons-agent` CLI to access the agent coordinator and specialized agents:

```bash
# Use workspace-level agent coordinator
kiro chat --agent virons-agent
```

See `../.kiro/agents/README.md` for complete agent catalog.

## Settings

This repo inherits workspace settings from `../.kiro/settings.json` and adds repo-specific overrides.

**Type**: microservices-monorepo
**Languages**: go, python

## Steering Files

**project.md** is always loaded at session start. Keep it under 150 lines.

**context.md** defines what else gets auto-loaded and what loads on-demand.
Total auto-load budget: ~10KB. Leave 190KB for task context.

## Commands

Repo-specific slash commands for common operations.

## Workflows

Repo-specific workflows for development tasks.
