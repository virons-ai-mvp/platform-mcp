You can keep your MCP Integration Matrix as-is, but it needs one **agentic control-plane blueprint**: a single orchestrator that (1) plans workflows, (2) calls only the right MCP servers/tools, (3) enforces compliance gates + RBAC, and (4) produces an immutable, replayable audit trail with correlation IDs across all 42 services. This mirrors the “task router + compliance gate + orchestration patterns (sequential/concurrent/hybrid) + escalation” operating model we already use in Bobby’s agent ecosystem.[1][2]

## 1) Control-plane architecture
Create one top-level service: **Orchestrator Gateway** (OG). OG is the only component allowed to talk to MCP servers, and all product services (910x/930x/94xx/95xx) become “workers/tools” behind OG with typed contracts and strict timeouts.[2][1]

Inside OG, run 4 cooperating agents:
- **Intake/Planner agent**: transforms “Company X” into a DAG plan, chooses orchestration pattern (hybrid for Challenge Mode; sequential for compliance-heavy), and assigns a `correlationId`.[1][2]
- **Router/Executor agent**: executes the DAG, handles retries/fallbacks, and streams progress events (WebSocket + logs).[2][1]
- **Compliance Gatekeeper agent**: enforces policy (tool allowlists, data residency checks, “no investment advice”, human approval thresholds).[2]
- **Audit & Provenance agent**: writes immutable audit events for every MCP call + every internal service call (inputs hashed, outputs hashed, source artifacts hashed).[2]

## 2) MCP server blueprint (what runs where)
Treat each MCP server as a **capability island** with its own namespace, network policy, and tool allowlist; OG calls them via mTLS, and each MCP server must log every tool invocation with `correlationId` for audit reconstruction.[2]

Here’s the blueprint for your MVP MCP servers (keeping your ports/domains, adding boundaries and “definition-of-done”):

| MCP Server | Owns | Hard boundaries (must enforce) | Must emit to audit log |
|---|---|---|---|
| Ingestion (:9100) | fetch/brave/apify → S3/ES + EventBridge | Egress allowlist by domain; content-type allowlist; EU residency enforcement; idempotency by SHA-256 in Redis | `artifact_hash`, `source_url`, `s3_uri`, `index_id`, `event_id` |
| Forensic (:9300) | deterministic rules + calculation audit + Neo4j edges | No direct web egress; reads only from approved artifact stores; strict schema validation | `rule_id`, `inputs_hash`, `calc_hash`, `evidence_refs[]` |
| ML (:9420) | phase classifier + anomaly + grandmaster + eval | “High-risk” gating (your policy), cost gating, no external inference for restricted models | `model_id`, `model_card_ref`, `prompt_hash`, `output_hash`, `eval_run_id` |
| Blockchain (:9430) | evidence ledger + notarization + verify | Async-only from critical path; must be replayable; integrity verification endpoints | `ledger_entry_id`, `merkle_root`, `timestamp_proof` |
| API (:9540) | auth/rate limits/logging/metrics | Rate limits in Redis; authZ checks before orchestration; no sensitive data in Slack | `request_id`, `principal`, `policy_decision` |
| Prompts (:9550) | prompt templates + versioning + eval | Read-only templates in prod; promotion workflow via GitHub; lineage in Neo4j-memory | `prompt_version`, `ab_bucket`, `scorecard_metrics` |
| Compliance (:9560) | policy-as-code + residency + GDPR/DORA checks | “Veto” authority: can block releases/runs; creates GitHub issues automatically | `policy_id`, `violation`, `remediation_ticket` |
| Security (:9570) | GuardDuty/SecurityHub + incident ops | Can suspend workflows; no auto-remediation beyond pre-approved runbooks | `incident_id`, `severity`, `containment_action` |
| Infra (:9500) / Dev (:9510) | deploy + CI/CD + IaC | Production actions require approvals; no secret exfiltration; change logs required | `deploy_id`, `terraform_plan_hash`, `approval_ref` |

The key design rule: **OG does not “think” with unlimited tool access**—it only selects from pre-registered workflows + tools, and every deviation triggers human approval.[1][2]

