<link rel="stylesheet" href="../../../../platform-resources/styles/virons-markdown.css">

# AWS MCP Server Integration Backlog

**Status**: 📋 Backlog
**Date**: 2026-03-05
**Purpose**: Document Tier 2 and Tier 3 servers for future integration phases

***

## Overview

This document tracks 33 AWS MCP servers not included in Tier 1 (Core) integration. Tier 2 servers (25) are candidates for Phase 2 integration, while Tier 3 servers (8) are archived for future consideration.

***

## Tier 2: Extended Integration (25 Servers)

### Infrastructure & Development (6 Servers)

| Server | Score | Use Case | Integration Estimate | Proposed Context |
|--------|-------|----------|---------------------|------------------|
| **aws-serverless-mcp-server** | 39 | SAM deployment, serverless patterns | M (2 weeks) | Infrastructure (9145) |
| **aws-api-mcp-server** | 37 | Generic AWS API access, service exploration | S (1 week) | Infrastructure (9146) |
| **git-repo-research-mcp-server** | 33 | Code analysis, repository insights | M (2 weeks) | Governance (9112) |
| **openapi-mcp-server** | 32 | API spec management, code generation | M (2 weeks) | Infrastructure (9147) |
| **aws-diagram-mcp-server** | 31 | Architecture visualization, documentation | S (1 week) | Infrastructure (9148) |
| **code-doc-gen-mcp-server** | 28 | Automated documentation, code analysis | M (2 weeks) | Governance (9113) |

**Rationale**: Useful for development workflows, but not critical for compliance or operations. SAM and OpenAPI support serverless/API development. Git research and code documentation support governance and code quality.

**Integration Priority**: Q1 2027 (after Tier 1 complete)

***

### Data Services (4 Servers)

| Server | Score | Use Case | Integration Estimate | Proposed Context |
|--------|-------|----------|---------------------|------------------|
| **valkey-mcp-server** | 38 | Valkey operations, caching | S (1 week) | Data-NoSQL (9186) |
| **memcached-mcp-server** | 35 | Memcached caching, simple key-value | S (1 week) | Data-NoSQL (9187) |
| **timestream-for-influxdb-mcp-server** | 35 | Time-series data, metrics storage | M (2 weeks) | Data-NoSQL (9188) |
| **aws-dataprocessing-mcp-server** | 35 | ETL operations, data transformation | M (2 weeks) | Data-Relational (9154) |

**Rationale**: Additional caching and time-series options. Valkey/Memcached complement ElastiCache. Timestream useful for IoT/metrics. Data processing supports ETL pipelines.

**Integration Priority**: Q2 2027 (if caching/time-series needs arise)

***

### AI/ML (4 Servers)

| Server | Score | Use Case | Integration Estimate | Proposed Context |
|--------|-------|----------|---------------------|------------------|
| **amazon-bedrock-agentcore-mcp-server** | 37 | Agent orchestration, AI workflows | M (2 weeks) | AI-ML (9163) |
| **aws-bedrock-data-automation-mcp-server** | 34 | Automated data processing, document understanding | M (2 weeks) | AI-ML (9164) |
| **aws-bedrock-custom-model-import-mcp-server** | 34 | Custom model import, fine-tuning | M (2 weeks) | AI-ML (9165) |
| **nova-canvas-mcp-server** | 22 | Image generation, style transfer | S (1 week) | AI-ML (9166) |

**Rationale**: Advanced Bedrock features for agent orchestration and custom models. Nova Canvas for image generation (limited fintech use). Useful if AI/ML capabilities expand beyond SageMaker.

**Integration Priority**: Q3 2027 (if advanced AI/ML features needed)

***

### Messaging & Integration (2 Servers)

| Server | Score | Use Case | Integration Estimate | Proposed Context |
|--------|-------|----------|---------------------|------------------|
| **amazon-mq-mcp-server** | 39 | Message broker, queue management | M (2 weeks) | Messaging (9172) |
| **aws-appsync-mcp-server** | 36 | GraphQL API, real-time subscriptions | M (2 weeks) | Messaging (9173) |

