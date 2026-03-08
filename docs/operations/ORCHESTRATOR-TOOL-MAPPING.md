# Orchestrator Tool Mapping

## virons-infrastructure-mcp → AWS Labs Servers

### EKS (eks-mcp-server)
- manage_eks_stacks
- manage_k8s_resource
- apply_yaml
- list_k8s_resources
- get_pod_logs
- get_k8s_events
- list_api_versions
- generate_app_manifest

### IAM (iam-mcp-server)
- list_iam_users
- get_iam_user
- create_user
- delete_user
- list_iam_roles
- create_iam_role
- list_iam_groups
- get_iam_group
- create_iam_group
- delete_iam_group

### Cost Explorer (cost-explorer-mcp-server)
- get_cost_and_usage
- get_cost_forecast

### CloudFormation (cfn-mcp-server)
- create_stack
- update_stack
- delete_stack
- describe_stacks
- list_stacks

### CloudWatch (cloudwatch-mcp-server)
- get_metric_statistics
- put_metric_data
- describe_alarms
- get_cloudwatch_logs

### Network (aws-network-mcp-server)
- describe_vpcs
- create_vpc
- delete_vpc
- describe_subnets
- create_subnet

### Terraform (terraform-mcp-server)
- terraform_init
- terraform_plan
- terraform_apply
- terraform_destroy

## virons-ml-mcp → AWS Labs Servers

### Bedrock (amazon-bedrock-agentcore-mcp-server)
- search_agentcore_docs
- fetch_agentcore_doc
- manage_agentcore_runtime

### SageMaker (sagemaker-ai-mcp-server) - MOCK
- create_training_job
- describe_training_job
- create_endpoint
- invoke_endpoint

## virons-forensic-mcp → AWS Labs Servers

### Neptune (amazon-neptune-mcp-server)
- execute_gremlin_query
- execute_sparql_query
- get_graph_summary

## virons-api-mcp → AWS Labs Servers

### OpenAPI (openapi-mcp-server)
- parse_openapi_spec
- generate_client_code
- validate_request

### ElastiCache (elasticache-mcp-server)
- create_cache_cluster
- describe_cache_clusters
- get_cache_value
- set_cache_value
