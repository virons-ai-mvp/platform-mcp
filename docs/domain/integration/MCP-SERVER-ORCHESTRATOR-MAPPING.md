# MCP Server → Orchestrator Mapping

**Date**: 2026-03-05
**Status**: Implementation Guide

This document maps all available MCP servers to Virons orchestrator domains, ensuring comprehensive coverage of the MCP ecosystem.

---

## Implemented Orchestrators (4/11)

### ✅ 1. virons-infrastructure-mcp-server (9140-9143)

**Purpose**: Infrastructure as Code orchestration

| MCP Server | Image | Port | Status |
|---|---|---|---|
| AWS CDK | `mcp/aws-cdk-mcp-server` | 9140 | ✅ Planned |
| CloudFormation | AWS CFN | 9141 | ✅ Planned |
| Terraform (HashiCorp) | `hashicorp/terraform-mcp-server` | 9142 | ✅ Planned |
| AWS Terraform | `mcp/aws-terraform` | 9142 | ✅ Planned |
| AWS IaC | AWS IaC | 9143 | ✅ Planned |
| AWS Diagram | `mcp/aws-diagram` | 9143 | 🆕 Add |

**Tools**: `deploy_infrastructure`, `list_stacks`, `destroy_infrastructure`

---

### ✅ 2. virons-security-mcp-server (9100-9104)

**Purpose**: Security scanning, compliance, audit

| MCP Server | Image | Port | Status |
|---|---|---|---|
| Gitleaks | (local) | 9100 | ✅ Planned |
| Compliance Gate | (local) | 9101 | ✅ Planned |
| CloudTrail | AWS CloudTrail | 9102 | ✅ Planned |
| IAM | AWS IAM | 9103 | ✅ Planned |
| Well-Architected | AWS Well-Architected | 9104 | ✅ Planned |

**Tools**: `scan_secrets`, `audit_cloudtrail`, `check_iam_policy`, `run_compliance_gate`

---

### ✅ 3. virons-operations-mcp-server (9121-9124)

**Purpose**: Container & compute orchestration

| MCP Server | Image | Port | Status |
|---|---|---|---|
| EKS | AWS EKS | 9121 | ✅ Planned |
| Lambda | AWS Lambda | 9122 | ✅ Planned |
| ECS | AWS ECS | 9123 | ✅ Planned |
| Step Functions | AWS Step Functions | 9124 | ✅ Planned |
| Kubernetes | `mcp/kubernetes` | 9125 | 🆕 Add |
| Docker | `docker:cli` | 9126 | 🆕 Add |

**Tools**: `list_clusters`, `deploy_lambda`, `deploy_ecs_service`, `start_workflow`

---

### ✅ 4. virons-monitoring-mcp-server (9190-9193)

**Purpose**: Metrics, logs, alerts, dashboards

| MCP Server | Image | Port | Status |
|---|---|---|---|
| CloudWatch | AWS CloudWatch | 9190 | ✅ Implemented |
| Prometheus | `ghcr.io/pab1it0/prometheus-mcp-server` | 9191 | ✅ Implemented |
| Grafana | `mcp/grafana` | 9192 | ✅ Implemented |
| Elasticsearch | `mcp/elasticsearch` | 9193 | ✅ Implemented |

**Tools**: `query_metrics`, `create_alert`, `create_dashboard`, `search_logs`

---

## Planned Orchestrators (7/11)

### 🚧 5. virons-data-relational-mcp-server (9150-9153)

**Purpose**: Relational database operations

| MCP Server | Image | Port | Status |
|---|---|---|---|
| Postgres | AWS RDS Postgres | 9150 | 🚧 Plan |
| MySQL | AWS RDS MySQL | 9151 | 🚧 Plan |
| Aurora DSQL | AWS Aurora DSQL | 9152 | 🚧 Plan |
| Redshift | AWS Redshift | 9153 | 🚧 Plan |

**Tools**: `query_database`, `create_table`, `backup_database`, `migrate_schema`

---

### 🚧 6. virons-data-nosql-mcp-server (9180-9189)

**Purpose**: NoSQL & cache operations

| MCP Server | Image | Port | Status |
|---|---|---|---|
| DynamoDB | AWS DynamoDB | 9180 | 🚧 Plan |
| DocumentDB | AWS DocumentDB | 9181 | 🚧 Plan |
| Keyspaces | AWS Keyspaces | 9182 | 🚧 Plan |
| Neptune | AWS Neptune | 9183 | 🚧 Plan |
| ElastiCache | AWS ElastiCache | 9184 | 🚧 Plan |
| S3 Tables | AWS S3 Tables | 9185 | 🚧 Plan |
| Valkey | `mcp/valkey-mcp-server` | 9186 | 🆕 Add |
| Redis | `mcp/redis` | 9187 | 🆕 Add |
| Neo4j | `mcp/neo4j` | 9188 | 🆕 Add |
| Neo4j Cypher | `mcp/neo4j-cypher` | 9188 | 🆕 Add |
| Neo4j Cloud | `mcp/neo4j-cloud-aura-api` | 9188 | 🆕 Add |
| Neo4j Modeling | `mcp/neo4j-data-modeling` | 9188 | 🆕 Add |
| Neo4j Memory | `mcp/neo4j-memory` | 9189 | 🆕 Add |

**Tools**: `query_nosql`, `create_collection`, `graph_query`, `cache_set`

---

### 🆕 7. virons-developer-mcp-server (9200-9209)

**Purpose**: Developer tools, code operations, automation

