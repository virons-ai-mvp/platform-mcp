# Compliance Steering — virons-services

Always-loaded. Applies to every file in this repository.

## Development Methodology

### Test-Driven Development (TDD) — MANDATORY
**Write tests FIRST, then code to pass tests.**

1. **Write failing test** — define expected behavior
2. **Write minimal code** — make test pass
3. **Refactor** — improve code while keeping tests green
4. **Repeat** — for each new feature or bug fix

**Coverage Target**: 95% minimum (unit + integration + comprehensive)
**Reference**: `docs/TESTING-STRATEGY.md` for patterns and examples

### Test Types Required
- **Unit tests** — isolated component testing with mocks
- **Integration tests** — service interactions with testcontainers
- **Comprehensive tests** — edge cases, error scenarios, end-to-end flows

## Regulatory Scope
- **BaFin MaRisk AT 8.1** — model governance, audit trail, deterministic-first ordering
- **GDPR Art 32** — data residency eu-central-1, encryption at rest/transit, PII minimisation
- **DORA Art 11** — ICT continuity, RTO ≤ 4h, RPO ≤ 1h, incident classification
- **EU AI Act** — high-risk AI systems require model cards, human oversight, conformity assessment

## Hard Rules (never violate)

### Calculation Ordering (BaFin AT 8.1)
`calculation_audit` MUST complete before `forensic_flags` are set. No exceptions.

### ML Gate
```python
gated_ml = ml_score if len(deterministic_flags) >= 1 else 0.0
```
ML scores are suppressed when no deterministic flag exists.

### Nonlinear Fusion
```python
S_prime = 1 - product(1 - s_i for s_i in scores)
```

### High-Risk AI Systems (EU AI Act)
- `anomaly-detector` (:9405) — requires model card at `docs/model-cards/anomaly-detector.md`
- `grandmaster-service` (:9421) — requires model card at `docs/model-cards/grandmaster-service.md`
- Both require human-in-the-loop override capability

### Data Residency (GDPR)
- All data MUST remain in `eu-central-1`
- No cross-region replication without explicit DPA amendment
- PII fields: encrypt with KMS key `alias/virons-pii`

### Audit Logging
- SHA-256 every ingested artifact (ingestion namespace)
- 100% request audit logging on API layer (api namespace)
- `write_audit()` call required in every forensic service write path

## Security Requirements (Automated)
- ✅ **Secret Scanning**: TruffleHog blocks commits with secrets (pre-commit hook)
- ✅ **Container Scanning**: Trivy scans for HIGH/CRITICAL CVEs (pre-push hook)
- ✅ **Audit Pattern**: Validates CalculationAudit before ForensicFlag writes (pre-commit hook)
- ✅ **SAST**: CodeQL scans Go, Python, JavaScript (CI)
- ✅ **Dependencies**: Dependabot weekly updates (CI)
- ✅ **Image Signing**: Cosign signs production images (CI)
- ✅ **Network Policies**: Zero-trust networking enforced (K8s)
- ✅ **Admission Control**: OPA policies enforce security (K8s)

## Compliance Checklist (run before every PR)
- [ ] `calculation_audit` precedes `forensic_flags` in call graph
- [ ] ML gate formula unchanged
- [ ] No hardcoded AWS account IDs or secrets (enforced by TruffleHog)
- [ ] All new PII fields encrypted
- [ ] Model cards updated if ML model changed
- [ ] Audit log coverage verified
- [ ] Security hooks passed (automatic)
- [ ] Container images signed (automatic in CI)
