# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for package initialization."""

import re
from importlib import reload
import virons.monitoring_mcp_server


def test_version():
    """Test version is valid semver."""
    version = virons.monitoring_mcp_server.__version__
    assert re.match(r"^\d+\.\d+\.\d+", version)


def test_module_reload():
    """Test module can be reloaded."""
    reload(virons.monitoring_mcp_server)
    assert virons.monitoring_mcp_server.__version__
