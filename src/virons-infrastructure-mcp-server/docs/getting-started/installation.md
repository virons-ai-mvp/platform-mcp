# Installation Guide

**Version**: 1.0
**Last Updated**: 2026-03-07

## Prerequisites

### System Requirements
- **OS**: macOS, Linux, or Windows (WSL2)
- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum
- **Disk**: 2GB free space

### Required Tools
- Python 3.11+
- pip
- Git
- Docker (optional, for local testing)
- kubectl (for Kubernetes deployment)
- Helm 3 (for Kubernetes deployment)

## Installation Methods

### Method 1: pip Install (Recommended)

```bash
# Install from PyPI
pip install virons-infrastructure-mcp-server

# Verify installation
virons-infrastructure-mcp-server --version
```

### Method 2: From Source

```bash
# Clone repository
git clone https://github.com/virons-ai/virons-infrastructure-mcp-server.git
cd virons-infrastructure-mcp-server

# Install in development mode
pip install -e ".[dev]"

# Verify installation
python -m virons.infrastructure_mcp_server.server --version
```

### Method 3: Docker

```bash
# Pull image
docker pull virons/infrastructure-mcp-server:latest

# Run container
docker run -p 8080:8080 virons/infrastructure-mcp-server:latest
```

## Python Environment Setup

### Using venv
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install package
pip install virons-infrastructure-mcp-server
```

### Using conda
```bash
# Create environment
conda create -n virons python=3.11

# Activate
conda activate virons

# Install package
pip install virons-infrastructure-mcp-server
```

### Using poetry
```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate shell
poetry shell
```

## Configuration

### Environment Variables
```bash
# Required
export AWS_REGION=eu-central-1
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key

# Optional
export LOG_LEVEL=INFO
export METRICS_PORT=8080
export DB_HOST=localhost
export DB_PORT=5432
```

### Configuration File
```yaml
# config.yaml
aws:
  region: eu-central-1

logging:
  level: INFO
  format: json

metrics:
  enabled: true
  port: 8080

upstream_servers:
  cdk:
    host: cdk-server
    port: 9140
  terraform:
    host: terraform-server
    port: 9142
  cloudformation:
    host: cfn-server
    port: 9141
```

## Verify Installation

### Check Version
```bash
# Using pip
virons-infrastructure-mcp-server --version

# Using Python module
python -m virons.infrastructure_mcp_server.server --version
```

### Test MCP Server
```bash
# Start server in stdio mode
python -m virons.infrastructure_mcp_server.server --transport stdio

# In another terminal, test with MCP client
echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}' | \
  python -m virons.infrastructure_mcp_server.server --transport stdio
```

### Test API Server
```bash
# Start API server
python -m virons.infrastructure_mcp_server.server --transport api --port 8080

# Test health endpoint
curl http://localhost:8080/health

# Open Swagger UI
open http://localhost:8080/api/docs
```

## Kubernetes Deployment

### Prerequisites
```bash
# Install kubectl
brew install kubectl  # macOS
# or
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install Helm
brew install helm  # macOS
# or
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify
kubectl version --client
helm version
```

### Deploy with Helm
```bash
# Add Helm repository
helm repo add virons https://charts.virons.ai
helm repo update

# Install
helm install virons-infrastructure virons/virons-infrastructure-mcp-server \
  --namespace virons-infrastructure \
  --create-namespace

# Verify deployment
kubectl get pods -n virons-infrastructure
kubectl get svc -n virons-infrastructure
```

### Deploy from Source
```bash
# Clone repository
git clone https://github.com/virons-ai/virons-infrastructure-mcp-server.git
cd virons-infrastructure-mcp-server

# Install with Helm
helm install virons-infrastructure ./helm/virons-infrastructure \
  --namespace virons-infrastructure \
  --create-namespace \
  --values helm/virons-infrastructure/values.yaml

# Check status
helm status virons-infrastructure -n virons-infrastructure
```

## Upstream MCP Servers

### Install CDK Server
```bash
# Using npm
npm install -g @virons/cdk-mcp-server

# Start server
cdk-mcp-server --port 9140
```

### Install Terraform Server
```bash
# Using pip
pip install virons-terraform-mcp-server

# Start server
terraform-mcp-server --port 9142
```

### Install CloudFormation Server
```bash
# Using pip
pip install virons-cloudformation-mcp-server

# Start server
cfn-mcp-server --port 9141
```

## Database Setup (Optional)

### PostgreSQL for Audit Logs
```bash
# Using Docker
docker run -d \
  --name virons-postgres \
  -e POSTGRES_DB=virons \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secure-password \
  -p 5432:5432 \
  postgres:15

# Create schema
psql -h localhost -U admin -d virons -f schema.sql
```

### AWS RDS (Production)
```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier virons-audit \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --engine-version 15.4 \
  --master-username admin \
  --master-user-password secure-password \
  --allocated-storage 100 \
  --backup-retention-period 7 \
  --multi-az \
  --storage-encrypted

# Wait for instance
aws rds wait db-instance-available \
  --db-instance-identifier virons-audit
```

## S3 Setup (Optional)

### Create Audit Log Bucket
```bash
# Create bucket
aws s3 mb s3://virons-audit-logs --region eu-central-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket virons-audit-logs \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket virons-audit-logs \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket virons-audit-logs \
  --lifecycle-configuration file://lifecycle.json
```

## Troubleshooting

### Python Version Issues
```bash
# Check Python version
python --version

# Install Python 3.11
brew install python@3.11  # macOS
# or
sudo apt install python3.11  # Ubuntu

# Use specific version
python3.11 -m pip install virons-infrastructure-mcp-server
```

### Permission Errors
```bash
# Install for user only
pip install --user virons-infrastructure-mcp-server

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install virons-infrastructure-mcp-server
```

### AWS Credentials
```bash
# Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_REGION=eu-central-1

# Verify credentials
aws sts get-caller-identity
```

### Port Already in Use
```bash
# Find process using port
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Kill process
kill -9 <PID>

# Or use different port
python -m virons.infrastructure_mcp_server.server --port 8081
```

### Import Errors
```bash
# Reinstall package
pip uninstall virons-infrastructure-mcp-server
pip install virons-infrastructure-mcp-server

# Clear pip cache
pip cache purge

# Install with verbose output
pip install -v virons-infrastructure-mcp-server
```

## Uninstallation

### Remove Package
```bash
# Using pip
pip uninstall virons-infrastructure-mcp-server

# Remove configuration
rm -rf ~/.virons

# Remove virtual environment
rm -rf venv
```

### Remove Kubernetes Deployment
```bash
# Uninstall Helm release
helm uninstall virons-infrastructure -n virons-infrastructure

# Delete namespace
kubectl delete namespace virons-infrastructure
```

### Remove Docker
```bash
# Stop container
docker stop virons-infrastructure

# Remove container
docker rm virons-infrastructure

# Remove image
docker rmi virons/infrastructure-mcp-server:latest
```

## Next Steps

- [First Deployment Tutorial](./first-deployment.md)
- [Configuration Guide](../reference/configuration.md)
- [Troubleshooting Guide](./troubleshooting.md)

## Support

- **Documentation**: https://docs.virons.ai
- **Issues**: https://github.com/virons-ai/virons-infrastructure-mcp-server/issues
- **Slack**: #support on Virons Slack
- **Email**: support@virons.ai

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
