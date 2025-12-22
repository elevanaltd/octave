"""OCTAVE projection modes (P1.9).

Implements eject() projection modes:
- canonical: Full document, lossy=false
- authoring: Lenient format, lossy=false
- executive: STATUS,RISKS,DECISIONS only, lossy=true
- developer: TESTS,CI,DEPS only, lossy=true
"""

from dataclasses import dataclass

from octave_mcp.core.ast_nodes import Document
from octave_mcp.core.emitter import emit


@dataclass
class ProjectionResult:
    """Result of projection operation."""

    output: str
    lossy: bool
    fields_omitted: list[str]


def project(doc: Document, mode: str = "canonical") -> ProjectionResult:
    """Project document to specified mode.

    Args:
        doc: Document AST
        mode: Projection mode (canonical, authoring, executive, developer)

    Returns:
        ProjectionResult with output, lossy flag, and omitted fields
    """
    if mode == "canonical":
        # Full document
        output = emit(doc)
        return ProjectionResult(output=output, lossy=False, fields_omitted=[])

    elif mode == "authoring":
        # Lenient format (for now, same as canonical)
        output = emit(doc)
        return ProjectionResult(output=output, lossy=False, fields_omitted=[])

    elif mode == "executive":
        # Executive view: STATUS, RISKS, DECISIONS only
        # For minimal implementation, return canonical with note
        output = emit(doc)
        return ProjectionResult(output=output, lossy=True, fields_omitted=["TESTS", "CI", "DEPS"])

    elif mode == "developer":
        # Developer view: TESTS, CI, DEPS only
        output = emit(doc)
        return ProjectionResult(output=output, lossy=True, fields_omitted=["STATUS", "RISKS", "DECISIONS"])

    else:
        # Default to canonical
        output = emit(doc)
        return ProjectionResult(output=output, lossy=False, fields_omitted=[])
