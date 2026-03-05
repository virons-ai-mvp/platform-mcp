# 3-Repo Workflow Compliance Comparison

**Repos**: platform-og, platform-mcp, platform-infrastructure  
**Date**: 2026-03-05  
**Purpose**: Ensure consistent security, compliance, and governance across all Virons platform repos

---

## Executive Summary

| Category | platform-og | platform-mcp | platform-infrastructure | Status |
|----------|-------------|--------------|------------------------|--------|
| **Workflows** | 1 | 24 | 36 | ⚠️ Inconsistent |
| **Security** | ❌ Basic | ✅ 7 workflows | ✅ 8 workflows | 🔴 og missing |
| **Compliance** | ❌ None | ⚠️ 1 workflow | ✅ 5 workflows | 🔴 og critical |
| **Governance** | ❌ None | ❌ None | ✅ 6 workflows | 🔴 Both missing |
| **Testing** | ✅ Basic | ✅ 2 workflows | ✅ 4 workflows | 🟡 og minimal |

**Critical Finding**: platform-og has NO security scanning, NO compliance gates, NO governance - **immediate action required**

---

## 1. Workflow Inventory

### platform-og (1 workflow) 🔴 CRITICAL GAP

```
.github/workflows/
└── ci.yaml                    # Basic CI only
```

**What it has**:
- ✅ Lint (ruff)
- ✅ Type check (mypy)
- ✅ Tests (pytest)
- ✅ Coverage (codecov)
- ✅ Docker build
- ✅ Helm lint

**What it's MISSING** (critical):
- ❌ Secret scanning (gitleaks)
- ❌ SAST (bandit, semgrep)
- ❌ Dependency scanning
- ❌ Container scanning (trivy)
- ❌ CodeQL
- ❌ Compliance gates
- ❌ Governance enforcement
- ❌ Pre-commit validation

### platform-mcp (24 workflows) 🟡 GOOD

```
.github/workflows/
├── Security (7)
│   ├── bandit.yml
│   ├── codeql.yml
│   ├── semgrep.yml
│   ├── trivy.yml
│   ├── checkov.yml
│   ├── dependency-review-action.yml
│   └── scorecard-analysis.yml
├── Compliance (1)
│   └── virons-compliance-gate.yml
├── Testing (2)
│   ├── python.yml
│   └── pre-commit.yml
└── Other (14)
    ├── release.yml
    ├── gh-pages.yml
    ├── stale.yml
    └── ...
```

**Gaps**:
- ❌ gitleaks (secret scanning)
- ❌ Org governance
- ❌ Workflow governance
- ❌ Secrets rotation

### platform-infrastructure (36 workflows) ✅ COMPREHENSIVE

```
.github/workflows/
├── Security (8)
│   ├── codeql.yml
│   ├── compliance-gate.yml
│   ├── terraform-security-scan.yml
│   └── ...
├── Compliance (5)
│   ├── compliance-gate.yml
│   ├── compliance-checklist.yml
│   ├── org-compliance-report.yml
│   ├── tdd-governance-gate.yml
│   └── ddd-boundary-gate.yml
├── Governance (6)
│   ├── org-governance-enforce.yml
│   ├── workflow-governance.yml
│   ├── well-architected-gate.yml
│   └── ...
└── Testing (4)
    ├── terraform-test.yml
    ├── terraform-validate.yml
    └── ...
```

---

## 2. Security Scanning Comparison

| Scanner | platform-og | platform-mcp | platform-infrastructure | Regulation |
|---------|-------------|--------------|------------------------|------------|
| **gitleaks** | ❌ | ❌ | ✅ | GDPR Art 32, BaFin AT 8.1 |
| **bandit** | ❌ | ✅ | ✅ | BaFin AT 8.1 |
| **CodeQL** | ❌ | ✅ | ✅ | GDPR Art 32 |
| **semgrep** | ❌ | ✅ | ❌ | BaFin AT 8.1 |
| **trivy** | ❌ | ✅ | ❌ | DORA Art 11 |
| **checkov** | ❌ | ✅ | ❌ | BaFin AT 8.1 |
| **gosec** | N/A | N/A | ✅ | BaFin AT 8.1 |
| **Dependency Review** | ❌ | ✅ | ❌ | DORA Art 11 |
| **Scorecard** | ❌ | ✅ | ❌ | Security posture |

