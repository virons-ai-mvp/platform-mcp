<link rel="stylesheet" href="../../../../platform-resources/styles/virons-markdown.css">

# AWS MCP Server Scores

**Status**: ✅ Complete  
**Date**: 2026-03-05  
**Purpose**: Scored evaluation of all 67 AWS MCP servers for integration prioritization

***

## Scoring Summary

- **Tier 1 (Core)**: 28 servers (Score ≥ 40) - Immediate integration
- **Tier 2 (Extended)**: 24 servers (Score 20-39) - Phase 2 integration
- **Tier 3 (Future)**: 15 servers (Score < 20) - Archive for future

***

## Tier 1: Core Integration (Score ≥ 40)

### Security & Compliance Context

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **cloudtrail-mcp-server** | 10 (30) | 9 (18) | 10 (20) | 3 (3) | **71** | Critical for audit trail (BaFin AT 8.1), forensic analysis, security investigations |
| **iam-mcp-server** | 10 (30) | 7 (14) | 6 (12) | 5 (5) | **61** | Essential for access control (BaFin, GDPR), policy management, security simulation |
| **well-architected-security-mcp-server** | 9 (27) | 8 (16) | 5 (10) | 3 (3) | **56** | Security posture assessment, compliance monitoring, GuardDuty/Security Hub integration |

### Monitoring & Observability Context

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **cloudwatch-mcp-server** | 8 (24) | 10 (20) | 7 (14) | 4 (4) | **62** | Critical for incident response, alarm troubleshooting, log analysis, DORA Art 11 |
| **prometheus-mcp-server** | 6 (18) | 9 (18) | 6 (12) | 3 (3) | **51** | Time-series metrics, PromQL queries, operational monitoring |
| **cloudwatch-appsignals-mcp-server** | 7 (21) | 8 (16) | 6 (12) | 3 (3) | **52** | Service-level monitoring, SLO tracking, distributed tracing |

### Operations Context

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **eks-mcp-server** | 5 (15) | 8 (16) | 7 (14) | 9 (9) | **54** | Container orchestration, cluster management, deployment automation |
| **lambda-tool-mcp-server** | 4 (12) | 7 (14) | 7 (14) | 8 (8) | **48** | Serverless compute, function management, event-driven architecture |
| **ecs-mcp-server** | 4 (12) | 7 (14) | 6 (12) | 8 (8) | **46** | Container orchestration, task/service management |
| **stepfunctions-tool-mcp-server** | 5 (15) | 6 (12) | 6 (12) | 7 (7) | **46** | Workflow orchestration, state machine execution, DORA resilience |

### Compliance Context

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **cost-explorer-mcp-server** | 6 (18) | 7 (14) | 4 (8) | 3 (3) | **43** | Cost transparency (BaFin AT 8.1), anomaly detection, forecasting |
| **billing-cost-management-mcp-server** | 6 (18) | 6 (12) | 4 (8) | 3 (3) | **41** | Financial controls (BaFin), budget management, cost allocation |

### Infrastructure Context (New: 9140-9149)

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **cdk-mcp-server** | 7 (21) | 5 (10) | 6 (12) | 10 (10) | **53** | IaC deployment (GDPR Art 25), infrastructure by design, CDK synthesis |
| **cfn-mcp-server** | 7 (21) | 6 (12) | 6 (12) | 9 (9) | **54** | CloudFormation stacks, template validation, drift detection |
| **terraform-mcp-server** | 7 (21) | 5 (10) | 6 (12) | 9 (9) | **52** | Multi-cloud IaC, state management, Terraform operations |
| **aws-iac-mcp-server** | 6 (18) | 5 (10) | 5 (10) | 8 (8) | **46** | General IaC operations, template generation |
| **aws-network-mcp-server** | 7 (21) | 6 (12) | 5 (10) | 6 (6) | **49** | VPC management (GDPR Art 32), network security, DORA resilience |

