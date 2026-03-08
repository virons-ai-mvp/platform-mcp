# virons-services — Project Reference

**Repo**: virons-services | **Type**: Microservices monorepo | **Cluster**: virons-mvp (EKS 1.31)
**Region**: eu-central-1 | **Compliance**: BaFin MaRisk AT 8.1, GDPR Art 32, DORA Art 11, EU AI Act

## Critical Rules (Non-Negotiable)

| Rule | Requirement |
|---|---|
| **TDD** | **Write tests FIRST, then code to pass tests. See `docs/TESTING-STRATEGY.md`** |
| **Coverage** | **95% minimum — unit + integration + comprehensive tests required** |
| BaFin AT 8.1 | `write_audit()` BEFORE `forensic_flags` — every forensic calculation |
| ML Gate | `gated_ml = ml_score if len(deterministic_flags) >= 1 else 0.0` |
| Nonlinear Fusion | `S' = 1 − ∏(1 − sᵢ)` |
| GDPR | All data in eu-central-1, 100% request audit logging on API layer |
| EU AI Act | anomaly-detector + grandmaster-service = high-risk AI, model card required |
| SHA-256 | Every ingested artifact hashed → stored in `ingestion_log` |
| Blockchain | Async write only — NEVER blocks forensic engine |
| Challenge Mode | <90 second pipeline SLA |

## Service Catalog

### virons-ingestion (Go 1.23)
| Service | Port | Status |
|---|---|---|
| corporate-filings | 9101 | template |
| financial-news | 9102 | planned |
| market-data | 9109 | planned |
| esg-sanctions | 9110 | planned |
| insider-behaviour | 9117 | planned |

### virons-forensic (Python 3.12)
| Service | Port | Status |
|---|---|---|
| bedrock-gateway | 9300 | planned |
| graph-query-service | 9301 | planned |
| cache-service | 9303 | planned |
| beneish-calculator | 9401 | template |
| altman-calculator | 9402 | planned |
| qoe-analyser | 9403 | planned |
| narrative-nlp | 9404 | planned |
| anomaly-detector | 9405 | planned |
| governance-detector | 9406 | planned |
| risk-scorer | 9409 | planned |
| retrospective-validator | 9410 | planned |
| challenge-mode-service | 9411 | planned |
| false-positive-registry | 9412 | planned |
| regulatory-dossier | 9413 | planned |
| person-network-service | 9414 | planned |
| explode-mode-service | 9415 | planned |

### virons-ml (Python 3.12)
| Service | Port | Status |
|---|---|---|
| phase-classifier | 9420 | planned |
| grandmaster-service | 9421 | planned |
| scenario-watch-service | 9422 | planned |
| grandmaster-alert-engine | 9423 | planned |
| scenario-calibration | 9424 | planned |

### virons-blockchain (Go 1.23)
| Service | Port | Status |
|---|---|---|
| forensic-ledger-service | 9430 | planned |
| report-notarizer | 9431 | planned |
| integrity-verifier | 9432 | planned |

### virons-api (Go 1.23 + Next.js 15)
| Service | Port | Status |
|---|---|---|
| api-gateway | 8000 | planned |
| rest-api | 8001 | planned |
| websocket-api | 8002 | planned |
| investor-dashboard | 6001 | planned |
| guided-demo-mode | 6002 | planned |

## AWS Coordinates

- **Account**: virons-management (412179655775)
- **Profile**: `virons-management`
- **ECR**: `412179655775.dkr.ecr.eu-central-1.amazonaws.com/virons`
- **Bedrock**: eu-central-1, Nova Pro (`amazon.nova-pro-v1:0`)
- **Cluster**: `virons-mvp` (EKS 1.31, eu-central-1)
- **Node Groups**: ng-general (m6i.large Spot), ng-inference (m6i.xlarge On-Demand)
- **ArgoCD**: app-of-apps pattern, `infra/k8s/argocd/`

## Quick Commands

```bash
make help                              # all commands
make dev                               # start local dev stack (Docker Compose)
make test                              # run all tests
make lint                              # golangci-lint + ruff + black
make security-scan                     # trivy + gosec + bandit + gitleaks
make new-service NAME=x NS=y LANG=z   # scaffold new service
make compliance-check SERVICE=x       # BaFin/EU AI Act validation
```

## Shared Packages

- **Python**: `from virons_common import write_audit, get_logger, setup_metrics`
- **Go**: `import "virons/internal/logging"` | `"virons/internal/metrics"` | `"virons/internal/health"`

## Demo Environment

- URL: `demo.virons.ai` (always-on)
- Redis: pre-warmed with synthetic data
- Demo lock: toggle via `guided-demo-mode` service (:6002)
- Challenge Mode: <90s SLA enforced
