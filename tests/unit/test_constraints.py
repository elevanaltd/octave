"""Tests for constraint chain evaluation (Gap 2).

Tests constraint parsing, evaluation, conflict detection, and error formatting.
Covers all 8 constraint types: REQ, OPT, CONST, ENUM, TYPE, REGEX, DIR, APPEND_ONLY.
"""

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
