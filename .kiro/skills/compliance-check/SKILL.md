# Compliance Check Skill

**Name**: compliance-check
**Description**: Validate a service against BaFin, GDPR, DORA, and EU AI Act requirements.
**Arguments**: `[service-path]`
**User-invocable**: true

## Checks

### Security (All Services)
- [ ] No secrets in code (enforced by TruffleHog pre-commit hook)
- [ ] Container images scanned (enforced by Trivy pre-push hook)
- [ ] Images signed with Cosign (enforced in CI)
- [ ] Resource limits defined (enforced by OPA)
- [ ] Runs as non-root (enforced by OPA)
- [ ] Uses trusted registry: ghcr.io/virons-ai (enforced by OPA)

### BaFin AT 8.1 (Forensic Services Only)
- [ ] `write_audit()` called before `forensic_flags` write
- [ ] Calculation ordering: audit → deterministic → ML gate → fusion
- [ ] ML gate formula: `gated_ml = ml_score if len(deterministic_flags) >= 1 else 0.0`
- [ ] Nonlinear fusion: `S' = 1 − ∏(1 − sᵢ)`

### EU AI Act (ML Services Only)
- [ ] Model card exists at `docs/model-cards/{service-name}.md`
- [ ] Human oversight capability documented
- [ ] ML gate enforced (no standalone ML scores)
- [ ] Conformity assessment plan present

### GDPR Art 32 (All Services)
- [ ] Data residency: eu-central-1 only
- [ ] No PII in logs
- [ ] Request audit logging (API layer)
- [ ] KMS encryption for PII fields: `alias/virons-pii`

### DORA Art 11 (All Services)
- [ ] Health endpoints: `/health/live`, `/health/ready`
- [ ] Metrics endpoint: `/metrics`
- [ ] Graceful shutdown handler
- [ ] PodDisruptionBudget configured
- [ ] Resource limits set

## Output

```
Compliance Report: {service-name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Security:            ✅ PASS
BaFin AT 8.1:        ✅ PASS
EU AI Act:           ✅ PASS
GDPR Art 32:         ❌ FAIL
  - PII in logs: services/handler.go:42
DORA Art 11:         ✅ PASS

Overall: FAIL (1 violation)
```

## Example

```bash
compliance-check forensic/risk-scorer
```
