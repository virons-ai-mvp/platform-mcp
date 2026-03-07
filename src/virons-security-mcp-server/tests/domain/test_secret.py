"""Tests for secret scanning domain entities."""
import pytest
from virons.security_mcp_server.domain.secret import SecretFinding, ScanRequest


def test_secret_finding_requires_type():
    with pytest.raises(ValueError):
        SecretFinding(type="", file="test.py", line=10, secret="xxx")


def test_secret_finding_requires_file():
    with pytest.raises(ValueError):
        SecretFinding(type="api_key", file="", line=10, secret="xxx")


def test_secret_finding_creation():
    finding = SecretFinding(
        type="aws_access_key",
        file="config.py",
        line=42,
        secret="AKIA***",
        commit="abc123"
    )
    assert finding.type == "aws_access_key"
    assert finding.file == "config.py"
    assert finding.line == 42


def test_scan_request_requires_path():
    with pytest.raises(ValueError):
        ScanRequest(repository_path="", scan_history=False)


def test_scan_request_creation():
    request = ScanRequest(repository_path="/repo", scan_history=True)
    assert request.repository_path == "/repo"
    assert request.scan_history is True


def test_scan_request_defaults_to_no_history():
    request = ScanRequest(repository_path="/repo")
    assert request.scan_history is False
