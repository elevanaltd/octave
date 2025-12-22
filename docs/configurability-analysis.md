# OCTAVE MCP Server: Configurability and Modularity Analysis

**Date**: 2025-12-22
**Author**: Technical Architect
**Working Directory**: `/Volumes/OCTAVE/octave/worktrees/octave-build`

## Executive Summary

The OCTAVE MCP Server correctly hardcodes core grammar and operators as these are part of the OCTAVE v5.1.0 language specification. However, schema management and projection modes need significant improvement to enable real-world extensibility.

**Key Finding**: The architecture follows the correct principle of **"Spec-Static, Schema-Dynamic"** - grammar rules should be hardcoded for interoperability, but schema repositories and projection modes should be configurable for extensibility.

## Analysis Overview

### Specifications Reviewed
1. `specs/octave-5-llm-core.oct.md` - Core grammar (v5.1.0)
2. `specs/octave-5-llm-data.oct.md` - Compression tiers
3. `specs/octave-5-llm-schema.oct.md` - Schema definitions
4. `specs/octave-5-llm-execution.oct.md` - Validation and debugging
5. `specs/octave-mcp-architecture.oct.md` - MCP server architecture

### Implementation Reviewed
1. `src/octave_mcp/core/lexer.py` - Tokenization with ASCII aliases
2. `src/octave_mcp/core/parser.py` - AST construction
3. `src/octave_mcp/core/repair.py` - Repair tier classification
4. `src/octave_mcp/core/validator.py` - Schema validation
5. `src/octave_mcp/core/projector.py` - Projection modes
6. `src/octave_mcp/schemas/loader.py` - Schema loading (minimal)
7. `src/octave_mcp/schemas/repository.py` - Schema repository (minimal)

## Key Question: "If changing the rules in core means changing the code, is that correct?"

**Answer**: **YES** for core grammar, **NO** for schemas and projections.

### Why This Dichotomy Exists

#### Part 1: Core Grammar SHOULD Be Hardcoded

The OCTAVE specification defines a formal language with:
- **Operators**: `→`, `⊕`, `⧺`, `⇌`, `∨`, `∧`, `§` with defined precedence
- **ASCII Aliases**: `->`, `+`, `~`, `vs`, `|`, `&`, `#` with normalization rules
- **Structural Rules**: Envelope markers, indentation, META block placement
- **Repair Tiers**: NORMALIZATION (always), REPAIR (opt-in), FORBIDDEN (never)

**These are language features, not configuration options.**

**Analogy**: Just as Python doesn't let you configure what `def` means or JavaScript doesn't let you change operator precedence, OCTAVE grammar rules are part of the language definition.

**Evidence from Spec** (`octave-mcp-architecture.oct.md` §1):
```
CORE_PRINCIPLE::one_language_disciplined_tolerance

DEFINITION::[
  ONE_LANGUAGE::OCTAVE[single_spec,single_canonical_form],
  DISCIPLINED_TOLERANCE::finite_rewrite_system[not_inference]
]

LITMUS_TEST::"If you removed the LLM and replaced it with a dumb text emitter,
              would this system still add value?"→YES
```

The spec explicitly states that OCTAVE is deterministic, not probabilistic. Grammar rules must be static to ensure all implementations agree.

#### Part 2: Schemas and Projections SHOULD Be Configurable

Schemas define **document types** (SESSION_LOG, DECISION_LOG, etc.), not the OCTAVE language itself.

**Current Limitation**: The schema repository is minimally implemented:

```python
# src/octave_mcp/schemas/repository.py (current state)
class SchemaRepository:
    def __init__(self):
        self._schemas: dict[str, Schema] = {}
        # Future: Load builtin schemas from package
        # self._load_builtin_schemas()  # COMMENTED OUT

    def register(self, name: str, schema: Schema | None):
        """Register custom schema."""
        self._schemas[name] = schema  # type: ignore

    def get(self, name: str) -> Schema | None:
        """Retrieve schema by name."""
        return self._schemas.get(name)
```

**This blocks real-world usage** because:
1. Applications need custom schemas for their domains
2. No way to load schemas from files or URLs
3. No schema discovery mechanism
4. No versioning support

**Evidence from Spec** (`octave-5-llm-schema.oct.md` §6):
```
§6::SCHEMA_SKELETON
// Minimal valid schema document structure
TEMPLATE:
  ===MY_SCHEMA===
  META:
    TYPE::PROTOCOL_DEFINITION
    VERSION::"1.0"
```

