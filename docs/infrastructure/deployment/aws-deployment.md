With 1,000 Challenge Mode runs/day and a <300s target, design for **bursty concurrency** (e.g., 10–50 runs in parallel) and let EKS scale compute quickly while keeping stateful systems managed and stable.
On EKS, use Karpenter (or EKS Auto Mode built on Karpenter) for fast, demand-driven node provisioning and consolidation, and lock down AWS access via IRSA so every pod has least-privilege credentials.[1][2][3]

## Capacity model (what to size for)
1,000/day is only ~0.7 runs/min on average, but demos/users cluster in bursts, so your p95 latency will be dominated by (a) ingestion fetch timeouts, (b) Bedrock calls (Nova Pro), and (c) stateful bottlenecks (Postgres/OpenSearch/Neo4j).[4]
Make the orchestrator enforce a per-run **time budget** (e.g., 240s hard stop, leaving 60s safety) and degrade gracefully to cached artifacts when ingestion is slow (your design already includes Redis cache + demo lock).[4]

## EKS shape (simple, scalable)
Use **Karpenter** with 3–4 NodePools (separation is what keeps overhead low while still controlling blast radius): one “system” pool (orchestrator/API), one “compute” pool (forensics/ML), one “ingestion-egress” pool (the only workloads allowed outbound internet), and optionally one “stateful-helpers” pool (internal gateways/workers).[2][1][4]
Do **IRSA** for every namespace/service account that touches AWS (S3 artifacts, Secrets Manager, CloudWatch, OpenSearch) so you never ship static AWS keys into pods.[3]

Action items:
- Install/enable: ALB controller + ExternalDNS + EBS CSI driver (PVCs), and deploy Karpenter (or EKS Auto Mode) for burst scaling.[5][1][2]
- Enforce default-deny NetworkPolicies; only the ingestion namespace can egress to allowlisted domains (fetch/brave/apify).[4]

## OpenSearch + Redis sizing approach
For OpenSearch (managed) treat it like two workloads: **write-heavy logs/audit** and **read/search for artifacts & hashes**; keep shard sizing sane because too many/tiny shards kills performance.[6]
AWS’s guidance is to aim for shard sizes around **10–30 GiB** when search latency matters (and 30–50 GiB for write-heavy log analytics), and keep shard counts within node limits (also consider “shards per GiB of heap” guidance).[6]

For Redis (ElastiCache), plan on cluster-mode enabled if you expect growth; AWS recommends choosing an instance size that fits workload, then scaling by shard count as capacity needs change.[7]
Use Redis for (1) idempotency keys, (2) rate limiting, (3) Challenge Mode cache (24h TTL), and (4) pre-warmed historical cases—those are the levers that keep you under 300s even when upstream is slow.[4]

## Models (keep <300s reliably)
Keep deterministic forensics as the “always-run” path and gate Nova Pro calls hard: your plan already says Grandmaster should only fire when Phase-3 confidence crosses threshold or the signal is stale.[4]
Run Nova Micro for cheap/batch classifications (narrative NLP/phase), and reserve Nova Pro for Grandmaster structured outputs; cache intermediate results by `(company_id, period, artifact_hash)` so repeats are near-instant.[4]

## Two sizing questions (so I can give concrete instance counts)
1) What’s your expected **burst**: peak runs per minute (e.g., 5/min, 20/min, 100/min) during demo/press moments?
2) For OpenSearch, will you store only audit/artifact metadata (hashes + pointers) or also full forensic outputs (rule results, embeddings, timelines)?

