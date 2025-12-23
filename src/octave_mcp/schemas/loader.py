"""Schema loader (P1.11).

Parse .oct.md schema files into Schema objects for validator consumption.
"""

from pathlib import Path
from typing import Any

from octave_mcp.core.parser import parse


def load_schema(schema_path: str | Path) -> dict[str, Any]:
    """Load schema from .oct.md file.

    DEFERRED: Full schema loading requires holographic pattern parser.
    See docs/implementation-roadmap.md Gap 1 (Holographic Pattern Parsing).
    Estimated: 1-2 days, Phase 1 foundational work

    Once Gap 1 is complete, this will:
    - Parse holographic patterns: ["example"∧CONSTRAINT→§TARGET]
    - Extract constraint chains: REQ∧ENUM[A,B]∧REGEX["pattern"]
    - Build complete schema definition for validator
    - Support POLICY blocks with VERSION, UNKNOWN_FIELDS, TARGETS

    Current implementation: Returns minimal schema stub (META fields only)

    Args:
        schema_path: Path to schema file

    Returns:
        Schema dictionary for validator (minimal stub until Gap 1 complete)
    """
    with open(schema_path) as f:
        content = f.read()

    # Parse schema document
    doc = parse(content)

    # Extract schema definition
    schema: dict[str, Any] = {}

    # MINIMAL STUB: Return basic structure only
    # Cannot parse holographic patterns without Gap 1 infrastructure
    if doc.meta:
        schema["META"] = {"fields": {}, "required": []}

    return schema


def load_builtin_schemas() -> dict[str, dict[str, Any]]:
    """Load all builtin schemas.

    Returns:
        Dictionary of schema name -> schema definition
    """
    schemas = {}

    # Load META schema
    builtin_dir = Path(__file__).parent / "builtin"
    if (builtin_dir / "meta.oct.md").exists():
        schemas["META"] = load_schema(builtin_dir / "meta.oct.md")

    return schemas
