"""Tests for LogEntry domain entities - TDD."""
import pytest
from datetime import datetime
from virons.monitoring_mcp_server.domain.log_entry import LogEntry, LogQuery


def test_log_entry_creation():
    """Test log entry entity creation."""
    log = LogEntry(
        timestamp=datetime.now(),
        message="Application started",
        level="INFO",
        source="elasticsearch",
        labels={"app": "api"}
    )
    
    assert log.message == "Application started"
    assert log.level == "INFO"
    assert log.source == "elasticsearch"


def test_log_entry_requires_message():
    """Test log entry validation - message required."""
    with pytest.raises(ValueError, match="Log message required"):
        LogEntry(
            timestamp=datetime.now(),
            message="",
            level="INFO",
            source="elasticsearch",
            labels={}
        )


def test_log_entry_validates_level():
    """Test log entry validates level."""
    with pytest.raises(ValueError, match="Invalid log level"):
        LogEntry(
            timestamp=datetime.now(),
            message="Test",
            level="INVALID",
            source="elasticsearch",
            labels={}
        )


def test_log_query_creation():
    """Test log query value object."""
    query = LogQuery(
        query="error",
        start_time="2026-03-07T00:00:00Z",
        end_time="2026-03-07T01:00:00Z",
        source="elasticsearch"
    )
    
    assert query.query == "error"
    assert query.source == "elasticsearch"
    assert query.size == 100


def test_log_query_requires_query():
    """Test log query validation - query required."""
    with pytest.raises(ValueError, match="Query required"):
        LogQuery(
            query="",
            start_time="2026-03-07T00:00:00Z",
            end_time="2026-03-07T01:00:00Z"
        )


def test_log_query_validates_source():
    """Test log query validates source."""
    with pytest.raises(ValueError, match="Invalid source"):
        LogQuery(
            query="error",
            start_time="2026-03-07T00:00:00Z",
            end_time="2026-03-07T01:00:00Z",
            source="invalid"
        )


def test_log_query_validates_size():
    """Test log query validates size."""
    with pytest.raises(ValueError, match="Size must be between"):
        LogQuery(
            query="error",
            start_time="2026-03-07T00:00:00Z",
            end_time="2026-03-07T01:00:00Z",
            size=20000
        )
