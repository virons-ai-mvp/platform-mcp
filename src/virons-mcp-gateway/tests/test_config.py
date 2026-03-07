# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for config loader."""

import json
import os
from tempfile import NamedTemporaryFile

import pytest

from virons.mcp_gateway.infrastructure.config import (
    GatewayConfig,
    _substitute_env_vars,
    load_config,
)


class TestConfigLoader:
    """Test config loader functionality."""

    def test_substitute_env_vars_with_default(self):
        """Test env var substitution uses default when var not set."""
        result = _substitute_env_vars("${MISSING_VAR:http://localhost:9100}")
        assert result == "http://localhost:9100"

    def test_substitute_env_vars_with_env_value(self):
        """Test env var substitution uses env value when set."""
        os.environ["TEST_VAR"] = "http://custom:8080"
        result = _substitute_env_vars("${TEST_VAR:http://localhost:9100}")
        assert result == "http://custom:8080"
        del os.environ["TEST_VAR"]

    def test_substitute_env_vars_multiple(self):
        """Test multiple env var substitutions."""
        os.environ["HOST"] = "example.com"
        os.environ["PORT"] = "9999"
        result = _substitute_env_vars("http://${HOST:localhost}:${PORT:8080}/api")
        assert result == "http://example.com:9999/api"
        del os.environ["HOST"]
        del os.environ["PORT"]

    def test_load_config_success(self):
        """Test loading valid config file."""
        config_data = {
            "services": [
                {
                    "name": "infrastructure-mcp",
                    "url": "${INFRA_URL:http://localhost:9100}",
                    "tools": ["terraform_validate", "kubectl_apply"],
                },
                {
                    "name": "security-mcp",
                    "url": "http://localhost:9500",
                    "tools": ["scan_security"],
                },
            ]
        }

        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name

        try:
            config = load_config(config_path)
            assert isinstance(config, GatewayConfig)
            assert len(config.services) == 2
            assert config.services[0].name == "infrastructure-mcp"
            assert config.services[0].url == "http://localhost:9100"
            assert len(config.services[0].tools) == 2
        finally:
            os.unlink(config_path)

    def test_load_config_with_env_override(self):
        """Test loading config with env var override."""
        config_data = {
            "services": [
                {
                    "name": "test-service",
                    "url": "${TEST_SERVICE_URL:http://localhost:9000}",
                    "tools": ["test_tool"],
                }
            ]
        }

        os.environ["TEST_SERVICE_URL"] = "http://production:8080"

        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name

        try:
            config = load_config(config_path)
            assert config.services[0].url == "http://production:8080"
        finally:
            os.unlink(config_path)
            del os.environ["TEST_SERVICE_URL"]

    def test_load_config_file_not_found(self):
        """Test loading non-existent config file raises error."""
        with pytest.raises(FileNotFoundError, match="Config file not found"):
            load_config("/nonexistent/config.json")

    def test_load_config_empty_services(self):
        """Test loading config with empty services list."""
        config_data = {"services": []}

        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name

        try:
            config = load_config(config_path)
            assert len(config.services) == 0
        finally:
            os.unlink(config_path)
