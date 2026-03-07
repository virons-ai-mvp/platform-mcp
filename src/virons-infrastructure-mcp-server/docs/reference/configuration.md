# Configuration Reference

**Version**: 1.0
**Last Updated**: 2026-03-07

## Overview

Complete configuration reference for the Virons Infrastructure MCP Server.

## Configuration Methods

### 1. Environment Variables
```bash
export AWS_REGION=eu-central-1
export LOG_LEVEL=INFO
```

### 2. Configuration File
```yaml
# config.yaml
aws:
  region: eu-central-1
```

### 3. Command Line Arguments
```bash
python -m virons.infrastructure_mcp_server.server --port 8080 --log-level DEBUG
```

### 4. Helm Values
```yaml
# values.yaml
config:
  aws:
    region: eu-central-1
```

## Environment Variables

### AWS Configuration

**AWS_REGION**
- **Description**: Default AWS region
- **Type**: String
- **Default**: `us-east-1`
- **Example**: `eu-central-1`

**AWS_ACCESS_KEY_ID**
- **Description**: AWS access key (not recommended, use IAM roles)
- **Type**: String
- **Default**: None
- **Example**: `AKIAIOSFODNN7EXAMPLE`

**AWS_SECRET_ACCESS_KEY**
- **Description**: AWS secret key (not recommended, use IAM roles)
- **Type**: String
- **Default**: None
- **Example**: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

**AWS_PROFILE**
- **Description**: AWS CLI profile name
- **Type**: String
- **Default**: `default`
- **Example**: `virons-prod`

### Server Configuration

**SERVER_HOST**
- **Description**: Server bind address
- **Type**: String
- **Default**: `0.0.0.0`
- **Example**: `127.0.0.1`

**SERVER_PORT**
- **Description**: Server port
- **Type**: Integer
- **Default**: `8080`
- **Example**: `9100`

**TRANSPORT**
- **Description**: Transport mode
- **Type**: String
- **Values**: `stdio`, `http`, `api`
- **Default**: `stdio`

**WORKERS**
- **Description**: Number of worker processes
- **Type**: Integer
- **Default**: `4`
- **Example**: `8`

### Logging Configuration

**LOG_LEVEL**
- **Description**: Logging level
- **Type**: String
- **Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Default**: `INFO`

**LOG_FORMAT**
- **Description**: Log output format
- **Type**: String
- **Values**: `json`, `text`
- **Default**: `json`

**LOG_FILE**
- **Description**: Log file path
- **Type**: String
- **Default**: `logs/server.log`
- **Example**: `/var/log/virons/server.log`

### Database Configuration

**DB_HOST**
- **Description**: Database host
- **Type**: String
- **Default**: `localhost`
- **Example**: `virons-audit.xxxxx.rds.amazonaws.com`

**DB_PORT**
- **Description**: Database port
- **Type**: Integer
- **Default**: `5432`

**DB_NAME**
- **Description**: Database name
- **Type**: String
- **Default**: `virons`

**DB_USER**
- **Description**: Database username
- **Type**: String
- **Default**: `admin`

**DB_PASSWORD**
- **Description**: Database password
- **Type**: String
- **Default**: None
- **Security**: Store in secrets manager

**DB_POOL_SIZE**
- **Description**: Connection pool size
- **Type**: Integer
- **Default**: `10`
- **Example**: `20`

### S3 Configuration

**S3_BUCKET**
- **Description**: S3 bucket for audit logs
- **Type**: String
- **Default**: None
- **Example**: `virons-audit-logs`

**S3_PREFIX**
- **Description**: S3 key prefix
- **Type**: String
- **Default**: `audit-logs/`
- **Example**: `prod/audit-logs/`

**S3_REGION**
- **Description**: S3 bucket region
- **Type**: String
- **Default**: Same as AWS_REGION
- **Example**: `eu-central-1`

### Upstream Servers

**CDK_SERVER_HOST**
- **Description**: CDK MCP server host
- **Type**: String
- **Default**: `cdk-server`
- **Example**: `localhost`

**CDK_SERVER_PORT**
- **Description**: CDK MCP server port
- **Type**: Integer
- **Default**: `9140`

