"""Tests for OCTAVE lexer with ASCII normalization (P1.2)."""

import pytest

from octave_mcp.core.lexer import LexerError, TokenType, tokenize


class TestLexerBasicTokenization:
    """Test basic tokenization of canonical OCTAVE."""

    def test_tokenize_assignment_operator(self):
        """Should tokenize :: as ASSIGN."""
        tokens = tokenize("KEY::value")
        assert len(tokens) >= 3
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "KEY"
        assert tokens[1].type == TokenType.ASSIGN
        assert tokens[1].value == "::"
        assert tokens[2].type == TokenType.IDENTIFIER
        assert tokens[2].value == "value"

    def test_tokenize_block_operator(self):
        """Should tokenize : as BLOCK."""
        tokens = tokenize("KEY:")
        assert len(tokens) >= 2
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "KEY"
        assert tokens[1].type == TokenType.BLOCK
        assert tokens[1].value == ":"

    def test_tokenize_longest_match_rule(self):
        """Should recognize :: before : (longest match)."""
        tokens = tokenize("KEY::value")
        # Should have ASSIGN (::) not BLOCK (:) + BLOCK (:)
        assign_tokens = [t for t in tokens if t.type == TokenType.ASSIGN]
        block_tokens = [t for t in tokens if t.type == TokenType.BLOCK]
        assert len(assign_tokens) == 1
        assert len(block_tokens) == 0


class TestASCIINormalization:
    """Test ASCII alias normalization to unicode operators."""

    def test_normalize_arrow_operator(self):
        """Should normalize -> to →."""
        tokens = tokenize("A->B")
        arrow_token = [t for t in tokens if t.type == TokenType.FLOW][0]
        assert arrow_token.value == "→"
        assert arrow_token.normalized_from == "->"

    def test_normalize_synthesis_operator(self):
        """Should normalize + to ⊕."""
        tokens = tokenize("A+B")
        synth_token = [t for t in tokens if t.type == TokenType.SYNTHESIS][0]
        assert synth_token.value == "⊕"
        assert synth_token.normalized_from == "+"

    def test_normalize_concat_operator(self):
        """Should normalize ~ to ⧺."""
        tokens = tokenize("A~B")
        concat_token = [t for t in tokens if t.type == TokenType.CONCAT][0]
        assert concat_token.value == "⧺"
        assert concat_token.normalized_from == "~"

    def test_normalize_tension_operator(self):
        """Should normalize vs to ⇌ with word boundaries."""
        tokens = tokenize("A vs B")
        tension_token = [t for t in tokens if t.type == TokenType.TENSION][0]
        assert tension_token.value == "⇌"
        assert tension_token.normalized_from == "vs"

    def test_normalize_alternative_operator(self):
        """Should normalize | to ∨."""
        tokens = tokenize("A|B")
        alt_token = [t for t in tokens if t.type == TokenType.ALTERNATIVE][0]
        assert alt_token.value == "∨"
        assert alt_token.normalized_from == "|"

    def test_normalize_constraint_operator(self):
        """Should normalize & to ∧."""
        tokens = tokenize("[A&B]")
        constraint_token = [t for t in tokens if t.type == TokenType.CONSTRAINT][0]
        assert constraint_token.value == "∧"
        assert constraint_token.normalized_from == "&"

    def test_normalize_section_marker(self):
        """Should normalize # to §."""
        tokens = tokenize("#1::OVERVIEW")
        section_token = [t for t in tokens if t.type == TokenType.SECTION][0]
        assert section_token.value == "§"
        assert section_token.normalized_from == "#"


class TestVsWordBoundaries:
    """Test 'vs' operator requires word boundaries."""

    def test_vs_with_spaces(self):
        """Should accept 'vs' with spaces."""
        tokens = tokenize("Speed vs Quality")
        tension_tokens = [t for t in tokens if t.type == TokenType.TENSION]
        assert len(tension_tokens) == 1
        assert tension_tokens[0].value == "⇌"

    def test_vs_in_brackets(self):
        """Should accept 'vs' in brackets."""
        tokens = tokenize("[A vs B]")
        tension_tokens = [t for t in tokens if t.type == TokenType.TENSION]
        assert len(tension_tokens) == 1

    def test_vs_without_boundaries_rejected(self):
        """Should reject 'vs' without word boundaries."""
        with pytest.raises(LexerError) as exc_info:
            tokenize("SpeedvsQuality")
        assert "E005" in str(exc_info.value)
        assert "word boundaries" in str(exc_info.value).lower()


class TestUnicodeNormalization:
    """Test NFC unicode normalization."""

    def test_nfc_normalization_applied(self):
        """Should apply NFC normalization to all text."""
        # Use composed form (NFC) vs decomposed (NFD)
        # The é character: composed é (U+00E9) vs decomposed e + ́ (U+0065 U+0301)
        import unicodedata

        composed = "café"  # NFC form
        decomposed = unicodedata.normalize("NFD", composed)  # NFD form

        tokens = tokenize(f'KEY::"{decomposed}"')
        string_token = [t for t in tokens if t.type == TokenType.STRING][0]
        # Should be normalized to NFC
        assert unicodedata.is_normalized("NFC", string_token.value)


class TestTabRejection:
    """Test that tabs are rejected with E005."""

    def test_tabs_rejected(self):
        """Should reject tabs with clear error E005."""
        with pytest.raises(LexerError) as exc_info:
            tokenize("KEY::\tvalue")
        assert "E005" in str(exc_info.value)
        assert "tab" in str(exc_info.value).lower()


