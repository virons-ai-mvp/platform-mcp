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
"""Tests for the virons.common.correlation module.

Validates GDPR Art 32 compliant correlation ID threading.
Reference: https://eur-lex.europa.eu/eli/reg/2016/679/oj
"""

import uuid
import pytest


def test_generate_correlation_id_returns_valid_uuid():
    from virons.common.correlation import generate_correlation_id

    corr_id = generate_correlation_id()
    assert isinstance(corr_id, str)
    parsed = uuid.UUID(corr_id)
    assert parsed.version == 4


def test_correlation_context_get_returns_none_initially():
    from virons.common.correlation import CorrelationContext

    ctx = CorrelationContext()
    assert ctx.get() is None


def test_correlation_context_set_and_get():
    from virons.common.correlation import CorrelationContext

    ctx = CorrelationContext()
    test_id = "test-correlation-id"
    ctx.set(test_id)
    assert ctx.get() == test_id


def test_correlation_context_propagates_across_calls():
    from virons.common.correlation import CorrelationContext

    ctx = CorrelationContext()
    test_id = "propagation-test"
    ctx.set(test_id)

    def nested_function():
        return ctx.get()

    assert nested_function() == test_id


def test_correlation_context_reset():
    from virons.common.correlation import CorrelationContext

    ctx = CorrelationContext()
    ctx.set("test-id")
    ctx.reset()
    assert ctx.get() is None
