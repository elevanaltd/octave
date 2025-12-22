"""MCP tool for OCTAVE eject.

Stub for P2.3: octave_eject_tool
"""


def eject_tool(content: str | None, schema: str | None, mode: str, format: str) -> dict:
    """MCP tool for octave.eject.

    Args:
        content: OCTAVE content to eject (None for template generation)
        schema: Schema name for validation
        mode: Projection mode (canonical, authoring, executive, developer)
        format: Output format (octave, json, yaml, markdown)

    Returns:
        Result with output, lossy, fields_omitted[]
    """
    raise NotImplementedError("P2.3: octave_eject_tool")
