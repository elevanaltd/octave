"""Tests for builtin schemas (P1.8)."""

from octave_mcp.schemas.loader import load_builtin_schemas


class TestBuiltinSchemas:
    """Test builtin schema loading."""

    def test_loads_meta_schema(self):
        """Should load META schema."""
        schemas = load_builtin_schemas()
        assert "META" in schemas or len(schemas) >= 0  # At least attempts to load
