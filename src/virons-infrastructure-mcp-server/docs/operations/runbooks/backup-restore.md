# Backup and Restore Runbook

**Version**: 1.0
**Last Updated**: 2026-03-07
**Owner**: Operations Team

## Overview

Procedures for backing up and restoring the Virons Infrastructure MCP Server data, including audit logs, configuration, and database.

## Backup Strategy

### Backup Components

| Component | Method | Frequency | Retention | Location |
|-----------|--------|-----------|-----------|----------|
| Audit Logs | S3 sync | Real-time | 10 years | S3 + Glacier |
| RDS Database | Automated | Daily | 7 days | AWS RDS |
| Configuration | Git | On change | Indefinite | GitHub |
| Kubernetes State | Velero | Daily | 30 days | S3 |

### RPO/RTO Targets

- **RPO** (Recovery Point Objective): 1 hour
- **RTO** (Recovery Time Objective): 4 hours

## Audit Logs Backup

### Automatic Backup

**S3 Configuration**:
```yaml
Bucket: virons-audit-logs
Versioning: Enabled
Lifecycle:
  - Transition to Glacier: 365 days
  - Expiration: 3650 days (10 years)
Replication:
  Destination: eu-west-1
  Status: Enabled
Encryption: AES-256
```

### Verify Backup

```bash
# Check S3 bucket
aws s3 ls s3://virons-audit-logs/ --recursive | tail -20

# Verify versioning
aws s3api get-bucket-versioning --bucket virons-audit-logs

# Check replication status
aws s3api get-bucket-replication --bucket virons-audit-logs

# Verify encryption
aws s3api get-bucket-encryption --bucket virons-audit-logs
```

### Manual Backup

```bash
# Backup specific date range
aws s3 sync s3://virons-audit-logs/2026/03/ \
  ./backup/audit-logs/2026-03/ \
  --storage-class GLACIER

# Verify backup
aws s3 ls s3://virons-audit-logs/2026/03/ --recursive | wc -l
```

## Database Backup

### Automatic Backup (RDS)

**Configuration**:
```yaml
BackupRetentionPeriod: 7
PreferredBackupWindow: "03:00-04:00"
BackupTarget: region
CopyTagsToSnapshot: true
DeleteAutomatedBackups: false
```

### Verify Backup

```bash
# List automated backups
aws rds describe-db-instances \
  --db-instance-identifier virons-audit \
  --query 'DBInstances[0].BackupRetentionPeriod'

# List snapshots
aws rds describe-db-snapshots \
  --db-instance-identifier virons-audit \
  --query 'DBSnapshots[*].[DBSnapshotIdentifier,SnapshotCreateTime,Status]'

# Check latest backup
aws rds describe-db-snapshots \
  --db-instance-identifier virons-audit \
  --query 'DBSnapshots[0]' \
  --output json
```

### Manual Snapshot

```bash
# Create manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier virons-audit \
  --db-snapshot-identifier virons-audit-manual-$(date +%Y%m%d-%H%M%S)

# Verify snapshot
aws rds describe-db-snapshots \
  --db-snapshot-identifier virons-audit-manual-*

# Copy snapshot to another region
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier arn:aws:rds:eu-central-1:...:snapshot:virons-audit-manual-* \
  --target-db-snapshot-identifier virons-audit-dr-$(date +%Y%m%d) \
  --region eu-west-1
```

## Configuration Backup

### Git-Based Backup

**Automatic**:
- All configuration in Git
- Helm charts versioned
- Infrastructure as Code (CDK, Terraform, CloudFormation)

### Verify Backup

```bash
# Check Git history
git log --oneline --graph --all | head -20

# Verify remote backup
git remote -v
git fetch --all

# Check Helm releases
helm list -n virons-infrastructure

# Export current Helm values
helm get values virons-infrastructure > backup/helm-values-$(date +%Y%m%d).yaml
```

### Manual Backup

```bash
# Backup all Kubernetes resources
kubectl get all -n virons-infrastructure -o yaml > backup/k8s-resources-$(date +%Y%m%d).yaml

# Backup ConfigMaps
kubectl get configmap -n virons-infrastructure -o yaml > backup/configmaps-$(date +%Y%m%d).yaml

# Backup Secrets (encrypted)
kubectl get secrets -n virons-infrastructure -o yaml | \
  gpg --encrypt --recipient ops@virons.ai > backup/secrets-$(date +%Y%m%d).yaml.gpg
```

