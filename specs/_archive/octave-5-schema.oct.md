===OCTAVE_V5_SCHEMA===
META:
  TYPE::PROTOCOL_DEFINITION
  VERSION::"5.0.0"
  STATUS::ACTIVE
  EXTENDS::octave-5.oct.md
  PURPOSE::"Holographic tuple specification - schema teaches syntax"

// =============================================================================
// OCTAVE v5 SCHEMA: THE HOLOGRAPHIC PATTERN
// "One line teaches syntax, defines schema, specifies extraction."
// =============================================================================

§1::HOLOGRAPHIC_PATTERN
PATTERN:
  DEFINITION::"KEY::[ EXAMPLE & CONSTRAINT -> §TARGET ]"
  COMPONENTS::[
    EXAMPLE::concrete_value[teaches_expected_format],
    CONSTRAINT::validation_rule[enforces_shape],
    TARGET::extraction_destination[routes_data]
  ]

  TUPLE_STRUCTURE::"[ EXAMPLE & CONSTRAINT -> §TARGET ]"

  WHY_HOLOGRAPHIC::[
    self_documenting::example_shows_format,
    self_validating::constraint_enforces_shape,
    self_routing::target_specifies_destination
  ]

§2::CONSTRAINT_STACKING
CONSTRAINT_STACKING:
  OPERATOR::"&"[logical_AND_all_must_pass]
  EVALUATION::left_to_right[fail_fast_on_first_violation]
  PRECEDENCE::TYPE->REGEX->ENUM->CONST->REQ|OPT

  CONFLICT_DETECTION:
    IMPOSSIBLE::"ENUM[A,B]&CONST[C]"->parse_error[empty_intersection]
    REDUNDANT::"TYPE(X)&TYPE(X)"->warning[duplicate_constraint]
    CONTRADICTORY::"REQ&OPT"->parse_error[mutually_exclusive]

  ERROR_FORMAT::"CONSTRAINT_CHAIN::{index}|{name}|EXPECTED::{rule}|GOT::{value}"

  EXAMPLES:
    VALID::["sess_123"&REQ&TYPE(STRING)&REGEX[^sess_\w+$]->§INDEXER]
    INVALID::["value"&ENUM[A,B]&CONST[C]->§META]
    EVALUATION_ORDER::[REQ->TYPE->REGEX][stop_on_first_failure]

§3::TARGET_RESOLUTION
TARGET_RESOLUTION:
  SEMANTICS::extraction_destination[not_function_call]
  ROUTING::parser_extracts->validator_checks->router_dispatches

  HANDLER_CONTRACT:
    SIGNATURE::handler(key,value,constraints)->{ok,error}
    PARAMETERS::[
      key::field_name[STRING],
      value::extracted_value[ANY],
      constraints::validation_results[OBJECT]
    ]
    RETURNS::{ok::true}|{error::reason}

  VALIDATION:
    PARSE_TIME::target_must_exist_in_META.TARGETS
    MISSING_TARGET::§UNKNOWN->ERROR[unknown_target_id]
    DECLARATION::META.TARGETS::[§NAME::handler|path]

  MULTI_TARGET:
    SYNTAX::"->§A|§B|§C"[broadcast_to_all]
    SEMANTICS::parallel_dispatch
    ERROR_MODE::all_or_nothing[first_failure_stops_all]
    EXAMPLE::CRITICAL::["breach"&REQ->§RISK_LOG|§INDEXER|§ALERT]

  FILE_PATHS:
    SYNTAX::§./relative[from_document_directory]
    ABSOLUTE::§/absolute[when_document_is_virtual]
    RESOLUTION::document_location->path_join->target_file
    ERROR::INVALID_PATH::{target}|{reason}

  BUILTIN_HANDLERS::[
    §SELF::document.retain,
    §META::document.update_metadata,
    §INDEXER::search_service.index,
    §DECISION_LOG::tracker.log_decision,
    §RISK_LOG::tracker.log_risk,
    §KNOWLEDGE_BASE::knowledge.store
  ]

