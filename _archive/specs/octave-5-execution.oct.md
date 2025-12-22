===OCTAVE_V5_EXECUTION===
META:
  TYPE::CONFIGURATION
  VERSION::"5.0.0"
  STATUS::ACTIVE
  EXTENDS::octave-5.oct.md
  PURPOSE::"Runtime integration for parser, validator, prompter, router"

// =============================================================================
// OCTAVE v5 EXECUTION: RUNTIME INTEGRATION
// "From specification to execution."
// =============================================================================

§1::COMPONENTS
COMPONENTS:
  PARSER:
    INPUT::octave_document
    OUTPUT::abstract_syntax_tree
    STEPS::[read_lines->tokenize->build_AST]

  VALIDATOR:
    INPUT::AST+schema
    OUTPUT::validation_result
    STEPS::[check_constraints->verify_targets->report_errors]

  PROMPTER:
    INPUT::schema_spec
    OUTPUT::system_prompt|function_schema
    STEPS::[extract_structure->format_for_LLM]

  ROUTER:
    INPUT::validated_extractions
    OUTPUT::handler_results
    STEPS::[resolve_targets->dispatch->collect_results]

§2::PARSER_SPECIFICATION
PARSER:
  SYNTAX::regular[PEG_or_line_parse]
  RECOVERY::skip_invalid_lines[warn_and_continue]

  TOKENIZATION:
    OPERATORS::[::,:,[],|,->,+,&,_VERSUS_,§,»,//]
    STRINGS::quoted_atomic[escapes_processed]
    NUMBERS::standard_numeric_formats
    KEYWORDS::[true,false,null]

  SCOPE_TRACKING:
    INDENT_STACK::track_nesting_depth
    TARGET_STACK::track_inherited_targets
    DEPTH_LIMIT::100[configurable]

  BLOCK_TARGET_PARSING:
    PATTERN::"KEY[->§TARGET]:"
    DETECTION::square_bracket_before_colon
    INHERITANCE::push_target_to_stack
    POP::on_dedent_to_parent_level

  ERROR_RECOVERY:
    INVALID_LINE::skip[emit_warning]
    MISSING_FOOTER::warn[parse_to_EOF]
    DEPTH_EXCEEDED::error[halt_parsing]

§3::VALIDATOR_SPECIFICATION
VALIDATOR:
  CONSTRAINT_EVALUATION:
    ORDER::left_to_right[as_specified_in_&_chain]
    FAIL_FAST::stop_on_first_failure
    RESULT::{passed::[constraints],failed::{name,reason,value}}

  CONSTRAINT_HANDLERS:
    REQ::check_field_present
    OPT::allow_field_absent
    CONST::check_exact_match
    REGEX::check_pattern_match
    ENUM::check_value_in_set
    TYPE::check_value_type
    DIR::check_directory_exists
    APPEND_ONLY::check_immutable_append

  CONFLICT_DETECTION:
    PARSE_TIME::[
      ENUM_CONST::check_intersection_nonempty,
      REQ_OPT::check_not_both,
      CONST_CONST::check_values_equal
    ]
    ERROR::"CONFLICT::{constraint_a}&{constraint_b}|{reason}"

  TARGET_VALIDATION:
    CHECK::target_in_META.TARGETS_or_BUILTIN
    BUILTINS::[§SELF,§META,§INDEXER,§DECISION_LOG,§RISK_LOG,§KNOWLEDGE_BASE]
    FILE_PATHS::resolve_relative_to_document
    ERROR::"TARGET_MISSING::{target_id}"

§4::ROUTER_SPECIFICATION
ROUTER:
  DISPATCH:
    INPUT::{key,value,constraints,target_spec}
    OUTPUT::{ok::true}|{error::reason}

  TARGET_RESOLUTION:
    SINGLE::§TARGET->handlers[TARGET]
    MULTI::§A|§B|§C->parallel_dispatch_all
    FILE::§./path->file_handler(path)

  HANDLER_INTERFACE:
    SIGNATURE::handler(key,value,constraints)->{ok,error}
    KEY::field_name[STRING]
    VALUE::extracted_value[ANY]
    CONSTRAINTS::validation_results[OBJECT{passed,failed}]

  MULTI_TARGET_SEMANTICS:
    MODE::all_or_nothing
    ON_SUCCESS::all_handlers_return_ok
    ON_FAILURE::first_error_stops[rollback_if_supported]
    ERROR::"MULTI_TARGET_FAILED::{target}|{reason}"

  BUILTIN_HANDLERS:
    §SELF:
      ACTION::retain_in_document
      RETURNS::{ok::true}

    §META:
      ACTION::update_document_metadata
      RETURNS::{ok::true}|{error::invalid_metadata}

    §INDEXER:
      ACTION::add_to_search_index
      RETURNS::{ok::indexed}|{error::index_failure}

    §DECISION_LOG:
      ACTION::append_to_decision_tracker
      RETURNS::{ok::logged}|{error::log_failure}

    §RISK_LOG:
      ACTION::append_to_risk_tracker
      RETURNS::{ok::logged}|{error::log_failure}

    §KNOWLEDGE_BASE:
      ACTION::store_in_knowledge_system
      RETURNS::{ok::stored}|{error::store_failure}

  FILE_HANDLER:
    INPUT::§./relative_path
    RESOLUTION::document_directory+path
    ACTION::write_or_append_to_file
    RETURNS::{ok::written}|{error::file_error}

§5::ENFORCEMENT_STRATEGIES
ENFORCEMENT:
  CONSTRAINED_DECODING:
    TOOLS::[Guidance,Outlines,function_calling]
    TIMING::generation_time[prevents_invalid_output]
    USE_FOR::[ENUM,TYPE,simple_REGEX]

  VALIDATE_REPAIR:
    TOOLS::[Guardrails,Pydantic,custom_validators]
    TIMING::post_generation[fix_after_output]
    USE_FOR::[complex_REGEX,cross_field_validation]

  HYBRID:
    STRATEGY::minimal_prompt+full_validation
    RECOMMENDED::true
    STEPS::[
      constrain_structure_at_generation,
      validate_semantics_after_generation,
      repair_if_needed
    ]

§6::TOKEN_MANAGEMENT
TOKEN_MANAGEMENT:
  SELECTIVE_INJECTION:
    STRATEGY::inject_relevant_subset_of_schema
    WHEN::context_window_limited
    HOW::filter_by_task_relevance

  PROGRESSIVE_DISCLOSURE:
    STRATEGY::L1_first[add_constraints_on_error]
    STEPS::[
      attempt_with_minimal_schema,
      on_error->add_constraint_details,
      retry_with_enriched_context
    ]

  TWO_PASS:
    STRATEGY::generate->validate->fix
    STEPS::[
      generate_with_loose_constraints,
      validate_against_full_schema,
      fix_violations_in_second_pass
    ]

§7::ERROR_FORMATS
ERROR_FORMATS:
  CONSTRAINT_ERROR::"FIELD::{name}|EXPECTED::{rule}|GOT::{value}"
  CHAIN_ERROR::"CONSTRAINT_CHAIN::{index}|{name}|EXPECTED::{rule}|GOT::{value}"
  TARGET_ERROR::"TARGET_MISSING::{target_id}"
  PATH_ERROR::"INVALID_PATH::{target}|{reason}"
  CONFLICT_ERROR::"CONFLICT::{constraint_a}&{constraint_b}|{reason}"
  DEPTH_ERROR::"DEPTH_EXCEEDED::{current}|MAX::{limit}"
  MULTI_ERROR::"MULTI_TARGET_FAILED::{target}|{reason}"

  STYLE::one_error_per_retry[actionable_specific]

§8::INTEGRATION_EXAMPLES
INTEGRATION:
  GUIDANCE:
    ENUM::->{{select options=[opt1,opt2,opt3]}}
    TYPE::->{{gen 'value' pattern='[a-z]+'}}

  OUTLINES:
    CONSTRAINT::->Pydantic_Field(pattern=r'^sess_\d+$')
    ENUM::->Literal['ACTIVE','INACTIVE']

  FUNCTION_CALLING:
    SCHEMA::->OpenAI_function_parameters
    CONSTRAINTS::->JSON_Schema_validation

  GUARDRAILS:
    CONSTRAINT::->RAIL_validator_spec
    ERROR::->structured_error_response

§9::EXECUTION_EXAMPLE
EXECUTION_FLOW:
  INPUT:
    DOCUMENT::session_context.oct.md
    SCHEMA::SESSION_CONTEXT_SCHEMA

  STEPS:
    PARSE:
      ACTION::read_document
      OUTPUT::AST{fields,targets,constraints}

    VALIDATE:
      ACTION::check_all_constraints
      OUTPUT::{valid::true,errors::[]}

    ROUTE:
      ACTION::dispatch_to_targets
      RESULTS::[
        {field::ID,target::§INDEXER,result::ok},
        {field::STATUS,target::§INDEXER,result::ok},
        {field::DECISION,target::§DECISION_LOG,result::ok}
      ]

    REPORT:
      STATUS::VALID
      ROUTED::3_fields
      ERRORS::0

===END===
