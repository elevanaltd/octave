# OCTAVE MCP Server: Configurability Summary

**Quick Reference** | [Full Analysis](./configurability-analysis.md) | [ADR-001](./adr/001-configurability-and-modularity-architecture.md)

## TL;DR

**Question**: "If changing the rules in core means changing the code, is that correct?"

**Answer**: **YES** for grammar, **NO** for schemas.

- ✅ **Grammar is correctly hardcoded** (operators, repair tiers, error codes)
- 🔧 **Schemas need to be configurable** (currently too minimal)
- ❌ **Safety boundaries must never be configurable** (forbidden repairs)

## Design Principle: "Spec-Static, Schema-Dynamic"

### Spec-Static (Hardcoded) ✅
**These are CORRECT as-is**:
- Core operators: `→`, `⊕`, `⧺`, `⇌`, `∨`, `∧`, `§`
- ASCII aliases: `->`, `+`, `~`, `vs`, `|`, `&`, `#`
- Repair tiers: NORMALIZATION, REPAIR, FORBIDDEN
- Error codes: E001-E007
- Envelope format: `===NAME=== ... ===END===`

**Why**: These are part of the OCTAVE v5.1.0 language specification. All implementations must agree for interoperability.

### Schema-Dynamic (Configurable) 🔧
**These NEED improvement**:
- ❗ **Schema repository** (P0 - blocking production)
  - Load schemas from files/URLs
  - Schema versioning (SESSION_LOG@2.0)
  - Discovery and listing
- **Projection modes** (P1 - usability)
  - Schema-specific views
  - Custom stakeholder projections
- **Configuration system** (P1 - customization)
  - User and project-level config
  - Schema paths and registries

**Why**: Applications need domain-specific document types. Schemas define structure, not language syntax.

### Never Configurable ❌
**These MUST remain non-configurable**:
- Forbidden repair rules (target inference, field insertion)
- Operator precedence and associativity
- Envelope structure requirements

**Why**: Safety boundaries protect against semantic corruption and security issues.

## Critical Gap: Schema Repository

**Current State** (`src/octave_mcp/schemas/repository.py`):
```python
def __init__(self):
    self._schemas: dict[str, Schema] = {}
    # Future: Load builtin schemas from package
    # self._load_builtin_schemas()  # COMMENTED OUT
```

**What's Broken**:
- ❌ Can't load schemas from files
- ❌ Can't fetch schemas from URLs
- ❌ No schema discovery
- ❌ No versioning support
- ❌ Only one builtin schema (`meta.oct.md`)

**Real-World Impact**: Applications cannot define custom document types without code changes.

## Implementation Priority

### P0: Schema Repository (BLOCKING)
**Effort**: 2-3 days

**Required Features**:
- Load from files: `./schemas/*.oct.md`
- Load from URLs: `https://registry.example.com/schemas/`
- Schema discovery: list available schemas
- Versioning: `SESSION_LOG@2.0`
- Caching: avoid repeated fetches

**Example Config**:
```yaml
schemas:
  paths:
    - "./schemas"
    - "$HOME/.octave/schemas"
  registries:
    - url: "https://octave-schemas.example.com"
```

### P1: Projection Modes (IMPORTANT)
**Effort**: 2 days

**Current Problem**: Hardcoded in `projector.py`:
```python
elif mode == "executive":
    fields_omitted=["TESTS", "CI", "DEPS"]  # Wrong for all schemas
```

**Solution**: Schema-driven projections:
```yaml
# In schema document
projections:
  executive:
    include: ["STATUS", "RISKS", "DECISIONS"]
  developer:
    include: ["TESTS", "CI", "DEPS"]
```

### P1: Configuration System (CUSTOMIZATION)
**Effort**: 1-2 days

**Config File** (`.octave-mcp.yaml`):
```yaml
version: "1.0"

schemas:
  paths: ["./schemas"]
  registries: ["https://example.com"]

validation:
  strict_mode: true
  unknown_field_policy: "REJECT"

pipeline:
  default_fix: false
```

### P2: Compression Tiers (ENHANCEMENT)
**Effort**: 3-4 days

**Current**: Not implemented (reserved in code)
**Future**: Actual compression behavior per spec

## Key Architectural Insights

### 1. Grammar vs Structure
**Grammar** (language-level):
- How to write `A→B→C`
- What `⊕` means
- Operator precedence

**Structure** (document-level):
- What fields SESSION_LOG has
- What values are valid
- Where data routes to

**Only grammar should be hardcoded.**

### 2. Safety Boundaries
The three-tier repair system protects semantic integrity:
- **TIER_NORMALIZATION**: Always safe (syntax cleanup)
- **TIER_REPAIR**: Bounded safe (value fixes with schema)
- **TIER_FORBIDDEN**: Never safe (intent guessing)

**Making TIER_FORBIDDEN configurable would be a security vulnerability.**

### 3. Interoperability
Different OCTAVE implementations (Python, TypeScript, Rust) must agree on:
- ✅ What `→` means (flow operator)
- ✅ Operator precedence (`A⊕B→C` = `(A⊕B)→C`)
- ✅ Error code meanings
- ❌ What schemas exist (implementation-specific)

## Validation Strategy

### Property Tests
```python
# Spec-static invariants
assert canonicalize(canonicalize(x)) == canonicalize(x)
assert parse("A⊕B→C") == Sequence(Synthesis(A, B), C)

# Schema-dynamic invariants
assert file_loader.load("META") ≈ url_loader.load("META")
assert custom_schema_overrides_builtin()

# Safety boundaries
with pytest.raises(ValidationError):
    ingest(missing_required_field, fix=True)  # Never auto-fills
```

## Files Changed

**Documentation Created**:
- `/docs/adr/001-configurability-and-modularity-architecture.md` (full ADR)
- `/docs/configurability-analysis.md` (detailed analysis)
- `/docs/configurability-summary.md` (this file)

**Implementation Files Reviewed**:
- `src/octave_mcp/core/lexer.py` - Operators ✅
- `src/octave_mcp/core/parser.py` - Grammar ✅
- `src/octave_mcp/core/repair.py` - Repair tiers ✅
- `src/octave_mcp/core/validator.py` - Error codes ✅
- `src/octave_mcp/schemas/loader.py` - Needs work 🔧
- `src/octave_mcp/schemas/repository.py` - Needs work 🔧
- `src/octave_mcp/core/projector.py` - Needs work 🔧

## Next Steps

1. **Review ADR-001** with stakeholders
2. **Approve implementation roadmap**
3. **Start P0 work**: Schema repository enhancement
4. **Define builtin schemas**: SESSION_LOG, DECISION_LOG, etc.
5. **Write comprehensive tests** for configurability boundaries

## References

- [Full Analysis](./configurability-analysis.md) - Complete technical analysis
- [ADR-001](./adr/001-configurability-and-modularity-architecture.md) - Architecture decision record
- [OCTAVE Spec](../specs/octave-5-llm-core.oct.md) - Core specification
- [MCP Architecture](../specs/octave-mcp-architecture.oct.md) - Server architecture spec

---

**Bottom Line**: The current architecture is **fundamentally sound**. Grammar is correctly hardcoded. The main gap is schema management, which needs to be fully implemented to enable real-world use.
