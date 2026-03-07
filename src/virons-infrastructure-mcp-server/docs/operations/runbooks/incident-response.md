# Incident Response Runbook

**Version**: 1.0
**Last Updated**: 2026-03-07
**Owner**: Operations Team

## Purpose

Procedures for responding to incidents affecting the Virons Infrastructure MCP Server.

## Severity Levels

| Level | Impact | Response Time | Escalation |
|-------|--------|---------------|------------|
| **P0 - Critical** | Service down, data loss | <15 min | Immediate |
| **P1 - High** | Degraded performance | <1 hour | Within 30 min |
| **P2 - Medium** | Minor issues | <4 hours | Within 2 hours |
| **P3 - Low** | Cosmetic, no impact | <24 hours | Next business day |

## Incident Response Team

### On-Call Rotation
- **Primary**: Platform Engineer
- **Secondary**: Senior Platform Engineer
- **Escalation**: Platform Lead
- **Compliance**: Compliance Officer (for audit/security incidents)

### Contact
- **PagerDuty**: https://virons-ai.pagerduty.com
- **Slack**: #incidents
- **Email**: incidents@virons.ai

## P0 - Critical Incidents

### Service Down

**Symptoms**:
- Health checks failing
- 5xx errors >50%
- No response from API

**Immediate Actions**:
```bash
# 1. Check pod status
kubectl get pods -l app=virons-infrastructure

# 2. Check logs
kubectl logs -l app=virons-infrastructure --tail=100

# 3. Check events
kubectl get events --sort-by='.lastTimestamp' | grep virons-infrastructure

# 4. Check resource usage
kubectl top pods -l app=virons-infrastructure
```

**Resolution Steps**:
1. **Restart pods** if OOMKilled or CrashLoopBackOff
   ```bash
   kubectl rollout restart deployment/virons-infrastructure
   ```

2. **Scale up** if resource constrained
   ```bash
   kubectl scale deployment/virons-infrastructure --replicas=5
   ```

3. **Rollback** if recent deployment
   ```bash
   helm rollback virons-infrastructure
   ```

4. **Check upstream** MCP servers
   ```bash
   # Test connectivity
   kubectl exec -it <pod> -- curl http://cdk-server:9140/health
   ```

**Communication**:
- Post in #incidents immediately
- Update status page
- Notify stakeholders every 15 minutes

### Data Loss

**Symptoms**:
- Audit logs missing
- Inconsistent data
- Backup failures

**Immediate Actions**:
```bash
# 1. Stop writes
kubectl scale deployment/virons-infrastructure --replicas=0

# 2. Check backup status
aws s3 ls s3://virons-audit-logs/ --recursive | tail -20

# 3. Verify database
psql -h <rds-endpoint> -U admin -d virons -c "SELECT COUNT(*) FROM audit_logs;"

# 4. Check replication lag
aws rds describe-db-instances --db-instance-identifier virons-audit
```

**Resolution Steps**:
1. **Identify scope** of data loss
2. **Restore from backup** if needed
3. **Verify data integrity**
4. **Resume operations** only after verification
5. **Document incident** for compliance

**Escalation**:
- Notify compliance team immediately
- Document all actions
- Prepare incident report

## P1 - High Priority

### Degraded Performance

**Symptoms**:
- Response time >5s (p95)
- Error rate >5%
- High CPU/memory usage

**Diagnostic Commands**:
```bash
# Check metrics
kubectl port-forward svc/virons-infrastructure 8080:8080
curl http://localhost:8080/metrics | grep mcp_tool_duration

# Check resource usage
kubectl top pods -l app=virons-infrastructure

# Check HPA status
kubectl get hpa virons-infrastructure

# Check logs for errors
kubectl logs -l app=virons-infrastructure | grep ERROR
```

**Resolution Steps**:
1. **Scale horizontally**
   ```bash
   kubectl scale deployment/virons-infrastructure --replicas=10
   ```

2. **Identify slow operations**
   ```bash
   kubectl logs -l app=virons-infrastructure | grep "duration_ms" | sort -k5 -n | tail -20
   ```

3. **Check upstream latency**
   ```bash
   # Monitor upstream response times
   kubectl logs -l app=virons-infrastructure | grep "upstream_duration"
   ```

4. **Optimize if needed**
   - Add caching
   - Increase timeouts
   - Optimize queries

### Security Incident