### Critical Gaps

**platform-og** (🔴 CRITICAL):
- Missing ALL security scanners
- No secret detection
- No SAST
- No dependency scanning
- **Regulatory violation**: BaFin AT 8.1, GDPR Art 32, DORA Art 11

**platform-mcp** (🟡 MEDIUM):
- Missing gitleaks (secret scanning)

**platform-infrastructure** (🟢 GOOD):
- Missing trivy, semgrep, checkov (but has equivalents)

---

## 3. Compliance Gates Comparison

| Gate | platform-og | platform-mcp | platform-infrastructure | Regulation |
|------|-------------|--------------|------------------------|------------|
| **BaFin AT 8.1** | ❌ | ✅ | ✅ | Audit trail |
| **GDPR Art 25** | ❌ | ✅ | ✅ | Data residency |
| **GDPR Art 32** | ❌ | ✅ | ✅ | Security |
| **DORA Art 11** | ❌ | ✅ | ✅ | ICT risk |
| **EU AI Act** | ❌ | ✅ | N/A | Model cards |
| **Aggregate Gate** | ❌ | ❌ | ✅ | All |
| **Checklist** | ❌ | ❌ | ✅ | All |
| **TDD Gate** | ❌ | ❌ | ✅ | Quality |
| **DDD Gate** | ❌ | ❌ | ✅ | Architecture |

### Critical Gaps

**platform-og** (🔴 CRITICAL):
- NO compliance validation whatsoever
- **Regulatory violation**: All 4 regulations (BaFin, GDPR, DORA, EU AI Act)
- Cannot be deployed to production

**platform-mcp** (🟡 MEDIUM):
- Missing aggregate compliance gate
- Missing compliance checklist
- Missing TDD/DDD gates

---

## 4. Governance Comparison

| Governance | platform-og | platform-mcp | platform-infrastructure |
|------------|-------------|--------------|------------------------|
| **Org-level** | ❌ | ❌ | ✅ |
| **Workflow** | ❌ | ❌ | ✅ |
| **DDD Boundary** | ❌ | ❌ | ✅ |
| **Service Contract** | ❌ | ❌ | ✅ |
| **Well-Architected** | ❌ | ❌ | ✅ |
| **Secrets Rotation** | ❌ | ❌ | ✅ |

### Critical Gaps

**Both platform-og and platform-mcp** (🔴 CRITICAL):
- No org-level governance
- No workflow governance
- No secrets rotation (DORA Art 11 violation)

---

## 5. Regulatory Compliance Matrix

### BaFin MaRisk AT 8.1 (IT Risk Management)

| Requirement | platform-og | platform-mcp | platform-infrastructure |
|-------------|-------------|--------------|------------------------|
| Audit trail | ❌ | ✅ | ✅ |
| Security scanning | ❌ | ✅ | ✅ |
| Change control | ❌ | ❌ | ✅ |
| Secret management | ❌ | ❌ | ✅ |
| **Status** | 🔴 **FAIL** | 🟡 **PARTIAL** | ✅ **PASS** |

### GDPR Art 32 (Security of Processing)

| Requirement | platform-og | platform-mcp | platform-infrastructure |
|-------------|-------------|--------------|------------------------|
| Encryption | ❌ | ✅ | ✅ |
| Access control | ❌ | ❌ | ✅ |
| Secret scanning | ❌ | ❌ | ✅ |
| Vulnerability mgmt | ❌ | ✅ | ✅ |
| **Status** | 🔴 **FAIL** | 🟡 **PARTIAL** | ✅ **PASS** |

### DORA Art 11 (ICT Risk Management)

