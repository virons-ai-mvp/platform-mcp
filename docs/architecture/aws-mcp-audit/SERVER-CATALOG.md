<link rel="stylesheet" href="../../../../platform-resources/styles/virons-markdown.css">

# AWS MCP Server Catalog

**Status**: 📊 In Progress  
**Date**: 2026-03-05  
**Purpose**: Comprehensive inventory of AWS MCP servers for integration audit

***

## Overview

This catalog documents all 67 AWS MCP servers available in the platform-mcp repository. Each server is categorized by primary function and evaluated for potential integration into virons-mcp-server bounded contexts.

## Catalog Structure

- **Server Name**: Official package name
- **Category**: Primary functional category
- **Description**: Core purpose and capabilities
- **Key Features**: Main functionality highlights
- **Compliance Tags**: Relevant regulations (BaFin AT 8.1, GDPR, DORA)

***

## Security & Compliance Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **iam-mcp-server** | AWS IAM management for users, roles, policies | User/role/policy CRUD, policy simulation, access key management, permissions boundary | BaFin AT 8.1 (access control), GDPR Art 25 (data protection by design) |
| **cloudtrail-mcp-server** | CloudTrail event lookup and Lake analytics | Event lookup (90 days), SQL analytics, user activity tracking, API call monitoring | BaFin AT 8.1 (audit trail), GDPR Art 32 (security monitoring), DORA Art 11 (incident detection) |
| **well-architected-security-mcp-server** | Security posture assessment against AWS Well-Architected Framework | Security service monitoring (GuardDuty, Security Hub, Inspector), compliance assessment, resource discovery | BaFin AT 8.1 (security controls), DORA Art 11 (risk management) |

***

## Monitoring & Observability Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **cloudwatch-mcp-server** | CloudWatch metrics, logs, and alarms | Alarm troubleshooting, log analysis, metric retrieval, alarm recommendations | DORA Art 11 (operational resilience), BaFin AT 8.1 (monitoring) |
| **cloudwatch-appsignals-mcp-server** | CloudWatch Application Signals for service monitoring | Service-level metrics, SLO tracking, distributed tracing | DORA Art 11 (service monitoring) |
| **cloudwatch-applicationsignals-mcp-server** | CloudWatch Application Signals (alternate) | Application performance monitoring, service maps | DORA Art 11 (operational visibility) |
| **prometheus-mcp-server** | Prometheus metrics integration | Time-series metrics, PromQL queries, alerting | DORA Art 11 (monitoring) |

***

## Cost Management Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **cost-explorer-mcp-server** | AWS Cost Explorer analysis | Cost breakdown by service/region, cost comparison, forecasting, natural language queries | BaFin AT 8.1 (cost transparency) |
| **billing-cost-management-mcp-server** | AWS Billing and Cost Management | Billing data retrieval, cost allocation tags, budget management | BaFin AT 8.1 (financial controls) |
| **aws-pricing-mcp-server** | AWS service pricing information | Pricing lookup, cost estimation, service comparison | - |

***

## Infrastructure & Orchestration Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **eks-mcp-server** | Amazon EKS cluster management | Cluster creation, resource lifecycle, deployment, troubleshooting, log retrieval | DORA Art 11 (infrastructure resilience) |
| **ecs-mcp-server** | Amazon ECS container orchestration | Task/service management, container deployment, cluster operations | DORA Art 11 (container orchestration) |
| **lambda-tool-mcp-server** | AWS Lambda function management | Function invocation, deployment, configuration, testing | - |
| **stepfunctions-tool-mcp-server** | AWS Step Functions workflow orchestration | State machine execution, workflow monitoring, debugging | - |
| **cdk-mcp-server** | AWS CDK infrastructure as code | CDK app synthesis, deployment, stack management | GDPR Art 25 (infrastructure by design) |
| **cfn-mcp-server** | CloudFormation stack management | Stack CRUD, template validation, change sets, drift detection | GDPR Art 25 (infrastructure by design) |
| **terraform-mcp-server** | Terraform infrastructure as code | Terraform plan/apply, state management, module operations | GDPR Art 25 (infrastructure by design) |
| **aws-iac-mcp-server** | General AWS IaC operations | Multi-tool IaC support, template generation | GDPR Art 25 (infrastructure by design) |
| **aws-serverless-mcp-server** | AWS Serverless Application Model (SAM) | SAM template deployment, local testing, API Gateway integration | - |

