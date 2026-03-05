# Workflow Compliance Comparison: platform-mcp vs platform-infrastructure

**Date**: 2026-03-05  
**Purpose**: Ensure platform-mcp has equivalent security, compliance, and governance workflows as platform-infrastructure

---

## Executive Summary

| Category | platform-infrastructure | platform-mcp | Status |
|----------|------------------------|--------------|--------|
| **Security Scanning** | ✅ 8 workflows | ⚠️ 7 workflows | Missing 1 |
| **Compliance Gates** | ✅ 5 workflows | ✅ 1 workflow | Need 4 more |
| **Governance** | ✅ 6 workflows | ❌ 0 workflows | Need 6 |
| **Testing** | ✅ 4 workflows | ✅ 2 workflows | Need 2 |
| **Total Workflows** | 36 workflows | 24 workflows | Need 12 |

---

## 1. Security Scanning Workflows

### ✅ Present in Both

| Workflow | platform-infrastructure | platform-mcp | Notes |
|----------|------------------------|--------------|-------|
| **CodeQL** | ✅ Python, Go | ✅ Python, Actions | MCP: Add TypeScript |
| **Bandit (Python SAST)** | ✅ | ✅ | ✅ Equivalent |
| **Trivy** | ❌ | ✅ | MCP has it |
| **Semgrep** | ❌ | ✅ | MCP has it |
| **Checkov** | ❌ | ✅ | MCP has it |
| **Dependency Review** | ❌ | ✅ | MCP has it |
| **Scorecard** | ❌ | ✅ | MCP has it |

### ❌ Missing in platform-mcp

| Workflow | Purpose | Priority |
|----------|---------|----------|
| **gosec** | Go SAST scanning | N/A (no Go in MCP) |
| **gitleaks** | Secret scanning | 🔴 HIGH - Add immediately |

### ❌ Missing in platform-infrastructure

| Workflow | Purpose | Priority |
|----------|---------|----------|
| **Trivy** | Container/IaC scanning | 🟡 MEDIUM |
| **Semgrep** | Multi-language SAST | 🟡 MEDIUM |
| **Checkov** | IaC security | 🟡 MEDIUM |

---

## 2. Compliance Gate Workflows

### ✅ Present in platform-infrastructure

| Workflow | Purpose | Regulatory Coverage |
|----------|---------|---------------------|
| **compliance-gate.yml** | Aggregate security checks | GDPR Art 32, BaFin AT 8.1, DORA Art 11 |
| **compliance-checklist.yml** | Compliance validation | All regulations |
| **org-compliance-report.yml** | Org-level compliance | Cross-repo |
| **terraform-security-scan.yml** | IaC security | BaFin AT 8.1 |
| **tdd-governance-gate.yml** | TDD enforcement | Quality |

### ✅ Present in platform-mcp

| Workflow | Purpose | Regulatory Coverage |
|----------|---------|---------------------|
| **virons-compliance-gate.yml** | Virons server compliance | BaFin AT 8.1, GDPR Art 25/32, DORA Art 11, EU AI Act |

### ❌ Missing in platform-mcp (CRITICAL)

| Workflow | Purpose | Priority |
|----------|---------|----------|
| **compliance-gate.yml** | Aggregate all security checks | 🔴 HIGH |
| **compliance-checklist.yml** | Comprehensive validation | 🔴 HIGH |
| **terraform-security-scan.yml** | IaC scanning (if applicable) | 🟡 MEDIUM |
| **tdd-governance-gate.yml** | TDD enforcement | 🟢 LOW (have pre-commit) |

---

## 3. Governance Workflows

### ✅ Present in platform-infrastructure

| Workflow | Purpose | Scope |
|----------|---------|-------|
| **org-governance-enforce.yml** | Org-level policy enforcement | Cross-repo |
| **workflow-governance.yml** | Workflow validation | CI/CD |
| **ddd-boundary-gate.yml** | DDD boundary validation | Architecture |
| **microservice-contract-gate.yml** | Service contract validation | Services |
| **well-architected-gate.yml** | AWS Well-Architected | Infrastructure |
| **reusable-org-*.yml** (6 files) | Reusable governance profiles | Org-wide |

