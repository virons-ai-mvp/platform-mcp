#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""Pre-commit hook: Check Virons license headers."""

import sys
from pathlib import Path


REQUIRED_HEADER = """# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0"""


def check_license_header(filepath: Path) -> bool:
    """Check if file has correct Virons license header.
    
    Args:
        filepath: Path to Python file
        
    Returns:
        True if compliant, False otherwise
    """
    content = filepath.read_text()
    lines = content.split('\n')
    
    # Check first two non-empty lines
    header_lines = [line for line in lines[:5] if line.strip()][:2]
    
    if len(header_lines) < 2:
        return False
    
    if "Copyright Virons Fintech" not in header_lines[0]:
        print(f"❌ {filepath}: Missing Virons copyright header")
        return False
    
    if "SPDX-License-Identifier: Apache-2.0" not in header_lines[1]:
        print(f"❌ {filepath}: Missing SPDX license identifier")
        return False
    
    return True


def main() -> int:
    """Main entry point."""
    files = [Path(f) for f in sys.argv[1:]]
    
    if not files:
        return 0
    
    print("🔍 Checking Virons license headers...")
    
    failed = []
    for filepath in files:
        if not check_license_header(filepath):
            failed.append(filepath)
    
    if failed:
        print(f"\n❌ License header check failed for {len(failed)} file(s)")
        print("Add this header to the top of each file:")
        print(REQUIRED_HEADER)
        return 1
    
    print("✓ Virons license headers validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
