"""OCTAVE schema validator (P1.5).

Validates AST against schema definitions with:
- Required field checking
- Type validation
- Enum validation (with prefix matching and ambiguity detection)
- Regex pattern validation
- Unknown field detection
- Constraint chain evaluation
"""

from dataclasses import dataclass
from typing import Any

from octave_mcp.core.ast_nodes import ASTNode, Document
from octave_mcp.core.constraints import EnumConstraint


@dataclass
class ValidationError:
    """Validation error with context."""

    code: str
    message: str
    field_path: str = ""
    line: int = 0


class Validator:
    """OCTAVE AST validator."""

    def __init__(self, schema: dict[str, Any] | None = None):
        """Initialize validator with optional schema."""
        self.schema = schema or {}
        self.errors: list[ValidationError] = []

    def validate(self, doc: Document, strict: bool = False) -> list[ValidationError]:
        """Validate document against schema.

        Args:
            doc: Document AST
            strict: If True, reject unknown fields

        Returns:
            List of validation errors (empty if valid)
        """
        self.errors = []

        # Validate META if schema defines it
        if "META" in self.schema and doc.meta:
            self._validate_meta(doc.meta, strict)

        # Validate sections
        for section in doc.sections:
            self._validate_section(section, strict)

        return self.errors

    def _validate_meta(self, meta: dict[str, Any], strict: bool) -> None:
        """Validate META block."""
        schema_meta = self.schema.get("META", {})

        # Check required fields
        required = schema_meta.get("required", [])
        for field in required:
            if field not in meta:
                self.errors.append(
                    ValidationError(
                        code="E003",
                        message=f"Cannot auto-fill missing required field '{field}'. Author must provide value.",
                        field_path=f"META.{field}",
                    )
                )

        # Check unknown fields in strict mode
        if strict:
            allowed = schema_meta.get("fields", {}).keys()
            for field in meta.keys():
                if field not in allowed and allowed:
                    self.errors.append(
                        ValidationError(
                            code="E007",
                            message=f"Unknown field '{field}' not allowed in STRICT mode.",
                            field_path=f"META.{field}",
                        )
                    )

        # Type validation
        fields_schema = schema_meta.get("fields", {})
        for field, value in meta.items():
            if field in fields_schema:
                self._validate_type(field, value, fields_schema[field])

    def _validate_section(self, section: ASTNode, strict: bool) -> None:
        """Validate a section.

        DEFERRED: Section validation requires schema infrastructure.
        See docs/implementation-roadmap.md:
        - Gap 1: Holographic Pattern Parsing (1-2 days)
        - Gap 2: Constraint Chain Evaluation (2-3 days)
        - Gap 3: Target Routing & Validation (1-2 days)

        Total Phase 1: 3-4 weeks foundational work

        Once complete, this will validate:
        - Holographic patterns: ["example"∧CONSTRAINT→§TARGET]
        - Constraint chains: REQ∧ENUM[A,B]∧REGEX["^[a-z]+$"]
        - Target routing: →§INDEXER, →§META, etc.
        - Block inheritance: Children inherit parent targets
        """
        # Type narrowing: section is typically Assignment | Block from Document.sections
        pass

    def _validate_type(self, field: str, value: Any, field_schema: dict[str, Any]) -> None:
        """Validate value type and enum constraints."""
        expected_type = field_schema.get("type")
        if not expected_type:
            return

        # Handle ENUM type with constraint evaluation
        if expected_type == "ENUM":
            enum_values = field_schema.get("values", [])
            constraint = EnumConstraint(allowed_values=enum_values)
            result = constraint.evaluate(value, path=f"META.{field}")

            if not result.valid:
                for error in result.errors:
                    self.errors.append(
                        ValidationError(
                            code=error.code,
                            message=error.message,
                            field_path=error.path,
                        )
                    )
            return

        # Handle standard types
        # I1: Reject booleans for NUMBER type (bool inherits from int in Python)
        if expected_type == "NUMBER":
            if isinstance(value, bool):
                self.errors.append(
                    ValidationError(
                        code="E007",
                        message=f"Field '{field}' expected NUMBER, got {type(value).__name__}",
                        field_path=field,
                    )
                )
                return
            if not isinstance(value, int | float):
                self.errors.append(
                    ValidationError(
                        code="E007",
                        message=f"Field '{field}' expected NUMBER, got {type(value).__name__}",
                        field_path=field,
                    )
                )
            return

        # Handle other types
        type_map: dict[str, type | tuple[type, ...]] = {
            "STRING": str,
            "BOOLEAN": bool,
            "LIST": list,
        }

        expected_python_type = type_map.get(expected_type)
        if expected_python_type and not isinstance(value, expected_python_type):
            self.errors.append(
                ValidationError(
                    code="E007",  # I4: Use E007 for type errors (consistency with constraints.py)
                    message=f"Field '{field}' expected {expected_type}, got {type(value).__name__}",
                    field_path=field,
                )
            )


def validate(doc: Document, schema: dict[str, Any] | None = None, strict: bool = False) -> list[ValidationError]:
    """Validate document against schema.

    Args:
        doc: Document AST
        schema: Schema definition (optional)
        strict: Reject unknown fields if True

    Returns:
        List of validation errors
    """
    validator = Validator(schema)
    return validator.validate(doc, strict)