**TERRAFORM_SERVER_HOST**
- **Description**: Terraform MCP server host
- **Type**: String
- **Default**: `terraform-server`

**TERRAFORM_SERVER_PORT**
- **Description**: Terraform MCP server port
- **Type**: Integer
- **Default**: `9142`

**CFN_SERVER_HOST**
- **Description**: CloudFormation MCP server host
- **Type**: String
- **Default**: `cfn-server`

**CFN_SERVER_PORT**
- **Description**: CloudFormation MCP server port
- **Type**: Integer
- **Default**: `9141`

### Metrics Configuration

**METRICS_ENABLED**
- **Description**: Enable Prometheus metrics
- **Type**: Boolean
- **Default**: `true`

**METRICS_PORT**
- **Description**: Metrics endpoint port
- **Type**: Integer
- **Default**: `8080`

**METRICS_PATH**
- **Description**: Metrics endpoint path
- **Type**: String
- **Default**: `/metrics`

### Compliance Configuration

**COMPLIANCE_LOGGING_ENABLED**
- **Description**: Enable compliance logging
- **Type**: Boolean
- **Default**: `true`

**AUDIT_LOG_RETENTION_DAYS**
- **Description**: Audit log retention period
- **Type**: Integer
- **Default**: `3650` (10 years)

**COMPLIANCE_REGULATIONS**
- **Description**: Applicable regulations
- **Type**: String (comma-separated)
- **Default**: `BaFin,GDPR,DORA,EU_AI_Act`

### Timeout Configuration

**DEFAULT_TIMEOUT**
- **Description**: Default operation timeout (seconds)
- **Type**: Integer
- **Default**: `300`
- **Example**: `600`

**DEPLOY_TIMEOUT**
- **Description**: Deployment timeout (seconds)
- **Type**: Integer
- **Default**: `600`

**DESTROY_TIMEOUT**
- **Description**: Destroy timeout (seconds)
- **Type**: Integer
- **Default**: `600`

**HTTP_TIMEOUT**
- **Description**: HTTP request timeout (seconds)
- **Type**: Integer
- **Default**: `30`

## Configuration File

### YAML Format

```yaml
# config.yaml

# AWS Configuration
aws:
  region: eu-central-1
  profile: virons-prod

# Server Configuration
server:
  host: 0.0.0.0
  port: 8080
  transport: api
  workers: 4

# Logging Configuration
logging:
  level: INFO
  format: json
  file: /var/log/virons/server.log

# Database Configuration
database:
  host: virons-audit.xxxxx.rds.amazonaws.com
  port: 5432
  name: virons
  user: admin
  pool_size: 20

# S3 Configuration
s3:
  bucket: virons-audit-logs
  prefix: prod/audit-logs/
  region: eu-central-1

# Upstream Servers
upstream:
  cdk:
    host: cdk-server
    port: 9140
  terraform:
    host: terraform-server
    port: 9142
  cloudformation:
    host: cfn-server
    port: 9141

# Metrics Configuration
metrics:
  enabled: true
  port: 8080
  path: /metrics

# Compliance Configuration
compliance:
  logging_enabled: true
  retention_days: 3650
  regulations:
    - BaFin
    - GDPR
    - DORA
    - EU_AI_Act

# Timeout Configuration
timeouts:
  default: 300
  deploy: 600
  destroy: 600
  http: 30
```

### Load Configuration File

```bash
# Using environment variable
export CONFIG_FILE=/etc/virons/config.yaml
python -m virons.infrastructure_mcp_server.server

# Using command line
python -m virons.infrastructure_mcp_server.server --config /etc/virons/config.yaml
```

## Helm Values

### values.yaml

```yaml
# Helm values for Kubernetes deployment

replicaCount: 3

image:
  repository: virons/infrastructure-mcp-server
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

config:
  aws:
    region: eu-central-1

  logging:
    level: INFO
    format: json

  database:
    host: virons-audit.xxxxx.rds.amazonaws.com
    port: 5432
    name: virons
    user: admin
    poolSize: 20

  s3:
    bucket: virons-audit-logs
    prefix: prod/audit-logs/

  upstream:
    cdk:
      host: cdk-server
      port: 9140
    terraform:
      host: terraform-server
      port: 9142
    cloudformation:
      host: cfn-server
      port: 9141

secrets:
  database:
    password: ""  # Set via --set or sealed secrets

serviceAccount:
  create: true
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/virons-infrastructure

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: infrastructure.virons.ai
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: infrastructure-tls
      hosts:
        - infrastructure.virons.ai
```

