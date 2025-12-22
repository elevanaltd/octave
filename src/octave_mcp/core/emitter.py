"""Canonical OCTAVE emitter.

Implements P1.4: canonical_emitter

Emits strict canonical OCTAVE from AST with:
- Unicode operators only
- No whitespace around ::
- Explicit envelope always present
- Deterministic formatting
- 2-space indentation
"""

import re
from typing import Any

from octave_mcp.core.ast_nodes import Assignment, Block, Document, InlineMap, ListValue

IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def needs_quotes(value: Any) -> bool:
    """Check if a string value needs quotes."""
    if not isinstance(value, str):
        return False

    # Empty string needs quotes
    if not value:
        return True

    # Reserved words need quotes to avoid becoming literals
    if value in ("true", "false", "null"):
        return True

    # If it's not a valid identifier, it needs quotes
    # This covers:
    # - Numbers (start with digit)
    # - Dashes (not allowed in identifiers)
    # - Special chars (spaces, colons, brackets, etc.)
    if not IDENTIFIER_PATTERN.match(value):
        return True

    return False


def emit_value(value: Any) -> str:
    """Emit a value in canonical form."""
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        if needs_quotes(value):
            # Escape special characters
            escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
            return f'"{escaped}"'
        return value
    elif isinstance(value, ListValue):
        if not value.items:
            return "[]"
        items = [emit_value(item) for item in value.items]
        return f"[{','.join(items)}]"
    elif isinstance(value, InlineMap):
        pairs = [f"{k}::{emit_value(v)}" for k, v in value.pairs.items()]
        return f"[{','.join(pairs)}]"
    else:
        # Fallback for unknown types
        return str(value)


def emit_assignment(assignment: Assignment, indent: int = 0) -> str:
    """Emit an assignment in canonical form."""
    indent_str = "  " * indent
    value_str = emit_value(assignment.value)
    return f"{indent_str}{assignment.key}::{value_str}"


def emit_block(block: Block, indent: int = 0) -> str:
    """Emit a block in canonical form."""
    indent_str = "  " * indent
    lines = [f"{indent_str}{block.key}:"]

    # Emit children
    for child in block.children:
        if isinstance(child, Assignment):
            lines.append(emit_assignment(child, indent + 1))
        elif isinstance(child, Block):
            lines.append(emit_block(child, indent + 1))

    return "\n".join(lines)


def emit_meta(meta: dict[str, Any]) -> str:
    """Emit META block."""
    if not meta:
        return ""

    lines = ["META:"]
    for key, value in meta.items():
        value_str = emit_value(value)
        lines.append(f"  {key}::{value_str}")

    return "\n".join(lines)


def emit(doc: Document) -> str:
    """Emit canonical OCTAVE from AST.

    Args:
        doc: Document AST

    Returns:
        Canonical OCTAVE text with explicit envelope,
        unicode operators, and deterministic formatting
    """
    lines = []

    # Always emit explicit envelope
    lines.append(f"==={doc.name}===")

    # Emit META if present
    if doc.meta:
        lines.append(emit_meta(doc.meta))

    # Emit separator if present
    if doc.has_separator:
        lines.append("---")

    # Emit sections
    for section in doc.sections:
        if isinstance(section, Assignment):
            lines.append(emit_assignment(section, 0))
        elif isinstance(section, Block):
            lines.append(emit_block(section, 0))

    # Always emit END envelope
    lines.append("===END===")

    return "\n".join(lines)
