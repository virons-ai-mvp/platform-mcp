# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for server.py."""

import pytest
from virons.infrastructure_mcp_server.server import create_server


def test_create_server():
    """Test server creation."""
    server = create_server()
    assert server is not None
    assert server.name == "virons.infrastructure-mcp-server"
