"""Tests for upstream proxy."""
import pytest
from virons.common.upstream_proxy import UpstreamProxy


@pytest.fixture
def proxy():
    """Create proxy instance."""
    config = {
        "service1": {"host": "localhost", "port": 9100},
        "service2": {"host": "localhost", "port": 9200}
    }
    return UpstreamProxy(config)


def test_proxy_initialization(proxy):
    """Test proxy initializes with config."""
    assert len(proxy.upstreams) == 2
    assert "service1" in proxy.upstreams


def test_get_upstream_for_tool(proxy):
    """Test getting upstream for a tool."""
    proxy._tool_cache["test_tool"] = "service1"
    
    upstream = proxy.get_upstream_for_tool("test_tool")
    assert upstream == "service1"


def test_get_upstream_for_unknown_tool(proxy):
    """Test getting upstream for unknown tool returns None."""
    upstream = proxy.get_upstream_for_tool("unknown")
    assert upstream is None


@pytest.mark.asyncio
async def test_call_unknown_tool_raises_error(proxy):
    """Test calling unknown tool raises ValueError."""
    with pytest.raises(ValueError, match="Unknown tool"):
        await proxy.call_tool("unknown_tool", {})

