"""MCP server entry point (P2.4).

Provides the MCP server with octave_ingest and octave_eject tools.
"""

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from octave_mcp.mcp.amend import AmendTool
from octave_mcp.mcp.create import CreateTool
from octave_mcp.mcp.eject import EjectTool
from octave_mcp.mcp.ingest import IngestTool


def create_server() -> Server:
    """Create and configure the MCP server.

    Returns:
        Configured Server instance with tools registered
    """
    server = Server("octave-mcp")

    # Initialize tools
    ingest_tool = IngestTool()
    eject_tool = EjectTool()
    create_tool = CreateTool()
    amend_tool = AmendTool()

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name=ingest_tool.get_name(),
                description=ingest_tool.get_description(),
                inputSchema=ingest_tool.get_input_schema(),
            ),
            Tool(
                name=eject_tool.get_name(),
                description=eject_tool.get_description(),
                inputSchema=eject_tool.get_input_schema(),
            ),
            Tool(
                name=create_tool.get_name(),
                description=create_tool.get_description(),
                inputSchema=create_tool.get_input_schema(),
            ),
            Tool(
                name=amend_tool.get_name(),
                description=amend_tool.get_description(),
                inputSchema=amend_tool.get_input_schema(),
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        """Route tool calls to appropriate handler.

        Args:
            name: Tool name (octave_ingest or octave_eject)
            arguments: Tool arguments

        Returns:
            List of TextContent with results

        Raises:
            ValueError: If tool name is unknown
        """
        if arguments is None:
            arguments = {}

        # Route to appropriate tool
        if name == "octave_ingest":
            result = await ingest_tool.execute(**arguments)
        elif name == "octave_eject":
            result = await eject_tool.execute(**arguments)
        elif name == "octave_create":
            result = await create_tool.execute(**arguments)
        elif name == "octave_amend":
            result = await amend_tool.execute(**arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

        # Return result as TextContent
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return server


async def main():
    """Run the MCP server via stdio."""
    server = create_server()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def run():
    """Start the MCP server (entry point)."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