| Requirement | platform-og | platform-mcp | platform-infrastructure |
|-------------|-------------|--------------|------------------------|
| Health monitoring | ✅ | ✅ | ✅ |
| Secret rotation | ❌ | ❌ | ✅ |
| Incident response | ❌ | ✅ | ✅ |
| Testing | ✅ | ✅ | ✅ |
| **Status** | 🔴 **FAIL** | 🟡 **PARTIAL** | ✅ **PASS** |

### EU AI Act (High-Risk AI Systems)

| Requirement | platform-og | platform-mcp | platform-infrastructure |
|-------------|-------------|--------------|------------------------|
| Model cards | ❌ | ✅ | N/A |
| Documentation | ❌ | ❌ | ✅ |
| Testing | ✅ | ✅ | ✅ |
| Audit trail | ❌ | ✅ | ✅ |
| **Status** | 🔴 **FAIL** | 🟡 **PARTIAL** | ✅ **PASS** |

---

## 6. CRITICAL: platform-og Immediate Actions

### 🔴 Phase 1: Security (Week 1 - URGENT)

**Copy from platform-infrastructure**:
```bash
cp platform-infrastructure/.github/workflows/codeql.yml platform-og/.github/workflows/
cp platform-infrastructure/.github/workflows/compliance-gate.yml platform-og/.github/workflows/
```

**Adapt for Python-only**:
- Remove Go/Terraform checks
- Keep Python SAST (bandit)
- Add gitleaks
- Add dependency scanning

**Minimum viable security**:
1. gitleaks.yml - Secret scanning
2. bandit.yml - Python SAST
3. codeql.yml - Code analysis
4. dependency-review.yml - Dependency scanning
5. trivy.yml - Container scanning

### 🔴 Phase 2: Compliance (Week 2 - CRITICAL)

**Create compliance gates**:
1. compliance-gate.yml - Aggregate security
2. virons-compliance-gate.yml - Virons-specific (copy from platform-mcp)
3. compliance-checklist.yml - Comprehensive validation

**Validate**:
- BaFin AT 8.1 (audit trail)
- GDPR Art 25 (data residency)
- GDPR Art 32 (security)
- DORA Art 11 (health checks)

### 🟡 Phase 3: Governance (Week 3 - HIGH)

**Add governance**:
1. org-governance-enforce.yml
2. workflow-governance.yml
3. secrets-rotation.yml
4. ddd-boundary-gate.yml

---

## 7. platform-mcp Actions

### 🔴 Phase 1: Critical Gaps (Week 1)

1. **gitleaks.yml** - Secret scanning (GDPR Art 32)
2. **compliance-gate.yml** - Aggregate security checks
3. **org-governance-enforce.yml** - Org policies

### 🟡 Phase 2: Governance (Week 2)

4. **workflow-governance.yml** - CI/CD governance
5. **secrets-rotation.yml** - Secret rotation (DORA Art 11)
6. **compliance-checklist.yml** - Comprehensive validation

---

## 8. Standardization Plan

### Goal: All 3 repos have equivalent security/compliance

**Standard Workflow Set** (minimum for all repos):

```
.github/workflows/
├── Security (mandatory)
│   ├── gitleaks.yml           # Secret scanning
│   ├── codeql.yml             # Code analysis
│   ├── bandit.yml             # Python SAST
│   ├── trivy.yml              # Container scanning
│   └── dependency-review.yml  # Dependency scanning
├── Compliance (mandatory)
│   ├── compliance-gate.yml    # Aggregate checks
│   ├── virons-compliance-gate.yml  # Virons-specific
│   └── compliance-checklist.yml    # Comprehensive
├── Governance (mandatory)
│   ├── org-governance-enforce.yml  # Org policies
│   ├── workflow-governance.yml     # CI/CD governance
│   └── secrets-rotation.yml        # Secret rotation
└── Testing (mandatory)
    ├── ci.yml                 # Basic CI
    └── pre-commit.yml         # Pre-commit validation
```

