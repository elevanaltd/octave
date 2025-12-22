"""Tests for MCP base tool infrastructure (P2.1).

Tests for BaseTool and SchemaBuilder following TDD discipline.
"""

import pytest
from mcp.types import Tool

from octave_mcp.mcp.base_tool import BaseTool, SchemaBuilder


class TestSchemaBuilder:
    """Test SchemaBuilder for JSON schema generation from tool parameters."""

    def test_create_string_parameter(self):
        """Test creating a basic string parameter."""
        schema = SchemaBuilder()
        schema.add_parameter("content", "string", required=True, description="Input content")

        result = schema.build()

        assert result["type"] == "object"
        assert "content" in result["properties"]
        assert result["properties"]["content"]["type"] == "string"
        assert result["properties"]["content"]["description"] == "Input content"
        assert "content" in result["required"]

    def test_create_boolean_parameter(self):
        """Test creating a boolean parameter."""
        schema = SchemaBuilder()
        schema.add_parameter("fix", "boolean", required=False, description="Apply repairs")

        result = schema.build()

        assert "fix" in result["properties"]
        assert result["properties"]["fix"]["type"] == "boolean"
        assert "fix" not in result.get("required", [])

    def test_create_enum_parameter(self):
        """Test creating an enum parameter."""
        schema = SchemaBuilder()
        schema.add_parameter(
            "mode",
            "string",
            required=True,
            description="Projection mode",
            enum=["canonical", "authoring", "executive", "developer"],
        )

        result = schema.build()

        assert "mode" in result["properties"]
        assert result["properties"]["mode"]["enum"] == ["canonical", "authoring", "executive", "developer"]

    def test_multiple_required_parameters(self):
        """Test creating multiple required parameters."""
        schema = SchemaBuilder()
        schema.add_parameter("content", "string", required=True, description="Content")
        schema.add_parameter("schema", "string", required=True, description="Schema name")
        schema.add_parameter("verbose", "boolean", required=False, description="Verbose output")

        result = schema.build()

        assert set(result["required"]) == {"content", "schema"}
        assert len(result["properties"]) == 3


class TestBaseTool:
    """Test BaseTool abstract class."""

    def test_base_tool_requires_implementation(self):
        """Test that BaseTool enforces abstract method implementation."""

        class IncompleteTool(BaseTool):
            """Tool missing required methods."""

            pass

        with pytest.raises(TypeError):
            IncompleteTool()

    def test_base_tool_with_implementation(self):
        """Test that BaseTool can be instantiated with all methods implemented."""

        class CompleteTool(BaseTool):
            """Minimal complete tool implementation."""

            def get_name(self) -> str:
                return "test.tool"

            def get_description(self) -> str:
                return "Test tool description"

            def get_input_schema(self) -> dict:
                schema = SchemaBuilder()
                schema.add_parameter("input", "string", required=True, description="Test input")
                return schema.build()

            async def execute(self, **kwargs) -> dict:
                return {"result": "success"}

        tool = CompleteTool()
        assert tool.get_name() == "test.tool"
        assert tool.get_description() == "Test tool description"

    def test_base_tool_to_mcp_tool(self):
        """Test converting BaseTool to MCP Tool object."""

        class TestTool(BaseTool):
            """Test tool for MCP conversion."""

            def get_name(self) -> str:
                return "octave.test"

            def get_description(self) -> str:
                return "Test tool for validation"

            def get_input_schema(self) -> dict:
                schema = SchemaBuilder()
                schema.add_parameter("param", "string", required=True, description="Test parameter")
                return schema.build()

            async def execute(self, **kwargs) -> dict:
                return {"status": "ok"}

        tool = TestTool()
        mcp_tool = tool.to_mcp_tool()

        assert isinstance(mcp_tool, Tool)
        assert mcp_tool.name == "octave.test"
        assert mcp_tool.description == "Test tool for validation"
        assert "param" in mcp_tool.inputSchema["properties"]

    def test_base_tool_parameter_validation(self):
        """Test that BaseTool validates parameters against schema."""

        class ValidationTool(BaseTool):
            """Tool with parameter validation."""

            def get_name(self) -> str:
                return "octave.validate"

            def get_description(self) -> str:
                return "Validation test tool"

            def get_input_schema(self) -> dict:
                schema = SchemaBuilder()
                schema.add_parameter("required_param", "string", required=True, description="Required")
                schema.add_parameter("optional_param", "boolean", required=False, description="Optional")
                return schema.build()

            async def execute(self, **kwargs) -> dict:
                return {"validated": True}

        tool = ValidationTool()

        # Valid parameters should pass
        valid_params = {"required_param": "value"}
        validated = tool.validate_parameters(valid_params)
        assert validated["required_param"] == "value"

        # Missing required parameter should raise error
        with pytest.raises(ValueError, match="required_param"):
            tool.validate_parameters({})
