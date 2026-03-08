# virons-services Repository Guidelines

Core guidelines for working with the virons-services microservices platform.

## TDD Workflow

1. Write test first (must fail)
2. Implement minimal code to pass
3. Run tests
4. Refactor if needed
5. Commit with conventional commit message

## Language Standards

| Namespace | Language | Version |
|---|---|---|
| ingestion | Go | 1.23 |
| blockchain | Go | 1.23 |
| api (REST/WS) | Go | 1.23 |
| forensic | Python | 3.12 |
| ml | Python | 3.12 |
| api (dashboard) | Next.js | 15 |

## Security Requirements

All services must have:
- IRSA (IAM Roles for Service Accounts) — no static credentials
- Private subnet placement
- Non-root container user
- Read-only root filesystem
- Resource limits (CPU/memory)
- Structured JSON logging (zerolog / structlog)

## Service Structure

```
{namespace}/{service-name}/
├── cmd/main.go          (Go) or main.py (Python)
├── internal/            (Go) or src/ (Python)
├── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── README.md
```

## Compliance — Non-Negotiable

- **BaFin AT 8.1**: `calculation_audit` written BEFORE `forensic_flags`
- **GDPR Art 32**: All data in eu-central-1, no PII in logs
- **DORA Art 11**: 100% request audit logging on API layer
- **EU AI Act**: Model cards required for anomaly-detector + grandmaster-service

## Commit Format

```
<type>(<scope>): <subject>

Types: feat, fix, docs, test, refactor, chore
Scope: service name (e.g. beneish-calculator, api-gateway)
```

## Port Assignment

See `.ai/context/repository.json` for full port registry. Never reuse a port.