**Rationale**: Amazon MQ provides traditional message broker (ActiveMQ/RabbitMQ). AppSync enables GraphQL APIs with real-time subscriptions. Useful if messaging patterns expand beyond SNS/SQS/MSK.

**Integration Priority**: Q4 2027 (if additional messaging patterns needed)

***

### Utilities (9 Servers)

| Server | Score | Use Case | Integration Estimate | Proposed Context |
|--------|-------|----------|---------------------|------------------|
| **aws-support-mcp-server** | 30 | Support case management, Trusted Advisor | S (1 week) | Operations (9125) |
| **syntheticdata-mcp-server** | 34 | Test data generation (GDPR Art 25) | M (2 weeks) | Compliance (9133) |
| **aws-documentation-mcp-server** | 26 | AWS docs retrieval, reference | S (1 week) | Governance (9114) |
| **aws-knowledge-mcp-server** | 25 | Knowledge base, troubleshooting guides | S (1 week) | Governance (9115) |
| **document-loader-mcp-server** | 22 | Document parsing, text extraction | S (1 week) | AI-ML (9167) |
| **finch-mcp-server** | 22 | Container runtime, local development | S (1 week) | Infrastructure (9149) |
| **core-mcp-server** | 22 | Core MCP utilities, foundational | S (1 week) | Infrastructure (9145) |
| **mcp-lambda-handler** | 31 | Lambda MCP deployment | M (2 weeks) | Infrastructure (9146) |
| **sagemaker-unified-studio-spark-upgrade-mcp-server** | 22 | Spark version management | S (1 week) | AI-ML (9168) |
| **sagemaker-unified-studio-spark-troubleshooting-mcp-server** | 23 | Spark job debugging | S (1 week) | AI-ML (9169) |

**Rationale**: Support utilities for documentation, testing, and troubleshooting. AWS Support for case management. Synthetic data for GDPR-compliant testing. Document loader for AI/ML pipelines. Finch for local container development. SageMaker Spark tools for Spark workloads.

**Integration Priority**: Q1-Q2 2027 (as needed for specific use cases)

***

## Tier 3: Future Consideration (8 Servers)

### Healthcare Servers (3 Servers) - Score: 20 each

| Server | Score | Rationale | Future Use Case |
|--------|-------|-----------|-----------------|
| **aws-healthomics-mcp-server** | 20 | Genomics workflows, not fintech-relevant | If expanding to health-tech vertical |
| **healthlake-mcp-server** | 20 | FHIR healthcare data, not fintech-relevant | If expanding to health-tech vertical |
| **healthimaging-mcp-server** | 20 | Medical imaging (DICOM), not fintech-relevant | If expanding to health-tech vertical |

**Archive Reason**: Healthcare-specific servers with no current fintech use case. GDPR Art 32 compliance for health data, but not applicable to financial services platform.

**Future Consideration**: If Virons expands to health-tech vertical or partners with healthcare providers.

***

### IoT & Location (2 Servers)

| Server | Score | Rationale | Future Use Case |
|--------|-------|-----------|-----------------|
| **aws-iot-sitewise-mcp-server** | 20 | Industrial IoT, not fintech-relevant | If expanding to IoT/industrial vertical |
| **aws-location-mcp-server** | 19 | Geolocation services, limited fintech use | If adding location-based fraud detection |

**Archive Reason**: IoT SiteWise targets industrial use cases (manufacturing, energy). Location Service has limited fintech applications (branch locator, ATM finder).

**Future Consideration**: Location Service could support fraud detection (geolocation anomalies), branch/ATM services.

***

### Niche Services (3 Servers)

| Server | Score | Rationale | Future Use Case |
|--------|-------|-----------|-----------------|
| **frontend-mcp-server** | 19 | Frontend tooling, not backend-focused | If adding frontend development support |
| **ccapi-mcp-server** | 15 | Cryptocurrency API, niche use case | If adding crypto trading features |
| **amazon-qbusiness-anonymous-mcp-server** | 19 | Q Business anonymous mode, limited use | If adding Q Business integration |
| **amazon-qindex-mcp-server** | 19 | Q index management, limited use | If adding Q Business integration |
| **aws-pricing-mcp-server** | 19 | Pricing lookup, limited operational value | If building cost estimation tools |

