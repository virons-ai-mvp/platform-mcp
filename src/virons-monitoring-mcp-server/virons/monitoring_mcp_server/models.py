# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Pydantic models for virons-monitoring-mcp-server."""

from typing import List, Optional

from pydantic import BaseModel, Field


class MetricQuery(BaseModel):
    """Metric query request."""

    metric_name: str = Field(..., description="Metric name")
    start_time: str = Field(..., description="Start time (ISO 8601)")
    end_time: str = Field(..., description="End time (ISO 8601)")
    dimensions: Optional[dict] = Field(None, description="Metric dimensions")


class MetricData(BaseModel):
    """Metric data point."""

    timestamp: str = Field(..., description="Timestamp")
    value: float = Field(..., description="Metric value")
    unit: str = Field(..., description="Unit")


class AlertRule(BaseModel):
    """Alert rule configuration."""

    name: str = Field(..., description="Alert name")
    metric: str = Field(..., description="Metric to monitor")
    threshold: float = Field(..., description="Alert threshold")
    comparison: str = Field(..., description="Comparison operator (gt|lt|eq)")
    audit_id: str = Field(..., description="BaFin AT 8.1 audit trail ID")


class DashboardConfig(BaseModel):
    """Dashboard configuration."""

    name: str = Field(..., description="Dashboard name")
    panels: List[dict] = Field(default_factory=list, description="Dashboard panels")
    audit_id: str = Field(..., description="BaFin AT 8.1 audit trail ID")
