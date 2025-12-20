===OCTAVE_V4_SPEC===
META:
  NAME::"OCTAVE (Olympian Common Text And Vocabulary Engine)"
  VERSION::"4.0"
  TYPE::PROTOCOL_DEFINITION
  STATUS::ACTIVE
  PURPOSE::"Canonical protocol+format contract for LLM-authored artifacts"
  TAGLINE::"Strict Protocol for Machines, Flexible Dialect for Minds"
  REFERENCES::[
    "/Volumes/OCTAVE/octave/specs/octave-4.oct.md",
    "hub/library/octave/octave-4-spec.oct.md",
    "/Volumes/OCTAVE/octave/tools/octave-validator.py",
    "/Volumes/OCTAVE/octave/guides/octave-micro-primer.oct.md",
    "/Volumes/OCTAVE/octave/examples/code-review-specialist-claude-subagent.oct.md"
  ]

// NOTE: The body of this spec is authored in OCTAVE syntax (key constraints, indentation, lists).
// Section numbers remain as comments for readability; enforcement targets are represented as data below.

DEF:
  PROTOCOL::"The rigid contract required for system tools (Indexer, Router) to function. MUST be strictly followed."
  DIALECT::"The flexible semantic layer used for high-bandwidth communication. GUIDANCE only."
  VALIDATION::"Operational Success via Extraction of Protocol Artifacts."

---

// 1.0_THE_PROTOCOL_CONTRACT (STRICT ENFORCEMENT)
PROTOCOL_CONTRACT:
  ENCODING::"UTF-8"

  // 1.1_DOCUMENT_ANATOMY (The Envelope)
  DOCUMENT_ANATOMY:
    HEADER_RULE::"First non-whitespace line"
    FOOTER_RULE::"Last non-whitespace line"
    HEADER_REGEX::"^===([A-Z0-9_]+)===$"
    FOOTER_REGEX::"^===END===$"
    PREFACE_LINE_REGEX::"^\\s*(//.*)?$"

  // 1.2_CONTEXT_ANCHOR (META)
  CONTEXT_ANCHOR:
    PLACEMENT_RULE::"Must appear immediately after Preface"
    TERMINATION_RULE::"Block ends at first line starting at column 0 that is not a comment or blank line"

    META_SCHEMAS:
      SESSION_CONTEXT:
        TYPE::"SESSION_CONTEXT"
        REQUIRED_KEYS::[TYPE, SESSION_ID, ROLE, DATE]
        KEY_TYPES:
          TYPE::"string"
          SESSION_ID::"string"
          ROLE::"string"
          DATE::"YYYY-MM-DD"

      PROTOCOL_DEFINITION:
        TYPE::"PROTOCOL_DEFINITION"
        REQUIRED_KEYS::[TYPE, VERSION, STATUS]
        KEY_TYPES:
          TYPE::"string"
          VERSION::"string"
          STATUS::"enum"
        STATUS_ENUM::[ACTIVE, DRAFT, DEPRECATED]

  // 1.3_KNOWLEDGE_ARTIFACTS (The Extraction Layer)
  KNOWLEDGE_ARTIFACTS:
    DECISIONS:
      FORMAT::"DECISION_{N}::Content..."
      REGEX::"^\\s*DECISION_\\d+::(.*?)(?=^\\s*DECISION_\\d+::|^===END===|\\Z)"
      FLAGS::[MULTILINE, DOTALL]
      EXAMPLES::[
        "DECISION_1::Use Redis for caching BECAUSE speed > cost"
      ]

    BLOCKERS:
      FORMAT::"{ID}⊗{STATUS}[{DETAILS}]"
      REGEX::"^\\s*(\\w+)⊗(resolved|blocked)\\[([^\\]]+)\\]"
      FLAGS::[MULTILINE]
      ENCODING_NOTE::"UTF-8 (⊗ = U+2297)"
      STATUS_OPTIONS::[resolved, blocked]
      EXAMPLES::[
        "auth_bug⊗resolved[Fixed token expiry logic]"
      ]

    LEARNINGS:
      FORMAT::"LEARNING::Content..."
      REGEX::"^\\s*LEARNING::(.*)"
      FLAGS::[MULTILINE]
      EXAMPLES::[
        "LEARNING::Cache invalidation is hard",
        "LEARNING::Redis requires config update"
      ]