The spec shows schemas are **documents** with their own versioning, implying they should be loadable and extensible.

## What's Hardcoded vs What Should Be Configurable

### ✅ CORRECTLY HARDCODED (Spec-Static)

#### 1. Operators and ASCII Aliases
**Location**: `src/octave_mcp/core/lexer.py` lines 79-87

```python
ASCII_ALIASES = {
    "->": "→",
    "+": "⊕",
    "~": "⧺",
    "vs": "⇌",
    "|": "∨",
    "&": "∧",
    "#": "§",
}
```

**Spec Reference**: `octave-5-llm-core.oct.md` §2::OPERATORS
```
§2::OPERATORS
// LAYER 2: EXPRESSION (inside values, precedence applies)
EXPRESSION:
  PREC::UNICODE::ASCII::SEMANTIC::USAGE::ASSOC
  1    []       []     container   [a,b,c]                   n/a
  2    ⧺        ~      concat      A⧺B[mechanical_join]      left
  3    ⊕        +      synthesis   A⊕B[emergent_whole]       left
  4    ⇌        vs     tension     A⇌B[binary_opposition]    none[binary_only]
```

**Verdict**: ✅ **Correct** - These are language-level definitions. Changing them would create incompatible OCTAVE dialects.

#### 2. Repair Tier Classification
**Location**: `src/octave_mcp/core/repair.py` (structure, not full implementation yet)

```python
# TIER_NORMALIZATION: Always applied (already handled by lexer/parser)
# TIER_REPAIR: Only when fix=true
# TIER_FORBIDDEN: Never automatic
```

**Spec Reference**: `octave-mcp-architecture.oct.md` §5::REPAIR_CLASSIFICATION
```
TIER_FORBIDDEN[never_automatic]:
  SCOPE::semantic_intent_and_structure
  EXAMPLES::[
    target_inference[never_guess→§TARGET],
    field_insertion[never_add_missing_REQ_fields],
    semantic_rewrite[never_change_meaning]
  ]

FORBIDDEN_RATIONALE::[
  "Schema constraints cannot tell you which missing field the author intended",
  "Autocorrect is safe for syntax, bounded for values, dangerous for intent"
]
```

**Verdict**: ✅ **Correct** - The three-tier system is a safety boundary. Making it configurable would allow bypassing semantic protections.

#### 3. Error Codes
**Location**: `src/octave_mcp/core/validator.py`, `src/octave_mcp/core/lexer.py`

```python
# lexer.py line 70
error_code: str = "E005"

# validator.py lines 66-71
ValidationError(
    code="E003",
    message=f"Cannot auto-fill missing required field '{field}'. Author must provide value.",
    field_path=f"META.{field}",
)
```

**Spec Reference**: `octave-mcp-architecture.oct.md` §8::ERROR_MESSAGES
```
E001::"Single colon assignment not allowed. Use KEY::value (double colon)."::
  "OCTAVE uses :: for assignment because : is the block operator. This prevents ambiguity."

E003::"Cannot auto-fill missing required field '{field}'. Author must provide value."::
  "Required fields represent author intent. The system cannot guess what you meant."
```

**Verdict**: ✅ **Correct** - Standard error codes enable cross-implementation tooling (IDE extensions, CI/CD, GitHub Actions). Error messages include educational rationale which is part of the spec.

#### 4. Envelope Structure
**Location**: `src/octave_mcp/core/parser.py` lines 78-85

```python
# Check for explicit envelope
if self.current().type == TokenType.ENVELOPE_START:
    token = self.advance()
    doc.name = token.value
else:
    # Infer envelope for single doc
    doc.name = "INFERRED"
```

**Spec Reference**: `octave-5-llm-core.oct.md` §1::ENVELOPE
```
§1::ENVELOPE
START::===NAME===[first_line,exact_match]
END::===END===[last_line,exact_match,mandatory]
ASSEMBLY::when_profiles_concatenated[core+schema+data]→only_final_===END===_terminates
```

**Verdict**: ✅ **Correct** - Envelope format is part of the OCTAVE document structure. This enables file discovery, concatenation, and tooling.

### 🔧 NEEDS IMPROVEMENT (Schema-Dynamic)

#### 1. Schema Repository - **CRITICAL GAP**
**Location**: `src/octave_mcp/schemas/loader.py`, `src/octave_mcp/schemas/repository.py`

