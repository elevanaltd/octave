# Assessment Validation - OCTAVE MCP Enforcement Gaps

**Date**: 2025-12-22
**Assessed By**: External reviewer
**Validated By**: system-steward
**Status**: CONFIRMED

## Executive Summary

The assessment is **accurate**. All five identified gaps exist in the current implementation and represent real enforcement risks. The core concern is valid: agents can write OCTAVE syntax, but the system lacks the enforcement mechanisms to guarantee correctness.

## Validated Findings

### 1. Return Shape: JSON-in-TextContent ✓ CONFIRMED

**Location**: `src/octave_mcp/mcp/server.py:72`

```python
return [TextContent(type="text", text=json.dumps(result, indent=2))]
```

**Evidence**: Tool results are wrapped as JSON strings inside TextContent. Clients must parse JSON from text rather than receiving structured data.

**Impact**:
- Agents must parse `result.text` as JSON
- Type safety lost at protocol boundary
- Silent failures if client assumes structured JSON

**Example**:
```python
# Client must do:
result = await call_tool("octave_ingest", {...})
data = json.loads(result[0].text)  # Parse JSON from text

# Instead of:
data = result.data  # Direct structured access
```

### 2. Validation is a Stub ✓ CONFIRMED

**Location**: `src/octave_mcp/mcp/ingest.py:136-137`

```python
# For now, skip actual schema validation (will be added with P2.5)
# Just create a basic validator
validator = Validator(schema=None)
```

**Evidence**: Schema validation is deferred. Current implementation:
- Instantiates `Validator(schema=None)`
- Comment explicitly states validation is TODO for P2.5
- No schema enforcement occurs

**Impact**:
- "BLOCK not warn" gates cannot block - they warn at best
- Invalid OCTAVE passes validation silently
- Agents cannot rely on validation feedback for correctness

**Example**:
```python
# This will not fail even with invalid schema:
result = await octave_ingest(
    content="INVALID::STRUCTURE",
    schema="SESSION_LOG"
)
# result.warnings may be empty even though structure is wrong
```

### 3. Format Fallback Silently Returns OCTAVE ✓ CONFIRMED

**Location**: `src/octave_mcp/mcp/eject.py:105-108`

```python
if output_format != "octave":
    # Return canonical OCTAVE with note
    output = f"# Format '{output_format}' not yet implemented - returning OCTAVE\n{result.output}"
    return {"output": output, "lossy": result.lossy, "fields_omitted": result.fields_omitted}
```

**Evidence**: Only `format="octave"` is implemented. Requests for `json`, `yaml`, or `markdown` return OCTAVE with a comment prefix.

**Impact**:
- Agents expecting JSON/YAML get OCTAVE with comment
- Easy to miss if agent doesn't inspect output
- Silent format mismatch if client assumes format match

**Example**:
```python
# Agent requests JSON:
result = await octave_eject(content=doc, schema="META", format="json")

# Gets OCTAVE with comment instead:
# Format 'json' not yet implemented - returning OCTAVE
===META===
TYPE::"SESSION_LOG"
===END===
```

### 4. Template Generation is Minimal ✓ CONFIRMED

**Location**: `src/octave_mcp/mcp/eject.py:84-91`

```python
if content is None:
    # For now, generate minimal template
    template = f"""===TEMPLATE===
META:
  TYPE::{schema_name}
  VERSION::"1.0"

# Template generated for schema: {schema_name}
===END==="""
    return {"output": template, "lossy": False, "fields_omitted": []}
```

**Evidence**: Template generation is not schema-driven. Returns hardcoded structure regardless of schema requirements.

**Impact**:
- Templates don't teach required fields for schema
- Agents can't discover schema structure via templates
- No guidance on what fields are mandatory

**Example**:
```python
# Agent requests template for SESSION_LOG:
result = await octave_eject(content=None, schema="SESSION_LOG", format="octave")

# Gets generic template, not SESSION_LOG-specific structure:
===TEMPLATE===
META:
  TYPE::SESSION_LOG
  VERSION::"1.0"
===END===

# Missing: AGENT, PHASE, WORK, OUTCOMES, etc.
```

### 5. Tokenization Unpacking Bug ✓ CONFIRMED

**Location**: `src/octave_mcp/mcp/ingest.py:100-103`

```python
tokens = tokenize(content)

if verbose:
    stages["TOKENIZE_COMPLETE"] = f"{len(tokens)} tokens produced"
```

