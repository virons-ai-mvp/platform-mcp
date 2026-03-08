# Security Validation Skill

**Name**: security-validation
**Description**: Run all security checks before commit/push
**Arguments**: `[--scope=local|ci|runtime]`
**User-invocable**: true

## Security Layers

### Local (Pre-commit/Pre-push)
```bash
# Runs automatically via Git hooks
git commit -m "feat: ..."  # TruffleHog + audit pattern validation
git push                    # Trivy container scanning
```

### CI (GitHub Actions)
- Secret scanning (TruffleHog)
- Container scanning (Trivy)
- SAST (CodeQL)
- Audit pattern validation
- Dependency scanning (Dependabot)
- Image signing (Cosign)

### Runtime (Kubernetes)
- NetworkPolicy enforcement (zero-trust)
- OPA admission control (trusted registry, non-root, resource limits)

## Manual Validation

### Check for Secrets
```bash
trufflehog git file://. --json --no-update
```

### Scan Containers
```bash
trivy image ghcr.io/virons-ai/service:tag
```

### Validate Audit Pattern
```bash
./scripts/validate-audit-pattern.sh
```

### Verify Image Signature
```bash
cosign verify ghcr.io/virons-ai/service:tag
```

## Security Checklist

Before every commit:
- [ ] No secrets in code (automatic)
- [ ] Audit pattern followed (automatic)
- [ ] Tests passing (manual)

Before every push:
- [ ] Container images scanned (automatic)
- [ ] No HIGH/CRITICAL CVEs (automatic warning)

Before every deploy:
- [ ] Images signed (automatic in CI)
- [ ] NetworkPolicy configured
- [ ] OPA policies pass
- [ ] Resource limits defined

## Emergency Bypass

**ONLY for production incidents:**
```bash
export VIRONS_EMERGENCY_BYPASS=true
git commit --no-verify
git push --no-verify
unset VIRONS_EMERGENCY_BYPASS
```

Document every bypass in `SECURITY.md` with reason and fix date.

## References

- `SECURITY.md` - Complete security documentation
- `docs/SOLO-DEVELOPER-QUICK-START.md` - Setup guide
- `k8s/opa-policies/README.md` - OPA deployment
- `.github/workflows/security-gate.yml` - CI security gate
