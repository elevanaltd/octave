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
        # DEFERRED: Implementation requires constraint evaluation infrastructure
        # See docs/implementation-roadmap.md Gap 2 (Constraint Chain Evaluation)
        # Estimated: 2-3 days, Phase 1 foundational work
        #
        # Once Gap 2 is complete, this will implement:
        # - Enum casefold: "active" → ACTIVE (only if unique match)
        # - Type coercion: "42" → 42 (if schema says NUMBER)
        # - Never add missing fields or invent targets (forbidden tier)
        pass

    # TIER_FORBIDDEN: Never automatic
    # These should remain as validation errors, never auto-fixed

    return doc, repair_log
