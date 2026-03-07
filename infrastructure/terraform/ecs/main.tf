# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Terraform configuration for ECS deployment."""

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# VPC and Networking
resource "aws_vpc" "virons_mcp" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "virons-mcp-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.virons_mcp.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name        = "virons-mcp-private-${count.index + 1}"
    Environment = var.environment
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

# ECS Cluster
resource "aws_ecs_cluster" "virons_mcp" {
  name = "virons-mcp-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Environment = var.environment
  }
}

# Security Group
resource "aws_security_group" "virons_mcp" {
  name        = "virons-mcp-sg"
  description = "Security group for Virons MCP services"
  vpc_id      = aws_vpc.virons_mcp.id

  ingress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  ingress {
    from_port   = 9100
    to_port     = 9400
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "virons-mcp-sg"
    Environment = var.environment
  }
}

# IAM Roles
resource "aws_iam_role" "ecs_task_execution" {
  name = "virons-mcp-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ECS Service - Infrastructure MCP
resource "aws_ecs_service" "infrastructure_mcp" {
  name            = "virons-infrastructure-mcp"
  cluster         = aws_ecs_cluster.virons_mcp.id
  task_definition = "virons-infrastructure-mcp:latest"
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.virons_mcp.id]
    assign_public_ip = false
  }

  tags = {
    Environment = var.environment
  }
}

# ECS Service - MCP Gateway
resource "aws_ecs_service" "mcp_gateway" {
  name            = "virons-mcp-gateway"
  cluster         = aws_ecs_cluster.virons_mcp.id
  task_definition = "virons-mcp-gateway:latest"
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.virons_mcp.id]
    assign_public_ip = false
  }

  tags = {
    Environment = var.environment
  }
}

# Outputs
output "cluster_name" {
  value = aws_ecs_cluster.virons_mcp.name
}

output "vpc_id" {
  value = aws_vpc.virons_mcp.id
}

output "security_group_id" {
  value = aws_security_group.virons_mcp.id
}
