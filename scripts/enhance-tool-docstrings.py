#!/usr/bin/env python3
"""Enhance tool docstrings with comprehensive Args documentation."""

# Tool documentation templates
TOOL_DOCS = {
    'get_stack_info': '''"""Get detailed stack information including status, resources, and outputs.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack to query
"""''',
    'get_stack_outputs': '''"""Get stack outputs (exported values from the stack).

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
"""''',
    'get_stack_resources': '''"""Get all resources managed by the stack.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
"""''',
    'get_stack_events': '''"""Get stack deployment events and history.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
"""''',
    'validate_template': '''"""Validate infrastructure template syntax and structure.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    template_path: Path to template file or directory
"""''',
    'update_stack': '''"""Update existing stack with new template or parameters.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack to update
    template_path: Path to updated template
    parameters: Optional deployment parameters
"""''',
    'list_resources': '''"""List all infrastructure resources across stacks.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
"""''',
    'tag_resource': '''"""Add tags to infrastructure resource for organization and cost tracking.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    resource_id: Resource identifier
    tags: Dictionary of tag key-value pairs
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
    'get_resource_info': '''"""Get detailed information about a specific resource.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    resource_id: Resource identifier
"""''',
    'get_resource_metrics': '''"""Get CloudWatch metrics for a specific resource.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    resource_id: Resource identifier
    metric_name: Name of the metric (CPUUtilization, NetworkIn, etc.)
    start_time: Start time for metrics (ISO 8601)
    end_time: End time for metrics (ISO 8601)
"""''',
    'get_resource_logs': '''"""Get CloudWatch logs for a specific resource.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    resource_id: Resource identifier
    start_time: Start time for logs (ISO 8601)
    end_time: End time for logs (ISO 8601)
"""''',
    'get_resource_cost': '''"""Get cost breakdown for a specific resource.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    resource_id: Resource identifier
    start_date: Start date for cost analysis
    end_date: End date for cost analysis
"""''',
    'get_health_status': '''"""Get health status of stack resources.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
"""''',
    'get_metrics': '''"""Get CloudWatch metrics for stack resources.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
    metric_name: Metric to retrieve (CPUUtilization, etc.)
"""''',
    'get_alarms': '''"""Get CloudWatch alarms for stack resources.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
"""''',
    'create_alarm': '''"""Create CloudWatch alarm for monitoring.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    alarm_name: Name for the alarm
    metric_name: Metric to monitor
    threshold: Alarm threshold value
    comparison_operator: Comparison operator (GreaterThanThreshold, etc.)
"""''',
    'get_logs': '''"""Get aggregated logs from CloudWatch.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    log_group: CloudWatch log group name
    start_time: Start time (ISO 8601)
    end_time: End time (ISO 8601)
"""''',
    'query_logs': '''"""Query logs with filters and search patterns.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    log_group: CloudWatch log group name
    query: CloudWatch Insights query
    start_time: Start time (ISO 8601)
    end_time: End time (ISO 8601)
"""''',
    'scan_security': '''"""Run security scan on infrastructure stack.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack to scan
"""''',
    'detect_drift': '''"""Detect configuration drift between actual and desired state.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
"""''',
    'get_audit_logs': '''"""Get audit logs for compliance tracking.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
    start_time: Start time (ISO 8601)
    end_time: End time (ISO 8601)
"""''',
    'create_backup': '''"""Create backup of infrastructure stack state.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack to backup
"""''',
    'list_backups': '''"""List available backups for a stack.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
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
    'get_cost_breakdown': '''"""Get detailed cost breakdown for a stack.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
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
    days: Number of days to forecast
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
    alert_threshold: Percentage threshold for alerts (e.g., 80)
"""''',
    'list_vpcs': '''"""List all VPCs in the account.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
"""''',
    'get_vpc_info': '''"""Get detailed VPC information including subnets and route tables.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    vpc_id: VPC identifier
"""''',
    'list_subnets': '''"""List subnets in a VPC.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    vpc_id: VPC identifier
"""''',
    'get_network_topology': '''"""Get network topology visualization data.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    vpc_id: VPC identifier
"""''',
    'test_connectivity': '''"""Test network connectivity between resources.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    source_id: Source resource identifier
    target_id: Target resource identifier
"""''',
    'get_security_groups': '''"""Get security group rules for a VPC.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    vpc_id: VPC identifier
"""''',
    'list_databases': '''"""List all databases (RDS, DynamoDB, etc.).

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
"""''',
    'get_database_info': '''"""Get detailed database information.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    db_id: Database identifier
"""''',
    'backup_database': '''"""Create database backup.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    db_id: Database identifier
"""''',
    'restore_database': '''"""Restore database from backup.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    db_id: Database identifier
    backup_id: Backup identifier
"""''',
    'get_database_metrics': '''"""Get database performance metrics.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    db_id: Database identifier
    metric_name: Metric name (CPUUtilization, DatabaseConnections, etc.)
"""''',
    'list_instances': '''"""List EC2 instances.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
"""''',
    'get_instance_info': '''"""Get detailed EC2 instance information.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    instance_id: Instance identifier
"""''',
    'start_instance': '''"""Start a stopped EC2 instance.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    instance_id: Instance identifier
"""''',
    'stop_instance': '''"""Stop a running EC2 instance.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    instance_id: Instance identifier
"""''',
    'get_instance_logs': '''"""Get EC2 instance logs.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    instance_id: Instance identifier
"""''',
    'list_buckets': '''"""List S3 buckets.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
"""''',
    'get_bucket_info': '''"""Get S3 bucket details including size, versioning, and encryption.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    bucket_name: Bucket name
"""''',
    'sync_bucket': '''"""Sync S3 bucket contents.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    source_bucket: Source bucket name
    target_bucket: Target bucket name
"""''',
    'get_storage_metrics': '''"""Get storage metrics for S3 buckets.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    bucket_name: Bucket name
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
    auto_approve: Auto-approve remediation without confirmation
"""''',
    'check_compliance': '''"""Check compliance against regulatory rules (BaFin, DORA, GDPR).

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
    rules: List of compliance rules to check
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
    report_type: Type of report (bafin|dora|gdpr|all)
"""''',
    'create_pipeline': '''"""Create CI/CD pipeline for infrastructure deployment.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    pipeline_name: Name for the pipeline
    source_repo: Source repository URL
    stages: Pipeline stages configuration
"""''',
    'trigger_pipeline': '''"""Trigger pipeline execution.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    pipeline_name: Name of the pipeline
"""''',
    'get_pipeline_status': '''"""Get pipeline execution status.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    pipeline_name: Name of the pipeline
"""''',
    'rollback_deployment': '''"""Rollback to previous deployment version.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
    version: Version to rollback to (optional, defaults to previous)
"""''',
    'blue_green_deploy': '''"""Perform blue/green deployment for zero-downtime updates.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
    template_path: Path to new template
"""''',
    'list_regions': '''"""List available AWS regions.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
"""''',
    'replicate_stack': '''"""Replicate stack to another region for disaster recovery.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
    target_region: Target AWS region
"""''',
    'get_global_resources': '''"""Get global resources (Route53, CloudFront, IAM).

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
"""''',
    'failover_region': '''"""Failover to another region during disaster.

Args:
    tool: IaC tool (cdk|cfn|terraform|iac)
    stack_name: Name of the stack
    target_region: Target region for failover
"""''',
    'list_clusters': '''"""List EKS/ECS clusters.

Returns:
    List of cluster information including name, status, and endpoint
"""''',
    'deploy_lambda': '''"""Deploy Lambda function.

Args:
    function_name: Function name
    runtime: Runtime (python3.10, nodejs20.x, etc.)
    handler: Handler path (e.g., index.handler)
    code_path: Path to deployment package (zip file or directory)
"""''',
    'deploy_ecs_service': '''"""Deploy ECS service.

Args:
    service_name: Service name
    cluster: ECS cluster name
    task_definition: Task definition ARN or family:revision
    desired_count: Desired number of tasks
"""''',
    'start_workflow': '''"""Start Step Functions workflow execution.

Args:
    state_machine_arn: State machine ARN
    input_data: Workflow input data (JSON)
"""''',
}

print('Tool documentation templates created.')
print(f'Total tools documented: {len(TOOL_DOCS)}')
print('\nTo apply these, update the docstrings in server.py files.')
