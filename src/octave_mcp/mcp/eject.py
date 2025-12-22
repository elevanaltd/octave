"""MCP tool for OCTAVE eject (P2.3).

Implements octave.eject tool with projection modes:
- canonical: Full document, lossy=false
- authoring: Lenient format, lossy=false
- executive: STATUS,RISKS,DECISIONS only, lossy=true
- developer: TESTS,CI,DEPS only, lossy=true
"""

from typing import Any

from octave_mcp.core.parser import parse
from octave_mcp.core.projector import project
from octave_mcp.mcp.base_tool import BaseTool, SchemaBuilder


class EjectTool(BaseTool):
    """MCP tool for octave.eject - projection and formatting."""

    def get_name(self) -> str:
        """Get tool name."""
        return "octave.eject"

    def get_description(self) -> str:
        """Get tool description."""
        return (
            "Eject OCTAVE content with projection modes. "
            "Supports canonical, authoring, executive, and developer views. "
            "Can generate templates when content is null. "
            "Output formats: octave, json, yaml, markdown."
        )

    def get_input_schema(self) -> dict[str, Any]:
        """Get input schema."""
        schema = SchemaBuilder()

        schema.add_parameter(
            "content", "string", required=False, description="OCTAVE content to eject (null for template generation)"
        )

        schema.add_parameter(
            "schema", "string", required=True, description="Schema name for validation or template generation"
        )

        schema.add_parameter(
            "mode",
            "string",
            required=False,
            description="Projection mode: canonical (full), authoring (lenient), executive (STATUS,RISKS,DECISIONS), developer (TESTS,CI,DEPS)",
            enum=["canonical", "authoring", "executive", "developer"],
        )

        schema.add_parameter(
            "format", "string", required=False, description="Output format", enum=["octave", "json", "yaml", "markdown"]
        )

        return schema.build()

    async def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute eject projection.

        Args:
            content: OCTAVE content to eject (None for template)
            schema: Schema name for validation/template
            mode: Projection mode (canonical, authoring, executive, developer)
            format: Output format (octave, json, yaml, markdown)

        Returns:
            Dictionary with:
            - output: Formatted content
            - lossy: Boolean (true if mode discards fields)
            - fields_omitted: List of dropped fields if lossy
        """
        # Validate and extract parameters
        params = self.validate_parameters(kwargs)
        content = params.get("content", None)
        schema_name = params["schema"]
        mode = params.get("mode", "canonical")
        output_format = params.get("format", "octave")

        # If content is None, generate template
        if content is None:
            # For now, generate minimal template
            template = f"""===TEMPLATE===
META:
  TYPE::{schema_name}
  VERSION::"1.0"

# Template generated for schema: {schema_name}
===END==="""
            return {"output": template, "lossy": False, "fields_omitted": []}

        # Parse content to AST
        try:
            doc = parse(content)
        except Exception as e:
            # If parsing fails, return error
            return {"output": f"# Parse error: {str(e)}\n{content}", "lossy": False, "fields_omitted": []}

        # Project to desired mode
        result = project(doc, mode=mode)

        # For now, only OCTAVE format is implemented
        # JSON, YAML, markdown are deferred to future work
        if output_format != "octave":
            # Return canonical OCTAVE with note
            output = f"# Format '{output_format}' not yet implemented - returning OCTAVE\n{result.output}"
            return {"output": output, "lossy": result.lossy, "fields_omitted": result.fields_omitted}

        return {"output": result.output, "lossy": result.lossy, "fields_omitted": result.fields_omitted}