**Symptoms**:
- Unauthorized access attempts
- Suspicious API calls
- Compliance violations

**Immediate Actions**:
```bash
# 1. Review access logs
kubectl logs -l app=virons-infrastructure | grep "AUDIT_"

# 2. Check for anomalies
kubectl logs -l app=virons-infrastructure | grep "401\|403"

# 3. Review recent changes
kubectl rollout history deployment/virons-infrastructure
```

**Resolution Steps**:
1. **Isolate affected systems**
2. **Rotate credentials**
3. **Review access logs**
4. **Notify security team**
5. **Document incident**

**Escalation**:
- Notify security@virons.ai immediately
- Preserve evidence
- Follow security incident response plan

## P2 - Medium Priority

### Upstream Server Issues

**Symptoms**:
- Specific tool failing (CDK, CFN, etc.)
- Timeout errors
- Connection refused

**Diagnostic Commands**:
```bash
# Check upstream health
kubectl exec -it <pod> -- curl http://cdk-server:9140/health
kubectl exec -it <pod> -- curl http://cfn-server:9141/health
kubectl exec -it <pod> -- curl http://terraform-server:9142/health

# Check network policies
kubectl get networkpolicies

# Check service endpoints
kubectl get endpoints
```

**Resolution Steps**:
1. **Verify upstream status**
2. **Check network connectivity**
3. **Review upstream logs**
4. **Coordinate with upstream team**
5. **Implement fallback if available**

## P3 - Low Priority

### Documentation Issues

**Symptoms**:
- Swagger UI not loading
- Incorrect API docs
- Missing examples

**Resolution Steps**:
1. Check OpenAPI schema generation
2. Verify FastAPI configuration
3. Update documentation
4. Deploy fix

## Post-Incident

### Incident Report Template

```markdown
# Incident Report: [Title]

**Date**: YYYY-MM-DD
**Severity**: P0/P1/P2/P3
**Duration**: X hours Y minutes
**Impact**: [Description]

## Timeline
- HH:MM - Incident detected
- HH:MM - Team notified
- HH:MM - Root cause identified
- HH:MM - Fix deployed
- HH:MM - Incident resolved

## Root Cause
[Detailed explanation]

## Resolution
[What was done to fix it]

## Prevention
[How to prevent in future]

## Action Items
- [ ] Item 1 (Owner: Name, Due: Date)
- [ ] Item 2 (Owner: Name, Due: Date)
```

### Post-Mortem Meeting

**Within 48 hours** of P0/P1 incidents:
1. Review timeline
2. Identify root cause
3. Discuss prevention
4. Assign action items
5. Update runbooks

### Compliance Reporting

For incidents affecting audit logs or compliance:
1. Notify compliance team within 1 hour
2. Document all actions
3. Prepare compliance report
4. Submit to regulators if required (within 72 hours)

## Monitoring and Alerts

### Critical Alerts
- Service down (health check failing)
- Error rate >10%
- Response time >10s (p95)
- Audit log write failures

### Warning Alerts
- Error rate >5%
- Response time >5s (p95)
- CPU >80%
- Memory >80%

### Info Alerts
- Deployment started
- Deployment completed
- Configuration changed

## Tools and Access

### Required Access
- Kubernetes cluster (kubectl)
- AWS Console (RDS, S3, CloudWatch)
- PagerDuty
- Slack #incidents channel
- Grafana dashboards

### Useful Commands
```bash
# Quick health check
./scripts/operations/verify-deployment.sh

# View logs
kubectl logs -l app=virons-infrastructure -f

# Check metrics
kubectl port-forward svc/virons-infrastructure 8080:8080
curl http://localhost:8080/metrics

# Restart service
kubectl rollout restart deployment/virons-infrastructure

# Scale service
kubectl scale deployment/virons-infrastructure --replicas=5

# Rollback deployment
helm rollback virons-infrastructure
```

## References

- [Deployment Guide](../deployment-guide.md)
- [Architecture Documentation](../../architecture/)
- [Compliance Policies](../../compliance/policies/)
- [PagerDuty Runbook](https://virons-ai.pagerduty.com/runbooks)

## Contact

- **On-Call**: PagerDuty
- **Escalation**: platform-lead@virons.ai
- **Security**: security@virons.ai
- **Compliance**: compliance@virons.ai

---

**Maintained by**: Operations Team
**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
