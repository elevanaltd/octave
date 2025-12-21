===OCTAVE_V5_DATA_PROFILE===
META:
  TYPE::PROTOCOL_DEFINITION
  VERSION::"5.0"
  STATUS::ACTIVE
  NAME::"OCTAVE Data Profile"
  PURPOSE::"Maximum token density for operational documents and context"
  EXTENDS::octave-5.oct.md

// =============================================================================
// DATA PROFILE: Telegram Mode
// For operational state, context injection, and compressed knowledge
// Activated implicitly for: SESSION_CONTEXT, KNOWLEDGE_ARTIFACT, CONFIGURATION
// =============================================================================

§1::DESIGN_PHILOSOPHY
PHILOSOPHY:
  GOAL::"Minimum tokens, maximum information"
  PRINCIPLE::"Structure provides compression through elimination of prose"
  VALIDATION::"External (against referenced schema) not embedded"
  TOKEN_PRIORITY::primary // Compression over ceremony

COMPARED_TO_SCHEMA:
  SCHEMA::"KEY:: [ example + CONST -> §TARGET ]" // ~15 tokens overhead
  DATA::"KEY::value" // ~2 tokens overhead
  SAVINGS::80%_per_line

§2::WHEN_TO_USE
USE_CASES::[
  "PROJECT-CONTEXT operational dashboards",
  "SESSION transcripts and state",
  "KNOWLEDGE artifacts for LLM injection",
  "Configuration files",
  "Compressed research summaries",
  "RAG context payloads"
]

§3::CORE_SYNTAX
MINIMAL_PATTERN:
  SYNTAX::"KEY::value"
  NO_BRACKETS::true
  NO_CONSTRAINTS::true   // Validated externally
  NO_TARGETS::true       // Implicit or schema-defined

LIST_SYNTAX:
  PIPE_FORM::"KEY::a|b|c"          // Saves 4 tokens vs [a, b, c]
  BRACKET_FORM::"KEY::[a,b,c]"     // Also valid
  INLINE::"KEY::[a->b->c]"         // Progression lists

§4::COMPRESSION_TECHNIQUES
TOKEN_REDUCTION:
  DROP_ARTICLES::true              // "the", "a", "an" unnecessary
  DROP_PREPOSITIONS::when_clear    // Context implies relationships
  UNDERSCORE_PHRASES::true         // "multi word" -> "multi_word"
  ABBREVIATE_COMMON::[             // Domain-specific shortcuts
    "implementation"->"impl",
    "configuration"->"config",
    "validation"->"valid",
    "completed"->"DONE",
    "in_progress"->"WIP"
  ]

STRUCTURE_AS_COMPRESSION:
  BEFORE::"The project is currently in phase B1, which is the foundation infrastructure phase"
  AFTER::"PHASE::B1_FOUNDATION"
  SAVINGS::~85%

§5::TELEGRAM_STYLE
TELEGRAM_RULES:
  ALLOWED::"Abbreviated values preserving semantic anchors"
  ANCHORS_PRESERVE::[numbers,names,codes,ratings,status]
  MAY_DROP::[articles,prepositions,conjunctions,filler]

  EXAMPLE:
    VERBOSE::"The system has been tested and all 5 smoke tests are passing"
    TELEGRAM::"tests::5/5_passing"

§6::HIERARCHY_COMPRESSION
NESTED_COMPRESSION:
  FLAT_WHEN_POSSIBLE::"Prefer KEY::a|b|c over nested blocks"
  NEST_WHEN_NEEDED::"Complex relationships require structure"

  GOOD:
    PHASES::[P0::DONE,P1::DONE,P2::WIP,P3::PENDING]

  AVOID:
    PHASES:
      P0:
        STATUS::DONE
      P1:
        STATUS::DONE
      // ... 4x more tokens for same info

§7::SCHEMA_REFERENCE
EXTERNAL_VALIDATION:
  MECHANISM::"META.SCHEMA::path/to/schema.oct.md"
  EFFECT::"Parser validates DATA against SCHEMA constraints"

  EXAMPLE:
    // In data document:
    META:
      TYPE::SESSION_CONTEXT
      SCHEMA::octave-5-session-schema.oct.md

    // Fields validated against schema without embedded constraints

§8::CONTEXT_DOCUMENT_PATTERNS
PROJECT_CONTEXT_TEMPLATE:
  META:
    TYPE::SESSION_CONTEXT
    VERSION::"1.0"
    STATUS::ACTIVE
    UPDATED::"2025-01-01T00:00:00Z"

  PURPOSE::"Single line summary"
  PHASE::B1_FOUNDATION
  STATUS::[pytest::5/5,ruff::2_errors,mypy::pending]
  BLOCKERS::[error1|error2|dependency]
  NEXT::[fix_errors,run_tests,implement_feature]

CHECKLIST_TEMPLATE:
  TASK_1::DONE
  TASK_2::WIP
  TASK_3::PENDING[blocked_by::TASK_2]

§9::KNOWLEDGE_ARTIFACT_PATTERNS
COMPRESSED_RESEARCH:
  // Instead of prose paragraphs:
  FINDING_1::JSON_SCHEMA[WEAK|STRONG|NONE]->validation_only
  FINDING_2::CUE[MEDIUM|STRONG|PARTIAL]->closest_analog
  VERDICT::synthesis_not_invention|gap_filled

COMPARISON_MATRIX:
  JSON_SCHEMA::WEAK|STRONG|NONE
  OPENAPI::MEDIUM|STRONG|PARTIAL
  CUE::MEDIUM|STRONG|PARTIAL
  GUARDRAILS::STRONG|STRONG|STRONG

§10::COMPRESSION_METRICS
EXPECTED_RATIOS:
  VS_PROSE::"5-10x reduction"
  VS_MARKDOWN::"1.5-3x reduction"
  VS_SCHEMA_MODE::"3-5x reduction"

MEASUREMENT:
  TOKENS_BEFORE::natural_language_prose
  TOKENS_AFTER::data_mode_octave
  RATIO::TOKENS_BEFORE/TOKENS_AFTER

§11::ANTI_PATTERNS
AVOID:
  HOLOGRAPHIC_IN_DATA::"Don't use [ example + CONST -> §TARGET ] in data docs"
  VERBOSE_KEYS::"Use 'impl' not 'implementation_details'"
  REDUNDANT_NESTING::"Flatten when structure doesn't add meaning"
  PROSE_VALUES::"Convert sentences to structured data"

===END===
