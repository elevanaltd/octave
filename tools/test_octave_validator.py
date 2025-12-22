#!/usr/bin/env python3
"""
Test suite for OCTAVE Validator v5.1.0 - Profiles and HestAI support

Tests validation profiles (protocol, hestai-agent, hestai-skill),
YAML frontmatter handling, and repository scanning mode.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add tools directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from octave-validator.py (hyphenated filename)
import importlib.util

spec = importlib.util.spec_from_file_location(
    "octave_validator", os.path.join(os.path.dirname(__file__), "octave-validator.py")
)
octave_validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(octave_validator)

OctaveValidator = octave_validator.OctaveValidator
validate_octave_document = octave_validator.validate_octave_document
validate_octave_file = octave_validator.validate_octave_file


def make_v4_doc(name, content, meta_type="test"):
    """Helper to create v4-compliant OCTAVE documents with META section."""
    return f"""==={name}===

META:
  TYPE::{meta_type}
  VERSION::"1.0"

{content}
===END==="""


class TestValidationProfiles(unittest.TestCase):
    """Test profile-based validation behavior."""

    def test_protocol_profile_strict_progression_operator(self):
        """Protocol profile should error on '->' outside lists."""
        doc = make_v4_doc("TEST", "FLOW::step1->step2->step3")
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertFalse(is_valid)
        self.assertTrue(any("Progression operator" in msg for msg in messages))

    def test_hestai_agent_profile_allows_progression_in_prose(self):
        """HestAI-agent profile should warn (not error) on '->' outside lists."""
        doc = make_v4_doc("TEST", "FLOW::step1->step2->step3")
        validator = OctaveValidator(profile="hestai-agent")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertTrue(is_valid)
        self.assertTrue(any("Progression operator" in msg for msg in messages))

    def test_hestai_skill_profile_allows_progression_in_prose(self):
        """HestAI-skill profile should warn (not error) on '->' outside lists."""
        doc = make_v4_doc("TEST", "FLOW::step1->step2->step3", meta_type="skill")
        validator = OctaveValidator(profile="hestai-skill")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertTrue(is_valid)
        self.assertTrue(any("Progression operator" in msg for msg in messages))

    def test_default_profile_is_protocol(self):
        """No profile specified should default to strict protocol validation."""
        doc = make_v4_doc("TEST", "FLOW::step1->step2->step3")
        validator = OctaveValidator()
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertFalse(is_valid)


class TestYAMLFrontmatter(unittest.TestCase):
    """Test YAML frontmatter handling for HestAI profiles."""

    def test_hestai_agent_skips_yaml_frontmatter(self):
        """HestAI-agent profile should skip YAML frontmatter validation."""
        doc = """---
name: test-agent
description: Test agent description
---

===AGENT===

META:
  TYPE::agent
  VERSION::"1.0"

ROLE::test
===END==="""
        validator = OctaveValidator(profile="hestai-agent")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertTrue(is_valid)

    def test_hestai_skill_skips_yaml_frontmatter(self):
        """HestAI-skill profile should skip YAML frontmatter validation."""
        doc = """---
name: test-skill
description: Test skill description
---

===SKILL===

META:
  TYPE::skill
  VERSION::"1.0"

PURPOSE::testing
===END==="""
        validator = OctaveValidator(profile="hestai-skill")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertTrue(is_valid)

    def test_protocol_profile_validates_yaml_frontmatter(self):
        """Protocol profile should validate YAML frontmatter as regular content."""
        doc = """---
name: test
---

===TEST===

META:
  TYPE::test
  VERSION::"1.0"

CONTENT::data
===END==="""
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        # Should error because --- is not a valid OCTAVE marker
        self.assertFalse(is_valid)


class TestHestAISkillValidation(unittest.TestCase):
    """Test HestAI-skill specific validation rules."""

    def test_validates_section_order_presence(self):
        """HestAI-skill profile should validate SECTION_ORDER exists."""
        doc = """---
name: test-skill
---

===SKILL===

META:
  TYPE::skill
  VERSION::"1.0"

@1::FIRST_SECTION
CONTENT::data

@2::SECOND_SECTION
MORE::data
===END==="""
        validator = OctaveValidator(profile="hestai-skill")
        is_valid, messages = validator.validate_octave_document(doc)
        # Should warn or error about missing SECTION_ORDER
        self.assertTrue(any("SECTION_ORDER" in msg for msg in messages))

    def test_validates_section_anchors(self):
        """HestAI-skill profile should validate @N section anchors."""
        doc = """---
name: test-skill
---

===SKILL===

META:
  TYPE::skill
  VERSION::"1.0"

SECTION_ORDER::[@1::FIRST, @2::SECOND]

