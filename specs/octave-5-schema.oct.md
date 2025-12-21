===OCTAVE_V5_SCHEMA_PROFILE===
META:
  TYPE::PROTOCOL_DEFINITION
  VERSION::"5.0"
  STATUS::ACTIVE
  NAME::"OCTAVE Schema Profile"
  PURPOSE::"Holographic pattern for self-teaching, validating, extractable specs"
  EXTENDS::octave-5.oct.md

// =============================================================================
// SCHEMA PROFILE: The Holographic Pattern (Annotation Level 4)
// For specifications that must TEACH + VALIDATE + EXTRACT
// Heritage: Guardrails RAIL + CUE unified data + BDD self-exemplifying
// =============================================================================

§1::THREE_AXES_ACHIEVEMENT
// Research finding: OCTAVE achieves all three where others get only two
AXES:
  TEACH::[
    MECHANISM::"Embedded examples in every field definition",
    HERITAGE::FROM[CUE_unified_data|OpenAPI_examples],
    STRENGTH::STRONG
  ]
  VALIDATE::[
    MECHANISM::"Constraints (REQ|OPT|CONST|REGEX|ENUM|TYPE) per field",
    HERITAGE::FROM[JSON_Schema|SHACL|Pydantic],
    STRENGTH::STRONG
  ]
  EXTRACT::[
    MECHANISM::"Extraction targets (->§TARGET) route data to handlers",
    HERITAGE::FROM[function_calling|attribute_grammars],
    STRENGTH::STRONG
  ]

COMPARISON::[
  JSON_Schema::[WEAK,STRONG,NONE],
  CUE::[MEDIUM,STRONG,PARTIAL],
  Guardrails::[STRONG,STRONG,STRONG],
  OCTAVE_SCHEMA::[STRONG,STRONG,STRONG]
]

§2::WHEN_TO_USE
USE_CASES::[
  "Language and protocol specifications",
  "Agent constitutions and definitions",
  "Skill definitions with trigger patterns",
  "Validation schemas for data documents",
  "Self-documenting API contracts"
]

IMPLICIT_ACTIVATION::[
  TYPE::LANGUAGE_SPECIFICATION,
  TYPE::PROTOCOL_DEFINITION,
  TYPE::AGENT_DEFINITION,
  TYPE::SKILL_DEFINITION
]

§3::HOLOGRAPHIC_PATTERN
CORE_PATTERN:
  SYNTAX::"KEY:: [ EXAMPLE + CONSTRAINT -> §TARGET ]"
  ANNOTATION_LEVEL::L4

  COMPONENTS:
    EXAMPLE::"Concrete value demonstrating expected format"
    CONSTRAINT::"Validation rule applied to field"
    TARGET::"Extraction destination for routing"

  MEANING::"One line teaches syntax, defines validation, specifies extraction"

  HERITAGE:
    GUARDRAILS::"RAIL spec compiles to prompt instructions"
    BDD::"Scenarios ARE concrete examples (Gherkin)"
    CUE::"Types, values, constraints are all the same"

§4::CONSTRAINTS
CONSTRAINT_TYPES:
  REQ::   [ "required"        + CONST -> §SELF ] // Field must be present
  OPT::   [ "optional"        + CONST -> §SELF ] // Field may be absent
  CONST:: [ "exact_match"     + CONST -> §SELF ] // Value must match exactly
  REGEX:: [ "pattern_match"   + CONST -> §SELF ] // Value must match regex
  ENUM::  [ "value_from_set"  + CONST -> §SELF ] // Value from allowed list
  TYPE::  [ "STRING|NUMBER|BOOLEAN|LIST|TEXT" + CONST -> §SELF ]

§5::EXTRACTION_TARGETS
TARGETS:
  §SELF::     [ "Document internal reference"    + CONST -> §SELF ]
  §META::     [ "Document metadata index"        + CONST -> §SELF ]
  §INDEXER::  [ "Searchable knowledge base"      + CONST -> §SELF ]
  §DECISION_LOG:: [ "Architectural decisions"    + CONST -> §SELF ]
  §RISK_LOG::     [ "Blockers and risks"         + CONST -> §SELF ]
  §KNOWLEDGE_BASE:: [ "Learnings and insights"   + CONST -> §SELF ]

