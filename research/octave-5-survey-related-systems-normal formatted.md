# Holographic Document Language: Survey of Related Systems

## 1. Overview of the Holographic Concept

A holographic document language is a single declarative specification that simultaneously:

1. **Teaches** an LLM the expected document format via embedded examples
2. **Validates** structural and semantic constraints at runtime
3. **Declares** extraction or routing behavior for downstream systems

A canonical example is:

```
ID:: [ "sess_123" + REQUIRED -> INDEXER ]
```

This single line:
- demonstrates the expected value shape (`"sess_123"`)
- encodes a validation constraint (`REQUIRED`)
- declares operational intent (`-> INDEXER`)

The defining properties of the approach are:
- **Machine-executable** – can be parsed and acted upon by code
- **LLM-legible** – an LLM can learn the format from examples
- **Self-documenting** – the document is written in the format it defines

We evaluate existing systems against three axes:

| Axis | Definition |
|------|------------|
| **Teach** | Format learning via examples (LLM-legible) |
| **Validate** | Structure/constraint enforcement |
| **Extract** | Routing/execution binding |

---

## 2. Declarative Schema Languages

### JSON Schema

**What it solves:**
A formal grammar for validating JSON structure and basic constraints.

**Coverage:**
- **Teach:** Weak — examples are optional annotations, not central or reliably consumed
- **Validate:** Strong — types, required fields, ranges, patterns
- **Extract:** None — no execution or routing semantics

**Limitation:**
JSON Schema is validation-only. There's no concept of binding semantic tokens to runtime behavior in the core spec.

**Extensibility:**
Custom keywords/vocabularies exist (UI, docs, policy), but these are not standardized for runtime routing.

**Precedent:**
People attempt extensions for routing intent; this shows the gap exists, but ad-hoc extension fails to unify teach+validate+extract.

---

### OpenAPI (Swagger)

**What it solves:**
Describes REST APIs using JSON Schema for data models.

**Coverage:**
- **Teach:** Medium — examples and descriptions aid humans (and indirectly LLMs)
- **Validate:** Strong — runtime request/response validation
- **Extract:** Partial — code generation creates stubs, not runtime routing

**Limitation:**
OpenAPI describes interface shape, not execution logic. The spec describes what the API looks like, not how to execute application logic.

**Extensibility:**
Vendor `x-*` extensions are used to hint routing/auth/policy intent; execution remains convention/codegen-driven, not spec-native.

**Precedent:**
Shows attempted solution to semantic routing problem; but vendor-specific and convention-dependent, not unified.

---

### Protocol Buffers / Avro

**What they solve:**
Binary serialization with strict schemas and cross-language code generation.

**Coverage:**
- **Teach:** Weak — formal schemas, no inline examples
- **Validate:** Strong — enforced by generated code
- **Extract:** Compile-time — bindings occur at codegen, not runtime

**Limitation:**
Not LLM-legible or example-driven. Execution semantics live in generated code, not the schema.

**Evolution:**
Schema compatibility constraints (Protobuf field numbering, Avro rules) encode ecosystem-level semantics; custom annotations (protoc-gen-validate) bolt on semantic validation.

---

## 3. Unified Schema Languages

### CUE

**What it solves:**
Unifies schemas, constraints, and data in one artifact. The philosophy is "types, values, and constraints are all the same."

**Coverage:**
- **Teach:** Medium — can include example data in spec demonstrating format; readability depends on idiomatic style
- **Validate:** Strong — rich constraints, types, defaults
- **Extract:** Partial — computes/emits configs but no side effects

**Limitation:**
No binding to runtime behavior. Learning curve is high due to unification engine.

**Nuance:**
Syntax is human-friendly by accident (JSON-like), not designed for LLM comprehension. This contrasts with holographic, which explicitly designs for AI legibility.

> **DECISION:** CUE is the closest non-LLM analog to the holographic approach; it unifies example+schema but lacks execution binding.

---

### JSON-LD + SHACL

**What they solve:**
Semantic annotation and constraint validation for RDF graphs.

**Coverage:**
- **Teach:** Semantic — context conveys meaning, not format examples
- **Validate:** Strong — SHACL shapes enforce cardinality, types, patterns
- **Extract:** Implicit — shapes could drive routing externally

**Limitation:**
Heavyweight and not designed for prompt engineering or LLM legibility.

**SPARQL:**
SHACL supports SPARQL-based executable constraints; routing/side-effects remain external.

---

## 4. Code-Centric Validation Systems

### Zod (TypeScript)

**Coverage:**
- **Teach:** Weak — schema in code, examples in tests/docs
- **Validate:** Strong — runtime type checking, constraints
- **Extract:** Code — returns typed object for manual routing

