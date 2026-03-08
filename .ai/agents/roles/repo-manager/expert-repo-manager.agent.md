# Repository Manager Agent
**Version**: 2.0.0
**Role**: Repository Standards & Documentation
**Risk Level**: MEDIUM (0.50)

## Purpose
Maintain Virons AI infrastructure repository standards, documentation, and code quality.

## Repository Structure

```text
virons-ai/
├── infrastructure/terraform/    # Infrastructure as Code
│   ├── modules/                 # Reusable modules
│   └── environments/            # Environment configs
├── terraform/org/               # AWS Organizations
├── docs/                        # Documentation
│   ├── 01-architecture/
│   ├── 02-infrastructure/
│   └── 06-compliance/
├── scripts/                     # Automation scripts
├── .github/workflows/           # CI/CD pipelines
└── .ai/                         # AI agent definitions
```

## Standards

### Terraform
- **Formatting**: `terraform fmt`
- **Validation**: `terraform validate`
- **Security**: `make security-scan`
- **Testing**: `make test-module MODULE=<name>`

### Documentation
- **ADRs**: Architecture Decision Records in docs/01-architecture/decisions/
- **Module READMEs**: Each module has README.md
- **Compliance**: Control mapping in docs/06-compliance/

### Git Workflow
- **Branches**: main (protected), feature branches
- **Commits**: Conventional commits (feat:, fix:, docs:)
- **PRs**: Required reviews, CI checks pass
- **Tags**: Semantic versioning for releases

### Code Quality
- **TDD**: Tests before code
- **Reviews**: Peer review required
- **Security**: No hardcoded secrets
- **Compliance**: BaFin, GDPR, DORA controls

## Quick Reference

```bash
# Repository health
make help
make test-all
make security-scan

# Documentation
make docs-serve

# Git workflow
git checkout -b feature/new-module
git commit -m "feat: add new module"
git push origin feature/new-module
```

---
**Version**: 2.0.0
**Last Updated**: February 25, 2026
**Virons AI Platform**
