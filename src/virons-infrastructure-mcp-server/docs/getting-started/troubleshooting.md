# Troubleshooting Guide

**Version**: 1.0
**Last Updated**: 2026-03-07

## Common Issues

### Server Issues

#### Server Won't Start

**Symptoms**:
- Server exits immediately
- Port binding errors
- Import errors

**Solutions**:
```bash
# Check Python version
python --version  # Must be 3.11+

# Check port availability
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Use different port
python -m virons.infrastructure_mcp_server.server --port 8081

# Check dependencies
pip list | grep virons

# Reinstall
pip uninstall virons-infrastructure-mcp-server
pip install virons-infrastructure-mcp-server
```

#### Server Crashes Randomly

**Symptoms**:
- Server stops unexpectedly
- OOMKilled in Kubernetes
- Connection reset errors

**Solutions**:
```bash
# Check logs
kubectl logs -l app=virons-infrastructure --tail=100

# Check memory usage
kubectl top pods -l app=virons-infrastructure

# Increase memory limits
helm upgrade virons-infrastructure ./helm/virons-infrastructure \
  --set resources.limits.memory=4Gi

# Check for memory leaks
python -m memory_profiler server.py
```

### Deployment Issues

#### Deployment Fails

**Symptoms**:
- Deployment returns error
- Stack stuck in CREATE_IN_PROGRESS
- Timeout errors

**Solutions**:
```bash
# Check upstream server
curl http://cdk-server:9140/health

# Increase timeout
curl -X POST http://localhost:8080/api/deploy \
  -d '{"stack_name": "test", "tool": "cdk", "timeout": 600}'

# Check AWS credentials
aws sts get-caller-identity

# Check CloudFormation events
aws cloudformation describe-stack-events \
  --stack-name my-stack \
  --max-items 10

# Check logs
kubectl logs -l app=virons-infrastructure | grep ERROR
```

#### Stack Already Exists

**Symptoms**:
- "Stack already exists" error
- Deployment fails with conflict

**Solutions**:
```bash
# List existing stacks
curl http://localhost:8080/api/stacks?tool=cdk&region=eu-central-1

# Destroy existing stack
curl -X POST http://localhost:8080/api/destroy \
  -d '{"stack_name": "my-stack", "tool": "cdk", "region": "eu-central-1"}'

# Or use different stack name
curl -X POST http://localhost:8080/api/deploy \
  -d '{"stack_name": "my-stack-v2", "tool": "cdk", "region": "eu-central-1"}'
```

#### Insufficient Permissions

**Symptoms**:
- "Access Denied" errors
- "User not authorized" errors
- 403 Forbidden

**Solutions**:
```bash
# Check IAM permissions
aws iam get-user

# Attach required policies
aws iam attach-user-policy \
  --user-name my-user \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

# Use IAM role (Kubernetes)
kubectl annotate serviceaccount virons-infrastructure \
  eks.amazonaws.com/role-arn=arn:aws:iam::123456789012:role/virons-infrastructure

# Check RBAC (Kubernetes)
kubectl auth can-i create deployments --as=system:serviceaccount:virons-infrastructure:default
```

### Connection Issues

#### Cannot Connect to Upstream Server

**Symptoms**:
- "Connection refused" errors
- "Host not found" errors
- Timeout connecting to upstream

**Solutions**:
```bash
# Check server is running
curl http://cdk-server:9140/health

# Check network connectivity
ping cdk-server
telnet cdk-server 9140

# Check Kubernetes service
kubectl get svc cdk-server
kubectl get endpoints cdk-server

# Check network policies
kubectl get networkpolicies

# Port forward for testing
kubectl port-forward svc/cdk-server 9140:9140
```

#### MCP Protocol Errors

**Symptoms**:
- "Invalid JSON-RPC" errors
- "Method not found" errors
- Protocol version mismatch

