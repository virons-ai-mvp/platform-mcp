# MCP Deployment Status

**Date**: 2026-03-08
**Status**: ⚠️ Architecture Issue Identified

## What We Built

### ✅ 9 Virons Orchestrator MCP Servers
All implemented as orchestrators delegating to awslabs + custom services:

1. **virons-infrastructure-mcp** (9100) - AWS infrastructure orchestrator
2. **virons-forensic-mcp** (9300) - Forensic accounting orchestrator
3. **virons-ml-mcp** (9420) - ML/AI orchestrator
4. **virons-blockchain-mcp** (9430) - Ledger orchestrator
5. **virons-dev-mcp** (9500) - DevOps orchestrator
6. **virons-api-mcp** (9540) - API gateway orchestrator
7. **virons-prompts-mcp** (9550) - Prompt library orchestrator
8. **virons-compliance-mcp** (9560) - Compliance orchestrator
9. **virons-security-mcp** (9570) - Security orchestrator

### ✅ 12 AWS Labs MCP Servers Identified
- eks-mcp-server
- cfn-mcp-server
- iam-mcp-server
- cost-explorer-mcp-server
- cloudwatch-mcp-server
- aws-network-mcp-server
- terraform-mcp-server
- amazon-bedrock-agentcore-mcp-server
- amazon-neptune-mcp-server
- core-mcp-server
- openapi-mcp-server
- elasticache-mcp-server

### ✅ Docker Compose Configuration
- Created `docker-compose.awslabs.yml` with all 21 services
- Fixed build contexts for all servers
- Configured dependencies between orchestrators and delegates

## Critical Issue Discovered

**MCP servers use stdio protocol, not HTTP**:
- MCP servers communicate via stdin/stdout
- They cannot run as standalone HTTP containers
- They need an MCP gateway/client to invoke them

## Current Architecture Problem

```
❌ Current (doesn't work):
   HTTP Client → virons-infrastructure-mcp:9100 (stdio server, no HTTP listener)
                 ↓
                 eks-mcp-server:9001 (stdio server, no HTTP listener)
```

## Solution Options

### Option 1: MCP Gateway (Recommended)
Use virons-mcp-gateway to route HTTP → stdio:
```
✅ Correct:
   HTTP Client → virons-mcp-gateway:9000 (HTTP listener)
                 ↓ (stdio)
                 virons-infrastructure-mcp (stdio)
                 ↓ (stdio)
                 eks-mcp-server (stdio)
```

### Option 2: HTTP Wrapper
Wrap each MCP server with FastAPI/Flask HTTP endpoint that:
- Accepts HTTP requests
- Invokes MCP server via stdio
- Returns HTTP response

### Option 3: Subprocess Mode
Run awslabs servers as subprocesses within orchestrators:
- Orchestrator spawns awslabs server process
- Communicates via stdio pipes
- No separate containers needed

## Recommendation

**Use existing virons-mcp-gateway**:
1. Gateway already exists and handles HTTP → stdio
2. Register all 9 orchestrators in gateway config
3. Orchestrators invoke awslabs servers via subprocess/stdio
4. No need for 21 separate containers

## Next Steps

1. Update virons-mcp-gateway config to register 9 orchestrators
2. Modify orchestrators to invoke awslabs servers as subprocesses
3. Test gateway → orchestrator → awslabs flow
4. Deploy as: 1 gateway + 9 orchestrator containers (10 total, not 21)
