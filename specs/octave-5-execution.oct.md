===OCTAVE_V5_EXECUTION===
META:
  TYPE::CONFIGURATION
  VERSION::"5.0"
  STATUS::ACTIVE
  EXTENDS::octave-5.oct.md

PURPOSE::runtime[parser+validator+prompter+router]

COMPONENTS:
  PARSER::[read_octave->extract_AST]
  VALIDATOR::[constraints->JSON_Schema|Pydantic]
  PROMPTER::[spec->system_prompt|function_schema]
  ROUTER::[targets->handlers]

ENFORCEMENT:
  CONSTRAINED::[Guidance,Outlines,function_calling]->generation_time
  VALIDATE_REPAIR::[Guardrails,Pydantic]->post_generation
  HYBRID::minimal_prompt+full_validation[recommended]

TOKEN_MANAGEMENT:
  SELECTIVE::inject_relevant_subset
  PROGRESSIVE::L1_first->add_constraints_on_error
  TWO_PASS::[generate->validate->fix]

ERROR_FORMAT:
  PATTERN::FIELD::{name}|EXPECTED::{rule}|GOT::{value}
  STYLE::one_error_per_retry|actionable

INTEGRATION:
  GUIDANCE::ENUM->{{select options=[...]}}
  OUTLINES::constraints->Pydantic_Field
  FUNCTION_CALLING::schema->OpenAI_function
  GUARDRAILS::constraints->RAIL_spec

TARGET_ROUTING:
  §INDEXER::search_service.index
  §DECISION_LOG::tracker.log_decision
  §META::document.update_metadata

PARSER_NOTES:
  SYNTAX::regular[PEG_or_line_parse]
  RECOVERY::skip_invalid_lines+warn

===END===
