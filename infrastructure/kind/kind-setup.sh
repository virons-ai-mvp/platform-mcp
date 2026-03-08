#!/usr/bin/env bash
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLUSTER_NAME="virons-mcp-cluster"

echo "🚀 Setting up Virons MCP Kind cluster..."

# Check if kind is installed
if ! command -v kind &> /dev/null; then
    echo "❌ kind is not installed. Install from: https://kind.sigs.k8s.io/docs/user/quick-start/#installation"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Install from: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check if cluster already exists
if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
    echo "⚠️  Cluster ${CLUSTER_NAME} already exists"
    read -p "Delete and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Deleting existing cluster..."
        kind delete cluster --name "${CLUSTER_NAME}"
    else
        echo "✓ Using existing cluster"
        exit 0
    fi
fi

# Create cluster
echo "📦 Creating Kind cluster..."
kind create cluster --config "${SCRIPT_DIR}/kind-config.yaml"

# Wait for cluster to be ready
echo "⏳ Waiting for cluster to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=300s

# Create virons namespace
echo "📁 Creating virons namespace..."
kubectl create namespace virons --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace virons virons.ai/managed=true --overwrite

# Apply network policies
echo "🔒 Applying network policies..."
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: virons-mcp-servers
  namespace: virons
spec:
  podSelector:
    matchLabels:
      virons.ai/type: mcp-server
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              virons.ai/managed: "true"
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              virons.ai/managed: "true"
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: TCP
          port: 53
        - protocol: UDP
          port: 53
EOF

echo ""
echo "================================================================================
✓ Virons MCP Kind Cluster Ready
================================================================================

📦 Cluster: ${CLUSTER_NAME}
📁 Namespace: virons
🔌 Port Range: 9300-9424

🚀 Next Steps:
  1. Deploy MCP servers: make register-server NAME=<server-name>
  2. Check status: kubectl get pods -n virons
  3. View logs: kubectl logs -n virons -l virons.ai/type=mcp-server

📚 Documentation:
  • Helm chart: infrastructure/kind/helm/virons-mcp-server/
  • Makefile: make help

================================================================================
"
