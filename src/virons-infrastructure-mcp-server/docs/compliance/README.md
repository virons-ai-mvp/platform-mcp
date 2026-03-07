# Compliance Documentation

Regulatory compliance documentation for BaFin, GDPR, DORA, and EU AI Act.

## Contents

- [Overview](overview.md) - Compliance requirements
- [Logging Implementation](logging-implementation.md) - BaFin audit trails
- [Policies](policies/) - Compliance policies
- [Audits](audits/) - Audit reports
- [Evidence](evidence/) - Compliance evidence

## Regulations

### BaFin MaRisk AT 8.1
- Audit trails with 10-year retention
- Calculation audit before forensic flags
- Write audit on every write operation
- Immutable logs

### GDPR Art 32
- Security measures for data processing
- Encryption at rest and in transit
- Access controls and audit logs

### DORA Art 11
- ICT risk management framework
- Health checks and monitoring
- Incident response procedures

### EU AI Act
- High-risk system documentation
- Model cards and versioning
- Human oversight mechanisms

## Implementation

See [Logging Implementation](logging-implementation.md) for technical details.
