"""Tests for §CONTEXT section (Issue #32).

The §CONTEXT section provides a local definition namespace:
- Syntax: §CONTEXT::IDENTIFIER with key::value children
- Phase 1: Local definitions only (no inheritance yet)
- Replaces legacy 0.DEF pattern
- Similar to §0::META but for contextual definitions
"""

from octave_mcp.core.parser import parse


class TestContextSectionParsing:
    """Test §CONTEXT section parsing."""

    def test_parse_simple_context_section(self):
        """Should parse §CONTEXT:: section with children."""
        content = """
§CONTEXT::
  FOO::"bar"
  NUM::42
"""
        doc = parse(content)
        # Should have one section
        assert len(doc.sections) == 1
        section = doc.sections[0]

        # Should be a Section with correct properties
        assert hasattr(section, "section_id")
        assert section.section_id == "CONTEXT" or section.key == "CONTEXT"

        # Should have children
        assert hasattr(section, "children")
        assert len(section.children) >= 2

    def test_parse_context_section_with_identifier_suffix(self):
        """Should parse §CONTEXT::LOCAL as identifier-based section."""
        content = """
§CONTEXT::LOCAL
  VAR1::"value1"
  VAR2::123
"""
        doc = parse(content)
        assert len(doc.sections) == 1
        section = doc.sections[0]

        # Should recognize CONTEXT:: pattern or LOCAL as section name
        assert section.key in ("CONTEXT", "LOCAL")
        assert len(section.children) >= 2

    def test_parse_multiple_context_sections(self):
        """Should handle multiple §CONTEXT sections."""
        content = """
§CONTEXT::GLOBAL
  A::"global_value"

§CONTEXT::LOCAL
  B::"local_value"
"""
        doc = parse(content)
        # Should have two sections
        assert len(doc.sections) == 2

    def test_parse_context_with_nested_structures(self):
        """Should support nested blocks within §CONTEXT."""
        content = """
§CONTEXT::
  SIMPLE::"value"
  NESTED:
    INNER::"deep_value"
"""
        doc = parse(content)
        assert len(doc.sections) == 1
        section = doc.sections[0]
        # Should have at least 2 children (SIMPLE and NESTED)
        assert len(section.children) >= 2


class TestContextSectionSemantics:
    """Test §CONTEXT section semantic behavior."""

    def test_context_replaces_legacy_def_pattern(self):
        """§CONTEXT should serve as modern replacement for 0.DEF."""
        # Legacy pattern (for reference):
        # 0.DEF::VAR::"value"

        # Modern pattern:
        content = """
§CONTEXT::
  VAR::"value"
  TIMEOUT::30
"""
        doc = parse(content)
        section = doc.sections[0]

        # Should be parseable as section with definitions
        assert hasattr(section, "children")
        assert len(section.children) == 2

    def test_context_with_complex_values(self):
        """Should handle complex value types in §CONTEXT."""
        content = """
§CONTEXT::
  LIST::[1, 2, 3]
  BOOL::true
  NULL::null
"""
        doc = parse(content)
        section = doc.sections[0]
        assert len(section.children) >= 3

    def test_context_before_other_sections(self):
        """§CONTEXT typically appears early in document."""
        content = """
§CONTEXT::
  BASE_URL::"https://api.example.com"

§1::MAIN_CONTENT
  ENDPOINT::"/users"
"""
        doc = parse(content)
        # Should parse both sections
        assert len(doc.sections) == 2
        # First section should be CONTEXT-related
        first = doc.sections[0]
        assert "CONTEXT" in first.key or first.section_id == "CONTEXT"


class TestContextSectionEdgeCases:
    """Test §CONTEXT edge cases and error handling."""

    def test_empty_context_section(self):
        """Should handle §CONTEXT with no children."""
        content = """
§CONTEXT::
"""
        doc = parse(content)
        assert len(doc.sections) == 1
        section = doc.sections[0]
        # Empty section should still parse
        assert hasattr(section, "children")

    def test_context_without_explicit_number(self):
        """§CONTEXT:: should work without numeric section ID."""
        content = """
§CONTEXT::
  VAR::"value"
"""
        doc = parse(content)
        # Should parse successfully
        assert len(doc.sections) == 1

    def test_context_interleaved_with_numbered_sections(self):
        """§CONTEXT can coexist with numbered sections."""
        content = """
§1::INTRO
  TEXT::"Introduction"

§CONTEXT::
  VERSION::"1.0"

§2::BODY
  TEXT::"Main content"
"""
        doc = parse(content)
        # Should parse all three sections
        assert len(doc.sections) == 3