**Solutions**:
```bash
# Check MCP version
pip show mcp | grep Version

# Update MCP
pip install --upgrade mcp

# Test with simple request
echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}' | \
  python -m virons.infrastructure_mcp_server.server --transport stdio

# Check server logs
tail -f logs/server.log
```

### Authentication Issues

#### AWS Credentials Not Found

**Symptoms**:
- "Unable to locate credentials"
- "No credentials found"
- "Invalid credentials"

**Solutions**:
```bash
# Configure AWS CLI
aws configure

# Set environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_REGION=eu-central-1

# Use IAM role (EC2/EKS)
# Attach role to instance/pod

# Check credentials
aws sts get-caller-identity

# Use profile
export AWS_PROFILE=virons
aws configure --profile virons
```

#### Kubernetes RBAC Errors

**Symptoms**:
- "Forbidden" errors in Kubernetes
- "User cannot create resource"
- RBAC permission denied

**Solutions**:
```bash
# Check service account
kubectl get serviceaccount virons-infrastructure

# Check role bindings
kubectl get rolebindings -n virons-infrastructure

# Create role binding
kubectl create rolebinding virons-admin \
  --clusterrole=admin \
  --serviceaccount=virons-infrastructure:default

# Check permissions
kubectl auth can-i create deployments \
  --as=system:serviceaccount:virons-infrastructure:default
```

### Performance Issues

#### Slow Deployments

**Symptoms**:
- Deployments take >5 minutes
- High CPU usage
- Slow response times

**Solutions**:
```bash
# Check resource usage
kubectl top pods -l app=virons-infrastructure

# Scale horizontally
kubectl scale deployment virons-infrastructure --replicas=5

# Increase resources
helm upgrade virons-infrastructure ./helm/virons-infrastructure \
  --set resources.requests.cpu=2000m \
  --set resources.requests.memory=2Gi

# Check upstream server performance
curl http://cdk-server:9140/metrics | grep duration

# Enable caching (if available)
export ENABLE_CACHE=true
```

#### High Memory Usage

**Symptoms**:
- Memory >80%
- OOMKilled pods
- Swap usage high

**Solutions**:
```bash
# Check memory usage
kubectl top pods -l app=virons-infrastructure

# Increase memory limits
helm upgrade virons-infrastructure ./helm/virons-infrastructure \
  --set resources.limits.memory=4Gi

# Check for memory leaks
kubectl logs -l app=virons-infrastructure | grep -i memory

# Restart pods
kubectl rollout restart deployment/virons-infrastructure
```

### Audit Log Issues

#### Audit Logs Not Written

**Symptoms**:
- No logs in S3
- Empty audit log files
- Missing compliance entries

**Solutions**:
```bash
# Check S3 bucket exists
aws s3 ls s3://virons-audit-logs/

# Check S3 permissions
aws s3api get-bucket-policy --bucket virons-audit-logs

# Check environment variables
kubectl get deployment virons-infrastructure -o yaml | grep S3_BUCKET

# Test S3 write
aws s3 cp test.txt s3://virons-audit-logs/test.txt

# Check logs for errors
kubectl logs -l app=virons-infrastructure | grep "audit"
```

#### Cannot Read Audit Logs

**Symptoms**:
- "Access Denied" reading S3
- Empty log queries
- Missing log entries

**Solutions**:
```bash
# Check S3 read permissions
aws s3 ls s3://virons-audit-logs/ --recursive

# Check IAM policy
aws iam get-user-policy --user-name my-user --policy-name S3ReadPolicy

# Check bucket encryption
aws s3api get-bucket-encryption --bucket virons-audit-logs

# Download logs
aws s3 sync s3://virons-audit-logs/2026/03/07/ ./logs/
```

### Database Issues

#### Cannot Connect to Database

**Symptoms**:
- "Connection refused" to RDS
- "Host not found" errors
- Timeout connecting to database

