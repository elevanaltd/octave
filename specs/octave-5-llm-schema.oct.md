===OCTAVE_SCHEMA===
META:
  TYPE::LLM_PROFILE
  VERSION::"5.0.3"
  STATUS::APPROVED
  TOKENS::"~80"
  REQUIRES::octave-5-llm-core
  PURPOSE::L4_holographic_definitions

// OCTAVE SCHEMA: Rules for defining document types. Inject WITH core.

§1::HOLOGRAPHIC_PATTERN
SYNTAX::KEY::["example"&CONSTRAINT->§TARGET]
BRACKETS::holographic_container[not_a_standard_list]
COMPONENTS::[EXAMPLE,CONSTRAINT,TARGET][all_required_for_L4]

EXAMPLE::concrete_value[teaches_expected_format]
CONSTRAINT::validation_chain[&_separated]
TARGET::extraction_destination[§prefixed]

§2::CONSTRAINTS
AVAILABLE::[REQ,OPT,CONST,REGEX,ENUM,TYPE,DIR,APPEND_ONLY]
CHAIN::constraint&constraint&constraint[left_to_right]
EVALUATION::fail_fast[stop_on_first_failure]

CONFLICT_ERRORS::[
  REQ&OPT[mutually_exclusive],
  ENUM[A,B]&CONST[C][empty_intersection],
  CONST[X]&CONST[Y][contradictory]
]

§3::TARGETS
BUILTIN::[§SELF,§META,§INDEXER,§DECISION_LOG,§RISK_LOG,§KNOWLEDGE_BASE]
FILE::§./relative/path[resolved_from_document_directory]
MULTI::§A|§B|§C[broadcast_to_all]
MULTI_FAILURE::non_transactional[partial_success_possible,handler_responsibility]
VALIDATION::target_must_exist[declared_in_POLICY.TARGETS_or_builtin]

§4::BLOCK_INHERITANCE
SYNTAX::BLOCK[->§TARGET]:
RULE::children_inherit_parent_target_unless_they_specify_own
OVERRIDE::CHILD[->§OTHER]:[replaces_inherited]
DEPTH::unlimited[100_level_parser_limit]

§5::POLICY_BLOCK
REQUIRED_IN_SCHEMA::[
  VERSION::"1.0",
  UNKNOWN_FIELDS::REJECT|IGNORE|WARN,
  TARGETS::[list_of_valid_targets]
]

§6::REFERENCE
EXAMPLES::see_core.§7.SCHEMA_PATTERN
BLOCK_EXAMPLE::see_core.§7.BLOCK_INHERITANCE_PATTERN

===END===
