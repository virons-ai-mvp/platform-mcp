#!/bin/bash
# Verify 10 Core MCP Servers are operational (5 pre-built + 5 custom)
# Usage: ./scripts/verify-core-servers.sh

set -e

SERVERS=(
    "kubernetes:9121"
    "terraform:9142"
    "aws-network:9144"
    "postgres:9150"
    "dynamodb:9180"
    "prometheus:9191"
    "redis:9184"
    "cloudwatch:9190"
    "cloudtrail:9102"
    "github:9111"
)

echo "🔍 Verifying 10 Core MCP Servers (5 pre-built + 5 custom)"
echo "=========================================================="

passed=0
failed=0

for server_entry in "${SERVERS[@]}"; do
    name="${server_entry%%:*}"
    port="${server_entry##*:}"

    echo -n "Testing $name ($port)... "

    if curl -sf "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✅"
        ((passed++))
    else
        echo "❌"
        ((failed++))
    fi
done

echo ""
echo "================================"
echo "Results: $passed passed, $failed failed"

if [ $failed -eq 0 ]; then
    echo "🎉 All core servers operational!"
    exit 0
else
    echo "⚠️  Some servers failed. Check docker-compose logs."
    exit 1
fi
