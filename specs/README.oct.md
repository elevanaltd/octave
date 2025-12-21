===OCTAVE_V5_SPECS===
META:
  TYPE::DOCUMENTATION
  VERSION::"5.0.3"
  STATUS::APPROVED

§1::CANONICAL_FILES
LLM_PROFILES::[
  octave-5-llm-core.oct.md["~200_tokens"][always_inject],
  octave-5-llm-schema.oct.md["~80_tokens"][for_L4_definitions],
  octave-5-llm-data.oct.md["~70_tokens"][for_compression],
  octave-5-llm-execution.oct.md["~100_tokens"][for_debugging],
  octave-5-llm-rationale.oct.md["~160_tokens"][for_training_or_design]
]

ARCHIVE::_archive/[historical_development_artifacts]

§2::INJECTION_TABLE
TASK::INJECT::TOKENS::USE_CASE

RUNTIME:
  any_octave::core::"~200"::base_syntax_and_operators
  compress_prose::core+data::"~270"::telegram_style_compression
  define_schema::core+schema::"~280"::L4_holographic_definitions
  debug_errors::core+execution::"~300"::understanding_validator_feedback
  full_generation::core+schema+data::"~350"::complete_generation_capability

TRAINING:
  model_fine_tune::core+rationale::"~360"::teaching_OCTAVE_to_base_models
  complex_reasoning::core+schema+rationale::"~440"::designing_new_protocols
  full_with_debug::core+schema+data+execution::"~450"::complete_with_error_handling
  maximum::core+schema+data+execution+rationale::"~610"::everything

§3::COMPOSITION_RULES
CORE::always_required[base_syntax]
SCHEMA::add_for[L4_holographic,constraint_chaining,targets,block_inheritance]
DATA::add_for[compression,abbreviations,inline_maps,forbidden_rewrites]
EXECUTION::add_for[error_formats,retry_protocol,validation_flow]
RATIONALE::add_for[design_philosophy,token_economics,training_context]

§4::VERSION_HISTORY
5.0.3::APPROVED[current]
  fixes::[empty_blocks,inline_map_nesting,broadcast_failure_semantics]
5.0.2::superseded
  fixes::[chaining_allowed,empty_lists,inline_maps,assembly_rule,error_ordering]
5.0.1::superseded[terminology_fixes]
5.0.0::superseded[initial_modular_split]

§5::SINGLE_SOURCE_OF_TRUTH
RULE::LLM_profiles_ARE_the_spec
MASTER_SPECS::archived[served_development_purpose]
DRIFT_PREVENTION::one_canonical_source_only

===END===
