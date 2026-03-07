# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Helm chart structure and values."""

from pathlib import Path

import yaml

HELM_DIR = Path(__file__).parent.parent.parent / "helm" / "virons-infrastructure"


class TestHelmChart:
    """Test Helm chart structure."""

    def test_chart_yaml_exists(self):
        """Chart.yaml must exist."""
        chart_file = HELM_DIR / "Chart.yaml"
        assert chart_file.exists(), "Chart.yaml not found"

    def test_chart_yaml_valid(self):
        """Chart.yaml must be valid YAML with required fields."""
        chart_file = HELM_DIR / "Chart.yaml"
        with open(chart_file) as f:
            chart = yaml.safe_load(f)

        assert chart["apiVersion"] == "v2"
        assert chart["name"] == "virons-infrastructure"
        assert chart["type"] == "application"
        assert "version" in chart

    def test_values_yaml_exists(self):
        """values.yaml must exist."""
        values_file = HELM_DIR / "values.yaml"
        assert values_file.exists(), "values.yaml not found"

    def test_values_yaml_has_upstream_config(self):
        """values.yaml must contain upstream server configuration."""
        values_file = HELM_DIR / "values.yaml"
        with open(values_file) as f:
            values = yaml.safe_load(f)

        assert "upstream" in values
        assert "cdk" in values["upstream"]
        assert "cfn" in values["upstream"]
        assert "terraform" in values["upstream"]
        assert "iac" in values["upstream"]

    def test_deployment_template_exists(self):
        """Deployment template must exist."""
        deployment = HELM_DIR / "templates" / "deployment.yaml"
        assert deployment.exists(), "deployment.yaml not found"

    def test_service_template_exists(self):
        """Service template must exist."""
        service = HELM_DIR / "templates" / "service.yaml"
        assert service.exists(), "service.yaml not found"

    def test_deployment_has_health_probes(self):
        """Deployment must have liveness and readiness probes."""
        deployment = HELM_DIR / "templates" / "deployment.yaml"
        with open(deployment) as f:
            content = f.read()

        assert "livenessProbe" in content
        assert "readinessProbe" in content
        assert "/health/live" in content
        assert "/health/ready" in content