### Data Services Context (New: 9150-9159)

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **postgres-mcp-server** | 8 (24) | 6 (12) | 9 (18) | 5 (5) | **59** | Audit log storage (BaFin AT 8.1), forensic data, GDPR Art 32 encryption |
| **dynamodb-mcp-server** | 7 (21) | 6 (12) | 9 (18) | 6 (6) | **57** | Transaction data, forensic analysis, high-performance NoSQL |
| **redshift-mcp-server** | 7 (21) | 5 (10) | 8 (16) | 5 (5) | **52** | Data warehouse, forensic analytics (BaFin), ML feature store |
| **mysql-mcp-server** | 7 (21) | 5 (10) | 8 (16) | 5 (5) | **52** | Relational data, audit logs, GDPR Art 32 compliance |
| **aurora-dsql-mcp-server** | 7 (21) | 6 (12) | 8 (16) | 5 (5) | **54** | Distributed SQL, high availability, forensic data storage |

### AI/ML Context (New: 9160-9169)

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **sagemaker-ai-mcp-server** | 5 (15) | 6 (12) | 10 (20) | 7 (7) | **54** | ML training/inference (:9420-9424), model deployment, feature engineering |
| **bedrock-kb-retrieval-mcp-server** | 4 (12) | 5 (10) | 9 (18) | 6 (6) | **46** | RAG for forensic analysis, semantic search, document retrieval |
| **amazon-kendra-index-mcp-server** | 4 (12) | 5 (10) | 8 (16) | 6 (6) | **44** | Intelligent search, document indexing, knowledge retrieval |

### Messaging Context (New: 9170-9179)

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **amazon-sns-sqs-mcp-server** | 5 (15) | 7 (14) | 7 (14) | 6 (6) | **49** | Event-driven architecture, async messaging, decoupling |
| **aws-msk-mcp-server** | 5 (15) | 7 (14) | 7 (14) | 6 (6) | **49** | Kafka streaming, event sourcing, real-time data pipelines |

***

## Tier 2: Extended Integration (Score 20-39)

### Infrastructure & Development

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **aws-serverless-mcp-server** | 4 (12) | 5 (10) | 5 (10) | 7 (7) | **39** | SAM deployment, serverless patterns |
| **aws-api-mcp-server** | 3 (9) | 6 (12) | 5 (10) | 6 (6) | **37** | Generic AWS API access, service exploration |
| **git-repo-research-mcp-server** | 3 (9) | 4 (8) | 4 (8) | 8 (8) | **33** | Code analysis, repository insights |
| **openapi-mcp-server** | 3 (9) | 4 (8) | 4 (8) | 7 (7) | **32** | API spec management, code generation |
| **aws-diagram-mcp-server** | 3 (9) | 4 (8) | 4 (8) | 6 (6) | **31** | Architecture visualization, documentation |
| **code-doc-gen-mcp-server** | 3 (9) | 3 (6) | 3 (6) | 7 (7) | **28** | Automated documentation, code analysis |

### Data Services

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **s3-tables-mcp-server** | 6 (18) | 4 (8) | 6 (12) | 4 (4) | **42** | Iceberg tables, data lake, analytics (just above Tier 1 threshold) |
| **amazon-neptune-mcp-server** | 6 (18) | 4 (8) | 6 (12) | 4 (4) | **42** | Graph database, relationship analysis (just above Tier 1 threshold) |
| **documentdb-mcp-server** | 6 (18) | 4 (8) | 5 (10) | 4 (4) | **40** | MongoDB-compatible, document storage (borderline Tier 1) |
| **amazon-keyspaces-mcp-server** | 6 (18) | 4 (8) | 5 (10) | 4 (4) | **40** | Cassandra-compatible, wide-column store (borderline Tier 1) |
| **elasticache-mcp-server** | 4 (12) | 6 (12) | 6 (12) | 4 (4) | **40** | Redis caching, session management (borderline Tier 1) |
| **valkey-mcp-server** | 4 (12) | 6 (12) | 5 (10) | 4 (4) | **38** | Valkey operations, caching |
| **memcached-mcp-server** | 4 (12) | 5 (10) | 5 (10) | 3 (3) | **35** | Memcached caching, simple key-value |
| **timestream-for-influxdb-mcp-server** | 4 (12) | 5 (10) | 5 (10) | 3 (3) | **35** | Time-series data, metrics storage |

