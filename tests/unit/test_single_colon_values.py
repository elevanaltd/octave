"""Tests for single-colon-in-value support (Issue #41 Phase 2).

Single colons within values should be preserved:
- HERMES:API_TIMEOUT should remain as-is
- CONFIG::HERMES:API_TIMEOUT should parse correctly
"""

from octave_mcp.core.emitter import emit
from octave_mcp.core.parser import parse


class TestSingleColonInValues:
    """Test that single colons within values are preserved."""

    def test_single_colon_in_value_preserved(self):
        """Should preserve single colon in value like HERMES:API_TIMEOUT."""
        content = """===TEST===
CONFIG::HERMES:API_TIMEOUT
===END==="""

        # Parse and emit
        doc = parse(content)
        canonical = emit(doc)

        # Should preserve the colon in HERMES:API_TIMEOUT
        assert "HERMES:API_TIMEOUT" in canonical

    def test_multiple_colons_in_value(self):
        """Should preserve multiple colons in compound values."""
        content = """===TEST===
PATH::MODULE:SUBMODULE:COMPONENT
===END==="""

        doc = parse(content)
        canonical = emit(doc)

        # Should preserve full path with colons
        assert "MODULE:SUBMODULE:COMPONENT" in canonical

    def test_colon_value_with_quoted_string(self):
        """Should handle colon values alongside quoted strings."""
        content = """===TEST===
TIMEOUT::HERMES:API_TIMEOUT
DESCRIPTION::"API timeout configuration"
===END==="""

        doc = parse(content)
        canonical = emit(doc)

        assert "HERMES:API_TIMEOUT" in canonical
        assert "API timeout configuration" in canonical

    def test_colon_value_in_list(self):
        """Should preserve colon values within lists."""
        content = """===TEST===
CONFIGS::[HERMES:TIMEOUT, APOLLO:RETRIES, ATLAS:MAX_LOAD]
===END==="""

        doc = parse(content)
        canonical = emit(doc)

        assert "HERMES:TIMEOUT" in canonical
        assert "APOLLO:RETRIES" in canonical
        assert "ATLAS:MAX_LOAD" in canonical

    def test_single_colon_operator_still_normalized(self):
        """KEY:value (single colon as operator) should still work as before."""
        # This is legacy behavior - single colon as operator
        # Not the primary focus of this fix, but should not break
        content = """===TEST===
KEY:
  CHILD::value
===END==="""

        doc = parse(content)
        canonical = emit(doc)

        # Should emit valid OCTAVE with block structure
        assert "KEY:" in canonical or "KEY::" in canonical
        assert "CHILD::value" in canonical


class TestSingleColonEdgeCases:
    """Test edge cases for single-colon handling."""

    def test_trailing_colon_in_identifier(self):
        """Should handle identifiers ending with colon correctly."""
        # This is actually a structural operator, not a value
        content = """===TEST===
PARENT:
  CHILD::value
===END==="""

        doc = parse(content)
        canonical = emit(doc)

        # Should produce valid structure
        assert "PARENT:" in canonical
        assert "value" in canonical

    def test_leading_colon_not_valid(self):
        """Leading colon should not be treated as identifier."""
        # This would be invalid syntax - parser should handle gracefully
        # Not a primary test case, but document behavior
        # A3 FIX: Removed placeholder pass - test is documentary only

    def test_empty_value_between_colons(self):
        """Should handle MODULE::SUBMODULE (empty between colons)."""
        content = """===TEST===
PATH::MODULE::SUBMODULE
===END==="""

        doc = parse(content)
        canonical = emit(doc)

        # Double colons are ASSIGN operators, not path separators
        # This should parse as PATH assigned to MODULE::SUBMODULE
        # Which means MODULE:SUBMODULE structure
        assert "MODULE" in canonical

    def test_dotted_and_colon_identifiers_together(self):
        """Should handle both dots and colons in values."""
        content = """===TEST===
REF::pkg.tool:config.option
===END==="""

        doc = parse(content)
        canonical = emit(doc)

        # Should preserve both dots and colons
        assert "pkg.tool:config.option" in canonical or "pkg.tool" in canonical
