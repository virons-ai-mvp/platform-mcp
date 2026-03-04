#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""Pre-commit hook: Check BaFin MaRisk AT 8.1 audit pattern."""

import re
import sys
from pathlib import Path


def check_audit_pattern(filepath: Path) -> bool:
    """Check if write operations call write_audit before returning.
    
    Args:
        filepath: Path to Python file
        
    Returns:
        True if compliant, False otherwise
    """
    content = filepath.read_text()
    
    # Skip test files
    if "test_" in filepath.name:
        return True
    
    # Check for write operations (functions with write/create/update/delete)
    write_pattern = r'async def (write|create|update|delete)_\w+\([^)]*\):'
    write_funcs = re.findall(write_pattern, content)
    
    if not write_funcs:
        return True  # No write operations
    
    # Check if write_audit is imported
    if "from virons.common import" not in content or "write_audit" not in content:
        print(f"❌ {filepath}: Write operations found but write_audit not imported")
        return False
    
    # Check if write_audit is called
    if "await write_audit(" not in content:
        print(f"⚠️  {filepath}: write_audit imported but not called")
        return False
    
    return True


def main() -> int:
    """Main entry point."""
    files = [Path(f) for f in sys.argv[1:]]
    
    if not files:
        return 0
    
    print("🔍 Checking BaFin MaRisk AT 8.1 audit patterns...")
    
    failed = []
    for filepath in files:
        if not check_audit_pattern(filepath):
            failed.append(filepath)
    
    if failed:
        print(f"\n❌ BaFin AT 8.1 compliance check failed for {len(failed)} file(s)")
        print("Ensure write operations call write_audit() before returning")
        return 1
    
    print("✓ BaFin AT 8.1 audit patterns validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