### AI/ML

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **amazon-bedrock-agentcore-mcp-server** | 3 (9) | 4 (8) | 7 (14) | 6 (6) | **37** | Agent orchestration, AI workflows |
| **aws-bedrock-data-automation-mcp-server** | 3 (9) | 4 (8) | 6 (12) | 5 (5) | **34** | Automated data processing, document understanding |
| **aws-bedrock-custom-model-import-mcp-server** | 3 (9) | 3 (6) | 7 (14) | 5 (5) | **34** | Custom model import, fine-tuning |
| **nova-canvas-mcp-server** | 2 (6) | 2 (4) | 4 (8) | 4 (4) | **22** | Image generation, limited fintech use |

### Messaging & Integration

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **amazon-mq-mcp-server** | 4 (12) | 6 (12) | 5 (10) | 5 (5) | **39** | Message broker, queue management |
| **aws-appsync-mcp-server** | 3 (9) | 5 (10) | 5 (10) | 7 (7) | **36** | GraphQL API, real-time subscriptions |

### Monitoring & Observability

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **cloudwatch-applicationsignals-mcp-server** | 6 (18) | 7 (14) | 5 (10) | 3 (3) | **45** | Application monitoring (actually Tier 1, reclassify) |

### Utilities

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **aws-documentation-mcp-server** | 2 (6) | 4 (8) | 3 (6) | 6 (6) | **26** | AWS docs retrieval, reference |
| **aws-knowledge-mcp-server** | 2 (6) | 4 (8) | 3 (6) | 5 (5) | **25** | Knowledge base, troubleshooting guides |
| **aws-support-mcp-server** | 4 (12) | 5 (10) | 3 (6) | 2 (2) | **30** | Support case management, Trusted Advisor |
| **syntheticdata-mcp-server** | 5 (15) | 3 (6) | 4 (8) | 5 (5) | **34** | Test data generation (GDPR Art 25) |

***

## Tier 3: Future Consideration (Score < 20)

### Specialized Domains (Limited Fintech Relevance)

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **aws-healthomics-mcp-server** | 4 (12) | 2 (4) | 1 (2) | 2 (2) | **20** | Genomics, not fintech-relevant (borderline) |
| **healthlake-mcp-server** | 4 (12) | 2 (4) | 1 (2) | 2 (2) | **20** | FHIR healthcare, not fintech-relevant (borderline) |
| **healthimaging-mcp-server** | 4 (12) | 2 (4) | 1 (2) | 2 (2) | **20** | Medical imaging, not fintech-relevant (borderline) |
| **aws-iot-sitewise-mcp-server** | 3 (9) | 3 (6) | 1 (2) | 3 (3) | **20** | Industrial IoT, not fintech-relevant (borderline) |
| **aws-location-mcp-server** | 2 (6) | 3 (6) | 2 (4) | 3 (3) | **19** | Geolocation, limited fintech use |

### Development Utilities (Low Priority)

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **frontend-mcp-server** | 2 (6) | 2 (4) | 2 (4) | 5 (5) | **19** | Frontend tooling, not backend-focused |
| **document-loader-mcp-server** | 2 (6) | 3 (6) | 3 (6) | 4 (4) | **22** | Document parsing, limited use (actually Tier 2, reclassify) |
| **finch-mcp-server** | 2 (6) | 3 (6) | 3 (6) | 5 (5) | **22** | Container runtime, local dev only (actually Tier 2, reclassify) |

### Niche Services

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **ccapi-mcp-server** | 1 (3) | 2 (4) | 3 (6) | 2 (2) | **15** | Cryptocurrency API, niche use case |
| **amazon-qbusiness-anonymous-mcp-server** | 2 (6) | 3 (6) | 2 (4) | 3 (3) | **19** | Q Business anonymous, limited use |
| **amazon-qindex-mcp-server** | 2 (6) | 3 (6) | 2 (4) | 3 (3) | **19** | Q index management, limited use |
| **aws-pricing-mcp-server** | 2 (6) | 3 (6) | 2 (4) | 3 (3) | **19** | Pricing lookup, limited operational value |

### SageMaker Specialized

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **sagemaker-unified-studio-spark-upgrade-mcp-server** | 2 (6) | 3 (6) | 3 (6) | 4 (4) | **22** | Spark upgrades, niche use (actually Tier 2, reclassify) |
| **sagemaker-unified-studio-spark-troubleshooting-mcp-server** | 2 (6) | 4 (8) | 3 (6) | 3 (3) | **23** | Spark troubleshooting, niche use (actually Tier 2, reclassify) |