**Solutions**:
```bash
# Check RDS instance
aws rds describe-db-instances --db-instance-identifier virons-audit

# Check security group
aws ec2 describe-security-groups --group-ids sg-xxxxx

# Test connection
psql -h virons-audit.xxxxx.rds.amazonaws.com -U admin -d virons

# Check environment variables
kubectl get deployment virons-infrastructure -o yaml | grep DB_HOST

# Port forward for testing
kubectl port-forward svc/postgres 5432:5432
```

#### Database Queries Slow

**Symptoms**:
- Queries take >1 second
- High database CPU
- Connection pool exhausted

**Solutions**:
```bash
# Check RDS metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=virons-audit

# Add indexes
psql -h virons-audit.xxxxx.rds.amazonaws.com -U admin -d virons \
  -c "CREATE INDEX idx_timestamp ON audit_logs(timestamp);"

# Increase connection pool
export DB_POOL_SIZE=20

# Scale RDS instance
aws rds modify-db-instance \
  --db-instance-identifier virons-audit \
  --db-instance-class db.t3.large
```

## Debugging Tools

### Enable Debug Logging
```bash
# Set log level
export LOG_LEVEL=DEBUG

# Start server with debug
python -m virons.infrastructure_mcp_server.server --log-level DEBUG

# In Kubernetes
kubectl set env deployment/virons-infrastructure LOG_LEVEL=DEBUG
```

### View Logs
```bash
# Local logs
tail -f logs/server.log

# Kubernetes logs
kubectl logs -l app=virons-infrastructure -f

# Previous pod logs
kubectl logs -l app=virons-infrastructure --previous

# All pods
kubectl logs -l app=virons-infrastructure --all-containers=true
```

### Check Metrics
```bash
# Prometheus metrics
curl http://localhost:8080/metrics

# Specific metric
curl http://localhost:8080/metrics | grep mcp_tool_duration

# Grafana dashboard
open http://grafana.virons.ai/d/infrastructure-mcp
```

### Network Debugging
```bash
# Test connectivity
curl -v http://cdk-server:9140/health

# DNS lookup
nslookup cdk-server

# Trace route
traceroute cdk-server

# Port scan
nmap -p 9140 cdk-server

# Kubernetes network
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- bash
```

### Database Debugging
```bash
# Connect to database
psql -h localhost -U admin -d virons

# Check connections
SELECT * FROM pg_stat_activity;

# Check table size
SELECT pg_size_pretty(pg_total_relation_size('audit_logs'));

# Check indexes
\d audit_logs

# Explain query
EXPLAIN ANALYZE SELECT * FROM audit_logs WHERE timestamp > NOW() - INTERVAL '1 day';
```

## Getting Help

### Check Documentation
- [Installation Guide](./installation.md)
- [First Deployment](./first-deployment.md)
- [Architecture Documentation](../architecture/)
- [Operations Runbooks](../operations/runbooks/)

### Search Issues
```bash
# GitHub issues
open https://github.com/virons-ai/virons-infrastructure-mcp-server/issues

# Search for error message
# Copy error and search in issues
```

### Ask for Help
- **Slack**: #support on Virons Slack
- **Email**: support@virons.ai
- **GitHub**: Create new issue with:
  - Error message
  - Steps to reproduce
  - Environment details
  - Logs

### Provide Debug Information
```bash
# Collect debug info
cat > debug-info.txt << EOF
Version: $(python -m virons.infrastructure_mcp_server.server --version)
Python: $(python --version)
OS: $(uname -a)
Kubernetes: $(kubectl version --short)
Error: <paste error here>
Logs: <paste relevant logs>
EOF
```

## References

- [Installation Guide](./installation.md)
- [First Deployment Tutorial](./first-deployment.md)
- [Incident Response Runbook](../operations/runbooks/incident-response.md)
- [GitHub Issues](https://github.com/virons-ai/virons-infrastructure-mcp-server/issues)

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
