# Copyright Virons Fintech. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ruff: noqa: D101, D102, D103
"""Tests for the virons.common.audit module.

Validates BaFin MaRisk AT 8.1 compliant audit logging.
Reference: https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Rundschreiben/2017/rs_1709_marisk_ba.html
"""

import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_write_audit_returns_audit_id():
    from virons.common.audit import write_audit

    audit_id = await write_audit(
        service_name='test-service',
        calculation_type='beneish',
        entity_id='entity-001',
        input_data={'score': 1.0},
        output_data={'flag': True},
    )
    assert isinstance(audit_id, str)
    assert len(audit_id) > 0
    assert 'test-service' in audit_id
    assert 'entity-001' in audit_id


@pytest.mark.asyncio
async def test_write_audit_logs_structured_data():
    from virons.common.audit import write_audit

    with patch('virons.common.audit.logger') as mock_logger:
        await write_audit(
            service_name='forensic',
            calculation_type='altman',
            entity_id='entity-002',
            input_data={'x': 1},
            output_data={'y': 2},
        )
        mock_logger.info.assert_called_once()
        call_kwargs = mock_logger.info.call_args[1]
        assert call_kwargs['service'] == 'forensic'
        assert call_kwargs['calculation_type'] == 'altman'
        assert call_kwargs['entity_id'] == 'entity-002'
        assert 'audit_id' in call_kwargs
        assert 'timestamp' in call_kwargs


@pytest.mark.asyncio
async def test_write_audit_requires_fields():
    from virons.common.audit import write_audit

    with pytest.raises(TypeError):
        await write_audit()

    with pytest.raises(TypeError):
        await write_audit(service_name='x')


@pytest.mark.asyncio
async def test_write_audit_accepts_optional_metadata():
    from virons.common.audit import write_audit

    audit_id = await write_audit(
        service_name='test',
        calculation_type='test',
        entity_id='e1',
        input_data={},
        output_data={},
        metadata={'correlation_id': 'abc-123'},
    )
    assert isinstance(audit_id, str)


@pytest.mark.asyncio
async def test_write_audit_metadata_defaults_to_none():
    from virons.common.audit import write_audit

    with patch('virons.common.audit.logger') as mock_logger:
        await write_audit(
            service_name='s',
            calculation_type='c',
            entity_id='e',
            input_data={},
            output_data={},
        )
        call_kwargs = mock_logger.info.call_args[1]
        assert call_kwargs['metadata'] == {}
