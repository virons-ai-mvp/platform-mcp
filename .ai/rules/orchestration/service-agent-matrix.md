# Service → Agent Matrix

Maps all 42 services to their primary agent(s).

## ingestion (Go 1.23)

| Service | Port | Primary Agent | Secondary |
|---|---|---|---|
| corporate-filings | 9101 | go-backend-engineer | devops-engineer |
| financial-news | 9102 | go-backend-engineer | devops-engineer |
| market-data | 9109 | go-backend-engineer | devops-engineer |
| esg-sanctions | 9110 | go-backend-engineer | compliance-validator |
| insider-behaviour | 9117 | go-backend-engineer | compliance-validator |

## forensic (Python 3.12)

| Service | Port | Primary Agent | Secondary |
|---|---|---|---|
| bedrock-gateway | 9300 | python-backend-engineer | devops-engineer |
| graph-query-service | 9301 | python-backend-engineer | — |
| cache-service | 9303 | python-backend-engineer | — |
| beneish-calculator | 9401 | python-backend-engineer | compliance-validator |
| altman-calculator | 9402 | python-backend-engineer | compliance-validator |
| qoe-analyser | 9403 | python-backend-engineer | compliance-validator |
| narrative-nlp | 9404 | python-backend-engineer | ml-engineer |
| anomaly-detector | 9405 | ml-engineer | compliance-validator |
| governance-detector | 9406 | python-backend-engineer | compliance-validator |
| risk-scorer | 9409 | python-backend-engineer | compliance-validator |
| retrospective-validator | 9410 | python-backend-engineer | compliance-validator |
| challenge-mode-service | 9411 | python-backend-engineer | — |
| false-positive-registry | 9412 | python-backend-engineer | compliance-validator |
| regulatory-dossier | 9413 | python-backend-engineer | compliance-validator |
| person-network-service | 9414 | python-backend-engineer | — |
| explode-mode-service | 9415 | python-backend-engineer | — |

## ml (Python 3.12) — EU AI Act High-Risk

| Service | Port | Primary Agent | Secondary |
|---|---|---|---|
| phase-classifier | 9420 | ml-engineer | compliance-validator |
| grandmaster-service | 9421 | ml-engineer | compliance-validator |
| scenario-watch-service | 9422 | ml-engineer | — |
| grandmaster-alert-engine | 9423 | ml-engineer | — |
| scenario-calibration | 9424 | ml-engineer | — |

## blockchain (Go 1.23)

| Service | Port | Primary Agent | Secondary |
|---|---|---|---|
| forensic-ledger-service | 9430 | go-backend-engineer | compliance-validator |
| report-notarizer | 9431 | go-backend-engineer | compliance-validator |
| integrity-verifier | 9432 | go-backend-engineer | security-auditor |

## api (Go 1.23 + Next.js 15)

| Service | Port | Primary Agent | Secondary |
|---|---|---|---|
| api-gateway | 8000 | go-backend-engineer | security-auditor |
| rest-api | 8001 | go-backend-engineer | compliance-validator |
| websocket-api | 8002 | go-backend-engineer | — |
| investor-dashboard | 6001 | go-backend-engineer | — |
| guided-demo-mode | 6002 | go-backend-engineer | — |

## Cross-Cutting Concerns

| Concern | Agent |
|---|---|
| K8s manifests (all services) | devops-engineer |
| Dockerfiles (all services) | devops-engineer |
| Security scans (all services) | security-auditor |
| BaFin/GDPR/DORA audits | compliance-validator |
| EU AI Act (anomaly-detector, grandmaster-service) | ml-engineer + compliance-validator |
| New service scaffolding | service-scaffolder |
