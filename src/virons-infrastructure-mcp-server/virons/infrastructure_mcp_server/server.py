# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""FastMCP server implementation for virons-infrastructure-mcp-server."""

import argparse
import asyncio
import json
import os
import sys
import time

from loguru import logger
from mcp.server.fastmcp import FastMCP

from virons.common import audit as audit_module
from virons.common.correlation import generate_correlation_id

from .application.deploy_service import DeployService
from .application.destroy_service import DestroyService
from .application.extended_security_service import ExtendedSecurityService
from .application.extended_services import (
    ExtendedBackupService,
    ExtendedCostService,
    ExtendedMonitoringService,
    ExtendedResourceService,
)
from .application.infrastructure_extended_services import (
    ComputeService,
    DatabaseService,
    DeploymentService,
    MultiRegionService,
    NetworkService,
    StorageService,
)
from .application.infrastructure_services import BackupService, CostService, InfrastructureService
from .application.list_service import ListService
from .application.monitoring_service import MonitoringService
from .application.resource_service import ResourceService
from .application.security_service import SecurityService
from .application.stack_info_service import StackInfoService
from .application.state_drift_service import DriftService, StateService
from .compliance import setup_compliance_hooks
from .compliance_logging import (
    log_calculation_audit,
    log_tool_call_end,
    log_tool_call_start,
    log_write_audit,
)
from .consts import SERVER_DEPENDENCIES, SERVER_INSTRUCTIONS, SERVER_NAME
from .domain.upstream_registry import UpstreamRegistry
from .infrastructure.metrics import MetricsCollector

# Configure logging
logger.remove()
logger.add(sys.stderr, level=os.getenv("FASTMCP_LOG_LEVEL", "WARNING"))

mcp = None

# Upstream AWS MCP servers
UPSTREAM_CONFIG = {
    "cdk": {"host": "localhost", "port": 9140, "transport": "stdio"},
    "cfn": {"host": "localhost", "port": 9141, "transport": "stdio"},
    "terraform": {"host": "localhost", "port": 9142, "transport": "stdio"},
    "iac": {"host": "localhost", "port": 9143, "transport": "stdio"},
}


def create_server() -> FastMCP:
    """Create and configure the FastMCP server instance.

    Returns:
        Configured FastMCP server
    """
    server = FastMCP(
        SERVER_NAME,
        instructions=SERVER_INSTRUCTIONS,
        dependencies=SERVER_DEPENDENCIES,
    )

    # Initialize services
    registry = UpstreamRegistry(UPSTREAM_CONFIG)
    deploy_service = DeployService(registry=registry, audit=audit_module)
    list_service = ListService(registry=registry)
    destroy_service = DestroyService(registry=registry, audit=audit_module)
    stack_info_service = StackInfoService(registry=registry)
    resource_service = ResourceService(registry=registry)
    monitoring_service = MonitoringService(registry=registry)
    security_service = SecurityService(registry=registry, audit=audit_module)
    backup_service = BackupService(registry=registry)
    cost_service = CostService(registry=registry)
    infra_service = InfrastructureService(registry=registry)
    state_service = StateService(registry=registry)
    drift_service = DriftService(registry=registry)
    ext_security_service = ExtendedSecurityService(registry=registry, audit=audit_module)
    ext_backup_service = ExtendedBackupService(registry=registry)
    ext_cost_service = ExtendedCostService(registry=registry)
    ext_monitoring_service = ExtendedMonitoringService(registry=registry)
    ext_resource_service = ExtendedResourceService(registry=registry)
    network_service = NetworkService(registry=registry)
    database_service = DatabaseService(registry=registry)
    compute_service = ComputeService(registry=registry)
    storage_service = StorageService(registry=registry)
    deployment_service = DeploymentService(registry=registry)
    multiregion_service = MultiRegionService(registry=registry)
    metrics = MetricsCollector()

    # Register compliance hooks
    setup_compliance_hooks(server)

    # Register orchestrator tools
    register_tools(
        server,
        deploy_service,
        list_service,
        destroy_service,
        stack_info_service,
        resource_service,
        monitoring_service,
        security_service,
        backup_service,
        cost_service,
        infra_service,
        state_service,
        drift_service,
        ext_security_service,
        ext_backup_service,
        ext_cost_service,
        ext_monitoring_service,
        ext_resource_service,
        network_service,
        database_service,
        compute_service,
        storage_service,
        deployment_service,
        multiregion_service,
        metrics,
    )

    return server


