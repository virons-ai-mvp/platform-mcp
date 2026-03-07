# Scaling Runbook

**Version**: 1.0
**Last Updated**: 2026-03-07
**Owner**: Operations Team

## Overview

Procedures for scaling the Virons Infrastructure MCP Server horizontally and vertically.

## Auto-Scaling (HPA)

### Current Configuration

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
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Check HPA Status

```bash
# View HPA status
kubectl get hpa virons-infrastructure

# Detailed HPA info
kubectl describe hpa virons-infrastructure

# Watch scaling events
kubectl get hpa virons-infrastructure -w
```

### Modify HPA

```bash
# Increase max replicas
kubectl patch hpa virons-infrastructure -p '{"spec":{"maxReplicas":20}}'

# Change CPU threshold
kubectl patch hpa virons-infrastructure -p '{"spec":{"metrics":[{"type":"Resource","resource":{"name":"cpu","target":{"type":"Utilization","averageUtilization":60}}}]}}'

# Update via Helm
helm upgrade virons-infrastructure ./helm/virons-infrastructure \
  --set autoscaling.maxReplicas=20 \
  --set autoscaling.targetCPUUtilizationPercentage=60
```

## Manual Scaling

### Horizontal Scaling

```bash
# Scale to specific replica count
kubectl scale deployment virons-infrastructure --replicas=5

# Verify scaling
kubectl get deployment virons-infrastructure
kubectl get pods -l app=virons-infrastructure

# Check pod distribution across nodes
kubectl get pods -l app=virons-infrastructure -o wide
```

### When to Scale Manually

**Scale Up**:
- Anticipated traffic spike (planned deployment)
- Performance degradation despite auto-scaling
- Testing capacity limits
- Before maintenance window

**Scale Down**:
- After traffic spike subsides
- Cost optimization during low-traffic periods
- Testing resilience with fewer replicas

### Scaling Limits

| Environment | Min | Max | Default |
|-------------|-----|-----|---------|
| Production | 3 | 20 | 5 |
| Staging | 2 | 10 | 3 |
| Development | 1 | 5 | 2 |

## Vertical Scaling

### Current Resources

```yaml
resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi
```

### Increase Resources

```bash
# Update via Helm
helm upgrade virons-infrastructure ./helm/virons-infrastructure \
  --set resources.requests.cpu=1000m \
  --set resources.requests.memory=1Gi \
  --set resources.limits.cpu=4000m \
  --set resources.limits.memory=4Gi

# Verify update
kubectl get deployment virons-infrastructure -o yaml | grep -A 10 resources
```

### Resource Sizing Guidelines

**CPU**:
- Light load: 500m request, 1000m limit
- Medium load: 1000m request, 2000m limit
- Heavy load: 2000m request, 4000m limit

**Memory**:
- Light load: 512Mi request, 1Gi limit
- Medium load: 1Gi request, 2Gi limit
- Heavy load: 2Gi request, 4Gi limit

## Scaling Scenarios

### Scenario 1: Traffic Spike

**Symptoms**:
- CPU >80%
- Response time >5s
- HPA at max replicas

**Actions**:
```bash
# 1. Increase max replicas
kubectl patch hpa virons-infrastructure -p '{"spec":{"maxReplicas":20}}'

# 2. Monitor scaling
kubectl get hpa virons-infrastructure -w

# 3. Check pod health
kubectl get pods -l app=virons-infrastructure

# 4. Verify performance
kubectl port-forward svc/virons-infrastructure 8080:8080
curl http://localhost:8080/metrics | grep mcp_tool_duration
```

### Scenario 2: Memory Pressure

**Symptoms**:
- OOMKilled pods
- Memory >90%
- Frequent restarts

**Actions**:
```bash
# 1. Check memory usage
kubectl top pods -l app=virons-infrastructure

# 2. Increase memory limits
helm upgrade virons-infrastructure ./helm/virons-infrastructure \
  --set resources.limits.memory=4Gi

# 3. Monitor pods
kubectl get pods -l app=virons-infrastructure -w

# 4. Check for memory leaks
kubectl logs -l app=virons-infrastructure | grep -i memory
```

### Scenario 3: Planned Maintenance

**Before Maintenance**:
```bash
# 1. Scale up for redundancy
kubectl scale deployment virons-infrastructure --replicas=6

# 2. Verify all pods healthy
kubectl get pods -l app=virons-infrastructure

# 3. Disable auto-scaling temporarily
kubectl patch hpa virons-infrastructure -p '{"spec":{"minReplicas":6,"maxReplicas":6}}'
```

**After Maintenance**:
```bash
# 1. Re-enable auto-scaling
kubectl patch hpa virons-infrastructure -p '{"spec":{"minReplicas":3,"maxReplicas":10}}'

# 2. Monitor scaling behavior
kubectl get hpa virons-infrastructure -w
```

### Scenario 4: Cost Optimization

**Off-Peak Hours**:
```bash
# Scale down during low traffic (e.g., nights, weekends)
kubectl patch hpa virons-infrastructure -p '{"spec":{"minReplicas":2}}'

# Monitor to ensure SLA maintained
kubectl get hpa virons-infrastructure
```

**Peak Hours**:
```bash
# Scale up before peak traffic
kubectl patch hpa virons-infrastructure -p '{"spec":{"minReplicas":5}}'
```

## Node Scaling

### Check Node Capacity

