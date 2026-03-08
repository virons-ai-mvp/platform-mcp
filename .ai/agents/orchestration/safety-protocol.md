# Agent Safety Protocol

**Purpose**: Risk assessment and human-in-the-loop controls
**Applies To**: All agents, all operations

## Risk Assessment Framework

### Risk Levels

**LOW** - Read-only operations
- File reading/analysis
- Terraform plan/validate
- AWS describe/list commands
- Documentation generation
- Test execution (no apply)

**MEDIUM** - Non-production changes
- Terraform apply in dev environment
- Creating test resources
- Updating documentation
- Modifying CI/CD pipelines
- Security group changes (dev)

**HIGH** - Production-impacting changes
- Terraform apply in staging/demo/production
- IAM policy modifications
- KMS key changes
- Database schema changes
- Network routing changes

**CRITICAL** - Destructive or compliance-sensitive
- Resource deletion
- Terraform destroy
- Disabling encryption
- Removing audit logging
- Compliance control changes

## Safety Protocol Steps

### 1. Parse Request
Extract:
- Operation type (read, create, modify, delete)
- Target environment (dev, staging, demo, production)
- Resources affected
- Estimated cost impact
- Compliance implications

### 2. Risk Assessment
Evaluate:
- Destructive potential
- Cost impact
- Security implications
- Compliance requirements
- Reversibility

### 3. Guardrail Check
Check against:
- .ai/rules/agent-restrictions.md
- .ai/rules/cost-guards.md
- Environment-specific policies
- Compliance requirements

Output: ALLOW, BLOCK, or REQUIRE_APPROVAL

### 4. Human Gate
If REQUIRE_APPROVAL:
  1. Present operation summary
  2. Show risk assessment
  3. Display cost estimate
  4. Provide rollback plan
  5. Request explicit approval
  6. Wait for confirmation

If BLOCK:
  1. Explain why blocked
  2. Suggest alternative approach
  3. Escalate if override needed

### 5. Execute with Safeguards
If approved:
  1. Create state backup
  2. Enable detailed logging
  3. Execute operation
  4. Monitor for errors
  5. Validate success
  6. Update audit log

If error:
  1. Stop execution
  2. Capture error details
  3. Initiate rollback
  4. Alert human
  5. Document incident

### 6. Post-Execution Validation
After execution:
  1. Verify resources created/modified
  2. Check health status
  3. Validate cost impact
  4. Confirm compliance maintained
  5. Update documentation
  6. Close audit trail

## Decision Tree

```
User Request
    ↓
Parse & Classify
    ↓
Risk Assessment
    ↓
    ├─ LOW → Execute → Validate → Done
    ├─ MEDIUM → Check Guardrails
    │              ↓
    │              ├─ ALLOW → Execute → Validate → Done
    │              └─ REQUIRE_APPROVAL → Human Gate → Execute → Validate → Done
    ├─ HIGH → Human Gate → Execute → Validate → Done
    └─ CRITICAL → BLOCK or Escalate
```

## Approval Templates

### Medium Risk Approval Request
```
🟡 APPROVAL REQUIRED: Medium Risk Operation

Operation: {operation_description}
Environment: {environment}
Risk Level: MEDIUM

Changes:
- {change_1}
- {change_2}

Cost Impact: ~${estimated_cost}/month
Rollback Plan: {rollback_steps}

Tests: ✅ Passed
Security Scan: ✅ Clean
Compliance: ✅ Verified

Proceed? (yes/no)
```

### High Risk Approval Request
```
🔴 APPROVAL REQUIRED: High Risk Operation

Operation: {operation_description}
Environment: {environment}
Risk Level: HIGH

⚠️  PRODUCTION IMPACT POSSIBLE

Changes:
- {change_1}
- {change_2}

Cost Impact: ~${estimated_cost}/month
Affected Resources: {resource_count}

Pre-Execution Checklist:
✅ Tests passed
✅ Security scan clean
✅ Compliance verified
✅ Rollback plan documented
✅ Monitoring configured

Proceed? (yes/no)
```

### Critical Operation Block
```
🛑 OPERATION BLOCKED: Critical Risk

Operation: {operation_description}
Risk Level: CRITICAL
Reason: {block_reason}

This operation is blocked by safety protocols:
- {violation_1}
- {violation_2}

Alternative Approaches:
1. {alternative_1}
2. {alternative_2}

To override, contact VP Engineering with:
- Business justification
- Risk mitigation plan
- Compliance approval
```

## Rollback Procedures

### Automatic Rollback Triggers
- Terraform apply fails
- Health checks fail after deployment
- Cost exceeds 150% of estimate
- Security scan fails post-deployment
- Compliance violation detected

### Rollback Steps
1. **Stop**: Halt any in-progress operations
2. **Assess**: Determine rollback scope
3. **Execute**: Apply previous Terraform state
4. **Verify**: Confirm rollback success
5. **Document**: Record incident details
6. **Review**: Post-mortem analysis

## Audit Logging

All operations must log:

```json
{
  "timestamp": "2026-02-25T08:30:00Z",
  "agent": "aws-architect",
  "operation": "terraform_apply",
  "environment": "dev",
  "risk_level": "MEDIUM",
  "approval_status": "APPROVED",
  "approver": "human_user",
  "resources_affected": ["aws_eks_cluster.main"],
  "cost_estimate": "$73/month",
  "execution_result": "SUCCESS",
  "rollback_available": true,
  "compliance_check": "PASSED"
}
```

## Escalation Matrix

| Risk Level | Approval Required | Escalation Path |
|------------|-------------------|-----------------|
| LOW | None | N/A |
| MEDIUM | User | Team Lead (if blocked) |
| HIGH | User + Review | Engineering Manager |
| CRITICAL | VP Engineering | CTO |
