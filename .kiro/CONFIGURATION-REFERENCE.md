# Kiro Configuration Reference

Complete configuration hierarchy for Virons AI MVP platform.

## Configuration Hierarchy

Settings cascade from **repo → org → parent-org → global**, with repo-level having highest priority.

```
1. Repo:        .kiro/settings.json (highest priority)
2. Org:         ~/repos/virons-fintech/virons-ai-mvp/.kiro/settings.json
3. Parent Org:  ~/repos/virons-fintech/.kiro/settings.json
4. Global:      ~/.kiro/settings/cli.json (lowest priority)
```

## Configuration Categories

### Project Identification
```json
{
  "project.name": "platform-mcp",
  "project.type": "mcp-server-platform",
  "project.description": "Multi-service MCP platform"
}
```

### AWS Configuration
```json
{
  "aws.profile": "virons-management",
  "aws.region": "eu-central-1",
  "aws.accountId": "412179655775",
  "aws.ecr": "412179655775.dkr.ecr.eu-central-1.amazonaws.com",
  "aws.bedrock.region": "eu-central-1",
  "aws.bedrock.model": "amazon.nova-pro-v1:0"
}
```

### Kubernetes Configuration
```json
{
  "kubernetes.cluster": "virons-mvp",
  "kubernetes.version": "1.31",
  "kubernetes.context": "arn:aws:eks:eu-central-1:412179655775:cluster/virons-mvp",
  "kubernetes.namespace": "mcp-platform"
}
```

### Compliance Configuration
```json
{
  "compliance.frameworks": ["BaFin", "GDPR", "DORA", "EU-AI-Act"],
  "compliance.dataResidency": "eu-central-1",
  "compliance.enforceAuditPattern": true,
  "compliance.auditLogging": true,
  "compliance.piiEncryption": true,
  "compliance.kmsKeyAlias": "alias/virons-pii",
  "compliance.bafin.at81": true,
  "compliance.gdpr.art32": true,
  "compliance.dora.art11": true,
  "compliance.euAiAct.highRisk": true,
  "compliance.modelCards.required": true,
  "compliance.humanOversight.required": true
}
```

### Testing Configuration
```json
{
  "testing.tddMode": true,
  "testing.minCoverage": 95,
  "testing.runOnSave": false,
  "testing.framework": "pytest",
  "testing.unitTests": true,
  "testing.integrationTests": true,
  "testing.comprehensiveTests": true,
  "testing.testContainers": true,
  "testing.e2eTests": true,
  "testing.coverageReport": "html"
}
```

### Security Configuration
```json
{
  "security.scanOnCommit": true,
  "security.blockSecretsCommit": true,
  "security.trivyScanOnPush": true,
  "security.truffleHog": true,
  "security.codeQL": true,
  "security.dependabot": true,
  "security.dependabotSchedule": "weekly",
  "security.imageSigning": true,
  "security.cosign": true,
  "security.allowedRegistries": [
    "ghcr.io/virons-ai",
    "412179655775.dkr.ecr.eu-central-1.amazonaws.com"
  ],
  "security.runAsNonRoot": true,
  "security.readOnlyRootFilesystem": true,
  "security.dropCapabilities": ["ALL"],
  "security.networkPolicies": true,
  "security.opaAdmissionControl": true,
  "security.podSecurityStandards": "restricted",
  "security.secretsManagement": "aws-secrets-manager"
}
```

### Linting & Formatting
```json
{
  "linting.autoFix": false,
  "linting.go": "golangci-lint",
  "linting.python": "ruff",
  "linting.pythonConfig": ".ruff.toml",
  "linting.preCommitHooks": true,
  "formatting.go": "gofmt",
  "formatting.python": "black",
  "formatting.pythonLineLength": 100,
  "formatting.pythonTarget": "py312"
}
```

### Docker Configuration
```json
{
  "docker.baseImage": "python:3.12-slim",
  "docker.registry": "ghcr.io/virons-ai",
  "docker.buildKit": true,
  "docker.multiStage": true,
  "docker.scanOnBuild": true
}
```

### MCP Configuration
```json
{
  "mcp.gateway.enabled": true,
  "mcp.gateway.port": 9000,
  "mcp.gateway.correlationId": true,
  "mcp.gateway.metrics": true,
  "mcp.gateway.healthChecks": true,
  "mcp.servers": {
    "infrastructure": {"port": 9100, "tools": 78, "enabled": true},
    "security": {"port": 9500, "tools": 4, "enabled": true},
    "operations": {"port": 9510, "tools": 4, "enabled": true},
    "monitoring": {"port": 9520, "tools": 4, "enabled": true}
  }
}
```

### Architecture Configuration
```json
{
  "architecture.pattern": "DDD",
  "architecture.layers": ["application", "domain", "infrastructure"],
  "architecture.testPyramid": true,
  "architecture.microservices": true,
  "architecture.eventDriven": true
}
```

### Monitoring Configuration
```json
{
  "monitoring.prometheus": true,
  "monitoring.grafana": true,
  "monitoring.alertManager": true,
  "monitoring.metricsPort": 9090,
  "monitoring.healthEndpoint": "/health",
  "monitoring.readinessEndpoint": "/ready",
  "monitoring.metricsEndpoint": "/metrics",
  "monitoring.distributedTracing": true,
  "monitoring.correlationId": true,
  "monitoring.logAggregation": "cloudwatch",
  "monitoring.metricsRetention": "30d",
  "monitoring.logsRetention": "90d"
}
```

