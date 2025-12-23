# OCTAVE Claude Code Skills

This directory contains three specialized Claude Code skills that enhance LLM and agent capabilities for working with OCTAVE documents.

## Quick Start

Three skills form a progression:

1. **octave-literacy** – Foundation skill for core OCTAVE syntax
2. **octave-compression** – Specialized workflow for prose-to-OCTAVE transformation
3. **octave-mastery** – Advanced semantic vocabulary and architectural patterns

Load them in this order (octave-compression and octave-mastery require octave-literacy first).

## Skill Overview

### octave-literacy
**Purpose**: Fundamental reading and writing capability for the OCTAVE format.

Provides core syntax rules, critical operators, and structural competence for working with OCTAVE documents.

**Triggers**: `octave format`, `write octave`, `octave syntax`, `structured output`

### octave-compression
**Purpose**: Transform verbose prose into semantic OCTAVE structures.

Provides a 4-phase workflow (Read → Extract → Compress → Validate) with rules for achieving 60-80% token reduction while preserving decision logic fidelity.

**Requires**: octave-literacy

**Triggers**: `compress to octave`, `semantic compression`, `documentation refactoring`

### octave-mastery
**Purpose**: Advanced semantic vocabulary and architectural patterns.

Provides the Semantic Pantheon (mythological vocabulary for complex concepts), narrative dynamics, system forces, and advanced syntax patterns for high-density specifications and agent design.

**Requires**: octave-literacy

**Triggers**: `octave architecture`, `agent design`, `semantic pantheon`, `advanced octave`

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