**Archive Reason**:
- Frontend MCP: Platform is backend-focused (virons-services)
- CCAPI: Cryptocurrency not core to fintech platform (blockchain is)
- Q Business: Limited use case without Q Business adoption
- Pricing: Cost Explorer provides sufficient cost management

**Future Consideration**:
- CCAPI if expanding to crypto trading
- Q Business if adopting Amazon Q for enterprise search
- Pricing if building customer-facing cost estimation tools

***

## Proposed New Contexts for Tier 2

To accommodate Tier 2 servers without exceeding 10 ports per context:

### Utilities Context (9200-9209) **NEW**

| Port | Server | Purpose |
|------|--------|---------|
| 9200 | aws-support-mcp-server | Support case management |
| 9201 | aws-documentation-mcp-server | AWS docs retrieval |
| 9202 | aws-knowledge-mcp-server | Knowledge base |
| 9203 | syntheticdata-mcp-server | Test data generation |
| 9204-9209 | *Reserved* | Future utility servers |

***

## Integration Roadmap

### Phase 1: Tier 1 Core (Q2-Q4 2026) - 33 Servers
- **Q2 2026**: Security, Compliance, Monitoring (10 servers)
- **Q3 2026**: Operations, Infrastructure, Data-Relational (13 servers)
- **Q4 2026**: Data-NoSQL, AI-ML, Messaging (10 servers)

### Phase 2: Tier 2 Extended (Q1-Q4 2027) - 25 Servers
- **Q1 2027**: Infrastructure & Development (6 servers)
- **Q2 2027**: Data Services (4 servers)
- **Q3 2027**: AI/ML (4 servers)
- **Q4 2027**: Messaging & Utilities (11 servers)

### Phase 3: Tier 3 Evaluation (2028+)
- **Q1 2028**: Re-evaluate healthcare servers if health-tech expansion
- **Q2 2028**: Re-evaluate IoT/Location if use cases emerge
- **Q3 2028**: Re-evaluate niche services based on platform evolution

***

## Decision Criteria for Tier 2 Promotion

A Tier 2 server can be promoted to immediate integration if:

1. **Compliance Requirement**: New regulation requires specific capability
2. **Platform Need**: Virons-services requires specific AWS service
3. **Operational Gap**: Monitoring/troubleshooting gap identified
4. **Customer Request**: Enterprise customer requires specific integration
5. **Score Increase**: Re-scoring shows score ≥ 40 due to new use case

***

## Effort Estimates

### Integration Effort by Size
- **S (Small)**: 1 week - Simple server, minimal configuration, basic testing
- **M (Medium)**: 2 weeks - Complex server, IAM policies, integration testing, runbooks
- **L (Large)**: 4 weeks - Very complex, multiple dependencies, extensive testing, compliance docs

### Tier 2 Total Effort
- Small (S): 11 servers × 1 week = 11 weeks
- Medium (M): 14 servers × 2 weeks = 28 weeks
- **Total**: 39 weeks (~9 months) for all Tier 2 servers

### Recommended Approach
- Parallel integration: 2-3 servers at a time
- Actual timeline: Q1-Q4 2027 (12 months with buffer)

***

## Monitoring and Review

### Quarterly Review Process
1. **Review Tier 2 Backlog**: Assess if any servers should be promoted
2. **Evaluate Tier 3 Archive**: Check if archived servers now relevant
3. **Update Scores**: Re-score based on new platform requirements
4. **Adjust Roadmap**: Update integration timeline based on priorities

### Triggers for Re-Evaluation
- New compliance regulation announced
- Platform architecture change (e.g., adding crypto trading)
- Customer feedback on missing capabilities
- AWS service updates or new features
- Virons business model pivot (e.g., health-tech expansion)

***

## Metadata

- **Document Owner**: Platform Architecture Team
- **Last Updated**: 2026-03-05
- **Next Review**: 2026-06-05 (Quarterly)
- **Related**: [Server Scores](SERVER-SCORES.md), [ADR-002](../decisions/ADR-002-aws-mcp-integration.md), [Context Mapping](CONTEXT-MAPPING.md)