**Evidence**:
- `tokenize()` returns `tuple[list[Token], list[Any]]` (line 136 of lexer.py)
- Code calls `len(tokens)` on the tuple, not the token list
- Repairs from tokenization are dropped

**Impact**:
- `len(tokens)` is always 2 (tuple length), not actual token count
- Verbose output shows wrong token count: "2 tokens produced"
- ASCII normalization repairs are lost
- Repair tracking incomplete

**Actual signature**:
```python
# From src/octave_mcp/core/lexer.py:136
def tokenize(content: str) -> tuple[list[Token], list[Any]]:
    """Returns: Tuple of (tokens, repairs)"""
```

**Should be**:
```python
tokens, tokenize_repairs = tokenize(content)
result["repairs"].extend(tokenize_repairs)

if verbose:
    stages["TOKENIZE_COMPLETE"] = f"{len(tokens)} tokens produced"
```

## Risk Assessment

### Current State
- **User Perspective**: Agents can write syntactically valid OCTAVE
- **System Reality**: No enforcement of semantic correctness
- **Gap**: "Write OCTAVE" ≠ "Guarantee correct OCTAVE"

### Production Blockers
1. **Validation stub** - Cannot enforce schema compliance
2. **Return shape** - Type safety lost at protocol boundary
3. **Tokenization bug** - Repair tracking broken, metrics wrong
4. **Format fallback** - Silent format mismatches
5. **Template generation** - Cannot teach schema structure

### Severity Classification
- **P0 (BLOCKING)**: #1 Validation stub, #5 Tokenization bug
- **P1 (HIGH)**: #2 Return shape, #3 Format fallback
- **P2 (MEDIUM)**: #4 Template generation

## Recommendations

### Immediate (P0)
1. **Fix tokenization unpacking** (5 lines)
   - Unpack `(tokens, repairs)` tuple
   - Track repairs from normalization
   - Fix verbose token count

2. **Implement schema validation** (P2.5 work)
   - Load schema definitions
   - Pass schema to `Validator(schema=...)`
   - Enable BLOCKING on validation errors

### Short-term (P1)
3. **Standardize return shape**
   - Return structured JSON directly, or
   - Document that clients must parse TextContent.text as JSON

4. **Fail explicitly on unsupported formats**
   - Return error for `json`/`yaml`/`markdown` instead of fallback
   - Make format mismatch obvious

### Medium-term (P2)
5. **Schema-driven templates**
   - Generate templates from schema definitions
   - Include required fields with type hints
   - Provide examples for complex structures

## Proposed Agent Contract

The reviewer's suggestion for "agent contract" is sound. Minimum requirements:

### Client-side
```python
# Parse TextContent as JSON
result = await call_tool("octave_ingest", {...})
data = json.loads(result[0].text)

# Check for validation errors
if data.get("warnings"):
    for warning in data["warnings"]:
        if warning["code"].startswith("E"):  # Errors
            raise ValidationError(f"OCTAVE invalid: {warning['message']}")
```

### Server-side (after P2.5)
```python
# Load schema
schema = load_schema(schema_name)
validator = Validator(schema=schema)

# BLOCK on errors (not warn)
errors = validator.validate(doc, strict=True)
if errors:
    raise ValidationError(errors)  # Hard failure
```

### Prompt-level
```
OCTAVE_COMPLIANCE::[
  REQUIRE::schema_validation_pass,
  FAIL_HARD::on_validation_error,
  VERIFY::result.warnings.empty,
  PARSE::TextContent.text_as_json
]
```

## Evidence Chain

All findings verified against:
- `src/octave_mcp/mcp/server.py` (return shape)
- `src/octave_mcp/mcp/ingest.py` (validation stub, tokenization bug)
- `src/octave_mcp/mcp/eject.py` (format fallback, template generation)
- `src/octave_mcp/core/lexer.py` (tokenize signature)

## Conclusion

**Assessment: ACCURATE**

The reviewer correctly identified that:
1. Agents can produce OCTAVE (true)
2. System cannot enforce OCTAVE correctness (true)
3. Risk is enforcement, not syntax (true)

The five specific gaps are all confirmed in current codebase. The system needs strong enforcement mechanisms before it can reliably guarantee OCTAVE compliance in production.

**Next Steps**:
1. Fix tokenization bug (immediate, 5 lines)
2. Implement schema validation (P2.5, blocking)
3. Standardize client contract (documentation)
4. Add integration tests for enforcement

**Buck stops here**: System Steward confirms this assessment and recommends prioritizing P0 fixes before expanding OCTAVE adoption.