**Limitation:**
Developer-facing, not a standalone artifact. No integrated notion of semantic actions.

---

### Pydantic (Python)

**Coverage:**
- **Teach:** Weak — `Field(example=...)` flows to docs only
- **Validate:** Strong — runtime validation, custom validators
- **Extract:** Framework — FastAPI auto-parses to model instance

**Limitation:**
Spec is embedded in code; not directly consumable by LLMs as a standalone artifact.

**Integration:**
LangChain/Guardrails use Pydantic for output parsing, showing that combining Pydantic (validation) with LLM prompting can achieve teach/validate/extract loops.

---

## 5. Grammars and Executable Specifications

### Attribute Grammars

**Coverage:**
- **Teach:** Weak — abstract rules, needs separate examples
- **Validate:** Strong — grammar enforces structure by parsing
- **Extract:** Strong — semantic actions can produce output/trigger code

**Limitation:**
High complexity; not user-friendly or LLM-legible. Writing attribute grammars is a specialized skill.

> **LEARNING:** Attribute grammars demonstrate all three axes are achievable in one artifact, but with prohibitive complexity.

---

### BDD / Gherkin

**Coverage:**
- **Teach:** Strong — scenarios ARE concrete examples in plain language
- **Validate:** Strong — test pass/fail indicates spec adherence
- **Extract:** Strong — step definitions execute described actions

**Limitation:**
Domain-specific to testing; not a general data schema system.

**Insight:**
Proves that mixing examples with executable hooks is viable and well-established.

---

## 6. LLM-Centric Structured Output Systems

### Enforcement Modes

There are two fundamentally different approaches to ensuring LLM outputs conform to structure:

| Mode | Systems | Mechanism |
|------|---------|-----------|
| **Constrained decoding** | Guidance, Outlines | Prevents invalid structure during generation; first-pass correctness |
| **Validate-and-repair** | Guardrails | Detects structure violations after generation; enables rich error feedback |

**Tradeoff:** Decoding-time prevention vs post-hoc repair affects latency, reliability, and error UX richness.

---

### OpenAI Function Calling

**What it solves:**
Structured JSON output via function signatures in prompt.

**Coverage:**
- **Teach:** Medium — schema guides model, no explicit examples
- **Validate:** Strong — JSON mode + schema enforcement ensure valid, conformant output (semantic correctness external)
- **Extract:** Strong but limited — outputs function name + args for dispatch; only discrete predeclared actions

**Scope limit:**
Does not cover scenarios where model produces documents rather than trigger functions; focused on tool use.

**Limitation:**
JSON only; no few-shot examples; predefined schemas only.

> **DECISION:** Function calling is the closest LLM technique to validate+execute binding, but has narrow scope (discrete tool calls, not document extraction).

---

### Guidance

**What it solves:**
Template-based LLM control with token-level constraints.

**Coverage:**
- **Teach:** Strong — template walks model through format
- **Validate:** Strong — token-by-token enforcement of regex/choices
- **Extract:** Strong — captures variables during generation

**Limitation:**
Spec is an executable prompt program, not a static artifact. Requires coding the logic.

**Guarantee:**
Guaranteed structure within expressible constraint class; may require retries/backtracking.

---

### Outlines

**What it solves:**
Structured output via Python types/Pydantic with constrained decoding.

**Coverage:**
- **Teach:** Strong — library automatically constructs prompt from schema
- **Validate:** Strong — grammar-based decoding guarantees structure
- **Extract:** Strong — returns typed Python objects

**Limitation:**
Schema implicit in code; not a shareable standalone artifact.

---

### Guardrails (RAIL)

**What it solves:**
Validate and auto-correct LLM outputs via RAIL spec (YAML/XML).

**Coverage:**
- **Teach:** Strong — compiles spec to prompt instructions
- **Validate:** Strong — post-generation checks with auto-retry
- **Extract:** Strong — parsed output as dict/Pydantic model

**Limitation:**
After-the-fact validation; no token-level steering. Post-generation can increase latency if retries needed.

> **DECISION:** Guardrails RAIL is the closest existing system to the holographic single-source ideal.

---

## 7. Comparative Coverage Matrix

| System | Teach | Validate | Extract |
|--------|-------|----------|---------|
| JSON Schema | Weak | Strong | None |
| OpenAPI | Medium | Strong | Partial |
| Protobuf / Avro | Weak | Strong | Compile-time |
| CUE | Medium | Strong | Partial |
| JSON-LD + SHACL | Semantic | Strong | Implicit |
| Zod / Pydantic | Weak | Strong | Code |
| Attribute Grammars | Weak | Strong | Strong |
| BDD / Gherkin | Strong | Strong | Strong |
| Function Calling | Medium | Strong | Strong |
| Guidance | Strong | Strong | Strong |
| Outlines | Strong | Strong | Strong |
| Guardrails | Strong | Strong | Strong |

