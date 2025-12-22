# OCTAVE Examples

Examples demonstrating OCTAVE compression across different scales and domains.

## Compression Tier Examples

Examples demonstrating OCTAVE 5.1.0 compression tiers on the same source document.

### Original Research Document

The source document for all compression tier examples.

- **Original prose** - ~14,900 LLM tokens → [`survey-original-raw.oct.md`](survey-original-raw.oct.md)
- **Human-readable summary** → [`survey-prose-version.md`](survey-prose-version.md)

### OCTAVE 5.1.0 Compression Tiers

Same source document compressed to four different fidelity tiers:

#### LOSSLESS Tier (100% Fidelity)

- **File:** [`survey-octave-5-lossless.oct.md`](survey-octave-5-lossless.oct.md)
- **Tokens:** ~14,900 (unchanged)
- **Loss:** None (except formatting)
- **Use:** Critical decisions, legal/safety analysis, audit trails, reference work

#### CONSERVATIVE Tier (85-90% Compression)

- **File:** [`survey-octave-5-conservative.oct.md`](survey-octave-5-conservative.oct.md)
- **Tokens:** ~4,800
- **Loss:** ~15% (redundancy, verbose transitions)
- **Use:** Research summaries, design decisions, technical analysis
- **Sweet spot:** Fits context window while preserving reasoning

#### AGGRESSIVE Tier (70% Compression)

- **File:** [`survey-octave-5-compressed.oct.md`](survey-octave-5-compressed.oct.md)
- **Tokens:** ~1,800
- **Loss:** ~30% (narrative depth, edge cases, historical context)
- **Use:** Context window scarcity, quick reference, decision support

#### ULTRA Tier (50% Compression)

- **File:** [`survey-octave-5-ultra.oct.md`](survey-octave-5-ultra.oct.md)
- **Tokens:** ~2,800
- **Loss:** ~50% (almost all narrative, reasoning, examples)
- **Use:** Embedding generation, dense indexing, lookup tables
- **Safeguard:** Explicitly declares unsuitability for decision-making

### Compression Assessment

Evaluation of the compression tiers showing what is preserved and lost at each level.

- **Human-Readable:** [`assessment-survey.md`](assessment-survey.md) - Full narrative for humans
- **LLM-Optimized:** [`assessment-survey-llm.oct.md`](assessment-survey-llm.oct.md) - Compressed format (~70%)

---

## Compression Comparisons

See [`compression-comparisons/`](compression-comparisons/) for comparative examples demonstrating OCTAVE's compression capabilities.

### System Status Report

Compresses a verbose incident report while preserving all critical information.

- **Before (JSON)** - 378 tokens → [`system-status-before.json`](compression-comparisons/system-status-before.json)
- **After (OCTAVE)** - 31 tokens → [`system-status-after.oct.md`](compression-comparisons/system-status-after.oct.md)
- **Compression ratio:** 12.2x

Key techniques: Mythological patterns (ICARIAN_TRAJECTORY, HUBRIS→NEMESIS), domain mapping

### Research Article Compression

Demonstrates compression of lengthy technical documentation.

- **Before (Markdown)** - ~1,800 tokens → [`research-article-before.md`](compression-comparisons/research-article-before.md)
- **After (OCTAVE)** - ~150 tokens → [`research-article-after.oct.md`](compression-comparisons/research-article-after.oct.md)
- **Compression ratio:** 12x

### LLMLingua Comparison

Comparative analysis of OCTAVE vs LLMLingua compression approaches.

- **Analysis (Markdown)** → [`octave-vs-llmlingua-compression-comparison-2025.md`](compression-comparisons/octave-vs-llmlingua-compression-comparison-2025.md)
- **Analysis (OCTAVE)** → [`octave-vs-llmlingua-compression-comparison-2025.oct.md`](compression-comparisons/octave-vs-llmlingua-compression-comparison-2025.oct.md)

---

## Templates

See [`templates/`](templates/) for reusable OCTAVE document templates.

---

## Integrations

See [`integrations/`](integrations/) for examples of OCTAVE integration with other tools.

### Repomix Integration

OCTAVE enhancement tools for Repomix output.

- [`integrations/repomix/`](integrations/repomix/) - Python scripts for OCTAVE-enhanced code summarization

---

## Key Insights

### The Reuse Threshold

OCTAVE's structural overhead becomes a feature when a document crosses the reuse threshold:

- **Below threshold:** One-off documents, single human reader → Use prose
- **Above threshold:** Multi-prompt injection, validation, transformation → Use OCTAVE

### Semantic Invariants vs Token Minimization

- **Prose** optimizes for human inference (narrative, persuasion)
- **OCTAVE** optimizes for semantic invariants (structure, reuse, transformation)

### Explicit Loss Control

Every OCTAVE 5 compressed document declares:
- `COMPRESSION_TIER` (LOSSLESS, CONSERVATIVE, AGGRESSIVE, ULTRA)
- `LOSS_PROFILE` (what is preserved, what is lost)

---

## Using These Examples

1. **Start with original:** Read the source document to understand full research
2. **Compare tiers:** Read CONSERVATIVE, then AGGRESSIVE, then ULTRA
3. **Evaluate assessment:** Compare markdown vs OCTAVE assessment versions
4. **Study comparisons:** See compression-comparisons/ for before/after examples