**Repo-specific additions**:
- platform-infrastructure: Terraform workflows
- platform-mcp: MCP-specific workflows
- platform-og: Service-specific workflows

---

## 9. Implementation Timeline

### Week 1 (CRITICAL - platform-og)
- [ ] Add gitleaks to platform-og
- [ ] Add bandit to platform-og
- [ ] Add CodeQL to platform-og
- [ ] Add trivy to platform-og
- [ ] Add dependency-review to platform-og

### Week 2 (HIGH - platform-og)
- [ ] Add compliance-gate to platform-og
- [ ] Add virons-compliance-gate to platform-og
- [ ] Add compliance-checklist to platform-og

### Week 3 (HIGH - platform-mcp)
- [ ] Add gitleaks to platform-mcp
- [ ] Add compliance-gate to platform-mcp
- [ ] Add org-governance to platform-mcp

### Week 4 (MEDIUM - Both)
- [ ] Add workflow-governance to both
- [ ] Add secrets-rotation to both
- [ ] Add compliance-checklist to platform-mcp

---

## 10. Success Criteria

✅ **Security Parity**: All 3 repos have equivalent security scanning  
✅ **Compliance Coverage**: All 4 regulations covered in all repos  
✅ **Governance**: Org-level policies enforced consistently  
✅ **Testing**: Comprehensive test coverage with gates  
✅ **Documentation**: All workflows documented  

### Validation

Run this check weekly:
```bash
# Count workflows
ls -1 platform-og/.github/workflows/*.y*ml | wc -l      # Should be >= 15
ls -1 platform-mcp/.github/workflows/*.y*ml | wc -l     # Should be >= 30
ls -1 platform-infrastructure/.github/workflows/*.y*ml | wc -l  # 36

# Check for critical workflows
for repo in platform-og platform-mcp platform-infrastructure; do
  echo "=== $repo ==="
  ls $repo/.github/workflows/ | grep -E "(gitleaks|compliance-gate|org-governance)" || echo "MISSING CRITICAL"
done
```

---

## 11. Risk Assessment

### platform-og (🔴 CRITICAL RISK)

**Current State**: 
- NO security scanning
- NO compliance validation
- NO governance
- **Cannot be deployed to production**

**Regulatory Risk**:
- BaFin MaRisk AT 8.1: VIOLATION (no audit trail validation)
- GDPR Art 32: VIOLATION (no security controls)
- DORA Art 11: VIOLATION (no ICT risk management)
- EU AI Act: VIOLATION (no model card validation)

**Business Impact**:
- Cannot pass regulatory audit
- Cannot deploy to EU
- Potential fines: Up to €20M or 4% of revenue (GDPR)

### platform-mcp (🟡 MEDIUM RISK)

**Current State**:
- Good security scanning
- Basic compliance validation
- NO governance

**Regulatory Risk**:
- GDPR Art 32: PARTIAL (missing secret scanning)
- DORA Art 11: PARTIAL (missing secret rotation)

**Business Impact**:
- Can deploy with caveats
- Needs improvement before audit

### platform-infrastructure (✅ LOW RISK)

**Current State**:
- Comprehensive security
- Full compliance validation
- Strong governance

**Regulatory Risk**: MINIMAL

---

## 12. Next Steps

1. **IMMEDIATE** (Today):
   - Create issues for platform-og critical gaps
   - Block platform-og deployments until Phase 1 complete

2. **Week 1**:
   - Implement platform-og Phase 1 (security)
   - Start platform-mcp critical gaps

3. **Week 2**:
   - Complete platform-og Phase 2 (compliance)
   - Complete platform-mcp critical gaps

4. **Week 3**:
   - Implement governance in both repos
   - Validate all workflows

5. **Week 4**:
   - Final validation
   - Documentation
   - Training

---

**Maintained By**: Virons Fintech Engineering Team  
**Last Updated**: 2026-03-05  
**Review Frequency**: Weekly until parity achieved, then monthly
