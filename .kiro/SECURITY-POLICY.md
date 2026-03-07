# Kiro Security Policy

## Permissions Model

### Allow (No Confirmation)
- ✅ Read any file
- ✅ Write to service directories (ingestion, forensic, ml, api, blockchain)
- ✅ Write to shared, cli, docs, scripts, k8s, .github, .kiro
- ✅ Run tests (Go, Python, Node)
- ✅ Run linters (golangci-lint, ruff, black, mypy)
- ✅ Run security tools (trufflehog, trivy, cosign verify)
- ✅ Run audit validation script
- ✅ Read-only kubectl commands

### Ask (Requires Confirmation)
- ⚠️ Git operations (commit, push, pull)
- ⚠️ Docker operations (build, push, run)
- ⚠️ Kubectl write operations (apply, delete, exec)
- ⚠️ Infrastructure tools (helm, argocd, terraform)
- ⚠️ File deletion (rm)
- ⚠️ Network operations (curl, wget)
- ⚠️ Package installation (pip, brew)
- ⚠️ Image signing (cosign sign)
- ⚠️ Write to .env*, .gitignore, .husky, Makefile, *.md

### Deny (Always Blocked)
- ❌ Bypass security hooks (--no-verify)
- ❌ Dangerous file operations (rm -rf, chmod 777)
- ❌ Privilege escalation (sudo)
- ❌ Code execution (eval, source)
- ❌ Write secrets (.env, *.pem, *.key, *secret*, *password*, *token*)

## MCP Servers

### Enabled (Safe)
- ✅ `filesystem` - Local file access (scoped to virons-services)
- ✅ `git` - Git history and blame (read-only)
- ✅ `context7` - Library documentation (no credentials)

### Disabled (Security Risk)
- ❌ `postgres` - Database access (credentials in env)
- ❌ `aws-kb` - AWS access (potential credential leakage)
- ❌ `aws-terraform` - Infrastructure access (too powerful)
- ❌ `MCP_DOCKER` - Docker access (container escape risk)

## Security Rules

### Never Allow Kiro To:
1. Commit or push with `--no-verify` (bypasses security hooks)
2. Write to `.env` files (secrets)
3. Write to `.pem`, `.key` files (private keys)
4. Execute `sudo` commands (privilege escalation)
5. Run `rm -rf` (destructive)
6. Access databases directly (use application layer)
7. Access AWS APIs directly (use AWS CLI with confirmation)

### Always Require Confirmation For:
1. Git operations (commit, push, pull, merge)
2. Docker operations (build, push, run)
3. Kubernetes write operations (apply, delete)
4. Package installation (pip, brew, npm)
5. Network operations (curl, wget)
6. Infrastructure changes (terraform, helm)

### Safe Without Confirmation:
1. Reading any file
2. Writing to service code directories
3. Running tests and linters
4. Running security scans
5. Read-only kubectl commands

## Conflict Prevention

### File Write Conflicts
- Kiro can write to service directories without confirmation
- Kiro must ask before modifying root-level config files
- Kiro cannot write to secret files

### Command Conflicts
- Kiro can run tests and linters freely
- Kiro must ask before git operations
- Kiro cannot bypass security hooks

### MCP Server Conflicts
- Only safe, read-only MCP servers enabled
- No database or cloud API access
- No credential exposure risk

## Audit Trail

All Kiro operations are logged via:
- Git commits (for code changes)
- Command history (for bash operations)
- Security hooks (for validation)

## Emergency Override

If Kiro needs to bypass security (production incident):
1. User must manually set `VIRONS_EMERGENCY_BYPASS=true`
2. User must use `--no-verify` explicitly
3. User must document in `SECURITY.md`
4. Kiro cannot do this automatically

## Review Schedule

Review this policy:
- After any security incident
- When adding new MCP servers
- When changing permission model
- Quarterly (minimum)

Last reviewed: 2026-02-26