CUSTOM::"Define domain-specific targets in META.TARGETS"

§6::PROGRESSIVE_ANNOTATION
// Spectrum from L1 to L4 - add metadata as needed
LEVELS:
  L1:: [ "KEY::value"                           + CONST -> §SELF ]
  L2:: [ "KEY::value+REQ"                       + CONST -> §SELF ]
  L3:: [ "KEY::value+REQ->§INDEXER"             + CONST -> §SELF ]
  L4:: [ "KEY:: [ \"example\" + REQ -> §INDEXER ]" + CONST -> §SELF ]

DEFAULTS_WHEN_OMITTED:
  NO_CONSTRAINT::assumes_OPT
  NO_TARGET::assumes_§SELF
  NO_QUOTES::value_is_literal[not_example]

§7::EXAMPLES
SIMPLE_SCHEMA:
  ID::       [ "sess_abc123"  + REQ   -> §INDEXER ]
  STATUS::   [ "ACTIVE"       + ENUM[ACTIVE,DRAFT,ARCHIVED] -> §META ]
  TAGS::     [ ["ui","auth"]  + OPT   -> §INDEXER ]
  CREATED::  [ "2025-01-01"   + REGEX[^\d{4}-\d{2}-\d{2}$] -> §META ]

NESTED_SCHEMA:
  USER:
    NAME::   [ "John Doe"       + REQ   -> §INDEXER ]
    EMAIL::  [ "j@example.com"  + REGEX[^.+@.+$] -> §SELF ]
    ROLES::  [ ["admin"]        + TYPE::LIST -> §SELF ]

§8::VALIDATION_RULES
// Failure mode mitigation: ERROR_FEEDBACK_QUALITY
CRITICAL_ERRORS::[
  "Missing required field (REQ constraint violated)",
  "Value doesn't match REGEX pattern",
  "Value not in ENUM set",
  "Type mismatch (TYPE constraint violated)"
]

ERROR_FEEDBACK:
  PRINCIPLE::"Minimal-diff messages for retry loops"
  FORMAT::"FIELD::{field_name} EXPECTED::{constraint} GOT::{actual}"
  EXAMPLE::"FIELD::STATUS EXPECTED::ENUM[ACTIVE,DRAFT] GOT::active"

§9::SELF_EXEMPLIFYING_PROPERTY
// Heritage: BDD/Gherkin - "scenarios ARE examples"
HOLOGRAPHIC_PRINCIPLE:
  STATEMENT::"This document is written in the format it defines"
  IMPLICATION::"Parsers can use the spec as test input"
  BENEFIT::"No separate examples needed; the spec IS the example"
  VALIDATION::"Run spec through its own validator"

§10::INTEGRATION_WITH_DATA_MODE
SCHEMA_DATA_RELATIONSHIP:
  SCHEMA::"Defines structure with holographic pattern (L4)"
  DATA::"Instances use minimal syntax (L1), validated against schema"

  REFERENCE_MECHANISM:
    IN_DATA::"META.SCHEMA::path/to/schema.oct.md"
    EFFECT::"Parser validates DATA fields against SCHEMA constraints"

§11::LLM_ENFORCEMENT_STRATEGY
// Research: CONSTRAINED_DECODING vs VALIDATE_AND_REPAIR
RECOMMENDED_APPROACH::HYBRID

STRATEGIES:
  CONSTRAINED_DECODING::[
    TOOLS::[Guidance,Outlines,function_calling],
    USE_WHEN::"Critical fields that must be valid first-pass",
    INJECT::"L4 fields into system prompt or function schema"
  ]
  VALIDATE_AND_REPAIR::[
    TOOLS::[Guardrails,Pydantic,custom_validators],
    USE_WHEN::"Large schemas where token budget matters",
    INJECT::"Minimal L2 hints; validate full schema post-generation"
  ]

§12::META_COMMENTARY
// Why this spec uses L4 holographic throughout
THIS_DOCUMENT:
  MODE::SCHEMA_L4[full_holographic]
  WHY::"Maximum teaching; demonstrates every pattern it defines"
  EXEMPLIFIES::"Self-exemplifying principle; spec IS example"
  PARADOX::"None - teaching schemas should use teaching mode"
  TOKEN_COST::"Acceptable; this is reference documentation"

===END===
