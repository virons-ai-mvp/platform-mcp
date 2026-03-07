# Access Control Policy

**Version**: 1.0
**Effective Date**: 2026-03-07
**Review Date**: 2027-03-07
**Owner**: Security Team

## Purpose

Define access control requirements for the Virons Infrastructure MCP Server to comply with GDPR Art 32, BaFin, and DORA regulations.

## Scope

All users, systems, and services accessing the Virons Infrastructure MCP Server.

## Principles

### Least Privilege
- Users granted minimum necessary permissions
- Time-limited access for temporary needs
- Regular access reviews

### Separation of Duties
- No single user has complete control
- Critical operations require multiple approvals
- Audit trail for all access

### Defense in Depth
- Multiple layers of security
- Network segmentation
- Encryption at rest and in transit

## Access Levels

| Level | Permissions | Use Case |
|-------|-------------|----------|
| **Read-Only** | View stacks, health, metrics | Monitoring, auditing |
| **Operator** | Deploy, list stacks | Day-to-day operations |
| **Admin** | Deploy, destroy, configure | Infrastructure management |
| **Compliance** | View audit logs, export | Compliance auditing |
| **System** | All operations | Automated systems |

## Role-Based Access Control (RBAC)

### Roles

#### Viewer
```yaml
permissions:
  - list_stacks
  - view_health
  - view_metrics
users:
  - monitoring-team
  - auditors
```

#### Operator
```yaml
permissions:
  - list_stacks
  - deploy_infrastructure
  - view_health
  - view_metrics
users:
  - devops-team
  - platform-engineers
```

#### Administrator
```yaml
permissions:
  - list_stacks
  - deploy_infrastructure
  - destroy_infrastructure  # Requires confirmation
  - view_health
  - view_metrics
  - configure_server
users:
  - platform-admins
  - senior-engineers
```

#### Compliance Officer
```yaml
permissions:
  - view_audit_logs
  - export_audit_logs
  - view_compliance_reports
users:
  - compliance-team
  - external-auditors
```

## Authentication

### API Access
- **Method**: API keys or OAuth 2.0
- **Rotation**: Every 90 days
- **Storage**: Encrypted in secrets manager
- **Transmission**: HTTPS only

### MCP Protocol
- **Method**: mTLS certificates
- **Rotation**: Every 365 days
- **Validation**: Certificate pinning
- **Revocation**: CRL/OCSP

### Internal Services
- **Method**: Service accounts with IAM roles
- **Rotation**: Automatic (AWS STS)
- **Scope**: Minimal permissions
- **Audit**: CloudTrail logging

## Authorization

### API Endpoints

```python
# Require authentication
@app.post("/api/v1/deploy")
@require_auth
@require_role("operator", "admin")
async def deploy_infrastructure(request: DeployRequest):
    pass

# Require admin role
@app.post("/api/v1/destroy")
@require_auth
@require_role("admin")
@require_confirmation
async def destroy_infrastructure(request: DestroyRequest):
    pass

# Public endpoint
@app.get("/health/live")
async def liveness():
    pass
```

### Audit Log Access

```sql
-- Only compliance team can access audit logs
GRANT SELECT ON audit_logs TO compliance_role;
REVOKE INSERT, UPDATE, DELETE ON audit_logs FROM ALL;

-- System can only insert
GRANT INSERT ON audit_logs TO system_role;
```

## Network Access Control

### Ingress Rules
```yaml
# Allow from ingress controller only
- from:
  - namespaceSelector:
      matchLabels:
        name: ingress-nginx
  ports:
  - protocol: TCP
    port: 8080
```

### Egress Rules
```yaml
# Allow to upstream MCP servers only
- to:
  - namespaceSelector:
      matchLabels:
        name: mcp-servers
  ports:
  - protocol: TCP
    port: 9140-9143

# Allow to AWS services
- to:
  - podSelector:
      matchLabels:
        app: aws-services
```

## Encryption

### At Rest
- **Audit logs**: AES-256 (KMS)
- **Configuration**: Encrypted ConfigMaps
- **Secrets**: AWS Secrets Manager
- **Backups**: S3 with SSE-KMS

### In Transit
- **External**: TLS 1.3
- **Internal**: mTLS (service mesh)
- **Upstream**: TLS 1.2+

## Access Monitoring

### Real-time Alerts
- Failed authentication attempts (>3 in 5 min)
- Privilege escalation attempts
- Unauthorized access to audit logs
- Unusual access patterns

### Audit Logging
```json
{
  "event": "access_attempt",
  "timestamp": "2026-03-07T09:00:00Z",
  "user_id": "user@virons.ai",
  "source_ip": "10.0.1.5",
  "endpoint": "/api/v1/deploy",
  "method": "POST",
  "status": "success",
  "role": "operator"
}
```

## Access Reviews

### Monthly
- Review active users
- Check for unused accounts
- Verify role assignments

### Quarterly
- Full access audit
- Remove inactive users
- Update role definitions

### Annually
- Policy review
- Compliance verification
- Penetration testing

## Emergency Access

### Break-Glass Procedure
1. Document emergency justification
2. Use emergency credentials
3. Notify security team immediately
4. Complete incident report within 24h
5. Rotate emergency credentials

### Emergency Roles
- Limited to critical operations
- Automatically logged and alerted
- Require post-incident review
- Credentials rotated after use

## Compliance Requirements

### GDPR Art 32
- ✅ Access controls implemented
- ✅ Encryption at rest and in transit
- ✅ Regular access reviews
- ✅ Audit logging

### BaFin MaRisk
- ✅ Separation of duties
- ✅ Least privilege principle
- ✅ Audit trail for all access
- ✅ Regular reviews

### DORA Art 6
- ✅ ICT security framework
- ✅ Access management
- ✅ Incident response
- ✅ Regular testing

## Violations

### Reporting
- Report to: security@virons.ai
- Response time: <1 hour
- Investigation: <24 hours

### Consequences
- First violation: Warning + training
- Second violation: Access suspension
- Third violation: Access revocation
- Severe violation: Immediate revocation + investigation

## References

- GDPR Art 32 - Security of Processing
- BaFin MaRisk - Access Control Requirements
- DORA Art 6 - ICT Risk Management
- NIST 800-53 - Access Control
- Internal: Security Incident Response Plan

## Contact

- **Policy Owner**: security@virons.ai
- **Questions**: security@virons.ai
- **Incidents**: security@virons.ai
- **Emergency**: +49-xxx-xxx-xxxx

---

**Approved by**: Security Team
**Date**: 2026-03-07
**Next Review**: 2027-03-07