---

// 2.0_THE_SYNTAX_SWEET_SPOT (DIALECT GUIDANCE)
DIALECT_GUIDANCE:
  INTENT::"Recommendations (SHOULD), not requirements (MUST)"
  FORMATTING_PROFILE:
    RULE_OF_FIVE:
      ASSIGNMENT::"Prefer KEY::VALUE (double-colon) for assignments"
      HIERARCHY::"Indent exactly 2 spaces per level"
      LISTS::"Use [item1, item2, item3] with no trailing comma"
      OPERATORS:
        FLOW::"Use FLOW::[A->B->C] for sequence (progression is list-only)"
        SYNTHESIS::"Use A+B to combine elements"
        TENSION::"Use A _VERSUS_ B to express trade-offs"
      STRUCTURE::"Start with ===NAME===, end with ===END==="

  TYPES_GUIDANCE:
    STRING::"bare_word or \"with spaces\""
    NUMBER::"42, 3.14, -1e10"
    BOOLEAN::"true, false (lowercase)"
    NULL::"null (lowercase)"

  CORE_STRUCTURE:
    ASSIGNMENT::"KEY::VALUE"
    BLOCKS::"KEY:"
    LISTS::"[A, B, C]"
  OPERATORS:
    SYNTHESIS::"+"
    TENSION::"_VERSUS_"
    FLOW::"->"
    DEFINITION::"::"

---

// 3.0_SEMANTIC_FLEXIBILITY (OPERATIONAL BINDINGS)
SEMANTIC_FLEXIBILITY:
  MYTHOLOGICAL_PRIMITIVES:
    ATHENA:
      SEMANTIC::"Strategy, Architecture, Wisdom"
      OPERATIONAL::"MANDATE_DECISION[24h]"

    HEPHAESTUS:
      SEMANTIC::"Implementation, Code, Build"
      OPERATIONAL::"BUILD_CHECK"

    HERMES:
      SEMANTIC::"Communication, Interfaces, APIs"
      OPERATIONAL::"CONTRACT_VERIFY"

  PATTERN_PRIMITIVES:
    ODYSSEAN:
      SEMANTIC::"Long, navigational journey"
      OPERATIONAL::"MILESTONE_TRACKING"

    SISYPHEAN:
      SEMANTIC::"Repetitive, futile cycles"
      OPERATIONAL::"ESCALATE_AFTER[3]"

    GORDIAN:
      SEMANTIC::"Cutting through complexity"
      OPERATIONAL::"SIMPLIFY_NOW"

---

// 4.0_VALIDATION_STRATEGY
VALIDATION_STRATEGY:
  METHODOLOGY:
    STEPS::[
      "READ_FILE(path)",
      "CHECK_BOUNDARIES: first/last non-whitespace lines match DOCUMENT_ANATOMY.HEADER_REGEX and DOCUMENT_ANATOMY.FOOTER_REGEX",
      "VALIDATE_PREFACE: starting after Header, all lines before META must match DOCUMENT_ANATOMY.PREFACE_LINE_REGEX",
      "EXTRACT_META: parse indented Key::Values; stop per CONTEXT_ANCHOR.TERMINATION_RULE; validate required keys by META TYPE",
      "EXTRACT_ARTIFACTS: run regex for DECISIONS, BLOCKERS, LEARNINGS",
      "REPORT: VALID, INVALID, WARNINGS (warnings if artifacts missing in SESSION_CONTEXT files)"
    ]

---

LEGACY:
  V3_STATUS::DEPRECATED
  NOTE::"OCTAVE v3 syntax/semantics specs are archived for reference; v4 is the canonical spec going forward."

===END===
