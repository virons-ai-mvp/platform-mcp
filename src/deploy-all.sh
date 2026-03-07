#!/bin/bash
# Build and deploy all Virons MCP servers to Kind cluster

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
KIND_CLUSTER="virons-local"

echo "🚀 Building and deploying Virons MCP servers..."
echo ""

# MCP servers to build and deploy
SERVERS=(
    "virons-infrastructure-mcp-server"
)

cd "$SCRIPT_DIR"

for SERVER in "${SERVERS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📦 Building $SERVER..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Build Docker image from workspace root
    cd "$WORKSPACE_ROOT"
    docker build \
        -f "src/$SERVER/Dockerfile" \
        -t "$SERVER:0.1.0" \
        . || { echo "❌ Build failed for $SERVER"; exit 1; }

    echo "✅ Built $SERVER:0.1.0"
    echo ""

    echo "📥 Loading image into Kind cluster..."
    kind load docker-image "$SERVER:0.1.0" --name "$KIND_CLUSTER" || { echo "❌ Failed to load image"; exit 1; }
    echo "✅ Image loaded"
    echo ""

    echo "🎯 Deploying to Kubernetes..."

    # Check if Helm release exists
    cd "$SCRIPT_DIR"
    if helm list -q | grep -q "^${SERVER%-mcp-server}$"; then
        echo "♻️  Upgrading existing release..."
        helm upgrade "${SERVER%-mcp-server}" "$SERVER/helm/${SERVER%-mcp-server}" || { echo "❌ Upgrade failed"; exit 1; }
    else
        echo "🆕 Installing new release..."
        helm install "${SERVER%-mcp-server}" "$SERVER/helm/${SERVER%-mcp-server}" || { echo "❌ Install failed"; exit 1; }
    fi

    echo "✅ Deployed $SERVER"
    echo ""

    # Delete old pods to force restart with new image
    echo "🔄 Restarting pods..."
    kubectl delete pod -l "app=${SERVER%-mcp-server}" --ignore-not-found=true

    echo "⏳ Waiting for pod to be ready..."
    kubectl wait --for=condition=ready pod -l "app=${SERVER%-mcp-server}" --timeout=60s || {
        echo "⚠️  Pod not ready, checking logs..."
        kubectl logs -l "app=${SERVER%-mcp-server}" --tail=20
    }

    echo "✅ $SERVER is running"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 All MCP servers deployed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Deployment status:"
kubectl get pods -l 'app in (virons-infrastructure)'
echo ""
echo "🔍 To view logs:"
echo "  kubectl logs -l app=virons-infrastructure -f"
echo ""
echo "🌐 To access services:"
echo "  kubectl port-forward svc/virons-infrastructure 8080:8080"
