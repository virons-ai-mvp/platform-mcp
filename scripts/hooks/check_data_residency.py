#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""Pre-commit hook: Check GDPR Art 25 data residency enforcement."""

import sys
from pathlib import Path


def check_data_residency(filepath: Path) -> bool:
    """Check if compliance.py enforces eu-central-1 data residency.
    
    Args:
        filepath: Path to compliance.py file
        
    Returns:
        True if compliant, False otherwise
    """
    content = filepath.read_text()
    
    # Must import enforce_region
    if "from virons.common import" not in content or "enforce_region" not in content:
        print(f"❌ {filepath}: Missing enforce_region import")
        return False
    
    # Must call enforce_region with eu-central-1
    if 'enforce_region("eu-central-1")' not in content and "enforce_region('eu-central-1')" not in content:
        print(f"❌ {filepath}: Missing enforce_region('eu-central-1') call")
        return False
    
    return True


def main() -> int:
    """Main entry point."""
    files = [Path(f) for f in sys.argv[1:]]
    
    if not files:
        return 0
    
    print("🔍 Checking GDPR Art 25 data residency...")
    
    failed = []
    for filepath in files:
        if not check_data_residency(filepath):
            failed.append(filepath)
    
    if failed:
        print(f"\n❌ GDPR Art 25 compliance check failed for {len(failed)} file(s)")
        print("Ensure compliance.py calls enforce_region('eu-central-1')")
        return 1
    
    print("✓ GDPR Art 25 data residency validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
