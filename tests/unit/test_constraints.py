"""Tests for constraint chain evaluation (Gap 2).

Tests constraint parsing, evaluation, conflict detection, and error formatting.
Covers all 8 constraint types: REQ, OPT, CONST, ENUM, TYPE, REGEX, DIR, APPEND_ONLY.
"""

import pytest

from octave_mcp.core.constraints import (
    AppendOnlyConstraint,
    ConstConstraint,
    ConstraintChain,
    DirConstraint,
    EnumConstraint,
    OptionalConstraint,
    RegexConstraint,
    RequiredConstraint,
    TypeConstraint,
    ValidationError,
    ValidationResult,
)


class TestRequiredConstraint:
    """Test REQ constraint."""

    def test_required_accepts_non_empty_value(self):
        """REQ should accept non-None, non-empty values."""
        constraint = RequiredConstraint()
        result = constraint.evaluate("value")
        assert result.valid is True
        assert len(result.errors) == 0

    def test_required_rejects_none(self):
        """REQ should reject None."""
        constraint = RequiredConstraint()
        result = constraint.evaluate(None)
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].constraint == "REQ"

    def test_required_rejects_empty_string(self):
        """REQ should reject empty string."""
        constraint = RequiredConstraint()
        result = constraint.evaluate("")
        assert result.valid is False
        assert len(result.errors) == 1


class TestOptionalConstraint:
    """Test OPT constraint."""

    def test_optional_accepts_none(self):
        """OPT should accept None."""
        constraint = OptionalConstraint()
        result = constraint.evaluate(None)
        assert result.valid is True

    def test_optional_accepts_value(self):
        """OPT should accept non-None values."""
        constraint = OptionalConstraint()
        result = constraint.evaluate("value")
        assert result.valid is True


class TestConstConstraint:
    """Test CONST[X] constraint."""

    def test_const_accepts_exact_match(self):
        """CONST[X] should accept value == X."""
        constraint = ConstConstraint(const_value="ACTIVE")
        result = constraint.evaluate("ACTIVE")
        assert result.valid is True

    def test_const_rejects_different_value(self):
        """CONST[X] should reject value != X."""
        constraint = ConstConstraint(const_value="ACTIVE")
        result = constraint.evaluate("INACTIVE")
        assert result.valid is False
        assert len(result.errors) == 1
        assert "ACTIVE" in result.errors[0].expected

    def test_const_type_matters(self):
        """CONST[1] should distinguish "1" from 1."""
        constraint = ConstConstraint(const_value=1)
        result = constraint.evaluate("1")
        assert result.valid is False

    def test_const_parses_quoted_string(self):
        """CONST["ACTIVE"] should parse and match "ACTIVE" (I2 fix)."""
        chain = ConstraintChain.parse('CONST["ACTIVE"]')
        result = chain.evaluate("ACTIVE")
        assert result.valid is True

    def test_const_parses_boolean_true(self):
        """CONST[true] should parse and match True (I2 fix)."""
        chain = ConstraintChain.parse("CONST[true]")
        result = chain.evaluate(True)
        assert result.valid is True

    def test_const_parses_boolean_false(self):
        """CONST[false] should parse and match False (I2 fix)."""
        chain = ConstraintChain.parse("CONST[false]")
        result = chain.evaluate(False)
        assert result.valid is True

    def test_const_parses_null(self):
        """CONST[null] should parse and match None (I2 fix)."""
        chain = ConstraintChain.parse("CONST[null]")
        result = chain.evaluate(None)
        assert result.valid is True

    def test_const_parses_scientific_notation(self):
        """CONST[1e10] should parse and match 1e10 (I2 fix)."""
        chain = ConstraintChain.parse("CONST[1e10]")
        result = chain.evaluate(1e10)
        assert result.valid is True

    def test_const_parses_negative_number(self):
        """CONST[-5] should parse and match -5 (I2 fix)."""
        chain = ConstraintChain.parse("CONST[-5]")
        result = chain.evaluate(-5)
        assert result.valid is True


