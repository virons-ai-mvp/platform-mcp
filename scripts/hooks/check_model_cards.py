#!/usr/bin/env python3
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""Pre-commit hook: Check EU AI Act model cards for high-risk servers."""

import sys
from pathlib import Path


HIGH_RISK_SERVERS = ["anomaly-detector", "grandmaster"]


def check_model_cards(server_path: Path) -> bool:
    """Check if high-risk server has model cards.
    
    Args:
        server_path: Path to server directory
        
    Returns:
        True if compliant, False otherwise
    """
    models_dir = server_path / "models"
    
    if not models_dir.exists():
        print(f"❌ {server_path.name}: Missing models/ directory")
        return False
    
    model_cards = list(models_dir.glob("*.md"))
    
    if not model_cards:
        print(f"❌ {server_path.name}: No model cards found in models/")
        print("   EU AI Act Art 11 requires technical documentation for high-risk AI")
        return False
    
    return True


def main() -> int:
    """Main entry point."""
    # Get all virons server directories
    src_dir = Path("src")
    
    if not src_dir.exists():
        return 0
    
    print("🔍 Checking EU AI Act model cards for high-risk servers...")
    
    failed = []
    for server_dir in src_dir.glob("virons-*-mcp-server"):
        # Check if it's a high-risk server
        is_high_risk = any(risk in server_dir.name for risk in HIGH_RISK_SERVERS)
        
        if is_high_risk:
            print(f"   Checking high-risk server: {server_dir.name}")
            if not check_model_cards(server_dir):
                failed.append(server_dir)
    
    if failed:
        print(f"\n❌ EU AI Act compliance check failed for {len(failed)} server(s)")
        print("High-risk AI systems require model cards per EU AI Act Art 11")
        return 1
    
    print("✓ EU AI Act model cards validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
