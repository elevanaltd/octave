"""Base MCP tool infrastructure.

Stub for P2.1: mcp_tool_base_implementation
"""


class BaseTool:
    """Base class for MCP tools."""

    def __init__(self, name: str, description: str):
        """Initialize base tool.

        Args:
            name: Tool name
            description: Tool description
        """
        raise NotImplementedError("P2.1: mcp_tool_base_implementation")

    def execute(self, **kwargs) -> dict:
        """Execute the tool.

        Args:
            **kwargs: Tool parameters

        Returns:
            Tool execution result
        """
        raise NotImplementedError("P2.1: mcp_tool_base_implementation")
