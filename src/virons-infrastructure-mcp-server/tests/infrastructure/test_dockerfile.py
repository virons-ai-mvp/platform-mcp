# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Dockerfile structure."""

from pathlib import Path

DOCKERFILE = Path(__file__).parent.parent.parent / "Dockerfile"


class TestDockerfile:
    """Test Dockerfile structure."""

    def test_dockerfile_exists(self):
        """Dockerfile must exist."""
        assert DOCKERFILE.exists(), "Dockerfile not found"

    def test_dockerfile_uses_multistage_build(self):
        """Dockerfile uses multi-stage build."""
        content = DOCKERFILE.read_text()

        assert "FROM python:3.13-slim AS builder" in content
        assert "FROM python:3.13-slim" in content

    def test_dockerfile_has_healthcheck(self):
        """Dockerfile has healthcheck."""
        content = DOCKERFILE.read_text()

        assert "HEALTHCHECK" in content
        assert "/health/live" in content

    def test_dockerfile_runs_as_nonroot(self):
        """Dockerfile runs as non-root user."""
        content = DOCKERFILE.read_text()

        assert "useradd" in content
        assert "USER virons" in content

    def test_dockerfile_exposes_port(self):
        """Dockerfile exposes port 8080."""
        content = DOCKERFILE.read_text()

        assert "EXPOSE 8080" in content
