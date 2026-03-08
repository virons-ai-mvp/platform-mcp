# MCP Server Image Catalog

## Available Pre-Built Images (43 servers)

### AWS Infrastructure (7 images)
- `mcp/aws-cdk-mcp-server` - AWS CDK IaC
- `mcp/aws-core-mcp-server` - Core AWS operations
- `mcp/aws-terraform` - Terraform for AWS
- `hashicorp/terraform-mcp-server` - Generic Terraform
- `mcp/aws-diagram` - AWS architecture diagrams
- `mcp/aws-documentation` - AWS docs search
- `docker:cli` - Docker operations

### Data & Databases (8 images)
- `mcp/redis` - Redis cache
- `mcp/valkey-mcp-server` - Valkey (Redis fork)
- `mcp/elasticsearch` - Elasticsearch search
- `mcp/neo4j` - Neo4j graph database
- `mcp/neo4j-cypher` - Cypher queries
- `mcp/neo4j-cloud-aura-api` - Neo4j Aura API
- `mcp/neo4j-data-modeling` - Graph modeling
- `mcp/neo4j-memory` - Neo4j memory store

### Monitoring & Observability (3 images)
- `ghcr.io/pab1it0/prometheus-mcp-server` - Prometheus metrics
- `mcp/grafana` - Grafana dashboards
- `mcp/context7` - Context tracking

### Messaging & Streaming (2 images)
- `aywengo/kafka-schema-reg-mcp:stable` - Kafka + Schema Registry
- `mcp/slack` - Slack integration

### DevOps & CI/CD (3 images)
- `mcp/kubernetes` - Kubernetes management
- `ghcr.io/github/github-mcp-server` - GitHub operations
- `mcp/git` - Git operations

### AI & Search (5 images)
- `mcp/brave-search` - Brave search
- `mcp/duckduckgo` - DuckDuckGo search
- `mcp/perplexity-ask` - Perplexity AI
- `mcp/apify-mcp-server` - Web scraping
- `mcp/wikipedia-mcp` - Wikipedia search

### Development Tools (8 images)
- `mcp/mcp-code-interpreter` - Code execution
- `mcp/mcp-python-refactoring` - Python refactoring
- `mcp/playwright` - Browser automation
- `mcp/puppeteer` - Browser automation
- `mcp/fetch` - HTTP requests
- `mcp/markitdown` - Markdown conversion
- `mcp/desktop-commander` - Desktop automation
- `mcp/dockerhub` - DockerHub search

### Knowledge & Memory (4 images)
- `mcp/memory` - Persistent memory
- `mcp/obsidian` - Obsidian notes
- `mcp/atlas-docs` - Atlas documentation
- `mcp/youtube-transcript` - YouTube transcripts

### Utilities (3 images)
- `mcp/time` - Time operations
- `mcp/github-chat` - GitHub chat
- `mcp/neo4j-memory` - Graph memory

## Integration Priority

### Tier 0: Already Available (Use Immediately)
These can be deployed NOW without building from source:

**Infrastructure (3 images)**
1. `mcp/kubernetes` → Port 9121 (replaces eks-mcp-server build)
2. `mcp/aws-terraform` → Port 9142 (replaces terraform build)
3. `mcp/aws-cdk-mcp-server` → Port 9140 (replaces cdk build)

**Data (2 images)**
4. `mcp/redis` → Port 9184 (replaces elasticache build)
5. `mcp/valkey-mcp-server` → Port 9186 (already planned)

**Monitoring (2 images)**
6. `ghcr.io/pab1it0/prometheus-mcp-server` → Port 9191 (replaces prometheus build)
7. `mcp/grafana` → Port 9301 (new, not in core 8)

**DevOps (2 images)**
8. `ghcr.io/github/github-mcp-server` → Port 9111 (governance)
9. `mcp/git` → Port 9112 (governance)

### Tier 1: High Value for Virons (Deploy Next)
**Messaging**
- `aywengo/kafka-schema-reg-mcp:stable` → Port 9171 (replaces aws-msk)

**Graph Database (Fraud Detection)**
- `mcp/neo4j` → Port 9183 (replaces amazon-neptune)
- `mcp/neo4j-cypher` → Port 9183 (same port, different tools)

**Search (Knowledge Base)**
- `mcp/elasticsearch` → Port 9302 (monitoring context)

