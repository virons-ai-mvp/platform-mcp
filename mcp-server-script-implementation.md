Task 1: Create virons.common — audit module (BaFin AT 8.1)
- Objective: Build src/virons-common/ with PEP 420 namespace, virons/common/audit.py implementing write_audit(). This is the foundation all
  servers depend on.
- Tests first: tests/test_audit.py — test returns audit_id, test logs structured data with loguru, test enforces required fields (
  correlation_id, service_name, calculation_type). tests/test_init.py — test __version__ exists and follows semver.
- Implementation: virons/__init__.py (PEP 420 extend_path), virons/common/__init__.py (exports + __version__), virons/common/audit.py —
  async write_audit(service_name, calculation_type, entity_id, input_data, output_data, metadata) using loguru structured logging, returns
  audit_id. DB write is a stub. pyproject.toml with hatchling, virons.common naming.
- Demo: from virons.common.audit import write_audit imports. uv run pytest passes — audit_id returned, structured log emitted.

Task 2: Add health, correlation, and residency modules to virons.common
- Objective: Complete the compliance baseline — DORA health, GDPR correlation threading, GDPR data residency guard.
- Tests first: tests/test_health.py — liveness returns ok, readiness fails when check fails, add_readiness_check works.
  tests/test_correlation.py — generates valid UUID, context propagation via contextvars. tests/test_residency.py — allows eu-central-1,
  rejects us-east-1, rejects None with DataResidencyError.
- Implementation: health.py — HealthCheck class with liveness(), readiness(), add_readiness_check(). correlation.py —
  generate_correlation_id() (UUID4), CorrelationContext (contextvars). residency.py — enforce_region(region) raises DataResidencyError if not
  eu-central-1. Update __init__.py exports.
- Demo: All imports work. enforce_region("us-east-1") raises. HealthCheck().liveness() returns {"status": "ok"}. uv run pytest all green.

Task 3: Scaffold script — argument parsing and directory creation
- Objective: Create scripts/scaffold_virons_server.py — the server domain's entry point. Accepts --name, --description, --port, --deps,
  --transport. Creates directory tree, refuses to overwrite.
- Tests first: scripts/tests/test_scaffold.py — valid args parse, missing required args fail, directory tree matches expected structure,
  idempotency (refuses overwrite with exit 1).
- Implementation: argparse, pathlib.Path. Creates full tree: src/virons-{name}-mcp-server/virons/{name}_mcp_server/ (server.py, models.py,
  consts.py, compliance.py), tests/ (4 test files), plus metadata files.
- Demo: python3 scripts/scaffold_virons_server.py --name test --description "Test" creates tree. Run again → "already exists", exit 1.
  Tests green.

Task 4: Scaffold — generate pyproject.toml and metadata files
- Objective: Template pyproject.toml (hatchling, virons.* naming, virons.common dependency, ruff/pyright/pytest/commitizen config), LICENSE
  , NOTICE (dual attribution), CHANGELOG.md, .gitignore, .python-version (3.10), uv-requirements.txt.
- Tests first: test pyproject.toml valid TOML, correct name/entry-point/deps. Test NOTICE contains "Virons Fintech" and "awslabs". Test
  .python-version is "3.10".
- Implementation: Template strings with substitution. NOTICE:
  virons.{name}-mcp-server\nCopyright {year} Virons Fintech. All Rights Reserved.\n\nBased on awslabs/mcp (https://github.com/awslabs/mcp)\nCopyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
- Demo: Scaffold a server, python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))" succeeds. Tests green.

Task 5: Scaffold — generate Python source files with compliance hooks
- Objective: Generate all .py files with Virons copyright header. Namespace __init__.py (PEP 420), package __init__.py (__version__),
  server.py (FastMCP + create_server + main with --allow-write and --transport), models.py (Pydantic stub), consts.py (SERVER_NAME,
  DATA_REGION), compliance.py (imports virons.common, provides audit_tool_call() wrapper).
- Tests first: test namespace init has extend_path. Test package init has __version__. Test server.py has create_server, main, FastMCP.
  Test compliance.py imports virons.common. Test all .py files start with copyright header.
- Implementation: server.py follows exact awslabs pattern. When --transport http, adds transport='sse' to mcp.run() and starts health
  endpoint thread. compliance.py provides audit_tool_call(correlation_id, tool_name, inputs, outputs).
- Demo: Generated server.py is valid Python. Tests green.

Task 6: Scaffold — generate Dockerfile, healthcheck, and test files
- Objective: Multi-stage Dockerfile (amazonlinux + uv, non-root, correct ENTRYPOINT), docker-healthcheck.sh (pgrep-based), and 4 test files
  (test_init.py, test_main.py, test_server.py, test_compliance.py) following awslabs patterns.
- Tests first: test Dockerfile has USER app, HEALTHCHECK, correct ENTRYPOINT. Test healthcheck references correct server. Test generated
  test files are valid Python.
- Implementation: Templates with {name} substitution. Test templates mirror awslabs patterns exactly.
- Demo: docker build succeeds. Generated tests pass with pytest. Tests green.

Task 7: Scaffold — generate README.md and validation summary
- Objective: README with compliance badges, install instructions, MCP config JSON. Final validation step in scaffold that checks all files
  exist. Print summary with compliance status.
- Tests first: test README contains server name, "Virons AI", compliance section. End-to-end test: scaffold into temp dir, verify all files
  exist.