§4::BLOCK_TARGET_INHERITANCE
BLOCK_INHERITANCE:
  SYNTAX::"BLOCK[->§TARGET]:children"
  SEMANTICS::lexical_scope[children_inherit_unless_override]

  RULES:
    INHERIT::children_without_target_use_parent_target
    OVERRIDE::child[->§NEW]replaces_parent_target
    NO_TARGET::children_must_specify_own_targets
    NESTING::unlimited[each_level_can_override]

  DEPTH_LIMIT:
    DEFAULT::100[levels]
    CONFIGURABLE::parser_setting
    ERROR::DEPTH_EXCEEDED->parse_error

  EXAMPLES:
    SIMPLE:
      RISKS[->§RISK_LOG]:
        CRITICAL::["auth_bypass"&OPEN]
        WARNING::["rate_limit"&MITIGATED]

    NESTED_OVERRIDE:
      SECURITY[->§./security.md]:
        RISKS[->§./risks.json]:
          SQL_INJECTION::["param_escape"&REQ]
          XSS::["output_sanitize"&REQ]
        MITIGATIONS::["validation"&DONE]

    MIXED:
      CONFIG[->§META]:
        SETTING::["value"&REQ]
        AUDIT::["event"&REQ->§DECISION_LOG]

§5::SCOPED_INJECTION
SCOPED_INJECTION:
  OPERATOR::"»"[block_injection]
  SYNTAX::BLOCK»{children}[inherits_context]

  USAGE::[
    template_expansion,
    content_injection,
    block_composition
  ]

  COMBINATION:
    WITH_TARGET::BLOCK[->§TARGET]»{children}
    CHILDREN_INHERIT::parent_target_applies_to_injected

  EXAMPLE:
    RISKS[->§RISK_LOG]»{
      CRITICAL::["auth_bypass"&OPEN]
      WARNING::["rate_limit"&MITIGATED->§SELF]
    }

§6::SCHEMA_DEFINITION
SCHEMA_STRUCTURE:
  POLICY:
    VERSION::["1.0"&REQ->§META]
    UNKNOWN_FIELDS::["REJECT"&REQ&ENUM[REJECT,IGNORE,WARN]->§SELF]
    TARGETS::[[§INDEXER,§DECISION_LOG,§RISK_LOG]&REQ->§SELF]

  FIELDS:
    PATTERN::"KEY::[ EXAMPLE & CONSTRAINTS -> §TARGET ]"
    REQUIRED_FIELDS::marked_with_REQ
    OPTIONAL_FIELDS::marked_with_OPT

§7::SCHEMA_EXAMPLE
SESSION_CONTEXT_SCHEMA:
  POLICY:
    VERSION::"1.0"
    UNKNOWN_FIELDS::REJECT
    TARGETS::[§INDEXER,§DECISION_LOG,§RISK_LOG]

  FIELDS:
    ID::["sess_abc123"&REQ&REGEX[^sess_[a-z0-9]+$]->§INDEXER]
    STATUS::["ACTIVE"&REQ&ENUM[ACTIVE,INACTIVE,ARCHIVED]->§INDEXER]
    PHASE::["B1_FOUNDATION"&REQ->§META]
    TAGS::[["ui","auth"]&OPT->§INDEXER]
    ROOT::["/.hestai/inbox"&DIR->§SELF]
    LOG::["events.jsonl"&APPEND_ONLY->§./processed/index.json]
    DECISION::["Use Redis for caching"&OPT->§DECISION_LOG]
    BLOCKER::["auth_bug"&OPT->§RISK_LOG]

§8::VALIDATION_PROTOCOL
VALIDATION:
  STAGES::[
    ENVELOPE->check_header_footer,
    META->validate_required_keys,
    CONSTRAINTS->evaluate_all_stacked,
    TARGETS->verify_existence,
    EXTRACT->route_to_handlers
  ]

  ERROR_TYPES::[
    missing_REQ::field_required_but_absent,
    REGEX_mismatch::value_does_not_match_pattern,
    ENUM_invalid::value_not_in_allowed_set,
    TYPE_wrong::value_type_mismatch,
    CONST_mismatch::value_does_not_equal_required,
    TARGET_missing::target_not_declared,
    DEPTH_exceeded::nesting_too_deep
  ]

  ERROR_FORMAT::"FIELD::{name}|EXPECTED::{rule}|GOT::{value}"

  SEVERITY:
    ERROR::[missing_REQ,REGEX_mismatch,ENUM_invalid,TYPE_wrong,TARGET_missing]
    WARNING::[redundant_constraint,deprecated_pattern]
    INFO::[optimization_suggestion]

===END===
