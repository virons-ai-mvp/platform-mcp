# Production Deployment Guide

## Prerequisites

- Kubernetes cluster (v1.24+)
- kubectl configured
- Helm 3.x
- Docker (for building images)
- Container registry access (for production)

## Build & Push Image

### Local Development (Kind)
```bash
cd /path/to/platform-mcp
docker build -f src/virons-infrastructure-mcp-server/Dockerfile \
  -t virons-infrastructure-mcp-server:0.1.0 .
kind load docker-image virons-infrastructure-mcp-server:0.1.0 --name virons-local
```

### Production (ECR/GCR/ACR)
```bash
# Tag for registry
docker tag virons-infrastructure-mcp-server:0.1.0 \
  <registry>/virons-infrastructure-mcp-server:0.1.0

# Push to registry
docker push <registry>/virons-infrastructure-mcp-server:0.1.0
```

## Deploy with Helm

### Install
```bash
cd src/virons-infrastructure-mcp-server
helm install virons-infrastructure \
  helm/virons-infrastructure \
  --set image.repository=<registry>/virons-infrastructure-mcp-server \
  --set image.tag=0.1.0 \
  --set image.pullPolicy=IfNotPresent
```

### Upgrade
```bash
helm upgrade virons-infrastructure \
  helm/virons-infrastructure \
  --set image.tag=0.1.1
```

### Uninstall
```bash
helm uninstall virons-infrastructure
```

## Configuration

### Environment Variables
Set in `helm/virons-infrastructure/values.yaml`:

```yaml
env:
  - name: FASTMCP_LOG_LEVEL
    value: "INFO"
  - name: AUDIT_ENABLED
    value: "true"
```

### Resource Limits
```yaml
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

### Replicas
```yaml
replicaCount: 2  # For HA
```

## Health Checks

The service exposes three endpoints:

- **Liveness**: `GET /health/live` - Pod is alive
- **Readiness**: `GET /health/ready` - Pod can serve traffic
- **Metrics**: `GET /metrics` - Prometheus metrics

### Test Health
```bash
kubectl port-forward svc/virons-infrastructure 8080:8080
curl http://localhost:8080/health/live
curl http://localhost:8080/health/ready
```

## Monitoring

### Prometheus Integration

Add ServiceMonitor (if using Prometheus Operator):
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: virons-infrastructure
spec:
  selector:
    matchLabels:
      app: virons-infrastructure
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Key Metrics
- `mcp_tool_calls_total` - Total tool invocations
- `mcp_tool_duration_seconds` - Tool execution time
- `mcp_errors_total` - Error count
- `mcp_upstream_healthy` - Upstream server status

## Troubleshooting

### Pod CrashLoopBackOff
```bash
# Check logs
kubectl logs -l app=virons-infrastructure --tail=50

# Check events
kubectl describe pod -l app=virons-infrastructure

# Common issues:
# - Missing virons.common dependency → Rebuild image
# - Missing prometheus_client → Check pyproject.toml
# - Health check failing → Check /health/ready endpoint
```

### Image Pull Errors
```bash
# Verify image exists
docker images | grep virons-infrastructure

# For Kind cluster
kind load docker-image virons-infrastructure-mcp-server:0.1.0

# For production, check registry credentials
kubectl get secret <registry-secret> -o yaml
```

### Health Check Failures
```bash
# Test directly in pod
kubectl exec -it <pod-name> -- curl localhost:8080/health/live

# Check if port is listening
kubectl exec -it <pod-name> -- netstat -tlnp | grep 8080
```

## Security

### Non-Root User
Container runs as user `virons` (UID 1000):
```dockerfile
USER virons
```

### Network Policies
Restrict ingress/egress:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: virons-infrastructure
spec:
  podSelector:
    matchLabels:
      app: virons-infrastructure
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector: {}
    ports:
    - protocol: TCP
      port: 8080
```

### Secrets Management
For audit trails and upstream credentials:
```bash
kubectl create secret generic virons-infrastructure-secrets \
  --from-literal=audit-key=<key> \
  --from-literal=upstream-token=<token>
```

## Compliance (BaFin)

### Audit Trails
- All write operations logged with correlation IDs
- Audit events stored in compliance format
- Retention: 10 years (configurable)

### Enable Audit
```bash
helm upgrade virons-infrastructure helm/virons-infrastructure \
  --set audit.enabled=true \
  --set audit.retention=10y
```

### Forensic Requirements
Per virons-services forensic namespace:
1. ✅ `calculation_audit` before `forensic_flags`
2. ✅ ML gate: `gated_ml = ml_score if len(deterministic_flags) >= 1 else 0.0`
3. ✅ Nonlinear fusion: `S' = 1 - prod(1 - s_i)`
4. ✅ `write_audit()` on every write path

## Scaling

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: virons-infrastructure
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: virons-infrastructure
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Backup & Recovery

### Helm Release Backup
```bash
helm get values virons-infrastructure > backup-values.yaml
helm get manifest virons-infrastructure > backup-manifest.yaml
```

### Restore
```bash
helm install virons-infrastructure helm/virons-infrastructure \
  -f backup-values.yaml
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: |
          docker build -f src/virons-infrastructure-mcp-server/Dockerfile \
            -t ${{ secrets.REGISTRY }}/virons-infrastructure-mcp-server:${{ github.sha }} .
      - name: Push
        run: docker push ${{ secrets.REGISTRY }}/virons-infrastructure-mcp-server:${{ github.sha }}
      - name: Deploy
        run: |
          helm upgrade virons-infrastructure helm/virons-infrastructure \
            --set image.tag=${{ github.sha }}
```

## Production Checklist

- [ ] Image pushed to production registry
- [ ] Resource limits configured
- [ ] Health checks passing
- [ ] Metrics endpoint accessible
- [ ] Audit trails enabled
- [ ] Network policies applied
- [ ] Secrets configured
- [ ] HPA configured (if needed)
- [ ] Monitoring alerts set up
- [ ] Backup strategy in place
- [ ] Runbook documented
- [ ] On-call rotation defined

## Support

For issues or questions:
- Check logs: `kubectl logs -l app=virons-infrastructure -f`
- Check metrics: `kubectl port-forward svc/virons-infrastructure 8080:8080`
- Review events: `kubectl get events --sort-by='.lastTimestamp'`
