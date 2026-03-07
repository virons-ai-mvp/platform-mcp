"""Tests for compliance domain entities."""
import pytest
from virons.security_mcp_server.domain.compliance import ComplianceResult, GateCheck


def test_compliance_result_requires_status():
    with pytest.raises(ValueError):
        ComplianceResult(status="", gate_type="pre-commit", artifact="test.jar")


def test_compliance_result_validates_status():
    with pytest.raises(ValueError):
        ComplianceResult(status="invalid", gate_type="pre-commit", artifact="test.jar")


def test_compliance_result_creation():
    result = ComplianceResult(
        status="passed",
        gate_type="pre-deploy",
        artifact="/path/to/artifact.jar",
        checks_passed=5,
        checks_failed=0
    )
    assert result.status == "passed"
    assert result.checks_passed == 5


def test_gate_check_requires_gate_type():
    with pytest.raises(ValueError):
        GateCheck(gate_type="", artifact_path="/path")


def test_gate_check_validates_gate_type():
    with pytest.raises(ValueError):
        GateCheck(gate_type="invalid", artifact_path="/path")


def test_gate_check_creation():
    check = GateCheck(gate_type="post-deploy", artifact_path="/artifact.jar")
    assert check.gate_type == "post-deploy"
    assert check.artifact_path == "/artifact.jar"
