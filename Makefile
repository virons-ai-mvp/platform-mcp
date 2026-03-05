# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

.PHONY: help setup-cluster delete-cluster status register-server unregister-server

CLUSTER_NAME := virons-mcp-cluster
NAMESPACE := virons
HELM_CHART := infrastructure/kind/helm/virons-mcp-server

help: ## Show this help message
	@echo "Virons MCP Infrastructure - Make targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

setup-cluster: ## Create Kind cluster and setup infrastructure
	@echo "🚀 Setting up Virons MCP cluster..."
	@bash infrastructure/kind/kind-setup.sh

delete-cluster: ## Delete Kind cluster
	@echo "🗑️  Deleting cluster $(CLUSTER_NAME)..."
	@kind delete cluster --name $(CLUSTER_NAME)

status: ## Show cluster status
	@echo "📊 Cluster Status:"
	@kubectl cluster-info --context kind-$(CLUSTER_NAME) || echo "❌ Cluster not running"
	@echo ""
	@echo "📦 MCP Servers:"
	@kubectl get pods -n $(NAMESPACE) -l virons.ai/type=mcp-server || echo "No servers deployed"

register-server: ## Register MCP server (usage: make register-server NAME=infrastructure PORT=9300)
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Error: NAME is required"; \
		echo "Usage: make register-server NAME=infrastructure PORT=9300"; \
		exit 1; \
	fi
	@if [ -z "$(PORT)" ]; then \
		echo "❌ Error: PORT is required"; \
		echo "Usage: make register-server NAME=infrastructure PORT=9300"; \
		exit 1; \
	fi
	@echo "📦 Registering $(NAME) MCP server on port $(PORT)..."
	@helm upgrade --install \
		virons-$(NAME)-mcp-server \
		$(HELM_CHART) \
		--namespace $(NAMESPACE) \
		--create-namespace \
		--set server.name=$(NAME) \
		--set server.port=$(PORT) \
		--wait
	@echo "✓ Server registered successfully"

unregister-server: ## Unregister MCP server (usage: make unregister-server NAME=infrastructure)
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Error: NAME is required"; \
		echo "Usage: make unregister-server NAME=infrastructure"; \
		exit 1; \
	fi
	@echo "🗑️  Unregistering $(NAME) MCP server..."
	@helm uninstall virons-$(NAME)-mcp-server --namespace $(NAMESPACE)
	@echo "✓ Server unregistered successfully"
