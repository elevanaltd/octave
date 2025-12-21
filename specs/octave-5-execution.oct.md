===OCTAVE_V5_EXECUTION===
META:
  TYPE::PROTOCOL_DEFINITION
  VERSION::"5.0"
  STATUS::ACTIVE
  NAME::"OCTAVE Execution Profile"
  PURPOSE::"Runtime integration, enforcement strategies, and implementation guidance"
  EXTENDS::octave-5.oct.md

// =============================================================================
// EXECUTION PROFILE: The Runtime Layer
// Bridges spec and implementation with operational guidance
// Contains: Parser, Validator, Prompter, Router components
// =============================================================================

§1::EXECUTION_LAYER_ARCHITECTURE
// Research: Minimal execution layer requires four components
COMPONENTS:
  PARSER::[
    FUNCTION::"Read OCTAVE, extract field/example/constraint/target",
    IMPLEMENTATION::"Simple string parsing or PEG (syntax is regular)",
    OUTPUT::structured_AST
  ]
  VALIDATOR::[
    FUNCTION::"Map constraints to validation checks",
    IMPLEMENTATION::"Translate REQ/REGEX/ENUM to JSON Schema draft-07 or Pydantic",
    OUTPUT::validation_result[pass|fail+errors]
  ]
  PROMPTER::[
    FUNCTION::"Feed spec to LLM as template or function schema",
    IMPLEMENTATION::"Inject schema into system prompt; optionally use function calling",
    OUTPUT::llm_prompt
  ]
  ROUTER::[
    FUNCTION::"Dispatch fields to targets based on -> bindings",
    IMPLEMENTATION::"Config mapping target labels to handlers/endpoints",
    OUTPUT::routed_data
  ]

ARCHITECTURE::"Spec compiler + orchestrator: teach -> validate -> extract loop"

§2::LLM_ENFORCEMENT_MODES
// Research: Two fundamentally different approaches
MODES:
  CONSTRAINED_DECODING:
    DESCRIPTION::"Prevents invalid structure during generation"
    TOOLS::[Guidance,Outlines,function_calling]
    MECHANISM::"Token-level steering based on grammar/schema"
    LATENCY::higher[schema_in_prompt]
    GUARANTEE::first_pass_structural_correctness
    USE_WHEN::"Critical fields that must be valid immediately"

  VALIDATE_AND_REPAIR:
    DESCRIPTION::"Detects violations after generation; enables rich feedback"
    TOOLS::[Guardrails,Pydantic,custom_validators]
    MECHANISM::"Post-generation checking with auto-retry"
    LATENCY::variable[depends_on_retry_count]
    GUARANTEE::eventual_consistency
    USE_WHEN::"Large schemas where token budget matters"

RECOMMENDED::HYBRID
HYBRID_APPROACH:
  STRATEGY::"Minimal schema in prompt; full validation post-generation"
  INJECT::"Critical L4 fields for constrained decoding"
  VALIDATE::"All fields against full schema externally"
  BENEFIT::"Balances token cost vs validation strength"

§3::TOKEN_BUDGET_MANAGEMENT
// Research: Schema-as-teaching consumes prompt tokens
PROBLEM::"Large specs consume excessive prompt tokens; cannot stuff entire spec"
REALISM::"This is why no one dumps large OpenAPI specs into prompts"

STRATEGIES:
  SELECTIVE_INJECTION:
    MECHANISM::"Include only relevant schema subset"
    IMPLEMENTATION::"Schema selector based on task context"
    EXAMPLE::"For user creation, inject USER schema, not full spec"

  PROGRESSIVE_DISCLOSURE:
    MECHANISM::"Reveal schema complexity incrementally"
    IMPLEMENTATION::"Start L1, add constraints on error"
    EXAMPLE::"First pass minimal; retry with L4 on validation failure"

  STAGED_PROMPTING:
    MECHANISM::"Multi-turn with schema chunks"
    IMPLEMENTATION::"Schema→Generate→Validate→Refine loop"

  TWO_PASS_VALIDATION:
    MECHANISM::"Generate freely; validate against external schema"
    IMPLEMENTATION::[
      "Pass 1: Minimal hints in prompt, generate output",
      "Pass 2: Validate output against full schema offline",
      "Pass 3: If errors, re-prompt with error feedback"
    ]