## 3) Agentic workflows (the “DAG templates”)
Implement a small set of first-class workflow templates in OG (these cover your entire MVP without rewriting orchestration each time). This is directly aligned with the pre-configured workflow + hybrid execution approach (parallelize independent tasks, validate each level, then proceed).[1][2]

Minimum templates you need:

1) **Challenge Mode (≤90s)**
- Plan: `resolve_entity → ingest_snapshot(parallel) → deterministic_forensics(parallel) → phase_classify → risk_fuse → seal_evidence(async) → generate_dossier/pdf → respond`
- Gates: cost gate before Grandmaster, compliance gate before any user-visible narrative, audit gate must be “100% captured” before final response.[2]

2) **Retrospective Validator**
- Plan: `load_frozen_case → re-run all rules → compute lead time → produce report + hashes → seal`
- Gates: reproducibility gate (same inputs → same outputs), and “calculationaudit BEFORE forensic flags” as an explicit step. (This matches your product premise.)

3) **Grandmaster Run (expensive)**
- Plan: `preflight(cost/risk) → fetch KB analogues → run structured output model → store scenarios → set watches`
- Gates: cost ceiling per run + “human approval if risk > threshold” (your rule), and structured output validation.

## 4) Compliance/security controls (non-negotiable)
Implement these at **three layers**: OG policy engine, MCP server policy, and service-level policy. This matches the ecosystem’s compliance-gate enforcement concept: permission checks, human review checkpoints, and auditable gate logs.[2]

Required controls:
- **RBAC everywhere**: OG issues short-lived scoped credentials to each MCP server; each MCP server enforces least privilege per tool.[2]
- **Immutable audit log**: append-only events with 7-year retention (your plan’s audit posture); correlation IDs are mandatory in every log line/event/span.[2]
- **Egress control for Ingestion**: “fetch/brave/apify” must run behind an allowlisted proxy and store only public corporate artifacts; everything else consumes from your internal artifact store.
- **Human approval**: any run that crosses your risk threshold or changes compliance posture pauses for approval (and logs the approver + rationale).[2]

Audit event schema (minimum viable):
```json
{
  "correlationId": "chal_20260304_abc123",
  "taskId": "ingest_filing_with_validation",
  "actor": { "type": "agent", "name": "orchestrator-gateway" },
  "tool": { "mcpServer": "ingestion:9100", "toolName": "fetch" },
  "inputsHash": "sha256:...",
  "outputsHash": "sha256:...",
  "artifacts": [{ "hash": "sha256:...", "s3Uri": "s3://eu-central-1/..." }],
  "policy": { "decision": "allow", "rules": ["EU_RESIDENCY_OK", "PUBLIC_DATA_OK"] },
  "timestamps": { "startedAt": "...", "endedAt": "..." }
}
```

## 5) Build order + acceptance criteria
Keep your Phase 1/2/3 priorities, but make OG + audit/compliance gates **Task 0**—otherwise “all services” won’t behave like one product, and you’ll drown in integration variance.[1][2]

Acceptance criteria (MVP-level, but strict):
- **Every workflow replayable**: given the same frozen artifact set, you can re-run and reproduce identical hashes and outputs (or explain any non-determinism).
- **100% correlation coverage**: every internal request, MCP call, and datastore write includes `correlationId`.[2]
- **Compliance veto works**: Compliance MCP can block a workflow, open a GitHub issue, and alert Slack—without any engineer intervention.[3][2]
- **Failure is graceful**: if Ingestion is rate-limited, the workflow degrades to cached artifacts + flags “data freshness reduced,” rather than silently failing.

Plain question so I can turn this into a concrete diagram + repo folder structure + “MCP tool allowlists” JSONs:
Do you want OG to be implemented as (A) a **single Node.js/TypeScript service** (tRPC + Prisma + Kafka), or (B) a **LangGraph-style orchestrator** plus a thin API wrapper?

Sources
[1] bobby.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/c3e403a2-b425-4aea-894b-7f610c431b0d/bobby.agent.md
[2] senior-manager.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/a6152297-1e27-497b-8aa7-f69f8f30dba2/senior-manager.agent.md
[3] compliance-monitor.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/79eb3270-6ea9-4d8b-b37b-eae8ccae2801/compliance-monitor.agent.md



