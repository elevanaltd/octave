===OCTAVE_V5_SCHEMA_PROFILE===
META:
  TYPE::PROTOCOL_DEFINITION
  VERSION::"5.0"
  STATUS::ACTIVE
  NAME::"OCTAVE Schema Profile"
  PURPOSE::"Holographic pattern for validation, extraction, and self-teaching specs"
  EXTENDS::octave-5.oct.md

// =============================================================================
// SCHEMA PROFILE: The Holographic Pattern
// For specifications that must TEACH + VALIDATE + EXTRACT
// Activated implicitly for: LANGUAGE_SPECIFICATION, PROTOCOL_DEFINITION,
//                           AGENT_DEFINITION, SKILL_DEFINITION
// =============================================================================

§1::WHEN_TO_USE
USE_CASES::[
  "Language/protocol specifications",
  "Agent constitutions and definitions",
  "Skill definitions with trigger patterns",
  "Validation schemas",
  "Self-documenting API contracts"
]

CHARACTERISTICS:
  SELF_TEACHING::true   // Document teaches its own format
  VALIDATION::embedded  // Constraints are part of syntax
  EXTRACTION::explicit  // Targets specified per field
  TOKEN_PRIORITY::secondary // Clarity over compression

§2::HOLOGRAPHIC_PATTERN
CORE_PATTERN:
  SYNTAX::"KEY:: [ EXAMPLE + CONSTRAINT -> §TARGET ]"

  COMPONENTS:
    EXAMPLE::"Concrete value demonstrating expected format"
    CONSTRAINT::"Validation rule (REQ|OPT|CONST|REGEX|ENUM|TYPE)"
    TARGET::"Extraction destination (§SELF|§INDEXER|§DECISION_LOG|§RISK_LOG)"

  MEANING::"One line teaches syntax, defines validation, specifies extraction"

§3::CONSTRAINTS
CONSTRAINT_TYPES:
  REQ::required_field
  OPT::optional_field
  CONST::exact_match_only
  REGEX::pattern_match
  ENUM::value_from_set
  TYPE::STRING|NUMBER|BOOLEAN|LIST|TEXT

§4::EXTRACTION_TARGETS
TARGETS:
  §SELF::document_internal_reference
  §META::document_metadata_index
  §INDEXER::searchable_knowledge_base
  §DECISION_LOG::architectural_decisions
  §RISK_LOG::blockers_and_risks
  §KNOWLEDGE_BASE::learnings_and_insights

CUSTOM_TARGETS::"Define in META.TARGETS for domain-specific routing"

§5::PROGRESSIVE_ANNOTATION
DEFAULTS:
  NO_CONSTRAINT::assumes_OPT
  NO_TARGET::assumes_§SELF
  NO_QUOTES::value_is_literal_not_example

SHORTHAND_LEVELS:
  MINIMAL::"KEY::value"                           // Just data
  CONSTRAINED::"KEY::value+REQ"                   // Add validation
  TARGETED::"KEY::value+REQ->§INDEXER"            // Add extraction
  FULL::"KEY:: [ \"example\" + REQ -> §INDEXER ]" // Full holographic

§6::EXAMPLES
SIMPLE_SCHEMA:
  ID::       [ "sess_abc123" + REQ   -> §INDEXER ]
  STATUS::   [ "ACTIVE"      + ENUM[ACTIVE,DRAFT,ARCHIVED] -> §META ]
  TAGS::     [ ["ui","auth"] + OPT   -> §INDEXER ]
  CREATED::  [ "2025-01-01"  + REGEX[^\d{4}-\d{2}-\d{2}$] -> §META ]

NESTED_SCHEMA:
  USER:
    NAME::   [ "John Doe"    + REQ   -> §INDEXER ]
    EMAIL::  [ "j@example.com" + REGEX[^.+@.+$] -> §SELF ]
    ROLES::  [ ["admin"]     + TYPE::LIST -> §SELF ]

§7::VALIDATION_RULES
CRITICAL_ERRORS::[
  "Missing required field (REQ constraint violated)",
  "Value doesn't match REGEX pattern",
  "Value not in ENUM set",
  "Type mismatch (TYPE constraint violated)"
]

WARNINGS::[
  "Unknown extraction target",
  "Constraint on optional field that's missing"
]

§8::SELF_DOCUMENTING_PROPERTY
HOLOGRAPHIC_PRINCIPLE:
  STATEMENT::"This document is written in the format it defines"
  IMPLICATION::"Parsers can use the spec as test input"
  BENEFIT::"No separate examples needed; the spec IS the example"

§9::INTEGRATION_WITH_DATA_MODE
SCHEMA_DATA_RELATIONSHIP:
  SCHEMA::"Defines structure with holographic pattern"
  DATA::"Instances validated against schema, use minimal syntax"

  DATA_REFERENCES_SCHEMA:
    MECHANISM::"META.SCHEMA::path/to/schema.oct.md"
    VALIDATION::"Data fields checked against schema constraints"

===END===