**Observation:**
No single system achieves all three goals in a simple, unified artifact.

**Closest systems:** Guardrails, Outlines, CUE, function calling — but each has specific focus and limitations.

---

## 8. Novelty Assessment

The holographic approach is **not an invention of new primitives**, but a synthesis:

| Component | Draws From |
|-----------|------------|
| Validation | JSON Schema, CUE, SHACL constraint patterns |
| Examples | CUE unified data, OpenAPI examples |
| Execution | Function calling, attribute grammar semantics |

**What is genuinely novel:**

1. **Unified syntax** — Example + Validation + Routing in a single line
2. **Self-exemplifying document** — Written in the format it defines
3. **Explicit LLM legibility** — Designed for AI comprehension, not just machine parsing

**Metaphor:** Combining wheels into a car, not reinventing wheels.

---

## 9. Failure Modes

Complete taxonomy of risks:

| Failure Mode | Description | Mitigation |
|--------------|-------------|------------|
| **Complexity trap** | Spec becomes programming language with Turing completeness | Keep declarative; limit to 80% use cases |
| **Spec drift** | Spec and code diverge if not directly executable | Spec must drive execution, not describe it |
| **LLM misinterpretation** | Model ignores or misunderstands terse symbolic spec | Include meta-spec showing interpretation; validate output |
| **Valid-but-wrong** | Schema enforces structure but not semantic correctness; model produces garbage in valid format | Add semantic validators (entailment, fact-checking); validation must cover form + content |
| **Error feedback quality** | Validator errors must translate to model-fixable feedback; poor error UX kills retry loops | Invest in minimal-diff error messages and corrective prompts |
| **Scalability** | Large specs consume excessive prompt tokens | Selective spec injection; compile to efficient validators |
| **Adoption** | Perceived as reinventing JSON Schema + Guardrails | Clear benefits over piecemeal solutions; leverage existing components |

**Implication (valid-but-wrong):** This is a common challenge in LLM pipelines. The spec catches structural errors, but content may be useless. Validation of intent is harder than validation of form — a gap outside the scope of most schema-like systems.

---

## 10. Minimal Execution Layer

Required components:

| Component | Function |
|-----------|----------|
| **Parser** | Read DSL lines, extract field/example/constraint/target |
| **Validator** | Map constraints to checks; leverage JSON Schema or Pydantic |
| **Prompter** | Feed spec to LLM as template or function schema |
| **Router** | Dispatch fields to targets based on `->` bindings |

**Implementation strategy:**
- Parser: Simple string parsing or PEG (syntax is regular)
- Validator: Translate REQ/REGEX/ENUM to JSON Schema draft-07
- Prompter: Include spec in system prompt; optionally use function calling
- Router: Config mapping target labels to handlers/endpoints

**Architecture:**
Spec compiler + orchestrator implementing a teach → validate → extract loop.

---

## 11. Operational Constraints

**Observation:**
Schema-as-teaching consumes prompt tokens and increases latency/cost. You cannot always stuff the entire spec into the LLM prompt.

**Solutions:**
- Schema selection (choose relevant subset)
- Schema summarization
- Progressive disclosure
- Staged prompting
- Compilation to efficient validators

**Implication:**
The execution layer must support selective spec injection and potentially a two-pass approach (generate, then validate). Single-pass full-spec approach is not feasible at scale.

**Realism:**
This explains why no one dumps large OpenAPI specs into prompts today. The same constraint applies to the holographic approach.

---

## 12. Conclusion

**Verdict:**
- Reinvention: No
- Gap filled: Yes
- Value: Synthesis of proven ideas optimized for the LLM era

**Key insight:**
Many systems pick two of three (teach/validate/extract). The holographic approach achieves all three in one artifact.

**Learning:**
Single-source specs that guide AI generation and drive execution address a meaningful gap in LLM tooling.

---

## Appendix: Decisions and Learnings

### Decisions (explicit assessment artifacts)

1. **CUE** is the closest non-LLM analog to holographic; unifies example+schema but lacks execution binding
2. **Guardrails RAIL** is the closest to the holographic single-source ideal in the LLM space
3. **Function calling** is the closest LLM technique to validate+execute binding, but has narrow scope (discrete tool calls only)

### Learnings (extracted knowledge)

1. Attribute grammars demonstrate all three axes are achievable, but with prohibitive complexity
2. Single-source specs that guide AI and drive execution address a meaningful gap in LLM tooling
