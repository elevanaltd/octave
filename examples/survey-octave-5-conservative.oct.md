===HOLOGRAPHIC_SURVEY===
META:
  TYPE::RESEARCH_SUMMARY
  VERSION::"5.1.0"
  SOURCE::survey-original-raw.oct.md
  COMPRESSION_TIER::CONSERVATIVE
  COMPRESSION_RATIO::~15%_loss|~85%_retained
  ORIGINAL_TOKENS::5600
  COMPRESSED_TOKENS::4800
  LOSS_PROFILE::redundancy⊕verbose_transitions|explanatory_depth_preserved
  NARRATIVE_DEPTH::maintained[tradeoff_reasoning_inline,execution_strategies_explained]

---

NOTE::CONSERVATIVE tier: preserves explanatory depth and tradeoff narratives;
      only redundancy and verbose transitions are removed.
      For more aggressive compression, see AGGRESSIVE tier example.

// Holographic Document Language: Survey Related Systems
// Compressed using OCTAVE 5.1.0 CONSERVATIVE tier (keep reasoning, drop redundancy)

OVERVIEW::
  CONCEPT::single declarative spec→teaches_format⊕validates_rules⊕routes_data
  EXAMPLE::ID::[`sess_123`∧REQ→INDEXER]
  RATIONALE::self-documenting schema[shows_example, marks_constraints, indicates_routing]
  GOAL::single-source⊕executable⊕machine-legible⊕LLM-legible
  AXES::[teach_format,validate_structure,extract_routing]
  TRADEOFF::all three unified→most systems pick two

DECLARATIVE_SCHEMAS:
  JSON_SCHEMA:
    SOLVES::[format_grammar,validation,structure_definition]
    TEACH::limited[examples∨descriptions_separate_from_spec]
    VALIDATE::strong[types,required,ranges,patterns,allowed_formats]
    EXTRACT::none[requires_external_code∨code_generation]
    TRADEOFF::schema∨examples_often_separated|no_runtime_binding_concept
    WHY_SEPARATE::examples→documentation_or_OpenAPI|spec_alone_isn't_executable_routing_plan

  OPENAPI:
    SOLVES::[API_contracts,endpoints,request∧response_bodies,discovery]
    TEACH::moderate[examples∨descriptions_in_docs_help_developers]
    VALIDATE::schema-based[runtime_compliance_checks_via_framework]
    EXTRACT::codegen_form[generates_handlers∨SDK]
    TRADEOFF::bundles_examples_with_schema→teaching_benefit|still_not_unified_executable
    WHY_LIMITED::spec_describes_API_shape|doesn't_describe_execution_logic|routing_annotations_not_standard

  PROTOBUF_AVRO:
    SOLVES::[binary_serialization,cross-language_data,RPC∨storage]
    TEACH::minimal[formal_syntax_not_LLM-legible|no_inline_example_data]
    VALIDATE::type-enforcement[required_fields,default_values,optional∨required_labels]
    EXTRACT::codegen[generated_code_bindings]
    STRATEGY::codegen_approach_trades_formal_correctness_for_adoption
    WHY_NOT_LLM::schemas_assume_separate_documentation_stage|example_illustration_not_built_in
    NOTE_AVRO::schemas_always_included_with_data[self-descriptive]|schema_evolution_supported[defaults]

