===OCTAVE_SCHEMA_SPEC===
META:
  TYPE::PROTOCOL_EXTENSION
  PARENT::"specs/octave-4.oct.md"
  VERSION::"1.3"
  PURPOSE::"Minimal DSL for Schema & Extraction Contracts"

// 1.0_MECHANICS
MECHANICS:
  TOKENIZATION::"Double-quoted strings ATOMIC. Schema=[Shape]->Flow. Data=Key::Value."
  ENCODING:
    STRING_ESCAPE::"\" = \\\" | \\ = \\\\ | newline = \n | tab = \t. Literal newlines forbidden."
    MULTILINE_LIST::"Indented block for TYPE(LIST): each line is one quoted string element."
    MULTILINE_TEXT::"Indented block for TYPE(TEXT): raw lines joined with \n, operators must be quoted."
    BLOCK_END::"Dedent terminates block."
    WHITESPACE::"2-space indent, tabs forbidden, trailing spaces trimmed."

// 2.0_SCHEMA_DSL_STRUCTURE
DEF_SCHEMA:
  POLICY:
    VERSION::[REQ, STRING]
    UNKNOWN_FIELDS::[REQ, ENUM(REJECT, IGNORE, WARN)]
    TARGETS::[REQ, LIST]
    UNKNOWN_TARGET::[REQ, ENUM(FAIL, WARN)]

  FIELDS:
    PATTERN::"KEY :: [ SHAPE_CONSTRAINTS ] -> EXTRACTION_TARGET"
    SHAPE::"REQ|OPT, CONST(x), REGEX(r), TYPE(t), ENUM(a,b)"

// 3.0_GOLDEN_EXAMPLE
SESSION_CONTEXT_SCHEMA:
  POLICY:
    VERSION::"1.0"
    UNKNOWN_FIELDS::REJECT
    TARGETS::[INDEXER, DECISION_LOG, RISK_LOG]

  FIELDS:
    // Shape (Validation) -------------------------> Flow (Extraction)
    ID       :: [REQ, REGEX:"^sess_[a-z0-9]+"] -> INDEXER
    STATUS   :: [REQ, ENUM(ACTIVE, ARCHIVED)]  -> INDEXER
    DECISION :: [OPT, TYPE(TEXT)]              -> DECISION_LOG
    NOTES    :: [OPT, TYPE(LIST)]              -> INDEXER

===END===