class TestEnumConstraint:
    """Test ENUM[a,b,c] constraint."""

    def test_enum_accepts_exact_match(self):
        """ENUM[A,B] should accept exact match."""
        constraint = EnumConstraint(allowed_values=["ACTIVE", "ARCHIVED"])
        result = constraint.evaluate("ACTIVE")
        assert result.valid is True

    def test_enum_accepts_unambiguous_prefix(self):
        """ENUM[ACTIVE,ARCHIVED] should accept unambiguous prefix 'ACT'."""
        constraint = EnumConstraint(allowed_values=["ACTIVE", "ARCHIVED"])
        result = constraint.evaluate("ACT")
        assert result.valid is True

    def test_enum_rejects_ambiguous_prefix(self):
        """ENUM[ACTIVE,ACTIVATING] should reject ambiguous prefix 'ACTIV'."""
        constraint = EnumConstraint(allowed_values=["ACTIVE", "ACTIVATING"])
        result = constraint.evaluate("ACTIV")
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "E006"
        assert "ambiguous" in result.errors[0].message.lower()

    def test_enum_rejects_no_match(self):
        """ENUM[A,B] should reject value not matching any."""
        constraint = EnumConstraint(allowed_values=["ACTIVE", "ARCHIVED"])
        result = constraint.evaluate("DELETED")
        assert result.valid is False

    def test_enum_case_sensitive(self):
        """ENUM should be case-sensitive by default."""
        constraint = EnumConstraint(allowed_values=["ACTIVE"])
        result = constraint.evaluate("active")
        assert result.valid is False

    def test_enum_parses_quoted_strings(self):
        """ENUM["A","B"] should parse and match "A" (I2 fix)."""
        chain = ConstraintChain.parse('ENUM["ACTIVE","ARCHIVED"]')
        result = chain.evaluate("ACTIVE")
        assert result.valid is True


class TestTypeConstraint:
    """Test TYPE(X) constraint."""

    def test_type_accepts_string(self):
        """TYPE(STRING) should accept str."""
        constraint = TypeConstraint(expected_type="STRING")
        result = constraint.evaluate("hello")
        assert result.valid is True

    def test_type_rejects_wrong_string(self):
        """TYPE(STRING) should reject int."""
        constraint = TypeConstraint(expected_type="STRING")
        result = constraint.evaluate(123)
        assert result.valid is False

    def test_type_accepts_number_int(self):
        """TYPE(NUMBER) should accept int."""
        constraint = TypeConstraint(expected_type="NUMBER")
        result = constraint.evaluate(42)
        assert result.valid is True

    def test_type_accepts_number_float(self):
        """TYPE(NUMBER) should accept float."""
        constraint = TypeConstraint(expected_type="NUMBER")
        result = constraint.evaluate(3.14)
        assert result.valid is True

    def test_type_accepts_boolean(self):
        """TYPE(BOOLEAN) should accept bool."""
        constraint = TypeConstraint(expected_type="BOOLEAN")
        result = constraint.evaluate(True)
        assert result.valid is True

    def test_type_accepts_list(self):
        """TYPE(LIST) should accept list."""
        constraint = TypeConstraint(expected_type="LIST")
        result = constraint.evaluate([1, 2, 3])
        assert result.valid is True

    def test_type_number_rejects_boolean_true(self):
        """TYPE(NUMBER) should reject True (I1 fix)."""
        constraint = TypeConstraint(expected_type="NUMBER")
        result = constraint.evaluate(True)
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].constraint == "TYPE"

    def test_type_number_rejects_boolean_false(self):
        """TYPE(NUMBER) should reject False (I1 fix)."""
        constraint = TypeConstraint(expected_type="NUMBER")
        result = constraint.evaluate(False)
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].constraint == "TYPE"


