===LLM_OCTAVE_QUICK_REFERENCE===
// (Olympian Common Text And Vocabulary Engine)
// OCTAVE Quick Reference - Essential syntax and semantics for LLM comprehension

META:
  NAME::"OCTAVE Quick Reference"
  VERSION::"1.0"
  PURPOSE::"Provide a comprehensive, one-page reference for OCTAVE syntax and semantics."
  ENCODING::"UTF-8"

---

SYNTAX_OPERATORS:
  ASSIGNMENT::"::"              // KEY::VALUE
  PROGRESSION::"->"              // STATE->STATE (lists only)
  COMMENT::"//"                 // To end of line
  SYNTHESIS::"+"                // DOMAIN+DOMAIN
  TENSION::"_VERSUS_"                  // FORCE_VERSUS_FORCE

STRUCTURE:
  DOCUMENT::"===NAME==="
  SECTION::"SECTION_NAME:"
  INDENT::"  "                  // Exactly 2 spaces
  DEFINITION::"0.DEF:"            // Custom terms

DATA_TYPES:
  STRING_BARE::identifier
  STRING_QUOTED::"with spaces"
  STRING_MULTILINE::"""
  content
  """
  NUMBER::42, 3.14, -1e10
  BOOLEAN::true, false          // Lowercase only
  NULL::null                    // Lowercase only
  LIST::[item1, item2]          // No trailing comma
  OBJECT::{{k:v, k2:v2}}        // Inline only

---

SEMANTIC_OPERATORS*:
  SYNTHESIS:"+"::"Combines elements into a greater whole (e.g., ATHENA+HEPHAESTUS)"
  TENSION:"_VERSUS_"::"Creative or destructive conflict between forces (e.g., INNOVATION_VERSUS_STABILITY)"
  PROGRESSION:"->"::"Narrative sequence or causal flow (e.g., [PROMETHEAN->HUBRIS->NEMESIS])"

SEMANTIC_PANTHEON*:
  DOMAINS::"Core areas of concern (e.g., APOLLO, HERMES, ATHENA)"
  PATTERNS::"Recurring narrative dynamics (e.g., ODYSSEAN, ICARIAN, GORDIAN)"
  FORCES::"Abstract systemic dynamics (e.g., CHAOS, KAIROS, NEMESIS)"

(*: See Semantics Spec for full list and definitions)

---

EXAMPLE_COMPOSITION:
  SYSTEM_STATUS:
    STATE::ICARIAN_TRAJECTORY
    TENSION::ARES _VERSUS_ HEPHAESTUS
    NEXT_ACTION::[ATHENA:PLAN->GORDIAN:EXECUTE]

===END===