### Deployment Configuration
```json
{
  "deployment.strategy": "rolling",
  "deployment.maxUnavailable": 1,
  "deployment.maxSurge": 1,
  "deployment.minReadySeconds": 10,
  "deployment.progressDeadlineSeconds": 600,
  "deployment.argocd": true,
  "deployment.appOfApps": true,
  "deployment.gitops": true,
  "deployment.autoSync": false
}
```

### Resource Configuration
```json
{
  "resources.requests.cpu": "100m",
  "resources.requests.memory": "128Mi",
  "resources.limits.cpu": "500m",
  "resources.limits.memory": "512Mi"
}
```

### Autoscaling Configuration
```json
{
  "autoscaling.enabled": true,
  "autoscaling.minReplicas": 2,
  "autoscaling.maxReplicas": 10,
  "autoscaling.targetCPU": 70,
  "autoscaling.targetMemory": 80
}
```

### Resilience Configuration
```json
{
  "resilience.pdb.enabled": true,
  "resilience.pdb.minAvailable": 1,
  "resilience.gracefulShutdown": 30,
  "resilience.rto": "4h",
  "resilience.rpo": "1h",
  "resilience.backups.enabled": true,
  "resilience.backups.schedule": "0 2 * * *",
  "resilience.backups.retention": "30d"
}
```

### Documentation Configuration
```json
{
  "documentation.required": true,
  "documentation.docusaurus": true,
  "documentation.autoGenerate": true,
  "documentation.verifyOnPush": true,
  "documentation.examplesRequired": true,
  "documentation.testExamples": true,
  "documentation.architectureDecisions": true,
  "documentation.apiDocs": true
}
```

### Git Hooks Configuration
```json
{
  "git.hooks.enabled": true,
  "git.hooks.preCommit": ["trufflehog", "ruff", "pytest-fast"],
  "git.hooks.prePush": ["trivy", "verify-docs", "ddd-validation", "tdd-validation"],
  "git.hooks.commitMsg": ["conventional-commits"]
}
```

### CI/CD Configuration
```json
{
  "ci.provider": "github-actions",
  "ci.securityGate": true,
  "ci.qualityGate": true,
  "ci.coverageThreshold": 95,
  "ci.deployOnMerge": false,
  "ci.requireApprovals": 2,
  "ci.requireCodeOwners": true
}
```

### Python Configuration
```json
{
  "python.version": "3.12",
  "python.packageManager": "uv",
  "python.virtualenv": ".venv",
  "python.lockFile": "uv.lock"
}
```

### Go Configuration
```json
{
  "go.version": "1.23",
  "go.modules": true,
  "go.linter": "golangci-lint",
  "go.formatter": "gofmt"
}
```

### User Preferences (Global Only)
```json
{
  "user.name": "Amjad Alissa Alkhalaf",
  "user.email": "amjad@virons.ai",
  "chat.model": "claude-3-7-sonnet-20250219",
  "chat.temperature": 0.7,
  "chat.disableMarkdownRendering": false,
  "editor.defaultEditor": "cursor",
  "editor.autoSave": true,
  "terminal.shell": "zsh",
  "ui.theme": "dark",
  "privacy.telemetry": false
}
```

## Best Practices

### Global Settings (~/.kiro/settings/cli.json)
Use for personal preferences only:
- User information
- Chat model and temperature
- Editor preferences
- UI theme and appearance
- Terminal settings
- Privacy settings

### Parent Org Settings (~/repos/virons-fintech/.kiro/settings.json)
Use for organization-wide standards:
- Compliance frameworks
- Security policies
- Testing standards
- Git hooks
- CI/CD requirements
- Documentation standards

### Org Settings (~/repos/virons-fintech/virons-ai-mvp/.kiro/settings.json)
Use for product-level defaults:
- AWS account and region
- Kubernetes cluster
- Compliance specifics (BaFin, GDPR, DORA, EU AI Act)
- Monitoring and observability
- Deployment strategies
- Architecture patterns

### Repo Settings (.kiro/settings.json)
Use for project-specific configuration:
- Project name and type
- Service ports and tools
- MCP server configuration
- Resource limits
- Autoscaling parameters
- Project-specific overrides

## Viewing Configuration

```bash
# View all settings (merged)
kiro-cli config list

# View specific setting
kiro-cli config get testing.minCoverage

# View setting with source
kiro-cli config get testing.minCoverage --show-source

# View all settings from specific scope
kiro-cli config list --scope repo
kiro-cli config list --scope org
kiro-cli config list --scope global
```

## Modifying Configuration

```bash
# Set repo-level (project-specific)
kiro-cli config set mcp.gateway.port 9000 --scope repo

# Set org-level (team standards)
kiro-cli config set testing.minCoverage 95 --scope org

# Set global (personal preferences)
kiro-cli config set chat.model claude-3-7-sonnet-20250219 --scope global
```

## Version Control

- ✅ **Commit repo-level** (.kiro/settings.json) - team shares project config
- ✅ **Commit org-level** (virons-ai-mvp/.kiro/settings.json) - team shares org config
- ✅ **Commit parent org-level** (virons-fintech/.kiro/settings.json) - company standards
- ❌ **Never commit global** (~/.kiro/settings/cli.json) - personal preferences

## Compliance Validation

All configuration changes are validated against:
- BaFin MaRisk AT 8.1
- GDPR Art 32
- DORA Art 11
- EU AI Act

Run compliance check:
```bash
kiro-cli compliance-check
```

## Security Validation

All configuration changes are validated for:
- No secrets in config files
- Allowed registries only
- Security policies enforced
- Resource limits defined

Run security validation:
```bash
kiro-cli security-validation
```
