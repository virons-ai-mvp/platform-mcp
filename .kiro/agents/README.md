# MCP Platform Agents

Specialized agents for platform-mcp development tasks. These agents reference workspace-level agent definitions in `../.ai/agents/`.

## Available Agents

### python-mcp-engineer
**Purpose**: Python MCP server development and tool creation
**Base Agent**: `../.ai/agents/roles/backend/python-backend-engineer.agent.md`
**Tools**: read, write, shell, grep, glob
**Use When**: Developing MCP servers, creating tools, writing Python code

### mcp-tool-specialist
**Purpose**: MCP tool development and documentation
**Base Agent**: `../.ai/agents/roles/ai/agentic-ai-expert.agent.md`
**Tools**: read, write, shell, grep, glob
**Use When**: Creating new tools, documenting tools, validating tool documentation

### compliance-validator
**Purpose**: BaFin, GDPR, DORA, EU AI Act compliance validation
**Base Agent**: `../.ai/agents/roles/security/compliance-monitor.agent.md`
**Tools**: read, grep, glob (read-only)
**Use When**: Validating compliance, auditing security, checking regulatory requirements

### devops-engineer
**Purpose**: Docker, Kubernetes, CI/CD, deployment automation
**Base Agent**: `../.ai/agents/roles/devops/expert-devops-engineer.agent.md`
**Tools**: read, write, shell, grep, glob
**Use When**: Deploying services, managing infrastructure, configuring CI/CD

## Workspace-Level Coordinator

Use `virons-agent` CLI to access the workspace-level agent coordinator:
- **Agent**: `../.ai/agents/orchestration/agent-coordinator.md`
- **Purpose**: Routes requests to specialized agents with guardrails
- **Features**: Risk assessment, approval gates, compliance checks

```bash
# Use virons-agent coordinator
kiro chat --agent virons-agent
```

## Available Agents

### python-mcp-engineer
**Purpose**: Python MCP server development and tool creation
**Tools**: read, write, shell, grep, glob
**Use When**: Developing MCP servers, creating tools, writing Python code

### mcp-tool-specialist
**Purpose**: MCP tool development and documentation
**Tools**: read, write, shell, grep, glob
**Use When**: Creating new tools, documenting tools, validating tool documentation

### compliance-validator
**Purpose**: BaFin, GDPR, DORA, EU AI Act compliance validation
**Tools**: read, grep, glob (read-only)
**Use When**: Validating compliance, auditing security, checking regulatory requirements

### devops-engineer
**Purpose**: Docker, Kubernetes, CI/CD, deployment automation
**Tools**: read, write, shell, grep, glob
**Use When**: Deploying services, managing infrastructure, configuring CI/CD

## Agent Selection Matrix

| Task | Agent | Rationale |
|------|-------|-----------|
| Create new MCP tool | mcp-tool-specialist | Specialized in tool development |
| Fix Python code | python-mcp-engineer | Python expertise |
| Update documentation | mcp-tool-specialist | Documentation focus |
| Validate compliance | compliance-validator | Compliance expertise |
| Deploy to Kubernetes | devops-engineer | Infrastructure expertise |
| Write tests | python-mcp-engineer | Testing expertise |
| Security audit | compliance-validator | Security focus |
| Docker optimization | devops-engineer | Container expertise |

## Usage

### Via Kiro CLI

```bash
# Use specific agent
kiro chat --agent python-mcp-engineer

# List available agents
kiro agents list
```

### Via Agent Configuration

Agents are defined in `.kiro/agents/*.json` files with:
- Name and description
- Prompt/instructions
- Allowed tools
- MCP server access

## Coordination Patterns

### Sequential Tasks
Use agents in sequence for dependent tasks:
1. python-mcp-engineer → Create tool
2. mcp-tool-specialist → Document tool
3. compliance-validator → Validate compliance

### Parallel Tasks
Use agents in parallel for independent tasks:
- python-mcp-engineer → Implement tool A
- python-mcp-engineer → Implement tool B
- devops-engineer → Update deployment

### Review Pattern
Use compliance-validator to review work:
1. python-mcp-engineer → Make changes
2. compliance-validator → Review and validate
3. python-mcp-engineer → Fix issues if needed

## Best Practices

1. **Choose the right agent** - Use the agent selection matrix
2. **Provide context** - Load relevant documentation before invoking agent
3. **Sequential for dependencies** - Use sequential pattern when tasks depend on each other
4. **Parallel for independence** - Use parallel pattern when tasks are independent
5. **Validate after changes** - Always run compliance-validator after significant changes

## Related

- Commands: `.kiro/commands/`
- Workflows: `.kiro/workflows/`
- Steering: `.kiro/steering/`