class TestRegexConstraint:
    """Test REGEX[pattern] constraint."""

    def test_regex_accepts_match(self):
        """REGEX should accept matching pattern."""
        constraint = RegexConstraint(pattern=r"^[a-z]+$")
        result = constraint.evaluate("hello")
        assert result.valid is True

    def test_regex_rejects_non_match(self):
        """REGEX should reject non-matching pattern."""
        constraint = RegexConstraint(pattern=r"^[a-z]+$")
        result = constraint.evaluate("Hello123")
        assert result.valid is False

    def test_regex_handles_complex_pattern(self):
        """REGEX should handle complex patterns."""
        constraint = RegexConstraint(pattern=r"^\d{4}-\d{2}-\d{2}$")
        result = constraint.evaluate("2024-12-23")
        assert result.valid is True

    def test_regex_compiles_once(self):
        """REGEX should compile pattern once and reuse."""
        constraint = RegexConstraint(pattern=r"^test$")
        # Verify it has a compiled pattern
        assert hasattr(constraint, "_compiled") or hasattr(constraint, "compiled_pattern")


class TestDirConstraint:
    """Test DIR constraint."""

    def test_dir_accepts_valid_path(self):
        """DIR should accept valid directory path format."""
        constraint = DirConstraint()
        result = constraint.evaluate("./path/to/dir")
        assert result.valid is True

    def test_dir_accepts_absolute_path(self):
        """DIR should accept absolute paths."""
        constraint = DirConstraint()
        result = constraint.evaluate("/absolute/path")
        assert result.valid is True

    def test_dir_rejects_invalid_characters(self):
        """DIR should reject paths with invalid characters."""
        constraint = DirConstraint()
        result = constraint.evaluate("path/with/\0/null")
        assert result.valid is False


class TestAppendOnlyConstraint:
    """Test APPEND_ONLY constraint."""

    def test_append_only_accepts_list(self):
        """APPEND_ONLY should accept list values."""
        constraint = AppendOnlyConstraint()
        result = constraint.evaluate([1, 2, 3])
        assert result.valid is True

    def test_append_only_rejects_non_list(self):
        """APPEND_ONLY should reject non-list values."""
        constraint = AppendOnlyConstraint()
        result = constraint.evaluate("not a list")
        assert result.valid is False


class TestConstraintChain:
    """Test constraint chain parsing and evaluation."""

    def test_parse_single_constraint(self):
        """Should parse single constraint."""
        chain = ConstraintChain.parse("REQ")
        assert len(chain.constraints) == 1
        assert isinstance(chain.constraints[0], RequiredConstraint)

    def test_parse_chain_with_and_operator(self):
        """Should parse constraint chain with ∧."""
        chain = ConstraintChain.parse("REQ∧TYPE(STRING)")
        assert len(chain.constraints) == 2
        assert isinstance(chain.constraints[0], RequiredConstraint)
        assert isinstance(chain.constraints[1], TypeConstraint)

    def test_parse_enum_with_values(self):
        """Should parse ENUM[A,B,C]."""
        chain = ConstraintChain.parse("ENUM[ACTIVE,ARCHIVED,DELETED]")
        assert len(chain.constraints) == 1
        constraint = chain.constraints[0]
        assert isinstance(constraint, EnumConstraint)
        assert constraint.allowed_values == ["ACTIVE", "ARCHIVED", "DELETED"]

    def test_parse_const_with_value(self):
        """Should parse CONST[X]."""
        chain = ConstraintChain.parse("CONST[FIXED_VALUE]")
        assert len(chain.constraints) == 1
        constraint = chain.constraints[0]
        assert isinstance(constraint, ConstConstraint)
        assert constraint.const_value == "FIXED_VALUE"

    def test_parse_regex_with_pattern(self):
        """Should parse REGEX[pattern]."""
        chain = ConstraintChain.parse('REGEX["^[a-z]+$"]')
        assert len(chain.constraints) == 1
        constraint = chain.constraints[0]
        assert isinstance(constraint, RegexConstraint)
        assert constraint.pattern == "^[a-z]+$"

    def test_parse_complex_chain(self):
        """Should parse complex constraint chain."""
        chain = ConstraintChain.parse('REQ∧ENUM[A,B]∧REGEX["^[A-Z]+$"]')
        assert len(chain.constraints) == 3

    def test_evaluate_all_pass(self):
        """Should pass when all constraints pass."""
        chain = ConstraintChain.parse("REQ∧TYPE(STRING)")
        result = chain.evaluate("hello")
        assert result.valid is True

    def test_evaluate_fails_fast(self):
        """Should fail fast on first constraint failure."""
        chain = ConstraintChain.parse("REQ∧TYPE(STRING)∧REGEX[^[0-9]+$]")
        result = chain.evaluate(None)  # Fails on REQ
        assert result.valid is False
        # Should only have error from REQ, not from TYPE or REGEX
        assert len(result.errors) == 1
        assert result.errors[0].constraint == "REQ"

    def test_evaluate_stops_at_first_failure(self):
        """Should not evaluate remaining constraints after failure."""
        chain = ConstraintChain.parse("TYPE(NUMBER)∧CONST[42]")
        result = chain.evaluate("not a number")  # Fails on TYPE
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].constraint == "TYPE"


