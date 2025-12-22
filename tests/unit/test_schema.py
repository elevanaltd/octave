"""Tests for schema validation (P1.5)."""

import pytest

from octave_mcp.core.parser import parse
from octave_mcp.core.validator import validate


class TestRequiredFields:
    """Test required field validation."""

    def test_errors_on_missing_required_field(self):
        """Should error on missing required fields."""
        schema = {
            "META": {
                "required": ["TYPE", "VERSION"],
                "fields": {
                    "TYPE": {"type": "STRING"},
                    "VERSION": {"type": "STRING"},
                },
            }
        }

        content = """===TEST===
META:
  TYPE::TEST_DOC
===END===
"""
        doc = parse(content)
        errors = validate(doc, schema)
        assert len(errors) > 0
        assert any("VERSION" in e.message for e in errors)
        assert any(e.code == "E003" for e in errors)


class TestTypeValidation:
    """Test type checking."""

    def test_validates_string_type(self):
        """Should validate STRING type."""
        schema = {"META": {"fields": {"TYPE": {"type": "STRING"}}}}

        content = """===TEST===
META:
  TYPE::TEST_DOC
===END===
"""
        doc = parse(content)
        errors = validate(doc, schema)
        # TYPE is a string, should pass
        type_errors = [e for e in errors if "TYPE" in e.field_path and "expected" in e.message]
        assert len(type_errors) == 0


class TestUnknownFields:
    """Test unknown field detection."""

    def test_strict_mode_rejects_unknown_fields(self):
        """Should error on unknown fields in strict mode."""
        schema = {"META": {"fields": {"TYPE": {"type": "STRING"}}}}

        content = """===TEST===
META:
  TYPE::TEST_DOC
  UNKNOWN_FIELD::value
===END===
"""
        doc = parse(content)
        errors = validate(doc, schema, strict=True)
        assert len(errors) > 0
        assert any("UNKNOWN_FIELD" in e.message for e in errors)
        assert any(e.code == "E007" for e in errors)

    def test_lenient_mode_allows_unknown_fields(self):
        """Should allow unknown fields in lenient mode."""
        schema = {"META": {"fields": {"TYPE": {"type": "STRING"}}}}

        content = """===TEST===
META:
  TYPE::TEST_DOC
  UNKNOWN_FIELD::value
===END===
"""
        doc = parse(content)
        errors = validate(doc, schema, strict=False)
        unknown_errors = [e for e in errors if "UNKNOWN_FIELD" in e.message]
        assert len(unknown_errors) == 0  # Lenient mode allows unknown fields


class TestEnumValidation:
    """Test enum validation (E006)."""

    @pytest.mark.skip(reason="E006: Enum validation not implemented yet (P1.5)")
    def test_errors_on_ambiguous_enum_match(self):
        """Should error when multiple enum values match (E006)."""
        schema = {
            "META": {
                "fields": {
                    "STATUS": {
                        "type": "ENUM",
                        "values": ["ACTIVE", "ARCHIVED", "ACTIVATING"],
                    }
                }
            }
        }

        content = """===TEST===
META:
  TYPE::TEST_DOC
  STATUS::ACTIV
===END===
"""
        doc = parse(content)
        errors = validate(doc, schema)
        # Should error because "ACTIV" matches both "ACTIVE" and "ACTIVATING"
        assert len(errors) > 0
        assert any(e.code == "E006" for e in errors)
        assert any("ambiguous" in e.message.lower() for e in errors)

    @pytest.mark.skip(reason="E006: Enum validation not implemented yet (P1.5)")
    def test_allows_unambiguous_enum_match(self):
        """Should allow unambiguous partial enum match."""
        schema = {
            "META": {
                "fields": {
                    "STATUS": {
                        "type": "ENUM",
                        "values": ["ACTIVE", "ARCHIVED"],
                    }
                }
            }
        }

        content = """===TEST===
META:
  TYPE::TEST_DOC
  STATUS::ACT
===END===
"""
        doc = parse(content)
        errors = validate(doc, schema)
        # Should succeed because "ACT" only matches "ACTIVE"
        status_errors = [e for e in errors if "STATUS" in e.field_path]
        assert len(status_errors) == 0
