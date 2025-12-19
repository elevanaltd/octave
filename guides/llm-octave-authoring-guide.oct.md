===LLM_OCTAVE_AUTHORING_GUIDE===
// (Olympian Common Text And Vocabulary Engine)
// OCTAVE Authoring Guide - Best practices for creating clear, effective OCTAVE documents.

META:
  NAME::"OCTAVE Authoring Guide & Checklist"
  VERSION::"1.0"
  PURPOSE::"Provide guidelines for high-quality OCTAVE document creation and validation."
  ENCODING::"UTF-8"

---

SECTION_I:CORE_PRINCIPLES:
  CLARITY::"Prefer clear, direct statements over complex ones."
  COMPRESSION::"Use the semantic pantheon to achieve high-density meaning."
  CONSISTENCY::"Follow the syntax and semantic rules precisely."
  CONTEXT::"Ensure every statement has a clear purpose and connection."

---

SECTION_II:AUTHORING_BEST_PRACTICES:

  HIERARCHY:
    DESCRIPTION::"Group related concepts logically using indentation."
    RULE::"Aim for 2-3 levels of depth to maintain readability."
    EXAMPLE:
      SYSTEM:
        COMPONENT:
          PROPERTY::VALUE

  SEMANTICS:
    DESCRIPTION::"Leverage the PANTHEON for maximum impact."
    RULE::"Use DOMAINS for components, PATTERNS for narratives, and FORCES for dynamics."
    EXAMPLE:
      PROJECT_STATUS:
        STATE::ODYSSEAN // A long, transformative journey
        TENSION::INNOVATION _VERSUS_ STABILITY

  DEFINITIONS:
    DESCRIPTION::"Define custom, domain-specific terms in the 0.DEF section."
    RULE::"Only define terms that are not part of the core OCTAVE vocabulary and are used multiple times."

  COMMENTS:
    DESCRIPTION::"Use comments (//) to clarify intent or add context that isn't part of the data."
    RULE::"A good OCTAVE document often needs few comments, as the semantics should be clear."

---

SECTION_III:ADVANCED_TECHNIQUES:

  COMPOSITION:
    DESCRIPTION::"Combine semantic and syntactic elements for precision."
    RULE::"Follow the order: DOMAIN[:ASPECT]:SYNTACTIC[:INSTANCE]"
    EXAMPLE:
      VALID::HERMES:SVC:API // A service in the communication domain
      INVALID::SVC:API:HERMES // Syntactic element cannot come first

  GRANULARITY:
    DESCRIPTION::"Use up to three levels of specificity for semantic elements."
    PATTERN::"DOMAIN[:ASPECT][:INSTANCE]"
    EXAMPLES:
      L1::HERMES
      L2::HERMES:AUTH
      L3::HERMES:AUTH:OAUTH2

  STRING_VS_SEMANTIC:
    DESCRIPTION::"Know when to use a semantic token versus a plain string."
    USE_SEMANTIC::"For concepts, relationships, and validated patterns (e.g., POSEIDON:DB)"
    USE_STRING::"For external IDs, specific config values, and instance names (e.g., \"postgres-prod-01\")"
    EXAMPLE::"POSEIDON:DB→\"postgres-prod-01\" // The semantic domain points to a specific string instance"

---

SECTION_IV:VALIDATION_CHECKLIST:

  SYNTAX_CHECKS:
    - [ ] Document is wrapped in ===DOCUMENT_NAME=== markers.
    - [ ] All assignments use the `::` operator with no surrounding spaces.
    - [ ] Indentation is exactly 2 spaces per level. No tabs are used.
    - [ ] Lists `[...]` do not have trailing commas.
    - [ ] `true`, `false`, and `null` are always lowercase.

  SEMANTIC_CHECKS:
    - [ ] The PANTHEON vocabulary is used correctly and appropriately.
    - [ ] Semantic operators (+, _VERSUS_, ->) are used according to their defined meanings.
    - [ ] The composition of statements is logical and easy to understand.

  QUALITY_CHECKS:
    - [ ] The document is well-structured and easy to read.
    - [ ] The level of compression is appropriate for the content's complexity.
    - [ ] The overall message is clear, concise, and unambiguous.

===END===
