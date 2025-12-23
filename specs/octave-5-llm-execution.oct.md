===OCTAVE_EXECUTION===
META:
  TYPE::LLM_PROFILE
  VERSION::"5.1.0"
  STATUS::APPROVED
  IMPLEMENTATION::PARTIAL
  TOKENS::"~100"
  REQUIRES::octave-5-llm-core
  PURPOSE::validation_and_error_handling
  IMPLEMENTATION_NOTES::"Validator (134 LOC) handles META and basic structure validation. Parse errors caught. Constraint validation, error formatting, and retry protocol not implemented."
  IMPLEMENTATION_REF::[src/octave_mcp/core/validator.py]
  CRITICAL_GAPS::[constraint_validation,type_checking,regex_validation,error_message_formatting,retry_protocol]

---

// OCTAVE EXECUTION: Understanding validation feedback. Inject when debugging/iterating.

§1::VALIDATION_FLOW
STAGES::[PARSE->VALIDATE->ROUTE]

PARSE:
  CHECKS::[envelope,syntax,structure,indent]
  FAILURE::unparseable[no_recovery]

VALIDATE:
  CHECKS::[constraints,targets,types,conflicts]
  FAILURE::structured_error[retry_possible]

ROUTE:
  CHECKS::[target_exists,handler_accepts]
  FAILURE::routing_error[fix_target]

§2::ERROR_FORMATS
CONSTRAINT_ERROR::"FIELD::{name}|EXPECTED::{rule}|GOT::{value}"
CHAIN_ERROR::"CONSTRAINT_CHAIN::{index}|{constraint}|EXPECTED::{rule}|GOT::{value}"
TARGET_ERROR::"TARGET_MISSING::{target_id}|ALLOWED::[§SELF,§META,§INDEXER,§*_LOG,§KNOWLEDGE_BASE,POLICY.TARGETS]"
CONFLICT_ERROR::"CONFLICT::{constraint_a}&{constraint_b}|{reason}"
DEPTH_ERROR::"DEPTH_EXCEEDED::{level}|MAX::100"
PARSE_ERROR::"SYNTAX::line_{n}[1_indexed]|{reason}"
UNKNOWN_FIELD::"UNKNOWN_KEY::{key}|POLICY::REJECT|IGNORE|WARN"

ERROR_ORDERING::parse_errors_first->constraint_errors_top_down->target_errors_last
MULTI_ERROR::returns_first_only[fix_one_retry]

§3::VALIDATOR_CATCHES
ALWAYS_CHECKED::[
  constraint_conflicts[REQ&OPT,ENUM&CONST],
  target_existence[must_be_declared_or_builtin],
  type_mismatches[STRING_vs_NUMBER],
  regex_validity[pattern_must_compile],
  depth_limits[100_levels_max]
]

NOT_CHECKED::[
  semantic_correctness[validator_only_checks_structure],
  business_logic[your_responsibility],
  broadcast_rollback[handler_manages_partial_failure]
]

§4::RETRY_PROTOCOL
STRATEGY::one_error_at_a_time[fix_then_retry]
MAX_RETRIES::3
FEEDBACK_LOOP::[generate->validate->error->fix->retry]

ON_PARSE_ERROR:
  ACTION::check_envelope_and_indent_first
  COMMON::[tabs,missing_===END===,space_around_::]

ON_CONSTRAINT_ERROR:
  ACTION::read_EXPECTED_and_GOT_carefully
  COMMON::[wrong_type,invalid_enum_value,regex_mismatch]

ON_TARGET_ERROR:
  ACTION::use_builtin_or_declare_in_POLICY.TARGETS
  BUILTIN::[§SELF,§META,§INDEXER,§DECISION_LOG,§RISK_LOG,§KNOWLEDGE_BASE]

§5::SEVERITY
ERROR::must_fix[blocks_processing]
WARNING::should_fix[processing_continues]
INFO::suggestion[optional_improvement]

§6::INTEGRATION_HINTS
CONSTRAINED_DECODING::[Guidance,Outlines][prevents_errors_at_generation]
VALIDATE_REPAIR::[Pydantic,Guardrails][catches_errors_post_generation]
RECOMMENDED::hybrid[minimal_constraints+full_validation]

§7::REFERENCE
CORE_ERRORS::see_core.§6.NEVER
CONSTRAINT_RULES::see_schema.§2.CONSTRAINTS
COMPRESSION_RULES::see_data.§6.FORBIDDEN_REWRITES

===END===