UNIFIED_LANGUAGES:
  CUE:
    SOLVES::[unify_schema⊕data⊕constraints_in_single_file]
    PHILOSOPHY::"types,values,constraints_are_all_same"|no_hard_separation_between_schema∧instance
    TEACH::strong[example_blocks_demonstrate_format|unified_structure_shows_pattern]
    VALIDATE::extensive[optional,required,ranges,regex,enums,default_values,merges_schema∧data]
    EXTRACT::partial[executable_constraint_solver|computes_outputs∨validates|doesn't_trigger_external_side-effects_by_default]
    STRENGTH::closest_non-LLM_analog|demonstrates_unified_approach
    CHALLENGE::learning_curve_vs_legibility|complex_unification_engine_harder_for_LLM_to_grok
    REASONING::CUE_proves_concept_but_needs_external_integration_for_execution

  JSON_LD_SHACL:
    SOLVES::[semantic_annotation,linked_data,RDF_constraints]
    TEACH::semantic[context_maps_to_ontologies|LLM_could_infer_meaning_if_familiar_with_schema.org]
    VALIDATE::very_strong[cardinalities,types,conditions,custom_SPARQL∨JavaScript_rules]
    EXTRACT::semantic_routing[categorize_validate|not_imperative_execution]
    LIMITATION::heavyweight|not_LLM-legible_in_raw_form|SHACL_shapes_are_RDF_graphs_themselves
    NOTE::different_problem_domain|ensures_data_quality_in_knowledge_graphs|not_designed_for_prompt_engineering

CODE_LIBRARIES:
  ZOD:
    SOLVES::[runtime_schema_validation_via_code]
    APPROACH::TypeScript-first|brings_compile-time_type_checking_to_runtime
    TEACH::implicit[schema_in_code_readable_to_developers|not_LLM-accessible_as_standalone_document]
    VALIDATE::strong[types,ranges,regex,enums,constraint_enforcement]
    EXTRACT::native_typed_objects[routing_through_code]
    LIMITATION::code-embedded_not_declarative|no_semantic_actions_in_schema|manual_routing

  PYDANTIC:
    SOLVES::[data_validation∧transformation_via_type_hints]
    APPROACH::Python_dataclasses_plus_runtime_checks|used_in_FastAPI_for_request_validation
    TEACH::field_metadata[Field(description=,example=)|metadata_flows_to_OpenAPI_docs]
    VALIDATE::strong[type_enforcement,constraints,custom_validators,JSON_Schema_generation]
    EXTRACT::framework_integrated[FastAPI_orchestrates_routing|model_parameter→validation→function_logic]
    ECOSYSTEM::Guardrails∧LangChain_use_Pydantic_as_output_schemas|shows_integration_potential
    KEY_INSIGHT::Pydantic_alone_doesn't_teach_LLM|glue_code_around_it_does_the_teaching

EXECUTION_STRATEGIES:
  GRAMMAR_APPROACH::
    METHOD::Parsing_Expression_Grammar∨Attribute_Grammar
    SOLVES::[formal_syntax_definition,syntax_validation,semantic_execution_through_rules]
    STRENGTH::unifies_validation∧semantic_actions
    CHALLENGE::verbose|specialized_skill|poor_error_messages_for_debugging|maintenance_burden_if_complex
    PRACTICAL_ISSUE::if_used_for_generation→too_restrictive|model_might_get_stuck
    HISTORY::formal_spec_attempts→maintenance_problems|why_simpler_schemas_dominate

  BDD_GHERKIN::
    METHOD::natural_language_scenarios→step_definitions→code_execution
    STRENGTH::readable_examples∧executable_tests|proven_concept
    LIMITATION::test-specific|verbose|not_compact_like_holographic_DSL
    LESSON::mixing_readable_examples_with_executable_hooks→successful_pattern
    FAILURE_MODE::ambiguity→natural_language_interpretation_errors

LLM_STRUCTURED_OUTPUT:
  FUNCTION_CALLING:
    SOLVES::[structured_JSON_generation_with_routing]
    TEACH::schema_informs_model[keys,types,descriptions→LLM_infers_format]
    VALIDATE::structural[OpenAI_enforces_JSON∧schema_compliance]
    EXTRACT::routing_implicit[function_name⊕args→system_calls_function]
    BENEFIT::built-in_execution|schema_directly_drives_action
    LIMITATION::no_explicit_examples|JSON-only|not_freeform_text|token_cost_of_stuffing_schema|narrow_use_case

  GUIDANCE:
    SOLVES::[token-level_steering∧format_enforcement_during_generation]
    METHOD::template_prompts_with_constraints|validates_tokens_as_they_stream
    TEACH::strong[inline_examples∨explicit_format_in_prompt]
    VALIDATE::real-time[regex∨type∨choice_enforcement,stops_invalid_tokens,retry_logic]
    EXTRACT::immediate[captured→variables_ready_for_use]
    BENEFIT::guarantees_structure|during_generation_not_after
    TRADEOFF::powerful_but_requires_coding|template_maintenance_complex|not_static_artifact

  OUTLINES:
    SOLVES::[high-level_structured_generation_interface]
    METHOD::Python_type_hints∨Pydantic_models→automatic_grammar∨regex_construction
    TEACH::implicit[library_constructs_appropriate_prompt_from_schema]
    VALIDATE::guaranteed[grammar∨regex_filtering_tokens]
    EXTRACT::automatic[Pydantic_parsing→structured_objects]
    BENEFIT::abstracts_complexity|almost_as_fast_as_freetext_generation
    LIMITATION::code-embedded|not_static_artifact|limited_nesting|Pydantic-tied

  GUARDRAILS:
    SOLVES::[validation∧correction_with_repair_loops]
    METHOD::RAIL_spec_in_YAML|includes_format_definitions∧validators
    TEACH::strong[schema→prompt_augmentation|can_include_few-shot_examples_in_spec]
    VALIDATE::comprehensive[schema∧validators∧semantic_checks,auto-correction_on_failure]
    EXTRACT::parsed_objects[Python_dict∨Pydantic_model]
    BENEFIT::single_source_for_format∧validation|retry_loop_improves_reliability
    EXECUTION::allows_conditional_flows|fallback_handling
    TRADEOFF::YAML_spec_somewhat_verbose|after-fact_validation_can_increase_latency|requires_re-prompting_on_failure
    CHALLENGE::semantic_validation_separate|can_have_valid_JSON_that_is_logically_wrong

COMPARATIVE_MATRIX::
  TEACH::
    strong::[CUE,BDD,Guidance,Guardrails,JSON_LD_semantic]
    moderate::[OpenAPI,Pydantic,Function_Calling]
    weak::[Protobuf,JSON_Schema,Zod,Attribute_Grammars,Outlines]

  VALIDATE::
    strong::[JSON_Schema,Pydantic,Protobuf,CUE,SHACL,Guardrails]
    moderate::[OpenAPI,BDD,Guidance,Outlines]
    weak::[JSON-LD,Function_Calling]

  EXTRACT::
    strong::[Function_Calling,Guidance,BDD,Attribute_Grammars,Guardrails]
    moderate::[Protobuf,Outlines,Pydantic⊕FastAPI]
    weak::[CUE,JSON_Schema,OpenAPI,Zod,JSON-LD]

STRUCTURAL_VS_SEMANTIC::
  INSIGHT::original_research_distinguished_three_validation_types
  STRUCTURAL::shape∨types∨required_fields[most_systems_handle]
  SEMANTIC::cross-field_meaning∨entailment∨factual_correctness[most_systems_miss]
  OPERATIONAL::is_this_route_action_allowed[rarely_addressed]
  RISK::systems_can_produce_VALID_BUT_WRONG_outputs
  MITIGATION::need_semantic_validators∨entailment_checkers[increases_complexity]

NOVELTY::
  UNIQUE_TO_HOLOGRAPHIC::[example∧rule→action_in_one_line|LLM-legible_syntax|self-referential_bootstrap]
  SYNTHESIS::combines[declarative_rigor⊕pedagogical_examples⊕spec→execution_binding]
  WHAT_OTHERS_MISS::no_existing_system_unifies_all_three_seamlessly_in_simple_way
  CLOSEST_ANALOG::[Guardrails⊕Outlines⊕CUE_as_non-LLM_reference]
  TRADEOFF_COVERAGE::most_systems_cover_two_axes
    SCHEMA∧EXECUTION::[Attribute_Grammars_hard_to_read|Function_Calling_minimal_teaching|BDD_for_scenarios]
    SCHEMA∧EXAMPLE::[CUE_data_with_schema|OpenAPI_schema_with_examples_no_execution]
    EXAMPLE∧EXECUTION::[BDD_scenario→code|documentation_with_embedded_tests]

FAILURE_MODES::
  COMPLEXITY_RISK::balance_expressiveness↔simplicity|must_avoid_Turing-completeness
    WHY::attribute_grammars_prove_too_much_power→unmaintainable|simpler_schemas_win_adoption
  DRIFT_RISK::must_treat_spec∧code_as_unified|if_separate→drift_inevitable
    MITIGATION::make_spec_part_of_build_workflow|like_JSON_Schema_enforcement_in_CI
  LLM_MISINTERPRETATION::model_might_ignore_or_misunderstand_spec
    SOLUTION::provide_few-shot_examples∨meta-spec_explanation|include_spec_in_system_prompt
  OVER_RELIANCE::models_don't_always_obey_100_percent
    OBSERVED::edge_cases_where_model_outputs_valid_but_wrong|adds_extra_text_when_not_needed
    MITIGATION::runtime_validator_layer[like_Guardrails]|can't_assume_perfect_model_output
  PERFORMANCE_SCALABILITY::large_specs→token_cost|can't_always_fit_entire_spec_in_prompt
    SEEN_IN::OpenAPI_specs_too_large|similar_to_Toolformer_function_selection_problem
    APPROACH::selective_spec_injection|two-pass_validation[generate_then_check_outside_model]
  USER_ADOPTION::wheel_reinvention_concern|need_clear_benefit_vs_existing_tools
    STRATEGY::leverage_existing[JSON_Schema_validator,function_calling,Guardrails]|don't_rebuild
    POSITIONING::coherent_orchestration→the_car_that_moves_forward|not_individual_wheels

MINIMAL_EXECUTION_LAYER:
  COMPONENT_1_PARSER::
    TASK::read_holographic_lines→extract[field_name,example,constraint,target]
    IMPLEMENTATION::straightforward_string_parsing∨simple_PEG
    COMPLEXITY::low[syntax_is_regular]

  COMPONENT_2_VALIDATOR::
    TASK::convert_spec→validation_rules
    MAPPING::REQ→required_field|REGEX[pattern]→regex_check|ENUM[A,B]→allowed_set
    STRATEGY::leverage_existing[compile_to_JSON_Schema∨Pydantic∨use_spec_directly]
    HANDLING::unknown_fields_policy[warn∨reject]
    COMPLEXITY::medium[but_libraries_exist]

  COMPONENT_3_TEACHING::
    TASK::prepare_LLM_to_follow_spec
    NAIVE_METHOD::include_spec_in_prompt[system∨few-shot]
    ENHANCEMENT::include_example_outputs_showing_expected_format
    ADVANCED::use_function_calling[transform_spec_to_OpenAI_schema]∨Guidance_templates
    VALIDATION_STEP::validate_after_generation|if_fails→feedback_loop_with_model
    COMPLEXITY::medium-high[depends_on_sophistication]

  COMPONENT_4_ROUTING::
    TASK::dispatch_fields_to_targets_based_on_spec
    MAPPING::TARGET_labels→handlers∨API_calls∨functions
    ARCHITECTURE::plugin_system[if_target==INDEXER→call_IndexerClient.index()]
    KEY_BENEFIT::loop_over_parsed_output∧dispatch_by_target|no_hardcoded_field_routing_in_code
    COMPLEXITY::low[once_parsing_done]

SYNTHESIS::
  ARCHITECTURE::spec_compiler⊕orchestrator
    FLOW::parse_spec→teach_LLM→validate_output→route_to_targets
    LEVERAGE::existing_tech[re_for_regex,OpenAI_functions,configuration_mapping]
  NOVELTY::not_reinventing_algorithms|assembling_proven_components_via_single_source
  FEASIBILITY::meaningful_gap_exists|synthesizing_benefits_vs_picking_two_of_three

CONCLUSION::
  REIMVENTION_VS_SYNTHESIS::not_wheel_reinvention|combining_wheels_into_cohesive_car
  COMPONENTS_EXIST::schema_language∧examples∧execution_hooks→all_proven
  INTEGRATION::holographic_language_orchestrates_them_via_one_source
  BENEFIT::developer∨analyst_writes_one_document→gets_documentation∧validation∧automation
  MARKET_FIT::given_rise_of_LLM_applications|single-source_schema_for_prompt∧post-processing_not_fully_solved
  CHALLENGE::design_so_not_burdensome[aid_not_chore]|implement_robustly[leverage_analogs'_lessons]
  OUTCOME::if_successful→addresses_genuine_gap|streamlines_reliable_LLM_app_development

===END===
