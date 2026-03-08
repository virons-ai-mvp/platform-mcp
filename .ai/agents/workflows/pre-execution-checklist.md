# Pre-Execution Checklist

**Purpose**: Mandatory validation before any infrastructure change

## Before ANY Terraform Apply or K8s Change

### 1. Testing ✅
- [ ] `pytest tests/ -v` passes
- [ ] No failures in `tests/integration/<affected-context>/`

### 2. Governance Gates ✅
- [ ] `python3 scripts/ci/well_architected_gate.py ...` passes
- [ ] `python3 scripts/ci/validate_ddd_boundaries.py ...` passes
- [ ] `python3 scripts/ci/validate_service_contracts.py ...` passes

### 3. Security ✅
- [ ] `make security-scan` clean
- [ ] No hardcoded credentials
- [ ] KMS encryption enabled
- [ ] Private subnets used (unless ALB/CloudFront)
- [ ] All resources tagged (Environment, Project, ManagedBy, CostCenter)
- [ ] Resources in eu-central-1 only

### 4. Cost Impact ✅
- [ ] Budget impact assessed
- [ ] Within environment limits: Dev $400 · Staging $900 · Demo $1,200 · Prod $2,500

### 5. Terraform ✅
- [ ] `terraform validate` passes
- [ ] `terraform plan` reviewed and saved

### 6. Approval ✅
- [ ] Human approval obtained
- [ ] Production change window confirmed: **Tue–Thu 10:00–16:00 CET**

## Org-Level Changes (`.github/governance/`, `scripts/org/`, reusable workflows)

Additional checks — these affect all 9 repos:
- [ ] Impact on all repo profiles assessed (`repo-manifest.yaml`)
- [ ] `python3 scripts/org/generate-compliance-dashboard.py virons-fintech` run post-change
- [ ] VP Engineering approval obtained

## Failure Response

If ANY check fails: **STOP** → document reason → fix → revalidate.