| MCP Server | Image | Port | Status |
|---|---|---|---|
| Git | `mcp/git` | 9200 | 🆕 New |
| GitHub | `ghcr.io/github/github-mcp-server` | 9201 | 🆕 New |
| GitHub Chat | `mcp/github-chat` | 9202 | 🆕 New |
| Code Interpreter | `mcp/mcp-code-interpreter` | 9203 | 🆕 New |
| Python Refactoring | `mcp/mcp-python-refactoring` | 9204 | 🆕 New |
| Playwright | `mcp/playwright` | 9205 | 🆕 New |
| Puppeteer | `mcp/puppeteer` | 9206 | 🆕 New |

**Tools**: `git_commit`, `create_pr`, `run_code`, `refactor_python`, `automate_browser`

---

### 🆕 8. virons-documentation-mcp-server (9210-9214)

**Purpose**: Documentation, knowledge management

| MCP Server | Image | Port | Status |
|---|---|---|---|
| AWS Documentation | `mcp/aws-documentation` | 9210 | 🆕 New |
| Atlas Docs | `mcp/atlas-docs` | 9211 | 🆕 New |
| Markitdown | `mcp/markitdown` | 9212 | 🆕 New |
| Obsidian | `mcp/obsidian` | 9213 | 🆕 New |
| Wikipedia | `mcp/wikipedia-mcp` | 9214 | 🆕 New |

**Tools**: `search_docs`, `convert_markdown`, `query_wiki`, `manage_notes`

---

### 🆕 9. virons-integration-mcp-server (9215-9224)

**Purpose**: External integrations, APIs, messaging

| MCP Server | Image | Port | Status |
|---|---|---|---|
| Kafka Schema Registry | `aywengo/kafka-schema-reg-mcp` | 9215 | 🆕 New |
| Slack | `mcp/slack` | 9216 | 🆕 New |
| Apify | `mcp/apify-mcp-server` | 9217 | 🆕 New |
| Fetch | `mcp/fetch` | 9218 | 🆕 New |
| Brave Search | `mcp/brave-search` | 9219 | 🆕 New |
| DuckDuckGo | `mcp/duckduckgo` | 9220 | 🆕 New |
| Perplexity | `mcp/perplexity-ask` | 9221 | 🆕 New |
| YouTube | `mcp/youtube-transcript` | 9222 | 🆕 New |
| DockerHub | `mcp/dockerhub` | 9223 | 🆕 New |
| Context7 | `mcp/context7` | 9224 | 🆕 New |

**Tools**: `send_slack`, `scrape_web`, `search_web`, `fetch_transcript`, `manage_context`

---

### 🆕 10. virons-utility-mcp-server (9225-9229)

**Purpose**: Utility functions, helpers

| MCP Server | Image | Port | Status |
|---|---|---|---|
| Time | `mcp/time` | 9225 | 🆕 New |
| Memory | `mcp/memory` | 9226 | 🆕 New |
| Desktop Commander | `mcp/desktop-commander` | 9227 | 🆕 New |

**Tools**: `get_time`, `manage_memory`, `control_desktop`

---

### 🚧 11. virons-ai-ml-mcp-server (9160-9162)

**Purpose**: AI/ML model operations

| MCP Server | Image | Port | Status |
|---|---|---|---|
| SageMaker | AWS SageMaker | 9160 | 🚧 Plan |
| Bedrock KB | AWS Bedrock KB | 9161 | 🚧 Plan |
| Kendra | AWS Kendra | 9162 | 🚧 Plan |

**Tools**: `train_model`, `deploy_endpoint`, `query_kb`, `search_kendra`

---

## Implementation Priority

### Phase 0 (Week 1-2) - ✅ COMPLETE
- [x] virons-infrastructure-mcp-server
- [x] virons-security-mcp-server
- [x] virons-operations-mcp-server
- [x] virons-monitoring-mcp-server

### Phase 1 (Week 3-4) - 🚧 IN PROGRESS
- [ ] virons-data-relational-mcp-server
- [ ] virons-data-nosql-mcp-server

### Phase 2 (Week 5-6) - 🔜 NEXT
- [ ] virons-developer-mcp-server
- [ ] virons-documentation-mcp-server

### Phase 3 (Week 7-8) - 📋 PLANNED
- [ ] virons-integration-mcp-server
- [ ] virons-utility-mcp-server
- [ ] virons-ai-ml-mcp-server

---

## Orchestrator Pattern

Each orchestrator:
1. **Wraps** multiple official MCP servers
2. **Adds** Virons compliance layer (BaFin, GDPR, DORA)
3. **Provides** unified domain API
4. **Audits** all write operations
5. **Enforces** EU data residency

```python
# Example: Monitoring Orchestrator
UPSTREAM = {
    "cloudwatch": {"host": "localhost", "port": 9190},
    "prometheus": {"image": "ghcr.io/pab1it0/prometheus-mcp-server"},
    "grafana": {"image": "mcp/grafana"},
    "elasticsearch": {"image": "mcp/elasticsearch"},
}

@server.tool()
async def query_metrics(source: str, metric: str) -> dict:
    # Route to appropriate upstream MCP server
    # Add compliance audit trail
    # Return unified response
```

---

## Testing Strategy (TDD)

Each orchestrator follows TDD:
1. Write tests first (5 minimum)
2. Implement tools
3. Verify all tests pass
4. Commit with audit trail

**Current Status**: 4 orchestrators, 20/20 tests passing ✅

---

**Maintained By**: Virons Fintech Engineering Team
**Last Updated**: 2026-03-05
