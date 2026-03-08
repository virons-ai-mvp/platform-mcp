# AWS Labs MCP Servers Deployment Plan

## Required Servers (15 total)

Virons orchestrators delegate to these 15 awslabs MCP servers:

### ✅ Ready to Deploy (12 servers with Dockerfiles)

| Server | Port | Used By | Status |
|--------|------|---------|--------|
| eks-mcp-server | 9001 | virons-infrastructure-mcp | ✅ Dockerfile |
| ecs-mcp-server | 9002 | virons-infrastructure-mcp | ⚠️ No Dockerfile |
| cfn-mcp-server | 9003 | virons-infrastructure-mcp | ✅ Dockerfile |
| iam-mcp-server | 9004 | virons-infrastructure-mcp, virons-security-mcp | ✅ Dockerfile |
| cost-explorer-mcp-server | 9005 | virons-infrastructure-mcp | ✅ Dockerfile |
| cloudwatch-mcp-server | 9006 | virons-infrastructure-mcp | ✅ Dockerfile |
| aws-network-mcp-server | 9007 | virons-infrastructure-mcp | ✅ Dockerfile |
| terraform-mcp-server | 9010 | virons-infrastructure-mcp | ✅ Dockerfile |
| amazon-bedrock-agentcore-mcp-server | 9020 | virons-ml-mcp | ✅ Dockerfile |
| sagemaker-ai-mcp-server | 9021 | virons-ml-mcp | ⚠️ No Dockerfile |
| amazon-neptune-mcp-server | 9030 | virons-forensic-mcp | ✅ Dockerfile |
| core-mcp-server | 9040 | virons-compliance-mcp | ✅ Dockerfile |
| git-repo-research-mcp-server | 9070 | virons-dev-mcp | ⚠️ No Dockerfile |
| openapi-mcp-server | 9080 | virons-api-mcp | ✅ Dockerfile |
| elasticache-mcp-server | 9081 | virons-api-mcp | ✅ Dockerfile |

### ⚠️ Need Dockerfiles (3 servers)

1. **ecs-mcp-server** - Has pyproject.toml, needs Dockerfile
2. **git-repo-research-mcp-server** - Has pyproject.toml, needs Dockerfile
3. **sagemaker-ai-mcp-server** - Has pyproject.toml, needs Dockerfile

## Deployment Strategy

### Option 1: Containers (Recommended)
Add all 15 servers to `docker-compose.core.yml`:
- 12 servers ready to build
- 3 servers need Dockerfile generation first

**Pros**: Isolated, scalable, consistent with existing architecture
**Cons**: Higher resource usage (15 containers)

### Option 2: Subprocess
Run awslabs servers as subprocesses from orchestrators:
- Use `mcp` CLI to start servers
- Orchestrators manage lifecycle

**Pros**: Lower resource usage
**Cons**: Complex lifecycle management, harder to scale

### Option 3: Hybrid (Recommended for MVP)
- **Containers**: 12 servers with Dockerfiles (deploy immediately)
- **Mock**: 3 servers without Dockerfiles (keep mock responses in orchestrators)
- **Future**: Add real implementations when needed

## Recommendation

**Deploy 12 containerized awslabs servers immediately**:
- Add to docker-compose.core.yml
- Keep 3 missing servers as mocks in orchestrators
- Total: 9 Virons orchestrators + 12 awslabs servers = 21 containers

This provides real AWS integration while keeping deployment simple.
