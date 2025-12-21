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
// =============================================================================

§1::DESIGN_PRINCIPLES
PRINCIPLES:
  P1::MINIMAL_CORE[syntax_only|profiles_extend]
  P2::COMPRESSION_BY_DEFAULT[no_overhead_unless_needed]
  P3::PROGRESSIVE_ANNOTATION[add_metadata_optionally]
  P4::IMPLICIT_MODE[TYPE_determines_parsing]
  P5::LLM_LEGIBLE[familiar_patterns|predictable_structure]

§2::DOCUMENT_ENVELOPE
ENVELOPE:
  HEADER::"===DOCUMENT_NAME===" // First non-whitespace line
  FOOTER::"===END===" // Last non-whitespace line
  META::REQUIRED[immediately_after_header]
  ENCODING::UTF-8

§3::META_BLOCK
META_REQUIREMENTS:
  REQUIRED::[TYPE,VERSION,STATUS]
  OPTIONAL::[NAME,PURPOSE,MODE,SCHEMA]

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

§4::OPERATORS
OPERATORS:
  ASSIGN::"::"          // KEY::VALUE
  BLOCK::":"            // KEY: starts indented block
  LIST::"[]"            // [a,b,c] or [a|b|c]
  PIPE::"|"             // Lightweight list separator
  FLOW::"->"            // Progression or extraction
  SYNTHESIZE::"+"       // Binary combination (A+B only)
  TENSION::"_VERSUS_"   // Opposition/tradeoff
  REFERENCE::"§"        // Section anchor
  COMMENT::"//"         // Line comment

§5::DATA_TYPES
TYPES:
  STRING::bare_word|"quoted with spaces"
  NUMBER::42|3.14|-1e10
  BOOLEAN::true|false   // lowercase only
  NULL::null            // lowercase only
  LIST::[a,b,c]|a|b|c   // Bracket or pipe form

§6::HIERARCHY
STRUCTURE:
  INDENTATION::2_spaces_per_level
  NESTING::unlimited_depth
  KEYS::alphanumeric_underscore[no_colon|no_space]
  CASE::preserved_case_sensitive

§7::MODE_SYSTEM
MODE_DETERMINATION:
  IMPLICIT_FROM_TYPE::[
    SCHEMA_MODE::[LANGUAGE_SPECIFICATION,PROTOCOL_DEFINITION,AGENT_DEFINITION,SKILL_DEFINITION],
    DATA_MODE::[SESSION_CONTEXT,KNOWLEDGE_ARTIFACT,CONFIGURATION]
  ]
  EXPLICIT_OVERRIDE::"MODE::SCHEMA or MODE::DATA in META"

MODE_EFFECTS:
  SCHEMA_MODE::extends[octave-5-schema.oct.md]
  DATA_MODE::extends[octave-5-data.oct.md]

§8::SECTION_ANCHORS
ANCHORS:
  SYNTAX::"§{N}::{NAME}"
  EXAMPLE::§1::INTRODUCTION
  PURPOSE::navigation|extraction|reference

§9::KNOWLEDGE_ARTIFACTS
EXTRACTABLE_PATTERNS:
  DECISION::"DECISION_{N}::content"
  BLOCKER::"{ID}⊗{status}[details]"
  LEARNING::"LEARNING::content"

§10::VALIDATION_SEVERITY
SEVERITY:
  ERROR::document_invalid
  WARNING::valid_with_issues
  INFO::suggestion

===END===
