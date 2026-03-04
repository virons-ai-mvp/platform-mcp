import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  mainSidebar: [
    {
      type: "category",
      label: "Get Started",
      collapsed: false,
      items: ["intro", "installation", "vibe_coding"],
    },
    {
      type: "category",
      label: "Available MCP Servers for AWS",
      collapsed: false,
      items: [
        {
          type: "category",
          label: "Getting Started",
          items: [
            {
              type: 'link',
              label: 'AWS MCP',
              href: 'https://docs.aws.amazon.com/aws-mcp/latest/userguide/what-is-mcp-server.html',
            },
            "servers/aws-api-infrastructure-mcp-server",
            "servers/aws-knowledge-infrastructure-mcp-server",
          ],
        },
        {
          type: "category",
          label: "Documentation",
          items: ["servers/aws-documentation-infrastructure-mcp-server"],
        },
        {
          type: "category",
          label: "Infrastructure & Deployment",
          items: [
            "servers/aws-iac-infrastructure-mcp-server",
            "servers/ccapi-infrastructure-mcp-server",
            "servers/cdk-infrastructure-mcp-server",
            "servers/cfn-infrastructure-mcp-server",
            "servers/terraform-infrastructure-mcp-server",
            "servers/eks-infrastructure-mcp-server",
            "servers/ecs-infrastructure-mcp-server",
            "servers/finch-infrastructure-mcp-server",
            "servers/lambda-tool-infrastructure-mcp-server",
            "servers/stepfunctions-tool-infrastructure-mcp-server",
            "servers/aws-serverless-infrastructure-mcp-server",
            "servers/aws-support-infrastructure-mcp-server",
            "servers/aws-network-infrastructure-mcp-server",
          ],
        },
        {
          type: "category",
          label: "AI & Machine Learning",
          items: [
            "servers/bedrock-kb-retrieval-infrastructure-mcp-server",
            "servers/amazon-qindex-infrastructure-mcp-server",
            "servers/amazon-qbusiness-anonymous-infrastructure-mcp-server",
            "servers/document-loader-infrastructure-mcp-server",
            "servers/nova-canvas-infrastructure-mcp-server",
            "servers/aws-bedrock-custom-model-import-infrastructure-mcp-server",
            "servers/amazon-bedrock-agentcore-infrastructure-mcp-server",
            "servers/sagemaker-ai-infrastructure-mcp-server",
          ],
        },
        {
          type: "category",
          label: "Data & Analytics",
          items: [
            "servers/documentdb-infrastructure-mcp-server",
            "servers/dynamodb-infrastructure-mcp-server",
            "servers/elasticache-infrastructure-mcp-server",
            "servers/valkey-infrastructure-mcp-server",
            "servers/memcached-infrastructure-mcp-server",
            "servers/timestream-for-influxdb-infrastructure-mcp-server",
            "servers/amazon-keyspaces-infrastructure-mcp-server",
            "servers/amazon-neptune-infrastructure-mcp-server",
            "servers/aurora-dsql-infrastructure-mcp-server",
            "servers/mysql-infrastructure-mcp-server",
            "servers/postgres-infrastructure-mcp-server",
            "servers/aws-dataprocessing-infrastructure-mcp-server",
            "servers/redshift-infrastructure-mcp-server",
            "servers/s3-tables-infrastructure-mcp-server",
            "servers/aws-appsync-infrastructure-mcp-server",
            "servers/aws-iot-sitewise-infrastructure-mcp-server",
            "servers/sagemaker-unified-studio-spark-troubleshooting-infrastructure-mcp-server",
            "servers/sagemaker-unified-studio-spark-upgrade-infrastructure-mcp-server"
          ],
        },
        {
          type: "category",
          label: "Developer Tools & Support",
          items: [
            "servers/core-infrastructure-mcp-server",
            "servers/git-repo-research-infrastructure-mcp-server",
            "servers/openapi-infrastructure-mcp-server",
            "servers/aws-diagram-infrastructure-mcp-server",
            "servers/prometheus-infrastructure-mcp-server",
            "servers/code-doc-gen-infrastructure-mcp-server",
            "servers/frontend-infrastructure-mcp-server",
            "servers/iam-infrastructure-mcp-server",
            "servers/kendra-index-infrastructure-mcp-server",
            "servers/syntheticdata-infrastructure-mcp-server",
            "servers/aws-bedrock-data-automation-infrastructure-mcp-server",
            "servers/aws-location-infrastructure-mcp-server",
            "servers/aws-msk-infrastructure-mcp-server",
          ],
        },
        {
          type: "category",
          label: "Integration & Messaging",
          items: [
            "servers/amazon-mq-infrastructure-mcp-server",
            "servers/amazon-sns-sqs-infrastructure-mcp-server",
          ],
        },
        {
          type: "category",
          label: "Cost & Operations",
          items: [
            "servers/aws-pricing-infrastructure-mcp-server",
            "servers/cost-explorer-infrastructure-mcp-server",
            "servers/cloudwatch-infrastructure-mcp-server",
            "servers/cloudwatch-applicationsignals-infrastructure-mcp-server",
            "servers/well-architected-security-infrastructure-mcp-server",
            "servers/cloudtrail-infrastructure-mcp-server",
            "servers/billing-cost-management-infrastructure-mcp-server",
          ],
        },
        {
          type: "category",
          label: "Healthcare & Lifesciences",
          items: [
            "servers/aws-healthomics-infrastructure-mcp-server",
            "servers/healthimaging-infrastructure-mcp-server",
            "servers/healthlake-infrastructure-mcp-server",
          ],
        },
      ],
    },
    {
      type: "category",
      label: "Samples",
      collapsed: false,
      items: [
        "samples/mcp-integration-with-kb",
        "samples/mcp-integration-with-nova-canvas",
        "samples/stepfunctions-tool-infrastructure-mcp-server",
      ],
    },
  ],
};

export default sidebars;
