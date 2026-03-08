<link rel="stylesheet" href="../../../platform-resources/styles/virons-markdown.css">

# MCP Security Policies

## Overview

***

**Scope**: All MCP servers (Security, Governance, Operations, Compliance contexts)
**Compliance**: BaFin AT 8.1, GDPR Art 32, DORA Art 11
**Status**: ✅ Active

## Access Control

***

### IAM Roles

| Role | Permissions | Principals |
|------|-------------|------------|
| **virons-mcp-admin** | Full access to all MCP servers | Platform team |
| **virons-mcp-developer** | Read-only access, scan/validate | Developers |
| **virons-mcp-auditor** | Read-only audit logs | Compliance team |
| **virons-mcp-rotation** | Secret rotation only | secrets-rotation service |

### IAM Policy: Developer Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "mcp:Scan",
        "mcp:Validate",
        "mcp:GetHealth"
      ],
      "Resource": [
        "arn:aws:mcp:eu-central-1:*:server/gitleaks",
        "arn:aws:mcp:eu-central-1:*:server/compliance-gate"
      ]
    },
    {
      "Effect": "Deny",
      "Action": [
        "mcp:Rotate",
        "mcp:UpdatePolicy"
      ],
      "Resource": "*"
    }
  ]
}
```

## Network Security

***

### Network Policies

```yaml
# Security Context isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mcp-security-context
  namespace: virons-mcp
spec:
  podSelector:
    matchLabels:
      context: security
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: virons-services
    ports:
    - protocol: TCP
      port: 9100
    - protocol: TCP
      port: 9101
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: audit-db
    ports:
    - protocol: TCP
      port: 5432
```

### Security Groups (AWS)

```hcl
# MCP servers security group
resource "aws_security_group" "mcp_servers" {
  name        = "virons-mcp-servers"
  description = "Security group for MCP servers"
  vpc_id      = var.vpc_id

  # Allow traffic from EKS nodes
  ingress {
    from_port   = 9100
    to_port     = 9139
    protocol    = "tcp"
    cidr_blocks = [var.eks_cidr]
  }

  # Allow audit database
  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.audit_db_cidr]
  }

  # Allow AWS Secrets Manager
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name       = "virons-mcp-servers"
    Compliance = "BaFin-GDPR-DORA"
  }
}
```

## Encryption

***

### TLS Configuration

```yaml
# Helm values
security:
  tls:
    enabled: true
    version: "1.3"
    ciphers:
      - TLS_AES_256_GCM_SHA384
      - TLS_CHACHA20_POLY1305_SHA256
    cert:
      source: cert-manager
      issuer: letsencrypt-prod
```

### Secrets Encryption

```yaml
# AWS KMS key for secrets
kms:
  key_id: arn:aws:kms:eu-central-1:xxx:key/virons-mcp
  rotation: enabled
  policy:
    - sid: AllowMCPServers
      effect: Allow
      principals:
        - arn:aws:iam::xxx:role/virons-mcp-rotation
      actions:
        - kms:Decrypt
        - kms:Encrypt
        - kms:GenerateDataKey
```

## Authentication

***

### API Token Authentication

```python
# MCP server authentication
from virons_mcp.shared.auth import require_token

@app.post("/scan")
@require_token(roles=["developer", "admin"])
async def scan_repository(repo: str, token: str = Header(...)):
    """Scan repository (requires valid token)."""
    # Audit
    await write_audit(
        server="gitleaks",
        action="scan_repository",
        user_id=token.user_id,
        resource=repo,
        result="SUCCESS"
    )
    return await gitleaks.scan(repo)
```

### Token Rotation

- **Frequency**: 90 days (DORA Art 11)
- **Method**: Automated via secrets-rotation server
- **Notification**: 7 days before expiration

## Audit Requirements

***

### Mandatory Audit Events

| Event | Server | Retention |
|-------|--------|-----------|
| **scan_repository** | gitleaks | 7 years |
| **secret_detected** | gitleaks | 7 years |
| **validate_policy** | org-governance | 7 years |
| **rotate_secret** | secrets-rotation | 7 years |
| **compliance_check** | compliance-checklist | 7 years |

### Audit Log Access

```bash
# Auditors only (read-only)
kubectl create role audit-reader \
  --verb=get,list \
  --resource=pods/log \
  -n virons-mcp

kubectl create rolebinding audit-reader-binding \
  --role=audit-reader \
  --group=compliance-team \
  -n virons-mcp
```

## Vulnerability Management

***

### Container Scanning

```yaml
# Trivy scan in CI/CD
- name: Scan container image
  run: |
    trivy image \
      --severity HIGH,CRITICAL \
      --exit-code 1 \
      virons-mcp/gitleaks:latest
```

### Dependency Scanning

```bash
# Python dependencies
pip-audit --requirement requirements.txt

# Helm chart
helm lint charts/virons-mcp
```

## Incident Response

***

### Security Incidents

| Severity | Response Time | Escalation |
|----------|---------------|------------|
| **Critical** | <15 min | Security team + compliance |
| **High** | <1 hour | Security team |
| **Medium** | <4 hours | Platform team |
| **Low** | <24 hours | Platform team |

### Runbooks

- [Secret Rotation Failure](../operations/runbooks/SECRET-ROTATION-FAILURE.md)
- [MCP Server Outage](../operations/runbooks/MCP-SERVER-OUTAGE.md)
- [Unauthorized Access](../operations/runbooks/UNAUTHORIZED-ACCESS.md)

## Compliance Checklist

***

- [x] IAM roles with least privilege
- [x] Network policies per context
- [x] TLS 1.3 encryption
- [x] AWS KMS for secrets
- [x] API token authentication
- [x] Token rotation <90 days
- [x] Audit logging for all actions
- [x] Container vulnerability scanning
- [x] Incident response procedures

## Monitoring

***

```yaml
# Security alarms
SecurityAlarms:
  - name: unauthorized-access
    metric: UnauthorizedAccessAttempts
    threshold: 5
    period: 5m
    action: alert

  - name: failed-authentication
    metric: FailedAuthAttempts
    threshold: 10
    period: 5m
    action: block

  - name: secret-age-violation
    metric: SecretAge
    threshold: 90
    period: 1d
    action: alert
```

## References

***

- [BaFin AT 8.1 Compliance](../compliance/bafin/BAFIN-AT-8.1.md)
- [GDPR Art 32 Compliance](../compliance/gdpr/GDPR-ART-25-32.md)
- [DORA Art 11 Compliance](../compliance/dora/DORA-ART-11.md)

## Navigation
← [Docs Home](../README.md)

***

**Last Updated**: 2026-03-05
**Security Owner**: security@virons.ai
**Compliance Owner**: compliance@virons.ai