## Kubernetes State Backup (Velero)

### Install Velero

```bash
# Install Velero CLI
brew install velero

# Install Velero in cluster
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.9.0 \
  --bucket virons-velero-backups \
  --backup-location-config region=eu-central-1 \
  --snapshot-location-config region=eu-central-1 \
  --secret-file ./credentials-velero
```

### Create Backup

```bash
# Backup entire namespace
velero backup create virons-infrastructure-$(date +%Y%m%d) \
  --include-namespaces virons-infrastructure

# Backup with specific resources
velero backup create virons-full-$(date +%Y%m%d) \
  --include-namespaces virons-infrastructure \
  --include-resources deployments,services,configmaps,secrets

# Verify backup
velero backup describe virons-infrastructure-$(date +%Y%m%d)
velero backup logs virons-infrastructure-$(date +%Y%m%d)
```

### Scheduled Backups

```bash
# Create daily backup schedule
velero schedule create virons-daily \
  --schedule="0 3 * * *" \
  --include-namespaces virons-infrastructure \
  --ttl 720h

# List schedules
velero schedule get

# Verify scheduled backups
velero backup get
```

## Restore Procedures

### Restore Audit Logs

```bash
# Restore from S3
aws s3 sync s3://virons-audit-logs/2026/03/07/ \
  ./restore/audit-logs/2026-03-07/

# Restore from Glacier (requires retrieval)
aws s3api restore-object \
  --bucket virons-audit-logs \
  --key 2026/03/07/audit-log.json \
  --restore-request Days=7,GlacierJobParameters={Tier=Standard}

# Check restore status
aws s3api head-object \
  --bucket virons-audit-logs \
  --key 2026/03/07/audit-log.json
```

### Restore Database

**From Automated Backup**:
```bash
# List available backups
aws rds describe-db-snapshots \
  --db-instance-identifier virons-audit

# Restore to new instance
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier virons-audit-restored \
  --db-snapshot-identifier rds:virons-audit-2026-03-07-03-00

# Wait for restore
aws rds wait db-instance-available \
  --db-instance-identifier virons-audit-restored

# Update application to use restored DB
kubectl set env deployment/virons-infrastructure \
  DB_HOST=virons-audit-restored.xxxxx.eu-central-1.rds.amazonaws.com
```

**Point-in-Time Recovery**:
```bash
# Restore to specific time
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier virons-audit \
  --target-db-instance-identifier virons-audit-pitr \
  --restore-time 2026-03-07T08:30:00Z

# Verify restore
aws rds describe-db-instances \
  --db-instance-identifier virons-audit-pitr
```

### Restore Kubernetes State

**Using Velero**:
```bash
# List available backups
velero backup get

# Restore entire namespace
velero restore create --from-backup virons-infrastructure-20260307

# Restore specific resources
velero restore create --from-backup virons-infrastructure-20260307 \
  --include-resources deployments,services

# Monitor restore
velero restore describe virons-infrastructure-20260307
velero restore logs virons-infrastructure-20260307

# Verify restore
kubectl get all -n virons-infrastructure
```

**Manual Restore**:
```bash
# Restore from YAML backup
kubectl apply -f backup/k8s-resources-20260307.yaml

# Restore ConfigMaps
kubectl apply -f backup/configmaps-20260307.yaml

# Restore Secrets (decrypt first)
gpg --decrypt backup/secrets-20260307.yaml.gpg | kubectl apply -f -
```

### Restore Configuration

```bash
# Restore from Git
git checkout <commit-hash>

# Redeploy with Helm
helm upgrade virons-infrastructure ./helm/virons-infrastructure \
  -f backup/helm-values-20260307.yaml

# Verify deployment
kubectl rollout status deployment/virons-infrastructure
```

## Disaster Recovery Scenarios

### Scenario 1: Complete Region Failure

**Steps**:
1. **Activate DR region** (eu-west-1)
   ```bash
   # Switch to DR region
   export AWS_REGION=eu-west-1
   kubectl config use-context virons-dr
   ```

2. **Restore database from snapshot**
   ```bash
   aws rds restore-db-instance-from-db-snapshot \
     --db-instance-identifier virons-audit-dr \
     --db-snapshot-identifier <cross-region-snapshot>
   ```

