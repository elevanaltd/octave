===OCTAVE_V5===
META:
  TYPE::LANGUAGE_SPECIFICATION
  VERSION::"5.0"
  STATUS::ACTIVE
  NAME::"OCTAVE (Olympian Common Text And Vocabulary Engine)"
  PURPOSE::"Minimal core DSL for structured LLM communication"

// =============================================================================
// OCTAVE v5 CORE: The Lightest Weight Foundation
// This document defines ONLY universal syntax. Profiles extend this.
// Self-exemplifying: written in the format it defines.
// =============================================================================

§1::DESIGN_PRINCIPLES
PRINCIPLES:
  P1::MINIMAL_CORE[syntax_only|profiles_extend]
  P2::COMPRESSION_BY_DEFAULT[no_overhead_unless_needed]
  P3::PROGRESSIVE_ANNOTATION[add_metadata_optionally]
  P4::IMPLICIT_MODE[TYPE_determines_parsing]
  P5::LLM_LEGIBLE[familiar_patterns|predictable_structure]

§2::HERITAGE_AND_PROVENANCE
// OCTAVE synthesizes proven patterns, not reinventing wheels
HERITAGE:
  VALIDATION_PATTERNS::FROM[JSON_Schema|CUE|SHACL]
  EXAMPLE_APPROACH::FROM[CUE_unified_data|OpenAPI_examples]
  EXECUTION_SEMANTICS::FROM[function_calling|attribute_grammars]
  SELF_EXEMPLIFYING::FROM[BDD_Gherkin|"scenarios_ARE_examples"]
  COMPRESSION::FROM[LLMLingua|telegram_style]

UNIQUE_SYNTHESIS:
  ACHIEVEMENT::"TEACH + VALIDATE + EXTRACT in single artifact"
  COMPARISON::[
    JSON_Schema::WEAK|STRONG|NONE,
    CUE::MEDIUM|STRONG|PARTIAL,
    Guardrails::STRONG|STRONG|STRONG,
    OCTAVE::STRONG|STRONG|STRONG
  ]

§3::DOCUMENT_ENVELOPE
ENVELOPE:
  HEADER::"===DOCUMENT_NAME===" // First non-whitespace line
  FOOTER::"===END===" // Last non-whitespace line
  META::REQUIRED[immediately_after_header]
  ENCODING::UTF-8

§4::META_BLOCK
META_REQUIREMENTS:
  REQUIRED::[TYPE,VERSION,STATUS]
  OPTIONAL::[NAME,PURPOSE,MODE,SCHEMA,EXTENDS]

TYPE_VALUES::[
  LANGUAGE_SPECIFICATION,
  PROTOCOL_DEFINITION,
  AGENT_DEFINITION,
  SKILL_DEFINITION,
  SESSION_CONTEXT,
  KNOWLEDGE_ARTIFACT,
  CONFIGURATION
]

STATUS_VALUES::[ACTIVE,DRAFT,DEPRECATED,ARCHIVED]

§5::OPERATORS
OPERATORS:
  ASSIGN::"::"          // KEY::VALUE
  BLOCK::":"            // KEY: starts indented block
  LIST::"[]"            // [a,b,c] or [a|b|c]
  PIPE::"|"             // Lightweight list separator (saves 4+ tokens)
  FLOW::"->"            // Progression or extraction target
  SYNTHESIZE::"+"       // Binary combination (A+B only, no chaining)
  TENSION::"_VERSUS_"   // Opposition/tradeoff
  REFERENCE::"§"        // Section anchor
  COMMENT::"//"         // Line comment

§6::DATA_TYPES
TYPES:
  STRING::bare_word|"quoted with spaces"
  NUMBER::42|3.14|-1e10
  BOOLEAN::true|false   // lowercase only
  NULL::null            // lowercase only
  LIST::[a,b,c]|a|b|c   // Bracket or pipe form

