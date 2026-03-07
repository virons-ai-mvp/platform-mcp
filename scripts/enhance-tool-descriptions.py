#!/usr/bin/env python3
"""Enhance tool descriptions by adding Args sections based on input schemas."""

import json
import requests
import sys


def format_param_description(param_name, param_info, required_params):
    """Generate parameter description from schema."""
    is_required = param_name in required_params

    # Common parameter descriptions
    descriptions = {
        'tool': 'IaC tool (cdk|cfn|terraform|iac)',
        'stack_name': 'Name of the stack',
        'template_path': 'Path to template file or directory',
        'parameters': 'Deployment parameters',
        'resource_id': 'Resource identifier',
        'tags': 'Dictionary of tag key-value pairs',
        'tag_keys': 'List of tag keys to remove',
        'filters': 'Search filters (tags, resource_type, etc.)',
        'metric_name': 'Metric name (CPUUtilization, NetworkIn, etc.)',
        'start_time': 'Start timestamp (ISO 8601)',
        'end_time': 'End timestamp (ISO 8601)',
        'backup_id': 'Backup identifier',
        'vpc_id': 'VPC identifier',
        'db_id': 'Database identifier',
        'instance_id': 'Instance identifier',
        'bucket_name': 'Bucket name',
        'source_bucket': 'Source bucket name',
        'target_bucket': 'Target bucket name',
        'log_group': 'CloudWatch log group name',
        'query': 'CloudWatch Insights query or search query',
        'alarm_name': 'Name for the alarm',
        'threshold': 'Alert threshold value',
        'comparison_operator': 'Comparison operator (GreaterThanThreshold, LessThanThreshold, etc.)',
        'rules': 'List of compliance rules to check',
        'days': 'Number of days',
        'budget_amount': 'Monthly budget amount',
        'alert_threshold': 'Percentage threshold for alerts (e.g., 80)',
        'source_id': 'Source resource identifier',
        'target_id': 'Target resource identifier',
        'auto_approve': 'Auto-approve without confirmation',
        'confirm': 'Explicit confirmation required (must be True)',
        'version': 'Version to rollback to',
        'target_region': 'Target AWS region',
        'pipeline_name': 'Pipeline name',
        'source_repo': 'Source repository URL',
        'stages': 'Pipeline stages configuration',
        'function_name': 'Function name',
        'runtime': 'Runtime (python3.10, nodejs20.x, etc.)',
        'handler': 'Handler path (e.g., index.handler)',
        'code_path': 'Path to deployment package',
        'service_name': 'Service name',
        'cluster': 'ECS cluster name or EKS cluster name',
        'task_definition': 'Task definition ARN or family:revision',
        'desired_count': 'Desired number of tasks',
        'state_machine_arn': 'State machine ARN',
        'input_data': 'Workflow input data (JSON)',
        'source': 'Data source (cloudwatch|prometheus|elasticsearch)',
        'name': 'Name',
        'metric': 'Metric to monitor',
        'comparison': 'Comparison operator (gt|lt|eq)',
        'panels': 'List of panel configurations',
        'report_type': 'Type of report (bafin|dora|gdpr|all)',
        'start_date': 'Start date for analysis',
        'end_date': 'End date for analysis',
        'repository_path': 'Path to git repository',
        'scan_history': 'Scan full git history',
        'event_name': 'Filter by event name',
        'policy_document': 'IAM policy JSON',
        'resource_type': 'Resource type (user|role|group)',
        'artifact_path': 'Path to artifact',
        'gate_type': 'Gate type (pre-commit|pre-deploy|post-deploy)',
    }

    desc = descriptions.get(
        param_name, param_info.get('title', param_name).replace('_', ' ').capitalize()
    )

    if not is_required:
        default = param_info.get('default')
        if default is not None:
            desc += f' (optional, default: {default})'
        else:
            desc += ' (optional)'

    return f'    {param_name}: {desc}'


def enhance_description(tool):
    """Enhance tool description with Args section."""
    current_desc = tool['description'].strip()

    # If already has Args section, return as-is
    if 'Args:' in current_desc:
        return current_desc

    # Get first line of description
    first_line = current_desc.split('\n')[0]

    # Build Args section from schema
    schema = tool.get('input_schema', {})
    props = schema.get('properties', {})
    required = schema.get('required', [])

    if not props:
        # No parameters, return original description
        return first_line

    # Build enhanced description
    enhanced = first_line + '\n\nArgs:\n'

    # Sort parameters: required first, then optional
    sorted_params = sorted(props.items(), key=lambda x: (x[0] not in required, x[0]))

    for param_name, param_info in sorted_params:
        enhanced += format_param_description(param_name, param_info, required) + '\n'

    return enhanced


def main():
    """Fetch tools from gateway and enhance descriptions."""
    gateway_url = 'http://localhost:9000/tools'

    try:
        response = requests.get(gateway_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        tools = data.get('tools', [])

        print('# Enhanced Tool Descriptions\n')
        print(f'Total tools: {len(tools)}\n')
        print('=' * 80 + '\n')

        for tool in tools:
            enhanced = enhance_description(tool)
            print(f'{tool["name"]} - {enhanced}\n')

        # Statistics
        with_args = sum(1 for t in tools if 'Args:' in enhance_description(t))
        print(f'\n{"=" * 80}')
        print('Statistics:')
        print(f'  Total tools: {len(tools)}')
        print(f'  With Args section: {with_args}')
        print(f'  Missing Args: {len(tools) - with_args}')

    except requests.RequestException as e:
        print(f'Error connecting to gateway: {e}', file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f'Error parsing JSON response: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