### Tier 2: Nice to Have
**AI/Search**: brave-search, duckduckgo, perplexity-ask, wikipedia
**Development**: playwright, puppeteer, code-interpreter
**Knowledge**: memory, obsidian, atlas-docs
**Utilities**: time, fetch, markitdown

## Revised Pareto Plan (Using Pre-Built Images)

### 8 Core Servers → 5 Build + 3 Pre-Built

**MUST BUILD (5 servers)** - No pre-built images available:
1. aws-iac-mcp-server (9143) - Unified IaC
2. postgres-mcp-server (9150) - Primary DB
3. dynamodb-mcp-server (9180) - NoSQL
4. s3-tables-mcp-server (9185) - Data lake
5. cloudwatch-mcp-server (9190) - Monitoring
6. cloudtrail-mcp-server (9102) - Audit

**USE PRE-BUILT (3 servers)** - Available now:
7. `mcp/kubernetes` (9121) - Replaces eks-mcp-server
8. `mcp/aws-terraform` (9142) - Replaces terraform-mcp-server
9. `ghcr.io/pab1it0/prometheus-mcp-server` (9191) - Replaces prometheus build

**BONUS (2 servers)** - Easy wins:
10. `mcp/redis` (9184) - Cache layer
11. `ghcr.io/github/github-mcp-server` (9111) - GitHub ops

## Updated docker-compose.core.yml

```yaml
# Replace these services with pre-built images:

  virons-kubernetes-mcp:
    image: mcp/kubernetes@sha256:5565164f78ee41f3de9d957dbd3c7349fb06be8e95799a2a650cdd90d6d6d529
    container_name: virons-kubernetes-mcp
    ports:
      - "9121:9121"
    environment:
      PORT: 9121
    volumes:
      - ~/.kube:/root/.kube:ro
    networks:
      - virons-mcp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9121/health"]

  virons-terraform-mcp:
    image: mcp/aws-terraform@sha256:db3126c26fc13947f8d200235a872b35cdf7235f07c8fc63c262fb40196dd18e
    container_name: virons-terraform-mcp
    ports:
      - "9142:9142"
    environment:
      PORT: 9142
      AWS_REGION: eu-central-1
    volumes:
      - ~/.aws:/root/.aws:ro
    networks:
      - virons-mcp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9142/health"]

  virons-prometheus-mcp:
    image: ghcr.io/pab1it0/prometheus-mcp-server@sha256:32d47c88845ee78bc343d4c3a39a24b1bd9bebce4f53becdbbf5704221185925
    container_name: virons-prometheus-mcp
    ports:
      - "9191:9191"
    environment:
      PORT: 9191
    networks:
      - virons-mcp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9191/health"]

  virons-redis-mcp:
    image: mcp/redis@sha256:ab96ec0a8618804fe4e08414d27e515c85df8a58806e4f8353331e14670c3b10
    container_name: virons-redis-mcp
    ports:
      - "9184:9184"
    environment:
      PORT: 9184
    networks:
      - virons-mcp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9184/health"]

  virons-github-mcp:
    image: ghcr.io/github/github-mcp-server@sha256:7b1384cdd6d025c09256af2fb6cb79bc5e87aedc957c8826b5e50d8cb82f0be3
    container_name: virons-github-mcp
    ports:
      - "9111:9111"
    environment:
      PORT: 9111
      GITHUB_TOKEN: ${GITHUB_TOKEN}
    networks:
      - virons-mcp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9111/health"]
```

## Impact on Timeline

**Original Plan**: 2-4 weeks for 8 servers (all builds)
**Revised Plan**: 1-2 weeks for 10 servers (5 builds + 5 pre-built)

**Week 1**: Deploy 5 pre-built images (1 day) + Build 3 critical (aws-iac, postgres, dynamodb)
**Week 2**: Build remaining 3 (s3-tables, cloudwatch, cloudtrail) + Integration testing

## Recommendation

1. **Immediate**: Deploy 5 pre-built images (kubernetes, terraform, prometheus, redis, github)
2. **Week 1**: Build 3 critical (aws-iac, postgres, dynamodb)
3. **Week 2**: Build 3 observability (s3-tables, cloudwatch, cloudtrail)
4. **Week 3**: Integration testing + Phase 2 planning

This reduces build effort by 50% and accelerates deployment by 50%.
