"""Unit tests for property test failure fixes.

These tests capture the exact falsifying examples from property tests
to ensure fixes work correctly.
"""

import pytest

from octave_mcp.core.emitter import emit, needs_quotes
from octave_mcp.core.lexer import tokenize
from octave_mcp.core.parser import ParserError, parse


class TestReservedKeywordFix:
    """Test that reserved keywords are handled correctly."""

    def test_meta_as_regular_key_should_fail(self):
        """META should not be allowed as a regular document key.

        Falsifying example: ===A===\nMETA::"0"\n===END===
        """
        doc = '===A===\nMETA::"0"\n===END==='

        # Should raise ParserError (not ValueError) because META is reserved
        with pytest.raises(ParserError):
            parse(doc)


class TestLexerVsOperatorFix:
    """Test that 'vs' operator is not matched inside quoted strings."""

    def test_vs_inside_quoted_string_should_not_error(self):
        """'vs' inside a quoted string should not trigger operator boundary error.

        Falsifying examples: A::"0vs", A::"vs"
        """
        # Test 1: "0vs"
        doc1 = '===TEST===\nA::"0vs"\n===END==='
        tokens1, _ = tokenize(doc1)
        ast1 = parse(tokens1)
        assert ast1 is not None

        # Test 2: "vs"
        doc2 = '===TEST===\nA::"vs"\n===END==='
        tokens2, _ = tokenize(doc2)
        ast2 = parse(tokens2)
        assert ast2 is not None

    def test_vs_as_identifier_is_valid(self):
        """Strings like 'AvsBs' or 'devs' are valid identifiers, not operator errors.

        The lexer should only match 'vs' as TENSION operator when it has word boundaries.
        Identifiers containing 'vs' (like AvsBs, devs, vserver) are valid.
        """
        # These should all tokenize successfully as IDENTIFIER tokens
        valid_identifiers = ["AvsBs", "devs", "vserver", "offset_vs_limit"]

        for identifier in valid_identifiers:
            doc = f"===TEST===\n{identifier}::value\n===END==="
            tokens, _ = tokenize(doc)
            # Should tokenize without error
            assert any(t.value == identifier for t in tokens)


class TestEmitterQuotingFix:
    """Test that emitter preserves quotes for reserved operator words."""

    def test_needs_quotes_for_operator_words(self):
        """Operator words like 'vs' should be flagged as needing quotes."""
        # These are operator words that must be quoted
        assert needs_quotes("vs") is True
        assert needs_quotes("true") is True
        assert needs_quotes("false") is True
        assert needs_quotes("null") is True

    def test_emit_preserves_quotes_for_vs(self):
        """Emitting a document with A::"vs" should preserve quotes.

        Falsifying example: A::"vs" → emits A::vs → re-parses as operator
        """
        # Parse document with quoted "vs"
        doc = '===TEST===\nA::"vs"\n===END==='
        tokens, _ = tokenize(doc)
        ast = parse(tokens)

        # Emit to canonical form
        output = emit(ast)

        # Should contain quoted "vs", not bare vs
        assert '"vs"' in output or "'vs'" in output
        assert "A::vs" not in output  # Must not emit unquoted

        # Verify round-trip works
        tokens2, _ = tokenize(output)
        ast2 = parse(tokens2)
        output2 = emit(ast2)

        assert output == output2  # Idempotence

    def test_emit_preserves_quotes_for_other_operators(self):
        """All ASCII operator aliases should be quoted when used as values."""
        operator_words = ["vs", "true", "false", "null"]

        for word in operator_words:
            doc = f'===TEST===\nKEY::"{word}"\n===END==='
            tokens, _ = tokenize(doc)
            ast = parse(tokens)
            output = emit(ast)

            # Should preserve quotes
            assert f'"{word}"' in output or f"'{word}'" in output
            assert f"KEY::{word}\n" not in output  # Not unquoted
