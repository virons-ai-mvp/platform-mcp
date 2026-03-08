#!/bin/bash
# Discover tools from awslabs MCP servers

AWSLABS_SERVERS=(
  "eks-mcp-server"
  "cfn-mcp-server"
  "iam-mcp-server"
  "cost-explorer-mcp-server"
  "cloudwatch-mcp-server"
  "aws-network-mcp-server"
  "terraform-mcp-server"
  "amazon-bedrock-agentcore-mcp-server"
  "amazon-neptune-mcp-server"
  "openapi-mcp-server"
  "elasticache-mcp-server"
)

echo "# AWS Labs MCP Server Tools"
echo ""

for server in "${AWSLABS_SERVERS[@]}"; do
  echo "## $server"

  # Check README for tools
  readme="src/awslabs/$server/README.md"
  if [ -f "$readme" ]; then
    grep -A 2 "^#### \`" "$readme" | grep -E "^#### \`|^[A-Z]" | head -20
  fi

  echo ""
done
