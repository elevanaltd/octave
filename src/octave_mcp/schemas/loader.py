"""Schema loader (P1.11).

Parse .oct.md schema files into Schema objects for validator consumption.
"""

from pathlib import Path
from typing import Any

from octave_mcp.core.parser import parse


def load_schema(schema_path: str | Path) -> dict[str, Any]:
    """Load schema from .oct.md file.

    Args:
        schema_path: Path to schema file

    Returns:
        Schema dictionary for validator
    """
    with open(schema_path, "r") as f:
        content = f.read()

    # Parse schema document
    doc = parse(content)

    # Extract schema definition
    schema: dict[str, Any] = {}

    # Build schema from document structure
    # For minimal implementation, return basic structure
    if doc.meta:
        schema["META"] = {"fields": {}, "required": []}

        # Would normally parse FIELDS block here
        # For now, return minimal schema

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