class TestEnvelopeTokenization:
    """Test envelope markers."""

    def test_start_envelope(self):
        """Should tokenize ===NAME=== as ENVELOPE_START."""
        tokens = tokenize("===TEST===")
        assert tokens[0].type == TokenType.ENVELOPE_START
        assert tokens[0].value == "TEST"

    def test_end_envelope(self):
        """Should tokenize ===END=== as ENVELOPE_END."""
        tokens = tokenize("===END===")
        assert tokens[0].type == TokenType.ENVELOPE_END


class TestStringTokenization:
    """Test string literal handling."""

    def test_quoted_string(self):
        """Should tokenize quoted strings."""
        tokens = tokenize('KEY::"hello world"')
        string_token = [t for t in tokens if t.type == TokenType.STRING][0]
        assert string_token.value == "hello world"

    def test_bare_word_string(self):
        """Should tokenize bare words as identifiers."""
        tokens = tokenize("KEY::value")
        value_token = [t for t in tokens if t.value == "value"][0]
        assert value_token.type == TokenType.IDENTIFIER

    def test_string_escapes(self):
        """Should handle escape sequences in strings."""
        tokens = tokenize(r'KEY::"line1\nline2\ttab\"quote"')
        string_token = [t for t in tokens if t.type == TokenType.STRING][0]
        assert '"' in string_token.value
        # Escapes should be preserved in token value


class TestNumberTokenization:
    """Test number literal handling."""

    def test_integer(self):
        """Should tokenize integers."""
        tokens = tokenize("COUNT::42")
        number_token = [t for t in tokens if t.type == TokenType.NUMBER][0]
        assert number_token.value == 42

    def test_negative_integer(self):
        """Should tokenize negative integers."""
        tokens = tokenize("OFFSET::-10")
        number_token = [t for t in tokens if t.type == TokenType.NUMBER][0]
        assert number_token.value == -10

    def test_float(self):
        """Should tokenize floats."""
        tokens = tokenize("PI::3.14")
        number_token = [t for t in tokens if t.type == TokenType.NUMBER][0]
        assert number_token.value == 3.14

    def test_scientific_notation(self):
        """Should tokenize scientific notation."""
        tokens = tokenize("BIG::-1e10")
        number_token = [t for t in tokens if t.type == TokenType.NUMBER][0]
        assert number_token.value == -1e10


class TestBooleanAndNull:
    """Test boolean and null literal handling."""

    def test_true_literal(self):
        """Should tokenize 'true' as BOOLEAN."""
        tokens = tokenize("ENABLED::true")
        bool_token = [t for t in tokens if t.type == TokenType.BOOLEAN][0]
        assert bool_token.value is True

    def test_false_literal(self):
        """Should tokenize 'false' as BOOLEAN."""
        tokens = tokenize("ENABLED::false")
        bool_token = [t for t in tokens if t.type == TokenType.BOOLEAN][0]
        assert bool_token.value is False

    def test_null_literal(self):
        """Should tokenize 'null' as NULL."""
        tokens = tokenize("VALUE::null")
        null_token = [t for t in tokens if t.type == TokenType.NULL][0]
        assert null_token.value is None


class TestComments:
    """Test comment handling."""

    def test_line_comment(self):
        """Should tokenize // comments."""
        tokens = tokenize("KEY::value // this is a comment")
        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT]
        assert len(comment_tokens) == 1
        assert "this is a comment" in comment_tokens[0].value

    def test_comment_at_line_start(self):
        """Should tokenize comments at line start."""
        tokens = tokenize("// Full line comment\nKEY::value")
        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT]
        assert len(comment_tokens) == 1


class TestBrackets:
    """Test bracket tokenization."""

    def test_square_brackets(self):
        """Should tokenize [ and ] as LIST_START/LIST_END."""
        tokens = tokenize("[a,b,c]")
        assert tokens[0].type == TokenType.LIST_START
        list_end_tokens = [t for t in tokens if t.type == TokenType.LIST_END]
        assert len(list_end_tokens) == 1


class TestNormalizationLog:
    """Test that normalizations are logged."""

    def test_normalization_logged(self):
        """Should log all ASCII normalizations."""
        tokens = tokenize("A->B+C")
        normalizations = [t for t in tokens if hasattr(t, "normalized_from") and t.normalized_from]
        assert len(normalizations) >= 2  # -> and +

    def test_unicode_input_not_logged(self):
        """Should not log normalizations for unicode input."""
        tokens = tokenize("A→B⊕C")
        normalizations = [t for t in tokens if hasattr(t, "normalized_from") and t.normalized_from]
        assert len(normalizations) == 0


class TestWhitespace:
    """Test whitespace handling."""

    def test_whitespace_preserved_in_position(self):
        """Should track positions correctly across whitespace."""
        tokens = tokenize("KEY :: value")
        # Positions should reflect actual character positions
        assert all(hasattr(t, "line") and hasattr(t, "column") for t in tokens)

    def test_newlines_tracked(self):
        """Should track line numbers across newlines."""
        tokens = tokenize("LINE1::a\nLINE2::b")
        line2_tokens = [t for t in tokens if hasattr(t, "line") and t.line == 2]
        assert len(line2_tokens) > 0