Sources
[1] Karpenter - Amazon EKS - AWS Documentation https://docs.aws.amazon.com/eks/latest/best-practices/karpenter.html
[2] Scale cluster compute with Karpenter and Cluster Autoscaler https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html
[3] IAM roles for service accounts - Amazon EKS - AWS Documentation https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
[4] file.txt https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/156227976/44195eb8-48db-471c-b9a8-552f88dc4a2a/file.txt
[5] AWS add-ons - Amazon EKS https://docs.aws.amazon.com/eks/latest/userguide/workloads-add-ons-available-eks.html
[6] Choosing the number of shards - Amazon OpenSearch Service https://docs.aws.amazon.com/opensearch-service/latest/developerguide/bp-sharding.html
[7] Best practices for sizing your Amazon ElastiCache for Redis clusters https://aws.amazon.com/blogs/database/best-practices-for-sizing-your-amazon-elasticache-for-redis-clusters/
[8] Migrating from Cluster Autoscaler - Karpenter https://karpenter.sh/docs/getting-started/migrating-from-cas/
[9] Karpenter vs Cluster Autoscaler: The Ultimate Guide - PerfectScale https://www.perfectscale.io/blog/karpenter-vs-cluster-autoscaler
[10] Optimize EKS: Karpenter Migration and Cluster Optimization Guide https://allcloud.io/go/emea-il-aws-eks-migration-from-cluster-autoscaler-to-karpenter-guide/
[11] How to Scale ElastiCache Redis Clusters - OneUptime https://oneuptime.com/blog/post/2026-02-12-scale-elasticache-redis-clusters/view
[12] EKS Cluster Autoscaler: 6 Best Practices For Effective Autoscaling https://cast.ai/blog/eks-cluster-autoscaler-6-best-practices-for-effective-autoscaling/
[13] The Scoop On OpenSearch sizing - DEV Community https://dev.to/aws-builders/the-scoop-on-opensearch-sizing-1c9e
[14] Mastering EKS scaling with Karpenter: A practical guide - Diatom Labs https://blog.diatomlabs.com/mastering-eks-scaling-with-karpenter-a-practical-guide-a6e239645a45
[15] Seven rules for OpenSearch sizing https://dev.to/aws-builders/seven-rules-for-opensearch-sizing-jo3
[16] Scaling AWS ElastiCache Redis Instances: What You Need to Know https://howik.com/scaling-aws-elasticache-redis-instances
[17] Cluster Autoscaling with Karpenter https://www.reddit.com/r/kubernetes/comments/14kbi8k/cluster_autoscaling_with_karpenter/
[18] amazon-opensearch-service-developer-guide/doc_source/sizing-domains.md at master · awsdocs/amazon-opensearch-service-developer-guide https://github.com/awsdocs/amazon-opensearch-service-developer-guide/blob/master/doc_source/sizing-domains.md


Deploy Virons on AWS with **one EKS cluster** (eu-central-1) that runs (a) the LangGraph orchestrator + thin API, (b) all MCP servers as “capability islands” in separate namespaces, and (c) your 42 services as workloads behind those MCP tools.[1][2][3]
For models, keep inference on **Amazon Bedrock** via your bedrock-gateway (Nova Micro for cheap/batch NLP; Nova Pro for Grandmaster structured outputs), and enforce your phase-confidence/staleness cost gate in the orchestrator.[1]

## EKS infrastructure (MVP)
Use EKS Managed Node Groups (separate node groups for control-plane workloads vs compute-heavy forensics/ML) and isolate by Kubernetes namespaces: `orchestrator`, `mcp-ingestion`, `mcp-forensic`, `mcp-ml`, `mcp-evidence`, `mcp-api`, `mcp-compliance`, `mcp-security`, plus `services-*`.[3][1]
Install AWS EKS add-ons you will immediately need for stateful workloads—at minimum the **EBS CSI driver** add-on for PVC-backed storage on EKS.[4]
For AWS access from pods, standardize on **IRSA (IAM roles for service accounts)** so each namespace/service account gets least-privilege access without static credentials.[5][3]

## Data services (AWS-managed)
Make Postgres the system of record for the shared schema, CalculationAudit, and the MVP “SHA-256 Merkle tree in Postgres/pgcrypto” evidence chain you already specified.[1]
Use ElastiCache Redis for idempotency (artifact_hash → ingestion_id), Challenge Mode caching (24h TTL), and API rate-limiting/demolock, because those are explicit MVP requirements in your map.[1]
Store raw artifacts in S3 (EU bucket) and index/search audit + artifacts + outputs in Elasticsearch/OpenSearch, while Neo4j remains the graph store powering person-network queries and “connected to prior fraud persons” workflows.[1]

## Orchestrator runtime (LangGraph)
Run the LangGraph supervisor as a deployment in the `orchestrator` namespace and persist state with a **checkpointer** so runs are resumable (and you can pause for approvals, then resume without re-running completed nodes).[6][3]
Back the checkpointer with a durable store (commonly Postgres) and treat the saved state as part of your audit trail keyed by `correlationId`.[3][6]
Expose only a thin API wrapper: `POST /orchestrate`, `GET /status/{correlationId}`, and `WS /progress/{correlationId}` to support Challenge Mode’s progress feed.[1]