***

## Data Services Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **postgres-mcp-server** | PostgreSQL database operations | Query execution, schema management, connection pooling | GDPR Art 32 (data security), BaFin AT 8.1 (data integrity) |
| **mysql-mcp-server** | MySQL database operations | Query execution, database administration, backup/restore | GDPR Art 32 (data security), BaFin AT 8.1 (data integrity) |
| **dynamodb-mcp-server** | Amazon DynamoDB NoSQL operations | Table CRUD, item operations, query/scan, GSI/LSI management | GDPR Art 32 (data security) |
| **aurora-dsql-mcp-server** | Amazon Aurora DSQL operations | Distributed SQL queries, Aurora-specific features | GDPR Art 32 (data security) |
| **redshift-mcp-server** | Amazon Redshift data warehouse | Query execution, cluster management, data loading | GDPR Art 32 (data security), BaFin AT 8.1 (data analytics) |
| **amazon-keyspaces-mcp-server** | Amazon Keyspaces (Cassandra) | CQL queries, table management, keyspace operations | GDPR Art 32 (data security) |
| **documentdb-mcp-server** | Amazon DocumentDB (MongoDB) | Document operations, collection management, aggregation | GDPR Art 32 (data security) |
| **amazon-neptune-mcp-server** | Amazon Neptune graph database | Graph queries (Gremlin/SPARQL), graph analytics | GDPR Art 32 (data security) |
| **timestream-for-influxdb-mcp-server** | Amazon Timestream for InfluxDB | Time-series data operations, InfluxQL queries | - |
| **s3-tables-mcp-server** | AWS S3 Tables (Apache Iceberg) | Table format operations, metadata management, query optimization | GDPR Art 32 (data security) |
| **elasticache-mcp-server** | Amazon ElastiCache (Redis) | Cache operations, cluster management, data structures | - |
| **memcached-mcp-server** | Amazon ElastiCache Memcached | Memcached operations, cache management | - |
| **valkey-mcp-server** | Amazon ElastiCache/MemoryDB Valkey | Valkey operations, data structures, pub/sub | - |

***

## AI/ML Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **amazon-bedrock-agentcore-mcp-server** | Amazon Bedrock agent orchestration | Agent creation, knowledge base integration, action groups | - |
| **bedrock-kb-retrieval-mcp-server** | Amazon Bedrock Knowledge Base retrieval | RAG operations, semantic search, document retrieval | - |
| **aws-bedrock-data-automation-mcp-server** | Bedrock Data Automation | Automated data processing, document understanding | - |
| **aws-bedrock-custom-model-import-mcp-server** | Bedrock custom model import | Model import, fine-tuning, deployment | - |
| **sagemaker-ai-mcp-server** | Amazon SageMaker ML operations | Model training, deployment, endpoint management, batch inference | - |
| **sagemaker-unified-studio-spark-upgrade-mcp-server** | SageMaker Unified Studio Spark upgrades | Spark version management, migration assistance | - |
| **sagemaker-unified-studio-spark-troubleshooting-mcp-server** | SageMaker Unified Studio Spark troubleshooting | Spark job debugging, performance optimization | - |
| **amazon-kendra-index-mcp-server** | Amazon Kendra intelligent search | Index management, document ingestion, search queries | - |
| **amazon-qbusiness-anonymous-mcp-server** | Amazon Q Business anonymous mode | Q Business queries without authentication | - |
| **amazon-qindex-mcp-server** | Amazon Q index management | Q index operations, data source configuration | - |
| **nova-canvas-mcp-server** | Amazon Nova Canvas image generation | AI image generation, style transfer, image editing | - |

***

## Networking Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **aws-network-mcp-server** | AWS core networking (VPC, subnets, routing) | VPC CRUD, subnet management, route tables, security groups | GDPR Art 32 (network security), DORA Art 11 (network resilience) |
| **aws-location-mcp-server** | Amazon Location Service | Geocoding, routing, geofencing, map rendering | - |

