# MCP Enterprise Gateway Architecture Blueprint

**Version:** 2.0 (March 2026)  
**Author:** Perplexity AI Agentic Expert  
**Target:** AWS EKS, EU Compliance (AI Act, BaFin, DORA, GDPR)  
**Overview:** Secure, scalable gateway proxying domain-specific MCP servers with centralized auth, audit, and guardrails. Polyglot (TS Gateway, Python servers), DDD architecture.[1][2]

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│             MCP Gateway (Node.js/TS + Fastify)               │  [:9601]
│  - JWT/OIDC (Cognito), RBAC (OPA), Audit (OTEL)             │
│  - DLP (Presidio), Guardrails, Rate-limit (Redis)            │
│  - Registry (Consul), Metrics (Prometheus), SQS HITL         │
└────────────┬────────────────────────────────────────────────┘
             │ HTTPS/mTLS (ALB + Cert-Manager + Istio)
    ┌────────┼────────┬────────┬────────┬────────┬────────┬────────┬────────┐
    │        │        │        │        │        │        │        │        │
    ▼        ▼        ▼        ▼        ▼        ▼        ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Infra   │ │Dev     │ │Forensic│ │ML      │ │Block   │ │API     │ │Prompts │ │Comp    │ │Sec     │
│:9600   │ │:9500   │ │:9300   │ │:9420   │ │:9430   │ │:8000   │ │:8100   │ │:9700   │ │:9800   │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
             │ All: DDD Python (domain/adapters/mcp_server.py)
             └─► Redis (cache) ◄── OTEL ─► Grafana/Prometheus/Loki
                          │
                          ▼ EKS (Karpenter, ArgoCD, Istio Mesh)
```

## Core Principles
1. **Gateway-Centric:** Auth/RBAC/DLP/audit centralized; servers domain-pure.
2. **DDD/Hexagonal:** `domain/` (logic), `adapters/` (I/O), `mcp_server.py` (wiring).
3. **Polyglot:** TS Gateway (ecosystem), Python servers (AI/ML), Go future-perf.
4. **Resilience:** Istio (mTLS/retries), HPA, Redis cache, SQS async.
5. **Observability:** OTEL traces/metrics/logs; SLOs (99.95% P99<200ms).
6. **Compliance:** AI Act traceability, BaFin/DORA resilience, GDPR minimization.

## Gateway Implementation (Node.js/TS, :9601)
```typescript
// src/gateway.ts
import Fastify from 'fastify';
import opa from 'opa-wasm';  // RBAC
import presidio from '@microsoft/presidio';  // DLP

