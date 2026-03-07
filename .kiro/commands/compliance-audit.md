# /compliance-audit - Run Compliance Audit

Validate BaFin, GDPR, DORA, and EU AI Act compliance across MCP servers.

## Usage

```
/compliance-audit [target]
```

## Arguments

- `target` - What to audit:
  - `all` - All MCP servers (default)
  - `infrastructure` - Infrastructure MCP server
  - `security` - Security MCP server
  - `operations` - Operations MCP server
  - `monitoring` - Monitoring MCP server
  - `gateway` - MCP gateway

## Example

```
/compliance-audit all
/compliance-audit infrastructure
```

## What It Checks

### BaFin MaRisk AT 8.1
- [ ] Audit logging enabled
- [ ] Request/response logging
- [ ] Correlation ID tracking
- [ ] Calculation ordering (if applicable)

### GDPR Art 32
- [ ] Data residency in eu-central-1
- [ ] PII encryption with KMS
- [ ] Request audit logging (100%)
- [ ] Data retention policies

### DORA Art 11
- [ ] RTO ≤ 4h
- [ ] RPO ≤ 1h
- [ ] PDB configured (min available 1)
- [ ] Graceful shutdown (30s)
- [ ] Health checks (/health, /ready)

### EU AI Act
- [ ] Model cards (if ML tools)
- [ ] Human oversight (if high-risk AI)
- [ ] Transparency requirements
- [ ] Risk assessment documentation

### Security
- [ ] Secrets scanning (TruffleHog)
- [ ] Vulnerability scanning (Trivy)
- [ ] Image signing (Cosign)
- [ ] Run as non-root
- [ ] Read-only root filesystem
- [ ] Network policies

### Monitoring
- [ ] Prometheus metrics (/metrics)
- [ ] Distributed tracing (correlation IDs)
- [ ] Health endpoints (/health, /ready)
- [ ] Structured logging

## Output

```
🔍 Compliance Audit Report
==========================

Server: virons-infrastructure-mcp
Status: ✅ COMPLIANT

BaFin MaRisk AT 8.1:
  ✅ Audit logging enabled
  ✅ Correlation ID tracking
  ✅ Request/response logging

GDPR Art 32:
  ✅ Data residency: eu-central-1
  ✅ PII encryption: alias/virons-pii
  ✅ Request audit logging: 100%

DORA Art 11:
  ✅ RTO: 4h
  ✅ RPO: 1h
  ✅ PDB: min available 1
  ✅ Health checks: /health, /ready

Security:
  ✅ Secrets scanning: enabled
  ✅ Vulnerability scanning: enabled
  ✅ Image signing: enabled
  ✅ Run as non-root: true
  ✅ Read-only filesystem: true

Monitoring:
  ✅ Prometheus metrics: /metrics
  ✅ Distributed tracing: enabled
  ✅ Health endpoints: /health, /ready

==========================
Summary: 18/18 checks passed
```

## Related

- Compliance Requirements: `.kiro/steering/compliance.md`
- Security Policy: `.kiro/SECURITY-POLICY.md`
- Monitoring Guide: `docs/operations/monitoring.md`
