# MCP Bounded Contexts

## Context Map

```
┌─────────────────────┐
│  Security Context   │
│  - gitleaks         │
│  - compliance-gate  │
└──────────┬──────────┘
           │
           │ publishes: scan_results
           ▼
┌─────────────────────┐
│ Compliance Context  │
│ - compliance-check  │
└──────────┬──────────┘
           │
           │ validates: policies
           ▼
┌─────────────────────┐
│ Governance Context  │
│ - org-governance    │
│ - workflow-gov      │
└──────────┬──────────┘
           │
           │ enforces: rotation
           ▼
┌─────────────────────┐
│ Operations Context  │
│ - secrets-rotation  │
└─────────────────────┘
```

## Bounded Context: Security

**Responsibility**: Secret scanning, vulnerability detection

**Services**:
- `gitleaks` (port 9100): Pre-commit secret scanning
- `compliance-gate` (port 9101): Compliance validation gate

**Domain Events**:
- `SecretDetected`
- `ScanCompleted`

**Compliance**: BaFin AT 8.1 (audit trail)

## Bounded Context: Governance

**Responsibility**: Policy enforcement, workflow validation

**Services**:
- `org-governance` (port 9102): Org-level policy checks
- `workflow-governance` (port 9103): Workflow validation

**Domain Events**:
- `PolicyViolated`
- `WorkflowApproved`

**Compliance**: GDPR Art 25 (data protection by design)

## Bounded Context: Operations

**Responsibility**: Secret rotation, operational automation

**Services**:
- `secrets-rotation` (port 9104): Automated secret rotation

**Domain Events**:
- `SecretRotated`
- `RotationFailed`

**Compliance**: DORA Art 11 (ICT risk management)

## Bounded Context: Compliance

**Responsibility**: Compliance checklist validation

**Services**:
- `compliance-checklist` (port 9105): Multi-regulation validation

**Domain Events**:
- `ComplianceCheckPassed`
- `ComplianceCheckFailed`

**Compliance**: BaFin AT 8.1, GDPR Art 32, DORA Art 11

## Integration Patterns

- **Event-Driven**: Security → Compliance → Governance
- **Request-Response**: Governance ↔ Operations
- **Shared Kernel**: Common compliance models
