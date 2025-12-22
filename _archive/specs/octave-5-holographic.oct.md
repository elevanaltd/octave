===OCTAVE_V5_HOLOGRAPHIC===
META:
  TYPE::PROTOCOL_DEFINITION
  VERSION::"5.0"
  STATUS::DRAFT
  PURPOSE::"Holographic Tuple Specification - Schema teaches syntax"

// OCTAVE-V5 HOLOGRAPHIC TUPLE SPECIFICATION
// "The Definition of the Format, Written in the Format."

§1::CORE_PATTERN
// HOLOGRAPHIC PATTERN: KEY:: [ EXAMPLE + CONSTRAINT -> §TARGET ]
// One line teaches syntax, defines schema, specifies extraction.
CORE:: [
  SYNTAX::    [ [KEY, "::", TUPLE] -> §DEFINITION ],
  TUPLE::     [ ["[", EXAMPLE, "+", CONSTRAINT, "->", "§TARGET", "]"] -> §STRUCTURE ],
  OPERATORS:: [
    "::" -> "ASSIGNS",
    "[]" -> "CONTAINS_SCOPE",
    "+"  -> "SYNTHESIZES",
    "->" -> "MAPS_FLOW",
    "§"  -> "REFERENCES_TARGET",
    "»"  -> "INJECTS_BLOCK"
  ]
]

§2::CONSTRAINTS
// Available constraint tokens
CONSTRAINTS:: [
  REQ   -> "Field is required",
  OPT   -> "Field is optional",
  CONST -> "Value must match exactly",
  ENUM  -> "Value from set",
  REGEX -> "Value matches pattern"
]

§3::TARGETS
// Extraction targets (where data flows)
TARGETS:: [INDEXER, DECISION_LOG, RISK_LOG, META, SELF]

§4::SCHEMA_EXAMPLE
// SESSION_CONTEXT schema using holographic tuples
SESSION_CONTEXT:: [
  ID::          [ "sess_abc123" + REQ -> §INDEXER ],
  STATUS::      [ "ACTIVE" + REQ -> §INDEXER ],
  TAGS::        [ ["ui", "auth"] + OPT -> §INDEXER ],
  ROOT_PATH::   [ "/.hestai/inbox" + DIR -> §SELF ],
  EVENT_LOG::   [ LIST + APPEND_ONLY -> §./processed/index.json ],
  DECISION::    [ "Use Redis for caching" + OPT -> §DECISION_LOG ],
  BLOCKER::     [ "auth_bug" + OPT -> §RISK_LOG ]
]

§5::SCOPED_INJECTION
// Scoped blocks for grouped extraction
RISKS [-> §.hestai/context/PROJECT-RISKS.md] » {
  CRITICAL:: [ "Policy Bypass" + MITIGATED -> §tests/policy_test.py ]
  WARNING::  [ "Rate limit gap" + OPEN -> §RISK_LOG ]
}

===END===
