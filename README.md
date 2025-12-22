# OCTAVE MCP Server

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-178%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)]()

Production-ready MCP (Model Context Protocol) server implementing the **OCTAVE protocol** - a lenient-to-canonical pipeline for structured AI communication with schema validation.

## What is OCTAVE?

OCTAVE (Olympian Common Text And Vocabulary Engine) is a protocol for AI communication that achieves 3-20x token reduction while maintaining clarity through:

- **Structured syntax** using mythological vocabulary and precise operators
- **Lenient input** with deterministic normalization (ASCII aliases, flexible whitespace)
- **Schema validation** ensuring documents meet requirements
- **Projection modes** for different stakeholders (executive, developer, authoring, canonical)

See the [main OCTAVE repository](https://github.com/elevanaltd/octave) for full specification and philosophy.

## Features

This MCP server provides two core tools:

### `octave.ingest` - Bring information in safely
- Accepts lenient OCTAVE syntax (ASCII aliases like `->` for `→`)
- Normalizes to canonical Unicode format
- Validates against schema requirements
- Optional schema-driven repairs for common errors
- Returns canonical OCTAVE + detailed repair log

### `octave.eject` - Present information appropriately
- Generates tailored views from canonical OCTAVE
- Multiple projection modes (canonical, authoring, executive, developer)
- Multiple output formats (octave, json, yaml, markdown)
- Tracks lossy transformations for transparency

## Installation

### From PyPI (recommended)

```bash
pip install octave-mcp
```

### From source

```bash
git clone https://github.com/elevanaltd/octave.git
cd octave
pip install -e .
```

## Quick Start

### 1. Command-Line Interface

#### Ingest lenient OCTAVE to canonical

```bash
octave ingest document.oct.md --schema DECISION_LOG
```

#### Eject to different formats

```bash
octave eject document.oct.md --mode executive --format markdown
```

#### Validate against schema

```bash
octave validate document.oct.md --schema DECISION_LOG --strict
```

### 2. MCP Server for Claude Desktop

Configure the MCP server in your Claude Desktop settings:

```json
{
  "mcpServers": {
    "octave": {
      "command": "octave-mcp-server"
    }
  }
}
```

See [MCP Configuration Guide](docs/mcp-configuration.md) for detailed setup.

### 3. Python API

```python
from octave_mcp.core.parser import parse
from octave_mcp.core.emitter import emit
from octave_mcp.core.validator import validate

# Parse lenient OCTAVE
doc = parse(content)

# Validate against schema
errors = validate(doc, strict=True)

# Emit canonical OCTAVE
canonical = emit(doc)
```

## Architecture

The OCTAVE MCP server implements a **non-reasoning control plane** that separates mechanical syntax operations from semantic decisions:

```
REASONING MACHINE (LLM / human)
    │
    │  (decides meaning, importance, tier)
    ▼
OCTAVE CONTROL PLANE (non-reasoning)
    │
    │  (normalizes, validates, projects, routes, logs loss)
    ▼
CANONICAL ARTIFACTS + VIEWS
```

### Three-Tier Repair Classification

Every transformation is classified and logged:

#### TIER: NORMALIZATION (always-on)
- Syntactic and lexical only
- Examples: ASCII → Unicode (`->` → `→`), whitespace normalization
- Guarantee: Semantics preserved

#### TIER: REPAIR (opt-in via `fix=true`)
- Schema-bounded value transforms only
- Examples: Enum casefold, type coercion
- Guarantee: May change value, but not structure or meaning

#### TIER: FORBIDDEN (never automatic)
- Semantic intent and structure—never touched
- Examples: Target inference, missing field insertion, semantic rewriting
- Rationale: Schema constraints cannot tell you what the author intended

## Documentation

- **[Usage Guide](docs/usage.md)** - Detailed usage examples and workflows
- **[API Reference](docs/api.md)** - Complete API documentation
- **[MCP Configuration](docs/mcp-configuration.md)** - Setup guide for MCP clients
- **[OCTAVE Specification](https://github.com/elevanaltd/octave/tree/main/specs)** - Full protocol specification

## Development

### Setup development environment

```bash
# Clone and setup
git clone https://github.com/elevanaltd/octave.git
cd octave
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -e ".[dev]"
```

### Run tests

```bash
# Run full test suite (178 tests)
pytest

# Run with coverage report
pytest --cov=octave_mcp --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/properties/  # Property-based tests with Hypothesis
```

### Quality gates

```bash
# Type checking
mypy src

# Linting
ruff check src tests

# Code formatting
black --check src tests
```

### CI/CD

The project uses GitHub Actions for continuous integration:
- Python 3.11, 3.12, 3.13 matrix testing
- Full test suite with coverage reporting
- Type checking with mypy
- Linting with ruff
- Automated PyPI publishing on release tags

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for details.

## Examples

### Example 1: Decision Log

**Input (lenient OCTAVE):**
```octave
DECISION:
  ID::"DEC-001"
  STATUS::"approved"
  RATIONALE::"Performance improvement needed"
  ALTERNATIVES::[caching, optimization, horizontal scaling]
  CHOICE::"horizontal scaling"
```

**Output (canonical OCTAVE):**
```octave
DECISION:
  ID::"DEC-001"
  STATUS::APPROVED
  RATIONALE::"Performance improvement needed"
  ALTERNATIVES::[caching, optimization, horizontal_scaling]
  CHOICE::horizontal_scaling
```

### Example 2: MCP Tool Usage

```python
# Via MCP server (async)
result = await ingest_tool.execute(
    content=lenient_octave,
    schema="DECISION_LOG",
    fix=True,
    verbose=True
)

# Result includes:
# - canonical: Normalized OCTAVE
# - repair_log: List of all transformations
# - validation_errors: Any schema violations
```

### Example 3: Projection Modes

```python
# Executive view (high-level summary)
executive = await eject_tool.execute(
    content=canonical,
    schema="PROJECT_STATUS",
    mode="executive",
    format="markdown"
)
# Result: Status, risks, decisions only

# Developer view (implementation focus)
developer = await eject_tool.execute(
    content=canonical,
    schema="PROJECT_STATUS",
    mode="developer",
    format="octave"
)
# Result: Tests, CI, dependencies, technical detail
```

## Use Cases

### When to Use OCTAVE

- **Multi-agent systems** requiring deterministic, auditable communication
- **Knowledge artifacts** needing structured, queryable representations
- **High-density prompts** where context isn't in the code
- **Documentation** that must be both human-readable and machine-parsable

### When a Simple Prompt is Better

- **Interactive tasks** with full context in code
- **One-off requests** without audit requirements
- **Prototyping** where structure overhead isn't justified

See the [main README](https://github.com/elevanaltd/octave#readme) for detailed use case analysis.

## Core Syntax (v5.1.0)

**Structural operators:**
- `::` — Assignment (KEY::value)
- `:` — Block header (KEY: with indented children)

**Expression operators (Unicode canonical, ASCII alias):**
- `→` / `->` — Flow/sequence
- `⊕` / `+` — Synthesis (emergent combination)
- `⧺` / `~` — Concatenation (mechanical join)
- `⇌` / `vs` — Tension (binary opposition)
- `∨` / `|` — Alternative (choice)
- `∧` / `&` — Constraint (all required)
- `§` — Target reference

**Basic structure:**
```octave
KEY::VALUE                         # Assignment
NESTED:                            # Block with children
  CHILD::VALUE
LIST::[A, B, C]                    # Collection
FLOW::[START→BUILD→DEPLOY]         # Sequence
TENSION::Speed⇌Quality→Balance     # Trade-off with resolution
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all quality gates pass
5. Submit a pull request

## License

Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You are free to share and adapt this work with appropriate credit.

## Resources

- **[OCTAVE Specification](https://github.com/elevanaltd/octave/tree/main/specs)** - Full v5.1.0 specification
- **[Evidence & Evolution](https://github.com/elevanaltd/octave/tree/main/evidence)** - Compression data and case studies
- **[Quick Reference](https://github.com/elevanaltd/octave/blob/main/guides/llm-octave-quick-reference.oct.md)** - One-page guide
- **[MCP Protocol](https://modelcontextprotocol.io/)** - Model Context Protocol documentation

## Support

- **Issues:** [GitHub Issues](https://github.com/elevanaltd/octave/issues)
- **Discussions:** [GitHub Discussions](https://github.com/elevanaltd/octave/discussions)

---

**OCTAVE MCP Server** - Making AI communication deterministic, auditable, and efficient.