### ❌ Missing in platform-mcp (CRITICAL)

| Workflow | Purpose | Priority |
|----------|---------|----------|
| **org-governance-enforce.yml** | Org policy enforcement | 🔴 HIGH |
| **workflow-governance.yml** | CI/CD validation | 🔴 HIGH |
| **ddd-boundary-gate.yml** | DDD validation | 🟡 MEDIUM |
| **mcp-contract-gate.yml** | MCP tool contract validation | 🟡 MEDIUM |

---

## 4. Testing Workflows

### ✅ Present in Both

| Workflow | platform-infrastructure | platform-mcp | Notes |
|----------|------------------------|--------------|-------|
| **Python Tests** | ✅ terraform-test.yml | ✅ python.yml | Different names |
| **Pre-commit** | ✅ | ✅ | ✅ Equivalent |

### ❌ Missing in platform-mcp

| Workflow | Purpose | Priority |
|----------|---------|----------|
| **terraform-validate.yml** | Terraform validation | N/A (no Terraform) |
| **terraform-ci.yml** | Terraform CI | N/A (no Terraform) |

---

## 5. Additional Workflows

### Platform-Infrastructure Only

| Workflow | Purpose | Applicable to MCP? |
|----------|---------|-------------------|
| **deploy.yml** | Deployment automation | ❌ No (different deployment) |
| **secrets-rotation.yml** | Secret rotation | ✅ Yes - Add |
| **notify-docs.yml** | Documentation notifications | ✅ Yes - Add |
| **diagram-sync-mcp.yml** | Diagram synchronization | ✅ Yes - Adapt |

### Platform-MCP Only

| Workflow | Purpose | Applicable to Infra? |
|----------|---------|---------------------|
| **release.yml** | Package release | ❌ No |
| **gh-pages.yml** | Documentation site | ❌ No |
| **stale.yml** | Stale issue management | ✅ Yes - Add |
| **merge-prevention.yml** | Branch protection | ✅ Yes - Add |

---

## 6. Critical Gaps in platform-mcp

### 🔴 HIGH Priority (Add Immediately)

1. **gitleaks** - Secret scanning (GDPR Art 32, BaFin AT 8.1)
2. **compliance-gate.yml** - Aggregate security checks
3. **compliance-checklist.yml** - Comprehensive compliance validation
4. **org-governance-enforce.yml** - Org-level policy enforcement
5. **workflow-governance.yml** - CI/CD governance

### 🟡 MEDIUM Priority (Add Soon)

6. **secrets-rotation.yml** - Automated secret rotation (DORA Art 11)
7. **notify-docs.yml** - Documentation change notifications
8. **ddd-boundary-gate.yml** - DDD architecture validation
9. **mcp-contract-gate.yml** - MCP tool contract validation (new)

### 🟢 LOW Priority (Nice to Have)

10. **stale.yml** - Issue management
11. **merge-prevention.yml** - Additional branch protection
12. **diagram-sync-mcp.yml** - Architecture diagram sync

---

## 7. Recommended Actions

### Phase 1: Critical Security (Week 1)

```bash
# Add to platform-mcp/.github/workflows/
1. gitleaks.yml                    # Secret scanning
2. compliance-gate.yml             # Aggregate security
3. compliance-checklist.yml        # Comprehensive validation
```

### Phase 2: Governance (Week 2)

```bash
4. org-governance-enforce.yml      # Org policies
5. workflow-governance.yml         # CI/CD governance
6. secrets-rotation.yml            # Secret rotation
```

### Phase 3: Architecture (Week 3)

```bash
7. ddd-boundary-gate.yml           # DDD validation
8. mcp-contract-gate.yml           # MCP contracts
9. notify-docs.yml                 # Doc notifications
```

