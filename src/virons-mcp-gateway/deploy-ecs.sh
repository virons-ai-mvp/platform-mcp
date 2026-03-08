#!/bin/bash
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Deploy MCP Gateway to ECS

set -e

AWS_REGION="${AWS_REGION:-eu-central-1}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="virons-mcp-gateway"
IMAGE_TAG="${IMAGE_TAG:-latest}"

echo "🚀 Deploying MCP Gateway to ECS"
echo "Region: $AWS_REGION"
echo "Account: $AWS_ACCOUNT_ID"

# Create ECR repository if not exists
echo "📦 Creating ECR repository..."
aws ecr describe-repositories --repository-names $ECR_REPO --region $AWS_REGION 2>/dev/null || \
  aws ecr create-repository --repository-name $ECR_REPO --region $AWS_REGION

# Login to ECR
echo "🔐 Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build and push image
echo "🏗️  Building Docker image..."
docker build -t $ECR_REPO:$IMAGE_TAG -f Dockerfile ../..

echo "📤 Pushing to ECR..."
docker tag $ECR_REPO:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG

# Create CloudWatch log group
echo "📝 Creating CloudWatch log group..."
aws logs create-log-group --log-group-name /ecs/virons-mcp-gateway --region $AWS_REGION 2>/dev/null || true

# Register task definition
echo "📋 Registering ECS task definition..."
envsubst < ecs-task-definition.json > /tmp/task-def.json
aws ecs register-task-definition --cli-input-json file:///tmp/task-def.json --region $AWS_REGION

# Update service (if exists)
echo "🔄 Updating ECS service..."
aws ecs update-service \
  --cluster virons-mcp-cluster \
  --service virons-mcp-gateway \
  --task-definition virons-mcp-gateway \
  --force-new-deployment \
  --region $AWS_REGION 2>/dev/null || \
  echo "⚠️  Service not found. Create service manually or use Terraform."

echo "✅ Deployment complete!"
echo "Image: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG"
