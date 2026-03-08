#!/usr/bin/env python3
"""Update tool docstrings in server.py files with enhanced Args documentation."""

import re
import sys
from pathlib import Path


# Enhanced docstrings for infrastructure server tools
ENHANCED_DOCSTRINGS = {
    'list_backups': '''"""List available backups for a stack.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'get_cost_breakdown': '''"""Get detailed cost breakdown for a stack.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'list_vpcs': '''"""List all VPCs in the account.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
        """''',
    'list_databases': '''"""List all databases (RDS, DynamoDB, etc.).

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
        """''',
    'list_instances': '''"""List EC2 instances.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
        """''',
    'get_state': '''"""Get Terraform/IaC state information.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'lock_state': '''"""Lock state for operations to prevent concurrent modifications.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'unlock_state': '''"""Unlock state after operations complete.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'backup_state': '''"""Backup current Terraform/IaC state.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'restore_state': '''"""Restore state from backup.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
            backup_id: State backup identifier
        """''',
    'get_drift_status': '''"""Get drift detection status.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'get_drift_details': '''"""Get detailed drift information showing what changed.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'remediate_drift': '''"""Auto-remediate detected drift by applying desired state.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
            auto_approve: Auto-approve remediation without confirmation (optional, default: False)
        """''',
    'check_compliance': '''"""Check compliance against regulatory rules (BaFin, DORA, GDPR).

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
            rules: List of compliance rules to check (optional)
        """''',
    'rotate_secrets': '''"""Rotate secrets and credentials for a stack.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'scan_vulnerabilities': '''"""Scan for security vulnerabilities in infrastructure.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'generate_compliance_report': '''"""Generate compliance report for auditing.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
            report_type: Type of report (bafin|dora|gdpr|all) (optional)
        """''',
    'restore_backup': '''"""Restore stack from a backup.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
            backup_id: Backup identifier to restore from
        """''',
    'delete_backup': '''"""Delete a backup.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
            backup_id: Backup identifier to delete
        """''',
    'test_recovery': '''"""Test disaster recovery procedures.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
            backup_id: Backup to test recovery from
        """''',
    'estimate_cost': '''"""Estimate deployment cost before creating resources.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            template_path: Path to template to estimate
        """''',
    'get_cost_forecast': '''"""Forecast future costs based on current usage.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
            days: Number of days to forecast (optional)
        """''',
    'get_cost_anomalies': '''"""Detect cost anomalies and unusual spending patterns.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'optimize_costs': '''"""Get cost optimization recommendations.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
        """''',
    'set_budget': '''"""Set cost budget alerts for a stack.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Name of the stack
            budget_amount: Monthly budget amount
            alert_threshold: Percentage threshold for alerts (e.g., 80) (optional)
        """''',
    'create_alarm': '''"""Create CloudWatch alarm for monitoring.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            alarm_name: Name for the alarm
            metric_name: Metric to monitor
            threshold: Alert threshold value
            comparison_operator: Comparison operator (GreaterThanThreshold, etc.) (optional)
        """''',
    'get_logs': '''"""Get aggregated logs from CloudWatch.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            log_group: CloudWatch log group name
            start_time: Start timestamp (ISO 8601) (optional)
            end_time: End timestamp (ISO 8601) (optional)
        """''',
    'query_logs': '''"""Query logs with filters and search patterns.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            log_group: CloudWatch log group name
            query: CloudWatch Insights query
            start_time: Start timestamp (ISO 8601) (optional)
            end_time: End timestamp (ISO 8601) (optional)
        """''',
    'get_resource_info': '''"""Get detailed information about a specific resource.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            resource_id: Resource identifier
        """''',
    'untag_resource': '''"""Remove tags from infrastructure resource.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            resource_id: Resource identifier
            tag_keys: List of tag keys to remove
        """''',
    'search_resources': '''"""Search resources by tags, type, or other criteria.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            filters: Search filters (tags, resource_type, etc.)
        """''',
    'get_resource_metrics': '''"""Get CloudWatch metrics for a specific resource.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            resource_id: Resource identifier
            metric_name: Metric name (CPUUtilization, NetworkIn, etc.)
            start_time: Start timestamp (ISO 8601) (optional)
            end_time: End timestamp (ISO 8601) (optional)
        """''',
    'get_resource_logs': '''"""Get CloudWatch logs for a specific resource.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            resource_id: Resource identifier
            start_time: Start timestamp (ISO 8601) (optional)
            end_time: End timestamp (ISO 8601) (optional)
        """''',
    'get_resource_cost': '''"""Get cost breakdown for a specific resource.

        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            resource_id: Resource identifier
            start_date: Start date for analysis (optional)
            end_date: End date for analysis (optional)
        """''',
}


def update_server_file(file_path: Path):
    """Update docstrings in a server.py file."""
    if not file_path.exists():
        print(f'❌ File not found: {file_path}')
        return False

    content = file_path.read_text()
    updated_content = content
    updates_made = 0

    for func_name, new_docstring in ENHANCED_DOCSTRINGS.items():
        # Pattern to match function definition and its docstring
        pattern = rf'(async def {func_name}\([^)]+\)[^:]*:)\s*"""[^"]*"""'
        replacement = rf'\1\n        {new_docstring}'

        if re.search(pattern, updated_content):
            updated_content = re.sub(pattern, replacement, updated_content)
            updates_made += 1
            print(f'  ✅ Updated {func_name}')

    if updates_made > 0:
        file_path.write_text(updated_content)
        print(f'\n✅ Updated {updates_made} docstrings in {file_path.name}')
        return True
    else:
        print(f'ℹ️  No updates needed for {file_path.name}')
        return False


def main():
    """Update tool docstrings in server.py files."""
    # Update infrastructure server
    infra_server = Path(
        'src/virons-infrastructure-mcp-server/virons/infrastructure_mcp_server/server.py'
    )

    print('🔧 Updating tool docstrings...\n')
    print(f'📝 Processing {infra_server}')

    if update_server_file(infra_server):
        print('\n✅ Docstring updates complete!')
        print('🔄 Restart services to apply changes: docker-compose restart')
    else:
        print('\n⚠️  No changes made')
        sys.exit(1)


if __name__ == '__main__':
    main()
