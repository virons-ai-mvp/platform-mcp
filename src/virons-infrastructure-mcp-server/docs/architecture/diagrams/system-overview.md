# System Overview Diagram

## High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        AI[AI Agent/LLM]
        CLI[CLI Client]
        API_CLIENT[REST API Client]
    end

    subgraph "API Layer"
        MCP[MCP Server<br/>stdio]
        HTTP[Health Server<br/>:8080]
        REST[FastAPI<br/>Swagger UI]
    end

    subgraph "Application Layer"
        DEPLOY[DeployService]
        LIST[ListService]
        DESTROY[DestroyService]
    end

    subgraph "Domain Layer"
        REGISTRY[UpstreamRegistry]
        MODELS[Domain Models]
    end

    subgraph "Infrastructure Layer"
        HEALTH[HealthChecker]
        METRICS[MetricsCollector]
        COMPLIANCE[ComplianceLogging]
    end

    subgraph "Upstream MCP Servers"
        CDK[AWS CDK<br/>:9140]
        CFN[CloudFormation<br/>:9141]
        TF[Terraform<br/>:9142]
        IAC[IaC<br/>:9143]
    end

    subgraph "Observability"
        PROM[Prometheus]
        LOGS[Audit Logs<br/>10-year retention]
    end

    AI -->|JSON-RPC| MCP
    CLI -->|stdio| MCP
    API_CLIENT -->|HTTP| REST

    MCP --> DEPLOY
    HTTP --> HEALTH
    REST --> DEPLOY
    REST --> LIST
    REST --> DESTROY

    DEPLOY --> REGISTRY
    LIST --> REGISTRY
    DESTROY --> REGISTRY

    DEPLOY --> COMPLIANCE
    DESTROY --> COMPLIANCE

    REGISTRY --> CDK
    REGISTRY --> CFN
    REGISTRY --> TF
    REGISTRY --> IAC

    HEALTH --> METRICS
    METRICS --> PROM
    COMPLIANCE --> LOGS

    style MCP fill:#e1f5ff
    style REST fill:#e1f5ff
    style COMPLIANCE fill:#ffe1e1
    style LOGS fill:#ffe1e1
```

## Component Responsibilities

### Client Layer
- **AI Agent/LLM**: Autonomous infrastructure management
- **CLI Client**: Human operators
- **REST API Client**: External systems integration

### API Layer
- **MCP Server**: Model Context Protocol (stdio)
- **Health Server**: Kubernetes probes
- **FastAPI**: REST API with Swagger UI

### Application Layer
- **DeployService**: Infrastructure deployment orchestration
- **ListService**: Stack listing and discovery
- **DestroyService**: Infrastructure destruction with confirmation

### Domain Layer
- **UpstreamRegistry**: MCP server registry and routing
- **Domain Models**: Business logic and validation

### Infrastructure Layer
- **HealthChecker**: Liveness and readiness probes
- **MetricsCollector**: Prometheus metrics
- **ComplianceLogging**: BaFin audit trails

### Upstream Servers
- **AWS CDK**: Cloud Development Kit
- **CloudFormation**: AWS native IaC
- **Terraform**: Multi-cloud IaC
- **IaC**: Generic infrastructure as code

## Data Flow

### Deploy Infrastructure
```
Client → API Layer → DeployService → ComplianceLogging (calculation_audit)
                                   → UpstreamRegistry → Upstream MCP Server
                                   → ComplianceLogging (write_audit)
                                   → MetricsCollector
                                   → Response
```

### Destroy Infrastructure
```
Client → API Layer → DestroyService → Validation (confirmation)
                                    → ComplianceLogging (calculation_audit)
                                    → UpstreamRegistry → Upstream MCP Server
                                    → ComplianceLogging (write_audit)
                                    → MetricsCollector
                                    → Response
```

## Compliance Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Compliance
    participant Upstream
    participant AuditLog

    Client->>API: deploy_infrastructure
    API->>Service: process request
    Service->>Compliance: log_tool_call_start()
    Service->>Compliance: log_calculation_audit()
    Service->>Upstream: execute deployment
    Upstream-->>Service: result
    Service->>Compliance: log_write_audit()
    Compliance->>AuditLog: store (10-year retention)
    Service->>Compliance: log_tool_call_end()
    Service-->>API: response
    API-->>Client: result
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API | FastAPI | REST API with Swagger |
| API | FastMCP | MCP protocol server |
| Application | Python 3.13 | Service layer |
| Domain | Pydantic | Data validation |
| Infrastructure | Prometheus | Metrics collection |
| Infrastructure | Loguru | Structured logging |
| Deployment | Docker | Containerization |
| Deployment | Kubernetes | Orchestration |
| Deployment | Helm | Package management |

## Network Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 8080 | HTTP | Health checks, metrics, REST API |
| stdin/stdout | stdio | MCP protocol |
| 9140 | stdio | AWS CDK upstream |
| 9141 | stdio | CloudFormation upstream |
| 9142 | stdio | Terraform upstream |
| 9143 | stdio | IaC upstream |

## Security Boundaries

```mermaid
graph LR
    subgraph "Public"
        CLIENT[Clients]
    end

    subgraph "DMZ"
        API[API Layer<br/>TLS 1.3]
    end

    subgraph "Application"
        SERVICES[Services<br/>Internal]
    end

    subgraph "Data"
        LOGS[Audit Logs<br/>Encrypted]
    end

    CLIENT -->|HTTPS| API
    API -->|Internal| SERVICES
    SERVICES -->|Encrypted| LOGS
```

## Deployment Architecture

See [deployment.md](deployment.md) for detailed deployment architecture.