```bash
# View node resources
kubectl top nodes

# Check node allocatable resources
kubectl describe nodes | grep -A 5 "Allocated resources"

# View pod distribution
kubectl get pods -o wide --all-namespaces | grep virons-infrastructure
```

### Cluster Autoscaler

**AWS EKS**:
```bash
# Check cluster autoscaler status
kubectl get deployment cluster-autoscaler -n kube-system

# View autoscaler logs
kubectl logs -n kube-system deployment/cluster-autoscaler

# Check node groups
aws eks describe-nodegroup \
  --cluster-name virons-prod \
  --nodegroup-name virons-workers
```

### Add Nodes Manually

```bash
# AWS EKS - update desired capacity
aws eks update-nodegroup-config \
  --cluster-name virons-prod \
  --nodegroup-name virons-workers \
  --scaling-config minSize=3,maxSize=10,desiredSize=5

# Verify nodes
kubectl get nodes
```

## Monitoring Scaling

### Key Metrics

```bash
# CPU usage
kubectl top pods -l app=virons-infrastructure

# Memory usage
kubectl top pods -l app=virons-infrastructure

# Request rate
kubectl port-forward svc/virons-infrastructure 8080:8080
curl http://localhost:8080/metrics | grep mcp_tool_calls_total

# Response time
curl http://localhost:8080/metrics | grep mcp_tool_duration_seconds
```

### Grafana Dashboards

**Scaling Dashboard**:
- Current replicas vs desired
- CPU/memory utilization
- Request rate and latency
- Pod distribution across nodes

**Access**: https://grafana.virons.ai/d/scaling

### Alerts

**Scale-Up Alerts**:
- CPU >80% for 5 minutes
- Memory >85% for 5 minutes
- HPA at max replicas
- Response time >5s (p95)

**Scale-Down Alerts**:
- CPU <20% for 30 minutes
- Memory <30% for 30 minutes
- Over-provisioned (cost alert)

## Scaling Best Practices

### Do's

✅ **Use HPA for automatic scaling**
✅ **Set appropriate resource requests/limits**
✅ **Monitor scaling metrics continuously**
✅ **Test scaling before production**
✅ **Document scaling decisions**
✅ **Scale gradually (not all at once)**
✅ **Verify pod health after scaling**

### Don'ts

❌ **Don't scale below minimum replicas (3 in prod)**
❌ **Don't set limits too low (causes throttling)**
❌ **Don't ignore OOMKilled pods**
❌ **Don't scale without monitoring**
❌ **Don't forget to update HPA after manual scaling**
❌ **Don't scale during active incidents**

## Scaling Checklist

### Before Scaling

- [ ] Check current resource usage
- [ ] Review recent performance metrics
- [ ] Verify node capacity available
- [ ] Check for any ongoing incidents
- [ ] Notify team of planned scaling

### During Scaling

- [ ] Execute scaling command
- [ ] Monitor pod creation/termination
- [ ] Verify all pods reach Ready state
- [ ] Check service endpoints updated
- [ ] Monitor application metrics

### After Scaling

- [ ] Verify performance improved
- [ ] Check resource utilization
- [ ] Review logs for errors
- [ ] Update documentation if permanent
- [ ] Schedule review if temporary

## Rollback Procedure

```bash
# If scaling causes issues, rollback immediately

# 1. Scale back to previous replica count
kubectl scale deployment virons-infrastructure --replicas=3

# 2. Reset HPA if modified
kubectl patch hpa virons-infrastructure -p '{"spec":{"minReplicas":3,"maxReplicas":10}}'

# 3. Rollback Helm release if resource changes
helm rollback virons-infrastructure

# 4. Verify stability
kubectl get pods -l app=virons-infrastructure
kubectl get hpa virons-infrastructure
```

## Capacity Planning

### Current Capacity

| Metric | Per Pod | 3 Pods | 10 Pods |
|--------|---------|--------|---------|
| CPU | 500m | 1.5 cores | 5 cores |
| Memory | 512Mi | 1.5Gi | 5Gi |
| Requests/sec | ~100 | ~300 | ~1000 |

### Growth Planning

**Monthly Review**:
- Analyze traffic trends
- Review resource utilization
- Adjust HPA settings
- Update node group capacity

**Quarterly Review**:
- Capacity forecast (6 months)
- Cost optimization analysis
- Performance benchmarking
- Update scaling policies

## Troubleshooting

### Pods Not Scaling

```bash
# Check HPA status
kubectl describe hpa virons-infrastructure

# Check metrics server
kubectl get apiservice v1beta1.metrics.k8s.io

# Check resource quotas
kubectl describe resourcequota -n virons-infrastructure

# Check node capacity
kubectl describe nodes | grep -A 5 "Allocated resources"
```

### Pods Stuck in Pending

```bash
# Check pod events
kubectl describe pod <pod-name>

# Check node resources
kubectl top nodes

# Check for taints/tolerations
kubectl describe nodes | grep Taints
```

### Uneven Pod Distribution

```bash
# Check pod distribution
kubectl get pods -l app=virons-infrastructure -o wide

# Add pod anti-affinity
helm upgrade virons-infrastructure ./helm/virons-infrastructure \
  --set affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight=100
```

## Contact

- **On-Call**: PagerDuty
- **Platform Team**: platform@virons.ai
- **Escalation**: platform-lead@virons.ai

## References

- [Kubernetes HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Incident Response](./incident-response.md)
- [Architecture Documentation](../../architecture/)

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
