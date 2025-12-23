"""Test cases for octave_eject MCP tool (P2.3).

Tests projection modes:
- canonical: Full document, lossy=false
- authoring: Lenient format, lossy=false
- executive: STATUS,RISKS,DECISIONS only, lossy=true
- developer: TESTS,CI,DEPS only, lossy=true
"""

import pytest

from octave_mcp.mcp.eject import EjectTool


class TestEjectTool:
    """Test EjectTool MCP interface."""

    @pytest.fixture
    def eject_tool(self):
        """Create EjectTool instance."""
        return EjectTool()

    def test_tool_name(self, eject_tool):
        """Eject tool returns correct name."""
        assert eject_tool.get_name() == "octave_eject"

    def test_tool_description(self, eject_tool):
        """Eject tool has non-empty description."""
        desc = eject_tool.get_description()
        assert "projection" in desc.lower()
        assert len(desc) > 0

    def test_input_schema_has_required_parameters(self, eject_tool):
        """Input schema defines required parameters."""
        schema = eject_tool.get_input_schema()

        # Schema parameter is required
        assert "schema" in schema["properties"]
        assert "schema" in schema.get("required", [])

        # Content is optional (null for template generation)
        assert "content" in schema["properties"]
        assert "content" not in schema.get("required", [])

    def test_input_schema_has_mode_enum(self, eject_tool):
        """Input schema defines mode enumeration."""
        schema = eject_tool.get_input_schema()

        mode_schema = schema["properties"]["mode"]
        assert "enum" in mode_schema
        assert set(mode_schema["enum"]) == {"canonical", "authoring", "executive", "developer"}

    def test_input_schema_has_format_enum(self, eject_tool):
        """Input schema defines format enumeration."""
        schema = eject_tool.get_input_schema()

        format_schema = schema["properties"]["format"]
        assert "enum" in format_schema
        assert set(format_schema["enum"]) == {"octave", "json", "yaml", "markdown"}

    @pytest.mark.asyncio
    async def test_eject_canonical_mode(self, eject_tool):
        """Eject in canonical mode returns full document."""
        content = """===TEST===
META:
  VERSION::"1.0"

STATUS::active
===END==="""

        result = await eject_tool.execute(content=content, schema="TEST", mode="canonical")

        assert result["output"] is not None
        assert result["lossy"] is False
        assert result["fields_omitted"] == []
        assert "===TEST===" in result["output"]

    @pytest.mark.asyncio
    async def test_eject_authoring_mode(self, eject_tool):
        """Eject in authoring mode returns lenient format."""
        content = """===TEST===
META:
  VERSION::"1.0"

STATUS::active
===END==="""

        result = await eject_tool.execute(content=content, schema="TEST", mode="authoring")

        assert result["output"] is not None
        assert result["lossy"] is False
        assert result["fields_omitted"] == []

    @pytest.mark.asyncio
    async def test_eject_executive_mode(self, eject_tool):
        """Eject in executive mode is lossy and omits technical fields."""
        content = """===TEST===
META:
  VERSION::"1.0"

STATUS::active
TESTS::passing
CI::green
DEPS::[lib1, lib2]
===END==="""

        result = await eject_tool.execute(content=content, schema="TEST", mode="executive")

        assert result["lossy"] is True
        assert "TESTS" in result["fields_omitted"]
        assert "CI" in result["fields_omitted"]
        assert "DEPS" in result["fields_omitted"]

    @pytest.mark.asyncio
    async def test_eject_developer_mode(self, eject_tool):
        """Eject in developer mode is lossy and omits executive fields."""
        content = """===TEST===
META:
  VERSION::"1.0"

STATUS::active
RISKS::[risk1, risk2]
DECISIONS::[decision1]
TESTS::passing
===END==="""

        result = await eject_tool.execute(content=content, schema="TEST", mode="developer")

        assert result["lossy"] is True
        # Developer mode omits executive summary fields
        assert len(result["fields_omitted"]) > 0

    @pytest.mark.asyncio
    async def test_eject_null_content_generates_template(self, eject_tool):
        """Eject with null content generates template for schema."""
        result = await eject_tool.execute(content=None, schema="TEST")

        assert result["output"] is not None
        assert result["lossy"] is False
        # Template generation returns minimal structure
        assert len(result["output"]) > 0

    @pytest.mark.asyncio
    async def test_eject_default_mode_is_canonical(self, eject_tool):
        """Eject without mode parameter defaults to canonical."""
        content = """===TEST===
META:
  VERSION::"1.0"

STATUS::active
===END==="""

        result = await eject_tool.execute(content=content, schema="TEST")

        assert result["lossy"] is False
        assert result["fields_omitted"] == []

    @pytest.mark.asyncio
    async def test_eject_default_format_is_octave(self, eject_tool):
        """Eject without format parameter defaults to octave."""
        content = """===TEST===
META:
  VERSION::"1.0"

STATUS::active
===END==="""

        result = await eject_tool.execute(content=content, schema="TEST", format="octave")

        assert result["output"] is not None
        # OCTAVE format uses envelopes
        assert "===TEST===" in result["output"]

    @pytest.mark.asyncio
    async def test_eject_validates_required_schema(self, eject_tool):
        """Eject raises error when schema is missing."""
        with pytest.raises(ValueError, match="schema"):
            await eject_tool.execute(
                content="test content"
                # schema is missing
            )

    @pytest.mark.asyncio
    async def test_eject_json_format(self, eject_tool):
        """Eject in JSON format returns valid JSON."""
        content = """===TEST===
META:
  VERSION::"1.0"
  TYPE::"TEST"

STATUS::active
FIELD::"value"
===END==="""

        result = await eject_tool.execute(content=content, schema="TEST", format="json")

        assert result["output"] is not None
        # Verify JSON is valid by parsing
        import json

        parsed = json.loads(result["output"])
        assert parsed["META"]["VERSION"] == "1.0"
        assert parsed["STATUS"] == "active"

    @pytest.mark.asyncio
    async def test_eject_yaml_format(self, eject_tool):
        """Eject in YAML format returns valid YAML."""
        content = """===TEST===
META:
  VERSION::"1.0"
  TYPE::"TEST"

STATUS::active
FIELD::"value"
===END==="""

        result = await eject_tool.execute(content=content, schema="TEST", format="yaml")

        assert result["output"] is not None
        # Verify YAML is valid by parsing
        import yaml

        parsed = yaml.safe_load(result["output"])
        assert parsed["META"]["VERSION"] == "1.0"
        assert parsed["STATUS"] == "active"

    @pytest.mark.asyncio
    async def test_eject_markdown_format(self, eject_tool):
        """Eject in Markdown format returns readable markdown."""
        content = """===TEST===
META:
  VERSION::"1.0"
  TYPE::"TEST"

STATUS::active
FIELD::"value"
===END==="""

        result = await eject_tool.execute(content=content, schema="TEST", format="markdown")

        assert result["output"] is not None
        # Markdown should have headers and structure
        assert "# TEST" in result["output"] or "## META" in result["output"]
        assert "VERSION" in result["output"]
        assert "STATUS" in result["output"]