You can keep your MCP Integration Matrix as-is, but it needs one **agentic control-plane blueprint**: a single orchestrator that (1) plans workflows, (2) calls only the right MCP servers/tools, (3) enforces compliance gates + RBAC, and (4) produces an immutable, replayable audit trail with correlation IDs across all 42 services. This mirrors the “task router + compliance gate + orchestration patterns (sequential/concurrent/hybrid) + escalation” operating model we already use in Bobby’s agent ecosystem.[1][2]

## 1) Control-plane architecture
Create one top-level service: **Orchestrator Gateway** (OG). OG is the only component allowed to talk to MCP servers, and all product services (910x/930x/94xx/95xx) become “workers/tools” behind OG with typed contracts and strict timeouts.[2][1]

Inside OG, run 4 cooperating agents:
- **Intake/Planner agent**: transforms “Company X” into a DAG plan, chooses orchestration pattern (hybrid for Challenge Mode; sequential for compliance-heavy), and assigns a `correlationId`.[1][2]
- **Router/Executor agent**: executes the DAG, handles retries/fallbacks, and streams progress events (WebSocket + logs).[2][1]
- **Compliance Gatekeeper agent**: enforces policy (tool allowlists, data residency checks, “no investment advice”, human approval thresholds).[2]
- **Audit & Provenance agent**: writes immutable audit events for every MCP call + every internal service call (inputs hashed, outputs hashed, source artifacts hashed).[2]

## 2) MCP server blueprint (what runs where)
Treat each MCP server as a **capability island** with its own namespace, network policy, and tool allowlist; OG calls them via mTLS, and each MCP server must log every tool invocation with `correlationId` for audit reconstruction.[2]

Here’s the blueprint for your MVP MCP servers (keeping your ports/domains, adding boundaries and “definition-of-done”):

| MCP Server | Owns | Hard boundaries (must enforce) | Must emit to audit log |
|---|---|---|---|
| Ingestion (:9100) | fetch/brave/apify → S3/ES + EventBridge | Egress allowlist by domain; content-type allowlist; EU residency enforcement; idempotency by SHA-256 in Redis | `artifact_hash`, `source_url`, `s3_uri`, `index_id`, `event_id` |
| Forensic (:9300) | deterministic rules + calculation audit + Neo4j edges | No direct web egress; reads only from approved artifact stores; strict schema validation | `rule_id`, `inputs_hash`, `calc_hash`, `evidence_refs[]` |
| ML (:9420) | phase classifier + anomaly + grandmaster + eval | “High-risk” gating (your policy), cost gating, no external inference for restricted models | `model_id`, `model_card_ref`, `prompt_hash`, `output_hash`, `eval_run_id` |
| Blockchain (:9430) | evidence ledger + notarization + verify | Async-only from critical path; must be replayable; integrity verification endpoints | `ledger_entry_id`, `merkle_root`, `timestamp_proof` |
| API (:9540) | auth/rate limits/logging/metrics | Rate limits in Redis; authZ checks before orchestration; no sensitive data in Slack | `request_id`, `principal`, `policy_decision` |
| Prompts (:9550) | prompt templates + versioning + eval | Read-only templates in prod; promotion workflow via GitHub; lineage in Neo4j-memory | `prompt_version`, `ab_bucket`, `scorecard_metrics` |
| Compliance (:9560) | policy-as-code + residency + GDPR/DORA checks | “Veto” authority: can block releases/runs; creates GitHub issues automatically | `policy_id`, `violation`, `remediation_ticket` |
| Security (:9570) | GuardDuty/SecurityHub + incident ops | Can suspend workflows; no auto-remediation beyond pre-approved runbooks | `incident_id`, `severity`, `containment_action` |
| Infra (:9500) / Dev (:9510) | deploy + CI/CD + IaC | Production actions require approvals; no secret exfiltration; change logs required | `deploy_id`, `terraform_plan_hash`, `approval_ref` |

The key design rule: **OG does not “think” with unlimited tool access**—it only selects from pre-registered workflows + tools, and every deviation triggers human approval.[1][2]

