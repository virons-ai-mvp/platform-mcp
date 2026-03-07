#!/bin/bash
# Deploy AWS Labs MCP Servers - Priority 2 (Infrastructure)

set -e

AWS_REGION="${AWS_REGION:-us-east-1}"
AWS_PROFILE="${AWS_PROFILE:-default}"

echo "🚀 Deploying Priority 2: Infrastructure AWS Labs MCP Servers"
echo "AWS Region: $AWS_REGION"
echo "AWS Profile: $AWS_PROFILE"
echo ""

# Priority 2: Infrastructure servers
declare -A SERVERS=(
    ["cdk-mcp-server"]="9140"
    ["cfn-mcp-server"]="9141"
    ["terraform-mcp-server"]="9142"
    ["aws-iac-mcp-server"]="9143"
)

# Start each server
for server in "${!SERVERS[@]}"; do
    port="${SERVERS[$server]}"
    echo "📦 Starting $server on port $port..."

    # Start with uvx in background
    AWS_REGION=$AWS_REGION AWS_PROFILE=$AWS_PROFILE \
    uvx "awslabs.${server}@latest" > "/tmp/${server}.log" 2>&1 &

    pid=$!
    echo "   PID: $pid"
    echo "   Logs: /tmp/${server}.log"

    # Wait a bit for startup
    sleep 3
done

echo ""
echo "⏳ Waiting for servers to start..."
sleep 5

echo ""
echo "🧪 Testing server health..."
for server in "${!SERVERS[@]}"; do
    port="${SERVERS[$server]}"
    echo -n "  $server (:$port)... "

    if curl -s -f "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✅ OK"
    else
        echo "❌ FAILED (check /tmp/${server}.log)"
    fi
done

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "  1. Check logs: tail -f /tmp/*.log"
echo "  2. Test Infrastructure MCP: curl http://localhost:9530/tools | jq"
