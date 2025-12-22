===OCTAVE_V5_DATA===
META:
  TYPE::CONFIGURATION
  VERSION::"5.0.0"
  STATUS::ACTIVE
  EXTENDS::octave-5.oct.md
  PURPOSE::"Data mode compression for maximum token density"

// =============================================================================
// OCTAVE v5 DATA: COMPRESSION PROTOCOL
// "Compress everything around the anchors, never the anchors themselves."
// =============================================================================

§1::DATA_MODE
DATA_MODE:
  ACTIVATION::[SESSION_CONTEXT,KNOWLEDGE_ARTIFACT,CONFIGURATION]
  PATTERN::"KEY::value"[L1_or_L2_only]
  DISTINCTION::data_uses_simple_assignment[no_holographic_tuples]

  LEVELS_ALLOWED::[L1,L2]
  LEVELS_FORBIDDEN::[L3,L4][use_schema_mode_instead]

§2::COMPRESSION_RULES
COMPRESSION:
  PRESERVE::[
    numbers::exact_values,
    names::identifiers_and_keys,
    codes::error_codes_and_ids,
    operators::all_octave_operators,
    anchors::§targets_and_sections,
    quoted::CONST_values_verbatim
  ]

  DROP::[
    articles::the_a_an,
    prepositions::of_for_to_with,
    filler::basically_essentially_simply,
    verbose_phrasing::compress_to_essence
  ]

  FLATTEN::prefer_pipes_over_deep_nesting

§3::ABBREVIATIONS
ABBREVIATIONS:
  STATUS::[
    DONE::completed,
    WIP::in_progress,
    PENDING::not_started,
    BLOCKED::waiting_on_blocker
  ]

  COMMON::[
    impl::implementation,
    config::configuration,
    env::environment,
    auth::authentication,
    db::database,
    msg::message,
    req::request,
    res::response
  ]

§4::LIST_FORMS
LIST_FORMS:
  PIPE:
    SYNTAX::a|b|c
    USE::alternatives_or_options
    EXAMPLE::STATUS::DONE|WIP|PENDING

  BRACKET:
    SYNTAX::[a,b,c]
    USE::ordered_collections
    EXAMPLE::TAGS::[ui,auth,api]

  FLOW:
    SYNTAX::[a->b->c]
    USE::sequential_steps
    EXAMPLE::PIPELINE::[INIT->BUILD->TEST->DEPLOY]

§5::COMPRESSION_CONTRACT
CONTRACT:
  MUST_PRESERVE::[
    CONST_values::byte_for_byte_match,
    code_blocks::fenced_code_verbatim,
    example_strings::canonical_format,
    quoted_canonical::behavior_definitions
  ]

  MUST_INVARIANTS::[
    claims::what_it_does,
    ratings::quality_assessments,
    limitations::where_it_breaks,
    distinctions::a_versus_b_preserved
  ]

  MAY_COMPRESS::[
    explanatory_prose::reduce_to_essence,
    expanded_rationale::drop_redundancy,
    duplicate_phrasing::single_statement
  ]

  MUST_NOT::[
    introduce_absolutes::unless_in_source,
    collapse_boundaries::preserve_distinctions,
    strengthen_claims::maintain_hedging
  ]

§6::VALIDATION
VALIDATION:
  EXTERNAL_SCHEMA::META.SCHEMA::path/to/schema.oct.md
  INTERNAL::constraints_from_L2_patterns

  CHECKS::[
    anchors_exact::CONST_values_match_source,
    boundaries_kept::distinctions_preserved,
    no_absolutes::hedging_matches_source
  ]

§7::COMPRESSION_RATIOS
RATIOS:
  VS_PROSE::5-10x[typical_reduction]
  VS_MARKDOWN::1.5-3x[format_overhead_removed]
  VS_JSON::1.2-2x[structural_overhead_reduced]

§8::DATA_EXAMPLES
EXAMPLE_SESSION:
  ID::sess_abc123
  STATUS::WIP
  PHASE::B1_FOUNDATION
  QUALITY::[tests::5/5,lint::2_errors,types::pending]
  BLOCKERS::ruff_B904|mypy_not_run
  NEXT::[fix_lint->run_types->impl_feature]
  COMMITS::[abc123::init,def456::port,ghi789::server]

EXAMPLE_PROJECT:
  NAME::hestai-mcp
  BRANCH::feat/oauth[3_ahead|0_behind]
  PHASE::B2_IMPLEMENTATION
  HEALTH::[ci::passing,coverage::87%,debt::low]
  RISKS::auth_token_expiry|rate_limit_gap
  DECISIONS::[D1::use_redis,D2::async_handlers]

EXAMPLE_KNOWLEDGE:
  TOPIC::OCTAVE_compression
  LEARNED::anchors_never_compress
  EVIDENCE::v5_spec_section_2
  APPLIES_TO::[prose_conversion,doc_optimization]

===END===
