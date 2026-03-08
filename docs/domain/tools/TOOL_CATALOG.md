# Virons MCP Gateway - Tool Documentation

Total tools: 90

================================================================================

deploy_infrastructure - Deploy infrastructure using CDK, CloudFormation, Terraform, or IaC.

Args:
    tool: string
    stack_name: string
    template_path: string
    parameters: dict (optional)

Examples:
    - Deploy a Terraform stack
    - Deploy a CDK stack


list_stacks - List deployed stacks.

Args:
    tool: string

Examples:
    - List all CloudFormation stacks
    - List all Terraform stacks


destroy_infrastructure - Destroy infrastructure stack.

Args:
    tool: string
    stack_name: string
    confirm: boolean (optional), default: False

Examples:
    - Destroy a test environment


get_stack_info - Get detailed stack information including status, resources, and outputs.

Args:
    tool: string
    stack_name: string

Examples:
    - Get detailed information about a stack


get_stack_outputs - Get stack outputs (exported values from the stack).

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


get_stack_resources - Get all resources managed by the stack.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


get_stack_events - Get stack deployment events and history.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


validate_template - Validate infrastructure template syntax and structure.

Args:
    tool: string
    template_path: string

Examples:
    - Basic usage


update_stack - Update existing stack with new template or parameters.

Args:
    tool: string
    stack_name: string
    template_path: string
    parameters: dict (optional)

Examples:
    - Update stack with new template


list_resources - List all infrastructure resources across stacks.

Args:
    tool: string

Examples:
    - Basic usage


tag_resource - Add tags to infrastructure resource for organization and cost tracking.

Args:
    tool: string
    resource_id: string
    tags: dict

Examples:
    - Basic usage


get_health_status - Get health status of stack resources.

Args:
    tool: string
    stack_name: string

Examples:
    - Check health of production stack


get_metrics - Get CloudWatch metrics for stack resources.

Args:
    tool: string
    stack_name: string
    metric_name: string

Examples:
    - Get CPU metrics for a stack


get_alarms - Get CloudWatch alarms for stack resources.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


scan_security - Run security scan on infrastructure stack.

Args:
    tool: string
    stack_name: string

Examples:
    - Run security scan on production stack


detect_drift - Detect configuration drift between actual and desired state.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


get_audit_logs - Get audit logs for compliance tracking.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


create_backup - Create backup of infrastructure stack state.

Args:
    tool: string
    stack_name: string

Examples:
    - Create backup of production stack


list_backups - List available backups for a stack.

Args:
    tool: string
    stack_name: string

Examples:
    - List all backups for a stack


get_cost_breakdown - Get detailed cost breakdown for a stack.

Args:
    tool: string
    stack_name: string

Examples:
    - Get cost breakdown for a stack


list_vpcs - List all VPCs in the account.

Args:
    tool: string

Examples:
    - Basic usage


list_databases - List all databases (RDS, DynamoDB, etc.).

Args:
    tool: string

Examples:
    - Basic usage


list_instances - List EC2 instances.

Args:
    tool: string

Examples:
    - Basic usage


get_state - Get Terraform/IaC state information.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


lock_state - Lock state for operations to prevent concurrent modifications.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


unlock_state - Unlock state after operations complete.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


backup_state - Backup current Terraform/IaC state.

Args:
    tool: string
    stack_name: string

Examples:
    - Backup Terraform state


restore_state - Restore state from backup.

Args:
    tool: string
    stack_name: string
    backup_id: string

Examples:
    - Restore Terraform state from backup


get_drift_status - Get drift detection status.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


get_drift_details - Get detailed drift information showing what changed.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


remediate_drift - Auto-remediate detected drift by applying desired state.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


check_compliance - Check compliance against regulatory rules (BaFin, DORA, GDPR).

Args:
    tool: string
    stack_name: string
    rules: list[any]

Examples:
    - Check BaFin compliance


rotate_secrets - Rotate secrets and credentials for a stack.

Args:
    tool: string
    stack_name: string

Examples:
    - Rotate secrets for a stack


scan_vulnerabilities - Scan for security vulnerabilities in infrastructure.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


generate_compliance_report - Generate compliance report for auditing.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


restore_backup - Restore stack from a backup.

Args:
    tool: string
    stack_name: string
    backup_id: string

Examples:
    - Restore from a specific backup


delete_backup - Delete a backup.

Args:
    tool: string
    backup_id: string

Examples:
    - Basic usage


test_recovery - Test disaster recovery procedures.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


estimate_cost - Estimate deployment cost before creating resources.

Args:
    tool: string
    template_path: string

Examples:
    - Estimate cost before deployment


get_cost_forecast - Forecast future costs based on current usage.

Args:
    tool: string
    stack_name: string
    days: integer (optional), default: 30

Examples:
    - Forecast costs for next 30 days


get_cost_anomalies - Detect cost anomalies and unusual spending patterns.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


optimize_costs - Get cost optimization recommendations.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


set_budget - Set cost budget alerts for a stack.

Args:
    tool: string
    stack_name: string
    amount: number
    currency: string (optional), default: USD

Examples:
    - Basic usage


create_alarm - Create CloudWatch alarm for monitoring.

Args:
    tool: string
    stack_name: string
    metric: string
    threshold: number

Examples:
    - Basic usage


get_logs - Get aggregated logs from CloudWatch.

Args:
    tool: string
    stack_name: string

Examples:
    - Basic usage


query_logs - Query logs with filters and search patterns.

Args:
    tool: string
    stack_name: string
    query: string

Examples:
    - Basic usage


get_resource_info - Get detailed information about a specific resource.