***

## Messaging & Integration Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **amazon-sns-sqs-mcp-server** | Amazon SNS/SQS messaging | Topic/queue management, message publishing, subscription | - |
| **amazon-mq-mcp-server** | Amazon MQ message broker | Broker management, queue/topic operations, message routing | - |
| **aws-msk-mcp-server** | Amazon MSK (Kafka) | Kafka cluster management, topic operations, consumer groups | - |
| **aws-appsync-mcp-server** | AWS AppSync GraphQL | GraphQL API management, resolver configuration, real-time subscriptions | - |

***

## Developer Tools Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **git-repo-research-mcp-server** | Git repository analysis | Code search, commit history, repository insights | - |
| **code-doc-gen-mcp-server** | Code documentation generation | Automated documentation, code analysis, docstring generation | - |
| **openapi-mcp-server** | OpenAPI specification operations | API spec validation, code generation, documentation | - |
| **aws-documentation-mcp-server** | AWS documentation search | AWS docs retrieval, service documentation, best practices | - |
| **aws-knowledge-mcp-server** | AWS knowledge base | AWS service information, troubleshooting guides | - |

***

## Specialized Domain Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **aws-healthomics-mcp-server** | AWS HealthOmics genomics | Genomic workflow management, variant analysis | GDPR Art 32 (health data security) |
| **healthlake-mcp-server** | AWS HealthLake FHIR | FHIR resource operations, healthcare data management | GDPR Art 32 (health data security) |
| **healthimaging-mcp-server** | AWS HealthImaging medical imaging | DICOM image management, medical imaging workflows | GDPR Art 32 (health data security) |
| **aws-iot-sitewise-mcp-server** | AWS IoT SiteWise industrial data | Asset modeling, time-series data, industrial analytics | - |

***

## Utility & Support Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **aws-api-mcp-server** | Generic AWS API operations | Direct AWS API calls, service exploration | - |
| **core-mcp-server** | Core MCP functionality | Base MCP operations, protocol utilities | - |
| **aws-support-mcp-server** | AWS Support case management | Support case CRUD, Trusted Advisor checks | - |
| **aws-diagram-mcp-server** | AWS architecture diagram generation | Infrastructure visualization, diagram as code | - |
| **document-loader-mcp-server** | Document loading and processing | Multi-format document parsing, text extraction | - |
| **syntheticdata-mcp-server** | Synthetic data generation | Test data generation, data masking | GDPR Art 25 (privacy by design) |
| **frontend-mcp-server** | Frontend development utilities | UI component generation, frontend tooling | - |
| **finch-mcp-server** | Finch container runtime | Container operations, local development | - |
| **ccapi-mcp-server** | Cryptocurrency API integration | Crypto market data, price tracking | - |
| **aws-dataprocessing-mcp-server** | Data processing workflows | ETL operations, data transformation | - |

***

## Virons Platform Servers

| Server Name | Description | Key Features | Compliance Tags |
|-------------|-------------|--------------|-----------------|
| **virons-common** | Virons shared utilities | Common functions, audit patterns, compliance helpers | BaFin AT 8.1, GDPR Art 25/32, DORA Art 11 |
| **mcp-lambda-handler** | Lambda handler for MCP servers | Serverless MCP deployment, Lambda integration | - |

***

## Summary Statistics

- **Total Servers**: 67
- **Security & Compliance**: 3
- **Monitoring & Observability**: 4
- **Cost Management**: 3
- **Infrastructure & Orchestration**: 9
- **Data Services**: 13
- **AI/ML**: 11
- **Networking**: 2
- **Messaging & Integration**: 4
- **Developer Tools**: 5
- **Specialized Domain**: 4
- **Utility & Support**: 8
- **Virons Platform**: 2

***

## Metadata

- **Document Owner**: Platform Architecture Team
- **Last Updated**: 2026-03-05
- **Next Review**: 2026-04-05
- **Related**: [ADR-001](../decisions/ADR-001-port-allocation.md), [Scoring Framework](SCORING-FRAMEWORK.md)
