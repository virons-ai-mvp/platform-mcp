# Using Virons Agents with Kiro

Quick guide for using the 16 specialized agents configured for virons-services.

## Quick Start

### List Available Agents
```bash
ls -1 .kiro/agents/*.json | xargs -n1 basename | sed 's/.json//'
```

### Invoke an Agent
```bash
kiro chat --agent <agent-name>
```

Example:
```bash
kiro chat --agent testing-engineer
kiro chat --agent compliance-monitor
kiro chat --agent go-backend-engineer
```

## Agent Selection Guide

### "I need to..."

**...create a new Go service**
```bash
kiro chat --agent go-backend-engineer
```
Then follow up with `testing-engineer` and `compliance-monitor`.

**...create a new Python service**
```bash
kiro chat --agent python-backend-engineer
```
Then follow up with `testing-engineer` and `compliance-monitor`.

**...add tests to a service**
```bash
kiro chat --agent testing-engineer
```

**...write documentation**
```bash
kiro chat --agent documentation-engineer
```

**...validate compliance**
```bash
kiro chat --agent compliance-monitor
```

**...deploy to Kubernetes**
```bash
kiro chat --agent kubernetes-engineer
```

**...optimize costs**
```bash
kiro chat --agent finops-agent
```

**...configure CI/CD**
```bash
kiro chat --agent devops-engineer
```

**...work with ML models**
```bash
kiro chat --agent ml-engineer
```

**...design infrastructure**
```bash
kiro chat --agent aws-architect
```

**...secure the system**
```bash
kiro chat --agent security-engineer
```

**...manage databases**
```bash
kiro chat --agent database-manager
```

**...plan disaster recovery**
```bash
kiro chat --agent disaster-recovery-agent
```

**...build APIs**
```bash
kiro chat --agent api-engineer
```

**...build frontend**
```bash
kiro chat --agent frontend-engineer
```

**...organize the repo**
```bash
kiro chat --agent repo-manager
```

## Multi-Agent Workflows

### New Service (Sequential)
```bash
# 1. Scaffold
kiro chat --agent python-backend-engineer
# Ask: "Create new forensic service: transaction-monitor on port 9408"

# 2. Add tests
kiro chat --agent testing-engineer
# Ask: "Add comprehensive tests for transaction-monitor"

# 3. Validate compliance
kiro chat --agent compliance-monitor
# Ask: "Validate compliance for forensic/transaction-monitor"

# 4. Deploy
kiro chat --agent devops-engineer
# Ask: "Add CI/CD for transaction-monitor"
```

### Security Audit (Parallel)
```bash
# Run these in separate sessions or sequentially
kiro chat --agent security-engineer
# Ask: "Perform threat modeling for API gateway"

kiro chat --agent compliance-monitor
# Ask: "Check GDPR compliance for API gateway"

kiro chat --agent kubernetes-engineer
# Ask: "Review NetworkPolicies for API namespace"
```

## Agent Capabilities

### Read-Only (Safe to Run Anytime)
- `compliance-monitor` — validation only
- `finops-agent` — cost analysis only

### Write Access (Review Changes)
- `go-backend-engineer`
- `python-backend-engineer`
- `api-engineer`
- `frontend-engineer`
- `testing-engineer`
- `documentation-engineer`
- `devops-engineer`
- `kubernetes-engineer`
- `database-manager`
- `repo-manager`

### High-Risk (Extra Caution)
- `aws-architect` — infrastructure changes
- `security-engineer` — IAM/KMS changes
- `ml-engineer` — model deployment
- `disaster-recovery-agent` — DR configuration

## Tips

1. **Start with read-only agents** for analysis and recommendations
2. **Use testing-engineer** after any code changes
3. **Always run compliance-monitor** for production changes
4. **Combine agents** for complex tasks (e.g., backend + testing + compliance)
5. **Check documentation** in `.kiro/agents/README.md` for detailed capabilities

## Common Patterns

### Development Cycle
```
go-backend-engineer → testing-engineer → compliance-monitor → devops-engineer
```

### Security Review
```
security-engineer → compliance-monitor → kubernetes-engineer
```

### Performance Optimization
```
database-manager → kubernetes-engineer → finops-agent → devops-engineer
```

### Documentation Update
```
documentation-engineer (standalone)
```

## References

- **Agent Directory**: `.kiro/agents/README.md`
- **Coordination Guide**: `.kiro/steering/agents.md`
- **Workflow Reference**: `.kiro/workflows/README.md`
- **Configuration Summary**: `.kiro/AGENT-CONFIGURATION.md`

## Troubleshooting

**Agent not found?**
```bash
# List all agents
ls -1 .kiro/agents/*.json

# Regenerate if needed
python3 scripts/generate-kiro-agents.py
```

**Need to add a new agent?**
1. Create `.ai/agents/roles/{category}/{agent-name}.agent.md`
2. Add to `scripts/generate-kiro-agents.py` in `AGENT_FILES` dict
3. Run `python3 scripts/generate-kiro-agents.py`
4. Update `.kiro/agents/README.md`

**Agent not following instructions?**
Check that the agent's prompt references the correct `.ai/agents/` file:
```bash
cat .kiro/agents/{agent-name}.json | grep prompt
```