### Platform Utilities

| Server | Compliance | Operational | Platform | Development | **Total** | Justification |
|--------|------------|-------------|----------|-------------|-----------|---------------|
| **core-mcp-server** | 2 (6) | 3 (6) | 3 (6) | 4 (4) | **22** | Core MCP utilities, foundational (actually Tier 2, reclassify) |
| **mcp-lambda-handler** | 3 (9) | 4 (8) | 4 (8) | 6 (6) | **31** | Lambda MCP deployment (actually Tier 2, reclassify) |
| **virons-common** | 8 (24) | 5 (10) | 8 (16) | 6 (6) | **56** | Virons shared utilities (actually Tier 1, already integrated) |
| **aws-dataprocessing-mcp-server** | 4 (12) | 4 (8) | 5 (10) | 5 (5) | **35** | ETL operations (actually Tier 2, reclassify) |

***

## Reclassifications After Review

### Move to Tier 1 (Score ≥ 40)
- **cloudwatch-applicationsignals-mcp-server** (45) - Application monitoring
- **s3-tables-mcp-server** (42) - Data lake, analytics
- **amazon-neptune-mcp-server** (42) - Graph analytics for fraud detection
- **documentdb-mcp-server** (40) - Document storage
- **amazon-keyspaces-mcp-server** (40) - Wide-column store
- **elasticache-mcp-server** (40) - Session management, caching

### Move to Tier 2 (Score 20-39)
- **document-loader-mcp-server** (22)
- **finch-mcp-server** (22)
- **sagemaker-unified-studio-spark-upgrade-mcp-server** (22)
- **sagemaker-unified-studio-spark-troubleshooting-mcp-server** (23)
- **core-mcp-server** (22)
- **mcp-lambda-handler** (31)
- **aws-dataprocessing-mcp-server** (35)

### Remain Tier 3 (Score < 20)
- Healthcare servers (HealthOmics, HealthLake, HealthImaging): 20 each
- **aws-iot-sitewise-mcp-server** (20)
- **aws-location-mcp-server** (19)
- **frontend-mcp-server** (19)
- **ccapi-mcp-server** (15)
- **amazon-qbusiness-anonymous-mcp-server** (19)
- **amazon-qindex-mcp-server** (19)
- **aws-pricing-mcp-server** (19)

***

## Final Tier Summary

### Tier 1 (Core): 34 Servers
- Security & Compliance: 3
- Monitoring & Observability: 4
- Operations: 4
- Compliance: 2
- Infrastructure: 5
- Data Services: 11
- AI/ML: 3
- Messaging: 2

### Tier 2 (Extended): 25 Servers
- Infrastructure & Development: 6
- Data Services: 4
- AI/ML: 4
- Messaging & Integration: 2
- Monitoring: 0
- Utilities: 9

### Tier 3 (Future): 8 Servers
- Specialized Domains: 5
- Development Utilities: 1
- Niche Services: 2

***

## Port Capacity Analysis

**Available Ports**: 34 (9102-9109, 9112-9119, 9121-9129, 9131-9139)  
**Tier 1 Servers**: 34  
**Status**: ✅ Exact fit! Need to expand to new contexts (9140-9179)

**Proposed New Contexts**:
- Infrastructure: 9140-9149 (5 servers)
- Data Services: 9150-9159 (11 servers - need 2 contexts!)
- AI/ML: 9160-9169 (3 servers)
- Messaging: 9170-9179 (2 servers)

**Revised Plan**: Split Data Services into two contexts
- Data Services (Relational): 9150-9159 (Postgres, MySQL, Aurora, Redshift)
- Data Services (NoSQL): 9180-9189 (DynamoDB, DocumentDB, Keyspaces, Neptune, ElastiCache, S3 Tables)

***

## Metadata

- **Document Owner**: Platform Architecture Team
- **Last Updated**: 2026-03-05
- **Next Review**: 2026-04-05
- **Related**: [Server Catalog](SERVER-CATALOG.md), [Scoring Framework](SCORING-FRAMEWORK.md), [Context Mapping](CONTEXT-MAPPING.md)