§7::HIERARCHY
STRUCTURE:
  INDENTATION::2_spaces_per_level[strict]
  NESTING::unlimited_depth
  KEYS::alphanumeric_underscore[no_colon|no_space]
  CASE::preserved_case_sensitive

§8::ANNOTATION_SPECTRUM
// Progressive disclosure: from minimal to full holographic
LEVELS:
  L0::bare_yaml                    // No OCTAVE features
  L1::"KEY::value"                 // Basic syntax only
  L2::"KEY::value+CONSTRAINT"      // Add validation
  L3::"KEY::value+CONSTRAINT->§X"  // Add extraction
  L4::"KEY:: [ example + CONST -> §TARGET ]" // Full holographic

MODE_DEFAULTS:
  SCHEMA_MODE::L4[teaching_priority]
  DATA_MODE::L1[compression_priority]
  HYBRID::explicit_level_per_field

§9::MODE_SYSTEM
MODE_DETERMINATION:
  IMPLICIT_FROM_TYPE::[
    SCHEMA_MODE::[LANGUAGE_SPECIFICATION,PROTOCOL_DEFINITION,AGENT_DEFINITION,SKILL_DEFINITION],
    DATA_MODE::[SESSION_CONTEXT,KNOWLEDGE_ARTIFACT,CONFIGURATION]
  ]
  EXPLICIT_OVERRIDE::"MODE::SCHEMA or MODE::DATA in META"

PROFILE_EXTENSIONS:
  SCHEMA_MODE::SEE[octave-5-schema.oct.md]
  DATA_MODE::SEE[octave-5-data.oct.md]
  EXECUTION::SEE[octave-5-execution.oct.md]

§10::SECTION_ANCHORS
ANCHORS:
  SYNTAX::"§{N}::{NAME}"
  EXAMPLE::§1::INTRODUCTION
  PURPOSE::navigation|extraction|reference

§11::KNOWLEDGE_ARTIFACTS
EXTRACTABLE_PATTERNS:
  DECISION::"DECISION_{N}::content"
  BLOCKER::"{ID}⊗{status}[details]"
  LEARNING::"LEARNING::content"

§12::VALIDATION_SEVERITY
SEVERITY:
  ERROR::document_invalid[blocks_processing]
  WARNING::valid_with_issues[allows_processing]
  INFO::suggestion[no_block]

§13::FAILURE_MODES
// Research-validated risks with mitigations
FAILURE_MODES:
  COMPLEXITY_TRAP:
    RISK::"Spec becomes programming language"
    MITIGATION::"Keep declarative; limit to 80% use cases"
    ENFORCEMENT::"No conditionals, loops, or Turing-complete features"

  SPEC_DRIFT:
    RISK::"Spec and implementation diverge"
    MITIGATION::"Spec must DRIVE execution, not describe it"
    ENFORCEMENT::"Executable specs via parser/validator/router"

  LLM_MISINTERPRETATION:
    RISK::"Model ignores or misunderstands terse syntax"
    MITIGATION::"Include meta-spec; validate all output"
    ENFORCEMENT::"Self-exemplifying documents"

  SCALABILITY:
    RISK::"Large specs consume excessive prompt tokens"
    MITIGATION::"Selective injection; two-pass validation"
    ENFORCEMENT::"DATA mode for operational context"

  VALID_BUT_WRONG:
    RISK::"Structurally valid but semantically incorrect"
    MITIGATION::"Semantic validators beyond structure"
    ENFORCEMENT::"Application-layer validation hooks"

§14::META_COMMENTARY
// Why this spec uses SCHEMA mode at L3
THIS_DOCUMENT:
  MODE::SCHEMA_L3[constraints_and_structure|minimal_examples]
  WHY::"Teaching priority; spec must self-document"
  EXEMPLIFIES::"LANGUAGE_SPECIFICATION pattern"
  DEMONSTRATES::"Core syntax without holographic overhead"

===END===
