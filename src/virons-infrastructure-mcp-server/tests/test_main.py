# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for main entry point."""

from unittest.mock import patch
from virons.infrastructure_mcp_server.server import create_server


def test_main_creates_server():
    """Test main function creates server."""
    server = create_server()
    assert server is not None
    assert server.name == "virons.infrastructure-mcp-server"

