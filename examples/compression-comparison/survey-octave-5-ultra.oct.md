===HOLOGRAPHIC_SURVEY===
META:
  TYPE::REFERENCE_INDEX
  VERSION::"5.1.0"
  SOURCE::survey-original-raw.oct.md
  COMPRESSION_TIER::ULTRA
  COMPRESSION_RATIO::~50%
  ORIGINAL_TOKENS::5600
  COMPRESSED_TOKENS::2800
  LOSS_PROFILE::narrative⊕reasoning|facts∧structure_preserved
  USE_CASE::embedding_generation,dense_indexing,lookup_tables,reference_only

---

NOTE::ULTRA tier: facts and structure only. No narrative, reasoning, or examples.
      Use for: embeddings, database lookups, dense reference tables.
      NOT suitable for: human reading, understanding tradeoffs, decision-making.

// SYSTEM COMPARISON FACT TABLE

SYSTEMS::[JSON_Schema,OpenAPI,Protobuf,Avro,CUE,JSON-LD,SHACL,Zod,Pydantic,Guidance,Outlines,Guardrails,Function_Calling,Attribute_Grammars,BDD_Gherkin]

JSON_SCHEMA::
  VALIDATES::[structure,types,ranges,patterns,formats]
  TEACHES::examples_in_docs|descriptions
  EXTRACTS::none|requires_external_code
  GAP::schema_separate_from_examples|no_runtime_binding

OPENAPI::
  VALIDATES::[structure,compliance]
  TEACHES::examples_in_docs
  EXTRACTS::codegen[generates_stubs]
  GAP::not_unified_executable|no_routing_semantics_standard

PROTOBUF::
  VALIDATES::[types,required,defaults]
  TEACHES::minimal|formal_not_legible
  EXTRACTS::codegen[native_bindings]
  GAP::no_inline_examples|no_execution_intent

AVRO::
  VALIDATES::[types,required,defaults]
  TEACHES::minimal|schema_with_data
  EXTRACTS::codegen|parse_to_objects
  GAP::no_execution_instructions|schema_evolution_only

CUE::
  VALIDATES::[types,ranges,patterns,enums,defaults]
  TEACHES::examples_inline|unified_schema_data
  EXTRACTS::partial|computes_output|no_side_effects_by_default
  STRENGTH::closest_non_LLM_analog
  GAP::no_execution_binding|learning_curve

JSON_LD::
  VALIDATES::via_SHACL[cardinalities,types,conditions,custom_code]
  TEACHES::semantic_context|not_format_examples
  EXTRACTS::semantic_categorization|manual_routing
  GAP::heavyweight|not_LLM_legible|niche_adoption

SHACL::
  VALIDATES::very_strong[cardinalities,types,complex_conditions,SPARQL]
  TEACHES::limited|RDF_graphs_not_readable
  EXTRACTS::pass_fail|categorization
  GAP::machine-oriented|separate_shapes|no_inline_examples

ZOD::
  VALIDATES::[types,ranges,patterns,enums]
  TEACHES::implicit|code_embedded
  EXTRACTS::native_objects
  GAP::developer-only|no_semantic_actions|manual_routing

PYDANTIC::
  VALIDATES::[types,constraints,custom_validators]
  TEACHES::field_metadata|examples_in_docs
  EXTRACTS::typed_objects|framework_integrated
  GAP::code_embedded|separate_examples|not_standalone_artifact

GUIDANCE::
  VALIDATES::[real_time|regex,types,choices]
  TEACHES::inline_examples|explicit_format
  EXTRACTS::captured_variables
  GAP::requires_coding|template_heavy|not_static

OUTLINES::
  VALIDATES::[guaranteed|grammar,regex_filtering]
  TEACHES::implicit|library_infers_from_schema
  EXTRACTS::automatic|Python_objects
  GAP::code_embedded|limited_nesting|Pydantic_tied

GUARDRAILS::
  VALIDATES::[schema,validators,semantic_checks,auto_correction]
  TEACHES::strong|YAML_spec,few_shot_examples
  EXTRACTS::parsed_objects|Python_dict_or_Pydantic
  GAP::verbose_YAML|after_fact_validation|retry_latency

FUNCTION_CALLING::
  VALIDATES::[structural|OpenAI_enforces_JSON_schema]
  TEACHES::schema_types_descriptions
  EXTRACTS::routing_implicit|function_call_direct
  GAP::no_explicit_examples|JSON_only|token_cost|narrow_use_case

ATTRIBUTE_GRAMMARS::
  VALIDATES::[strict|parsing_enforces_format]
  TEACHES::minimal|examples_separate
  EXTRACTS::semantic_actions|can_trigger_code
  STRENGTH::covers_all_three_axes
  GAP::verbose|specialized_skill|poor_error_messages|maintenance

BDD_GHERKIN::
  VALIDATES::via_tests|pass_fail_execution
  TEACHES::strong|readable_scenarios
  EXTRACTS::step_definitions|pattern_to_code
  GAP::test_specific|verbose|not_compact|ambiguity_risk

COMPARATIVE_TEACH::strong>:[CUE,BDD,Guidance,Guardrails,JSON_LD]|moderate::[OpenAPI,Pydantic,Function_Calling]|weak::[Protobuf,JSON_Schema,Zod,Attribute_Grammars,Outlines]

COMPARATIVE_VALIDATE::strong::[JSON_Schema,Pydantic,Protobuf,CUE,SHACL,Guardrails]|moderate::[OpenAPI,BDD,Guidance,Outlines]|weak::[JSON-LD,Function_Calling]

COMPARATIVE_EXTRACT::strong::[Function_Calling,Guidance,BDD,Attribute_Grammars,Guardrails]|moderate::[Protobuf,Outlines,Pydantic_FastAPI]|weak::[CUE,JSON_Schema,OpenAPI,Zod,JSON-LD]

HOLOGRAPHIC_NOVELTY::
  UNIQUE::[example_rule_action_in_one_line,LLM_legible_syntax,self_referential_bootstrap]
  SYNTHESIS::[declarative_rigor,pedagogical_examples,spec_execution_binding]
  GAP::no_existing_system_unifies_all_three_seamlessly

CLOSEST_ANALOGS::[Guardrails,Outlines,CUE]

FAILURE_MODES::
  COMPLEXITY::balance_expressiveness_vs_simplicity|avoid_Turing_completeness
  DRIFT::spec_code_must_stay_unified|separate_specs_diverge
  MISINTERPRETATION::LLM_might_ignore_or_misunderstand|need_few_shot
  OVER_RELIANCE::models_not_100_percent_obedient|need_validator_layer
  PERFORMANCE::large_specs_token_costly|selective_injection_needed
  ADOPTION::wheel_reinvention_concern|need_clear_benefit

MINIMAL_EXECUTION::
  PARSER::read_holographic_lines→extract_[name,example,constraint,target]
  VALIDATOR::convert_spec→validation_rules|map_to_JSON_Schema_or_Pydantic
  TEACHING::include_spec_in_prompt|few_shot_examples
  ROUTING::dispatch_fields_to_targets|configuration_mapping

CONCLUSION::
  STATUS::meaningful_synthesis_not_reinvention
  COMPONENTS::schema_language_examples_execution_hooks_all_exist
  INTEGRATION::orchestrates_via_single_source
  BENEFIT::one_document_provides_documentation_validation_automation
  MARKET::gap_not_filled_by_existing_single_source
  CHALLENGE::keep_simple_not_burdensome|implement_robustly

===END===