**Current State**:
```python
# loader.py
def load_builtin_schemas() -> dict[str, dict[str, Any]]:
    """Load all builtin schemas."""
    schemas = {}
    builtin_dir = Path(__file__).parent / "builtin"
    if (builtin_dir / "meta.oct.md").exists():
        schemas["META"] = load_schema(builtin_dir / "meta.oct.md")
    return schemas  # Only returns META schema
```

**What's Missing**:
1. **No file-based loading**: Can't load schemas from custom directories
2. **No URL loading**: Can't fetch schemas from remote registries
3. **No schema discovery**: Can't list available schemas
4. **No versioning**: Can't specify schema versions (e.g., SESSION_LOG v2.0)
5. **No caching**: Remote schemas would be fetched every time
6. **Minimal builtin schemas**: Only `meta.oct.md` exists

**Real-World Impact**:
- Applications can't define custom document types
- No way to share schemas across projects
- Schema evolution is impossible
- Testing with custom schemas requires code changes

**Required Implementation**:
```python
class SchemaRepository:
    def __init__(self, config: SchemaConfig):
        # Load from multiple sources: builtin, filesystem, URLs
        self.loaders: list[SchemaLoader] = [
            BuiltinSchemaLoader(),
            FileSchemaLoader(config.custom_paths),
            URLSchemaLoader(config.registries, config.cache_dir)
        ]

    def get(self, name: str, version: str | None = None) -> Schema:
        """Get schema with optional version."""
        for loader in self.loaders:
            try:
                return loader.load(name, version)
            except SchemaNotFoundError:
                continue
        raise SchemaNotFoundError(f"Schema '{name}' not found")
```

**Priority**: **P0** - Blocking for production use

#### 2. Projection Modes - **RIGIDITY ISSUE**
**Location**: `src/octave_mcp/core/projector.py` lines 45-54

**Current State**:
```python
elif mode == "executive":
    # Executive view: STATUS, RISKS, DECISIONS only
    output = emit(doc)
    return ProjectionResult(
        output=output,
        lossy=True,
        fields_omitted=["TESTS", "CI", "DEPS"]  # Hardcoded
    )
```

**What's Wrong**:
- Projection modes are hardcoded for a hypothetical document schema
- Different schemas need different projection modes
- Stakeholders may want custom views
- Field list doesn't actually filter (just emits full doc with note)

**Real-World Example**:
```yaml
# SESSION_LOG schema might define:
projections:
  executive:
    include: ["SESSION_ID", "STATUS", "PHASE", "BLOCKERS", "RISKS"]
  developer:
    include: ["SESSION_ID", "TESTS", "BUILD", "LINT", "COVERAGE"]

# DECISION_LOG schema might define:
projections:
  executive:
    include: ["DECISION_ID", "OUTCOME", "STAKEHOLDERS", "IMPACT"]
  technical:
    include: ["DECISION_ID", "RATIONALE", "ALTERNATIVES", "TRADEOFFS"]
```

**Required Implementation**:
```python
# Projection modes defined in schema document
class Schema:
    name: str
    version: str
    fields: dict[str, FieldSchema]
    projections: dict[str, ProjectionMode]  # NEW

class ProjectionMode:
    name: str
    include_fields: list[str] | Literal["*"]
    exclude_fields: list[str]
    lossy: bool
```

**Priority**: **P1** - Important for usability

#### 3. Compression Tiers - **NOT IMPLEMENTED**
**Location**: `src/octave_mcp/mcp/ingest.py` line 82 (commented out)

**Current State**:
```python
# tier = params.get("tier", "LOSSLESS")  # Reserved for future compression levels
```

**What's Missing**:
- Compression tier behavior is defined in spec but not implemented
- No actual compression happens (only normalization)
- Future work for presentation optimization

**Spec Reference**: `octave-5-llm-data.oct.md` §1b::COMPRESSION_TIERS

**Priority**: **P2** - Enhancement, not blocking

### ❌ SHOULD NEVER BE CONFIGURABLE (Safety Boundaries)

#### 1. Forbidden Repair Rules
**Why**: These protect against semantic corruption and security issues.

**Examples**:
- Never infer routing targets (`→§TARGET`)
- Never insert missing required fields
- Never guess schema from content
- Never change semantic meaning

**Spec Reference**: `octave-mcp-architecture.oct.md` §5::FORBIDDEN_RATIONALE
```
"Schema constraints cannot tell you whether a target was malicious or mistaken"
"Schema constraints cannot tell you whether dropping/adding a field changes downstream meaning"
```

#### 2. Core Grammar Precedence
**Why**: Operator precedence must be consistent across all implementations.

**Example**: `A⊕B→C` must always parse as `(A⊕B)→C` (synthesis binds tighter than flow).

