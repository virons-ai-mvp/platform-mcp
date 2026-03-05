<link rel="stylesheet" href="../../../platform-resources/styles/virons-markdown.css">

# GDPR Art 25 & 32 Compliance

## Overview

***

**Regulation**: GDPR Articles 25 (Data Protection by Design) & 32 (Security of Processing)  
**Scope**: All MCP servers handling organizational data  
**Status**: ✅ Compliant

## Art 25: Data Protection by Design

***

### Requirements

> "The controller shall implement appropriate technical and organisational measures designed to implement data-protection principles."

### Implementation

| Principle | MCP Implementation | Evidence |
|-----------|-------------------|----------|
| **Data Minimization** | No PII stored in MCP servers | [audit-schema.sql](../evidence/audit-schema.sql) |
| **Purpose Limitation** | Audit logs only for compliance | [privacy-policy.md](../policies/privacy-policy.md) |
| **Storage Limitation** | 7-year retention (legal requirement) | [retention-policy.md](../policies/retention-policy.md) |
| **Integrity** | Immutable audit logs | [BAFIN-AT-8.1.md](../bafin/BAFIN-AT-8.1.md) |

### Compliance Gate

```python
# compliance-gate server (port 9101)
async def validate_commit(commit: Commit):
    """GDPR Art 25: Data protection by design."""
    violations = []
    
    # Check for PII in code
    if contains_pii(commit.diff):
        violations.append("PII detected in code")
    
    # Check for unencrypted secrets
    if contains_plaintext_secrets(commit.diff):
        violations.append("Plaintext secrets detected")
    
    # Audit
    await write_audit(
        server="compliance-gate",
        action="validate_commit",
        result="FAILURE" if violations else "SUCCESS",
        details={"violations": violations}
    )
    
    return violations
```

## Art 32: Security of Processing

***

### Requirements

> "The controller and processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk."

### Security Measures

| Measure | Implementation | Status |
|---------|----------------|--------|
| **Encryption in Transit** | TLS 1.3 for all MCP servers | ✅ |
| **Encryption at Rest** | AWS KMS for secrets, RDS encryption | ✅ |
| **Access Control** | IAM roles, least privilege | ✅ |
| **Audit Logging** | Immutable PostgreSQL logs | ✅ |
| **Secret Rotation** | <90 days (DORA Art 11) | ✅ |
| **Network Segmentation** | Context-based port ranges | ✅ |

### Encryption

```yaml
# Helm chart values
security:
  tls:
    enabled: true
    version: "1.3"
    ciphers:
      - TLS_AES_256_GCM_SHA384
      - TLS_CHACHA20_POLY1305_SHA256
  
  secrets:
    provider: aws-secrets-manager
    kms_key: arn:aws:kms:eu-central-1:xxx:key/virons-mcp
    rotation: 90d
  
  database:
    encryption: true
    kms_key: arn:aws:kms:eu-central-1:xxx:key/virons-audit
```

## Data Processing Records

***

### Processing Activities

| Activity | Purpose | Legal Basis | Retention |
|----------|---------|-------------|-----------|
| **Audit Logging** | Compliance (BaFin/DORA) | Legal obligation | 7 years |
| **Secret Scanning** | Security (prevent breaches) | Legitimate interest | 90 days |
| **Policy Enforcement** | Governance | Legitimate interest | 90 days |

### Data Categories

- **Technical Data**: Timestamps, IP addresses, server names
- **Operational Data**: Actions, results, error messages
- **No PII**: User IDs are pseudonymized (email hashes)

## Compliance Checklist

***

- [x] Data protection by design implemented (compliance-gate)
- [x] PII detection in pre-commit hooks
- [x] TLS 1.3 encryption for all traffic
- [x] AWS KMS encryption for secrets at rest
- [x] RDS encryption for audit database
- [x] IAM least privilege access control
- [x] 7-year audit log retention (legal requirement)
- [x] Secret rotation <90 days
- [x] Network segmentation by context
- [x] Data processing records documented

## Monitoring

***

```yaml
# Security alarms
GDPRSecurityAlarm:
  - name: unencrypted-traffic
    metric: UnencryptedConnections
    threshold: 0
    action: block
  
  - name: secret-age-violation
    metric: SecretAge
    threshold: 90
    action: alert
  
  - name: unauthorized-access
    metric: UnauthorizedAccessAttempts
    threshold: 1
    action: alert
```

## References

***

- [GDPR Art 25 (Official Text)](references/gdpr-art-25.pdf)
- [GDPR Art 32 (Official Text)](references/gdpr-art-32.pdf)
- [Privacy Policy](../policies/privacy-policy.md)

## Navigation
← [Compliance Home](../README.md)

***

**Last Updated**: 2026-03-05  
**Compliance Owner**: compliance@virons.ai
