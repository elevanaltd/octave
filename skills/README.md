# OCTAVE Claude Code Skills

This directory contains three specialized Claude Code skills that enhance LLM and agent capabilities for working with OCTAVE documents.

## Quick Start

Four skills for progressive depth:

1. **octave-literacy** – Foundation skill for core OCTAVE syntax
2. **octave-compression** – Specialized workflow for prose-to-OCTAVE transformation
3. **octave-mastery** – Advanced semantic vocabulary and architectural patterns
4. **octave-mythology** – Functional mythological semantic compression (optional, evidence-backed)

Load literacy first. Compression and mastery require literacy. Mythology is optional—load when you want semantic shorthand activation.

## Skill Overview

### octave-literacy
**Domain**: HERMES (language/syntax)
**Purpose**: Core syntax, operators, structure

Enables reading/writing OCTAVE documents. Prerequisite for compression and mastery.

**Triggers**: `octave format`, `write octave`, `octave syntax`, `structured output`

### octave-compression
**Domain**: HEPHAESTUS (engineering/implementation)
**Purpose**: Prose → OCTAVE transformation (60-80% token reduction)

4-phase workflow: Read → Extract → Compress → Validate. Preserves decision logic while compressing tokens.

**Requires**: octave-literacy

**Triggers**: `compress to octave`, `semantic compression`, `documentation refactoring`

### octave-mastery
**Domain**: ATHENA (strategy/wisdom)
**Purpose**: Semantic density, pattern recognition, high-level design

Semantic Pantheon (10 domains), narrative dynamics (SISYPHEAN, ICARIAN, PROMETHEAN, PANDORAN, etc.), system forces (HUBRIS→NEMESIS, KAIROS, CHRONOS), advanced syntax.

**Requires**: octave-literacy

**Triggers**: `octave architecture`, `agent design`, `semantic pantheon`, `advanced octave`

### octave-mythology
**Domain**: All domains (toggleable)
**Purpose**: Functional mythological semantic compression (evidence-backed)

Practical mythology as compression shorthand: 60-70% token reduction, 88-96% comprehension, +17% quality. Domains, narrative patterns, system forces, agent communication patterns. Includes research evidence and anti-patterns.

**Optional**: Load when you want mythological semantic activation. Works with literacy, compression, mastery.

**Triggers**: `mythology`, `archetype`, `SISYPHEAN`, `ICARIAN`, `semantic compression`, `evidence-based`, `functional compression`

## Installation

For Claude Code users:

1. Skills in this directory are automatically discoverable
2. Activate via keyword triggers in your prompts (see "Triggers" above)
3. Or explicitly load: `/load octave-literacy`

For other systems supporting YAML frontmatter skills (Codex, Gemini):

1. Each skill is in `skill-name/SKILL.md` format
2. Copy the SKILL.md file to your system's skills directory
3. Register in your platform's configuration

## For Developers

Each skill follows the OCTAVE skills specification (`specs/octave-5-llm-skills.oct.md`):

- **Name**: `octave-[literacy|compression|mastery]`
- **Description**: Includes triggers and use cases
- **Format**: YAML frontmatter + OCTAVE body
- **Tools**: Read-only (no modifications)
- **Size**: All under 500 lines (skill constraint)

## See Also

- **Guides**: `guides/` for usage documentation and compression rules
- **Specs**: `specs/octave-5-llm-core.oct.md` for complete OCTAVE specification
- **AGENTS.md**: Agent guidance with skills documentation and architectural overview
