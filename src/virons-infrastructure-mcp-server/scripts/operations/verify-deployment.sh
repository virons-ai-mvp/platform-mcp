#!/bin/bash
# Verification script for virons-infrastructure-mcp-server deployment

set -e

echo "🔍 Verifying virons-infrastructure-mcp-server deployment..."
echo ""

# Check pod status
echo "📦 Pod Status:"
kubectl get pods -l app=virons-infrastructure
echo ""

# Check if pod is ready
POD_NAME=$(kubectl get pod -l app=virons-infrastructure -o jsonpath='{.items[0].metadata.name}')
POD_STATUS=$(kubectl get pod "$POD_NAME" -o jsonpath='{.status.phase}')

if [ "$POD_STATUS" != "Running" ]; then
    echo "❌ Pod is not running (status: $POD_STATUS)"
    echo "Logs:"
    kubectl logs "$POD_NAME" --tail=20
    exit 1
fi

echo "✅ Pod is running"
echo ""

# Port forward in background
echo "🔌 Setting up port forward..."
kubectl port-forward svc/virons-infrastructure 8080:8080 > /dev/null 2>&1 &
PF_PID=$!
sleep 3

# Test liveness endpoint
echo "🏥 Testing /health/live..."
LIVE_RESPONSE=$(curl -s http://localhost:8080/health/live)
LIVE_STATUS=$(echo "$LIVE_RESPONSE" | jq -r '.status' 2>/dev/null || echo "error")

if [ "$LIVE_STATUS" = "ok" ]; then
    echo "✅ Liveness check passed"
else
    echo "❌ Liveness check failed: $LIVE_RESPONSE"
    kill $PF_PID 2>/dev/null
    exit 1
fi
echo ""

# Test readiness endpoint
echo "🚦 Testing /health/ready..."
READY_RESPONSE=$(curl -s http://localhost:8080/health/ready)
READY_STATUS=$(echo "$READY_RESPONSE" | jq -r '.status' 2>/dev/null || echo "error")

if [ "$READY_STATUS" = "healthy" ]; then
    echo "✅ Readiness check passed"
else
    echo "❌ Readiness check failed: $READY_RESPONSE"
    kill $PF_PID 2>/dev/null
    exit 1
fi
echo ""

# Test metrics endpoint
echo "📊 Testing /metrics..."
METRICS_RESPONSE=$(curl -s http://localhost:8080/metrics)
MCP_METRICS=$(echo "$METRICS_RESPONSE" | grep "^# HELP mcp_" | wc -l | tr -d ' ')

if [ "$MCP_METRICS" -gt 0 ]; then
    echo "✅ Metrics endpoint working ($MCP_METRICS MCP metrics found)"
    echo ""
    echo "Available metrics:"
    echo "$METRICS_RESPONSE" | grep "^# HELP mcp_"
else
    echo "⚠️  No MCP metrics found yet (metrics will appear after tool calls)"
    echo "   But metrics endpoint is accessible"
fi
echo ""

# Cleanup
kill $PF_PID 2>/dev/null

# Check service
echo "🌐 Service Status:"
kubectl get svc virons-infrastructure
echo ""

# Check deployment
echo "🚀 Deployment Status:"
kubectl get deployment virons-infrastructure
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All verification checks passed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Deployment Details:"
echo "  Pod: $POD_NAME"
echo "  Status: $POD_STATUS"
echo "  Liveness: $LIVE_STATUS"
echo "  Readiness: $READY_STATUS"
echo "  Metrics: $MCP_METRICS custom metrics"
echo ""
echo "🎯 Next Steps:"
echo "  1. Test MCP tool calls (requires upstream servers)"
echo "  2. Configure Prometheus scraping"
echo "  3. Set up alerting rules"
echo "  4. Enable audit trail storage"
echo ""