Args:
    tool: string
    resource_id: string

Examples:
    - Basic usage


untag_resource - Remove tags from infrastructure resource.

Args:
    tool: string
    resource_id: string
    tag_keys: list[any]

Examples:
    - Basic usage


search_resources - Search resources by tags, type, or other criteria.

Args:
    tool: string
    tags: dict
    resource_type: string (optional)

Examples:
    - Basic usage


get_resource_metrics - Get CloudWatch metrics for a specific resource.

Args:
    tool: string
    resource_id: string
    metric_name: string

Examples:
    - Basic usage


get_resource_logs - Get CloudWatch logs for a specific resource.

Args:
    tool: string
    resource_id: string

Examples:
    - Basic usage


get_resource_cost - Get cost breakdown for a specific resource.

Args:
    tool: string
    resource_id: string

Examples:
    - Basic usage


get_vpc_info - Get detailed VPC information including subnets and route tables.

Args:
    tool: string
    vpc_id: string

Examples:
    - Basic usage


list_subnets - List subnets in a VPC.

Args:
    tool: string
    vpc_id: string (optional)

Examples:
    - Basic usage


get_network_topology - Get network topology visualization data.

Args:
    tool: string
    vpc_id: string

Examples:
    - Basic usage


test_connectivity - Test network connectivity between resources.

Args:
    tool: string
    source: string
    target: string

Examples:
    - Basic usage


get_security_groups - Get security group rules for a VPC.

Args:
    tool: string
    vpc_id: string (optional)

Examples:
    - Basic usage


get_database_info - Get detailed database information.

Args:
    tool: string
    db_id: string

Examples:
    - Basic usage


backup_database - Create database backup.

Args:
    tool: string
    db_id: string

Examples:
    - Basic usage


restore_database - Restore database from backup.

Args:
    tool: string
    db_id: string
    backup_id: string

Examples:
    - Basic usage


get_database_metrics - Get database performance metrics.

Args:
    tool: string
    db_id: string

Examples:
    - Basic usage


get_instance_info - Get detailed EC2 instance information.

Args:
    tool: string
    instance_id: string

Examples:
    - Basic usage


start_instance - Start a stopped EC2 instance.

Args:
    tool: string
    instance_id: string

Examples:
    - Basic usage


stop_instance - Stop a running EC2 instance.

Args:
    tool: string
    instance_id: string

Examples:
    - Basic usage


get_instance_logs - Get EC2 instance logs.

Args:
    tool: string
    instance_id: string

Examples:
    - Basic usage


list_buckets - List S3 buckets.

Args:
    tool: string

Examples:
    - Basic usage


get_bucket_info - Get S3 bucket details including size, versioning, and encryption.

Args:
    tool: string
    bucket_name: string

Examples:
    - Basic usage


sync_bucket - Sync S3 bucket contents.

Args:
    tool: string
    source: string
    target: string

Examples:
    - Basic usage


get_storage_metrics - Get storage metrics for S3 buckets.

Args:
    tool: string
    bucket_name: string

Examples:
    - Basic usage


create_pipeline - Create CI/CD pipeline for infrastructure deployment.

Args:
    tool: string
    name: string
    config: dict

Examples:
    - Basic usage


trigger_pipeline - Trigger pipeline execution.

Args:
    tool: string
    pipeline_id: string

Examples:
    - Basic usage


get_pipeline_status - Get pipeline execution status.

Args:
    tool: string
    pipeline_id: string

Examples:
    - Basic usage


rollback_deployment - Rollback to previous deployment version.

Args:
    tool: string
    stack_name: string
    version: string

Examples:
    - Basic usage


blue_green_deploy - Perform blue/green deployment for zero-downtime updates.

Args:
    tool: string
    stack_name: string
    template_path: string

Examples:
    - Basic usage


list_regions - List available AWS regions.

Args:
    tool: string

Examples:
    - Basic usage


replicate_stack - Replicate stack to another region for disaster recovery.

Args:
    tool: string
    stack_name: string
    target_region: string

Examples:
    - Basic usage


get_global_resources - Get global resources (Route53, CloudFront, IAM).

Args:
    tool: string

Examples:
    - Basic usage


failover_region - Failover to another region during disaster.

Args:
    tool: string
    stack_name: string
    target_region: string

Examples:
    - Basic usage


scan_secrets - Scan repository for secrets using Gitleaks.

Examples:
    - Scan repository for exposed secrets
    - Full history scan for leaked credentials


audit_cloudtrail - Query CloudTrail audit logs.

Examples:
    - Query CloudTrail for suspicious API calls


check_iam_policy - Validate IAM policy against security best practices.

Examples:
    - Validate IAM role policy for least privilege


run_compliance_gate - Run compliance gate checks.

Examples:
    - Pre-deploy compliance check


list_clusters - List EKS clusters.

Examples:
    - List ECS clusters in region


deploy_lambda - Deploy Lambda function.

Examples:
    - Deploy Lambda function


deploy_ecs_service - Deploy ECS service.

Examples:
    - Deploy ECS service


start_workflow - Start Step Functions workflow execution.

Examples:
    - Start Step Functions workflow


query_metrics - Query metrics from CloudWatch, Prometheus, or Elasticsearch.

Examples:
    - Query CloudWatch metrics


create_alert - Create monitoring alert rule.

Examples:
    - Create CloudWatch alarm


create_dashboard - Create Grafana dashboard.

Examples:
    - Create CloudWatch dashboard


search_logs - Search logs in Elasticsearch or CloudWatch.

Examples:
    - Search CloudWatch Logs


