===OCTAVE_V5===
// OCTAVE v5 complete reference (~200 tokens)

META:
  VERSION::"5.0"
  PURPOSE::"LLM-optimized syntax reference"

ENVELOPE:
  START::===NAME===
  META::TYPE+VERSION+STATUS[required]
  END::===END===

SYNTAX:
  ASSIGN::KEY::value
  BLOCK::KEY:[indent_2_spaces]
  LIST::[a,b,c]|a|b|c
  FLOW::->
  COMBINE::+[binary_only]
  ANCHOR::§
  COMMENT:://

TYPES::STRING|NUMBER|true|false|null|LIST

MODES:
  SCHEMA::[LANGUAGE_SPECIFICATION,PROTOCOL_DEFINITION,AGENT_DEFINITION]
  DATA::[SESSION_CONTEXT,KNOWLEDGE_ARTIFACT,CONFIGURATION]

SCHEMA_PATTERN::"KEY::[ example + CONSTRAINT -> §TARGET ]"
DATA_PATTERN::"KEY::value"

CONSTRAINTS::REQ|OPT|CONST|REGEX[pattern]|ENUM[a,b,c]|TYPE

TARGETS::§SELF|§META|§INDEXER|§DECISION_LOG|§KNOWLEDGE_BASE

COMPRESSION:
  PRESERVE::[numbers,names,codes,operators]
  DROP::[articles,prepositions]
  ABBREV::[impl,config,DONE,WIP,PENDING]

EXAMPLE_SCHEMA:
  ID::["sess_123"+REQ->§INDEXER]
  STATUS::["ACTIVE"+ENUM[ACTIVE,DRAFT]->§META]

EXAMPLE_DATA:
  PHASE::B1_FOUNDATION
  STATUS::[pytest::5/5,ruff::2_errors]
  NEXT::[fix_errors|deploy]

===END===
