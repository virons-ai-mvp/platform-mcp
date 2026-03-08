# Agent Guardrails System

**Purpose**: Comprehensive safety controls for AI agents working with infrastructure
**Last Updated**: 2026-02-25

## Overview

This guardrails system provides multi-layered protection against unintended infrastructure changes, cost overruns, and compliance violations.

## Core Files

### 1. agent-restrictions.md
**What it does**: Defines what agents can and cannot do
- NEVER execute list (requires approval)
- Read-only operations (always safe)
- Auto-reject scenarios (never allowed)
- Environment-specific rules

**Key Rules**:
- No `terraform apply` without approval
- No production changes without full review
- No hardcoded credentials
- No resources outside eu-central-1

### 2. cost-guards.md
**What it does**: Prevents budget overruns
- High-cost resource approval requirements
- Auto-reject expensive operations
- Cost estimation requirements
- Budget monitoring and alerts

**Key Limits**:
- Dev: $400/month
- Staging: $900/month
- Demo: $1,200/month
- Production: $2,500/month

### 3. orchestration/safety-protocol.md
**What it does**: Risk assessment and approval workflow
- 4-level risk framework (LOW/MEDIUM/HIGH/CRITICAL)
- Human-in-the-loop approval gates
- Rollback procedures
- Audit logging requirements

**Risk Levels**:
- LOW: Execute immediately
- MEDIUM: Request approval
- HIGH: Full review required
- CRITICAL: Block or escalate

### 4. workflows/pre-execution-checklist.md
**What it does**: Pre-deployment validation checklist
- Testing requirements
- Security scan requirements
- Compliance verification
- Cost impact assessment
- Terraform validation steps

**Must Pass Before Apply**:
- Tests pass
- Security scan clean
- Budget approved
- Human approval obtained

### 5. orchestration/agent-coordinator.md (Updated)
**What it does**: Orchestrates agent interactions with safety integration
- Routes requests to appropriate agents
- Applies safety protocol to all operations
- Enforces guardrails across all agents

## How It Works

```
User Request
    ↓
Agent Coordinator
    ↓
Safety Protocol (Parse & Assess Risk)
    ↓
Check Restrictions & Cost Guards
    ↓
    ├─ LOW RISK → Execute
    ├─ MEDIUM RISK → Request Approval → Execute
    ├─ HIGH RISK → Full Review → Execute
    └─ CRITICAL → Block or Escalate
    ↓
Pre-Execution Checklist
    ↓
Execute (if approved)
    ↓
Post-Execution Validation
    ↓
Audit Log
```

## Quick Reference

### For Agents

**Before ANY operation**:
1. Check agent-restrictions.md for permissions
2. Assess cost impact using cost-guards.md
3. Follow safety-protocol.md risk assessment
4. Complete pre-execution-checklist.md if applying changes

**Always Safe**:
- `terraform plan`
- `terraform validate`
- `make test-module`
- AWS describe/list commands
- File reading

**Always Requires Approval**:
- `terraform apply`
- `terraform destroy`
- Enabling stopped resources
- Production changes
- Security modifications

**Always Blocked**:
- Hardcoded credentials
- Disabling encryption
- Resources outside eu-central-1
- Missing required tags
- Skipping tests

### For Humans

**When to approve**:
- Agent shows complete plan
- Tests pass
- Security scan clean
- Cost within budget
- Rollback plan documented

**When to reject**:
- Incomplete information
- Tests failing
- Security concerns
- Cost too high
- No rollback plan

## Integration with Existing Workflows

### TDD Workflow (repository-guidelines.md)
1. Write test first ✅
2. **Run pre-execution checklist** ← NEW
3. Implement minimal code
4. **Check agent-restrictions** ← NEW
5. Run tests
6. **Assess cost impact** ← NEW
7. Refactor if needed
8. **Get approval if needed** ← NEW
9. Commit

### Deployment Workflow
1. Develop in feature branch
2. Run tests locally
3. **Agent checks restrictions** ← NEW
4. Create PR
5. **Agent assesses risk** ← NEW
6. CI/CD runs tests
7. **Pre-execution checklist** ← NEW
8. **Human approval** ← NEW
9. Merge to main
10. Deploy with monitoring

## Monitoring & Enforcement

### Automatic Enforcement
- Budget alerts at 50%, 80%, 100%, 120%
- Auto-stop non-essential resources at 100%
- Rollback on failed health checks
- Compliance violation detection

### Manual Review
- Weekly: Review blocked operations
- Monthly: Assess risk accuracy
- Quarterly: Comprehensive safety audit

## Emergency Procedures

### Production Incident
1. Assess severity
2. Implement mitigation
3. Notify stakeholders
4. Execute fix or rollback
5. Verify resolution
6. Post-mortem

### Cost Overrun
1. Identify source
2. Stop non-essential resources
3. Notify finance
4. Implement controls
5. Update budgets if justified

### Security Incident
1. Isolate affected resources
2. Notify security team
3. Preserve evidence
4. Implement containment
5. Remediate vulnerability

## Customization

To adjust guardrails for your needs:

1. **Tighten restrictions**: Edit agent-restrictions.md
2. **Adjust budgets**: Update cost-guards.md thresholds
3. **Change risk levels**: Modify safety-protocol.md framework
4. **Add checks**: Extend pre-execution-checklist.md

## Testing Guardrails

```bash
# Test that agents respect restrictions
.ai/tools/test-guardrails.sh

# Simulate approval workflow
.ai/tools/simulate-approval.sh

# Verify cost guards
.ai/tools/test-cost-guards.sh
```

## Compliance Mapping

| Guardrail | BaFin MaRisk | GDPR | DORA |
|-----------|--------------|------|------|
| agent-restrictions.md | AT 8.1 | Art 32 | Art 11 |
| cost-guards.md | AT 7.2 | - | Art 11 |
| safety-protocol.md | AT 8.1 | Art 32 | Art 11 |
| pre-execution-checklist.md | AT 8.1 | Art 32 | Art 11 |

## Support

Questions or issues with guardrails:
1. Check this README
2. Review specific guardrail file
3. Consult safety-protocol.md decision tree
4. Escalate to engineering manager

## Version History

- 2026-02-25: Initial guardrails system created
  - agent-restrictions.md
  - cost-guards.md
  - safety-protocol.md
  - pre-execution-checklist.md
  - Updated agent-coordinator.md
