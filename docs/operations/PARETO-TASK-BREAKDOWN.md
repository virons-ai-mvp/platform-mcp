# Pareto MCP Deployment - Task Breakdown

## Overview
Deploy 8 core MCP servers (20%) that deliver 80% of platform value in 2-4 weeks.

## Task List

### Phase 1: Infrastructure Foundation (Week 1)

#### Task 1.1: aws-iac-mcp-server (9143) - 3 days
- [ ] Check if Dockerfile exists in `src/awslabs/aws-iac-mcp-server/`
- [ ] Create Dockerfile if missing (use Python 3.13-slim base)
- [ ] Test local build: `docker build -t virons-aws-iac-mcp src/awslabs/aws-iac-mcp-server/`
- [ ] Create IAM policy: CloudFormation, CDK, Terraform permissions
- [ ] Add to docker-compose.core.yml (port 9143)
- [ ] Test health check: `curl http://localhost:9143/health`
- [ ] Test tool listing: `curl http://localhost:9143/tools | jq`
- [ ] Document basic operations in README

#### Task 1.2: eks-mcp-server (9121) - 2 days
- [ ] Check if Dockerfile exists
- [ ] Create/verify Dockerfile
- [ ] Create IAM policy: EKS read/write permissions
- [ ] Add to docker-compose.core.yml (port 9121)
- [ ] Test health check
- [ ] Test tool: list_clusters
- [ ] Document Kubernetes operations

#### Task 1.3: aws-network-mcp-server (9144) - 2 days
- [ ] Check if Dockerfile exists
- [ ] Create/verify Dockerfile
- [ ] Create IAM policy: VPC, subnet, security group permissions
- [ ] Add to docker-compose.core.yml (port 9144)
- [ ] Test health check
- [ ] Test tool: list_vpcs
- [ ] Document network operations

### Phase 2: Data Layer (Week 2)

#### Task 2.1: postgres-mcp-server (9150) - 2 days
- [ ] Check if Dockerfile exists
- [ ] Create/verify Dockerfile
- [ ] Create IAM policy: RDS permissions
- [ ] Add to docker-compose.core.yml (port 9150)
- [ ] Test health check
- [ ] Test tool: list_databases
- [ ] Document database operations

#### Task 2.2: dynamodb-mcp-server (9180) - 2 days
- [ ] Check if Dockerfile exists
- [ ] Create/verify Dockerfile
- [ ] Create IAM policy: DynamoDB permissions
- [ ] Add to docker-compose.core.yml (port 9180)
- [ ] Test health check
- [ ] Test tool: list_tables
- [ ] Document NoSQL operations

#### Task 2.3: s3-tables-mcp-server (9185) - 1 day
- [ ] Check if Dockerfile exists
- [ ] Create/verify Dockerfile
- [ ] Create IAM policy: S3 permissions
- [ ] Add to docker-compose.core.yml (port 9185)
- [ ] Test health check
- [ ] Test tool: list_buckets
- [ ] Document data lake operations

### Phase 3: Observability (Week 3)

#### Task 3.1: cloudwatch-mcp-server (9190) - 2 days
- [ ] Check if Dockerfile exists
- [ ] Create/verify Dockerfile
- [ ] Create IAM policy: CloudWatch permissions
- [ ] Add to docker-compose.core.yml (port 9190)
- [ ] Test health check
- [ ] Test tool: get_metrics
- [ ] Document monitoring operations

#### Task 3.2: cloudtrail-mcp-server (9102) - 2 days
- [ ] Check if Dockerfile exists
- [ ] Create/verify Dockerfile
- [ ] Create IAM policy: CloudTrail permissions
- [ ] Add to docker-compose.core.yml (port 9102)
- [ ] Test health check
- [ ] Test tool: lookup_events
- [ ] Document audit operations

### Phase 4: Integration & Testing (Week 4)

#### Task 4.1: Gateway Integration (2 days)
- [ ] Update virons-infrastructure-mcp-server with UPSTREAM_CONFIG
- [ ] Add all 8 servers to upstream registry
- [ ] Test gateway aggregation: `curl http://localhost:9000/tools`
- [ ] Verify tool count increased
- [ ] Test tool execution through gateway

#### Task 4.2: End-to-End Testing (3 days)
- [ ] Test infrastructure deployment flow
- [ ] Test data persistence flow
- [ ] Test monitoring flow
- [ ] Test audit trail flow
- [ ] Create integration test script
- [ ] Document test scenarios

#### Task 4.3: Documentation (2 days)
- [ ] Update README.md with 8 core servers
- [ ] Create quickstart guide
- [ ] Document common workflows
- [ ] Create troubleshooting guide
- [ ] Update architecture diagrams

#### Task 4.4: Production Readiness (1 day)
- [ ] Security review (IAM policies)
- [ ] Performance testing (load test)
- [ ] Create deployment runbook
- [ ] Create rollback procedure
- [ ] Tag release: v1.0.0-core

## Execution Strategy

### Daily Standup Questions
1. Which server are you deploying today?
2. Any blockers (missing Dockerfile, IAM issues)?
3. Health check passing?

### Definition of Done (Per Server)
- [ ] Dockerfile exists and builds successfully
- [ ] IAM policy defined (least privilege)
- [ ] Added to docker-compose.core.yml
- [ ] Health check returns 200 OK
- [ ] At least 1 tool tested successfully
- [ ] Basic documentation written

### Risk Mitigation
- **Missing Dockerfile**: Create minimal Dockerfile (5 lines)
- **IAM Permission Denied**: Start with broad permissions, narrow later
- **Health Check Fails**: Check logs, verify port, check AWS credentials
- **Tool Execution Fails**: Test with AWS CLI first, then debug MCP server

## Quick Commands

```bash
# Check if server exists
ls -la src/awslabs/<server-name>-mcp-server/

# Build single server
docker build -t virons-<server>-mcp src/awslabs/<server-name>-mcp-server/

# Run single server
docker run -p <port>:<port> -v ~/.aws:/root/.aws:ro virons-<server>-mcp

# Test health
curl http://localhost:<port>/health

# List tools
curl http://localhost:<port>/tools | jq '.tools[].name'

# Deploy all 8
docker-compose -f docker-compose.core.yml up -d

# Verify all 8
./scripts/verify-core-servers.sh

# Check logs
docker-compose -f docker-compose.core.yml logs -f <service>
```

## Success Metrics

- **Week 1**: 3 infrastructure servers deployed
- **Week 2**: 6 total servers deployed (3 data added)
- **Week 3**: 8 total servers deployed (2 observability added)
- **Week 4**: End-to-end test passing, documentation complete

## Blockers & Escalation

**Common Blockers:**
1. Missing Dockerfile → Create minimal one
2. IAM permission denied → Broaden policy temporarily
3. Port conflict → Check `docker ps`, kill conflicting process
4. AWS credentials → Verify `~/.aws/credentials` exists

**Escalation Path:**
- Blocker > 4 hours → Escalate to DevOps Engineer
- Blocker > 1 day → Escalate to AWS Architect
- Critical blocker → Skip server, move to next, circle back

## Phase 2 Planning (32 Remaining Servers)

After 8 core servers deployed, prioritize next batch:
- IAM management (iam-mcp-server)
- Cost optimization (cost-explorer-mcp-server)
- Additional databases (mysql, redshift)
- ML services (sagemaker, bedrock)
- Advanced monitoring (prometheus)

**Estimated Timeline**: 3-6 months for remaining 32 servers
