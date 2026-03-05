# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Tests for compliance hooks."""

import pytest
from virons.infrastructure_mcp_server.compliance import (
    audit_write_operation,
)


@pytest.mark.asyncio
async def test_audit_write_operation():
    """Test audit write operation creates audit trail."""
    audit_id = await audit_write_operation(
        operation_name="test_operation",
        entity_id="test-entity-123",
        input_data={"param": "value"},
        output_data={"result": "success"},
    )
    assert audit_id
    assert len(audit_id) == 36  # UUID format

