---
name: octave-literacy
description: Fundamental reading and writing capability for the OCTAVE format. Inject this to give an agent basic structural competence without the overhead of full architectural specifications. Triggers on: octave format, write octave, octave syntax, structured output.
allowed-tools: Read
---

# OCTAVE Literacy Skill

===OCTAVE_LITERACY===
META:
  TYPE::SKILL
  VERSION::"1.0"
  PURPOSE::"Essential syntax and operators for basic OCTAVE competence"
  TIER::LOSSLESS

§1::CORE_SYNTAX
  ASSIGNMENT::KEY::value   // Double colon is MANDATORY for data
  BLOCK::KEY:[indent_2]    // Single colon + newline + 2 spaces starts a block
  LIST::[a,b,c]            // Brackets for collections
  STRING::"value"          // Quotes required if contains spaces or special chars
  COMMENT:://              // Standard comment syntax

§2::OPERATORS
  →::Flow (Step 1 → Step 2 → Step 3)
  ⊕::Synthesis (Component A ⊕ Component B = New Whole)
  ⇌::Tension (Speed ⇌ Quality)
  ⧺::Concatenation (Prefix ~ Suffix)
  §::Target (→§DECISION_LOG)

§3::CRITICAL_RULES
  1::No spaces around assignment :: (KEY::value, not KEY :: value)
  2::Indent exactly 2 spaces per level (NO TABS)
  3::All keys must be [A-Z, a-z, 0-9, _]
  4::Envelopes are ===NAME=== at start and ===END=== at finish

§4::EXAMPLE_BLOCK
  ===EXAMPLE===
  STATUS::ACTIVE
  PHASES:
    PLAN::[Research → Design]
    BUILD::[Code ⊕ Test]
  METRICS:
    SPEED::"High"
    QUALITY::"Verified"
  ===END===

===END===