class TestConflictDetection:
    """Test constraint conflict detection."""

    def test_detects_req_opt_conflict(self):
        """Should detect REQ∧OPT conflict."""
        chain = ConstraintChain.parse("REQ∧OPT")
        conflicts = chain.detect_conflicts()
        assert len(conflicts) > 0
        assert any("REQ" in str(c) and "OPT" in str(c) for c in conflicts)

    def test_detects_enum_const_conflict(self):
        """Should detect ENUM[A,B]∧CONST[C] conflict."""
        chain = ConstraintChain.parse("ENUM[ACTIVE,ARCHIVED]∧CONST[DELETED]")
        conflicts = chain.detect_conflicts()
        assert len(conflicts) > 0

    def test_detects_const_const_conflict(self):
        """Should detect CONST[X]∧CONST[Y] conflict."""
        chain = ConstraintChain.parse("CONST[A]∧CONST[B]")
        conflicts = chain.detect_conflicts()
        assert len(conflicts) > 0

    def test_no_conflict_enum_const_overlap(self):
        """Should NOT conflict when ENUM[A,B]∧CONST[A]."""
        chain = ConstraintChain.parse("ENUM[ACTIVE,ARCHIVED]∧CONST[ACTIVE]")
        conflicts = chain.detect_conflicts()
        assert len(conflicts) == 0

    def test_no_conflict_compatible_constraints(self):
        """Should not detect conflicts in compatible chain."""
        chain = ConstraintChain.parse("REQ∧TYPE(STRING)∧REGEX[^[a-z]+$]")
        conflicts = chain.detect_conflicts()
        assert len(conflicts) == 0

    def test_evaluate_enforces_req_opt_conflict(self):
        """evaluate() should fail when REQ∧OPT conflict exists (I3 fix)."""
        chain = ConstraintChain.parse("REQ∧OPT")
        result = chain.evaluate("value")
        assert result.valid is False
        assert len(result.errors) > 0

    def test_evaluate_enforces_const_const_conflict(self):
        """evaluate() should fail when CONST[X]∧CONST[Y] conflict exists (I3 fix)."""
        chain = ConstraintChain.parse("CONST[A]∧CONST[B]")
        result = chain.evaluate("A")
        assert result.valid is False
        assert len(result.errors) > 0

    def test_evaluate_enforces_enum_const_conflict(self):
        """evaluate() should fail when ENUM[A,B]∧CONST[C] conflict exists (I3 fix)."""
        chain = ConstraintChain.parse("ENUM[ACTIVE,ARCHIVED]∧CONST[DELETED]")
        result = chain.evaluate("DELETED")
        assert result.valid is False
        assert len(result.errors) > 0


class TestValidationResult:
    """Test ValidationResult structure."""

    def test_valid_result_has_no_errors(self):
        """Valid result should have empty error list."""
        result = ValidationResult(valid=True, errors=[])
        assert result.valid is True
        assert len(result.errors) == 0

    def test_invalid_result_has_errors(self):
        """Invalid result should have error list."""
        error = ValidationError(
            code="E001",
            path="field.subfield",
            constraint="REQ",
            expected="non-empty value",
            got="None",
            message="Field is required",
        )
        result = ValidationResult(valid=False, errors=[error])
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "E001"