#### 3. Envelope Format
**Why**: File discovery, concatenation, and tooling depend on standard structure.

## Architectural Recommendation

### Design Principle: "Spec-Static, Schema-Dynamic"

**STATIC (Hardcoded in Python)**:
- Core grammar (operators, precedence, associativity)
- Repair tier classification system
- Error codes and educational messages
- Envelope markers and structural rules

**DYNAMIC (Loaded from Configuration/Schemas)**:
- Schema definitions (document types)
- Projection modes (stakeholder views)
- Custom validation rules (domain-specific)
- Compression tier behavior (presentation)

### Configuration Architecture

**Proposed Structure**:
```yaml
# ~/.octave/config.yaml (user-level)
# or .octave-mcp.yaml (project-level)

version: "1.0"

schemas:
  builtin: true
  paths:
    - "./schemas"
    - "$HOME/.octave/schemas"
  registries:
    - url: "https://octave-schemas.example.com"
      cache: true

validation:
  strict_mode: true
  unknown_field_policy: "REJECT"  # REJECT, WARN, or IGNORE

pipeline:
  default_fix: false
  verbose_logging: false
```

**Implementation Files Needed**:
1. `src/octave_mcp/config.py` - Configuration loading and validation
2. `src/octave_mcp/schemas/loaders/` - File, URL, builtin loaders
3. Enhanced `src/octave_mcp/schemas/repository.py` - Multi-source schema management
4. Enhanced `src/octave_mcp/core/projector.py` - Schema-driven projections

## Implementation Roadmap

### Phase 1: Schema Repository (P0)
**Goal**: Enable loading schemas from files and URLs

**Tasks**:
1. Create `SchemaConfig` class for configuration
2. Implement `FileSchemaLoader` for local schemas
3. Implement `URLSchemaLoader` with caching
4. Enhance `SchemaRepository` to use multiple loaders
5. Add schema discovery and listing
6. Support schema versioning (`SESSION_LOG@2.0`)

**Acceptance Criteria**:
- Can load schemas from `./schemas/*.oct.md`
- Can fetch schemas from remote registry
- Can list all available schemas
- Can specify schema versions in ingest tool

**Estimated Effort**: 2-3 days

### Phase 2: Projection Modes (P1)
**Goal**: Make projection modes schema-driven

**Tasks**:
1. Add `projections` section to schema format
2. Parse projection definitions from schema documents
3. Implement actual field filtering (currently just emits full doc)
4. Update `eject` tool to use schema-defined projections
5. Add projection mode validation

**Acceptance Criteria**:
- Schemas can define custom projection modes
- `eject(mode="executive")` actually filters fields
- Projection modes vary correctly by schema
- Lossy flag and omitted fields are accurate

**Estimated Effort**: 2 days

### Phase 3: Configuration System (P1)
**Goal**: Enable user and project-level configuration

**Tasks**:
1. Create `config.py` with YAML loading
2. Define configuration file schema
3. Add config search paths (project → user → default)
4. Integrate config into MCP server initialization
5. Add config validation with helpful errors

**Acceptance Criteria**:
- Config loads from `.octave-mcp.yaml` (project) or `~/.octave/config.yaml` (user)
- Invalid config fails at startup with clear message
- Default config works without any setup
- Config can override schema paths and validation settings

**Estimated Effort**: 1-2 days

### Phase 4: Compression Tiers (P2)
**Goal**: Implement actual compression behavior

**Tasks**:
1. Implement LOSSLESS tier (preserve everything)
2. Implement CONSERVATIVE tier (85-90% compression)
3. Implement AGGRESSIVE tier (70% compression)
4. Implement ULTRA tier (50% compression)
5. Add compression tier selection to ingest tool

**Acceptance Criteria**:
- Compression actually reduces output size
- Each tier meets fidelity targets from spec
- Compression is lossless within tier constraints
- Can demonstrate compression on real documents

**Estimated Effort**: 3-4 days (requires careful implementation)

## Validation and Testing

### Property-Based Tests Required

**Spec-Static Invariants**:
```python
def test_canonicalization_is_idempotent(doc):
    """canon(canon(x)) == canon(x)"""
    canonical = canonicalize(doc)
    assert canonicalize(canonical) == canonical

def test_operator_precedence_matches_spec():
    """A⊕B→C always parses as (A⊕B)→C"""
    ast = parse("A⊕B→C")
    assert ast.structure == Sequence(Synthesis(A, B), C)

def test_forbidden_repairs_never_activate():
    """TIER_FORBIDDEN rules can't be bypassed by config"""
    # Even with permissive config, should error
    with pytest.raises(ValidationError, match="E004"):
        ingest(content="FIELD::", schema="TEST", fix=True)
```