## 3) Agentic workflows (the “DAG templates”)
Implement a small set of first-class workflow templates in OG (these cover your entire MVP without rewriting orchestration each time). This is directly aligned with the pre-configured workflow + hybrid execution approach (parallelize independent tasks, validate each level, then proceed).[1][2]

Minimum templates you need:

1) **Challenge Mode (≤90s)**
- Plan: `resolve_entity → ingest_snapshot(parallel) → deterministic_forensics(parallel) → phase_classify → risk_fuse → seal_evidence(async) → generate_dossier/pdf → respond`
- Gates: cost gate before Grandmaster, compliance gate before any user-visible narrative, audit gate must be “100% captured” before final response.[2]

2) **Retrospective Validator**
- Plan: `load_frozen_case → re-run all rules → compute lead time → produce report + hashes → seal`
- Gates: reproducibility gate (same inputs → same outputs), and “calculationaudit BEFORE forensic flags” as an explicit step. (This matches your product premise.)

3) **Grandmaster Run (expensive)**
- Plan: `preflight(cost/risk) → fetch KB analogues → run structured output model → store scenarios → set watches`
- Gates: cost ceiling per run + “human approval if risk > threshold” (your rule), and structured output validation.

## 4) Compliance/security controls (non-negotiable)
Implement these at **three layers**: OG policy engine, MCP server policy, and service-level policy. This matches the ecosystem’s compliance-gate enforcement concept: permission checks, human review checkpoints, and auditable gate logs.[2]

Required controls:
- **RBAC everywhere**: OG issues short-lived scoped credentials to each MCP server; each MCP server enforces least privilege per tool.[2]
- **Immutable audit log**: append-only events with 7-year retention (your plan’s audit posture); correlation IDs are mandatory in every log line/event/span.[2]
- **Egress control for Ingestion**: “fetch/brave/apify” must run behind an allowlisted proxy and store only public corporate artifacts; everything else consumes from your internal artifact store.
- **Human approval**: any run that crosses your risk threshold or changes compliance posture pauses for approval (and logs the approver + rationale).[2]

Audit event schema (minimum viable):
```json
{
  "correlationId": "chal_20260304_abc123",
  "taskId": "ingest_filing_with_validation",
  "actor": { "type": "agent", "name": "orchestrator-gateway" },
  "tool": { "mcpServer": "ingestion:9100", "toolName": "fetch" },
  "inputsHash": "sha256:...",
  "outputsHash": "sha256:...",
  "artifacts": [{ "hash": "sha256:...", "s3Uri": "s3://eu-central-1/..." }],
  "policy": { "decision": "allow", "rules": ["EU_RESIDENCY_OK", "PUBLIC_DATA_OK"] },
  "timestamps": { "startedAt": "...", "endedAt": "..." }
}
```

## 5) Build order + acceptance criteria
Keep your Phase 1/2/3 priorities, but make OG + audit/compliance gates **Task 0**—otherwise “all services” won’t behave like one product, and you’ll drown in integration variance.[1][2]

Acceptance criteria (MVP-level, but strict):
- **Every workflow replayable**: given the same frozen artifact set, you can re-run and reproduce identical hashes and outputs (or explain any non-determinism).
- **100% correlation coverage**: every internal request, MCP call, and datastore write includes `correlationId`.[2]
- **Compliance veto works**: Compliance MCP can block a workflow, open a GitHub issue, and alert Slack—without any engineer intervention.[3][2]
- **Failure is graceful**: if Ingestion is rate-limited, the workflow degrades to cached artifacts + flags “data freshness reduced,” rather than silently failing.

Plain question so I can turn this into a concrete diagram + repo folder structure + “MCP tool allowlists” JSONs:
Do you want OG to be implemented as (A) a **single Node.js/TypeScript service** (tRPC + Prisma + Kafka), or (B) a **LangGraph-style orchestrator** plus a thin API wrapper?

