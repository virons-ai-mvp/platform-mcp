<link rel="stylesheet" href="../../../platform-resources/styles/virons-markdown.css">

# DORA Art 11: ICT Risk Management

## Overview

***

**Regulation**: DORA (Digital Operational Resilience Act) Article 11  
**Requirement**: ICT risk management framework, secret rotation, resilience testing  
**Scope**: Operations Context (secrets-rotation), all MCP servers  
**Status**: ✅ Compliant

## Requirements

***

### Art 11: ICT Risk Management Framework

> "Financial entities shall have a sound, comprehensive and well-documented ICT risk management framework as part of their overall risk management system."

**Platform-MCP Implementation**:
- Automated secret rotation (<90 days)
- Resilience testing (chaos engineering)
- Incident response procedures
- Change control with audit trail

## Secret Rotation Policy

***

### Rotation Requirements

| Secret Type | Max Age | Auto-Rotate | Notification |
|-------------|---------|-------------|--------------|
| **API Keys** | 90 days | ✅ Yes | 7 days before |
| **Database Passwords** | 90 days | ✅ Yes | 7 days before |
| **Service Tokens** | 90 days | ✅ Yes | 7 days before |
| **SSH Keys** | 180 days | ⚠️ Manual | 14 days before |

### Implementation

```python
# secrets-rotation server (port 9104)
from virons_mcp.operations.secrets_rotation import RotationPolicy

policy = RotationPolicy(
    max_age_days=90,  # DORA Art 11 requirement
    notification_days=7,
    auto_rotate=True,
    audit_enabled=True  # BaFin AT 8.1
)

async def rotate_secret(secret_id: str):
    """Rotate secret with DORA compliance."""
    # Check age
    secret = await get_secret(secret_id)
    age = (datetime.now() - secret.created_at).days
    
    if age > policy.max_age_days:
        # Rotate
        new_secret = await generate_new_secret()
        await update_secret(secret_id, new_secret)
        
        # Audit log (BaFin AT 8.1)
        await write_audit(
            server="secrets-rotation",
            context="operations",
            action="rotate_secret",
            resource=secret_id,
            result="SUCCESS",
            details={"age_days": age, "reason": "DORA_COMPLIANCE"}
        )
        
        return new_secret
```

## Secrets Inventory

***

### Current Secrets

| Secret ID | Type | Last Rotation | Next Rotation | Status |
|-----------|------|---------------|---------------|--------|
| `virons/api-key` | API Key | 2026-02-15 | 2026-05-16 | ✅ Compliant |
| `virons/db-password` | DB Password | 2026-01-20 | 2026-04-20 | ✅ Compliant |
| `virons/github-token` | Service Token | 2026-03-01 | 2026-05-30 | ✅ Compliant |
| `virons/ssh-key` | SSH Key | 2025-12-01 | 2026-06-01 | ✅ Compliant |

### Rotation Schedule

```bash
# Check rotation status
curl http://localhost:9104/status

# Force rotation
curl -X POST http://localhost:9104/rotate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"secret_id": "virons/api-key"}'

# Get rotation history
curl http://localhost:9104/history?secret_id=virons/api-key
```

## Resilience Testing

***

### Chaos Engineering

```yaml
# chaos-mesh/dora-test.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: mcp-pod-failure
spec:
  action: pod-failure
  mode: one
  selector:
    namespaces:
      - virons-mcp
    labelSelectors:
      context: operations
  duration: "30s"
  scheduler:
    cron: "@weekly"  # Weekly resilience test
```

### Test Scenarios

| Scenario | Frequency | Expected Outcome | Last Test |
|----------|-----------|------------------|-----------|
| **Pod Failure** | Weekly | Auto-restart <30s | 2026-03-01 |
| **Network Partition** | Monthly | Graceful degradation | 2026-02-15 |
| **Database Failure** | Quarterly | Failover to replica | 2026-01-10 |
| **Secret Rotation Failure** | Monthly | Retry + alert | 2026-02-20 |

## Incident Response

***

### Runbooks

- [Secret Rotation Failure](../../operations/runbooks/SECRET-ROTATION-FAILURE.md)
- [MCP Server Outage](../../operations/runbooks/MCP-SERVER-OUTAGE.md)
- [Database Connection Loss](../../operations/runbooks/DATABASE-CONNECTION-LOSS.md)

### Escalation

```yaml
# PagerDuty escalation policy
escalation_policy:
  - level: 1
    delay: 5m
    targets:
      - platform-oncall
  - level: 2
    delay: 15m
    targets:
      - platform-lead
      - compliance-team
```

## Compliance Checklist

***

- [x] Secret rotation policy defined (<90 days)
- [x] Automated rotation implemented
- [x] Secrets inventory maintained
- [x] Rotation notifications configured (7 days)
- [x] Audit trail for all rotations (BaFin AT 8.1)
- [x] Resilience testing (weekly chaos engineering)
- [x] Incident response runbooks documented
- [x] Escalation policy configured

## Monitoring

***

### Metrics

```python
# CloudWatch metrics
metrics = {
    "SecretRotationSuccess": {
        "unit": "Count",
        "threshold": ">99%"
    },
    "SecretAge": {
        "unit": "Days",
        "threshold": "<90"
    },
    "RotationLatency": {
        "unit": "Seconds",
        "threshold": "<30"
    }
}
```

### Alarms

```yaml
# Secret age alarm
SecretAgeAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: mcp-secret-age-violation
    MetricName: SecretAge
    Threshold: 90
    ComparisonOperator: GreaterThanThreshold
    EvaluationPeriods: 1
    AlarmActions:
      - !Ref ComplianceTeamSNS
```

## Evidence

***

### Rotation Reports

```bash
# Generate monthly rotation report
python scripts/generate_rotation_report.py \
  --month 2026-03 \
  --output compliance/reports/2026-03-rotation-report.pdf
```

### Audit Queries

```sql
-- Secrets older than 90 days
SELECT resource, MAX(timestamp) as last_rotation,
       EXTRACT(DAY FROM NOW() - MAX(timestamp)) as age_days
FROM audit_log
WHERE server = 'secrets-rotation'
  AND action = 'rotate_secret'
  AND result = 'SUCCESS'
GROUP BY resource
HAVING EXTRACT(DAY FROM NOW() - MAX(timestamp)) > 90;

-- Rotation failures (last 30 days)
SELECT timestamp, resource, details
FROM audit_log
WHERE server = 'secrets-rotation'
  AND action = 'rotate_secret'
  AND result = 'FAILURE'
  AND timestamp > NOW() - INTERVAL '30 days'
ORDER BY timestamp DESC;
```

## References

***

- [DORA Art 11 (Official Text)](references/dora-art-11.pdf)
- [Secrets Rotation Server](../../../src/virons_mcp/operations/secrets_rotation/)
- [Chaos Engineering Tests](../../../infrastructure/chaos-mesh/)

## Navigation
← [Compliance Home](../README.md)

***

**Last Updated**: 2026-03-05  
**Compliance Owner**: compliance@virons.ai  
**Technical Owner**: platform@virons.ai
