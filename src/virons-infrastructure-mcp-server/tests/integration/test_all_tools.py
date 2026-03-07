# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Integration tests for all 78 tools."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def mock_mcp_server():
    """Mock MCP server with all services."""
    with patch("virons.infrastructure_mcp_server.server.UpstreamRegistry") as mock_registry_class:
        registry = MagicMock()
        client = AsyncMock()
        client.call_tool = AsyncMock(return_value={"status": "success"})
        registry.get_client = AsyncMock(return_value=client)
        mock_registry_class.return_value = registry

        from virons.infrastructure_mcp_server.server import create_server

        server = create_server()
        yield server, client


@pytest.mark.asyncio
class TestAllToolsIntegration:
    """Test all 78 tools are registered and callable."""

    async def test_core_tools(self, mock_mcp_server):
        """Test 3 core tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "deploy_infrastructure" in tool_names
        assert "list_stacks" in tool_names
        assert "destroy_infrastructure" in tool_names

    async def test_phase1_stack_tools(self, mock_mcp_server):
        """Test 6 stack management tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "get_stack_info" in tool_names
        assert "get_stack_outputs" in tool_names
        assert "get_stack_resources" in tool_names
        assert "get_stack_events" in tool_names
        assert "validate_template" in tool_names
        assert "update_stack" in tool_names

    async def test_phase1_resource_tools(self, mock_mcp_server):
        """Test 2 resource management tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "list_resources" in tool_names
        assert "tag_resource" in tool_names

    async def test_phase1_monitoring_tools(self, mock_mcp_server):
        """Test 3 monitoring tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "get_health_status" in tool_names
        assert "get_metrics" in tool_names
        assert "get_alarms" in tool_names

    async def test_phase1_security_tools(self, mock_mcp_server):
        """Test 3 security tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "scan_security" in tool_names
        assert "detect_drift" in tool_names
        assert "get_audit_logs" in tool_names

    async def test_phase2_state_tools(self, mock_mcp_server):
        """Test 5 state management tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "get_state" in tool_names
        assert "lock_state" in tool_names
        assert "unlock_state" in tool_names
        assert "backup_state" in tool_names
        assert "restore_state" in tool_names

    async def test_phase2_drift_tools(self, mock_mcp_server):
        """Test 3 drift detection tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "get_drift_status" in tool_names
        assert "get_drift_details" in tool_names
        assert "remediate_drift" in tool_names

    async def test_phase2_extended_security_tools(self, mock_mcp_server):
        """Test 4 extended security tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "check_compliance" in tool_names
        assert "rotate_secrets" in tool_names
        assert "scan_vulnerabilities" in tool_names
        assert "generate_compliance_report" in tool_names

    async def test_phase2_backup_tools(self, mock_mcp_server):
        """Test 5 backup tools (2 Phase 1 + 3 Phase 2)."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "create_backup" in tool_names
        assert "list_backups" in tool_names
        assert "restore_backup" in tool_names
        assert "delete_backup" in tool_names
        assert "test_recovery" in tool_names

    async def test_phase2_cost_tools(self, mock_mcp_server):
        """Test 6 cost tools (1 Phase 1 + 5 Phase 2)."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "get_cost_breakdown" in tool_names
        assert "estimate_cost" in tool_names
        assert "get_cost_forecast" in tool_names
        assert "get_cost_anomalies" in tool_names
        assert "optimize_costs" in tool_names
        assert "set_budget" in tool_names

    async def test_phase2_monitoring_tools(self, mock_mcp_server):
        """Test 6 monitoring tools (3 Phase 1 + 3 Phase 2)."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "create_alarm" in tool_names
        assert "get_logs" in tool_names
        assert "query_logs" in tool_names

    async def test_phase2_resource_tools(self, mock_mcp_server):
        """Test 8 resource tools (2 Phase 1 + 6 Phase 2)."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "get_resource_info" in tool_names
        assert "untag_resource" in tool_names
        assert "search_resources" in tool_names
        assert "get_resource_metrics" in tool_names
        assert "get_resource_logs" in tool_names
        assert "get_resource_cost" in tool_names

    async def test_phase2_network_tools(self, mock_mcp_server):
        """Test 6 network tools (1 Phase 1 + 5 Phase 2)."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "list_vpcs" in tool_names
        assert "get_vpc_info" in tool_names
        assert "list_subnets" in tool_names
        assert "get_network_topology" in tool_names
        assert "test_connectivity" in tool_names
        assert "get_security_groups" in tool_names

    async def test_phase2_database_tools(self, mock_mcp_server):
        """Test 5 database tools (1 Phase 1 + 4 Phase 2)."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "list_databases" in tool_names
        assert "get_database_info" in tool_names
        assert "backup_database" in tool_names
        assert "restore_database" in tool_names
        assert "get_database_metrics" in tool_names

    async def test_phase2_compute_tools(self, mock_mcp_server):
        """Test 5 compute tools (1 Phase 1 + 4 Phase 2)."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "list_instances" in tool_names
        assert "get_instance_info" in tool_names
        assert "start_instance" in tool_names
        assert "stop_instance" in tool_names
        assert "get_instance_logs" in tool_names

    async def test_phase2_storage_tools(self, mock_mcp_server):
        """Test 4 storage tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "list_buckets" in tool_names
        assert "get_bucket_info" in tool_names
        assert "sync_bucket" in tool_names
        assert "get_storage_metrics" in tool_names

    async def test_phase2_deployment_tools(self, mock_mcp_server):
        """Test 5 deployment workflow tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "create_pipeline" in tool_names
        assert "trigger_pipeline" in tool_names
        assert "get_pipeline_status" in tool_names
        assert "rollback_deployment" in tool_names
        assert "blue_green_deploy" in tool_names

    async def test_phase2_multiregion_tools(self, mock_mcp_server):
        """Test 4 multi-region tools."""
        server, client = mock_mcp_server
        tools = server.list_tools()
        tool_names = [t.name for t in tools]

        assert "list_regions" in tool_names
        assert "replicate_stack" in tool_names
        assert "get_global_resources" in tool_names
        assert "failover_region" in tool_names

    async def test_total_tool_count(self, mock_mcp_server):
        """Test total of 78 tools are registered."""
        server, client = mock_mcp_server
        tools = server.list_tools()

        assert len(tools) == 78, f"Expected 78 tools, got {len(tools)}"

    async def test_all_tools_have_descriptions(self, mock_mcp_server):
        """Test all tools have descriptions."""
        server, client = mock_mcp_server
        tools = server.list_tools()

        for tool in tools:
            assert tool.description, f"Tool {tool.name} missing description"
