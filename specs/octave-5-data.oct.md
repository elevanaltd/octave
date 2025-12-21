===OCTAVE_V5_DATA_PROFILE===
META:
  TYPE::PROTOCOL_DEFINITION
  VERSION::"5.0"
  STATUS::ACTIVE
  NAME::"OCTAVE Data Profile"
  PURPOSE::"Maximum token density for operational documents and LLM context"
  EXTENDS::octave-5.oct.md

// =============================================================================
// DATA PROFILE: Telegram Mode (Annotation Level 1-2)
// For operational state, context injection, and compressed knowledge
// Heritage: LLMLingua + telegram-style + structure-as-compression
// =============================================================================

§1::THREE_AXES_IN_DATA_MODE
// Data mode trades teaching for compression
AXES:
  TEACH::REDUCED[structure_teaches|examples_external]
  VALIDATE::EXTERNAL[against_referenced_schema]
  EXTRACT::IMPLICIT[keys_are_extractable|no_explicit_targets]

TRADEOFF:
  GAIN::"5-10x token reduction vs prose"
  COST::"Less self-documenting; requires schema for validation"
  APPROPRIATE_WHEN::"Content pre-validated; token budget critical"

§2::WHEN_TO_USE
USE_CASES::[
  "PROJECT-CONTEXT operational dashboards",
  "SESSION transcripts and state",
  "KNOWLEDGE artifacts for LLM injection",
  "Configuration files",
  "Compressed research summaries",
  "RAG context payloads"
]

IMPLICIT_ACTIVATION::[
  TYPE::SESSION_CONTEXT,
  TYPE::KNOWLEDGE_ARTIFACT,
  TYPE::CONFIGURATION
]

§3::CORE_SYNTAX
MINIMAL_PATTERN:
  SYNTAX::"KEY::value"
  ANNOTATION_LEVEL::L1
  NO_BRACKETS::true
  NO_CONSTRAINTS::true[validated_externally]
  NO_TARGETS::true[implicit_or_schema_defined]

LIST_SYNTAX:
  PIPE_FORM::"KEY::a|b|c"        // Saves 4 tokens vs [a, b, c]
  BRACKET_FORM::"KEY::[a,b,c]"   // Also valid
  INLINE_FLOW::"KEY::[a->b->c]"  // Progression lists

§4::COMPRESSION_SAFETY
// Critical: What to preserve vs drop
ALWAYS_PRESERVE::[
  numbers,
  proper_nouns,
  codes_and_identifiers,
  enum_values,
  operators,
  section_anchors,
  extraction_targets
]

MAY_ABBREVIATE::[
  common_words,
  repeated_terms,
  filler_words
]

NEVER_COMPRESS::[
  "§ section anchors",
  "-> extraction operators",
  ":: assignment operators",
  "constraint types (REQ|OPT|CONST)"
]

§5::COMPRESSION_STRATEGIES
// Heritage: LLMLingua achieves 20x via token dropping
OCTAVE_NATIVE:
  MECHANISM::"Structure eliminates prose"
  COMPRESSION::5x_vs_prose

TELEGRAM_VALUES:
  MECHANISM::"Abbreviate within structure"
  COMPRESSION::additional_2x
  RULES::[
    drop_articles,
    drop_prepositions_when_clear,
    underscore_phrases,
    use_standard_abbreviations
  ]

STANDARD_ABBREVIATIONS::[
  impl::implementation,
  config::configuration,
  valid::validation,
  DONE::completed,
  WIP::in_progress,
  PENDING::not_started,
  req::required,
  opt::optional
]

§6::STRUCTURE_AS_COMPRESSION
// Key insight: Hierarchy eliminates explanatory prose
BEFORE:
  PROSE::"The project is currently in phase B1, which is the foundation infrastructure phase, and the pytest tests are passing with 5 out of 5 tests, but ruff has 2 errors remaining"

AFTER:
  OCTAVE:
    PHASE::B1_FOUNDATION
    TESTS::pytest[5/5_passing]
    LINT::ruff[2_errors]

SAVINGS::~85%_token_reduction

§7::HIERARCHY_COMPRESSION
FLATTEN_WHEN_POSSIBLE:
  GOOD::"PHASES::[P0::DONE,P1::DONE,P2::WIP,P3::PENDING]"
  VERBOSE:
    PHASES:
      P0:
        STATUS::DONE
      P1:
        STATUS::DONE
  SAVINGS::4x_fewer_tokens

NEST_WHEN_NEEDED::"Complex relationships require structure"

§8::SCHEMA_REFERENCE
// External validation against schema document
MECHANISM:
  IN_META::"SCHEMA::path/to/schema.oct.md"
  EFFECT::"Parser validates DATA against SCHEMA constraints"

EXAMPLE:
  META:
    TYPE::SESSION_CONTEXT
    SCHEMA::octave-session-schema.oct.md
    VERSION::"1.0"

§9::COMPRESSION_SPECTRUM
// LLMLingua compatibility for extreme cases
LEVELS:
  L0_OCTAVE_NATIVE::[structure_only|5x_reduction]
  L1_TELEGRAM::[abbreviated_values|additional_2x]
  L2_LLMLINGUA::[post_process_compression|additional_4x]
  L3_MAXIMUM::[combined|up_to_40x_reduction]

LLMLINGUA_COMPATIBILITY:
  APPROACH::"Apply LLMLingua to string values after OCTAVE structuring"
  BENEFIT::"Preserves structure while maximizing value compression"
  EXAMPLE:
    BEFORE::"purchased twelve boxes containing thirty highlighter pens"
    AFTER::"bought 12 boxes 30 pens"

§10::DOCUMENT_TEMPLATES
PROJECT_CONTEXT:
  META:
    TYPE::SESSION_CONTEXT
    VERSION::"1.0"
    STATUS::ACTIVE
  PURPOSE::"Single line summary"
  PHASE::B1_FOUNDATION
  QUALITY::[pytest::5/5,ruff::2_errors,mypy::pending]
  BLOCKERS::[error1|error2|dependency]
  NEXT::[fix_errors|run_tests|implement_feature]

KNOWLEDGE_ARTIFACT:
  META:
    TYPE::KNOWLEDGE_ARTIFACT
    VERSION::"1.0"
  FINDING_1::JSON_SCHEMA[WEAK|STRONG|NONE]
  FINDING_2::CUE[MEDIUM|STRONG|PARTIAL]
  VERDICT::synthesis_not_invention|gap_filled

§11::EXPECTED_RATIOS
COMPRESSION_METRICS:
  VS_PROSE::"5-10x reduction"
  VS_MARKDOWN::"1.5-3x reduction"
  VS_SCHEMA_MODE::"3-5x reduction"

MEASUREMENT:
  TOKENS_BEFORE::natural_language_prose
  TOKENS_AFTER::data_mode_octave
  RATIO::BEFORE/AFTER

§12::ANTI_PATTERNS
AVOID::[
  "Holographic pattern in data docs (L4 overhead)",
  "Verbose key names (use abbrev)",
  "Redundant nesting (flatten)",
  "Prose in values (convert to data)",
  "Repeated structure (use lists)"
]

§13::META_COMMENTARY
// Why this spec uses L2-L3 not L1
THIS_DOCUMENT:
  MODE::SCHEMA_L3[teaching_data_mode_requires_explanation]
  WHY::"Cannot teach compression using pure compression"
  PARADOX::"Teaching documents need teaching mode even when about compression"
  PRODUCTION_USAGE::"Actual data documents use L1"
  EXEMPLIFIES::"PROTOCOL_DEFINITION pattern"

===END===
