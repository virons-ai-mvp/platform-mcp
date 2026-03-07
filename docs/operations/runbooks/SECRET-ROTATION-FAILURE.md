<link rel="stylesheet" href="../../../../platform-resources/styles/virons-markdown.css">

# Runbook: Secret Rotation Failure

**Service**: secrets-rotation (port 9104)
**Severity**: 🔴 High
**MTTR Target**: <30 minutes
**Compliance**: DORA Art 11

## Symptoms

***

- Secret age >90 days (DORA violation)
- CloudWatch alarm: `mcp-secret-age-violation`
- PagerDuty alert: "Secret Rotation Failure"
- Audit log shows `rotate_secret` with `result=FAILURE`

## Impact

***

- **Compliance Risk**: DORA Art 11 violation
- **Security Risk**: Stale credentials increase breach risk
- **Operational Risk**: Services may fail if secrets expire

## Diagnosis

***

### 1. Check Secret Age

```bash
# Query audit log
kubectl exec -it -n virons-mcp deploy/secrets-rotation -- \
  psql $AUDIT_DB_URL -c "
    SELECT resource, MAX(timestamp) as last_rotation,
           EXTRACT(DAY FROM NOW() - MAX(timestamp)) as age_days
    FROM audit_log
    WHERE server = 'secrets-rotation'
      AND action = 'rotate_secret'
      AND result = 'SUCCESS'
    GROUP BY resource
    HAVING EXTRACT(DAY FROM NOW() - MAX(timestamp)) > 90;
  "
```

### 2. Check Rotation Logs

```bash
# Recent failures
kubectl logs -n virons-mcp -l app=secrets-rotation --tail=100 | grep ERROR

# Specific secret
curl http://localhost:9104/history?secret_id=virons/api-key
```

### 3. Check AWS Secrets Manager

```bash
# Verify secret exists
aws secretsmanager describe-secret \
  --secret-id virons/api-key \
  --region eu-central-1

# Check rotation status
aws secretsmanager get-secret-value \
  --secret-id virons/api-key \
  --region eu-central-1 | jq .CreatedDate
```

## Resolution

***

### Scenario 1: AWS Secrets Manager Permission Error

**Symptoms**: `AccessDeniedException` in logs

```bash
# 1. Check IAM role
aws iam get-role --role-name virons-mcp-secrets-rotation

# 2. Attach missing policy
aws iam attach-role-policy \
  --role-name virons-mcp-secrets-rotation \
  --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite

# 3. Restart pod
kubectl rollout restart deployment/secrets-rotation -n virons-mcp

# 4. Verify
curl -X POST http://localhost:9104/rotate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"secret_id": "virons/api-key"}'
```

### Scenario 2: Network Connectivity Issue

**Symptoms**: `ConnectionTimeout` in logs

```bash
# 1. Check network policy
kubectl get networkpolicy -n virons-mcp

# 2. Test connectivity
kubectl exec -it -n virons-mcp deploy/secrets-rotation -- \
  curl -v https://secretsmanager.eu-central-1.amazonaws.com

# 3. Fix network policy if needed
kubectl apply -f infrastructure/k8s/network-policy-secrets.yaml

# 4. Retry rotation
curl -X POST http://localhost:9104/rotate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"secret_id": "virons/api-key"}'
```

### Scenario 3: Secret Locked by Another Process

**Symptoms**: `ResourceInUseException` in logs

```bash
# 1. Check rotation status
aws secretsmanager describe-secret \
  --secret-id virons/api-key \
  --region eu-central-1 | jq .RotationEnabled

# 2. Cancel in-progress rotation
aws secretsmanager cancel-rotate-secret \
  --secret-id virons/api-key \
  --region eu-central-1

# 3. Wait 5 minutes, then retry
sleep 300
curl -X POST http://localhost:9104/rotate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"secret_id": "virons/api-key"}'
```

### Scenario 4: Manual Rotation Required

**Symptoms**: All automated attempts fail

```bash
# 1. Generate new secret
NEW_SECRET=$(openssl rand -base64 32)

# 2. Update in AWS Secrets Manager
aws secretsmanager update-secret \
  --secret-id virons/api-key \
  --secret-string "$NEW_SECRET" \
  --region eu-central-1

# 3. Update consuming services
kubectl set env deployment/service-name \
  API_KEY="$NEW_SECRET" \
  -n virons-services

# 4. Record in audit log
curl -X POST http://localhost:9104/audit \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "action": "manual_rotation",
    "secret_id": "virons/api-key",
    "reason": "automated_rotation_failed"
  }'
```

## Verification

***

```bash
# 1. Check secret age
curl http://localhost:9104/status | jq '.secrets[] | select(.id=="virons/api-key")'

# 2. Verify audit log
kubectl exec -it -n virons-mcp deploy/secrets-rotation -- \
  psql $AUDIT_DB_URL -c "
    SELECT * FROM audit_log
    WHERE server = 'secrets-rotation'
      AND resource = 'virons/api-key'
    ORDER BY timestamp DESC LIMIT 5;
  "

# 3. Test consuming service
curl -H "Authorization: Bearer $NEW_SECRET" \
  https://api.virons.ai/health
```

## Prevention

***

- [ ] Enable CloudWatch alarms for secret age >80 days (early warning)
- [ ] Set up weekly rotation dry-run tests
- [ ] Document all secrets in inventory
- [ ] Review IAM policies quarterly
- [ ] Test network policies in staging

## Escalation

***

| Time | Action |
|------|--------|
| **0-15 min** | Platform on-call investigates |
| **15-30 min** | Escalate to platform lead |
| **30+ min** | Escalate to compliance team (DORA violation) |

**PagerDuty**: https://virons-platform.pagerduty.com
**Slack**: #platform-incidents

## Post-Incident

***

1. Update audit log with root cause
2. Create incident report (template: `templates/incident-report.md`)
3. Update runbook with lessons learned
4. Schedule post-mortem (if >1 hour MTTR)

## References

***

- [DORA Art 11 Compliance](../../compliance/dora/DORA-ART-11.md)
- [Secrets Rotation Server](../../../src/virons_mcp/operations/secrets_rotation/)
- [AWS Secrets Manager Docs](https://docs.aws.amazon.com/secretsmanager/)

## Navigation
← [Runbooks Home](README.md)

***

**Last Updated**: 2026-03-05
**Owner**: platform@virons.ai
**On-Call**: [PagerDuty](https://virons-platform.pagerduty.com)