Sources
[1] bobby.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/c3e403a2-b425-4aea-894b-7f610c431b0d/bobby.agent.md
[2] senior-manager.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/a6152297-1e27-497b-8aa7-f69f8f30dba2/senior-manager.agent.md
[3] compliance-monitor.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/79eb3270-6ea9-4d8b-b37b-eae8ccae2801/compliance-monitor.agent.md



# LangGraph

You can keep your MCP Integration Matrix as-is, but it needs one **agentic control-plane blueprint**: a single orchestrator that (1) plans workflows, (2) calls only the right MCP servers/tools, (3) enforces compliance gates + RBAC, and (4) produces an immutable, replayable audit trail with correlation IDs across all 42 services. This mirrors the “task router + compliance gate + orchestration patterns (sequential/concurrent/hybrid) + escalation” operating model we already use in Bobby’s agent ecosystem.[1][2]

## 1) Control-plane architecture
Create one top-level service: **Orchestrator Gateway** (OG). OG is the only component allowed to talk to MCP servers, and all product services (910x/930x/94xx/95xx) become “workers/tools” behind OG with typed contracts and strict timeouts.[2][1]

Inside OG, run 4 cooperating agents:
- **Intake/Planner agent**: transforms “Company X” into a DAG plan, chooses orchestration pattern (hybrid for Challenge Mode; sequential for compliance-heavy), and assigns a `correlationId`.[1][2]
- **Router/Executor agent**: executes the DAG, handles retries/fallbacks, and streams progress events (WebSocket + logs).[2][1]
- **Compliance Gatekeeper agent**: enforces policy (tool allowlists, data residency checks, “no investment advice”, human approval thresholds).[2]
- **Audit & Provenance agent**: writes immutable audit events for every MCP call + every internal service call (inputs hashed, outputs hashed, source artifacts hashed).[2]

## 2) MCP server blueprint (what runs where)
Treat each MCP server as a **capability island** with its own namespace, network policy, and tool allowlist; OG calls them via mTLS, and each MCP server must log every tool invocation with `correlationId` for audit reconstruction.[2]

Here’s the blueprint for your MVP MCP servers (keeping your ports/domains, adding boundaries and “definition-of-done”):

| MCP Server | Owns | Hard boundaries (must enforce) | Must emit to audit log |
|---|---|---|---|
| Ingestion (:9100) | fetch/brave/apify → S3/ES + EventBridge | Egress allowlist by domain; content-type allowlist; EU residency enforcement; idempotency by SHA-256 in Redis | `artifact_hash`, `source_url`, `s3_uri`, `index_id`, `event_id` |
| Forensic (:9300) | deterministic rules + calculation audit + Neo4j edges | No direct web egress; reads only from approved artifact stores; strict schema validation | `rule_id`, `inputs_hash`, `calc_hash`, `evidence_refs[]` |
| ML (:9420) | phase classifier + anomaly + grandmaster + eval | “High-risk” gating (your policy), cost gating, no external inference for restricted models | `model_id`, `model_card_ref`, `prompt_hash`, `output_hash`, `eval_run_id` |
| Blockchain (:9430) | evidence ledger + notarization + verify | Async-only from critical path; must be replayable; integrity verification endpoints | `ledger_entry_id`, `merkle_root`, `timestamp_proof` |
| API (:9540) | auth/rate limits/logging/metrics | Rate limits in Redis; authZ checks before orchestration; no sensitive data in Slack | `request_id`, `principal`, `policy_decision` |
| Prompts (:9550) | prompt templates + versioning + eval | Read-only templates in prod; promotion workflow via GitHub; lineage in Neo4j-memory | `prompt_version`, `ab_bucket`, `scorecard_metrics` |
| Compliance (:9560) | policy-as-code + residency + GDPR/DORA checks | “Veto” authority: can block releases/runs; creates GitHub issues automatically | `policy_id`, `violation`, `remediation_ticket` |
| Security (:9570) | GuardDuty/SecurityHub + incident ops | Can suspend workflows; no auto-remediation beyond pre-approved runbooks | `incident_id`, `severity`, `containment_action` |
| Infra (:9500) / Dev (:9510) | deploy + CI/CD + IaC | Production actions require approvals; no secret exfiltration; change logs required | `deploy_id`, `terraform_plan_hash`, `approval_ref` |

