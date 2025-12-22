# OCTAVE Tools

Minimal utilities for OCTAVE validation and integration.

## Files

### `lint-octave.py`
**Purpose**: Fast syntax validation for OCTAVE documents  
**Usage**: `python3 lint-octave.py < document.oct.md`
**Returns**: `OCTAVE_VALID` or `OCTAVE_INVALID: <reason>`

Checks:
- Document markers (===NAME=== and ===END===)
- META section presence (META: after optional preface comments)
- Indentation (2-space multiples)
- Assignment syntax (KEY::VALUE)
- Balanced brackets
- No trailing commas in lists

### `octave-to-json.py`
**Purpose**: Convert OCTAVE to JSON for system integration  
**Usage**: `python3 octave-to-json.py document.oct.md > output.json`

Features:
- Preserves semantic operators (synthesis, tension, progression)
- Tracks blank lines for round-trip fidelity
- Maintains quoted strings
- Handles nested structures

### `json-to-octave.py`
**Purpose**: Convert JSON back to OCTAVE format  
**Usage**: `python3 json-to-octave.py input.json > document.oct.md`

Features:
- Restores original formatting including blank lines
- Reconstructs semantic operators
- Preserves document structure

### `octave-validator.py`
**Purpose**: Comprehensive OCTAVE v5.0.3 validator
**Note**: More complex validation with operator checks and v5.0.3 feature support

**v5.0.3 Features Supported**:
- Constraint chaining with `&` operator inside brackets: `["val"&REQ&REGEX->§TARGET]`
- Plus operator `+` chaining now allowed: `A+B+C`
- Inline maps: `[k::v,k2::v2]`
- Empty blocks: `KEY:` with no children
- Block inheritance: `BLOCK[->§TARGET]:` with children

## Round-Trip Example

```bash
# Convert OCTAVE to JSON and back
python3 octave-to-json.py input.oct.md | python3 json-to-octave.py > output.oct.md

# Verify perfect round-trip
diff input.oct.md output.oct.md
```

## Philosophy

These tools are "scaffolding you fold away" - they enable integration with JSON-based systems while keeping OCTAVE as the primary format for direct model emission.