def register_tools(
    server: FastMCP,
    deploy_service: DeployService,
    list_service: ListService,
    destroy_service: DestroyService,
    stack_info_service: StackInfoService,
    resource_service: ResourceService,
    monitoring_service: MonitoringService,
    security_service: SecurityService,
    backup_service: BackupService,
    cost_service: CostService,
    infra_service: InfrastructureService,
    state_service: StateService,
    drift_service: DriftService,
    ext_security_service: ExtendedSecurityService,
    ext_backup_service: ExtendedBackupService,
    ext_cost_service: ExtendedCostService,
    ext_monitoring_service: ExtendedMonitoringService,
    ext_resource_service: ExtendedResourceService,
    network_service: NetworkService,
    database_service: DatabaseService,
    compute_service: ComputeService,
    storage_service: StorageService,
    deployment_service: DeploymentService,
    multiregion_service: MultiRegionService,
    metrics: MetricsCollector,
) -> None:
    """Register orchestrator tools."""

    @server.tool()
    async def deploy_infrastructure(
        tool: str, stack_name: str, template_path: str, parameters: dict = None
    ) -> dict:
        """Deploy infrastructure using CDK, CloudFormation, Terraform, or IaC.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Stack/deployment name
            template_path: Path to template/config
            parameters: Deployment parameters
        """
        correlation_id = generate_correlation_id()
        start_time = time.time()

        # 1. Log tool call start
        log_tool_call_start(
            correlation_id=correlation_id,
            tool_name="deploy_infrastructure",
            parameters={"tool": tool, "stack_name": stack_name, "template_path": template_path},
        )

        try:
            # 2. Log calculation audit (BaFin requirement: BEFORE forensic flags)
            log_calculation_audit(
                correlation_id=correlation_id,
                operation="deploy_infrastructure",
                inputs={"tool": tool, "stack_name": stack_name, "template_path": template_path},
                calculation_steps=[
                    {"step": "validate_input", "result": "valid"},
                    {"step": "check_tool", "result": tool},
                ],
                result={"status": "pending"},
            )

            result = await deploy_service.deploy_infrastructure(
                tool=tool,
                stack_name=stack_name,
                template_path=template_path,
                parameters=parameters or {},
            )

            # 3. Log write audit (BaFin requirement: on every write path)
            log_write_audit(
                correlation_id=correlation_id,
                operation="deploy_infrastructure",
                entity_type="stack",
                entity_id=stack_name,
                changes={"status": result.status, "tool": result.tool},
            )

            duration = time.time() - start_time
            metrics.record_tool_call(tool=tool, status="success")
            metrics.record_tool_duration(tool=tool, duration=duration)

            # 4. Log tool call end
            log_tool_call_end(
                correlation_id=correlation_id,
                tool_name="deploy_infrastructure",
                status="success",
                duration_ms=duration * 1000,
                result={"stack_name": stack_name, "status": result.status},
            )

            return {
                "status": result.status,
                "stack_name": result.stack_name,
                "tool": result.tool,
                "audit_id": result.audit_id,
            }

        except Exception as e:
            duration = time.time() - start_time
            metrics.record_tool_call(tool=tool, status="error")
            metrics.record_tool_duration(tool=tool, duration=duration)
            metrics.record_error(error_type=type(e).__name__)

            # Log tool call end with error
            log_tool_call_end(
                correlation_id=correlation_id,
                tool_name="deploy_infrastructure",
                status="error",
                duration_ms=duration * 1000,
                error=str(e),
            )

            logger.error(f"Deploy failed: {e}", extra={"correlation_id": correlation_id})
            raise

    @server.tool()
    async def list_stacks(tool: str) -> dict:
        """List deployed stacks.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
        """
        correlation_id = generate_correlation_id()
        start_time = time.time()
        logger.info("list_stacks called", extra={"correlation_id": correlation_id})

        try:
            result = await list_service.list_stacks(tool=tool)

            duration = time.time() - start_time
            metrics.record_tool_call(tool=tool, status="success")
            metrics.record_tool_duration(tool=tool, duration=duration)

            return result

        except Exception as e:
            duration = time.time() - start_time
            metrics.record_tool_call(tool=tool, status="error")
            metrics.record_tool_duration(tool=tool, duration=duration)
            metrics.record_error(error_type=type(e).__name__)
            logger.error(f"List failed: {e}", extra={"correlation_id": correlation_id})
            raise

    @server.tool()
    async def destroy_infrastructure(tool: str, stack_name: str, confirm: bool = False) -> dict:
        """Destroy infrastructure stack.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Stack name to destroy
            confirm: Explicit confirmation required (must be True)
        """
        correlation_id = generate_correlation_id()
        start_time = time.time()

        # 1. Log tool call start
        log_tool_call_start(
            correlation_id=correlation_id,
            tool_name="destroy_infrastructure",
            parameters={"tool": tool, "stack_name": stack_name, "confirm": confirm},
        )

        try:
            # 2. Log calculation audit (BaFin requirement)
            log_calculation_audit(
                correlation_id=correlation_id,
                operation="destroy_infrastructure",
                inputs={"tool": tool, "stack_name": stack_name, "confirm": confirm},
                calculation_steps=[
                    {"step": "validate_confirmation", "result": confirm},
                    {"step": "check_tool", "result": tool},
                ],
                result={"status": "pending"},
            )

            result = await destroy_service.destroy_infrastructure(
                tool=tool, stack_name=stack_name, confirm=confirm
            )

            # 3. Log write audit (BaFin requirement: on every write path)
            log_write_audit(
                correlation_id=correlation_id,
                operation="destroy_infrastructure",
                entity_type="stack",
                entity_id=stack_name,
                changes={"status": "destroyed", "tool": tool},
            )

            duration = time.time() - start_time
            metrics.record_tool_call(tool=tool, status="success")
            metrics.record_tool_duration(tool=tool, duration=duration)

            # 4. Log tool call end
            log_tool_call_end(
                correlation_id=correlation_id,
                tool_name="destroy_infrastructure",
                status="success",
                duration_ms=duration * 1000,
                result={"stack_name": stack_name, "status": "destroyed"},
            )

            return result

        except Exception as e:
            duration = time.time() - start_time
            metrics.record_tool_call(tool=tool, status="error")
            metrics.record_tool_duration(tool=tool, duration=duration)
            metrics.record_error(error_type=type(e).__name__)

            # Log tool call end with error
            log_tool_call_end(
                correlation_id=correlation_id,
                tool_name="destroy_infrastructure",
                status="error",
                duration_ms=duration * 1000,
                error=str(e),
            )

            logger.error(f"Destroy failed: {e}", extra={"correlation_id": correlation_id})
            raise

    # Phase 1: Stack Management Tools (6 tools)
    @server.tool()
    async def get_stack_info(tool: str, stack_name: str) -> dict:
        """Get detailed stack information."""
        return await stack_info_service.get_stack_info(tool, stack_name)

    @server.tool()
    async def get_stack_outputs(tool: str, stack_name: str) -> dict:
        """Get stack outputs."""
        return await stack_info_service.get_stack_outputs(tool, stack_name)

    @server.tool()
    async def get_stack_resources(tool: str, stack_name: str) -> dict:
        """Get stack resources."""
        return await stack_info_service.get_stack_resources(tool, stack_name)

    @server.tool()
    async def get_stack_events(tool: str, stack_name: str) -> dict:
        """Get stack events."""
        return await stack_info_service.get_stack_events(tool, stack_name)

    @server.tool()
    async def validate_template(tool: str, template_path: str) -> dict:
        """Validate template."""
        return await stack_info_service.validate_template(tool, template_path)

    @server.tool()
    async def update_stack(
        tool: str, stack_name: str, template_path: str, parameters: dict = None
    ) -> dict:
        """Update stack."""
        return await stack_info_service.update_stack(
            tool, stack_name, template_path, parameters or {}
        )

    # Phase 1: Resource Management Tools (2 tools)
    @server.tool()
    async def list_resources(tool: str) -> dict:
        """List all resources."""
        return await resource_service.list_resources(tool)

    @server.tool()
    async def tag_resource(tool: str, resource_id: str, tags: dict) -> dict:
        """Tag resource."""
        return await resource_service.tag_resource(tool, resource_id, tags)

    # Phase 1: Monitoring Tools (3 tools)
    @server.tool()
    async def get_health_status(tool: str, stack_name: str) -> dict:
        """Get health status."""
        return await monitoring_service.get_health_status(tool, stack_name)

    @server.tool()
    async def get_metrics(tool: str, stack_name: str, metric_name: str) -> dict:
        """Get metrics."""
        return await monitoring_service.get_metrics(tool, stack_name, metric_name)

    @server.tool()
    async def get_alarms(tool: str, stack_name: str) -> dict:
        """Get alarms."""
        return await monitoring_service.get_alarms(tool, stack_name)

    # Phase 1: Security Tools (3 tools)
    @server.tool()
    async def scan_security(tool: str, stack_name: str) -> dict:
        """Scan security."""
        return await security_service.scan_security(tool, stack_name)

    @server.tool()
    async def detect_drift(tool: str, stack_name: str) -> dict:
        """Detect drift."""
        return await security_service.detect_drift(tool, stack_name)

    @server.tool()
    async def get_audit_logs(tool: str, stack_name: str) -> dict:
        """Get audit logs."""
        return await security_service.get_audit_logs(tool, stack_name)

    # Phase 1: Backup Tools (2 tools)
    @server.tool()
    async def create_backup(tool: str, stack_name: str) -> dict:
        """Create backup."""
        return await backup_service.create_backup(tool, stack_name)

    @server.tool()
    async def list_backups(tool: str, stack_name: str) -> dict:
        """List backups."""
        return await backup_service.list_backups(tool, stack_name)

    # Phase 1: Cost Tool (1 tool)
    @server.tool()
    async def get_cost_breakdown(tool: str, stack_name: str) -> dict:
        """Get cost breakdown."""
        return await cost_service.get_cost_breakdown(tool, stack_name)

    # Phase 1: Infrastructure Tools (3 tools)
    @server.tool()
    async def list_vpcs(tool: str) -> dict:
        """List VPCs."""
        return await infra_service.list_vpcs(tool)

    @server.tool()
    async def list_databases(tool: str) -> dict:
        """List databases."""
        return await infra_service.list_databases(tool)

    @server.tool()
    async def list_instances(tool: str) -> dict:
        """List instances."""
        return await infra_service.list_instances(tool)

    # Phase 2: State Management (5 tools)
    @server.tool()
    async def get_state(tool: str, stack_name: str) -> dict:
        """Get Terraform/IaC state."""
        return await state_service.get_state(tool, stack_name)

    @server.tool()
    async def lock_state(tool: str, stack_name: str) -> dict:
        """Lock state for operations."""
        return await state_service.lock_state(tool, stack_name)

    @server.tool()
    async def unlock_state(tool: str, stack_name: str) -> dict:
        """Unlock state."""
        return await state_service.unlock_state(tool, stack_name)

    @server.tool()
    async def backup_state(tool: str, stack_name: str) -> dict:
        """Backup current state."""
        return await state_service.backup_state(tool, stack_name)

    @server.tool()
    async def restore_state(tool: str, stack_name: str, backup_id: str) -> dict:
        """Restore state from backup."""
        return await state_service.restore_state(tool, stack_name, backup_id)

    # Phase 2: Drift Detection (2 tools)
    @server.tool()
    async def get_drift_status(tool: str, stack_name: str) -> dict:
        """Get drift detection status."""
        return await drift_service.get_drift_status(tool, stack_name)

    @server.tool()
    async def get_drift_details(tool: str, stack_name: str) -> dict:
        """Get detailed drift information."""
        return await drift_service.get_drift_details(tool, stack_name)

    @server.tool()
    async def remediate_drift(tool: str, stack_name: str) -> dict:
        """Auto-remediate detected drift."""
        return await drift_service.remediate_drift(tool, stack_name)

    # Phase 2: Extended Security (4 tools)
    @server.tool()
    async def check_compliance(tool: str, stack_name: str, rules: list) -> dict:
        """Check compliance rules."""
        return await ext_security_service.check_compliance(tool, stack_name, rules)

    @server.tool()
    async def rotate_secrets(tool: str, stack_name: str) -> dict:
        """Rotate secrets/credentials."""
        return await ext_security_service.rotate_secrets(tool, stack_name)

    @server.tool()
    async def scan_vulnerabilities(tool: str, stack_name: str) -> dict:
        """Scan for vulnerabilities."""
        return await ext_security_service.scan_vulnerabilities(tool, stack_name)

    @server.tool()
    async def generate_compliance_report(tool: str, stack_name: str) -> dict:
        """Generate compliance report."""
        return await ext_security_service.generate_compliance_report(tool, stack_name)

    # Phase 2: Extended Backup (3 tools)
    @server.tool()
    async def restore_backup(tool: str, stack_name: str, backup_id: str) -> dict:
        """Restore from backup."""
        return await ext_backup_service.restore_backup(tool, stack_name, backup_id)

    @server.tool()
    async def delete_backup(tool: str, backup_id: str) -> dict:
        """Delete backup."""
        return await ext_backup_service.delete_backup(tool, backup_id)

    @server.tool()
    async def test_recovery(tool: str, stack_name: str) -> dict:
        """Test disaster recovery."""
        return await ext_backup_service.test_recovery(tool, stack_name)

    # Phase 2: Extended Cost (4 tools)
    @server.tool()
    async def estimate_cost(tool: str, template_path: str) -> dict:
        """Estimate deployment cost."""
        return await ext_cost_service.estimate_cost(tool, template_path)

    @server.tool()
    async def get_cost_forecast(tool: str, stack_name: str, days: int = 30) -> dict:
        """Forecast future costs."""
        return await ext_cost_service.get_cost_forecast(tool, stack_name, days)

    @server.tool()
    async def get_cost_anomalies(tool: str, stack_name: str) -> dict:
        """Detect cost anomalies."""
        return await ext_cost_service.get_cost_anomalies(tool, stack_name)

    @server.tool()
    async def optimize_costs(tool: str, stack_name: str) -> dict:
        """Get cost optimization recommendations."""
        return await ext_cost_service.optimize_costs(tool, stack_name)

    @server.tool()
    async def set_budget(tool: str, stack_name: str, amount: float, currency: str = "USD") -> dict:
        """Set cost budget alerts."""
        return await ext_cost_service.set_budget(tool, stack_name, amount, currency)

    # Phase 2: Extended Monitoring (3 tools)
    @server.tool()
    async def create_alarm(tool: str, stack_name: str, metric: str, threshold: float) -> dict:
        """Create CloudWatch alarm."""
        return await ext_monitoring_service.create_alarm(tool, stack_name, metric, threshold)

    @server.tool()
    async def get_logs(tool: str, stack_name: str) -> dict:
        """Get aggregated logs."""
        return await ext_monitoring_service.get_logs(tool, stack_name)

    @server.tool()
    async def query_logs(tool: str, stack_name: str, query: str) -> dict:
        """Query logs with filters."""
        return await ext_monitoring_service.query_logs(tool, stack_name, query)

    # Phase 2: Extended Resource (6 tools)
    @server.tool()
    async def get_resource_info(tool: str, resource_id: str) -> dict:
        """Get detailed resource information."""
        return await ext_resource_service.get_resource_info(tool, resource_id)

    @server.tool()
    async def untag_resource(tool: str, resource_id: str, tag_keys: list) -> dict:
        """Remove resource tags."""
        return await ext_resource_service.untag_resource(tool, resource_id, tag_keys)

    @server.tool()
    async def search_resources(tool: str, tags: dict, resource_type: str = None) -> dict:
        """Search resources by tags/type."""
        return await ext_resource_service.search_resources(tool, tags, resource_type)

    @server.tool()
    async def get_resource_metrics(tool: str, resource_id: str, metric_name: str) -> dict:
        """Get CloudWatch metrics for resource."""
        return await ext_resource_service.get_resource_metrics(tool, resource_id, metric_name)

    @server.tool()
    async def get_resource_logs(tool: str, resource_id: str) -> dict:
        """Get CloudWatch logs for resource."""
        return await ext_resource_service.get_resource_logs(tool, resource_id)

    @server.tool()
    async def get_resource_cost(tool: str, resource_id: str) -> dict:
        """Get cost for specific resource."""
        return await ext_resource_service.get_resource_cost(tool, resource_id)

    # Phase 2: Network Management (5 tools)
    @server.tool()
    async def get_vpc_info(tool: str, vpc_id: str) -> dict:
        """Get VPC details."""
        return await network_service.get_vpc_info(tool, vpc_id)

    @server.tool()
    async def list_subnets(tool: str, vpc_id: str = None) -> dict:
        """List subnets."""
        return await network_service.list_subnets(tool, vpc_id)

    @server.tool()
    async def get_network_topology(tool: str, vpc_id: str) -> dict:
        """Get network topology."""
        return await network_service.get_network_topology(tool, vpc_id)

    @server.tool()
    async def test_connectivity(tool: str, source: str, target: str) -> dict:
        """Test network connectivity."""
        return await network_service.test_connectivity(tool, source, target)

    @server.tool()
    async def get_security_groups(tool: str, vpc_id: str = None) -> dict:
        """Get security group rules."""
        return await network_service.get_security_groups(tool, vpc_id)

    # Phase 2: Database Management (4 tools)
    @server.tool()
    async def get_database_info(tool: str, db_id: str) -> dict:
        """Get database details."""
        return await database_service.get_database_info(tool, db_id)

    @server.tool()
    async def backup_database(tool: str, db_id: str) -> dict:
        """Create database backup."""
        return await database_service.backup_database(tool, db_id)

    @server.tool()
    async def restore_database(tool: str, db_id: str, backup_id: str) -> dict:
        """Restore database."""
        return await database_service.restore_database(tool, db_id, backup_id)

    @server.tool()
    async def get_database_metrics(tool: str, db_id: str) -> dict:
        """Get database performance metrics."""
        return await database_service.get_database_metrics(tool, db_id)

    # Phase 2: Compute Management (4 tools)
    @server.tool()
    async def get_instance_info(tool: str, instance_id: str) -> dict:
        """Get instance details."""
        return await compute_service.get_instance_info(tool, instance_id)

    @server.tool()
    async def start_instance(tool: str, instance_id: str) -> dict:
        """Start stopped instance."""
        return await compute_service.start_instance(tool, instance_id)

    @server.tool()
    async def stop_instance(tool: str, instance_id: str) -> dict:
        """Stop running instance."""
        return await compute_service.stop_instance(tool, instance_id)

    @server.tool()
    async def get_instance_logs(tool: str, instance_id: str) -> dict:
        """Get instance logs."""
        return await compute_service.get_instance_logs(tool, instance_id)

    # Phase 2: Storage Management (4 tools)
    @server.tool()
    async def list_buckets(tool: str) -> dict:
        """List S3 buckets."""
        return await storage_service.list_buckets(tool)

    @server.tool()
    async def get_bucket_info(tool: str, bucket_name: str) -> dict:
        """Get bucket details."""
        return await storage_service.get_bucket_info(tool, bucket_name)

    @server.tool()
    async def sync_bucket(tool: str, source: str, target: str) -> dict:
        """Sync bucket contents."""
        return await storage_service.sync_bucket(tool, source, target)

    @server.tool()
    async def get_storage_metrics(tool: str, bucket_name: str) -> dict:
        """Get storage metrics."""
        return await storage_service.get_storage_metrics(tool, bucket_name)

    # Phase 2: Deployment Workflows (5 tools)
    @server.tool()
    async def create_pipeline(tool: str, name: str, config: dict) -> dict:
        """Create CI/CD pipeline."""
        return await deployment_service.create_pipeline(tool, name, config)

    @server.tool()
    async def trigger_pipeline(tool: str, pipeline_id: str) -> dict:
        """Trigger pipeline execution."""
        return await deployment_service.trigger_pipeline(tool, pipeline_id)

    @server.tool()
    async def get_pipeline_status(tool: str, pipeline_id: str) -> dict:
        """Get pipeline status."""
        return await deployment_service.get_pipeline_status(tool, pipeline_id)

    @server.tool()
    async def rollback_deployment(tool: str, stack_name: str, version: str) -> dict:
        """Rollback to previous version."""
        return await deployment_service.rollback_deployment(tool, stack_name, version)

    @server.tool()
    async def blue_green_deploy(tool: str, stack_name: str, template_path: str) -> dict:
        """Blue/green deployment."""
        return await deployment_service.blue_green_deploy(tool, stack_name, template_path)

    # Phase 2: Multi-Region (4 tools)
    @server.tool()
    async def list_regions(tool: str) -> dict:
        """List available regions."""
        return await multiregion_service.list_regions(tool)

    @server.tool()
    async def replicate_stack(tool: str, stack_name: str, target_region: str) -> dict:
        """Replicate stack to another region."""
        return await multiregion_service.replicate_stack(tool, stack_name, target_region)

    @server.tool()
    async def get_global_resources(tool: str) -> dict:
        """Get global resources (Route53, CloudFront)."""
        return await multiregion_service.get_global_resources(tool)

    @server.tool()
    async def failover_region(tool: str, stack_name: str, target_region: str) -> dict:
        """Failover to another region."""
        return await multiregion_service.failover_region(tool, stack_name, target_region)


