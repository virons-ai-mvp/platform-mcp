# Compliance Audit Command

**Description**: Run full compliance audit on a service or the entire repo.

**Usage**: `/compliance-audit [service-path or 'all']`

**Model**: claude-sonnet-4-5

## Behavior

Invoke the `virons-compliance-validator` agent to check:

### BaFin AT 8.1
- `write_audit()` present before every `forensic_flags` write
- Calculation ordering: audit → deterministic → ML gate → fusion

### EU AI Act
- Model card exists for high-risk AI services
- ML gate enforced: `gated_ml = ml_score if len(deterministic_flags) >= 1 else 0.0`
- Human oversight capability present

### GDPR Art 32
- Data residency: eu-central-1 only
- No PII in logs
- Request audit logging at API layer
- KMS encryption for PII fields

### DORA Art 11
- Health endpoints: `/health/live`, `/health/ready`
- Graceful shutdown handlers
- PodDisruptionBudget configured
- Resource limits set

## Namespace-Specific Checks

If argument is `all`, audit every namespace:

| Namespace | Regulations |
|---|---|
| `forensic/` | BaFin + GDPR + DORA |
| `ml/` | EU AI Act + GDPR + DORA |
| `ingestion/` | GDPR + DORA |
| `blockchain/` | DORA |
| `api/` | GDPR + DORA |

## Output

Compliance report with PASS/FAIL per service per regulation.
Flag any FAIL items with the specific file and line number.

## Example

```bash
/compliance-audit forensic/risk-scorer
/compliance-audit all
```