§4::FAILURE_MODE_IMPLEMENTATIONS
// Maps research failure modes to concrete implementations
COMPLEXITY_TRAP:
  MITIGATION::"Keep declarative; limit to 80% use cases"
  IMPLEMENTATION::[
    "No conditionals or loops in OCTAVE",
    "No computed values",
    "No Turing-complete features",
    "Reject specs with >500 fields"
  ]
  VALIDATION::"Parser rejects non-declarative constructs"

SPEC_DRIFT:
  MITIGATION::"Spec must DRIVE execution, not describe it"
  IMPLEMENTATION::[
    "Schema defines validation rules executed at runtime",
    "Extraction targets map to actual handlers",
    "No dead-letter specs"
  ]
  VALIDATION::"CI checks that all targets have registered handlers"

LLM_MISINTERPRETATION:
  MITIGATION::"Include meta-spec; validate all output"
  IMPLEMENTATION::[
    "Self-exemplifying specs as validation test cases",
    "Meta-spec comments explaining symbols",
    "100% output validation (no trust)"
  ]
  VALIDATION::"Parser consumes its own spec as test"

ERROR_FEEDBACK_QUALITY:
  MITIGATION::"Minimal-diff error messages for retry loops"
  IMPLEMENTATION::[
    "ERROR_FORMAT: FIELD::{name} EXPECTED::{constraint} GOT::{actual}",
    "Single error per retry (not error dump)",
    "Actionable correction hints"
  ]
  VALIDATION::"Error messages tested for LLM parseability"

VALID_BUT_WRONG:
  MITIGATION::"Semantic validators beyond structure"
  IMPLEMENTATION::[
    "Application-layer validation hooks",
    "Domain-specific semantic checks",
    "Human review for critical outputs"
  ]
  VALIDATION::"Semantic validation coverage metrics"

SCALABILITY:
  MITIGATION::"Selective injection; efficient validators"
  IMPLEMENTATION::[
    "Compile schema to JSON Schema for fast validation",
    "Cache compiled validators",
    "Lazy loading of schema sections"
  ]
  VALIDATION::"Performance benchmarks for validation"

§5::INTEGRATION_PATTERNS
// How to use OCTAVE with common LLM tools
WITH_GUIDANCE:
  APPROACH::"Compile OCTAVE constraints to Guidance grammar"
  EXAMPLE:
    OCTAVE::"STATUS:: [ \"ACTIVE\" + ENUM[ACTIVE,DRAFT,ARCHIVED] -> §META ]"
    GUIDANCE::"{{select 'STATUS' options=['ACTIVE','DRAFT','ARCHIVED']}}"

WITH_OUTLINES:
  APPROACH::"Convert OCTAVE schema to Pydantic model for Outlines"
  EXAMPLE:
    OCTAVE::"EMAIL:: [ \"j@test.com\" + REGEX[^.+@.+$] -> §SELF ]"
    PYDANTIC::"email: str = Field(pattern=r'^.+@.+$')"

WITH_FUNCTION_CALLING:
  APPROACH::"Compile OCTAVE to OpenAI function schema"
  EXAMPLE:
    OCTAVE::"USER:: [ {...} + REQ -> §SELF ]"
    FUNCTION::'{"name":"create_user","parameters":{...}}'

WITH_GUARDRAILS:
  APPROACH::"Translate OCTAVE to RAIL spec"
  EXAMPLE:
    OCTAVE::"NAME:: [ \"John\" + REQ -> §INDEXER ]"
    RAIL::"<string name='NAME' required='true'/>"

