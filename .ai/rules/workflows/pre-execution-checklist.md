# Pre-Execution Checklist

**Applies To**: All environments, all agents — before any `kubectl apply` or deployment

## Before ANY Deployment

### 1. Testing ✅
- [ ] Unit tests written (TDD — test first)
- [ ] Tests pass: `go test ./...` or `pytest`
- [ ] Coverage ≥ 80%

### 2. Security ✅
- [ ] `trivy image {image}` — no CRITICAL vulnerabilities
- [ ] `gosec ./...` (Go) or `bandit -r src/` (Python) — clean
- [ ] `gitleaks detect` — no secrets
- [ ] No hardcoded credentials
- [ ] Non-root container user
- [ ] Read-only root filesystem

### 3. Compliance ✅
- [ ] `calculation_audit` written BEFORE `forensic_flags` (forensic services)
- [ ] ML gate rule applied (ml services)
- [ ] Model card exists (anomaly-detector, grandmaster-service)
- [ ] 100% request audit logging (api services)
- [ ] SHA-256 hash on all ingested artifacts (ingestion services)
- [ ] All data in eu-central-1

### 4. K8s Manifest ✅
- [ ] `kubectl apply --dry-run=client` passes
- [ ] Resource limits set (CPU + memory)
- [ ] Liveness + readiness probes configured
- [ ] IRSA annotation on ServiceAccount
- [ ] Required labels: `app`, `version`, `namespace`

### 5. Cost Impact ✅
- [ ] Within environment budget
- [ ] No new node groups without approval

### 6. Approval ✅
- [ ] Human approval obtained
- [ ] Change window confirmed (production: Tue–Thu 10:00–16:00 CET)
- [ ] Rollback plan documented

## Failure Response

If ANY check fails:
1. STOP — do not proceed
2. Document failure reason
3. Fix the issue
4. Rerun checklist