### Override Values

```bash
# Install with custom values
helm install virons-infrastructure ./helm/virons-infrastructure \
  --set replicaCount=5 \
  --set config.aws.region=us-east-1 \
  --set secrets.database.password=secure-password

# Or use values file
helm install virons-infrastructure ./helm/virons-infrastructure \
  -f values-prod.yaml
```

## Command Line Arguments

```bash
python -m virons.infrastructure_mcp_server.server [OPTIONS]

Options:
  --transport TEXT        Transport mode: stdio, http, api [default: stdio]
  --host TEXT            Server host [default: 0.0.0.0]
  --port INTEGER         Server port [default: 8080]
  --config TEXT          Configuration file path
  --log-level TEXT       Log level: DEBUG, INFO, WARNING, ERROR [default: INFO]
  --log-file TEXT        Log file path [default: logs/server.log]
  --workers INTEGER      Number of workers [default: 4]
  --version              Show version and exit
  --help                 Show this message and exit
```

## Configuration Precedence

Priority (highest to lowest):
1. Command line arguments
2. Environment variables
3. Configuration file
4. Default values

**Example**:
```bash
# Config file sets port=8080
# Environment variable overrides: export SERVER_PORT=9000
# Command line overrides all: --port 9100
# Final port: 9100
```

## Validation

### Required Configuration

Minimum required configuration:
```bash
export AWS_REGION=eu-central-1
export CDK_SERVER_HOST=cdk-server
```

### Validate Configuration

```bash
# Dry run to validate
python -m virons.infrastructure_mcp_server.server --validate

# Check configuration
python -m virons.infrastructure_mcp_server.server --show-config
```

## Security Best Practices

### Secrets Management

❌ **Don't**:
```bash
export DB_PASSWORD=my-password  # Visible in process list
```

✅ **Do**:
```bash
# Use AWS Secrets Manager
export DB_PASSWORD=$(aws secretsmanager get-secret-value \
  --secret-id virons/db-password \
  --query SecretString \
  --output text)

# Or Kubernetes secrets
kubectl create secret generic virons-db \
  --from-literal=password=secure-password
```

### IAM Roles

✅ **Prefer IAM roles over access keys**:
```yaml
# Kubernetes service account with IAM role
serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/virons-infrastructure
```

### Encryption

✅ **Enable encryption**:
```yaml
database:
  ssl_mode: require
  ssl_cert: /etc/ssl/certs/rds-ca-2019-root.pem

s3:
  encryption: AES256
```

## Environment-Specific Configuration

### Development
```yaml
# config-dev.yaml
logging:
  level: DEBUG
database:
  host: localhost
upstream:
  cdk:
    host: localhost
    port: 9140
```

### Staging
```yaml
# config-staging.yaml
logging:
  level: INFO
database:
  host: virons-staging-db.local
autoscaling:
  minReplicas: 2
  maxReplicas: 5
```

### Production
```yaml
# config-prod.yaml
logging:
  level: WARNING
database:
  host: virons-audit.xxxxx.rds.amazonaws.com
  pool_size: 20
autoscaling:
  minReplicas: 3
  maxReplicas: 10
compliance:
  logging_enabled: true
  retention_days: 3650
```

## Troubleshooting

### Configuration Not Loading

```bash
# Check config file exists
ls -la /etc/virons/config.yaml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('/etc/virons/config.yaml'))"

# Check environment variables
env | grep VIRONS
```

### Connection Issues

```bash
# Test database connection
psql -h $DB_HOST -U $DB_USER -d $DB_NAME

# Test upstream servers
curl http://$CDK_SERVER_HOST:$CDK_SERVER_PORT/health
```

## References

- [Installation Guide](../getting-started/installation.md)
- [Deployment Guide](../operations/deployment-guide.md)
- [API Reference](./api-reference.md)

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
