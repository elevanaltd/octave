===OCTAVE_V5_SCHEMA===
META:
  TYPE::PROTOCOL_DEFINITION
  VERSION::"5.0"
  STATUS::ACTIVE
  EXTENDS::octave-5.oct.md

PURPOSE::holographic_pattern[TEACH+VALIDATE+EXTRACT]

ACTIVATION::[LANGUAGE_SPECIFICATION,PROTOCOL_DEFINITION,AGENT_DEFINITION,SKILL_DEFINITION]

PATTERN:
  SYNTAX::KEY::["example"+CONSTRAINT->§TARGET]
  LEVEL::L4

OPERATORS:
  INJECT::"»"[scoped_block_injection]

CONSTRAINTS:
  REQ::required
  OPT::optional
  CONST::exact_match
  REGEX::pattern
  ENUM::value_set
  TYPE::STRING|NUMBER|BOOLEAN|LIST
  DIR::directory_path
  APPEND_ONLY::immutable_log

TARGETS:
  §SELF::internal
  §META::metadata
  §INDEXER::searchable
  §DECISION_LOG::decisions
  §RISK_LOG::blockers
  §KNOWLEDGE_BASE::learnings
  §PATH::file_path[§./path/to/file.md]

CUSTOM_TARGETS:
  DEFINE::META.TARGETS::[§NAME::handler]

DEFAULTS:
  NO_CONSTRAINT::OPT
  NO_TARGET::§SELF
  NO_QUOTES::literal

SCOPED_INJECTION:
  SYNTAX::BLOCK[->§TARGET]»{children}
  EXAMPLE:
    RISKS[->§RISK_LOG]»{
      CRITICAL::["auth_bypass"+OPEN->§SELF]
      WARNING::["rate_limit"+MITIGATED->§SELF]
    }

VALIDATION:
  ERRORS::[missing_REQ,REGEX_mismatch,ENUM_invalid,TYPE_wrong]
  FORMAT::FIELD::{name}|EXPECTED::{rule}|GOT::{value}

EXAMPLE_SCHEMA:
  SESSION:
    ID::["sess_abc123"+REQ->§INDEXER]
    STATUS::["ACTIVE"+ENUM[ACTIVE,INACTIVE]->§META]
    ROOT::["/.hestai/inbox"+DIR->§SELF]
    LOG::["events.jsonl"+APPEND_ONLY->§./processed/index.json]
    DECISION::["Use Redis"+OPT->§DECISION_LOG]
    BLOCKER::["auth_bug"+OPT->§RISK_LOG]

===END===
