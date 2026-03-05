<link rel="stylesheet" href="../../../../platform-resources/styles/virons-markdown.css">

# Runbook: MCP Server Outage

**Service**: All MCP servers (9100-9139)  
**Severity**: 🟡 Medium  
**MTTR Target**: <15 minutes  
**Compliance**: DORA Art 11 (Resilience)

## Symptoms

***

- MCP server health check fails: `curl http://localhost:910X/health` returns 5xx
- Kiro CLI cannot connect to MCP server
- CloudWatch alarm: `mcp-server-unavailable`
- Kubernetes pod in `CrashLoopBackOff` or `Error` state

## Impact

***

- **Development**: Developers cannot use MCP tools (gitleaks, compliance-gate)
- **CI/CD**: Pre-commit hooks fail
- **Compliance**: Audit logging interrupted (BaFin AT 8.1)

## Diagnosis

***

### 1. Check Pod Status

```bash
# All MCP servers
kubectl get pods -n virons-mcp

# Specific server
kubectl get pod -n virons-mcp -l app=gitleaks

# Pod events
kubectl describe pod -n virons-mcp -l app=gitleaks
```

### 2. Check Logs

```bash
# Recent logs
kubectl logs -n virons-mcp -l app=gitleaks --tail=100

# Previous container (if crashed)
kubectl logs -n virons-mcp -l app=gitleaks --previous

# All containers in pod
kubectl logs -n virons-mcp -l app=gitleaks --all-containers
```

### 3. Check Resources

```bash
# Resource usage
kubectl top pod -n virons-mcp

# Resource limits
kubectl get pod -n virons-mcp -l app=gitleaks -o yaml | grep -A 5 resources
```

## Resolution

***

### Scenario 1: Pod CrashLoopBackOff

**Symptoms**: Pod restarts repeatedly

```bash
# 1. Check logs for error
kubectl logs -n virons-mcp -l app=gitleaks --previous

# 2. Common causes:
#    - Database connection failure
#    - Missing environment variables
#    - Port already in use

# 3. Fix database connection
kubectl get secret -n virons-mcp audit-db-credentials -o yaml

# 4. Restart pod
kubectl rollout restart deployment/gitleaks -n virons-mcp

# 5. Watch rollout
kubectl rollout status deployment/gitleaks -n virons-mcp
```

### Scenario 2: Out of Memory (OOMKilled)

**Symptoms**: Pod status shows `OOMKilled`

```bash
# 1. Check memory usage
kubectl top pod -n virons-mcp -l app=gitleaks

# 2. Increase memory limit
kubectl patch deployment gitleaks -n virons-mcp -p '
{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "gitleaks",
          "resources": {
            "limits": {"memory": "1Gi"},
            "requests": {"memory": "512Mi"}
          }
        }]
      }
    }
  }
}'

# 3. Verify
kubectl get deployment gitleaks -n virons-mcp -o yaml | grep -A 5 resources
```

### Scenario 3: Database Connection Failure

**Symptoms**: Logs show `connection refused` or `timeout`

```bash
# 1. Test database connectivity
kubectl exec -it -n virons-mcp deploy/gitleaks -- \
  psql $AUDIT_DB_URL -c "SELECT 1"

# 2. Check database status
aws rds describe-db-instances \
  --db-instance-identifier virons-audit-db \
  --region eu-central-1 | jq .DBInstances[0].DBInstanceStatus

# 3. Check security group
aws ec2 describe-security-groups \
  --group-ids sg-xxx \
  --region eu-central-1

# 4. Update network policy if needed
kubectl apply -f infrastructure/k8s/network-policy-audit-db.yaml
```

### Scenario 4: Image Pull Error

**Symptoms**: Pod status shows `ImagePullBackOff`

```bash
# 1. Check image
kubectl get deployment gitleaks -n virons-mcp -o yaml | grep image:

# 2. Verify image exists
aws ecr describe-images \
  --repository-name virons-mcp/gitleaks \
  --region eu-central-1

# 3. Check ECR credentials
kubectl get secret -n virons-mcp ecr-credentials

# 4. Recreate secret if needed
kubectl delete secret ecr-credentials -n virons-mcp
kubectl create secret docker-registry ecr-credentials \
  --docker-server=xxx.dkr.ecr.eu-central-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region eu-central-1) \
  -n virons-mcp
```

### Scenario 5: Port Conflict

**Symptoms**: Logs show `address already in use`

```bash
# 1. Check port allocation
kubectl get svc -n virons-mcp

# 2. Check for duplicate deployments
kubectl get deployment -n virons-mcp | grep gitleaks

# 3. Delete duplicate
kubectl delete deployment gitleaks-old -n virons-mcp

# 4. Verify port is free
kubectl exec -it -n virons-mcp deploy/gitleaks -- \
  netstat -tuln | grep 9100
```

## Verification

***

```bash
# 1. Check pod status
kubectl get pods -n virons-mcp -l app=gitleaks

# 2. Test health endpoint
kubectl port-forward -n virons-mcp svc/gitleaks 9100:9100 &
curl http://localhost:9100/health

# 3. Test functionality
curl -X POST http://localhost:9100/scan -d '{"repo": "."}'

# 4. Check audit logging
kubectl exec -it -n virons-mcp deploy/gitleaks -- \
  psql $AUDIT_DB_URL -c "
    SELECT COUNT(*) FROM audit_log
    WHERE server = 'gitleaks'
      AND timestamp > NOW() - INTERVAL '5 minutes';
  "
```

## Quick Recovery

***

```bash
# Nuclear option: delete and recreate
kubectl delete deployment gitleaks -n virons-mcp
helm upgrade --install virons-mcp charts/virons-mcp \
  --set servers.gitleaks.enabled=true \
  -n virons-mcp

# Wait for ready
kubectl wait --for=condition=ready pod \
  -l app=gitleaks \
  -n virons-mcp \
  --timeout=300s
```

## Prevention

***

- [ ] Set up liveness/readiness probes
- [ ] Configure resource limits (CPU/memory)
- [ ] Enable horizontal pod autoscaling
- [ ] Monitor database connection pool
- [ ] Test failover scenarios weekly

## Escalation

***

| Time | Action |
|------|--------|
| **0-5 min** | Platform on-call investigates |
| **5-15 min** | Escalate to platform lead |
| **15+ min** | Escalate to infrastructure team |

**PagerDuty**: https://virons-platform.pagerduty.com  
**Slack**: #platform-incidents

## References

***

- [Kubernetes Troubleshooting](https://kubernetes.io/docs/tasks/debug/)
- [MCP Server Architecture](../../architecture/README.md)
- [DORA Art 11 Compliance](../../compliance/dora/DORA-ART-11.md)

## Navigation
← [Runbooks Home](README.md)

***

**Last Updated**: 2026-03-05  
**Owner**: platform@virons.ai
