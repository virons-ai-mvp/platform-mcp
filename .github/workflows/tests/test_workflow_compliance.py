#!/usr/bin/env python3
"""
TDD: Workflow compliance tests for platform-mcp.

Tests that all required workflows exist and meet compliance requirements.
Run before implementing workflows to ensure TDD approach.
"""
import os
from pathlib import Path
import yaml
import pytest

WORKFLOWS_DIR = Path(__file__).parent.parent
REPO_ROOT = WORKFLOWS_DIR.parent.parent


class TestWorkflowExistence:
    """Test that required workflows exist."""

    def test_gitleaks_workflow_exists(self):
        """GDPR Art 32 - Secret scanning required."""
        assert (WORKFLOWS_DIR / "gitleaks.yml").exists()

    def test_compliance_gate_workflow_exists(self):
        """BaFin AT 8.1 - Aggregate security checks required."""
        assert (WORKFLOWS_DIR / "compliance-gate.yml").exists()

    def test_org_governance_workflow_exists(self):
        """DORA Art 11 - Org-level governance required."""
        assert (WORKFLOWS_DIR / "org-governance-enforce.yml").exists()

    def test_workflow_governance_exists(self):
        """CI/CD governance required."""
        assert (WORKFLOWS_DIR / "workflow-governance.yml").exists()

    def test_secrets_rotation_exists(self):
        """DORA Art 11 - Secret rotation required."""
        assert (WORKFLOWS_DIR / "secrets-rotation.yml").exists()

    def test_compliance_checklist_exists(self):
        """Comprehensive compliance validation required."""
        assert (WORKFLOWS_DIR / "compliance-checklist.yml").exists()


class TestGitleaksWorkflow:
    """Test gitleaks workflow compliance."""

    @pytest.fixture
    def workflow(self):
        path = WORKFLOWS_DIR / "gitleaks.yml"
        if not path.exists():
            pytest.skip("gitleaks.yml not yet implemented")
        with open(path) as f:
            return yaml.safe_load(f)

    def test_runs_on_pr(self, workflow):
        """Must run on pull requests."""
        on_events = workflow.get("on") or workflow.get(True)
        assert "pull_request" in on_events

    def test_runs_on_push(self, workflow):
        """Must run on push to main."""
        on_events = workflow.get("on") or workflow.get(True)
        assert "push" in on_events

    def test_uses_gitleaks_action(self, workflow):
        """Must use official gitleaks action."""
        jobs = workflow["jobs"]
        scan_job = jobs.get("gitleaks-scan") or jobs.get("secret-scan")
        assert scan_job is not None
        steps = scan_job["steps"]
        assert any("gitleaks/gitleaks-action" in str(step.get("uses", "")) for step in steps)

    def test_has_fetch_depth_zero(self, workflow):
        """Must scan full git history."""
        jobs = workflow["jobs"]
        scan_job = jobs.get("gitleaks-scan") or jobs.get("secret-scan")
        steps = scan_job["steps"]
        checkout = next((s for s in steps if "actions/checkout" in str(s.get("uses", ""))), None)
        assert checkout is not None
        assert checkout.get("with", {}).get("fetch-depth") == 0


class TestComplianceGateWorkflow:
    """Test compliance-gate workflow."""

    @pytest.fixture
    def workflow(self):
        path = WORKFLOWS_DIR / "compliance-gate.yml"
        if not path.exists():
            pytest.skip("compliance-gate.yml not yet implemented")
        with open(path) as f:
            return yaml.safe_load(f)

    def test_aggregates_security_checks(self, workflow):
        """Must aggregate multiple security jobs."""
        jobs = workflow["jobs"]
        gate_job = jobs.get("compliance-gate")
        assert gate_job is not None
        assert "needs" in gate_job
        assert len(gate_job["needs"]) >= 3  # At least 3 security checks

    def test_includes_secret_scan(self, workflow):
        """Must include secret scanning."""
        jobs = workflow["jobs"]
        assert any("secret" in name.lower() for name in jobs.keys())

    def test_includes_sast(self, workflow):
        """Must include SAST scanning."""
        jobs = workflow["jobs"]
        assert any("sast" in name.lower() or "bandit" in name.lower() for name in jobs.keys())

    def test_posts_pr_comment(self, workflow):
        """Must post compliance scorecard to PR."""
        jobs = workflow["jobs"]
        gate_job = jobs.get("compliance-gate")
        steps = gate_job["steps"]
        assert any("github-script" in str(step.get("uses", "")) for step in steps)


class TestOrgGovernanceWorkflow:
    """Test org-governance-enforce workflow."""

    @pytest.fixture
    def workflow(self):
        path = WORKFLOWS_DIR / "org-governance-enforce.yml"
        if not path.exists():
            pytest.skip("org-governance-enforce.yml not yet implemented")
        with open(path) as f:
            return yaml.safe_load(f)

    def test_uses_reusable_workflows(self, workflow):
        """Must use reusable workflow pattern or have multiple validation jobs."""
        jobs = workflow["jobs"]
        assert len(jobs) >= 2
        # Either uses reusable workflows OR has multiple validation jobs
        has_reusable = any("uses" in job for job in jobs.values())
        has_multiple_jobs = len(jobs) >= 4
        assert has_reusable or has_multiple_jobs

    def test_validates_governance_manifest(self, workflow):
        """Must validate .github/governance-manifest.yaml."""
        jobs = workflow["jobs"]
        # Should have a job that checks governance manifest
        assert any("governance" in name.lower() for name in jobs.keys())


class TestWorkflowGovernance:
    """Test workflow-governance.yml."""

    @pytest.fixture
    def workflow(self):
        path = WORKFLOWS_DIR / "workflow-governance.yml"
        if not path.exists():
            pytest.skip("workflow-governance.yml not yet implemented")
        with open(path) as f:
            return yaml.safe_load(f)

    def test_validates_workflow_structure(self, workflow):
        """Must validate workflow YAML structure."""
        jobs = workflow["jobs"]
        assert "validate-workflows" in jobs or "workflow-lint" in jobs


class TestSecretsRotation:
    """Test secrets-rotation.yml."""

    @pytest.fixture
    def workflow(self):
        path = WORKFLOWS_DIR / "secrets-rotation.yml"
        if not path.exists():
            pytest.skip("secrets-rotation.yml not yet implemented")
        with open(path) as f:
            return yaml.safe_load(f)

    def test_runs_on_schedule(self, workflow):
        """DORA Art 11 - Must run on schedule."""
        on_events = workflow.get("on") or workflow.get(True)
        assert "schedule" in on_events

    def test_has_manual_trigger(self, workflow):
        """Must support manual trigger."""
        on_events = workflow.get("on") or workflow.get(True)
        assert "workflow_dispatch" in on_events


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