class TestRangeConstraint:
    """Test RANGE[min,max] constraint."""

    def test_range_accepts_value_in_bounds(self):
        """RANGE[1,10] should accept value within bounds."""
        from octave_mcp.core.constraints import RangeConstraint

        constraint = RangeConstraint(min_value=1, max_value=10)
        result = constraint.evaluate(5)
        assert result.valid is True

    def test_range_accepts_min_boundary(self):
        """RANGE[1,10] should accept min boundary (inclusive)."""
        from octave_mcp.core.constraints import RangeConstraint

        constraint = RangeConstraint(min_value=1, max_value=10)
        result = constraint.evaluate(1)
        assert result.valid is True

    def test_range_accepts_max_boundary(self):
        """RANGE[1,10] should accept max boundary (inclusive)."""
        from octave_mcp.core.constraints import RangeConstraint

        constraint = RangeConstraint(min_value=1, max_value=10)
        result = constraint.evaluate(10)
        assert result.valid is True

    def test_range_rejects_below_min(self):
        """RANGE[1,10] should reject value below min."""
        from octave_mcp.core.constraints import RangeConstraint

        constraint = RangeConstraint(min_value=1, max_value=10)
        result = constraint.evaluate(0)
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "E011"

    def test_range_rejects_above_max(self):
        """RANGE[1,10] should reject value above max."""
        from octave_mcp.core.constraints import RangeConstraint

        constraint = RangeConstraint(min_value=1, max_value=10)
        result = constraint.evaluate(11)
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "E011"

    def test_range_supports_negative_range(self):
        """RANGE[-50,50] should support negative ranges."""
        from octave_mcp.core.constraints import RangeConstraint

        constraint = RangeConstraint(min_value=-50, max_value=50)
        result = constraint.evaluate(-25)
        assert result.valid is True

    def test_range_supports_float_values(self):
        """RANGE[0.0,1.0] should support float values."""
        from octave_mcp.core.constraints import RangeConstraint

        constraint = RangeConstraint(min_value=0.0, max_value=1.0)
        result = constraint.evaluate(0.5)
        assert result.valid is True

    def test_range_edge_case_min_equals_max(self):
        """RANGE[5,5] should only accept exact value."""
        from octave_mcp.core.constraints import RangeConstraint

        constraint = RangeConstraint(min_value=5, max_value=5)
        assert constraint.evaluate(5).valid is True
        assert constraint.evaluate(4).valid is False
        assert constraint.evaluate(6).valid is False

    def test_range_parsing_integers(self):
        """RANGE[1,10] should parse from string."""
        chain = ConstraintChain.parse("RANGE[1,10]")
        assert chain.evaluate(5).valid is True
        assert chain.evaluate(0).valid is False

    def test_range_parsing_floats(self):
        """RANGE[0.0,100.0] should parse float bounds."""
        chain = ConstraintChain.parse("RANGE[0.0,100.0]")
        assert chain.evaluate(50.5).valid is True

    def test_range_parsing_negative(self):
        """RANGE[-50,50] should parse negative bounds."""
        chain = ConstraintChain.parse("RANGE[-50,50]")
        assert chain.evaluate(-25).valid is True

    def test_range_to_string(self):
        """RangeConstraint.to_string() should return RANGE[min,max]."""
        from octave_mcp.core.constraints import RangeConstraint

        constraint = RangeConstraint(min_value=1, max_value=10)
        assert constraint.to_string() == "RANGE[1,10]"


