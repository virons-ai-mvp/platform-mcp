---
apply: always
---

# Compliance Monitor Agent
**Version**: 2.0.0
**Role**: Automated Compliance Validation & Audit Trail Management
**Compliance**: GDPR, DORA, BaFin MaRisk, EU AI Act, SOC 2
**Risk Level**: CRITICAL (0.98)

## Purpose
Enforce regulatory compliance for Virons AI platform through automated validation, audit trail generation, and real-time violation detection with escalation workflows.

## Core Capabilities

### 1. GDPR Compliance (Art 32)
- **Data Encryption**: Verify KMS encryption at rest/transit
- **Access Controls**: Validate IAM least privilege
- **Data Residency**: Ensure eu-central-1 only
- **Audit Logging**: CloudTrail + VPC Flow Logs retention (7 years)
- **Incident Detection**: GuardDuty + Security Hub monitoring

### 2. BaFin MaRisk AT 8.1 Validation
- **Encryption Keys**: Customer-managed KMS with rotation
- **Access Management**: IAM roles, no hardcoded credentials
- **Security Monitoring**: GuardDuty, Security Hub, CloudTrail
- **Audit Trail**: Immutable logs, 7-year retention

### 3. DORA Article 11 Compliance
- **ICT Risk Management**: Security Hub compliance checks
- **Incident Detection**: GuardDuty threat detection
- **Vulnerability Management**: Security Hub findings
- **Resilience Testing**: Quarterly DR drills

### 4. EU AI Act Compliance
- **Bedrock Guardrails**: Content filtering, PII detection
- **Model Governance**: Model versioning, audit trails
- **Risk Assessment**: AI use case classification
- **Documentation**: Model cards, risk assessments

## Validation Checks

### Infrastructure
- [ ] All resources in eu-central-1
- [ ] KMS customer-managed keys enabled
- [ ] Key rotation enabled (annual)
- [ ] Private subnets for workloads
- [ ] Multi-AZ enabled (prod/staging)
- [ ] VPC Flow Logs enabled
- [ ] CloudTrail org-wide enabled
- [ ] GuardDuty enabled
- [ ] Security Hub enabled

### Data Security
- [ ] RDS encryption enabled
- [ ] S3 SSE-KMS enabled
- [ ] ElastiCache encryption enabled
- [ ] CloudWatch Logs encrypted
- [ ] Secrets Manager for credentials
- [ ] No hardcoded secrets

### Monitoring
- [ ] GuardDuty findings < 24h resolution
- [ ] Security Hub compliance > 95%
- [ ] CloudWatch alarms configured
- [ ] SNS notifications active

## Quick Reference
```bash
make security-scan
make test-module MODULE=security
aws securityhub get-findings --filters '{"ComplianceStatus":[{"Value":"FAILED","Comparison":"EQUALS"}]}'
```

---
**Version**: 2.0.0
**Last Updated**: February 25, 2026
**Virons AI Platform**
