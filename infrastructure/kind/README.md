# Virons MCP Infrastructure

Shared Kind cluster infrastructure for all virons MCP servers.

## Overview

This directory contains the Infrastructure Domain for virons MCP servers:
- Kind cluster configuration
- Helm charts for deployment
- Network policies for security
- Makefile for cluster management

## Quick Start

```bash
# Setup cluster
make setup-cluster

# Check status
make status

# Register a server
make register-server NAME=infrastructure PORT=9300

# Unregister a server
make unregister-server NAME=infrastructure

# Delete cluster
make delete-cluster
```

## Architecture

```
infrastructure/kind/
├── kind-config.yaml           # Kind cluster configuration
├── kind-setup.sh              # Cluster setup script
└── helm/
    └── virons-mcp-server/     # Shared Helm chart
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
            ├── deployment.yaml
            └── service.yaml
```

## Cluster Configuration

- **Name**: `virons-mcp-cluster`
- **Namespace**: `virons`
- **Port Range**: 9300-9424
- **Nodes**: 1 control-plane + 1 worker
- **Network**: Calico with network policies

## Helm Chart

The shared Helm chart deploys MCP servers with:
- DORA Art 11 health checks (liveness, readiness)
- Resource limits and requests
- Security context (non-root, capabilities dropped)
- Network policies
- Compliance labels

## Usage

### Deploy a Server

```bash
# Using Makefile
make register-server NAME=infrastructure PORT=9300

# Using Helm directly
helm upgrade --install \
  virons-infrastructure-mcp-server \
  infrastructure/kind/helm/virons-mcp-server \
  --namespace virons \
  --set server.name=infrastructure \
  --set server.port=9300
```

### Check Server Status

```bash
kubectl get pods -n virons -l virons.ai/type=mcp-server
kubectl logs -n virons -l app=infrastructure-mcp-server
```

## Compliance

All deployed servers include:
- **BaFin MaRisk AT 8.1**: Audit trail integration
- **GDPR Art 25, 32**: Data residency (eu-central-1), security
- **DORA Art 11**: Health monitoring, capacity planning
- **EU AI Act**: Model card validation hooks

## DDD Context

| Key | Value |
|-----|-------|
| **Domain** | Infrastructure Domain |
| **Bounded Context** | Kubernetes Cluster Management |
| **Aggregates** | Kind Cluster, Helm Releases |

## Navigation

← [Platform MCP Root](../../)
