"""Tests for IAM policy domain entities."""
import pytest
from virons.security_mcp_server.domain.iam_policy import IAMPolicy, PolicyIssue


def test_iam_policy_requires_document():
    with pytest.raises(ValueError):
        IAMPolicy(policy_document={}, resource_type="user")


def test_iam_policy_validates_resource_type():
    with pytest.raises(ValueError):
        IAMPolicy(policy_document={"Version": "2012-10-17"}, resource_type="invalid")


def test_iam_policy_creation():
    policy = IAMPolicy(
        policy_document={"Version": "2012-10-17", "Statement": []},
        resource_type="role"
    )
    assert policy.resource_type == "role"
    assert policy.policy_document["Version"] == "2012-10-17"


def test_policy_issue_requires_severity():
    with pytest.raises(ValueError):
        PolicyIssue(severity="", message="Issue found", rule="rule-1")


def test_policy_issue_validates_severity():
    with pytest.raises(ValueError):
        PolicyIssue(severity="invalid", message="Issue", rule="rule-1")


def test_policy_issue_creation():
    issue = PolicyIssue(severity="high", message="Wildcard in action", rule="no-wildcards")
    assert issue.severity == "high"
    assert issue.message == "Wildcard in action"
