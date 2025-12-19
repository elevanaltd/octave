# OCTAVE Templates

Ready-to-use templates for OCTAVE adoption.

## Files

### `system-prompt-octave.md`
**Purpose**: System message for ChatGPT, Claude, or other LLMs  
**Usage**: Copy into system prompt field of your LLM interface

Features:
- OCTAVE v4 formatting profile (Rule of Five)
- Data type specifications
- Example response format
- "Answer only in OCTAVE v4, no prose" directive

### `annotation-tiering-rubric.oct.md`
**Purpose**: Guide for applying OCTAVE annotations strategically  
**Usage**: Reference when annotating codebases with OCTAVE

Tiers:
- **HOTSPOT** (100% annotation): Security surfaces, O(N²)+ algorithms, business logic
- **IMPORTANT** (60-80%): Integration points, error handling, configuration
- **PERIPHERAL** (0-20%): Pure functions, DTOs, generated code

Decision flow helps classify code into appropriate tiers.

## Implementation Strategy

1. **Use system prompt** for immediate OCTAVE emission from LLMs
2. **Apply tiering rubric** to avoid over-annotation
3. **Focus annotation effort** where comprehension delta is highest

## Philosophy

"Annotate until marginal comprehension delta < 5%"

These templates enable practical OCTAVE adoption without token bloat.
