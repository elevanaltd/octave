===OCTAVE_SCHEMA===
META:
  TYPE::LLM_PROFILE
  VERSION::"5.1.0"
  STATUS::APPROVED
  IMPLEMENTATION::PLANNED
  TOKENS::"~90"
  REQUIRES::octave-5-llm-core
  PURPOSE::L4_holographic_definitions
  IMPLEMENTATION_NOTES::"Gap 2 (constraint chain evaluation) implemented with 12 constraint types. Holographic patterns, targets, and block inheritance pending."
  IMPLEMENTATION_REF::[src/octave_mcp/core/schema.py,src/octave_mcp/core/constraints.py]
  CRITICAL_GAPS::[holographic_pattern_parsing,target_routing,block_inheritance,policy_blocks]
  IMPLEMENTED::[constraint_evaluation,constraint_conflicts]

---

// OCTAVE SCHEMA: Rules for defining document types. Inject WITH core.

§1::HOLOGRAPHIC_PATTERN
SYNTAX::KEY::["example"∧CONSTRAINT→§TARGET]
BRACKETS::holographic_container[not_a_standard_list]
COMPONENTS::[EXAMPLE,CONSTRAINT,TARGET][all_required_for_L4]

EXAMPLE::concrete_value[teaches_expected_format]
CONSTRAINT::validation_chain[∧_separated]
TARGET::extraction_destination[§prefixed]

§2::CONSTRAINTS
AVAILABLE::[REQ,OPT,CONST,REGEX,ENUM,TYPE,DIR,APPEND_ONLY,RANGE,MAX_LENGTH,MIN_LENGTH,DATE,ISO8601]
CHAIN::constraint∧constraint∧constraint[left_to_right]
EVALUATION::fail_fast[stop_on_first_failure]
REGEX_BRACKETS::quote_if_contains_brackets[REGEX["^[a-z]+$"]_not_REGEX[^[a-z]+$]]

CONSTRAINT_SYNTAX::[
  RANGE::"RANGE[min,max]"[numeric_bounds_inclusive],
  MAX_LENGTH::"MAX_LENGTH[N]"[string_or_list_max_size],
  MIN_LENGTH::"MIN_LENGTH[N]"[string_or_list_min_size],
  DATE::"DATE"[strict_YYYY_MM_DD_only],
  ISO8601::"ISO8601"[full_datetime_support]
]

CONFLICT_ERRORS::[
  REQ∧OPT[mutually_exclusive],
  ENUM[A,B]∧CONST[C][empty_intersection],
  CONST[X]∧CONST[Y][contradictory]
]

§3::TARGETS
BUILTIN::[§SELF,§META,§INDEXER,§DECISION_LOG,§RISK_LOG,§KNOWLEDGE_BASE]
FILE::§./relative/path[resolved_from_document_directory]
MULTI::§A∨§B∨§C[broadcast_to_all]
MULTI_FAILURE::non_transactional[partial_success_possible,handler_responsibility]
VALIDATION::target_must_exist[declared_in_POLICY.TARGETS∨builtin]

§4::BLOCK_INHERITANCE
SYNTAX::BLOCK[→§TARGET]:
RULE::children_inherit_parent_target_unless_they_specify_own
OVERRIDE::CHILD[→§OTHER]:[replaces_inherited]
DEPTH::unbounded_semantic[implementation_caps_at_100]

§5::POLICY_BLOCK
REQUIRED_IN_SCHEMA::[
  VERSION::"1.0",
  UNKNOWN_FIELDS::REJECT∨IGNORE∨WARN,
  TARGETS::[list_of_valid_targets]
]

§6::SCHEMA_SKELETON
// Minimal valid schema document structure
TEMPLATE:
  ===MY_SCHEMA===
  META:
    TYPE::PROTOCOL_DEFINITION
    VERSION::"1.0"
    STATUS::DRAFT

  POLICY:
    VERSION::"1.0"
    UNKNOWN_FIELDS::REJECT
    TARGETS::[§INDEXER,§DECISION_LOG]

  FIELDS:
    ID::["abc123"∧REQ→§INDEXER]
    STATUS::["ACTIVE"∧REQ∧ENUM[ACTIVE,DRAFT]→§INDEXER]
  ===END===

§7::REFERENCE
EXAMPLES::see_core.§7.SCHEMA_PATTERN
BLOCK_EXAMPLE::see_core.§7.BLOCK_INHERITANCE_PATTERN

===END===
