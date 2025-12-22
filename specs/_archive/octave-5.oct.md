===OCTAVE_V5===
META:
  TYPE::LANGUAGE_SPECIFICATION
  VERSION::"5.0.0"
  STATUS::ACTIVE
  NAME::"OCTAVE (Olympian Common Text And Vocabulary Engine)"
  PURPOSE::"Structured protocol for AI communication with mythological vocabulary"

// =============================================================================
// OCTAVE v5: CORE LANGUAGE SPECIFICATION
// "The definition of the format, written in the format."
// =============================================================================

§1::ENVELOPE
ENVELOPE:
  HEADER::===NAME===
  FOOTER::===END===
  META::required[first_block_after_header]
  ENCODING::UTF-8

§2::OPERATORS
OPERATORS:
  ASSIGN:
    SYMBOL::"::"
    MEANING::assigns_value_to_key
    EXAMPLE::STATUS::ACTIVE

  BLOCK:
    SYMBOL::":"
    MEANING::opens_indented_block
    EXAMPLE::CONFIG:[newline+indent]

  LIST:
    SYMBOL::"[]"
    MEANING::contains_ordered_elements
    EXAMPLE::[a,b,c]

  PIPE:
    SYMBOL::"|"
    MEANING::alternative_or_broadcast
    EXAMPLE::a|b|c

  FLOW:
    SYMBOL::"->"
    MEANING::sequential_transformation
    USAGE::list_context_only
    EXAMPLE::[INIT->BUILD->DEPLOY]

  COMBINE:
    SYMBOL::"+"
    MEANING::synthesizes_elements_into_whole
    USAGE::binary_only[no_chaining]
    EXAMPLE::APOLLO+HERMES

  CONSTRAINT_CHAIN:
    SYMBOL::"&"
    MEANING::logical_AND_for_constraints
    USAGE::left_to_right[fail_fast]
    EXAMPLE::REQ&TYPE(STRING)&REGEX[^\w+$]

  TENSION:
    SYMBOL::"_VERSUS_"
    MEANING::creative_opposition
    USAGE::binary_only[no_chaining]
    EXAMPLE::SPEED _VERSUS_ RELIABILITY

  ANCHOR:
    SYMBOL::"§"
    MEANING::references_target_or_section
    EXAMPLE::§INDEXER

  INJECT:
    SYMBOL::"»"
    MEANING::injects_block_content
    EXAMPLE::TEMPLATE»{children}

  COMMENT:
    SYMBOL::"//"
    MEANING::line_comment
    PLACEMENT::line_start_or_after_value

§3::TYPES
TYPES:
  STRING:
    BARE::identifier_no_spaces
    QUOTED::"text with spaces"
    ESCAPES::["\\\"","\\\\","\\n","\\t"]

  NUMBER:
    VALID::[42,3.14,-1e10]
    QUOTE_REQUIRED::["0xFF","0o755","0b1010"]

  BOOLEAN::[true,false][lowercase_only]

  NULL::null[lowercase_only]

  LIST::[a,b,c]|a|b|c

§4::STRUCTURE
STRUCTURE:
  INDENT::2_spaces[no_tabs]
  KEYS::alphanumeric_underscore[start_with_letter_or_underscore]
  NESTING::unlimited
  NEWLINES::forbidden_in_strings[use_escapes]

§5::MODES
MODES:
  SCHEMA:
    TYPES::[LANGUAGE_SPECIFICATION,PROTOCOL_DEFINITION,AGENT_DEFINITION,SKILL_DEFINITION]
    PATTERN::"KEY::[ example + CONSTRAINT -> §TARGET ]"
    LEVEL::L4

  DATA:
    TYPES::[SESSION_CONTEXT,KNOWLEDGE_ARTIFACT,CONFIGURATION]
    PATTERN::"KEY::value"
    LEVEL::L1|L2

§6::LEVELS
LEVELS:
  L1:
    PATTERN::KEY::value
    EXAMPLE::STATUS::ACTIVE

  L2:
    PATTERN::KEY::value&CONSTRAINT
    EXAMPLE::STATUS::ACTIVE&REQ

  L3:
    PATTERN::KEY::value&CONSTRAINT->§TARGET
    EXAMPLE::STATUS::ACTIVE&REQ->§META

  L4:
    PATTERN::KEY::["example"&CONSTRAINT->§TARGET]
    EXAMPLE::STATUS::["ACTIVE"&REQ&ENUM[ACTIVE,INACTIVE]->§META]
    USAGE::schema_definitions_only

§7::CONSTRAINTS
CONSTRAINTS:
  REQ::required[field_must_be_present]
  OPT::optional[field_may_be_absent]
  CONST::exact_match[value_must_equal]
  REGEX::pattern[value_must_match]
  ENUM::value_set[value_in_list]
  TYPE::STRING|NUMBER|BOOLEAN|LIST
  DIR::directory_path
  APPEND_ONLY::immutable_log

CONSTRAINT_STACKING:
  OPERATOR::"&"[logical_AND]
  EVALUATION::left_to_right[fail_fast]
  CONFLICTS::[
    IMPOSSIBLE::"ENUM[A,B]&CONST[C]"->ERROR,
    REDUNDANT::"TYPE(X)&TYPE(X)"->WARNING
  ]
  ERROR_FORMAT::"CONSTRAINT_CHAIN::{index}|{name}|EXPECTED::{rule}|GOT::{value}"

§8::TARGETS
TARGETS:
  BUILTIN::[§SELF,§META,§INDEXER,§DECISION_LOG,§RISK_LOG,§KNOWLEDGE_BASE]

  §SELF::internal[stays_in_document]
  §META::metadata[document_properties]
  §INDEXER::searchable[discovery_service]
  §DECISION_LOG::decisions[architectural_choices]
  §RISK_LOG::blockers[issues_and_risks]
  §KNOWLEDGE_BASE::learnings[captured_insights]
  §PATH::file_path[§./path/to/file.md]

  CUSTOM:
    DEFINE::META.TARGETS::[§NAME::handler]
    EXAMPLE::META.TARGETS::[§AUDIT::audit_service.log]

§9::SEVERITY
SEVERITY:
  ERROR::invalid[must_fix_before_proceed]
  WARNING::issues[should_fix]
  INFO::suggestion[may_improve]

§10::VALIDATION
VALIDATION:
  STEPS::[
    CHECK_ENVELOPE->header_and_footer_present,
    VALIDATE_META->required_keys_by_type,
    VALIDATE_CONSTRAINTS->all_constraints_pass,
    EXTRACT_ARTIFACTS->route_to_targets,
    REPORT->VALID|INVALID|WARNINGS
  ]

  UNKNOWN_FIELDS::[REJECT,IGNORE,WARN]
  UNKNOWN_TARGET::[FAIL,WARN]

§11::MODULARITY
MODULARITY:
  EXTENDS:
    SYNTAX::EXTENDS::parent_spec.oct.md
    SEMANTICS::adds_not_overrides
    CORE_UNCHANGED::[operators,constraints,envelope,types]

  SISTER_MODULES::[
    octave-5-schema.oct.md::holographic_patterns,
    octave-5-data.oct.md::compression_rules,
    octave-5-execution.oct.md::runtime_integration
  ]

§12::EXAMPLE
EXAMPLE:
  SESSION:
    ID::sess_abc123
    STATUS::ACTIVE
    PHASE::B1_FOUNDATION
    QUALITY::[tests::5/5,lint::passing]
    FLOW::[INIT->BUILD->DEPLOY]
    BLOCKERS::none

===END===
