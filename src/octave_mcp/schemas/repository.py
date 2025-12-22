"""Schema repository with builtin and custom schema support (P2.5).

Provides centralized schema storage and retrieval.
"""

from octave_mcp.core.schema import Schema


class SchemaRepository:
    """Repository for OCTAVE schemas."""

    def __init__(self):
        """Initialize schema repository."""
        self._schemas: dict[str, Schema] = {}
        # Future: Load builtin schemas from package
        # self._load_builtin_schemas()

    def _load_builtin_schemas(self):
        """Load builtin schemas from package.

        Reserved for future implementation when builtin schemas are defined.
        """
        # TODO: Load from src/octave_mcp/schemas/builtin/
        pass

    def register(self, name: str, schema: Schema | None):
        """Register custom schema.

        Args:
            name: Schema name
            schema: Schema object (can be None for stub)
        """
        self._schemas[name] = schema  # type: ignore

    def get(self, name: str) -> Schema | None:
        """Retrieve schema by name.

        Args:
            name: Schema name

        Returns:
            Schema object or None if not found
        """
        return self._schemas.get(name)

    def list_schemas(self) -> list[str]:
        """List all available schema names.

        Returns:
            List of schema names
        """
        return list(self._schemas.keys())
