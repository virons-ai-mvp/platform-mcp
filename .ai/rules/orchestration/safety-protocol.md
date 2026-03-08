# Agent Safety Protocol

**Applies To**: All agents, all operations

## Risk Levels

**LOW** — Read-only
- File reading, code analysis, test execution
- `kubectl get/describe/logs`
- AWS describe/list commands

**MEDIUM** — Non-production changes
- `kubectl apply` in dev namespace
- Creating/modifying service code
- Updating K8s manifests (dev)

**HIGH** — Production-impacting
- `kubectl apply` in staging/production
- Database schema migrations
- IAM/KMS changes

**CRITICAL** — Destructive or compliance-sensitive
- `kubectl delete` any resource
- Disabling encryption or audit logging
- Bypassing BaFin/GDPR/EU AI Act controls

## Protocol Steps

### 1. Parse Request
- Operation type (read / create / modify / delete)
- Target namespace and environment
- Compliance implications

### 2. Risk Assessment
- Destructive potential
- Cost impact
- Compliance requirements
- Reversibility

### 3. Guardrail Check
- `agent-restrictions.md` — permissions
- `cost-guards.md` — budget
- Compliance rules

Output: ALLOW / REQUIRE_APPROVAL / BLOCK

### 4. Human Gate (if REQUIRE_APPROVAL)

```
🟡 APPROVAL REQUIRED

Operation: {description}
Namespace: {namespace}
Risk Level: {level}

Changes: {list}
Cost Impact: ~${estimate}/month
Rollback Plan: {steps}

Tests: ✅ / ❌
Security Scan: ✅ / ❌
Compliance: ✅ / ❌

Proceed? (yes/no)
```

### 5. Execute with Safeguards
- Enable detailed logging
- Execute operation
- Monitor for errors
- Validate success
- Update audit log

### 6. Post-Execution Validation
- Verify resources created/modified
- Check health status
- Confirm compliance maintained

## Auto-Rollback Triggers

- `kubectl apply` fails
- Health checks fail after deployment
- Cost exceeds 150% of estimate
- Compliance violation detected

## Audit Log Entry

```json
{
  "timestamp": "ISO8601",
  "agent": "agent-name",
  "operation": "operation-type",
  "namespace": "virons-{namespace}",
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "approval_status": "AUTO|APPROVED|BLOCKED",
  "execution_result": "SUCCESS|FAILURE|ROLLBACK",
  "compliance_check": "PASSED|FAILED"
}
```
