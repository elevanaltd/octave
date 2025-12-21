===HOLOGRAPHIC_SURVEY===
META:
  TYPE::    [ "KNOWLEDGE_ARTIFACT" + CONST -> §META ]
  VERSION:: [ "1.0"                + REQ   -> §META ]
  STATUS::  [ "ACTIVE"             + REQ   -> §META ]
  NAME::    [ "Holographic Document Language: Survey of Related Systems" + OPT -> §META ]
  PURPOSE:: [ "Comparative analysis of schema/validation/execution systems vs holographic ideal" + OPT -> §META ]

// =============================================================================
// SURVEY: Systems evaluated against three goals:
//   TEACH  - Format learning via examples (LLM-legible)
//   VALIDATE - Structure/constraint enforcement
//   EXTRACT - Routing/execution binding
// =============================================================================

§1::HOLOGRAPHIC_CONCEPT
DEFINITION:
  GOAL::      [ "Single declarative spec: teaches format, validates structure, routes data" + CONST -> §SELF ]
  EXAMPLE::   [ "ID:: [ \"sess_123\" + REQUIRED -> INDEXER ]" + CONST -> §SELF ]
  PROPERTIES::[ [machine_executable, LLM_legible, self_documenting] + CONST -> §SELF ]

AXES:
  TEACH::    [ "LLM learns format via embedded examples"    + CONST -> §SELF ]
  VALIDATE:: [ "Structure/constraints enforced at runtime"  + CONST -> §SELF ]
  EXTRACT::  [ "Fields route to targets via spec bindings"  + CONST -> §SELF ]

