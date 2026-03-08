# Security Workflows

## Container Scanning

```bash
# Scan image before push
trivy image --exit-code 1 --severity CRITICAL \
  412179655775.dkr.ecr.eu-central-1.amazonaws.com/virons/{service}:{tag}
```

## Static Analysis

```bash
# Go
gosec ./...
golangci-lint run --enable=gosec,gocritic

# Python
bandit -r src/ -ll  # medium+ severity
```

## Secret Detection

```bash
gitleaks detect --source . --verbose
```

## SBOM Generation

```bash
syft {image} -o spdx-json > sbom.json
```

## K8s Security Checks

```bash
# Validate manifests
kubectl apply --dry-run=client -f k8s/

# Check for security issues
trivy config k8s/
```

## Required Dockerfile Patterns

```dockerfile
# Non-root user (mandatory)
RUN addgroup -S virons && adduser -S virons -G virons
USER virons

# Read-only filesystem (set in K8s manifest)
# securityContext:
#   readOnlyRootFilesystem: true
```

## Auto-Reject Conditions

- CRITICAL CVE in base image → update base image, do not suppress
- Hardcoded secret detected → remove immediately, rotate secret
- `runAsRoot: true` → fix before merge
- `privileged: true` → fix before merge