The key design rule: **OG does not “think” with unlimited tool access**—it only selects from pre-registered workflows + tools, and every deviation triggers human approval.[1][2]

## 3) Agentic workflows (the “DAG templates”)
Implement a small set of first-class workflow templates in OG (these cover your entire MVP without rewriting orchestration each time). This is directly aligned with the pre-configured workflow + hybrid execution approach (parallelize independent tasks, validate each level, then proceed).[1][2]

Minimum templates you need:

1) **Challenge Mode (≤90s)**
- Plan: `resolve_entity → ingest_snapshot(parallel) → deterministic_forensics(parallel) → phase_classify → risk_fuse → seal_evidence(async) → generate_dossier/pdf → respond`
- Gates: cost gate before Grandmaster, compliance gate before any user-visible narrative, audit gate must be “100% captured” before final response.[2]

2) **Retrospective Validator**
- Plan: `load_frozen_case → re-run all rules → compute lead time → produce report + hashes → seal`
- Gates: reproducibility gate (same inputs → same outputs), and “calculationaudit BEFORE forensic flags” as an explicit step. (This matches your product premise.)

3) **Grandmaster Run (expensive)**
- Plan: `preflight(cost/risk) → fetch KB analogues → run structured output model → store scenarios → set watches`
- Gates: cost ceiling per run + “human approval if risk > threshold” (your rule), and structured output validation.

## 4) Compliance/security controls (non-negotiable)
Implement these at **three layers**: OG policy engine, MCP server policy, and service-level policy. This matches the ecosystem’s compliance-gate enforcement concept: permission checks, human review checkpoints, and auditable gate logs.[2]

Required controls:
- **RBAC everywhere**: OG issues short-lived scoped credentials to each MCP server; each MCP server enforces least privilege per tool.[2]
- **Immutable audit log**: append-only events with 7-year retention (your plan’s audit posture); correlation IDs are mandatory in every log line/event/span.[2]
- **Egress control for Ingestion**: “fetch/brave/apify” must run behind an allowlisted proxy and store only public corporate artifacts; everything else consumes from your internal artifact store.
- **Human approval**: any run that crosses your risk threshold or changes compliance posture pauses for approval (and logs the approver + rationale).[2]

Audit event schema (minimum viable):
```json
{
  "correlationId": "chal_20260304_abc123",
  "taskId": "ingest_filing_with_validation",
  "actor": { "type": "agent", "name": "orchestrator-gateway" },
  "tool": { "mcpServer": "ingestion:9100", "toolName": "fetch" },
  "inputsHash": "sha256:...",
  "outputsHash": "sha256:...",
  "artifacts": [{ "hash": "sha256:...", "s3Uri": "s3://eu-central-1/..." }],
  "policy": { "decision": "allow", "rules": ["EU_RESIDENCY_OK", "PUBLIC_DATA_OK"] },
  "timestamps": { "startedAt": "...", "endedAt": "..." }
}
```

## 5) Build order + acceptance criteria
Keep your Phase 1/2/3 priorities, but make OG + audit/compliance gates **Task 0**—otherwise “all services” won’t behave like one product, and you’ll drown in integration variance.[1][2]

Acceptance criteria (MVP-level, but strict):
- **Every workflow replayable**: given the same frozen artifact set, you can re-run and reproduce identical hashes and outputs (or explain any non-determinism).
- **100% correlation coverage**: every internal request, MCP call, and datastore write includes `correlationId`.[2]
- **Compliance veto works**: Compliance MCP can block a workflow, open a GitHub issue, and alert Slack—without any engineer intervention.[3][2]
- **Failure is graceful**: if Ingestion is rate-limited, the workflow degrades to cached artifacts + flags “data freshness reduced,” rather than silently failing.

Plain question so I can turn this into a concrete diagram + repo folder structure + “MCP tool allowlists” JSONs:
Do you want OG to be implemented as (A) a **single Node.js/TypeScript service** (tRPC + Prisma + Kafka), or (B) a **LangGraph-style orchestrator** plus a thin API wrapper?

