"""Tests for OCTAVE canonical emitter (P1.4).

Tests AST → canonical OCTAVE string emission with:
- Unicode operators (never ASCII)
- No whitespace around ::
- Explicit envelope
- Deterministic output
- Idempotence
"""

import pytest

from octave_mcp.core.ast_nodes import Assignment, Block, Document, ListValue
from octave_mcp.core.emitter import emit
from octave_mcp.core.parser import parse


class TestCanonicalEmission:
    """Test canonical OCTAVE emission."""

    def test_emits_unicode_operators(self):
        """Should emit unicode operators, never ASCII."""
        doc = Document(
            name="TEST",
            sections=[Assignment(key="FLOW", value="A→B→C")],
        )
        result = emit(doc)
        assert "→" in result
        assert "->" not in result

    def test_no_whitespace_around_assignment(self):
        """Should emit KEY::value with no spaces."""
        doc = Document(name="TEST", sections=[Assignment(key="KEY", value="value")])
        result = emit(doc)
        assert "KEY::value" in result
        assert "KEY :: value" not in result

    def test_explicit_envelope_always_present(self):
        """Should always emit explicit envelope."""
        doc = Document(name="TEST", sections=[Assignment(key="KEY", value="value")])
        result = emit(doc)
        assert result.startswith("===TEST===")
        assert result.strip().endswith("===END===")

    def test_quoted_strings_where_required(self):
        """Should quote strings with spaces/special chars."""
        doc = Document(name="TEST", sections=[Assignment(key="KEY", value="hello world")])
        result = emit(doc)
        assert '"hello world"' in result

    def test_bare_strings_when_safe(self):
        """Should use bare words when no spaces/special chars."""
        doc = Document(name="TEST", sections=[Assignment(key="KEY", value="simple")])
        result = emit(doc)
        assert "KEY::simple" in result
        assert '"simple"' not in result

    def test_2_space_indentation(self):
        """Should use consistent 2-space indentation."""
        doc = Document(
            name="TEST",
            sections=[Block(key="BLOCK", children=[Assignment(key="CHILD", value="value")])],
        )
        result = emit(doc)
        lines = result.split("\n")
        # Find CHILD line
        child_line = [l for l in lines if "CHILD" in l][0]
        assert child_line.startswith("  ")  # 2 spaces
        assert not child_line.startswith("    ")  # Not 4 spaces

    def test_empty_list(self):
        """Should emit empty list as []."""
        doc = Document(name="TEST", sections=[Assignment(key="EMPTY", value=ListValue(items=[]))])
        result = emit(doc)
        assert "EMPTY::[]" in result

    def test_list_with_items(self):
        """Should emit list with comma-separated items."""
        doc = Document(name="TEST", sections=[Assignment(key="TAGS", value=ListValue(items=["a", "b", "c"]))])
        result = emit(doc)
        assert "TAGS::[a,b,c]" in result


class TestIdempotence:
    """Test emit is idempotent."""

    def test_emit_parse_emit_idempotent(self):
        """Should satisfy emit(parse(emit(parse(x)))) == emit(parse(x))."""
        original = """===TEST===
META:
  TYPE::TEST_DOC
  VERSION::"1.0"
---
DATA::value
TAGS::[a,b,c]
===END===
"""
        doc1 = parse(original)
        emitted1 = emit(doc1)
        doc2 = parse(emitted1)
        emitted2 = emit(doc2)
        assert emitted1 == emitted2


class TestMetaEmission:
    """Test META block emission."""

    def test_emits_meta_block(self):
        """Should emit META block."""
        doc = Document(
            name="TEST",
            meta={"TYPE": "TEST_DOC", "VERSION": "1.0"},
            sections=[],
        )
        result = emit(doc)
        assert "META:" in result
        assert "TYPE::TEST_DOC" in result
        assert "VERSION::" in result

    def test_emits_separator_when_present(self):
        """Should emit --- separator when has_separator=True."""
        doc = Document(name="TEST", has_separator=True, sections=[Assignment(key="KEY", value="value")])
        result = emit(doc)
        assert "---" in result


class TestBlockEmission:
    """Test block structure emission."""

    def test_emits_simple_block(self):
        """Should emit KEY: with nested children."""
        doc = Document(
            name="TEST",
            sections=[Block(key="CONFIG", children=[Assignment(key="NESTED", value="value")])],
        )
        result = emit(doc)
        assert "CONFIG:" in result
        assert "  NESTED::value" in result

    def test_emits_deeply_nested_blocks(self):
        """Should emit multiple nesting levels."""
        doc = Document(
            name="TEST",
            sections=[
                Block(
                    key="LEVEL1",
                    children=[
                        Block(key="LEVEL2", children=[Assignment(key="LEVEL3", value="value")]),
                    ],
                )
            ],
        )
        result = emit(doc)
        assert "LEVEL1:" in result
        assert "  LEVEL2:" in result
        assert "    LEVEL3::value" in result

    def test_empty_block(self):
        """Should emit empty block as KEY: with no children."""
        doc = Document(name="TEST", sections=[Block(key="EMPTY", children=[])])
        result = emit(doc)
        assert "EMPTY:" in result
