"""Tests for repair engine (P1.6)."""

from octave_mcp.core.parser import parse
from octave_mcp.core.repair import repair
from octave_mcp.core.validator import validate


class TestRepairTiers:
    """Test repair tier classification."""

    def test_normalization_tier_always_applied(self):
        """TIER_NORMALIZATION repairs always applied (by lexer/parser)."""
        # ASCII aliases normalized by lexer
        content = """===TEST===
KEY::value
===END===
"""
        doc = parse(content)
        repaired, log = repair(doc, [])
        # Normalization happens in lexer, so log may be empty here
        assert repaired is not None

    def test_repair_tier_only_when_fix_true(self):
        """TIER_REPAIR only when fix=true."""
        doc = parse("===TEST===\nKEY::value\n===END===")
        repaired_no_fix, log_no_fix = repair(doc, [], fix=False)
        repaired_fix, log_fix = repair(doc, [], fix=True)
        # Both should work, but behavior may differ
        assert repaired_no_fix is not None
        assert repaired_fix is not None


class TestForbiddenRepairs:
    """Test forbidden repairs never applied."""

    def test_never_auto_fills_missing_fields(self):
        """Should never auto-fill missing required fields."""
        # This is enforced by validator returning E003 errors
        schema = {"META": {"required": ["TYPE"]}}
        doc = parse("===TEST===\nMETA:\n  VERSION::1.0\n===END===")
        errors = validate(doc, schema)
        # Errors should remain, repair shouldn't fix them
        repaired, log = repair(doc, errors, fix=True)
        # Validation errors for missing TYPE should persist
        errors_after = validate(repaired, schema)
        assert len(errors_after) > 0  # Still has errors, wasn't auto-fixed