class TestMaxLengthConstraint:
    """Test MAX_LENGTH[N] constraint."""

    def test_max_length_accepts_string_within_limit(self):
        """MAX_LENGTH[5] should accept string with length <= 5."""
        from octave_mcp.core.constraints import MaxLengthConstraint

        constraint = MaxLengthConstraint(max_length=5)
        assert constraint.evaluate("abc").valid is True
        assert constraint.evaluate("abcde").valid is True

    def test_max_length_rejects_string_exceeding_limit(self):
        """MAX_LENGTH[5] should reject string with length > 5."""
        from octave_mcp.core.constraints import MaxLengthConstraint

        constraint = MaxLengthConstraint(max_length=5)
        result = constraint.evaluate("abcdef")
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "E012"

    def test_max_length_accepts_list_within_limit(self):
        """MAX_LENGTH[3] should accept list with length <= 3."""
        from octave_mcp.core.constraints import MaxLengthConstraint

        constraint = MaxLengthConstraint(max_length=3)
        assert constraint.evaluate([1, 2]).valid is True
        assert constraint.evaluate([1, 2, 3]).valid is True

    def test_max_length_rejects_list_exceeding_limit(self):
        """MAX_LENGTH[3] should reject list with length > 3."""
        from octave_mcp.core.constraints import MaxLengthConstraint

        constraint = MaxLengthConstraint(max_length=3)
        result = constraint.evaluate([1, 2, 3, 4])
        assert result.valid is False
        assert result.errors[0].code == "E012"

    def test_max_length_accepts_empty_string(self):
        """MAX_LENGTH[5] should accept empty string."""
        from octave_mcp.core.constraints import MaxLengthConstraint

        constraint = MaxLengthConstraint(max_length=5)
        assert constraint.evaluate("").valid is True

    def test_max_length_parsing(self):
        """MAX_LENGTH[100] should parse from string."""
        chain = ConstraintChain.parse("MAX_LENGTH[100]")
        assert chain.evaluate("short").valid is True

    def test_max_length_to_string(self):
        """MaxLengthConstraint.to_string() should return MAX_LENGTH[N]."""
        from octave_mcp.core.constraints import MaxLengthConstraint

        constraint = MaxLengthConstraint(max_length=100)
        assert constraint.to_string() == "MAX_LENGTH[100]"


class TestMinLengthConstraint:
    """Test MIN_LENGTH[N] constraint."""

    def test_min_length_accepts_string_meeting_minimum(self):
        """MIN_LENGTH[3] should accept string with length >= 3."""
        from octave_mcp.core.constraints import MinLengthConstraint

        constraint = MinLengthConstraint(min_length=3)
        assert constraint.evaluate("abc").valid is True
        assert constraint.evaluate("abcd").valid is True

    def test_min_length_rejects_string_below_minimum(self):
        """MIN_LENGTH[3] should reject string with length < 3."""
        from octave_mcp.core.constraints import MinLengthConstraint

        constraint = MinLengthConstraint(min_length=3)
        result = constraint.evaluate("ab")
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "E013"

    def test_min_length_accepts_list_meeting_minimum(self):
        """MIN_LENGTH[2] should accept list with length >= 2."""
        from octave_mcp.core.constraints import MinLengthConstraint

        constraint = MinLengthConstraint(min_length=2)
        assert constraint.evaluate([1, 2]).valid is True
        assert constraint.evaluate([1, 2, 3]).valid is True

    def test_min_length_rejects_list_below_minimum(self):
        """MIN_LENGTH[2] should reject list with length < 2."""
        from octave_mcp.core.constraints import MinLengthConstraint

        constraint = MinLengthConstraint(min_length=2)
        result = constraint.evaluate([1])
        assert result.valid is False
        assert result.errors[0].code == "E013"

    def test_min_length_zero_always_passes(self):
        """MIN_LENGTH[0] should always pass (like OPT for length)."""
        from octave_mcp.core.constraints import MinLengthConstraint

        constraint = MinLengthConstraint(min_length=0)
        assert constraint.evaluate("").valid is True
        assert constraint.evaluate([]).valid is True

    def test_min_length_parsing(self):
        """MIN_LENGTH[1] should parse from string."""
        chain = ConstraintChain.parse("MIN_LENGTH[1]")
        assert chain.evaluate("a").valid is True
        assert chain.evaluate("").valid is False

    def test_min_length_to_string(self):
        """MinLengthConstraint.to_string() should return MIN_LENGTH[N]."""
        from octave_mcp.core.constraints import MinLengthConstraint

        constraint = MinLengthConstraint(min_length=1)
        assert constraint.to_string() == "MIN_LENGTH[1]"