---

## 8. Compliance Mapping

### BaFin MaRisk AT 8.1 (IT Risk Management)

| Requirement | platform-infrastructure | platform-mcp | Gap |
|-------------|------------------------|--------------|-----|
| Audit trail | ✅ compliance-gate | ✅ virons-compliance-gate | ✅ |
| Secret management | ✅ secrets-rotation | ❌ | 🔴 Add |
| Security scanning | ✅ Multiple | ✅ Multiple | ✅ |
| Change control | ✅ workflow-governance | ❌ | 🔴 Add |

### GDPR Art 32 (Security of Processing)

| Requirement | platform-infrastructure | platform-mcp | Gap |
|-------------|------------------------|--------------|-----|
| Encryption | ✅ terraform-security | ✅ checkov | ✅ |
| Access control | ✅ org-governance | ❌ | 🔴 Add |
| Secret scanning | ✅ gitleaks | ❌ | 🔴 Add |
| Vulnerability mgmt | ✅ Multiple | ✅ Multiple | ✅ |

### DORA Art 11 (ICT Risk Management)

| Requirement | platform-infrastructure | platform-mcp | Gap |
|-------------|------------------------|--------------|-----|
| Health monitoring | ✅ | ✅ virons-compliance-gate | ✅ |
| Secret rotation | ✅ secrets-rotation | ❌ | 🔴 Add |
| Incident response | ✅ compliance-gate | ✅ virons-compliance-gate | ✅ |
| Testing | ✅ Multiple | ✅ Multiple | ✅ |

### EU AI Act (High-Risk AI Systems)

| Requirement | platform-infrastructure | platform-mcp | Gap |
|-------------|------------------------|--------------|-----|
| Model cards | N/A | ✅ virons-compliance-gate | ✅ |
| Documentation | ✅ notify-docs | ❌ | 🟡 Add |
| Testing | ✅ | ✅ | ✅ |
| Audit trail | ✅ | ✅ | ✅ |

---

## 9. Implementation Plan

### Step 1: Copy & Adapt from platform-infrastructure

```bash
# Copy workflows that need minimal changes
cp platform-infrastructure/.github/workflows/gitleaks.yml platform-mcp/.github/workflows/
cp platform-infrastructure/.github/workflows/secrets-rotation.yml platform-mcp/.github/workflows/
cp platform-infrastructure/.github/workflows/notify-docs.yml platform-mcp/.github/workflows/
```

### Step 2: Create New MCP-Specific Workflows

```bash
# Create new workflows for MCP-specific needs
- mcp-contract-gate.yml          # Validate MCP tool contracts
- mcp-server-health-gate.yml     # Validate server health endpoints
- mcp-integration-test.yml       # Integration testing
```

### Step 3: Adapt Existing Workflows

```bash
# Adapt infrastructure workflows for MCP context
- compliance-gate.yml            # Remove Terraform, add Python/TypeScript
- org-governance-enforce.yml     # Add MCP-specific rules
- workflow-governance.yml        # Add MCP workflow patterns
```

---

## 10. Success Criteria

✅ **Security Parity**: platform-mcp has equivalent or better security scanning  
✅ **Compliance Coverage**: All 4 regulations covered (BaFin, GDPR, DORA, EU AI Act)  
✅ **Governance**: Org-level policies enforced consistently  
✅ **Testing**: Comprehensive test coverage with gates  
✅ **Documentation**: All workflows documented and maintained  

---

## 11. Next Steps

1. **Review this document** with team
2. **Prioritize gaps** based on regulatory requirements
3. **Create issues** for each missing workflow
4. **Implement Phase 1** (critical security) immediately
5. **Schedule Phases 2-3** for next 2 weeks

---

**Maintained By**: Virons Fintech Engineering Team  
**Last Updated**: 2026-03-05  
**Review Frequency**: Monthly