§2::DECLARATIVE_SCHEMA_LANGUAGES
JSON_SCHEMA:
  SOLVES::     [ "Formal grammar for JSON structure validation" + CONST -> §INDEXER ]
  TEACH::      [ "WEAK: annotations/examples separate from schema" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: types, required, ranges, patterns" + CONST -> §SELF ]
  EXTRACT::    [ "NONE: no routing/execution semantics" + CONST -> §SELF ]
  LIMITATION:: [ "Validation only; no integrated teaching or execution binding" + CONST -> §SELF ]
  EXTENSIBILITY:: [ "Custom keywords/vocabularies allow non-validation semantics (UI, docs, policy); not standardized for runtime routing" + OPT -> §SELF ]

OPENAPI:
  SOLVES::     [ "RESTful API contracts with JSON Schema models" + CONST -> §INDEXER ]
  TEACH::      [ "MEDIUM: examples in docs, human-readable" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: schema validation at runtime" + CONST -> §SELF ]
  EXTRACT::    [ "PARTIAL: codegen creates stubs, not runtime routing" + CONST -> §SELF ]
  LIMITATION:: [ "Describes API shape, not execution logic" + CONST -> §SELF ]
  EXTENSIBILITY:: [ "x-* extensions used to encode routing/auth/policy; execution via codegen + conventions, not spec-native" + OPT -> §SELF ]

PROTOBUF_AVRO:
  SOLVES::     [ "Binary serialization with schema definitions" + CONST -> §INDEXER ]
  TEACH::      [ "WEAK: formal schemas, no inline examples" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: type enforcement via generated code" + CONST -> §SELF ]
  EXTRACT::    [ "COMPILE_TIME: codegen bindings, not runtime directives" + CONST -> §SELF ]
  LIMITATION:: [ "Schema-to-code path; not LLM-legible or example-driven" + CONST -> §SELF ]
  AVRO_NOTE::  [ "Schema always embedded with data for self-description" + OPT -> §SELF ]
  EVOLUTION::  [ "Schema compatibility (Protobuf field numbering, Avro rules) encode ecosystem-level semantics; custom annotations (protoc-gen-validate) bolt on semantic validation" + OPT -> §SELF ]

§3::UNIFIED_SCHEMA_LANGUAGES
CUE:
  SOLVES::     [ "Unify schemas, constraints, and data in one artifact" + CONST -> §INDEXER ]
  PHILOSOPHY:: [ "Types, values, constraints are all the same" + CONST -> §SELF ]
  TEACH::      [ "STRONG: example-shaped instances in spec; LLM teaching depends on prompt framing" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: rich constraints, types, defaults" + CONST -> §SELF ]
  EXTRACT::    [ "PARTIAL: computes/emits configs but no side-effects" + CONST -> §SELF ]
  LIMITATION:: [ "No runtime behavior binding; learning curve for unification engine" + CONST -> §SELF ]
  DECISION_1:: [ "CUE closest non-LLM analog to holographic; unifies example+schema" + OPT -> §DECISION_LOG ]

JSON_LD_SHACL:
  SOLVES::     [ "Semantic annotations + graph constraints for RDF data" + CONST -> §INDEXER ]
  TEACH::      [ "SEMANTIC: context gives meaning, not format examples" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: SHACL shapes enforce cardinality, types, patterns" + CONST -> §SELF ]
  EXTRACT::    [ "IMPLICIT: shape validation could drive routing" + CONST -> §SELF ]
  LIMITATION:: [ "Heavyweight; not designed for LLM prompt engineering" + CONST -> §SELF ]
  SPARQL::     [ "SHACL supports SPARQL-based executable constraints; routing/side-effects remain external" + OPT -> §SELF ]

§4::CODE_CENTRIC_VALIDATION
ZOD:
  SOLVES::     [ "TypeScript runtime schema validation with type inference" + CONST -> §INDEXER ]
  TEACH::      [ "WEAK: schema in code, examples in tests/docs" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: runtime type checking, constraints" + CONST -> §SELF ]
  EXTRACT::    [ "CODE: returns typed object for manual routing" + CONST -> §SELF ]
  LIMITATION:: [ "Developer-centric; not presentable to LLM" + CONST -> §SELF ]

PYDANTIC:
  SOLVES::     [ "Python data validation via type hints" + CONST -> §INDEXER ]
  TEACH::      [ "WEAK: Field(example=...) flows to docs only" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: runtime validation, custom validators" + CONST -> §SELF ]
  EXTRACT::    [ "FRAMEWORK: FastAPI auto-parses to model instance" + CONST -> §SELF ]
  LIMITATION:: [ "Spec embedded in code; not standalone artifact" + CONST -> §SELF ]
  INTEGRATION::[ "LangChain/Guardrails use Pydantic for output parsing" + OPT -> §SELF ]

§5::GRAMMARS_AND_EXECUTABLE_SPECS
ATTRIBUTE_GRAMMARS:
  SOLVES::     [ "Formal syntax + semantic actions attached to parse rules" + CONST -> §INDEXER ]
  TEACH::      [ "WEAK: abstract rules, needs separate examples" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: grammar enforces structure by parsing" + CONST -> §SELF ]
  EXTRACT::    [ "STRONG: semantic actions can produce output/trigger code" + CONST -> §SELF ]
  LIMITATION:: [ "High complexity; not user-friendly or LLM-legible" + CONST -> §SELF ]
  LEARNING::   [ "Covers all three axes but with prohibitive complexity" + OPT -> §KNOWLEDGE_BASE ]

BDD_GHERKIN:
  SOLVES::     [ "Natural language scenarios linked to executable step definitions" + CONST -> §INDEXER ]
  TEACH::      [ "STRONG: scenarios ARE concrete examples" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: test pass/fail indicates spec adherence" + CONST -> §SELF ]
  EXTRACT::    [ "STRONG: step definitions execute described actions" + CONST -> §SELF ]
  LIMITATION:: [ "Domain-specific to testing; not data schemas" + CONST -> §SELF ]
  INSIGHT::    [ "Proves mixing examples with executable hooks is viable" + OPT -> §SELF ]

§6::LLM_CENTRIC_TOOLS

LLM_ENFORCEMENT_MODES:
  CONSTRAINED_DECODING:: [ "Guidance/Outlines: prevents invalid structure during generation; first-pass correctness" + CONST -> §SELF ]
  VALIDATE_AND_REPAIR::  [ "Guardrails: detects structure violations after generation; enables rich error feedback" + CONST -> §SELF ]
  TRADEOFF::             [ "Decoding speed + latency (retries); complexity vs error UX richness" + CONST -> §SELF ]

OPENAI_FUNCTION_CALLING:
  SOLVES::     [ "Structured JSON output via function signatures in prompt" + CONST -> §INDEXER ]
  TEACH::      [ "MEDIUM: schema guides model, no explicit examples" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: JSON mode + schema enforcement ensure valid, conformant output (semantic correctness external)" + CONST -> §SELF ]
  EXTRACT::    [ "STRONG: model outputs function name + args for dispatch" + CONST -> §SELF ]
  LIMITATION:: [ "JSON only; no few-shot examples; predefined schemas only" + CONST -> §SELF ]
  DECISION_2:: [ "Function calling closest LLM technique to validate+execute binding" + OPT -> §DECISION_LOG ]

GUIDANCE:
  SOLVES::     [ "Template-based LLM control with token-level constraints" + CONST -> §INDEXER ]
  TEACH::      [ "STRONG: template walks model through format" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: token-by-token enforcement of regex/choices" + CONST -> §SELF ]
  EXTRACT::    [ "STRONG: captures variables during generation" + CONST -> §SELF ]
  LIMITATION:: [ "Spec is executable prompt program, not static artifact" + CONST -> §SELF ]
  GUARANTEE::  [ "Guaranteed structure within expressible constraint class; may require retries/backtracking" + OPT -> §SELF ]

OUTLINES:
  SOLVES::     [ "Structured output via Python types/Pydantic with constrained decoding" + CONST -> §INDEXER ]
  TEACH::      [ "AUTO: library constructs prompt from schema" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: grammar-based decoding guarantees structure" + CONST -> §SELF ]
  EXTRACT::    [ "STRONG: returns typed Python objects" + CONST -> §SELF ]
  LIMITATION:: [ "Schema implicit in code; not shareable artifact" + CONST -> §SELF ]

GUARDRAILS:
  SOLVES::     [ "Validate and auto-correct LLM outputs via RAIL spec" + CONST -> §INDEXER ]
  SPEC_FORMAT::[ "YAML/XML with schema, types, constraints, validators" + CONST -> §SELF ]
  TEACH::      [ "STRONG: compiles spec to prompt instructions" + CONST -> §SELF ]
  VALIDATE::   [ "STRONG: post-generation checks with auto-retry" + CONST -> §SELF ]
  EXTRACT::    [ "STRONG: parsed output as dict/Pydantic model" + CONST -> §SELF ]
  LIMITATION:: [ "After-the-fact validation; no token-level steering" + CONST -> §SELF ]
  DECISION_3:: [ "Guardrails RAIL closest to holographic single-source ideal" + OPT -> §DECISION_LOG ]

§7::COMPARATIVE_MATRIX
// Coverage: [TEACH, VALIDATE, EXTRACT] scored as [NONE|WEAK|MEDIUM|PARTIAL|STRONG|AUTO]

COVERAGE:
  JSON_SCHEMA::      [ [WEAK, STRONG, NONE]    + CONST -> §INDEXER ]
  OPENAPI::          [ [MEDIUM, STRONG, PARTIAL] + CONST -> §INDEXER ]
  PROTOBUF_AVRO::    [ [WEAK, STRONG, COMPILE_TIME] + CONST -> §INDEXER ]
  CUE::              [ [STRONG, STRONG, PARTIAL] + CONST -> §INDEXER ]
  JSON_LD_SHACL::    [ [SEMANTIC, STRONG, IMPLICIT] + CONST -> §INDEXER ]
  ZOD_PYDANTIC::     [ [WEAK, STRONG, CODE]    + CONST -> §INDEXER ]
  ATTR_GRAMMARS::    [ [WEAK, STRONG, STRONG]  + CONST -> §INDEXER ]
  BDD_GHERKIN::      [ [STRONG, STRONG, STRONG] + CONST -> §INDEXER ]
  FUNCTION_CALLING:: [ [MEDIUM, STRONG, STRONG] + CONST -> §INDEXER ]
  GUIDANCE::         [ [STRONG, STRONG, STRONG] + CONST -> §INDEXER ]
  OUTLINES::         [ [AUTO, STRONG, STRONG]  + CONST -> §INDEXER ]
  GUARDRAILS::       [ [STRONG, STRONG, STRONG] + CONST -> §INDEXER ]

GAP_ANALYSIS:
  OBSERVATION:: [ "No single system achieves all three in simple unified artifact" + CONST -> §SELF ]
  CLOSEST::     [ [Guardrails, Outlines, CUE, function_calling] + CONST -> §SELF ]
  MISSING::     [ "LLM-legible self-exemplifying spec with execution binding" + CONST -> §SELF ]

§8::NOVELTY_ASSESSMENT
HOLOGRAPHIC_INNOVATION:
  UNIFIED_SYNTAX::    [ "Example + Validation + Routing in single line" + CONST -> §SELF ]
  SELF_EXEMPLIFYING:: [ "Document written in format it defines" + CONST -> §SELF ]
  LLM_LEGIBILITY::    [ "Designed for AI comprehension, not just machine parsing" + CONST -> §SELF ]

SYNTHESIS_NOT_INVENTION:
  VALIDATION::  [ "Draws from JSON Schema, CUE, SHACL constraint patterns" + CONST -> §SELF ]
  EXAMPLES::    [ "Draws from CUE unified data, OpenAPI examples" + CONST -> §SELF ]
  EXECUTION::   [ "Draws from function calling, attribute grammar semantics" + CONST -> §SELF ]
  METAPHOR::    [ "Combining wheels into car, not reinventing wheels" + CONST -> §SELF ]

§9::FAILURE_MODES
COMPLEXITY_TRAP:
  RISK::       [ "Spec becomes programming language with full Turing completeness" + CONST -> §RISK_LOG ]
  MITIGATION:: [ "Keep declarative; limit to 80% use cases" + CONST -> §SELF ]

SPEC_DRIFT:
  RISK::       [ "Spec and code diverge if not directly executable" + CONST -> §RISK_LOG ]
  MITIGATION:: [ "Spec must drive execution, not describe it" + CONST -> §SELF ]

LLM_MISINTERPRETATION:
  RISK::       [ "Model ignores or misunderstands terse symbolic spec" + CONST -> §RISK_LOG ]
  MITIGATION:: [ "Include meta-spec showing interpretation; validate output" + CONST -> §SELF ]

MODEL_OBEDIENCE:
  RISK::       [ "Syntactically valid but semantically wrong output" + CONST -> §RISK_LOG ]
  MITIGATION:: [ "Validation layer catches deviations; retry loop" + CONST -> §SELF ]

SCALABILITY:
  RISK::       [ "Large specs consume excessive prompt tokens" + CONST -> §RISK_LOG ]
  MITIGATION:: [ "Selective spec injection; compile to efficient validators" + CONST -> §SELF ]

ADOPTION:
  RISK::       [ "Perceived as reinventing JSON Schema + Guardrails" + CONST -> §RISK_LOG ]
  MITIGATION:: [ "Clear benefits over piecemeal solutions; leverage existing components" + CONST -> §SELF ]

VALID_BUT_WRONG:
  RISK::       [ "Schema enforces structure but not semantic correctness; output passes validation yet is factually/logically wrong" + CONST -> §RISK_LOG ]
  MITIGATION:: [ "Add semantic validators (entailment, fact-checking); validation chain must cover form + content" + CONST -> §SELF ]

ERROR_FEEDBACK_QUALITY:
  RISK::       [ "Validator errors must translate to model-fixable feedback; poor error UX kills retry loops" + CONST -> §RISK_LOG ]
  MITIGATION:: [ "Invest in minimal-diff error messages and corrective prompts; test feedback loop quality" + CONST -> §SELF ]

§10::MINIMAL_EXECUTION_LAYER
COMPONENTS:
  PARSER::     [ "Read DSL lines, extract field/example/constraint/target" + REQ -> §SELF ]
  VALIDATOR::  [ "Map constraints to checks; leverage JSON Schema or Pydantic" + REQ -> §SELF ]
  PROMPTER::   [ "Feed spec to LLM as template or function schema" + REQ -> §SELF ]
  ROUTER::     [ "Dispatch fields to targets based on -> bindings" + REQ -> §SELF ]

IMPLEMENTATION_STRATEGY:
  PARSER::     [ "Simple string parsing or PEG (syntax is regular)" + CONST -> §SELF ]
  VALIDATOR::  [ "Translate REQ/REGEX/ENUM to JSON Schema draft-07" + CONST -> §SELF ]
  PROMPTER::   [ "Include spec in system prompt; optionally use function calling" + CONST -> §SELF ]
  ROUTER::     [ "Config mapping target labels to handlers/endpoints" + CONST -> §SELF ]

ARCHITECTURE::  [ "Spec compiler + orchestrator: teach->validate->extract loop" + CONST -> §SELF ]

§11::OPERATIONAL_CONSTRAINTS
CONTEXT_AND_LATENCY:
  OBSERVATION:: [ "Schema-as-teaching consumes prompt tokens and increases latency/cost" + CONST -> §SELF ]
  SOLUTIONS::   [ [schema_selection, schema_summarization, progressive_disclosure, staged_prompting] + CONST -> §SELF ]
  IMPLICATION:: [ "Execution layer must support selective spec injection; real systems cannot always use full spec in every call" + CONST -> §SELF ]

§12::CONCLUSIONS
VERDICT:
  REINVENTION:: [ false + CONST -> §SELF ]
  GAP_FILLED::  [ true  + CONST -> §SELF ]
  VALUE::       [ "Synthesis of proven ideas optimized for LLM era" + CONST -> §SELF ]

KEY_INSIGHT:
  STATEMENT:: [ "Many systems pick two of three; holographic achieves all three in one artifact" + CONST -> §KNOWLEDGE_BASE ]

LEARNING:: [ "Single-source specs that guide AI and drive execution address meaningful gap in LLM tooling" + CONST -> §KNOWLEDGE_BASE ]

===END===