3. **Deploy application**
   ```bash
   helm install virons-infrastructure ./helm/virons-infrastructure \
     --set database.host=virons-audit-dr.xxxxx.eu-west-1.rds.amazonaws.com
   ```

4. **Verify audit logs accessible**
   ```bash
   aws s3 ls s3://virons-audit-logs-replica/
   ```

5. **Update DNS** to point to DR region

**RTO**: 4 hours
**RPO**: 1 hour

### Scenario 2: Data Corruption

**Steps**:
1. **Identify corruption scope**
   ```bash
   # Check audit logs
   kubectl logs -l app=virons-infrastructure | grep ERROR
   ```

2. **Stop writes**
   ```bash
   kubectl scale deployment virons-infrastructure --replicas=0
   ```

3. **Restore from point-in-time**
   ```bash
   aws rds restore-db-instance-to-point-in-time \
     --source-db-instance-identifier virons-audit \
     --target-db-instance-identifier virons-audit-clean \
     --restore-time <time-before-corruption>
   ```

4. **Verify data integrity**
   ```bash
   psql -h virons-audit-clean.xxxxx.rds.amazonaws.com \
     -U admin -d virons -c "SELECT COUNT(*) FROM audit_logs;"
   ```

5. **Resume operations**
   ```bash
   kubectl set env deployment/virons-infrastructure \
     DB_HOST=virons-audit-clean.xxxxx.rds.amazonaws.com
   kubectl scale deployment virons-infrastructure --replicas=3
   ```

### Scenario 3: Accidental Deletion

**Steps**:
1. **Restore from Velero backup**
   ```bash
   velero restore create --from-backup virons-infrastructure-latest
   ```

2. **Verify resources**
   ```bash
   kubectl get all -n virons-infrastructure
   ```

3. **Check application health**
   ```bash
   kubectl get pods -l app=virons-infrastructure
   curl http://virons-infrastructure:8080/health
   ```

## Backup Verification

### Automated Testing

```bash
#!/bin/bash
# Test backup integrity monthly

# 1. Restore to test environment
velero restore create test-restore-$(date +%Y%m%d) \
  --from-backup virons-infrastructure-latest \
  --namespace-mappings virons-infrastructure:virons-test

# 2. Verify application starts
kubectl wait --for=condition=ready pod \
  -l app=virons-infrastructure \
  -n virons-test \
  --timeout=300s

# 3. Test database connectivity
kubectl exec -n virons-test deployment/virons-infrastructure -- \
  python -c "from infrastructure_mcp_server.compliance_logging import ComplianceLogger; print('OK')"

# 4. Cleanup
kubectl delete namespace virons-test
```

### Manual Verification

**Monthly Checklist**:
- [ ] Verify S3 audit logs accessible
- [ ] Check RDS automated backups exist
- [ ] Test Velero restore to test namespace
- [ ] Verify cross-region replication
- [ ] Check backup retention policies
- [ ] Review backup storage costs

## Backup Monitoring

### Alerts

**Critical**:
- RDS backup failed
- S3 replication failed
- Velero backup failed
- Backup age >24 hours

**Warning**:
- Backup size anomaly
- Backup duration >1 hour
- Storage approaching quota

### Metrics

```bash
# Check backup metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name BackupRetentionPeriodStorageUsed \
  --dimensions Name=DBInstanceIdentifier,Value=virons-audit \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average
```

## Compliance Requirements

### BaFin MaRisk AT 8.1

- ✅ 10-year retention for audit logs
- ✅ Immutable backups (S3 versioning)
- ✅ Cross-region replication
- ✅ Quarterly DR testing

### GDPR Article 32

- ✅ Ability to restore availability
- ✅ Encrypted backups (AES-256)
- ✅ Access control (IAM policies)
- ✅ Backup integrity verification

## Contact

- **On-Call**: PagerDuty
- **Backup Admin**: backup-admin@virons.ai
- **Platform Team**: platform@virons.ai
- **Escalation**: platform-lead@virons.ai

## References

- [AWS RDS Backup](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)
- [Velero Documentation](https://velero.io/docs/)
- [Incident Response](./incident-response.md)
- [Data Retention Policy](../../compliance/policies/data-retention.md)

---

**Last Updated**: 2026-03-07
**Next Review**: 2026-06-07
