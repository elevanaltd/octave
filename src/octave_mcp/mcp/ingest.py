"""MCP tool for OCTAVE ingest.

Stub for P2.2: octave_ingest_tool
"""


def ingest_tool(content: str, schema: str | None, tier: str, fix: bool, verbose: bool) -> dict:
    """MCP tool for octave.ingest.

    Args:
        content: OCTAVE content to ingest
        schema: Schema name for validation
        tier: Compression tier (LOSSLESS, CONSERVATIVE, AGGRESSIVE, ULTRA)
        fix: Apply TIER_REPAIR fixes
        verbose: Show pipeline stages

    Returns:
        Result with canonical, repairs[], warnings[], stages[]
    """
    raise NotImplementedError("P2.2: octave_ingest_tool")
