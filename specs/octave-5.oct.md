===OCTAVE_V5===
META:
  TYPE::LANGUAGE_SPECIFICATION
  VERSION::"5.0"
  STATUS::ACTIVE

ENVELOPE:
  HEADER::===NAME===
  FOOTER::===END===
  META::required[first_block]

OPERATORS:
  ASSIGN::"::"
  BLOCK::":"
  LIST::"[]"
  PIPE::"|"
  FLOW::"->"
  COMBINE::"+"
  TENSION::"_VERSUS_"
  ANCHOR::"§"
  COMMENT::"//"

TYPES:
  STRING::bare_word|"quoted"
  NUMBER::42|3.14|-1e10
  BOOLEAN::true|false
  NULL::null
  LIST::[a,b,c]|a|b|c

STRUCTURE:
  INDENT::2_spaces
  KEYS::alphanumeric_underscore
  NESTING::unlimited

CONSTRAINTS:
  REQ::required
  OPT::optional
  CONST::exact_match
  REGEX::pattern[^\d+$]
  ENUM::set[a,b,c]
  TYPE::STRING|NUMBER|BOOLEAN|LIST

TARGETS:
  §SELF::internal
  §META::metadata
  §INDEXER::searchable
  §DECISION_LOG::decisions
  §KNOWLEDGE_BASE::learnings

MODES:
  SCHEMA::[LANGUAGE_SPECIFICATION,PROTOCOL_DEFINITION,AGENT_DEFINITION,SKILL_DEFINITION]
  DATA::[SESSION_CONTEXT,KNOWLEDGE_ARTIFACT,CONFIGURATION]

LEVELS:
  L1::KEY::value
  L2::KEY::value+CONSTRAINT
  L3::KEY::value+CONSTRAINT->§TARGET
  L4::KEY::["example"+CONSTRAINT->§TARGET]

SEVERITY:
  ERROR::invalid
  WARNING::issues
  INFO::suggestion

EXAMPLE:
  SESSION:
    ID::sess_abc123
    STATUS::ACTIVE
    PHASE::B1_FOUNDATION
    QUALITY::[tests::5/5,lint::passing]
    FLOW::[INIT->BUILD->DEPLOY]
    BLOCKERS::none

===END===
