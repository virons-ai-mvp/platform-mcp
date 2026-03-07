"""Tests for audit event domain entities."""
import pytest
from virons.security_mcp_server.domain.audit import AuditEvent, AuditQuery


def test_audit_event_requires_event_name():
    with pytest.raises(ValueError):
        AuditEvent(event_name="", timestamp="2026-03-07T10:00:00Z", user="admin")


def test_audit_event_requires_timestamp():
    with pytest.raises(ValueError):
        AuditEvent(event_name="CreateUser", timestamp="", user="admin")


def test_audit_event_creation():
    event = AuditEvent(
        event_name="CreateUser",
        timestamp="2026-03-07T10:00:00Z",
        user="admin",
        resource="arn:aws:iam::123:user/test"
    )
    assert event.event_name == "CreateUser"
    assert event.user == "admin"


def test_audit_query_requires_start_time():
    with pytest.raises(ValueError):
        AuditQuery(start_time="", end_time="2026-03-07T10:00:00Z")


def test_audit_query_requires_end_time():
    with pytest.raises(ValueError):
        AuditQuery(start_time="2026-03-07T10:00:00Z", end_time="")


def test_audit_query_creation():
    query = AuditQuery(
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        event_name="CreateUser"
    )
    assert query.start_time == "2026-03-07T00:00:00Z"
    assert query.event_name == "CreateUser"
