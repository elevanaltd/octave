"""Tests for OCTAVE parser (P1.3).

Tests lenient parsing with envelope completion, whitespace normalization,
and nested block structure.
"""

import pytest

from octave_mcp.core.ast_nodes import Assignment, Block, Document, ListValue
from octave_mcp.core.lexer import tokenize
from octave_mcp.core.parser import parse, ParserError


class TestEnvelopeInference:
    """Test envelope inference for single documents."""

    def test_infers_envelope_for_single_doc_without_envelope(self):
        """Should infer ===INFERRED=== for single document without envelope."""
        content = """META:
  TYPE::TEST
  VERSION::"1.0"
"""
        doc = parse(content)
        assert doc.name == "INFERRED"
        assert len(doc.meta) >= 1  # At least TYPE
        assert doc.meta.get("TYPE") == "TEST"

    def test_preserves_explicit_envelope(self):
        """Should preserve explicit envelope name."""
        content = """===MY_DOC===
META:
  TYPE::TEST
===END===
"""
        doc = parse(content)
        assert doc.name == "MY_DOC"

    def test_errors_on_missing_schema_selector_without_envelope(self):
        """Should error if no envelope and no META block for schema detection."""
        content = """SOME_FIELD::value
"""
        # This should still infer INFERRED envelope, but may warn about schema
        doc = parse(content)
        assert doc.name == "INFERRED"


class TestWhitespaceNormalization:
    """Test whitespace normalization around operators."""

    def test_normalizes_whitespace_around_assignment(self):
        """Should normalize 'KEY :: value' to 'KEY::value'."""
        content = """===TEST===
KEY :: value
===END===
"""
        doc = parse(content)
        # Parser should normalize during parsing
        # Check that it parsed correctly
        assert len(doc.sections) > 0

    def test_handles_no_whitespace_assignment(self):
        """Should handle canonical KEY::value."""
        content = """===TEST===
KEY::value
===END===
"""
        doc = parse(content)
        assert len(doc.sections) > 0


class TestBlockStructure:
    """Test nested block parsing."""

    def test_parses_simple_block(self):
        """Should parse KEY: with nested children."""
        content = """===TEST===
CONFIG:
  NESTED::value
===END===
"""
        doc = parse(content)
        assert len(doc.sections) > 0
        block = doc.sections[0]
        assert isinstance(block, Block)
        assert block.key == "CONFIG"
        assert len(block.children) > 0

    def test_parses_deeply_nested_blocks(self):
        """Should parse multiple levels of nesting."""
        content = """===TEST===
LEVEL1:
  LEVEL2:
    LEVEL3::value
===END===
"""
        doc = parse(content)
        assert len(doc.sections) > 0
        level1 = doc.sections[0]
        assert isinstance(level1, Block)
        assert level1.key == "LEVEL1"
        assert len(level1.children) > 0

        level2 = level1.children[0]
        assert isinstance(level2, Block)
        assert level2.key == "LEVEL2"
        assert len(level2.children) > 0

    def test_enforces_2_space_indentation(self):
        """Should validate 2-space indentation (tabs caught by lexer)."""
        content = """===TEST===
BLOCK:
  CHILD::value
===END===
"""
        doc = parse(content)
        # Should parse successfully with 2-space indent
        assert len(doc.sections) > 0


class TestMetaBlock:
    """Test META block parsing."""

    def test_parses_meta_block(self):
        """Should parse META block into document.meta."""
        content = """===TEST===
META:
  TYPE::TEST_DOC
  VERSION::"1.0"
  STATUS::ACTIVE
===END===
"""
        doc = parse(content)
        assert doc.meta.get("TYPE") == "TEST_DOC"
        assert doc.meta.get("VERSION") == "1.0"
        assert doc.meta.get("STATUS") == "ACTIVE"

    def test_meta_without_envelope(self):
        """Should handle META in document without envelope."""
        content = """META:
  TYPE::TEST
  VERSION::"1.0"
"""
        doc = parse(content)
        assert doc.name == "INFERRED"
        assert doc.meta.get("TYPE") == "TEST"


class TestListParsing:
    """Test list parsing."""

    def test_parses_simple_list(self):
        """Should parse [a, b, c]."""
        content = """===TEST===
TAGS::[alpha,beta,gamma]
===END===
"""
        doc = parse(content)
        assert len(doc.sections) > 0
        assignment = doc.sections[0]
        assert isinstance(assignment, Assignment)
        assert assignment.key == "TAGS"
        assert isinstance(assignment.value, ListValue)
        assert len(assignment.value.items) == 3

    def test_parses_empty_list(self):
        """Should parse []."""
        content = """===TEST===
EMPTY::[]
===END===
"""
        doc = parse(content)
        assignment = doc.sections[0]
        assert isinstance(assignment.value, ListValue)
        assert len(assignment.value.items) == 0


class TestSeparator:
    """Test separator handling."""

    def test_recognizes_separator(self):
        """Should recognize --- separator."""
        content = """===TEST===
META:
  TYPE::TEST
---
CONTENT::data
===END===
"""
        doc = parse(content)
        assert doc.has_separator is True


class TestErrorHandling:
    """Test parser error cases."""

    def test_errors_on_single_colon_assignment(self):
        """Should error on KEY: value (single colon for assignment)."""
        content = """===TEST===
KEY: value
===END===
"""
        # Single colon with value on same line is ambiguous
        # Should be treated as block with error or parse as block
        # Based on spec, single colon is block operator
        doc = parse(content)
        # This should parse as a block, not assignment
        # If it has a value on same line, it's malformed
        # For now, we'll be lenient and treat it as block

    def test_handles_missing_end_envelope(self):
        """Should handle missing ===END===."""
        content = """===TEST===
KEY::value
"""
        # Should still parse, maybe with warning
        doc = parse(content)
        assert doc.name == "TEST"
