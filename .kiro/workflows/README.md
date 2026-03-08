# Workflow Quick Reference

Quick reference for common workflows in virons-services. Full workflow definitions in `.ai/agents/workflows/`.

## Available Workflows

### Security Workflows
**File**: `.ai/agents/workflows/security-workflows.md`

- Incident response (P0-P4 severity)
- Security incidents and breaches
- DDoS attacks and mitigation
- Vulnerability management (CVE assessment, patching)
- Penetration testing
- Compliance audits (GDPR, PCI-DSS, SOC2)
- AML/KYC verification
- Fraud detection tuning
- Secrets rotation
- SSL certificate renewal
- Alert configuration and investigation
- Incident postmortems
- SLO/SLI definition

**Primary Agents**: `security-engineer`, `compliance-monitor`, `devops-engineer`

### Database Workflows
**File**: `.ai/agents/workflows/database-workflows.md`

- Database migrations
- Performance tuning
- Backup and restore
- Replication setup
- Query optimization
- Index management

**Primary Agents**: `database-manager`, `devops-engineer`

### Pre-Execution Checklist
**File**: `.ai/agents/workflows/pre-execution-checklist.md`

Mandatory checks before executing any task:
- TDD requirements
- Compliance validation
- Security checks
- Test coverage
- Documentation updates

**Primary Agents**: All agents must follow this checklist

## Workflow Invocation

### Direct Reference
```
User: "Follow security incident response workflow for P1 incident"
→ Load .ai/agents/workflows/security-workflows.md
→ security-engineer + compliance-monitor
```

### Implicit Workflow
```
User: "Optimize database queries for risk-scorer"
→ Detect database optimization task
→ Load .ai/agents/workflows/database-workflows.md
→ database-manager
```

## Common Workflow Patterns

### New Service Development
1. **Pre-execution**: Check TDD requirements, compliance scope
2. **Scaffold**: Backend engineer (Go/Python)
3. **Test**: Testing engineer (unit + integration)
4. **Document**: Documentation engineer
5. **Validate**: Compliance monitor
6. **Deploy**: DevOps engineer

### Security Incident
1. **Assess**: Security engineer (severity, scope)
2. **Contain**: DevOps engineer (isolate, mitigate)
3. **Investigate**: Security engineer (root cause)
4. **Remediate**: Appropriate engineer (fix)
5. **Document**: Documentation engineer (postmortem)
6. **Validate**: Compliance monitor (regulatory reporting)

### Database Migration
1. **Plan**: Database manager (migration strategy)
2. **Test**: Testing engineer (migration tests)
3. **Backup**: DevOps engineer (pre-migration backup)
4. **Execute**: Database manager (run migration)
5. **Verify**: Testing engineer (post-migration tests)
6. **Monitor**: DevOps engineer (performance monitoring)

### Performance Optimization
1. **Profile**: DevOps engineer (identify bottlenecks)
2. **Database**: Database manager (query optimization)
3. **Resources**: Kubernetes engineer (HPA, limits)
4. **Cost**: FinOps agent (cost analysis)
5. **Test**: Testing engineer (load tests)
6. **Monitor**: DevOps engineer (metrics, alerts)

## Workflow Extensions

To add new workflows:
1. Create `.ai/agents/workflows/{workflow-name}.md`
2. Define workflow steps, agents, and decision points
3. Update this reference document
4. Add to agent coordination guide if needed

## References

- **Workflow Directory**: `.ai/agents/workflows/`
- **Agent Coordination**: `.kiro/steering/agents.md`
- **Agent Directory**: `.kiro/agents/README.md`
- **Safety Protocol**: `.ai/agents/orchestration/safety-protocol.md`