@1::FIRST_SECTION
CONTENT::data

@2::SECOND_SECTION
MORE::data
===END==="""
        validator = OctaveValidator(profile="hestai-skill")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertTrue(is_valid)


class TestScanMode(unittest.TestCase):
    """Test directory scanning functionality."""

    def setUp(self):
        """Create temporary directory with test files."""
        self.temp_dir = tempfile.mkdtemp()

        # Valid file
        valid_path = Path(self.temp_dir) / "valid.oct.md"
        valid_path.write_text(make_v4_doc("VALID", "KEY::value"))

        # Invalid file
        invalid_path = Path(self.temp_dir) / "invalid.oct.md"
        invalid_path.write_text(
            """===INVALID===

META:
  TYPE::test
  VERSION::\"1.0\"

KEY = value
===END=="""
        )

        # Non-OCTAVE file (should be ignored)
        other_path = Path(self.temp_dir) / "readme.md"
        other_path.write_text("# Not an OCTAVE file")

    def tearDown(self):
        """Clean up temporary directory."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_scan_directory_finds_octave_files(self):
        """Scan mode should find all *.oct.md files."""
        scan_directory = octave_validator.scan_directory
        results = scan_directory(self.temp_dir)
        self.assertEqual(len(results), 2)

    def test_scan_directory_reports_per_file_results(self):
        """Scan mode should report validation result per file."""
        scan_directory = octave_validator.scan_directory
        results = scan_directory(self.temp_dir)

        valid_result = next((r for r in results if r["file"].endswith("/valid.oct.md")), None)
        invalid_result = next((r for r in results if r["file"].endswith("/invalid.oct.md")), None)

        self.assertIsNotNone(valid_result)
        self.assertIsNotNone(invalid_result)
        self.assertTrue(valid_result["valid"])
        self.assertFalse(invalid_result["valid"])

    def test_scan_directory_aggregates_results(self):
        """Scan mode should provide summary of passed/failed."""
        scan_directory = octave_validator.scan_directory
        format_scan_results = octave_validator.format_scan_results
        results = scan_directory(self.temp_dir)
        summary = format_scan_results(results)

        self.assertIn("1 passed", summary)
        self.assertIn("1 failed", summary)


class TestErrorConsistencyAcrossProfiles(unittest.TestCase):
    """Test that protocol integrity errors are ALWAYS errors, regardless of profile."""

    def test_tabs_always_error_protocol(self):
        """Tabs should be errors in protocol profile."""
        doc = make_v4_doc("TEST", "	KEY::value")
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertFalse(is_valid)
        self.assertTrue(any("Tab" in msg for msg in messages))

    def test_tabs_always_error_hestai_agent(self):
        """Tabs should be errors even in hestai-agent profile."""
        doc = make_v4_doc("TEST", "	KEY::value")
        validator = OctaveValidator(profile="hestai-agent")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertFalse(is_valid)
        self.assertTrue(any("Tab" in msg for msg in messages))

    def test_tabs_always_error_hestai_skill(self):
        """Tabs should be errors even in hestai-skill profile."""
        doc = make_v4_doc("TEST", "	KEY::value")
        validator = OctaveValidator(profile="hestai-skill")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertFalse(is_valid)
        self.assertTrue(any("Tab" in msg for msg in messages))

    def test_missing_markers_always_error_all_profiles(self):
        """Missing ===MARKERS=== should error in all profiles."""
        doc = "KEY::value"
        for profile in ["protocol", "hestai-agent", "hestai-skill"]:
            validator = OctaveValidator(profile=profile)
            is_valid, messages = validator.validate_octave_document(doc)
            self.assertFalse(is_valid, f"Expected error for missing markers in {profile} profile")
            self.assertTrue(any("marker" in msg.lower() for msg in messages))


class TestWarningVsErrorBehavior(unittest.TestCase):
    """Test that warnings don't affect validity but errors do."""

    def test_warnings_only_document_is_valid(self):
        """Document with only warnings should be valid=True."""
        doc = make_v4_doc(
            "TEST",
            """KEY::value
_old_unicode_→_operator""",
        )
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertTrue(is_valid)  # Valid despite warnings
        self.assertTrue(len(validator.warnings) > 0)  # But has warnings
        self.assertEqual(len(validator.errors), 0)

    def test_errors_make_document_invalid(self):
        """Document with errors should be valid=False."""
        doc = make_v4_doc(
            "TEST",
            """KEY::value
	tabbed_line::bad""",
        )
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertFalse(is_valid)
        self.assertTrue(len(validator.errors) > 0)

    def test_hestai_profile_progression_warning_is_valid(self):
        """HestAI profile with -> warning should still be valid=True."""
        doc = make_v4_doc("TEST", "FLOW::step1->step2")
        validator = OctaveValidator(profile="hestai-agent")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertTrue(is_valid)  # Valid despite progression warning
        self.assertTrue(any("Progression operator" in msg for msg in messages))


