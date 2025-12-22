# OCTAVE Examples

Examples demonstrating OCTAVE compression across different scales and domains.

---

## Pre-OCTAVE 5 Examples

Examples using earlier compression approaches and mythological patterns.

See [`pre-octave-5-examples/`](pre-octave-5-examples/) for:

### System Status Report

Compresses a verbose incident report while preserving all critical information.

- **Before (JSON)** - 378 tokens → [`system-status-before.json`](pre-octave-5-examples/system-status-before.json)
- **After (OCTAVE)** - 31 tokens → [`system-status-after.oct.md`](pre-octave-5-examples/system-status-after.oct.md)
- **Compression ratio:** 12.2x

Key techniques: Mythological patterns (ICARIAN_TRAJECTORY, HUBRIS→NEMESIS), domain mapping (APOLLO, HERMES, POSEIDON), structured compression

### Research Article Compression

Demonstrates compression of lengthy technical documentation while preserving key information.

- **Before (Markdown)** - ~1,800 tokens → [`research-article-before.md`](pre-octave-5-examples/research-article-before.md)
- **After (OCTAVE)** - ~150 tokens → [`research-article-after.oct.md`](pre-octave-5-examples/research-article-after.oct.md)
- **Compression ratio:** 12x

### Code Review Specialist Agent

Claude subagent specification compressed using OCTAVE patterns.

See [`code-review-specialist-claude-subagent.oct.md`](pre-octave-5-examples/code-review-specialist-claude-subagent.oct.md)

### LLMLingua Comparison

Comparative analysis of OCTAVE vs LLMLingua compression approaches.

- **Analysis (Markdown)** → [`octave-vs-llmlingua-compression-comparison-2025.md`](pre-octave-5-examples/octave-vs-llmlingua-compression-comparison-2025.md)
- **Analysis (OCTAVE)** → [`octave-vs-llmlingua-compression-comparison-2025.oct.md`](pre-octave-5-examples/octave-vs-llmlingua-compression-comparison-2025.oct.md)

---

## Post-OCTAVE 5 Examples

Examples demonstrating OCTAVE 5.1.0 compression tiers on the same source document.

See [`post-octave-5-examples/`](post-octave-5-examples/) for a complete compression demonstration suite.

### Original Research Document

The source document for all compression tier examples.

- **Original prose** - ~14,900 LLM tokens → [`survey-original-raw.oct.md`](post-octave-5-examples/survey-original-raw.oct.md)
- **Human-readable summary** → [`survey-prose-version.md`](post-octave-5-examples/survey-prose-version.md)

### OCTAVE 5.1.0 Compression Tiers

Same source document compressed to four different fidelity tiers, demonstrating the OCTAVE 5 compression framework.

#### LOSSLESS Tier (100% Fidelity)

- **File:** [`survey-octave-5-lossless.oct.md`](post-octave-5-examples/survey-octave-5-lossless.oct.md)
- **Tokens:** ~14,900 (unchanged)
- **Loss:** None (except formatting)
- **Use:** Critical decisions, legal/safety analysis, audit trails, reference work
- **Characteristics:** Complete original research with all nuance, explanatory depth, and reasoning chains

#### CONSERVATIVE Tier (85-90% Compression)

- **File:** [`survey-octave-5-conservative.oct.md`](post-octave-5-examples/survey-octave-5-conservative.oct.md)
- **Tokens:** ~4,800
- **Loss:** ~15% (redundancy, verbose transitions)
- **Use:** Research summaries, design decisions, technical analysis
- **Characteristics:** Explanatory depth preserved, tradeoff narratives intact, redundancy removed
- **Sweet spot:** Fits context window while preserving reasoning

#### AGGRESSIVE Tier (70% Compression)

- **File:** [`survey-octave-5-compressed.oct.md`](post-octave-5-examples/survey-octave-5-compressed.oct.md)
- **Tokens:** ~1,800
- **Loss:** ~30% (narrative depth, edge cases, historical context)
- **Use:** Context window scarcity, quick reference, decision support
- **Characteristics:** Core thesis and conclusions preserved, analytical landscape intact
- **Verdict:** Demonstrates analytical truth survives heavy compression

#### ULTRA Tier (50% Compression)

- **File:** [`survey-octave-5-ultra.oct.md`](post-octave-5-examples/survey-octave-5-ultra.oct.md)
- **Tokens:** ~2,800
- **Loss:** ~50% (almost all narrative, reasoning, examples)
- **Use:** Embedding generation, dense indexing, lookup tables
- **Characteristics:** Facts and structure only, not suitable for human reading
- **Safeguard:** Explicitly declares unsuitability for decision-making

### Compression Assessment

Evaluation of the compression tiers showing what is preserved and lost at each level.

#### Human-Readable Assessment

- **File:** [`assessment-survey.md`](post-octave-5-examples/assessment-survey.md)
- **Format:** Markdown (publication-ready)
- **Audience:** Humans evaluating OCTAVE approach
- **Content:** Full narrative explaining each tier, reuse threshold concept, when OCTAVE becomes superior

#### LLM-Optimized Assessment

- **File:** [`assessment-survey-llm.oct.md`](post-octave-5-examples/assessment-survey-llm.oct.md)
- **Format:** OCTAVE AGGRESSIVE tier
- **Compression:** ~70% (3,000 → 900 tokens)
- **Audience:** LLM injection, cross-tier consistency
- **Self-referential:** The assessment OF compression, written IN compressed format

This demonstrates meta-level dogfooding: the assessment preserves all verdicts while dropping narrative pacing.

### Comparison Guide

- **File:** [`post-octave-5-examples/compression-comparison/README.oct.md`](post-octave-5-examples/compression-comparison/README.oct.md)
- **Content:** Side-by-side comparison of all four tiers with selection matrix and use cases

---

## Key Insights from OCTAVE 5 Examples

### The Reuse Threshold

OCTAVE's structural overhead becomes a feature (not a cost) when a document crosses the reuse threshold:

**Below threshold:** One-off documents, single human reader → Use prose
**Above threshold:** Multi-prompt injection, validation, transformation, indexing → Use OCTAVE

### Semantic Invariants vs Token Minimization

- **Prose** optimizes for human inference (narrative, persuasion)
- **OCTAVE** optimizes for semantic invariants (structure, reuse, transformation)

These are complementary optimization targets, not competing approaches.

### Explicit Loss Control

Every OCTAVE 5 compressed document declares:
- `COMPRESSION_TIER` (LOSSLESS, CONSERVATIVE, AGGRESSIVE, ULTRA)
- `LOSS_PROFILE` (what is preserved, what is lost)
- Loss declarations prevent silent degradation

---

## Using These Examples

1. **Start with original:** Read the source document to understand full research
2. **Compare tiers:** Read CONSERVATIVE, then AGGRESSIVE, then ULTRA
3. **Evaluate assessment:** Compare markdown vs OCTAVE assessment versions
4. **Review guide:** Use the comparison guide to understand tier selection
5. **Study reversibility:** See how lower tiers derive from higher tiers without re-reasoning
