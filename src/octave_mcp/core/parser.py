"""OCTAVE parser with lenient input support.

Implements P1.3: lenient_parser_with_envelope_completion

Parses lexer tokens into AST with:
- Envelope inference for single documents
- Whitespace normalization around ::
- Nested block structure with indentation
- META block extraction
"""

from typing import Any

from octave_mcp.core.ast_nodes import Assignment, Block, Document, InlineMap, ListValue
from octave_mcp.core.lexer import Token, TokenType, tokenize


class ParserError(Exception):
    """Parser error with position information."""

    def __init__(self, message: str, token: Token | None = None, error_code: str = "E001"):
        self.message = message
        self.token = token
        self.error_code = error_code
        if token:
            super().__init__(f"{error_code} at line {token.line}, column {token.column}: {message}")
        else:
            super().__init__(f"{error_code}: {message}")


class Parser:
    """OCTAVE parser with lenient input support."""

    def __init__(self, tokens: list[Token]):
        """Initialize parser with token stream."""
        self.tokens = tokens
        self.pos = 0
        self.current_indent = 0

    def current(self) -> Token:
        """Get current token."""
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF
        return self.tokens[self.pos]

    def peek(self, offset: int = 1) -> Token:
        """Peek ahead at token."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF
        return self.tokens[pos]

    def advance(self) -> Token:
        """Consume and return current token."""
        token = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def expect(self, token_type: TokenType) -> Token:
        """Expect specific token type and consume it."""
        token = self.current()
        if token.type != token_type:
            raise ParserError(f"Expected {token_type}, got {token.type}", token)
        return self.advance()

    def skip_whitespace(self) -> None:
        """Skip newlines and comments."""
        while self.current().type in (TokenType.NEWLINE, TokenType.COMMENT):
            self.advance()

    def parse_document(self) -> Document:
        """Parse a complete OCTAVE document."""
        doc = Document()
        self.skip_whitespace()

        # Check for explicit envelope
        if self.current().type == TokenType.ENVELOPE_START:
            token = self.advance()
            doc.name = token.value
            self.skip_whitespace()
        else:
            # Infer envelope for single doc
            doc.name = "INFERRED"

        # Parse META block first if present
        if self.current().type == TokenType.IDENTIFIER and self.current().value == "META":
            meta_block = self.parse_meta_block()
            doc.meta = meta_block
            self.skip_whitespace()

        # Check for separator
        if self.current().type == TokenType.SEPARATOR:
            doc.has_separator = True
            self.advance()
            self.skip_whitespace()

        # Parse document body
        while self.current().type != TokenType.ENVELOPE_END and self.current().type != TokenType.EOF:
            # Skip indentation at document level
            if self.current().type == TokenType.INDENT:
                self.advance()
                continue

            # Parse section (assignment or block)
            section = self.parse_section(0)
            if section:
                doc.sections.append(section)

            self.skip_whitespace()

        # Expect END envelope (lenient - allow missing)
        if self.current().type == TokenType.ENVELOPE_END:
            self.advance()

        return doc

    def parse_meta_block(self) -> dict[str, Any]:
        """Parse META block into dictionary."""
        meta: dict[str, Any] = {}

        # Consume META identifier
        self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.BLOCK)
        self.skip_whitespace()

        # Expect indentation for META children
        if self.current().type != TokenType.INDENT:
            return meta

        indent_level = self.current().value
        self.advance()

        # Parse META fields
        while True:
            # Check if we're still in META block
            if self.current().type == TokenType.NEWLINE:
                self.advance()
                # Check next line's indentation
                if self.current().type == TokenType.INDENT:
                    if self.current().value < indent_level:
                        break  # End of META block
                    self.advance()
                elif self.current().type != TokenType.EOF:
                    break  # No indentation, end of META
                else:
                    break
            elif self.current().type == TokenType.EOF:
                break

            # Parse META field (must be assignment)
            if self.current().type == TokenType.IDENTIFIER:
                key = self.current().value
                self.advance()

                if self.current().type == TokenType.ASSIGN:
                    self.advance()
                    value = self.parse_value()
                    meta[key] = value
                else:
                    # Skip malformed field
                    continue

            self.skip_whitespace()

        return meta

    def parse_section(self, base_indent: int) -> Assignment | Block | None:
        """Parse a top-level section (assignment or block)."""
        if self.current().type != TokenType.IDENTIFIER:
            return None

        key = self.current().value
        self.advance()

        # Check for assignment or block
        if self.current().type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_value()
            return Assignment(key=key, value=value, line=self.current().line, column=self.current().column)

        elif self.current().type == TokenType.BLOCK:
            block_token = self.current()
            self.advance()

            # E001: Check if there's a value on the same line as the block operator
            # This catches "KEY: value" which should be "KEY::value"
            next_token = self.current()
            if (next_token.type == TokenType.IDENTIFIER and
                next_token.line == block_token.line):
                raise ParserError(
                    "Single colon assignment not allowed. Use KEY::value (double colon). "
                    "OCTAVE uses :: for assignment because : is the block operator. This prevents ambiguity.",
                    block_token,
                    "E001"
                )

            self.skip_whitespace()

            # Parse block children
            children: list[Assignment | Block] = []

            # Expect indentation for children
            if self.current().type == TokenType.INDENT:
                child_indent = self.current().value
                self.advance()

                while True:
                    # Parse child
                    child = self.parse_section(child_indent)
                    if child:
                        children.append(child)

                    self.skip_whitespace()

                    # Check if more children
                    if self.current().type == TokenType.INDENT:
                        if self.current().value < child_indent:
                            break  # Dedent, end of block
                        elif self.current().value == child_indent:
                            self.advance()  # Same level, continue
                        else:
                            # Deeper indent handled by recursive call
                            self.advance()
                    elif self.current().type in (TokenType.EOF, TokenType.ENVELOPE_END):
                        break
                    else:
                        break  # No indentation, end of block

            return Block(key=key, children=children, line=self.current().line, column=self.current().column)

        return None

    def parse_value(self) -> Any:
        """Parse a value (string, number, boolean, null, list)."""
        token = self.current()

        if token.type == TokenType.STRING:
            self.advance()
            return token.value

        elif token.type == TokenType.NUMBER:
            self.advance()
            return token.value

        elif token.type == TokenType.BOOLEAN:
            self.advance()
            return token.value

        elif token.type == TokenType.NULL:
            self.advance()
            return None

        elif token.type == TokenType.LIST_START:
            return self.parse_list()

        elif token.type == TokenType.IDENTIFIER:
            # Bare word
            self.advance()
            return token.value

        elif token.type == TokenType.FLOW:
            # Flow expression like A→B→C
            return self.parse_flow_expression()

        else:
            # Try to consume as bare word
            value = str(token.value)
            self.advance()
            return value

    def parse_list(self) -> ListValue:
        """Parse list [a, b, c]."""
        self.expect(TokenType.LIST_START)
        items: list[Any] = []

        # Handle empty list
        if self.current().type == TokenType.LIST_END:
            self.advance()
            return ListValue(items=[])

        # Parse list items
        while True:
            # Parse item value
            item = self.parse_list_item()
            items.append(item)

            # Check for comma or end
            if self.current().type == TokenType.COMMA:
                self.advance()
                # Skip whitespace after comma
                while self.current().type == TokenType.NEWLINE:
                    self.advance()
            elif self.current().type == TokenType.LIST_END:
                break
            else:
                # Allow whitespace/newlines in lists
                if self.current().type == TokenType.NEWLINE:
                    self.advance()
                else:
                    break

        self.expect(TokenType.LIST_END)
        return ListValue(items=items)

    def parse_list_item(self) -> Any:
        """Parse a single list item."""
        # Check for inline map [k::v, k2::v2]
        if self.current().type == TokenType.IDENTIFIER and self.peek().type == TokenType.ASSIGN:
            # Inline map item
            pairs: dict[str, Any] = {}
            key = self.current().value
            self.advance()
            self.expect(TokenType.ASSIGN)
            value = self.parse_value()
            pairs[key] = value
            return InlineMap(pairs=pairs)

        # Regular value
        return self.parse_value()

    def parse_flow_expression(self) -> str:
        """Parse flow expression like A→B→C."""
        parts = []

        # Collect all parts of flow
        while self.current().type in (TokenType.IDENTIFIER, TokenType.FLOW, TokenType.STRING):
            if self.current().type == TokenType.FLOW:
                parts.append(self.current().value)
                self.advance()
            elif self.current().type in (TokenType.IDENTIFIER, TokenType.STRING):
                parts.append(self.current().value)
                self.advance()
            else:
                break

        return "".join(str(p) for p in parts)


def parse(content: str) -> Document:
    """Parse OCTAVE content into AST.

    Args:
        content: Raw OCTAVE text (lenient or canonical)

    Returns:
        Document AST

    Raises:
        ParserError: On syntax errors
    """
    tokens = tokenize(content)
    parser = Parser(tokens)
    return parser.parse_document()
