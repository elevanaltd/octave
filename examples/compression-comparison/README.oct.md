===COMPRESSION_COMPARISON===
META:
  TYPE::COMPARISON_GUIDE
  VERSION::"5.1.0"
  PURPOSE::demonstrate OCTAVE 5 compression tiers on same source document
  SOURCE::survey-original-raw.oct.md[5600 tokens]

---

TIER_COMPARISON::

LOSSLESS::
  TARGET::100%_fidelity
  TOKENS::5600[unchanged]
  LOSS::none[except_whitespace∨formatting]
  USE::critical_decisions,legal_documents,safety_analysis,audit_trails,reference_work
  WHAT_PRESERVED::[all_nuance,all_edge_cases,full_tradeoff_narratives,complete_lineage]
  METHOD::preserve_all_prose|keep_examples|document_tradeoffs
  FILE::survey-octave-5-lossless.oct.md

CONSERVATIVE::
  TARGET::85-90%_compression
  TOKENS::4800[~15%_loss]
  LOSS::redundancy⊕verbose_transitions[but_NOT_narratives]
  USE::research_summaries,design_decisions,technical_analysis,reference_with_context
  WHAT_PRESERVED::[explanatory_depth,tradeoff_narratives,execution_strategies,reasoning_chains]
  WHAT_LOST::[repetition,some_edge_cases,verbose_phrasing,transitional_prose]
  METHOD::drop_stopwords|compress_examples→inline|keep_tradeoff_narratives|remove_verbose_transitions
  FILE::survey-octave-5-conservative.oct.md
  EXAMPLE::5000_tokens→450-700_tokens_in_practice

AGGRESSIVE::
  TARGET::70%_compression
  TOKENS::1800[~68%_loss]
  LOSS::explanatory_depth⊕execution_narratives[but_CORE_thesis_preserved]
  USE::context_window_scarcity,quick_reference,decision_support,dense_summaries
  WHAT_PRESERVED::[core_thesis,analytical_conclusions,landscape_coverage,novelty_claims]
  WHAT_LOST::[explanatory_depth,execution_tradeoff_narratives,edge_case_exploration,historical_lineage]
  METHOD::drop_stopwords|compress_narratives→assertions|inline_all_examples|remove_historical_context
  FILE::survey-octave-5-compressed.oct.md
  EXAMPLE::5600_tokens→1800_tokens[shows_landscape∧conclusions_without_depth]

ULTRA::
  TARGET::50%_compression
  TOKENS::2800[~50%_loss]
  LOSS::all_narrative[only_facts∧structure_remain]
  USE::extreme_scarcity,embedding_generation,dense_indexing,lookup_tables
  WHAT_PRESERVED::[facts,numbers,names,structure,core_assertions]
  WHAT_LOST::[almost_all_explanatory_content,reasoning,tradeoff_discussion,examples]
  METHOD::bare_assertions|minimal_lists|no_examples|no_prose
  FILE::survey-octave-5-ultra.oct.md
  OUTCOME::structure∧facts_only|poor_readability|not_for_human_consumption|suitable_for_embeddings∧indexing

SELECTION_MATRIX::

  IF[critical_question_affects_safety∨legal_standing]
    THEN→LOSSLESS[no_room_for_loss]

  IF[research_artifact_published∨audience_needs_understanding]
    THEN→CONSERVATIVE[preserve_reasoning,drop_redundancy]

  IF[token_budget_tight∧loss_acceptable]
    THEN→AGGRESSIVE[keep_conclusions,lose_depth]

  IF[embedding_generation∨database_lookup]
    THEN→ULTRA[structure_only]

KEY_INSIGHTS::
  LOSSLESS_COST::preserves_everything|same_token_count_as_original[formatting_only_improvement]
  CONSERVATIVE_EFFICIENCY::achieves_~15%_token_reduction|keeps_reasoning_chains|ideal_research_documents
  AGGRESSIVE_DENSITY::achieves_~70%_reduction|still_maintains_novelty_argument∧conclusions|shown_in_assessment_as_valid
  TRADEOFF::each_tier_explicitly_declares_what_is_lost[enables_informed_reader_expectations]

METADATA_REQUIREMENT::
  ALL_COMPRESSED_DOCS::must_include_COMPRESSION_TIER_in_META
  MUST_DECLARE::[COMPRESSION_TIER,COMPRESSION_RATIO,LOSS_PROFILE,NARRATIVE_DEPTH]
  ENABLES::reader_immediately_understands_compression_intent∧loss_characteristics
  TRANSPARENCY::explicit_loss_profile_prevents_silent_degradation

FILE_STRUCTURE::
  survey-original-raw.oct.md::source_uncompressed[5600_tokens]
  survey-octave-5-lossless.oct.md::LOSSLESS_tier_example[100%_fidelity|5600_tokens]
  survey-octave-5-conservative.oct.md::CONSERVATIVE_tier_example[85%_compression|4800_tokens]
  survey-octave-5-aggressive.oct.md::AGGRESSIVE_tier_example[70%_compression|1800_tokens]
  survey-octave-5-ultra.oct.md::ULTRA_tier_example[50%_compression|2800_tokens]

HOW_TO_COMPARE::
  STEP_1::read_survey-original-raw.oct.md[understand_full_narrative]
  STEP_2::read_survey-octave-5-conservative.oct.md[see_reasoning_preserved]
  STEP_3::read_survey-octave-5-aggressive.oct.md[see_landscape_compressed]
  STEP_4::compare_against_assessment[assessment-5e4ad2eb.txt]
  OBSERVATION::CONSERVATIVE_should_feel_like_research_summary_with_depth]
  OBSERVATION::AGGRESSIVE_should_feel_like_decision_table_not_narrative]

RULES_APPLIED::
  CORE_RULES::see_@octave-5-llm-core.oct.md[envelope,operators,structure]
  DATA_RULES::see_@octave-5-llm-data.oct.md[compression_intent,compression_tiers,preservation_rules]
  COMPRESSION_DISCIPLINE::
    PRESERVE::[numbers_exact,names_identifiers,codes,operators,anchors,quoted_definitions]
    DROP::[the,a,an,of,for,to,with,that,which,basically,essentially,simply]
    REWRITE::verbose_phrase→minimal_token[preserve_meaning]

===END===