## Models (Bedrock + gating)
Implement your existing Bedrock gateway pattern where Nova Micro handles low-cost batch NLP/classification tasks and Nova Pro is reserved for the expensive “Grandmaster” structured-output reasoning path.[1]
Enforce your Grandmaster “cost gate” (only fire when Phase-3 confidence crosses threshold or state is stale) inside the LangGraph router node, not inside UI code, so the control-plane remains the single source of truth.[3][1]
Keep the deterministic forensic engine primary and treat ML as additive under your own rule (“ML score only counts if a deterministic rule fired”), which preserves explainability for Explode Mode and investor trust.[1]

## Security controls (EKS-only)
Use NetworkPolicies with a CNI that enforces them (e.g., Cilium) to implement “capability islands,” especially to ensure only the Ingestion namespace has controlled outbound egress to `fetch/brave/apify` targets.[7][1]
Lock down AWS permissions via IRSA so each MCP server can only access the specific AWS resources it needs (S3 write for ingestion, CloudWatch metrics for monitoring, Secrets Manager read for runtime secrets, etc.).[5][3]
Make audit events non-optional: every MCP tool call and every internal service call must carry `correlationId` and write an immutable audit record, consistent with your orchestration framework’s compliance gate enforcement model.[3][1]

Two quick decisions will let me finalize this into an exact AWS/EKS module plan (Terraform + namespaces + IRSA roles + storage classes):
1) Do you want **Neo4j** self-hosted on EKS (StatefulSet + PVC) or keep Neo4j Aura (your map mentions Aura free tier)?[1]
2) For “Elasticsearch,” are you using **Amazon OpenSearch Service** (managed) or self-hosted Elasticsearch inside EKS?

Sources
[1] file.txt https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/156227976/44195eb8-48db-471c-b9a8-552f88dc4a2a/file.txt
[2] Build multi-agent systems with LangGraph and ... https://aws.amazon.com/blogs/machine-learning/build-multi-agent-systems-with-langgraph-and-amazon-bedrock/
[3] senior-manager.agent.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_112d9c15-234e-4f27-a125-415d4b806c22/a6152297-1e27-497b-8aa7-f69f8f30dba2/senior-manager.agent.md
[4] AWS add-ons - Amazon EKS https://docs.aws.amazon.com/eks/latest/userguide/workloads-add-ons-available-eks.html
[5] IAM roles for service accounts - Amazon EKS - AWS Documentation https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
[6] Persistence https://langchain-ai.github.io/langgraphjs/concepts/persistence/
[7] Using Network Policies in EKS with Cilium - Deployment https://deployment.properties/posts/devsecops/eks-cilium-network-policies/
[8] IAM roles for service accounts · Issue #128 - GitHub https://github.com/aws/aws-eks-best-practices/issues/128
[9] IAM Roles for Service Accounts - Eksctl User Guide https://docs.aws.amazon.com/eks/latest/eksctl/iamserviceaccounts.html
[10] IAM Roles for Service Accounts (IRSA) in AWS EKS within and cross ... https://dev.to/piyushjajoo/iam-roles-for-service-accounts-irsa-in-aws-eks-within-and-cross-aws-accounts-32pl
[11] Enable IAM Roles for Service Accounts (IRSA) on the EKS cluster https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up-enable-IAM-service-accounts.html
[12] EKS EBS CSI Driver Module https://docs.gruntwork.io/reference/modules/terraform-aws-eks/eks-ebs-csi-driver/
[13] IAM Roles for Service Accounts configuration - EKS Anywhere https://anywhere.eks.amazonaws.com/docs/getting-started/optional/irsa/
[14] Cilium vs Calico: Comparing Kubernetes Networking Solutions https://dev.to/mechcloud_academy/cilium-vs-calico-comparing-kubernetes-networking-solutions-10if
[15] How to Set Up IAM Roles for EKS Service Accounts (IRSA) https://oneuptime.com/blog/post/2026-02-12-set-up-iam-roles-for-eks-service-accounts-irsa/view
[16] How to Provision Persistent Volume on EKS Cluster using EBS CSI ... https://devopscube.com/provsion-persistent-volume-on-eks/
[17] Configure Kubernetes Network Policies for hybrid nodes https://docs.aws.amazon.com/eks/latest/userguide/hybrid-nodes-network-policies.html
[18] Step 5: Verify IRSA Configuration https://oneuptime.com/blog/post/2026-01-30-aws-eks-irsa/view
[19] How to connect EBS CSI Driver in AWS EKS: A Step-by-Step Guide #devops #aws #eks #ebs #csi https://www.youtube.com/watch?v=JWi6lFUpSuw