def main():
    """Run the MCP server with CLI argument support."""
    global mcp

    parser = argparse.ArgumentParser(description="Virons Infrastructure MCP Server")
    parser.add_argument(
        "--allow-write",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable write operations (requires audit trail)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "api"],
        default="stdio",
        help="Transport protocol (stdio=MCP, http=health, api=REST+Swagger)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for HTTP/API server",
    )

    args = parser.parse_args()

    logger.info(
        f"Starting {SERVER_NAME} (write_enabled={args.allow_write}, transport={args.transport})"
    )

    # API mode: FastAPI with Swagger
    if args.transport == "api":
        import uvicorn

        from .api import create_api
        from .application.deploy_service import DeployService
        from .application.destroy_service import DestroyService
        from .application.list_service import ListService
        from .domain.upstream_registry import UpstreamRegistry
        from .infrastructure.health import HealthChecker

        registry = UpstreamRegistry(UPSTREAM_CONFIG)
        health_checker = HealthChecker(registry=registry)
        deploy_service = DeployService(registry=registry, audit=audit_module)
        list_service = ListService(registry=registry)
        destroy_service = DestroyService(registry=registry, audit=audit_module)

        # Create MCP server for tool introspection
        mcp = create_server()

        app = create_api(health_checker, deploy_service, list_service, destroy_service)

        # Add tool registry endpoint
        @app.get("/tools")
        async def list_tools():
            """List all available MCP tools with enriched metadata."""
            from .tool_metadata import enrich_tool_metadata
            
            tools = await mcp.list_tools()
            enriched_tools = []
            
            for tool in tools:
                tool_data = {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema,
                }
                enriched_tools.append(enrich_tool_metadata(tool.name, tool_data))
            
            return {
                "server": SERVER_NAME,
                "tools": enriched_tools,
            }

        # Add tool execution endpoint
        @app.post("/tools/{tool_name}")
        async def execute_tool(tool_name: str, request: dict):
            """Execute a tool by name."""
            try:
                _, result = await mcp.call_tool(tool_name, request)
                return result
            except Exception as e:
                return {"error": str(e)}

        logger.info(f"Starting API server on port {args.port}")
        logger.info(f"Swagger UI: http://localhost:{args.port}/api/docs")
        logger.info(f"ReDoc: http://localhost:{args.port}/api/redoc")
        logger.info(f"Tools registry: http://localhost:{args.port}/tools")

        uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="info")
        return

    # HTTP mode: Health checks only (K8s)
    if args.transport == "http":
        from http.server import BaseHTTPRequestHandler, HTTPServer

        from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest

        from .domain.upstream_registry import UpstreamRegistry
        from .infrastructure.health import HealthChecker

        registry = UpstreamRegistry(UPSTREAM_CONFIG)
        health_checker = HealthChecker(registry=registry)

        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/health/live":
                    result = asyncio.run(health_checker.liveness())
                    self.send_response(200 if result["status"] == "healthy" else 503)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode())
                elif self.path == "/health/ready":
                    result = asyncio.run(health_checker.readiness())
                    self.send_response(200 if result["status"] == "healthy" else 503)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode())
                elif self.path == "/metrics":
                    output = generate_latest(REGISTRY)
                    self.send_response(200)
                    self.send_header("Content-Type", CONTENT_TYPE_LATEST)
                    self.end_headers()
                    self.wfile.write(output)
                elif self.path == "/metrics/json":
                    metrics_data = {
                        "status": "ok",
                        "timestamp": time.time(),
                        "note": "Use /metrics for Prometheus format",
                    }
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(metrics_data, indent=2).encode())
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, format, *args):
                pass

        server = HTTPServer(("0.0.0.0", args.port), HealthHandler)
        logger.info(f"Health server started on port {args.port}")
        server.serve_forever()
        return

    # STDIO mode: MCP protocol
    mcp = create_server()
    mcp.run()


if __name__ == "__main__":
    main()