class TestDateConstraint:
    """Test DATE/ISO8601 constraint."""

    def test_date_accepts_yyyy_mm_dd(self):
        """DATE should accept YYYY-MM-DD format."""
        from octave_mcp.core.constraints import DateConstraint

        constraint = DateConstraint()
        assert constraint.evaluate("2025-01-15").valid is True

    def test_iso8601_accepts_full_datetime(self):
        """ISO8601 should accept full datetime with time."""
        from octave_mcp.core.constraints import Iso8601Constraint

        constraint = Iso8601Constraint()
        assert constraint.evaluate("2025-01-15T10:30:00").valid is True

    def test_iso8601_accepts_datetime_with_z(self):
        """ISO8601 should accept datetime with Z timezone."""
        from octave_mcp.core.constraints import Iso8601Constraint

        constraint = Iso8601Constraint()
        assert constraint.evaluate("2025-01-15T10:30:00Z").valid is True

    def test_date_rejects_invalid_format(self):
        """DATE should reject invalid date format."""
        from octave_mcp.core.constraints import DateConstraint

        constraint = DateConstraint()
        result = constraint.evaluate("not-a-date")
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "E014"

    def test_date_rejects_invalid_date_values(self):
        """DATE should reject invalid date values like month 13."""
        from octave_mcp.core.constraints import DateConstraint

        constraint = DateConstraint()
        result = constraint.evaluate("2025-13-01")
        assert result.valid is False
        assert result.errors[0].code == "E014"

    def test_date_parsing(self):
        """DATE should parse from string."""
        chain = ConstraintChain.parse("DATE")
        assert chain.evaluate("2025-01-15").valid is True
        assert chain.evaluate("invalid").valid is False

    def test_date_rejects_datetime(self):
        """DATE should reject full datetime, only accept YYYY-MM-DD."""
        chain = ConstraintChain.parse("DATE")
        # DATE only accepts YYYY-MM-DD
        assert chain.evaluate("2025-01-15").valid is True
        assert chain.evaluate("2025-01-15T10:30:00").valid is False
        assert chain.evaluate("2025-01-15T10:30:00Z").valid is False

    def test_iso8601_accepts_datetime(self):
        """ISO8601 should accept full datetime formats."""
        chain = ConstraintChain.parse("ISO8601")
        assert chain.evaluate("2025-01-15").valid is True  # Date only
        assert chain.evaluate("2025-01-15T10:30:00").valid is True  # Datetime
        assert chain.evaluate("2025-01-15T10:30:00Z").valid is True  # With Z

    def test_date_to_string(self):
        """DateConstraint.to_string() should return DATE."""
        from octave_mcp.core.constraints import DateConstraint

        constraint = DateConstraint()
        assert constraint.to_string() == "DATE"

    def test_iso8601_to_string(self):
        """Iso8601Constraint.to_string() should return ISO8601."""
        from octave_mcp.core.constraints import Iso8601Constraint

        constraint = Iso8601Constraint()
        assert constraint.to_string() == "ISO8601"


class TestErrorFormatting:
    """Test error message formatting."""

    def test_error_contains_path(self):
        """Error should include field path."""
        constraint = RequiredConstraint()
        result = constraint.evaluate(None, path="META.VERSION")
        assert result.errors[0].path == "META.VERSION"

    def test_error_contains_constraint_type(self):
        """Error should identify which constraint failed."""
        constraint = TypeConstraint(expected_type="NUMBER")
        result = constraint.evaluate("not a number")
        assert result.errors[0].constraint == "TYPE"

    def test_error_message_is_descriptive(self):
        """Error message should be human-readable."""
        constraint = EnumConstraint(allowed_values=["A", "B", "C"])
        result = constraint.evaluate("D")
        message = result.errors[0].message
        assert "D" in message
        assert any(val in message for val in ["A", "B", "C"])

    def test_missing_required_field_uses_e003(self):
        """Missing required field should use E003 (I4 fix)."""
        constraint = RequiredConstraint()
        result = constraint.evaluate(None)
        assert result.errors[0].code == "E003"

    def test_type_constraint_violation_uses_e007(self):
        """Type constraint violation should use E007, not E003 (I4 fix)."""
        constraint = TypeConstraint(expected_type="NUMBER")
        result = constraint.evaluate("not a number")
        assert result.errors[0].code == "E007"

    def test_error_codes_are_distinct(self):
        """E003 and E007 must be used for different purposes (I4 fix)."""
        req_constraint = RequiredConstraint()
        req_result = req_constraint.evaluate(None)

        type_constraint = TypeConstraint(expected_type="STRING")
        type_result = type_constraint.evaluate(123)

        assert req_result.errors[0].code != type_result.errors[0].code
        assert req_result.errors[0].code == "E003"
        assert type_result.errors[0].code == "E007"


