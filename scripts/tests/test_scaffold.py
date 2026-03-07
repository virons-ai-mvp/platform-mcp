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
"""Tests for scaffold_virons_server.py script."""

import pytest
import subprocess
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).parent.parent / 'scaffold_virons_server.py'
TEST_OUTPUT_DIR = Path(__file__).parent / 'test_output'


@pytest.fixture(autouse=True)
def cleanup_test_output():
    """Clean up test output directory before and after each test."""
    import shutil

    if TEST_OUTPUT_DIR.exists():
        shutil.rmtree(TEST_OUTPUT_DIR)
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)
    yield
    if TEST_OUTPUT_DIR.exists():
        shutil.rmtree(TEST_OUTPUT_DIR)


def test_valid_args_parse():
    """Test that valid arguments are accepted."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            '--name',
            'test',
            '--description',
            'Test server',
            '--port',
            '9500',
            '--output-dir',
            str(TEST_OUTPUT_DIR),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert 'Scaffold Complete' in result.stdout
    assert 'virons-test-mcp-server' in result.stdout
    assert 'Compliance Baseline' in result.stdout


def test_missing_required_args_fail():
    """Test that missing required arguments cause failure."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert 'required' in result.stderr.lower()


def test_directory_tree_matches_expected():
    """Test that generated directory structure matches expected layout."""
    subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            '--name',
            'infrastructure',
            '--description',
            'Infrastructure MCP server',
            '--port',
            '9300',
            '--output-dir',
            str(TEST_OUTPUT_DIR),
        ],
        check=True,
    )

    server_dir = TEST_OUTPUT_DIR / 'virons-infrastructure-mcp-server'

    # Check main structure
    assert server_dir.exists()
    assert (server_dir / 'virons').exists()
    assert (server_dir / 'virons' / 'infrastructure_mcp_server').exists()
    assert (server_dir / 'tests').exists()

    # Check Python source files
    assert (server_dir / 'virons' / 'infrastructure_mcp_server' / 'server.py').exists()
    assert (server_dir / 'virons' / 'infrastructure_mcp_server' / 'models.py').exists()
    assert (server_dir / 'virons' / 'infrastructure_mcp_server' / 'consts.py').exists()
    assert (server_dir / 'virons' / 'infrastructure_mcp_server' / 'compliance.py').exists()
    assert (server_dir / 'virons' / 'infrastructure_mcp_server' / '__init__.py').exists()

    # Check test files
    assert (server_dir / 'tests' / 'test_server.py').exists()
    assert (server_dir / 'tests' / 'test_init.py').exists()
    assert (server_dir / 'tests' / 'test_main.py').exists()
    assert (server_dir / 'tests' / 'test_compliance.py').exists()

    # Check metadata files
    assert (server_dir / 'pyproject.toml').exists()
    assert (server_dir / 'README.md').exists()
    assert (server_dir / 'LICENSE').exists()
    assert (server_dir / 'NOTICE').exists()
    assert (server_dir / 'CHANGELOG.md').exists()
    assert (server_dir / 'COMPLIANCE.md').exists()
    assert (server_dir / '.gitignore').exists()
    assert (server_dir / '.python-version').exists()

    # Check DDD README files
    assert (server_dir / 'virons' / 'README.md').exists()
    assert (server_dir / 'virons' / 'infrastructure_mcp_server' / 'README.md').exists()
    assert (server_dir / 'tests' / 'README.md').exists()

    # Check Docker files
    assert (server_dir / 'Dockerfile').exists()
    assert (server_dir / 'docker-healthcheck.sh').exists()
    assert (server_dir / '.dockerignore').exists()

    # Verify healthcheck is executable
    import os

    assert os.access(server_dir / 'docker-healthcheck.sh', os.X_OK)


def test_idempotency_refuses_overwrite():
    """Test that scaffold refuses to overwrite existing directory."""
    # First run - should succeed
    result1 = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            '--name',
            'test',
            '--description',
            'Test',
            '--port',
            '9500',
            '--output-dir',
            str(TEST_OUTPUT_DIR),
        ],
        capture_output=True,
        text=True,
    )
    assert result1.returncode == 0

    # Second run - should fail
    result2 = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            '--name',
            'test',
            '--description',
            'Test',
            '--port',
            '9500',
            '--output-dir',
            str(TEST_OUTPUT_DIR),
        ],
        capture_output=True,
        text=True,
    )
    assert result2.returncode == 1
    assert 'already exists' in result2.stderr.lower()


def test_custom_deps_accepted():
    """Test that custom dependencies are accepted."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            '--name',
            'test',
            '--description',
            'Test',
            '--port',
            '9500',
            '--deps',
            'boto3,requests',
            '--output-dir',
            str(TEST_OUTPUT_DIR),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    pyproject = TEST_OUTPUT_DIR / 'virons-test-mcp-server' / 'pyproject.toml'
    content = pyproject.read_text()
    assert 'boto3' in content
    assert 'requests' in content


def test_transport_flag_accepted():
    """Test that --transport flag is accepted."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            '--name',
            'test',
            '--description',
            'Test',
            '--port',
            '9500',
            '--transport',
            'http',
            '--output-dir',
            str(TEST_OUTPUT_DIR),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