**Schema-Dynamic Invariants**:
```python
def test_schema_loader_order_independence(schema_name):
    """Same schema from any loader returns equivalent result"""
    schema_from_file = file_loader.load(schema_name)
    schema_from_url = url_loader.load(schema_name)
    assert schemas_equivalent(schema_from_file, schema_from_url)

def test_custom_schemas_override_builtins():
    """Custom schema with same name takes precedence"""
    repo = SchemaRepository(config_with_custom_path)
    schema = repo.get("META")
    assert schema.source == "custom"
```

**Configuration Invariants**:
```python
def test_invalid_config_fails_at_startup():
    """Bad config prevents server from starting"""
    with pytest.raises(ConfigError):
        server = OctaveMCPServer(config_path="invalid.yaml")

def test_config_does_not_affect_grammar():
    """Config changes don't alter operator behavior"""
    # Different configs should produce same parse tree
    ast1 = parse_with_config("A→B", config1)
    ast2 = parse_with_config("A→B", config2)
    assert ast1 == ast2
```

### Integration Tests Required

1. **End-to-End Schema Loading**:
   - Load schema from file
   - Validate document against schema
   - Detect schema version mismatches

2. **Projection Mode Application**:
   - Executive view omits technical fields
   - Developer view omits business fields
   - Round-trip through canonical preserves data

3. **Configuration Layering**:
   - Project config overrides user config
   - User config overrides defaults
   - Environment variables override file config

## Consequences

### Positive
1. **Clear Architecture**: Spec-static vs schema-dynamic principle provides design clarity
2. **Interoperability**: Hardcoded grammar ensures all OCTAVE implementations agree
3. **Safety**: Forbidden repairs remain non-configurable, preventing corruption
4. **Extensibility**: Schema repository enables domain-specific extensions
5. **Evolution**: Spec versioning (5.0.3 → 5.1.0) handled through code, not config drift

### Negative
1. **Grammar Changes Require Code Updates**: True, but correct - grammar changes are spec changes
2. **Implementation Effort**: Schema repository needs significant work (P0)
3. **Migration Path**: Existing minimal schemas need enhancement

### Risks and Mitigations

**Risk**: Config complexity makes system harder to use
**Mitigation**: Provide sensible defaults that work without any config

**Risk**: Remote schema loading introduces network dependency
**Mitigation**: Implement caching and fallback to builtin schemas

**Risk**: Schema versioning creates compatibility issues
**Mitigation**: Support version pinning and clear upgrade paths

## Comparison to Similar Systems

### YAML/JSON Schema
- **Similar**: Schema definitions are separate from parser
- **Different**: YAML grammar is hardcoded, schemas define document structure
- **OCTAVE Parallel**: Grammar hardcoded, schemas dynamic

### TypeScript
- **Similar**: Core language syntax is fixed, type definitions are external
- **Different**: TypeScript allows arbitrary type definitions
- **OCTAVE Parallel**: Operators fixed, schemas customizable

### Protobuf
- **Similar**: Wire format is fixed, message schemas are defined in .proto files
- **Different**: Protobuf schemas compiled to code
- **OCTAVE Parallel**: OCTAVE schemas loaded at runtime

## Conclusion

The OCTAVE MCP Server **correctly** hardcodes core grammar elements that are part of the OCTAVE v5.1.0 specification. These are language-level definitions that must remain consistent across implementations for interoperability.

However, the schema management system is currently **too minimal** for production use. The primary gap is the schema repository, which needs to support:
1. Loading schemas from files and URLs
2. Schema versioning and discovery
3. Custom schema registration
4. Caching for remote schemas

Projection modes also need enhancement to be schema-driven rather than hardcoded.

**Final Recommendation**: Proceed with implementation roadmap in priority order:
1. **P0**: Enhanced schema repository (blocks production use)
2. **P1**: Schema-driven projection modes (improves usability)
3. **P1**: Configuration system (enables customization)
4. **P2**: Compression tier implementation (enhancement)

This approach maintains the architectural integrity of "one language, disciplined tolerance" while enabling the extensibility needed for real-world applications.

See [ADR-001](/Volumes/OCTAVE/octave/worktrees/octave-build/docs/adr/001-configurability-and-modularity-architecture.md) for detailed architectural decision record.
