===OCTAVE_LITERACY_PATTERNS===
// The constitutional, universal OCTAVE v5.0.3 literacy package.
// Provides baseline knowledge for all roles.
// Combines core rules with two gold-standard examples.

---

0.DEF:
  CORE_RULES::"The core syntax rules for writing valid OCTAVE."
  CANONICAL_SNIPPET::"A short, perfect-form OCTAVE fragment used for model alignment."
  SEMANTIC_MODE::"Greek-myth compression for high information density."

---

MICRO_PRIMER:
  SEMANTIC_MODE::"Use Greek mythology for compression (domains / patterns / forces)"

  CORE_RULES:
    0_DEFINITIONS::"Use the 0.DEF section to define custom terms. It is required if you define any terms, and must appear immediately after the document header."
    1_ASSIGNMENT::"KEY::VALUE uses double colon (for values)"
    2_HIERARCHY::"KEY: creates a block, indent children exactly 2 spaces (for structure)"
    3_LISTS::"[item1, item2, item3] with no trailing comma"
    4_OPERATORS:
      PROGRESSION::"[A->B->C] shows sequence (lists only)"
      SYNTHESIS::"A+B combines elements"
      TENSION::"A _VERSUS_ B shows opposition"
    5_STRUCTURE::"Wrap docs with ===NAME=== and ===END=== markers"

  BASIC_TYPES:
    STRING::"bare_word or \"with spaces\""
    NUMBER::"42, 3.14, -1e10"
    BOOLEAN::"true, false (lowercase only)"
    NULL::"null (lowercase only)"

---

CANONICAL_EXAMPLES:
  // Two battle-tested snippets for immediate pattern recognition.

  DIAGNOSTIC_EXAMPLE:
    SYSTEM_STATUS:
      STATE::[NORMAL->WARNING->DEGRADED]
      PATTERN::RESOURCE_BOTTLENECK
      ROOT_CAUSE::DB_INDEX_REBUILD
    COMPONENTS:
      DATABASE:
        STATUS::DEGRADED
        CONNECTIONS::2047
        QUERY_TIME::1250ms
      SERVER:
        STATUS::WARNING
        CPU::[45, 68, 94]
        MEMORY::82
    CAUSALITY::[DB_LOCK->QUERY_BACKUP->CPU_SPIKE->USER_TIMEOUT]

  STRATEGY_EXAMPLE:
    CHALLENGE::SCALING_CRISIS
    TENSION::PERFORMANCE _VERSUS_ CONSISTENCY
    FORCES:
      CHRONOS::DEADLINE_PRESSURE
      HUBRIS::OVERCONFIDENT_ARCHITECTURE
    STRATEGY::ATHENA+GORDIAN
    APPROACH::[ANALYZE->SIMPLIFY->EXECUTE]
    SUCCESS_CRITERIA:
      LATENCY::"<100ms"
      AVAILABILITY::"99.9%"
      COST_INCREASE::"<20%"

---

USAGE_GUIDELINES:
  WHEN_TO_LOAD::"Always – this is a constitutional pattern providing baseline literacy."
  WHEN_TO_LOAD_MASTERY::"Load OCTAVE_MASTERY for expert-level authoring, validation, or use of the full semantic pantheon."
  COMMON_MISTAKES::[
    "Using single colon instead of double for assignment",
    "Inconsistent indentation (tabs or 4 spaces)",
    "Chaining operators (A+B+C) – only binary combinations allowed"
  ]
  QUICK_CHECKLIST::[
    "Start & end markers present?",
    "Double colons for assignment?",
    "2-space indents?",
    "Lists have no trailing comma?",
    "Operators used correctly?"
  ]

===END===