- Implementation: README template. Summary:
  ✅ Scaffolded virons-{name}-mcp-server (X files)\n   Compliance: BaFin ✓ | GDPR ✓ | DORA ✓ | EU AI Act ✓\n   Next: cd src/virons-{name}-mcp-server && uv sync && uv run pytest
- Demo: Full scaffold produces complete directory. README renders. Summary shows all checks. Tests green.

Task 8: Shared Kind cluster setup (Infrastructure Domain)
- Objective: Create kind-config.yaml, scripts/kind-setup.sh, scripts/kind-teardown.sh, k8s/helm/virons-mcp/ (Chart.yaml, values-local.yaml,
  templates/), and Makefile targets (kind-up, kind-down, kind-status). Adapted from platform-services pattern but for MCP servers with dual
  transport.
- Tests first: tests/infra/test_kind_config.py — test kind-config.yaml is valid YAML, test it has containerd registry mirror, test port
  mappings don't conflict. tests/infra/test_helm_values.py — test values-local.yaml is valid YAML, test each server entry has required fields
  (name, image, port, resources).
- Implementation: kind-config.yaml with K8s 1.31, local registry on port 5001, port mappings for virons servers. kind-setup.sh — creates
  registry, creates cluster, connects network, waits for ready. Helm chart with deployment + service + healthcheck per server. Makefile with
  kind-up, kind-down, kind-status, kind-deploy.
- Demo: make kind-up creates cluster. kubectl get nodes shows ready. make kind-down tears down. Tests green.

Task 9: make register-server target (Infrastructure Domain)
- Objective: Create scripts/register-server.sh and Makefile target that appends a new virons server to kind-config.yaml (port mapping) and
  k8s/helm/virons-mcp/values-local.yaml (server entry). Separate bounded context from scaffold.
- Tests first: tests/infra/test_register_server.py — test adds port mapping to kind-config, test adds server entry to Helm values, test
  rejects duplicate port, test rejects duplicate name.
- Implementation: Python script (for YAML manipulation). Takes --name, --port. Appends containerPort: 30{port} / hostPort: {port} to kind-
  config. Appends server block to values-local.yaml with image, service type NodePort, resource limits.
- Demo: make register-server NAME=infrastructure PORT=9600 updates both files. Run again → "already registered". Tests green.

Task 10: Virons compliance gate CI workflow (Governance Domain)
- Objective: Create .github/workflows/virons-compliance-gate.yml that runs on PRs/pushes touching src/virons-*. Checks BaFin audit ordering
  (write_audit before forensic_flags), GDPR PII in logs, DORA health endpoints, EU AI Act model cards. Adapted from platform-services
  compliance-gate.yml but scoped to virons servers.
- Tests first: tests/ci/test_compliance_gate.py — test workflow YAML is valid, test it triggers on correct paths, test each check step
  exists (BaFin, GDPR, DORA, EU AI Act).
- Implementation: Workflow triggers on push/pull_request with paths: ['src/virons-*/**']. Steps: checkout, BaFin audit pattern check (grep
  for forensic_flags without preceding write_audit), GDPR PII check (grep for email/ssn/credit_card near log), DORA health check (verify
  health.py or HealthCheck import exists), EU AI Act model card check (for ml-related servers).
- Demo: Create a test file violating BaFin ordering → CI fails. Fix it → CI passes. Tests green.

Task 11: Add platform-mcp to org governance (Governance Domain)
- Objective: Add platform-mcp entry to .github-repo/governance/repo-manifest.yaml with profile mcp-servers, required checks (org-baseline,
  org-security, org-compliance, org-mcp-health, virons-compliance-gate), and required MCP servers. Update mcp-required.yaml with mcp-servers
  profile. Add governance unit tests.
- Tests first: Update .github-repo/tests/governance/test_validate_manifest.py — test platform-mcp entry exists, test it has correct
  profile, test required checks include virons-compliance-gate. Update .github-repo/tests/test_workflows.py if needed.
- Implementation: Append to repo-manifest.yaml:
  {name: platform-mcp, profile: mcp-servers, default_branch: main, required_checks: [org-baseline, org-security, org-compliance, org-mcp-health, virons-compliance-gate], mcp_required: [aws-documentation, aws-terraform, kubernetes]}
  . Add mcp-servers profile to mcp-required.yaml.
- Demo: python scripts/governance/validate_manifest.py passes with platform-mcp included. Tests green.

Task 12: Pre-commit hook additions for virons compliance (Governance Domain)
- Objective: Add virons-specific hooks to platform-mcp/.pre-commit-config.yaml — BaFin audit pattern validation (pre-commit), virons
  license header check (pre-commit). These complement the existing awslabs hooks (ruff, gitleaks, detect-secrets, pyright, pytest).
- Tests first: test .pre-commit-config.yaml is valid YAML, test it contains virons audit pattern hook, test it contains virons license
  header hook, test hooks don't conflict with existing awslabs hooks.
- Implementation: Add local hook check-virons-audit-pattern that greps src/virons-* for forensic_flags without preceding write_audit. Add
  local hook check-virons-license-header that verifies # Copyright Virons Fintech in src/virons-*/**/*.py. Both as language: system hooks
  using simple shell scripts in scripts/hooks/.
- Demo: pre-commit run --all-files passes on compliant code, fails on non-compliant. Tests green.