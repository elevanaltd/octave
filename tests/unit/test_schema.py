"""Tests for schema validation (P1.5)."""

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
