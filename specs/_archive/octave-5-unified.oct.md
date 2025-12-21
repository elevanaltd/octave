===OCTAVE_V5===
META:
  TYPE::      [ "PROTOCOL_DEFINITION" + CONST -> META ]
  VERSION::   [ "5.0"                 + REQ   -> META ]
  STATUS::    [ "DRAFT"               + REQ   -> META ]
  PURPOSE::   [ "Self-teaching holographic DSL" + OPT -> META ]

// =============================================================================
// OCTAVE v5: THE HOLOGRAPHIC PATTERN
// "This document is written in the format it defines."
// =============================================================================

POLICY:
  VERSION::        [ "5.0"   + REQ -> SELF ]
  UNKNOWN_FIELDS:: [ "WARN"  + REQ -> SELF ]
  TARGETS::        [ [META, SELF, INDEXER, DECISION_LOG, RISK_LOG] + REQ -> SELF ]

// 1.0 THE PATTERN
PATTERN:
  DEFINITION:: [ "KEY:: [ EXAMPLE + CONSTRAINT -> TARGET ]" + CONST -> SELF ]
  COMPONENTS:: [
    EXAMPLE::    [ "concrete_value"  + REQ -> "Teaches expected format" ],
    CONSTRAINT:: [ "REQ|OPT|REGEX"   + REQ -> "Validates input" ],
    TARGET::     [ "INDEXER"         + REQ -> "Extraction destination" ]
  ]

// 2.0 CONSTRAINTS
CONSTRAINTS:
  REQ::   [ "required"       + CONST -> SELF ]
  OPT::   [ "optional"       + CONST -> SELF ]
  REGEX:: [ "pattern_match"  + CONST -> SELF ]
  ENUM::  [ "value_from_set" + CONST -> SELF ]
  TYPE::  [ "STRING|LIST|TEXT" + CONST -> SELF ]
  CONST:: [ "exact_match"    + CONST -> SELF ]

// 3.0 MECHANICS
MECHANICS:
  TOKENIZATION:: [ "Double-quoted strings are ATOMIC" + CONST -> SELF ]
  ESCAPES::      [ ["\\\"", "\\\\", "\\n", "\\t"]     + CONST -> SELF ]
  NEWLINES::     [ "forbidden_in_strings"             + CONST -> SELF ]
  MULTILINE::    [ "indented_block_per_line"          + CONST -> SELF ]
  WHITESPACE::   [ "2_space_indent_no_tabs"           + CONST -> SELF ]
  COMMENTS::     [ "line_start_only"                  + CONST -> SELF ]

// 4.0 SCHEMA EXAMPLE (how to define a document type)
SESSION_CONTEXT_SCHEMA:
  POLICY:
    VERSION::        [ "1.0"    + REQ -> SELF ]
    UNKNOWN_FIELDS:: [ "REJECT" + REQ -> SELF ]
    TARGETS::        [ [INDEXER, DECISION_LOG, RISK_LOG] + REQ -> SELF ]

  FIELDS:
    ID::       [ "sess_abc123"  + REQ   -> INDEXER ]
    STATUS::   [ "ACTIVE"       + REQ   -> INDEXER ]
    TAGS::     [ ["ui", "auth"] + OPT   -> INDEXER ]
    DECISION:: [ "Use Redis"    + OPT   -> DECISION_LOG ]
    BLOCKER::  [ "auth_bug"     + OPT   -> RISK_LOG ]

// 5.0 DATA INSTANCE (how documents use simple KEY::VALUE)
DATA_FORMAT:
  RULE:: [ "Data uses KEY::VALUE only, no tuples" + CONST -> SELF ]
  EXAMPLE:: [
    "ID::sess_abc123",
    "STATUS::ACTIVE",
    "TAGS::[ui, auth]",
    "DECISION::Use Redis for caching"
  ]

===END===
