#!/bin/bash
# Deploy 8 Core MCP Servers (Pareto 20/80)
# Usage: ./scripts/deploy-core-mcp-servers.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Deploying 8 Core MCP Servers (Pareto 20/80)"
echo "================================================"

# Core servers in deployment order
SERVERS=(
    "aws-iac-mcp-server:9143"
    "eks-mcp-server:9121"
    "aws-network-mcp-server:9144"
    "postgres-mcp-server:9150"
    "dynamodb-mcp-server:9180"
    "s3-tables-mcp-server:9185"
    "cloudwatch-mcp-server:9190"
    "cloudtrail-mcp-server:9102"
)

# Check if server exists
check_server() {
    local server_name=$1
    local server_path="$PROJECT_ROOT/src/awslabs/$server_name"

    if [ ! -d "$server_path" ]; then
        echo "❌ Server not found: $server_name"
        return 1
    fi
    echo "✅ Found: $server_name"
    return 0
}

# Deploy single server
deploy_server() {
    local server_name=$1
    local port=$2

    echo ""
    echo "📦 Deploying $server_name on port $port..."

    # Check if server exists
    if ! check_server "$server_name"; then
        return 1
    fi

    # Build and start container
    docker-compose up -d "virons-${server_name%-mcp-server}-mcp" 2>/dev/null || {
        echo "⚠️  Container not in docker-compose.yml, skipping..."
        return 0
    }

    # Wait for health check
    echo "⏳ Waiting for health check..."
    for i in {1..30}; do
        if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
            echo "✅ $server_name is healthy"
            return 0
        fi
        sleep 2
    done

    echo "❌ $server_name failed health check"
    return 1
}

# Main deployment
main() {
    cd "$PROJECT_ROOT"

    echo ""
    echo "Step 1: Checking server availability..."
    echo "========================================"

    for server_entry in "${SERVERS[@]}"; do
        server_name="${server_entry%%:*}"
        check_server "$server_name"
    done

    echo ""
    echo "Step 2: Deploying servers..."
    echo "============================"

    deployed=0
    failed=0

    for server_entry in "${SERVERS[@]}"; do
        server_name="${server_entry%%:*}"
        port="${server_entry##*:}"

        if deploy_server "$server_name" "$port"; then
            ((deployed++))
        else
            ((failed++))
        fi
    done

    echo ""
    echo "================================================"
    echo "Deployment Summary"
    echo "================================================"
    echo "✅ Deployed: $deployed"
    echo "❌ Failed: $failed"
    echo "📊 Total: ${#SERVERS[@]}"

    if [ $failed -eq 0 ]; then
        echo ""
        echo "🎉 All core servers deployed successfully!"
        echo ""
        echo "Next steps:"
        echo "1. Test gateway: curl http://localhost:9000/tools | jq"
        echo "2. Check services: docker-compose ps"
        echo "3. View logs: docker-compose logs -f"
    else
        echo ""
        echo "⚠️  Some servers failed to deploy. Check logs above."
        return 1
    fi
}

main "$@"
