#!/usr/bin/env python3
"""Sanity test random MCP tools."""

import asyncio
import random
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent / 'src/virons-infrastructure-mcp'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'src/virons-forensic-mcp'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'src/virons-compliance-mcp'))


async def test_infrastructure_list_iam_users():
    """Test list_iam_users from virons-infrastructure-mcp."""
    from server import list_iam_users

    try:
        result = await list_iam_users()
        print(f'✅ list_iam_users: {len(result.get("users", []))} users')
        return True
    except Exception as e:
        print(f'❌ list_iam_users: {e}')
        return False


async def test_compliance_check_gdpr():
    """Test check_gdpr_data_flow from virons-compliance-mcp."""
    from server import check_gdpr_data_flow

    try:
        result = await check_gdpr_data_flow(
            source='eu-central-1', destination='eu-west-1', data_type='personal'
        )
        print(f'✅ check_gdpr_data_flow: {result.get("compliant", False)}')
        return True
    except Exception as e:
        print(f'❌ check_gdpr_data_flow: {e}')
        return False


async def test_forensic_get_graph_status():
    """Test get_graph_status from virons-forensic-mcp."""
    from server import get_graph_status

    try:
        result = await get_graph_status()
        print(f'✅ get_graph_status: {result.get("status", "unknown")}')
        return True
    except Exception as e:
        print(f'❌ get_graph_status: {e}')
        return False


async def main():
    """Run tests."""
    tests = [
        test_infrastructure_list_iam_users,
        test_compliance_check_gdpr,
        test_forensic_get_graph_status,
    ]

    selected = random.sample(tests, 2)
    print(f'🎲 Running {len(selected)} random tests...\n')

    results = await asyncio.gather(*[t() for t in selected], return_exceptions=True)

    passed = sum(1 for r in results if r is True)
    print(f'\n📊 Results: {passed}/{len(selected)} passed')


if __name__ == '__main__':
    asyncio.run(main())