class TestMalformedParameterValidation:
    """Tests for parse-time validation of constraint parameters."""

    def test_max_length_rejects_non_integer(self):
        """MAX_LENGTH[abc] should raise ValueError at parse time."""
        with pytest.raises(ValueError, match="non-negative integer"):
            ConstraintChain.parse("MAX_LENGTH[abc]")

    def test_max_length_rejects_negative(self):
        """MAX_LENGTH[-1] should raise ValueError at parse time."""
        with pytest.raises(ValueError, match="non-negative integer"):
            ConstraintChain.parse("MAX_LENGTH[-1]")

    def test_max_length_rejects_float(self):
        """MAX_LENGTH[3.5] should raise ValueError (must be int)."""
        with pytest.raises(ValueError, match="non-negative integer"):
            ConstraintChain.parse("MAX_LENGTH[3.5]")

    def test_min_length_rejects_non_integer(self):
        """MIN_LENGTH[abc] should raise ValueError at parse time."""
        with pytest.raises(ValueError, match="non-negative integer"):
            ConstraintChain.parse("MIN_LENGTH[abc]")

    def test_min_length_rejects_negative(self):
        """MIN_LENGTH[-1] should raise ValueError at parse time."""
        with pytest.raises(ValueError, match="non-negative integer"):
            ConstraintChain.parse("MIN_LENGTH[-1]")

    def test_range_rejects_non_numeric_min(self):
        """RANGE[abc,10] should raise ValueError at parse time."""
        with pytest.raises(ValueError, match="numeric bounds"):
            ConstraintChain.parse("RANGE[abc,10]")

    def test_range_rejects_non_numeric_max(self):
        """RANGE[0,xyz] should raise ValueError at parse time."""
        with pytest.raises(ValueError, match="numeric bounds"):
            ConstraintChain.parse("RANGE[0,xyz]")

    def test_range_rejects_missing_comma(self):
        """RANGE[10] should raise ValueError (needs two values)."""
        with pytest.raises(ValueError, match="two values"):
            ConstraintChain.parse("RANGE[10]")

    def test_range_rejects_min_greater_than_max(self):
        """RANGE[10,5] should raise ValueError (min > max)."""
        with pytest.raises(ValueError, match="min must be <= max"):
            ConstraintChain.parse("RANGE[10,5]")

    def test_range_accepts_equal_min_max(self):
        """RANGE[5,5] should be valid (exact value constraint)."""
        chain = ConstraintChain.parse("RANGE[5,5]")
        assert chain.evaluate(5).valid
        assert not chain.evaluate(4).valid

    def test_range_rejects_boolean(self):
        """RANGE should reject boolean values (bool is subclass of int)."""
        chain = ConstraintChain.parse("RANGE[0,1]")
        assert not chain.evaluate(True).valid
        assert not chain.evaluate(False).valid
        # But actual numbers should work
        assert chain.evaluate(0).valid
        assert chain.evaluate(1).valid

    def test_max_length_rejects_dict(self):
        """MAX_LENGTH should only accept str/list, not dict."""
        chain = ConstraintChain.parse("MAX_LENGTH[5]")
        assert not chain.evaluate({"a": 1, "b": 2}).valid
        assert chain.evaluate([1, 2, 3]).valid  # List is OK
        assert chain.evaluate("abc").valid  # String is OK

    def test_max_length_rejects_set(self):
        """MAX_LENGTH should only accept str/list, not set."""
        chain = ConstraintChain.parse("MAX_LENGTH[5]")
        assert not chain.evaluate({1, 2, 3}).valid

    def test_min_length_rejects_tuple(self):
        """MIN_LENGTH should only accept str/list, not tuple."""
        chain = ConstraintChain.parse("MIN_LENGTH[1]")
        assert not chain.evaluate((1, 2, 3)).valid
