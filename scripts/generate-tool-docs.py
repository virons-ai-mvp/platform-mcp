#!/usr/bin/env python3
"""Generate comprehensive tool documentation from gateway API."""

import json
import requests
import sys


def format_param_type(prop):
    """Format parameter type from schema."""
    ptype = prop.get('type', 'any')
    if ptype == 'object':
        return 'dict'
    if ptype == 'array':
        items = prop.get('items', {})
        item_type = items.get('type', 'any')
        return f'list[{item_type}]'
    return ptype


def generate_tool_doc(tool):
    """Generate formatted documentation for a tool."""
    name = tool['name']
    desc = tool['description'].split('\n')[0]  # First line only

    # Build Args section from input_schema
    schema = tool.get('input_schema', {})
    props = schema.get('properties', {})
    required = schema.get('required', [])

    args_lines = []
    for param_name, param_info in props.items():
        param_type = format_param_type(param_info)
        is_required = param_name in required
        req_marker = '' if is_required else ' (optional)'

        # Try to extract description from existing description field
        default = param_info.get('default')
        default_str = f', default: {default}' if default is not None else ''

        args_lines.append(f'    {param_name}: {param_type}{req_marker}{default_str}')

    # Format output
    doc = f'{name} - {desc}\n'
    if args_lines:
        doc += '\nArgs:\n' + '\n'.join(args_lines) + '\n'

    # Add examples if available
    examples = tool.get('examples', [])
    if examples:
        doc += '\nExamples:\n'
        for ex in examples[:2]:  # Limit to 2 examples
            ex_desc = ex.get('description', '')
            doc += f'    - {ex_desc}\n'

    return doc


def main():
    """Generate tool documentation from gateway API."""
    gateway_url = 'http://localhost:9000/tools'

    try:
        response = requests.get(gateway_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        tools = data.get('tools', [])

        print('# Virons MCP Gateway - Tool Documentation\n')
        print(f'Total tools: {len(tools)}\n')
        print('=' * 80 + '\n')

        for tool in tools:
            print(generate_tool_doc(tool))
            print()

    except requests.RequestException as e:
        print(f'Error connecting to gateway: {e}', file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f'Error parsing JSON response: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
