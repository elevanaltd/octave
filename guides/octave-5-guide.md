# OCTAVE v5 Guide

## What is OCTAVE?

OCTAVE (Olympian Common Text And Vocabulary Engine) is a structured format for LLM-to-LLM communication. It achieves 5-10x token compression vs prose while remaining machine-parseable and human-readable.

## File Structure

### For LLM Consumption (inject these)

| File | Tokens | Use When |
|------|--------|----------|
| `specs/octave-5-llm-core.oct.md` | "~200" | Writing or parsing any OCTAVE document |

**This is the only file you need for most LLM operations.**

### For Human Reference (read these)

| File | Purpose |
|------|---------|
| `specs/octave-5.oct.md` | Core syntax, operators, types, failure modes |
| `specs/octave-5-schema.oct.md` | Holographic pattern for specs (TEACH+VALIDATE+EXTRACT) |
| `specs/octave-5-data.oct.md` | Compression rules for operational documents |
| `specs/octave-5-execution.oct.md` | Runtime integration (parser, validator, router) |

## Two Modes

### SCHEMA Mode (for specifications)
- Implicit for: `LANGUAGE_SPECIFICATION`, `PROTOCOL_DEFINITION`, `AGENT_DEFINITION`, `SKILL_DEFINITION`
- Pattern: `KEY:: [ "example" + CONSTRAINT -> §TARGET ]`
- Purpose: Self-teaching documents that validate and extract

### DATA Mode (for operational docs)
- Implicit for: `SESSION_CONTEXT`, `KNOWLEDGE_ARTIFACT`, `CONFIGURATION`
- Pattern: `KEY::value`
- Purpose: Maximum token density, validated against external schema

## Quick Syntax Reference

```octave
===DOCUMENT_NAME===
META:
  TYPE::SESSION_CONTEXT    // Determines mode
  VERSION::"1.0"
  STATUS::ACTIVE

SECTION:
  KEY::value               // Basic assignment
  LIST::[a,b,c]            // Or: a|b|c (saves tokens)
  FLOW::[A->B->C]          // Progression
  NESTED:
    CHILD::value           // 2-space indent

===END===
```

## Compression Rules

**Always preserve:** numbers, names, codes, operators, anchors

**May abbreviate:**
- `implementation` → `impl`
- `configuration` → `config`
- `completed` → `DONE`
- `in_progress` → `WIP`

**Drop:** articles (the, a), prepositions when clear, filler words

## Heritage

OCTAVE synthesizes patterns from:
- **JSON Schema** - constraint patterns
- **CUE** - unified data/schema
- **Guardrails RAIL** - teach+validate+extract
- **BDD/Gherkin** - self-exemplifying specs
- **LLMLingua** - telegram-style compression
