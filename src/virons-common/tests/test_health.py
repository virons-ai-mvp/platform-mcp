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
"""Tests for the virons.common.health module.

Validates DORA Art 11 compliant health monitoring.
Reference: https://eur-lex.europa.eu/eli/reg/2022/2554/oj
"""

import pytest


def test_liveness_returns_ok():
    from virons.common.health import HealthCheck

    hc = HealthCheck()
    result = hc.liveness()
    assert result == {"status": "ok"}


def test_readiness_returns_ok_when_no_checks():
    from virons.common.health import HealthCheck

    hc = HealthCheck()
    result = hc.readiness()
    assert result == {"status": "ok", "checks": {}}


def test_readiness_fails_when_check_fails():
    from virons.common.health import HealthCheck

    hc = HealthCheck()
    hc.add_readiness_check("db", lambda: False)
    result = hc.readiness()
    assert result["status"] == "degraded"
    assert result["checks"]["db"] is False


def test_add_readiness_check_works():
    from virons.common.health import HealthCheck

    hc = HealthCheck()
    hc.add_readiness_check("cache", lambda: True)
    result = hc.readiness()
    assert result["status"] == "ok"
    assert result["checks"]["cache"] is True


def test_readiness_all_checks_pass():
    from virons.common.health import HealthCheck

    hc = HealthCheck()
    hc.add_readiness_check("db", lambda: True)
    hc.add_readiness_check("cache", lambda: True)
    result = hc.readiness()
    assert result["status"] == "ok"
    assert result["checks"]["db"] is True
    assert result["checks"]["cache"] is True