const app = Fastify({ logger: true });
app.register(rateLimit, { redis: process.env.REDIS_URL });
app.addHook('preHandler', async (req) => {
  await cognitoVerify(req.headers.authorization);  // OIDC
  await opaEnforce(req.user, req.path);  // e.g., "infra.*"
  presidioScan(req.body);  // GDPR PII
});
app.register(mcpProxyPlugin, { registry: consulFetchServers() });
app.listen({ port: 9601 });
```

**Helm:** Namespace `mcp-gateway`, replicas=3, HPA.

## Domain Servers: Complete Tool Lists
All Python (`uv init`, `mcp[cli]`, Pydantic). Prefix tools via Gateway (e.g., `infra.list_ec2`).

### Infra (:9600) - AWS/EKS [awslabs/mcp]
| Tool | Inputs | Outputs | Deps |
|------|--------|---------|------|
| `list_accounts` | `filter:str` | `list[dict]` | Organizations |
| `list_ec2_instances` | `account:str,region:str,tags:dict` | `list[Instance]` | EC2 |
| `get_cost_analysis` | `period:str,filters:dict` | `CostReport` | CE |
| `validate_cloudformation` | `template:str` | `ValidationResult` | cfn-lint |
| `deploy_stack` | `template:str,params:dict` | `StackStatus` | CFN |
| `eks_list_clusters` | `region:str` | `list[Cluster]` | EKS/kubectl |
| `eks_get_logs` | `cluster:str,namespace:str,pod:str` | `LogStream` | kubectl |
| `eks_scale_deployment` | `cluster:str,deployment:str,replicas:int` | `ScaleStatus` | kubectl |
| `terraform_plan` | `tf_code:str` | `PlanDiff` | terraform |
| `get_cloudwatch_logs` | `log_group:str,query:str` | `LogEvents` | Logs |
| `list_s3_buckets` | `prefix:str` | `list[Bucket]` | S3 |
| `network_vpc_insights` | `vpc_id:str` | `NetworkReport` | VPC |

### Dev (:9500) - Git/DevOps
| Tool | Inputs | Outputs | Deps |
|------|--------|---------|------|
| `list_repos` | `org:str` | `list[Repo]` | GitHub |
| `get_pr_diff` | `repo:str,pr_num:int` | `DiffReport` | GitHub |
| `create_pr` | `repo:str,title:str,body:str,branch:str` | `PR` | GitHub |
| `run_code_analysis` | `repo:str,ref:str` | `QualityGate` | Sonar |
| `trigger_build` | `pipeline:str,vars:dict` | `BuildStatus` | Actions |
| `list_issues` | `repo:str,labels:list` | `list[Issue]` | GitHub |
| `docker_build_push` | `dockerfile:str,tag:str` | `ImageDigest` | docker |
| `argocd_sync` | `app:str` | `SyncStatus` | argocd |
| `get_test_coverage` | `repo:str,commit:str` | `CoverageReport` | Codecov |
| `search_code` | `query:str,path:str` | `CodeMatches` | GitHub |

### Forensic (:9300) - Logs/Threats
| Tool | Inputs | Outputs | Deps |
|------|--------|---------|------|
| `analyze_pcap` | `pcap_file:str,filter:str` | `ThreatReport` | tshark |
| `query_logs` | `index:str,query:str,time:tuple` | `LogResults` | Splunk/Logs |
| `extract_iocs` | `content:str` | `IOCs` | YARA |
| `check_urlhaus` | `urls:list` | `ThreatScores` | URLhaus |
| `file_integrity` | `file_path:str,expected_hash:str` | `IntegrityReport` | hashlib |
| `timeline_events` | `logs:str` | `Timeline` | Parser |
| `credential_hunt` | `content:str` | `CredsFound` | Regex |
| `network_top_talkers` | `pcap:str` | `CommMatrix` | tshark |
| `compliance_audit` | `logs:str` | `AuditFindings` | Rules |
| `generate_evidence` | `analysis_id:str` | `Report` | ReportLab |

### ML (:9420) - Bedrock/SageMaker
| Tool | Inputs | Outputs | Deps |
|------|--------|---------|------|
| `list_models` | `provider:str` | `list[Model]` | Bedrock |
| `invoke_model` | `model_id:str,prompt:str` | `Response` | Bedrock |
| `deploy_endpoint` | `model:str,instance:str` | `EndpointArn` | SageMaker |
| `list_datasets` | `location:str` | `DatasetInfo` | S3 |
| `train_job` | `algo:str,data:str` | `JobArn` | SageMaker |
| `evaluate_model` | `endpoint:str,test_data:str` | `EvalMetrics` | Custom |
| `redshift_query` | `cluster:str,sql:str` | `QueryResult` | Redshift |
| `feature_store_get` | `name:str,record:str` | `Features` | FeatureStore |
| `hyperparam_tune` | `job:str` | `BestTrial` | SageMaker |

### Blockchain (:9430) - Web3
| Tool | Inputs | Outputs | Deps |
|------|--------|---------|------|
| `get_block` | `chain:str,block:str` | `Block` | web3 |
| `get_tx_receipt` | `tx_hash:str` | `Receipt` | web3 |
| `balance_query` | `address:str,tokens:list` | `Balances` | Alchemy |
| `decode_logs` | `logs:list` | `DecodedEvents` | abi |
| `simulate_tx` | `tx:dict` | `SimResult` | eth_call |
| `nft_metadata` | `contract:str,token_id:str` | `Metadata` | Etherscan |
| `chain_health` | `chain:str` | `Health` | RPC |

### API (:8000) - REST/GraphQL
| Tool | Inputs | Outputs | Deps |
|------|--------|---------|------|
| `call_rest_api` | `url:str,method:str,headers:dict,body:dict` | `Response` | httpx |
| `graphql_query` | `endpoint:str,query:str,vars:dict` | `GraphQLResult` | gql |
| `soap_call` | `wsdl:str,operation:str` | `SOAPResponse` | zeep |
| `oauth_token` | `provider:str` | `Tokens` | oauthlib |
| `cache_get_set` | `key:str,value:str` | `CacheValue` | redis |

### Prompts (:8100) - Library
| Tool | Inputs | Outputs | Deps |
|------|--------|---------|------|
| `search_prompts` | `query:str,tags:list` | `list[Prompt]` | SQLite |
| `get_prompt` | `id:str` | `PromptTemplate` | - |
| `chain_prompts` | `prompts:list,vars:dict` | `ChainedPrompt` | Jinja2 |
| `suggest_prompt` | `task:str` | `Suggestions` | Bedrock |

### Compliance (:9700) - EU Regs
| Tool | Inputs | Outputs | Deps |
|------|--------|---------|------|
| `search_regulations` | `query:str,reg:str` | `RegulationText` | SQLite |
| `check_gdpr_compliance` | `data_flow:str` | `GDPRFindings` | Rules |
| `ai_act_risk_assess` | `system_desc:str` | `RiskLevel` | Annex |
| `dora_ict_resilience` | `vendor_list:list` | `DORAReport` | Art.28 |
| `bafin_marisk_check` | `it_controls:dict` | `BaFinGaps` | Guidelines |
| `generate_audit_evidence` | `controls:list` | `AuditReport` | ReportLab |
| `cross_reg_compare` | `regs:list` | `ComparisonTable` | DB |
| `sanctions_screen` | `entities:list` | `ScreeningHits` | OpenSanctions |
| `control_mapping` | `framework:str` | `Mappings` | YAML |
| `incident_report_gen` | `incident:dict` | `ReportTemplate` | - |

### Security (:9800) - Posture/Threats
| Tool | Inputs | Outputs | Deps |
|------|--------|---------|------|
| `assess_security_posture` | `accounts:list` | `PostureScore` | Config |
| `list_findings` | `severity:str,type:str` | `list[Finding]` | SecurityHub |
| `iam_policy_check` | `policy:str,principal:str` | `PolicyRisks` | Analyzer |
| `check_config_rules` | `rules:list` | `ComplianceStatus` | Config |
| `vulnerability_scan` | `resources:list` | `VulnReport` | Inspector |
| `analyze_cloudtrail` | `query:str,time:tuple` | `Events` | Athena |
| `recommend_remediations` | `findings:list` | `RemediationPlan` | Custom |
| `network_baseline` | `vpc:str` | `BaselineReport` | Flow Logs |
| `secrets_scan` | `resources:list` | `SecretsFound` | GuardDuty |
| `mcp_server_audit` | `period:str` | `AuditTrail` | CloudTrail |

## Deployment Guide
1. **Infra (Terraform):** EKS, Istio, Redis, Cognito.
2. **Monorepo Structure:**
   ```
   mcp-org/
   ├── gateway/     # TS
   ├── servers/
   │   ├── infra/   # Python per domain
   │   └── ...
   ├── infra/       # Terraform/Helm
   └── docs/        # This MD
   ```
3. **CI/CD:** ArgoCD GitOps, GitHub Actions build/push ECR.
4. **Testing:** Pytest (unit), MCP Inspector (e2e), Locust (load).
5. **Monitoring:** Grafana dashboards (tool latency, error rates).

**Resources:** awslabs/mcp, awesome-mcp-servers, mcp-cloud-compliance. Total: 70+ tools, extensible via registry.[2][3][4]

Sources
[1] Build an MCP server - Model Context Protocol https://modelcontextprotocol.io/docs/develop/build-server
[2] awslabs/mcp: Official MCP Servers for AWS - GitHub https://github.com/awslabs/mcp
[3] punkpeye/awesome-mcp-servers - GitHub https://github.com/punkpeye/awesome-mcp-servers
[4] GitHub - uprightsleepy/mcp-cloud-compliance: Conversational cloud security compliance auditing. MCP server enabling natural language queries about AWS security posture via Claude and other AI assistants. https://github.com/uprightsleepy/mcp-cloud-compliance
