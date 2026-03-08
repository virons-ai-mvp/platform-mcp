# Kiro Configuration Hierarchy

Configuration is loaded in order of precedence (highest to lowest):

## 1. Repo-level (Highest Priority)
**Location**: `.kiro/settings.json`
**Scope**: Project-specific overrides
**Use for**: AWS coordinates, K8s cluster, project-specific compliance rules

```json
{
  "project.name": "virons-services",
  "aws.profile": "virons-management",
  "aws.region": "eu-central-1",
  "kubernetes.cluster": "virons-mvp",
  "compliance.frameworks": ["BaFin", "GDPR", "DORA", "EU-AI-Act"],
  "testing.minCoverage": 95
}
```

## 2. Org-level (Medium Priority)
**Location**: `~/repos/virons-fintech/.kiro/settings.json`
**Scope**: Organization-wide defaults
**Use for**: Shared compliance rules, testing standards, security policies

```json
{
  "compliance.frameworks": ["BaFin", "GDPR", "DORA", "EU-AI-Act"],
  "testing.tddMode": true,
  "testing.minCoverage": 95,
  "security.scanOnCommit": true
}
```

## 3. Global (Lowest Priority)
**Location**: `~/.kiro/settings/cli.json`
**Scope**: User-wide preferences
**Use for**: Personal preferences, editor choice, model selection

```json
{
  "chat.model": "claude-3-7-sonnet-20250219",
  "editor.defaultEditor": "cursor",
  "chat.temperature": 0.7
}
```

## Configuration Keys

### Project
- `project.name` - Project identifier
- `project.type` - Architecture type (microservices-monorepo, etc.)

### AWS
- `aws.profile` - AWS CLI profile name
- `aws.region` - Default AWS region
- `aws.accountId` - AWS account ID

### Kubernetes
- `kubernetes.cluster` - EKS cluster name
- `kubernetes.context` - kubectl context ARN

### Compliance
- `compliance.frameworks` - Array of regulatory frameworks
- `compliance.dataResidency` - Data residency region
- `compliance.enforceAuditPattern` - Enforce BaFin audit pattern

### Testing
- `testing.tddMode` - Enable TDD-first workflow
- `testing.minCoverage` - Minimum test coverage percentage
- `testing.runOnSave` - Auto-run tests on file save

### Security
- `security.scanOnCommit` - Run TruffleHog on commit
- `security.blockSecretsCommit` - Block commits with secrets
- `security.trivyScanOnPush` - Run Trivy on push

### Linting & Formatting
- `linting.autoFix` - Auto-fix linting issues
- `linting.go` - Go linter (golangci-lint)
- `linting.python` - Python linter (ruff)
- `formatting.go` - Go formatter (gofmt)
- `formatting.python` - Python formatter (black)

### Chat
- `chat.model` - LLM model identifier
- `chat.temperature` - Model temperature (0.0-1.0)
- `chat.maxTokens` - Maximum context tokens
- `chat.disableMarkdownRendering` - Disable markdown in responses

### Editor
- `editor.defaultEditor` - Default code editor (cursor, vscode, etc.)

### MCP
- `mcp.autoLoad` - Auto-load MCP servers
- `mcp.loadedBefore` - Internal flag for first-run experience

## Viewing Current Configuration

```bash
# View all settings (merged)
kiro-cli config list

# View specific setting
kiro-cli config get testing.minCoverage

# View setting source
kiro-cli config get testing.minCoverage --show-source
```

## Modifying Configuration

```bash
# Set repo-level (recommended for project settings)
kiro-cli config set aws.region eu-central-1 --scope repo

# Set org-level (recommended for team standards)
kiro-cli config set testing.minCoverage 95 --scope org

# Set global (recommended for personal preferences)
kiro-cli config set chat.model claude-3-7-sonnet-20250219 --scope global
```

## Best Practices

1. **Global**: Personal preferences only (editor, model, temperature)
2. **Org-level**: Team standards (compliance, testing, security)
3. **Repo-level**: Project specifics (AWS, K8s, data residency)

4. **Never commit global settings** to version control
5. **Always commit repo-level settings** to version control
6. **Optionally commit org-level settings** if shared across repos
