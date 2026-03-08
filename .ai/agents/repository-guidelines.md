# Repository Guidelines

## Architecture

This repo uses **DDD bounded contexts** — not flat Terraform modules.

```
bounded-contexts/<context>/
├── context.contract.yaml   # domain contract (API, events, dependencies)
├── domain/                 # Terraform domain definitions
├── infrastructure/terraform/
└── tests/domain/ security/ compliance/
```

Cross-context dependencies are enforced by `bounded-contexts/dependency-map.yaml`. Circular dependencies are forbidden. Violations fail the `ddd-boundary-gate` CI check.

## TDD Workflow

1. Write failing test in `tests/integration/<context>/` or `tests/unit/`
2. Implement minimal code to pass
3. Run `pytest tests/ -v`
4. Commit

## Security Requirements

All resources must have:
- KMS encryption
- Private subnet placement (unless ALB/CloudFront)
- Tags: `Environment`, `Project`, `ManagedBy`, `CostCenter`
- CloudWatch logging
- Region: `eu-central-1` only

## Governance Gates

All PRs to `main` must pass:
- Well-Architected gate (`scripts/ci/well_architected_gate.py`)
- DDD boundary gate (`scripts/ci/validate_ddd_boundaries.py`)
- Service contract gate (`scripts/ci/validate_service_contracts.py`)
- TDD gate (`scripts/ci/tdd_governance_gate.py`)
- MCP health gate (`scripts/ci/mcp_gate.sh`)

## Org Scope

This repo is the **control plane** for all 9 virons-fintech repos. Changes to `.github/governance/` affect the entire org. Always run `python3 scripts/org/generate-compliance-dashboard.py virons-fintech` after org-level changes.

## Commit Format

```
<type>(<scope>): <subject>
Types: feat, fix, docs, test, refactor, chore
Scope: context name (e.g., compute, security, ai-ml) or infra/k8s/governance
```
