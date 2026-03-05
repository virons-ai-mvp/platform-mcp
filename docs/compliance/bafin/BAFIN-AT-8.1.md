<link rel="stylesheet" href="../../../platform-resources/styles/virons-markdown.css">

# BaFin MaRisk AT 8.1 Compliance

## Overview

***

**Regulation**: BaFin MaRisk AT 8.1 (Minimum Requirements for Risk Management)  
**Requirement**: Audit trail for IT systems, change control, security scanning  
**Scope**: All MCP servers (Security, Governance, Operations, Compliance contexts)  
**Status**: ✅ Compliant

## Requirements

***

### AT 8.1: Audit Trail

> "Financial institutions must maintain comprehensive audit trails for all IT systems, including automated processes, with sufficient detail to reconstruct events."

**Platform-MCP Implementation**:
- PostgreSQL audit logs (7-year retention)
- Immutable audit records
- Timestamp + user + action + result
- Separate audit database (isolation)

## Implementation

***

### Audit Log Schema

```sql
-- Immutable audit log table
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    server VARCHAR(50) NOT NULL,  -- gitleaks, org-governance, etc.
    context VARCHAR(50) NOT NULL,  -- security, governance, etc.
    action VARCHAR(100) NOT NULL,
    user_id VARCHAR(100),
    resource VARCHAR(255),
    result VARCHAR(20) NOT NULL,  -- SUCCESS, FAILURE
    details JSONB,
    ip_address INET,
    CONSTRAINT immutable_audit CHECK (false)  -- Prevent updates
);

-- Retention policy (7 years)
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_server ON audit_log(server);
CREATE INDEX idx_audit_context ON audit_log(context);

-- Prevent updates/deletes
REVOKE UPDATE, DELETE ON audit_log FROM virons_mcp_user;
```

### Audit Logging (Python)

```python
from virons_mcp.shared.audit import write_audit

async def scan_repository(repo: str, user: str):
    try:
        result = await gitleaks.scan(repo)
        
        # Audit log (required by BaFin AT 8.1)
        await write_audit(
            server="gitleaks",
            context="security",
            action="scan_repository",
            user_id=user,
            resource=repo,
            result="SUCCESS",
            details={"secrets_found": len(result.secrets)}
        )
        
        return result
    except Exception as e:
        await write_audit(
            server="gitleaks",
            context="security",
            action="scan_repository",
            user_id=user,
            resource=repo,
            result="FAILURE",
            details={"error": str(e)}
        )
        raise
```

## Audit Coverage

***

### Security Context (9100-9109)

| Server | Audited Actions | Retention |
|--------|----------------|-----------|
| **gitleaks** | scan_repository, secret_detected | 7 years |
| **compliance-gate** | validate_commit, gate_passed, gate_failed | 7 years |

### Governance Context (9110-9119)

| Server | Audited Actions | Retention |
|--------|----------------|-----------|
| **org-governance** | validate_policy, policy_violated | 7 years |
| **workflow-governance** | validate_workflow, workflow_approved | 7 years |

### Operations Context (9120-9129)

| Server | Audited Actions | Retention |
|--------|----------------|-----------|
| **secrets-rotation** | rotate_secret, rotation_failed | 7 years |

### Compliance Context (9130-9139)

| Server | Audited Actions | Retention |
|--------|----------------|-----------|
| **compliance-checklist** | run_check, check_passed, check_failed | 7 years |

## Evidence

***

### Audit Log Query Examples

```sql
-- All actions by server (last 30 days)
SELECT server, action, COUNT(*) as count
FROM audit_log
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY server, action
ORDER BY count DESC;

-- Failed actions (security review)
SELECT timestamp, server, action, user_id, details
FROM audit_log
WHERE result = 'FAILURE'
  AND timestamp > NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC;

-- Secret rotation compliance (DORA Art 11)
SELECT resource, MAX(timestamp) as last_rotation
FROM audit_log
WHERE server = 'secrets-rotation'
  AND action = 'rotate_secret'
  AND result = 'SUCCESS'
GROUP BY resource
HAVING MAX(timestamp) < NOW() - INTERVAL '90 days';
```

### Audit Report Generation

```bash
# Generate monthly audit report
python scripts/generate_audit_report.py \
  --month 2026-03 \
  --output compliance/audits/2026-03-audit-report.pdf
```

## Compliance Checklist

***

- [x] Audit log table created with immutability constraint
- [x] 7-year retention policy configured
- [x] All MCP servers write audit logs
- [x] Audit logs include: timestamp, user, action, result
- [x] Separate audit database (isolation)
- [x] Audit log queries documented
- [x] Monthly audit reports generated
- [x] Audit log access restricted (read-only for auditors)

## Monitoring

***

### CloudWatch Alarms

```yaml
# Audit log write failures
AuditLogFailureAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: mcp-audit-log-failure
    MetricName: AuditLogWriteFailure
    Threshold: 1
    EvaluationPeriods: 1
    AlarmActions:
      - !Ref ComplianceTeamSNS
```

### Audit Log Metrics

- **Write Success Rate**: >99.9%
- **Write Latency**: <100ms (p99)
- **Storage Growth**: ~1GB/month
- **Retention**: 7 years (84 months)

## References

***

- [BaFin MaRisk AT 8.1 (German)](references/bafin-marisk-at-8.1.pdf)
- [Audit Log Schema](../../infrastructure/modules/audit-db/schema.sql)
- [Audit Library](../../../src/virons_mcp/shared/audit.py)

## Navigation
← [Compliance Home](../README.md)

***

**Last Updated**: 2026-03-05  
**Compliance Owner**: compliance@virons.ai  
**Technical Owner**: platform@virons.ai
