# Agent Restrictions

**Compliance**: BaFin MaRisk AT 8.1, GDPR Art 32, DORA Art 11, EU AI Act

## NEVER Execute Without Human Approval

- `kubectl apply` in production namespace
- `kubectl delete` any resource
- `aws eks update-cluster-config`
- `aws rds modify-db-instance` / `delete-db-instance`
- Database schema migrations in staging/production
- Scaling node groups
- Modifying IAM roles/policies
- Changing KMS key policies

## Read-Only Operations (Always Safe)

- `kubectl get`, `kubectl describe`, `kubectl logs`
- `aws eks describe-cluster`
- `aws rds describe-db-instances`
- `aws ec2 describe-*`
- `aws s3 ls`
- File reading, code analysis, documentation generation
- Running tests locally

## Auto-Reject (Never Allow)

### Security Violations
- Hardcoding AWS credentials or API keys
- Disabling KMS encryption
- `runAsRoot: true` in K8s manifests
- `privileged: true` in K8s manifests
- Security groups with `0.0.0.0/0` ingress (except ALB port 443)
- IAM policies with `*` actions

### Compliance Violations
- Resources outside eu-central-1 (GDPR data residency)
- Writing `forensic_flags` before `calculation_audit` (BaFin AT 8.1)
- Bypassing ML gate rule
- Deploying high-risk AI without model card (EU AI Act)
- Removing audit logging
- Missing required K8s labels (app, version, namespace)

### Process Violations
- Committing directly to main branch
- Deploying without passing tests
- Skipping compliance-validator for forensic/ml changes

## Environment Rules

### Development
- `kubectl apply` allowed after human approval
- Cost limit: $400/month

### Staging / Production
- Full review + security scan + compliance check + approval
- Change window (production): Tue–Thu 10:00–16:00 CET
- Rollback plan mandatory

## Escalation

LOW (read-only) → Execute immediately
MEDIUM (dev apply) → Show plan, request approval
HIGH (staging/prod) → Full review + approval
CRITICAL (security/compliance) → Block + escalate
