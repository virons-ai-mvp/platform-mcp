# Service Development Workflow

## New Service Checklist

Use `/new-service` command to scaffold. Manual steps:

### 1. Port Assignment
Check `.ai/context/repository.json` — never reuse a port.

### 2. Scaffold Structure
```
{namespace}/{service-name}/
├── cmd/main.go          (Go) or main.py (Python)
├── internal/            (Go) or src/ (Python)
│   ├── handler/
│   ├── service/
│   └── repository/
├── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── README.md
```

### 3. Dockerfile Requirements
```dockerfile
FROM golang:1.23-alpine AS builder  # or python:3.12-slim
# ... build steps ...
FROM alpine:3.19  # or distroless/python3
RUN addgroup -S virons && adduser -S virons -G virons
USER virons
EXPOSE {port}
```

### 4. K8s Manifest Requirements
```yaml
spec:
  template:
    spec:
      serviceAccountName: {service}-sa  # IRSA
      securityContext:
        runAsNonRoot: true
        readOnlyRootFilesystem: true
      containers:
        - resources:
            requests: {cpu: "100m", memory: "128Mi"}
            limits: {cpu: "500m", memory: "512Mi"}
          livenessProbe: {httpGet: {path: /health}}
          readinessProbe: {httpGet: {path: /ready}}
```

### 5. Health Endpoints (Mandatory)
- `GET /health` → 200 OK `{"status": "ok"}`
- `GET /ready` → 200 OK when dependencies ready
- `GET /metrics` → Prometheus metrics

### 6. TDD Cycle
1. Write failing test
2. Implement minimal code
3. Pass test
4. Refactor
5. Commit: `feat({service}): add {feature}`

### 7. Compliance Gate
Run before PR:
```bash
/compliance-audit {namespace}/{service}
```
