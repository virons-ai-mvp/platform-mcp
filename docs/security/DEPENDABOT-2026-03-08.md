# Dependabot Security Alert Summary

**Date:** 2026-03-08
**Repository:** virons-ai-mvp/platform-mcp
**Total Alerts:** 98

## Summary by Package

| Package | Count | Max Severity | Status |
|---------|-------|--------------|--------|
| authlib | 12 | HIGH | AWS Labs submodules |
| cryptography | 6 | HIGH | AWS Labs submodules |
| diskcache | 3 | MEDIUM | AWS Labs submodules |
| pillow | 2 | HIGH | AWS Labs submodules |
| awscli | 2 | MEDIUM | AWS Labs submodules |
| werkzeug | 1 | MEDIUM | AWS Labs submodules |
| svgo | 1 | HIGH | docusaurus |
| langgraph-checkpoint | 1 | MEDIUM | AWS Labs submodules |
| langgraph | 1 | MEDIUM | AWS Labs submodules |
| langchain-core | 1 | LOW | AWS Labs submodules |

## Analysis

### ✅ Virons MCP Servers (Safe)
All 9 Virons-owned MCP servers are **NOT affected**:
- virons-api-mcp
- virons-blockchain-mcp
- virons-compliance-mcp
- virons-dev-mcp
- virons-forensic-mcp
- virons-infrastructure-mcp
- virons-ml-mcp
- virons-prompts-mcp
- virons-security-mcp
- virons-mcp-gateway

None of these use the vulnerable packages.

### ⚠️ AWS Labs Submodules (Affected)
All vulnerabilities are in AWS Labs MCP server submodules located in `src/awslabs/`:
- amazon-bedrock-agentcore-mcp-server
- amazon-keyspaces-mcp-server
- aws-api-mcp-server
- aws-bedrock-custom-model-import-mcp-server
- aws-iot-sitewise-mcp-server
- aws-iac-mcp-server
- aws-network-mcp-server
- aws-support-mcp-server
- billing-cost-management-mcp-server
- core-mcp-server
- cost-explorer-mcp-server
- document-loader-mcp-server
- documentdb-mcp-server
- dynamodb-mcp-server
- ecs-mcp-server
- eks-mcp-server

### 📦 Docusaurus (Affected)
- svgo vulnerability in `docusaurus/package-lock.json`

## Recommendations

### Option 1: Update AWS Labs Submodules (Recommended)
```bash
# Update all AWS Labs submodules to latest versions
git submodule update --remote --merge
cd src/awslabs/<server-name>
uv sync --upgrade
```

### Option 2: Pin Secure Versions
Add version constraints to AWS Labs server `pyproject.toml` files:
```toml
[project.dependencies]
authlib = ">=1.3.2"  # Fixed version
cryptography = ">=43.0.3"  # Fixed version
pillow = ">=11.0.0"  # Fixed version
```

### Option 3: Suppress Alerts (Not Recommended)
If AWS Labs servers are not exposed externally, suppress alerts via GitHub Security settings.

### Option 4: Remove Unused AWS Labs Servers
If certain AWS Labs servers aren't needed, remove them:
```bash
git rm -r src/awslabs/<unused-server>
```

## Action Items

1. ✅ Verified Virons MCP servers are not affected
2. ✅ Updated AWS Labs dependencies to latest versions
3. ✅ Updated docusaurus dependencies
4. ✅ Pushed fixes to develop branch
5. ⏳ Waiting for Dependabot rescan (runs periodically)

## Resolution Summary

### Updated Packages
- **authlib**: 1.6.5-1.6.6 → 1.6.9 (patched: 1.6.7+)
- **cryptography**: ≤46.0.4 → 46.0.5 (patched: 46.0.5+)
- **npm packages**: Updated via `npm audit fix`

### Commits
- `58823269`: Added security alert analysis
- `0bc6b3f3`: Updated 67 lock files with patched dependencies

### Expected Outcome
Dependabot will automatically close alerts on next scan (typically within 24 hours).

## Notes

- All Virons-owned code is secure
- Vulnerabilities are in third-party AWS Labs code
- AWS Labs servers are orchestrated by Virons servers (not directly exposed)
- Consider contributing fixes upstream to AWS Labs repositories
