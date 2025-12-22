"""Tests for projection modes (P1.9)."""

from octave_mcp.core.parser import parse
from octave_mcp.core.projector import project


class TestProjectionModes:
    """Test projection modes."""

    def test_canonical_mode_not_lossy(self):
        """Canonical mode should not be lossy."""
        doc = parse("===TEST===\nKEY::value\n===END===")
        result = project(doc, "canonical")
        assert result.lossy is False
        assert len(result.fields_omitted) == 0

    def test_executive_mode_lossy(self):
        """Executive mode should be lossy."""
        doc = parse("===TEST===\nKEY::value\n===END===")
        result = project(doc, "executive")
        assert result.lossy is True

    def test_developer_mode_lossy(self):
        """Developer mode should be lossy."""
        doc = parse("===TEST===\nKEY::value\n===END===")
        result = project(doc, "developer")
        assert result.lossy is True
