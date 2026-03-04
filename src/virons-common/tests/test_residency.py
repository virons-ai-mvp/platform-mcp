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
"""Tests for the virons.common.residency module.

Validates GDPR Art 25 compliant data residency enforcement.
Reference: https://eur-lex.europa.eu/eli/reg/2016/679/oj
"""

import pytest


def test_enforce_region_allows_eu_central_1():
    from virons.common.residency import enforce_region

    enforce_region("eu-central-1")


def test_enforce_region_rejects_us_east_1():
    from virons.common.residency import enforce_region, DataResidencyError

    with pytest.raises(DataResidencyError, match="eu-central-1"):
        enforce_region("us-east-1")


def test_enforce_region_rejects_none():
    from virons.common.residency import enforce_region, DataResidencyError

    with pytest.raises(DataResidencyError, match="eu-central-1"):
        enforce_region(None)


def test_enforce_region_rejects_empty_string():
    from virons.common.residency import enforce_region, DataResidencyError

    with pytest.raises(DataResidencyError, match="eu-central-1"):
        enforce_region("")


def test_data_residency_error_is_exception():
    from virons.common.residency import DataResidencyError

    assert issubclass(DataResidencyError, Exception)
