"""OCTAVE repair engine with tier classification (P1.6).

Implements schema-driven repair with NORMALIZATION/REPAIR/FORBIDDEN tiers:
- TIER_NORMALIZATION: Always applied (ascii→unicode, whitespace, quotes, envelope)
- TIER_REPAIR: Only when fix=true (enum casefold, type coercion)
- TIER_FORBIDDEN: Always errors (no target inference, no field insertion)
"""

from octave_mcp.core.ast_nodes import Document
from octave_mcp.core.repair_log import RepairLog
from octave_mcp.core.validator import ValidationError


def repair(doc: Document, validation_errors: list[ValidationError], fix: bool = False) -> tuple[Document, RepairLog]:
    """Apply repairs based on tier classification.

    Args:
        doc: Parsed document AST
        validation_errors: Errors from validation
        fix: Whether to apply TIER_REPAIR fixes

    Returns:
        Tuple of (repaired document, repair log)
    """
    repair_log = RepairLog(repairs=[])

    # TIER_NORMALIZATION: Always applied (already handled by lexer/parser)
    # These are logged during parsing (ascii→unicode, whitespace, envelope)

    # TIER_REPAIR: Only when fix=true
    if fix:
        # Could implement enum casefold, type coercion here
        # For now, just return as-is
        pass

    # TIER_FORBIDDEN: Never automatic
    # These should remain as validation errors, never auto-fixed

    return doc, repair_log
