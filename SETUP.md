# OCTAVE MCP Server - Development Setup

## B0: Workspace Setup Complete ✅

This workspace has been prepared for OCTAVE MCP Server development following the BUILD-PLAN at `/Volumes/OCTAVE/octave/worktrees/octave-build/docs/workflow/build-plan.oct.md`.

## Quick Start

### 1. Activate Virtual Environment
```bash
source .venv/bin/activate
```

### 2. Verify Installation
```bash
# Check package imports
python -c "import octave_mcp; print(f'Version: {octave_mcp.__version__}')"

# Test CLI
python -m octave_mcp.cli.main --version
```

### 3. Run Quality Checks
```bash
# Linting
ruff check src/octave_mcp/

# Formatting
black --check src/octave_mcp/

# Type checking (when implementations added)
mypy src/octave_mcp/

# Tests
pytest
```

## Project Structure

```
/Volumes/OCTAVE/octave/worktrees/octave-build/
├── pyproject.toml              # Package configuration
├── src/octave_mcp/
│   ├── core/                   # Core parsing/validation (P1.2-P1.6)
│   │   ├── lexer.py           # ASCII normalization
│   │   ├── parser.py          # Envelope completion
│   │   ├── emitter.py         # Canonical emission
│   │   ├── schema.py          # Schema validation
│   │   └── repair.py          # Tier-based repairs
│   ├── cli/                    # Command-line interface (P1.7)
│   │   └── main.py            # ingest/eject/validate commands
│   ├── mcp/                    # MCP server tools (P2.1-P2.4)
│   │   ├── base_tool.py       # Base tool infrastructure
│   │   ├── ingest.py          # octave.ingest tool
│   │   ├── eject.py           # octave.eject tool
│   │   └── server.py          # MCP server entry point
│   └── schemas/                # Schema repository (P2.5)
│       ├── repository.py      # Schema loading/management
│       └── builtin/           # Built-in schema definitions
└── tests/
    ├── unit/                   # Unit tests
    ├── integration/            # Integration tests
    └── vectors/                # Test vector files
```

## Current Status

**Phase**: B0 - Workspace Setup
**Status**: COMPLETE ✅

All files created as minimal stubs with `NotImplementedError` placeholders referencing their BUILD-PLAN task IDs (e.g., "P1.2: lenient_lexer_with_ascii_normalization").

## Next Steps: B1 Implementation

Ready to begin implementation tasks according to BUILD-PLAN dependency order:

1. **P1.1**: ✅ COMPLETE - Project structure setup
2. **P1.2**: READY - Lenient lexer with ASCII normalization
3. **P1.3**: BLOCKED by P1.2 - Lenient parser with envelope completion
4. **P1.4**: BLOCKED by P1.3 - Canonical emitter
5. **P1.5**: BLOCKED by P1.4 - Schema validator
6. **P1.6**: BLOCKED by P1.5 - Repair engine

## Development Guidelines

### Adding New Code
- Follow TDD: Write tests first (RED → GREEN → REFACTOR)
- Update stub to real implementation
- Maintain type hints for mypy strict mode
- Keep functions focused and testable

### Quality Gates
All quality checks must pass before PR:
```bash
ruff check src tests
black --check src tests
mypy src
pytest
```

### Commit Messages
Follow conventional commits:
- `test: Add test for lexer ASCII normalization`
- `feat: Implement lenient lexer (P1.2)`
- `refactor: Extract normalization table`

## Reference Architecture

PAL MCP Server patterns: `/Volumes/HestAI-Tools/pal-mcp-server/`
OCTAVE Specifications: `/Volumes/OCTAVE/octave/worktrees/octave-build/specs/`

## Dependencies

- **Python**: >=3.11
- **MCP SDK**: >=1.0.0 (Anthropic official)
- **CLI**: click >=8.0.0
- **Validation**: pydantic >=2.0.0
- **Testing**: pytest, hypothesis
- **Quality**: ruff, black, mypy

---

*Workspace created following HestAI methodology - structural integrity over velocity*