Sources
[1] bobby.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/c3e403a2-b425-4aea-894b-7f610c431b0d/bobby.agent.md
[2] senior-manager.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/a6152297-1e27-497b-8aa7-f69f8f30dba2/senior-manager.agent.md
[3] compliance-monitor.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/79eb3270-6ea9-4d8b-b37b-eae8ccae2801/compliance-monitor.agent.md



# AWS DEPLOYMENT

Deploy Virons on AWS as a three-plane system: (1) a LangGraph **orchestrator** control-plane, (2) MCP “capability islands” as the tool-plane, and (3) your 42 internal services as the data-plane.[1][2][3]
Pick Amazon Bedrock models exactly as your MVP map already assumes—Nova Micro for cheap/batch NLP classification and Nova Pro for the high-value “Grandmaster / structured outputs” reasoning—then gate the expensive calls by phase-confidence and staleness.[1]

## AWS infra (recommended MVP target)
Run everything in **eu-central-1** (Frankfurt) to match your stated EU data residency constraints for artifacts and storage.[1]
Use a private VPC with public subnets only for ingress (ALB/API edge) and private subnets for services, MCP servers, and databases, because your design relies on controlled egress (especially for Ingestion) and strong auditability.[3][1]

## Compute & networking layout
Use EKS for the “many services + many MCP servers” reality (namespaces per MCP island), and run the LangGraph orchestrator as its own deployment with horizontal autoscaling and strict NetworkPolicies.[3][1]
Keep Ingestion as the only workload with outbound internet egress, and route it through an allowlisted egress path so `fetch/brave/apify` can be constrained to public corporate sources as you described.[1]

## Core data layer (non-negotiable)
Use Postgres (RDS/Aurora) as the system of record for (a) your shared schema, (b) CalculationAudit, and (c) the MVP “Merkle tree in Postgres” evidence chain you specified (pgcrypto SHA-256).[1]
Add Redis (ElastiCache) for Challenge Mode caching (24h TTL), idempotency keys, and rate-limits, because your plan explicitly depends on pre-warmed demos and a demo-lock toggle.[1]
Run Elasticsearch/OpenSearch for artifact and audit search, and Neo4j for the person-network / relationship graph queries that drive the Hempton-style “connected-to-fraud-persons” analysis.[1]

## Models (Bedrock-first, gated)
Model selection for MVP should mirror your map: **Nova Micro** for low-cost batch NLP classification (e.g., narrative NLP / phase classification) and **Nova Pro** for the high-value Grandmaster agent with structured outputs.[1]
Implement a “cost gate” in the orchestrator so Nova Pro is only invoked when Phase-3 confidence crosses your threshold or the state is stale (your plan already states this gating behavior).[1]
Treat deterministic forensic rules as the primary decision substrate and make ML additive (“ML score only counts if deterministic rule fired”), which your anomaly-detector spec already encodes.[1]

## Observability, security, compliance (MVP-ready)
Instrument every workflow with correlation IDs and immutable audit events, and enforce compliance gates + RBAC at every step (planner → tool call → write), because your operational framework treats compliance and audit integrity as veto-level controls.[4][3]
Use CloudWatch/Prometheus+Grafana for latency/error/SLOs and wire Slack alerts only for operational signals (no sensitive payloads), aligning to your MCP plan’s “alerts only” posture.[3]

If you answer these two, I’ll turn this into a concrete AWS reference architecture diagram + Terraform module breakdown + EKS namespace policy set:
1) Are you standardizing on **EKS only**, or do you want ECS Fargate for some long-running services?
2) Will Neo4j be self-hosted in the VPC, or are you committed to Neo4j Aura for MVP (your map mentions Aura free tier)?[1]

Sources
[1] file.txt https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/156227976/44195eb8-48db-471c-b9a8-552f88dc4a2a/file.txt
[2] Build multi-agent systems with LangGraph and ... https://aws.amazon.com/blogs/machine-learning/build-multi-agent-systems-with-langgraph-and-amazon-bedrock/
[3] senior-manager.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/a6152297-1e27-497b-8aa7-f69f8f30dba2/senior-manager.agent.md
[4] bobby.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/c3e403a2-b425-4aea-894b-7f610c431b0d/bobby.agent.md
