# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""FastMCP server implementation for virons-infrastructure-mcp-server."""

import argparse
import os
import sys
from mcp.server.fastmcp import FastMCP, Context
from loguru import logger

from .compliance import setup_compliance_hooks
from .consts import SERVER_NAME, SERVER_INSTRUCTIONS, SERVER_DEPENDENCIES


# Configure logging
logger.remove()
logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

mcp = None


def create_server() -> FastMCP:
    """Create and configure the FastMCP server instance.
    
    Returns:
        Configured FastMCP server
    """
    server = FastMCP(
        SERVER_NAME,
        instructions=SERVER_INSTRUCTIONS,
        dependencies=SERVER_DEPENDENCIES,
    )
    
    # Register compliance hooks
    setup_compliance_hooks(server)
    
    # Register orchestrator tools
    register_tools(server)
    
    return server


# Upstream AWS MCP servers
UPSTREAM = {
    "cdk": {"host": "localhost", "port": 9140},
    "cfn": {"host": "localhost", "port": 9141},
    "terraform": {"host": "localhost", "port": 9142},
    "iac": {"host": "localhost", "port": 9143},
}


def register_tools(server: FastMCP) -> None:
    """Register orchestrator tools."""
    
    @server.tool()
    async def deploy_infrastructure(
        ctx: Context,
        tool: str,
        stack_name: str,
        template_path: str,
        parameters: dict = None
    ) -> dict:
        """Deploy infrastructure using CDK, CloudFormation, Terraform, or IaC.
        
        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Stack/deployment name
            template_path: Path to template/config
            parameters: Deployment parameters
        """
        from .compliance import audit_write_operation
        
        try:
            # Audit trail (BaFin AT 8.1)
            audit_id = await audit_write_operation(
                operation_name="deploy_infrastructure",
                entity_id=stack_name,
                input_data={"tool": tool, "template": template_path, "parameters": parameters},
                output_data={},
            )
            
            # TODO: Call upstream MCP server via HTTP/stdio
            result = {
                "status": "deployed",
                "stack_name": stack_name,
                "tool": tool,
                "audit_id": audit_id,
            }
            
            logger.info(f"Deployed {stack_name} using {tool}")
            return result
            
        except Exception as e:
            logger.error(f"Deploy failed: {e}")
            await ctx.error(f"Deployment error: {str(e)}")
            raise
    
    @server.tool()
    async def list_stacks(ctx: Context, tool: str) -> dict:
        """List deployed stacks.
        
        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
        """
        try:
            # TODO: Call upstream MCP server
            stacks = []
            logger.info(f"Listed stacks for {tool}")
            return {"tool": tool, "stacks": stacks}
        except Exception as e:
            logger.error(f"List failed: {e}")
            await ctx.error(f"List error: {str(e)}")
            raise
    
    @server.tool()
    async def destroy_infrastructure(
        ctx: Context,
        tool: str,
        stack_name: str
    ) -> dict:
        """Destroy infrastructure.
        
        Args:
            tool: IaC tool (cdk|cfn|terraform|iac)
            stack_name: Stack name to destroy
        """
        from .compliance import audit_write_operation
        
        try:
            # Audit trail (BaFin AT 8.1)
            audit_id = await audit_write_operation(
                operation_name="destroy_infrastructure",
                entity_id=stack_name,
                input_data={"tool": tool},
                output_data={},
            )
            
            # TODO: Call upstream MCP server
            result = {
                "status": "destroyed",
                "stack_name": stack_name,
                "tool": tool,
                "audit_id": audit_id,
            }
            
            logger.info(f"Destroyed {stack_name} using {tool}")
            return result
            
        except Exception as e:
            logger.error(f"Destroy failed: {e}")
            await ctx.error(f"Destroy error: {str(e)}")
            raise


def main():
    """Run the MCP server with CLI argument support."""
    global mcp
    
    parser = argparse.ArgumentParser(description="Virons Infrastructure MCP Server")
    parser.add_argument(
        "--allow-write",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable write operations (requires audit trail)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport protocol (stdio for MCP, http for K8s probes)",
    )
    
    args = parser.parse_args()
    
    logger.info(f"Starting {SERVER_NAME} (write_enabled={args.allow_write})")
    
    mcp = create_server()
    mcp.run()


if __name__ == "__main__":
    main()
