#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""Pre-commit hook: Run tests for virons servers."""

import subprocess
import sys
from pathlib import Path


def run_tests() -> int:
    """Run pytest for all virons servers.
    
    Returns:
        0 if all tests pass, 1 otherwise
    """
    src_dir = Path("src")
    
    if not src_dir.exists():
        return 0
    
    print("🧪 Running tests for virons servers...")
    
    failed = []
    for server_dir in src_dir.glob("virons-*"):
        if not (server_dir / "pyproject.toml").exists():
            continue
        
        print(f"\n   Testing {server_dir.name}...")
        
        result = subprocess.run(
            ["uv", "run", "pytest", "-q"],
            cwd=server_dir,
            capture_output=True,
            text=True,
        )
        
        if result.returncode != 0:
            print(f"   ❌ Tests failed for {server_dir.name}")
            print(result.stdout)
            failed.append(server_dir.name)
        else:
            print(f"   ✓ Tests passed for {server_dir.name}")
    
    if failed:
        print(f"\n❌ Tests failed for {len(failed)} server(s): {', '.join(failed)}")
        return 1
    
    print("\n✓ All virons server tests passed")
    return 0


def main() -> int:
    """Main entry point."""
    return run_tests()


if __name__ == "__main__":
    sys.exit(main())