WITH_PYDANTIC:
  APPROACH::"Generate Pydantic models from OCTAVE schema"
  BENEFIT::"FastAPI auto-parsing, type hints, runtime validation"

§6::TWO_PASS_VALIDATION_PATTERN
// Detailed implementation of recommended approach
PATTERN:
  PASS_1_GENERATE:
    INPUT::user_request + minimal_schema_hints
    OUTPUT::raw_llm_output
    SCHEMA_IN_PROMPT::L2[key_constraints_only]

  PASS_2_VALIDATE:
    INPUT::raw_llm_output + full_schema
    VALIDATOR::compiled_json_schema|pydantic
    OUTPUT::validation_result

  PASS_3_REPAIR:
    CONDITION::IF[validation_failed]
    INPUT::original_output + error_feedback
    PROMPT::"Fix the following error: {minimal_diff_message}"
    MAX_RETRIES::3

RETRY_STRATEGY:
  SINGLE_ERROR::"Report one error at a time for focused fix"
  PROGRESSIVE::"Each retry adds more schema context"
  BACKOFF::"Increasing schema injection on each failure"

§7::ERROR_MESSAGE_SPECIFICATION
// Minimal-diff format for LLM retry loops
FORMAT:
  STRUCTURE::"FIELD::{field} EXPECTED::{constraint} GOT::{value}"
  EXAMPLES::[
    "FIELD::STATUS EXPECTED::ENUM[ACTIVE,DRAFT] GOT::active",
    "FIELD::EMAIL EXPECTED::REGEX[^.+@.+$] GOT::invalid",
    "FIELD::NAME EXPECTED::REQ GOT::null"
  ]

PRINCIPLES::[
  "One error per message",
  "Show expected vs actual",
  "No stack traces",
  "Actionable without context lookup"
]

§8::PARSER_IMPLEMENTATION_NOTES
SYNTAX_CHARACTERISTICS::"OCTAVE syntax is regular (no recursion in grammar)"
RECOMMENDED::"PEG parser or simple line-by-line processing"

TOKENIZATION:
  OPERATORS::["::",":","->","+","§","//","[","]","|"]
  IDENTIFIERS::alphanumeric_underscore
  STRINGS::bare_words|"quoted"
  INDENTATION::significant[2_spaces]

ERROR_RECOVERY:
  STRATEGY::"Skip invalid lines with warning; continue parsing"
  RATIONALE::"Partial parse more useful than complete failure"

§9::VALIDATOR_IMPLEMENTATION_NOTES
CONSTRAINT_TO_JSON_SCHEMA:
  REQ::'"required":["field"]'
  OPT::no_required_entry
  CONST::'"const":"value"'
  REGEX::'"pattern":"regex"'
  ENUM::'"enum":["a","b","c"]'
  TYPE::'"type":"string|number|boolean|array"'

VALIDATION_APPROACH:
  RECOMMEND::jsonschema_python|ajv_javascript
  BENEFIT::"Leverage mature validation libraries"

§10::ROUTER_IMPLEMENTATION_NOTES
TARGET_MAPPING:
  CONFIGURATION::"Target labels map to handler functions/endpoints"
  EXAMPLE:
    §INDEXER::index_service.add
    §DECISION_LOG::decision_tracker.log
    §META::document_metadata.update

ROUTING_FLOW:
  PARSE::octave_document
  EXTRACT::fields_with_targets
  DISPATCH::to_registered_handlers

§11::META_COMMENTARY
// Why this spec uses L2 data-ish style
THIS_DOCUMENT:
  MODE::DATA_L2[operational_focus|implementation_guidance]
  WHY::"Implementation guide, not teaching artifact; compression valued"
  EXEMPLIFIES::"Production usage pattern for operational docs"
  NOTE::"Uses more structure than pure L1 for clarity"

===END===