class TestFileErrorHandling(unittest.TestCase):
    """Test error handling for file I/O issues."""

    def test_missing_file_returns_error_message(self):
        """Missing file should return error message."""
        result = validate_octave_file("/tmp/does_not_exist_12345.oct.md")
        self.assertIn("File error", result)

    def test_missing_file_result_indicates_failure(self):
        """Missing file should be treated as validation failure."""
        result = validate_octave_file("/tmp/does_not_exist_12345.oct.md")
        # Should contain error indication for proper exit code handling
        self.assertTrue("Error" in result or "error" in result)


class TestMultilineListContext(unittest.TestCase):
    """Test that -> inside multiline lists is correctly recognized."""

    def test_progression_in_multiline_list_is_valid(self):
        """Progression operator in multiline list should be valid."""
        doc = make_v4_doc(
            "TEST",
            """FLOW::[
  step1->step2,
  step3->step4
]""",
        )
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        # Should be valid - progression is inside list structure
        self.assertTrue(is_valid, f"Expected multiline list with -> to be valid, got: {messages}")

    def test_progression_in_single_line_list_is_valid(self):
        """Progression operator in single-line list should be valid (baseline)."""
        doc = make_v4_doc("TEST", "FLOW::[step1->step2->step3]")
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertTrue(is_valid)


class TestBackwardCompatibility(unittest.TestCase):
    """Test that existing behavior is preserved."""

    def test_validate_octave_document_function_unchanged(self):
        """Module-level function should work as before."""
        doc = make_v4_doc("TEST", "KEY::value")
        result = validate_octave_document(doc)
        self.assertIn("valid", result.lower())

    def test_validate_octave_file_function_unchanged(self):
        """File validation function should work as before."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".oct.md", delete=False) as f:
            f.write(make_v4_doc("TEST", "KEY::value"))
            temp_path = f.name

        try:
            result = validate_octave_file(temp_path)
            self.assertIn("valid", result.lower())
        finally:
            os.unlink(temp_path)

    def test_cli_default_behavior_preserved(self):
        """CLI without flags should validate single file strictly."""
        # This will be tested via integration test
        pass


class TestOCTAVEv5Features(unittest.TestCase):
    """Test OCTAVE v5.1.0 specific features."""

    def test_constraint_chaining_inside_brackets_valid(self):
        """Constraint operator & chaining inside brackets should be valid."""
        doc = make_v4_doc(
            "TEST",
            """CONFIG::[
  "value"&REQ&REGEX->§TARGET
]""",
        )
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertTrue(is_valid, f"Expected & chaining inside brackets to be valid, got: {messages}")

    def test_constraint_outside_brackets_invalid(self):
        """Constraint operator & outside brackets should be invalid."""
        doc = make_v4_doc("TEST", """VALUE::"test"&REQ&REGEX""")
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        self.assertFalse(is_valid)
        self.assertTrue(any("Constraint operator" in msg for msg in messages))

    def test_plus_chaining_now_allowed(self):
        """Plus operator + chaining should be allowed in v5.0.3."""
        doc = make_v4_doc("TEST", """COMBO::A+B+C""")
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        # v5.1.0 allows chaining, so no error expected
        self.assertTrue(is_valid, f"Expected A+B+C to be valid in v5.1.0, got: {messages}")

    def test_inline_maps_valid(self):
        """Inline maps [k::v,k2::v2] should be valid."""
        doc = make_v4_doc("TEST", """CONFIG::[name::"test",version::"1.0"]""")
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        # Should be valid - inline map syntax
        self.assertTrue(is_valid, f"Expected inline map to be valid, got: {messages}")

    def test_empty_block_valid(self):
        """Empty block KEY: with no children should be valid."""
        doc = make_v4_doc(
            "TEST",
            """EMPTY:
NEXT_KEY::value""",
        )
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        # Should be valid - empty blocks allowed in v5.1.0
        self.assertTrue(is_valid, f"Expected empty block to be valid, got: {messages}")

    def test_block_inheritance_with_target(self):
        """Block inheritance BLOCK[->§TARGET]: with children should be valid."""
        doc = make_v4_doc(
            "TEST",
            """INHERITED[->§BASE]:
  CHILD::value""",
        )
        validator = OctaveValidator(profile="protocol")
        is_valid, messages = validator.validate_octave_document(doc)
        # Should be valid - block inheritance with target
        self.assertTrue(is_valid, f"Expected block inheritance to be valid, got: {messages}")


if __name__ == "__main__":
    unittest.main()
