# Holographic Document Language: Survey of Related Systems

## Overview of the "Holographic" Approach

The holographic document language concept envisions a single declarative specification that simultaneously:

1. **Teaches** an LLM the desired document format by example
2. **Validates** rules (required fields, patterns, constraints)
3. **Declares** extraction or routing behavior for each piece of data

For example, a line like:

```
ID:: [ "sess_123" + REQUIRED -> INDEXER ]
```

serves as a self-documenting schema: it shows an example value ("sess_123"), marks the field as required, and indicates that the ID field should be sent to an INDEXER component. The goal is a single-source, executable spec that is both machine-executable and LLM-legible (understandable by a language model via examples).

This section surveys existing systems and standards to see how they compare along three axes:

- **Teaching format** – Can an LLM learn the format from examples?
- **Validation** – Does it enforce structure and constraints?
- **Extraction/routing** – Does it specify what to do with data?

For each system, we note what problem it solves, which of the three goals it supports, and where it falls short relative to the holographic ideal.

---

## Declarative Schema Languages

### JSON Schema

**What it solves:** JSON Schema provides a formal grammar for defining the structure and contents of JSON data. It is primarily used to validate JSON documents, ensuring required properties are present and values meet constraints (e.g. number ranges, string patterns). JSON Schema is human- and machine-readable and serves as a "blueprint" of what JSON objects are considered valid.

**Teach/Validate/Extract:**
- **Validate** – Excellent. JSON Schema can enforce types, required fields, value ranges, allowed formats, etc. (e.g. ensuring an age is an integer between 18 and 64).
- **Teach** – Weak. While some JSON Schema versions allow examples as metadata, these are not primarily meant for LLM consumption, and JSON Schema does not generate examples by itself – it only describes what's valid.
- **Extract** – None. JSON Schema does not natively support extraction or routing instructions; it focuses on describing data shape with no mechanism to trigger actions based on schema content.

**Limitations:** JSON Schema covers the validation axis but falls short on integrated teaching and execution aspects. Examples are often separate from the schema (in documentation or OpenAPI files rather than the schema itself). There's no concept of binding semantic tokens to runtime behavior. If you wanted to route or act on data (as the holographic spec's `-> INDEXER` suggests), you'd need custom extensions or external code.

---

### OpenAPI (Swagger)

**What it solves:** OpenAPI is a standard for describing RESTful API contracts, including endpoints, their parameters, and the structure of request/response bodies. It leverages JSON Schema for data models and is meant to be read by both humans and machines, enabling discovery of service capabilities without needing to read source code.

**Teach/Validate/Extract:**
- **Teach** – Medium. OpenAPI includes human-friendly descriptions and example values for fields, which help document the format for human developers and could be shown to an LLM as examples.
- **Validate** – Strong. You can validate actual API requests/responses against the schema at runtime.
- **Extract** – Partial. OpenAPI defines operations (endpoints) and ties each data schema to a particular operation. Code generation tools use the spec to create handlers or stubs, which is a form of extraction: e.g., generating a function for an endpoint that yields a data object of the described schema. Still, the actual runtime behavior (what happens to data after validation) is implemented in code outside the spec.

**Limitations:** OpenAPI is closer to the holographic idea than pure JSON Schema in that it often bundles examples with the schema. However, it falls short of a unified executable spec. The spec describes what the API looks like, not how to execute application logic. Semantic or routing annotations (like `-> INDEXER`) are not standard in OpenAPI, though one could use vendor-specific extensions (x-... fields) to hint at operational intent.

---

### Protocol Buffers and Apache Avro

**What they solve:** Protocol Buffers (protobuf) and Avro are binary serialization formats with schema definitions. They are used to define structured data for efficient storage or RPC, often in distributed systems. You write a schema (.proto files for Protobuf, or a JSON schema for Avro), and tools generate code in various languages to read/write that data. Protobuf is language- and platform-neutral, and it generates native code bindings for ease of use. Avro similarly defines records, enums, arrays, etc., and emphasizes that data files are always stored with their schema for self-description.

**Teach/Validate/Extract:**
- **Validate** – Strong. A protobuf message or Avro record is validated to ensure it matches the schema – required fields are present, fields have the correct type, etc.
- **Teach** – Weak. Protobuf schemas are quite formal and not designed for an LLM to read as examples. They contain field names and types, but no example data inline. Avro schemas, being JSON, could include default values and doc strings, but again no explicit examples of data instances.
- **Extract** – Compile-time. Once you have a schema, tools automatically parse binary data into structured objects. The "operational intent" is typically compiled into the program – the schema itself doesn't contain directives like `-> INDEXER`; the mapping to runtime logic is through generated code.

**Limitations:** Protobuf/Avro excel at shape validation and cross-language data exchange, but are not LLM-legible or example-driven. There is no notion of embedding an example value in a .proto file (beyond comments for humans). The specs are also not inherently "executable" beyond enabling (through codegen) the serialization processes. They don't unify the documentation of format with its execution.

---

## Unified Schema and Constraint Languages

### CUE Language

**What it solves:** CUE is a configuration and data constraint language that aims to unify schemas, configuration data, and constraints in one place. In CUE, the same file can contain type definitions, value constraints, and actual data, using a syntax that is a superset of JSON with enhancements. The philosophy is that "types, values, and constraints are all the same" in CUE – there is no hard separation between a schema and an instance. This allows you to define a schema, refine it with additional constraints (like regex patterns, bounds, etc.), and even include concrete example data all in one unified structure.

**Teach/Validate/Extract:**
- **Teach** – Strong. CUE specs often include example blocks that concretely show the format. The syntax is relatively human-friendly (similar to JSON/YAML but with type notations), so an LLM could potentially read a CUE file and extract the pattern.
- **Validate** – Strong. You can mark fields optional or required, set allowed value ranges, regex patterns, enums, and more. You can actually embed an example and have the system verify it.
- **Extract** – Partial. CUE is designed to be executable in the sense that you can run the CUE tool to produce a final JSON/YAML output or validate inputs. It can perform computations like default propagation. However, CUE itself doesn't trigger external side-effects by default – it's more about computing a result or verifying constraints rather than calling arbitrary systems.

**Limitations:** CUE comes very close to the holographic ideal on the teach + validate combination. Where it breaks relative to the holographic approach is binding to runtime behaviors. CUE ensures data consistency but does not inherently know about an INDEXER or other target system – those would be abstract labels unless you write additional code to interpret them. Another challenge is complexity: CUE's power comes with a learning curve.

**Key insight:** CUE is the closest non-LLM-centric analog to the holographic approach, showing that unifying examples with schema is achievable.

---

### JSON-LD with SHACL

**What it solves:** JSON-LD is a way to annotate JSON data with Linked Data semantics – giving context and meaning to JSON fields by mapping them to an ontology or vocabulary (like schema.org). It makes JSON data self-descriptive and unambiguous for machines. SHACL (Shapes Constraint Language) is a W3C standard for describing constraints on RDF graphs. SHACL lets you define "shapes" that data must conform to – essentially schema rules for graph data, including cardinalities, types, and complex conditions.

**Teach/Validate/Extract:**
- **Teach** – Semantic. A JSON-LD context gives meaning to terms. An LLM that knows schema.org might infer that ID is a unique identifier concept, but this doesn't teach the format per se.
- **Validate** – Strong. SHACL shapes provide very expressive validation rules, including semantic consistency, not just structure.
- **Extract** – Implicit. One could use the semantics to route data: if data conforms to a RiskLogEntry shape, send it to a risk log store. In practice, using SHACL in execution is usually about rejecting data that doesn't conform or categorizing data, with the actual routing logic separate.

**Limitations:** The combination of JSON-LD + SHACL provides a rich semantic schema but is quite heavyweight and not designed for ease of use in prompt engineering. SHACL is more for software agents and developers with domain knowledge. It lacks inline examples. It solves a slightly different problem (ensuring data quality in knowledge graphs) rather than instructing an AI assistant how to format output.

---

## Code-Centric Validation Libraries

### Zod (TypeScript)

**What it solves:** Zod is a TypeScript-first runtime schema validation library. It allows developers to define a schema in code (using a fluent API) and then parse/validate data against it. On success, it returns a strongly-typed object that TypeScript knows matches the schema.

**Teach/Validate/Extract:**
- **Validate** – Strong. You can enforce constraints like string regex patterns, numeric ranges, enums, etc.
- **Teach** – Weak. Zod schemas don't provide explicit teaching-by-example; examples would live in tests or comments. An LLM wouldn't easily intuit the expected format just from the Zod code unless it's very familiar with Zod syntax.
- **Extract** – Code-level. Once data is validated, you get a native JS object with proper types. At that point, you can route or use it in code as needed. Zod itself doesn't automate routing.

**Limitations:** Zod is very developer-centric and not a separate "schema file" that you might present to an LLM. It lacks an integrated notion of semantic actions. It's just validation; execution logic is entirely outside the schema.

---

### Pydantic (Python)

**What it solves:** Pydantic is a popular Python library for data validation and settings management. It allows you to define Python classes (models) with type hints, and it will automatically validate and convert input data to those types. It's used in frameworks like FastAPI to validate request bodies and query params.

**Teach/Validate/Extract:**
- **Validate** – Strong. Pydantic will ensure that an email field matches an email regex or that a list of integers has no negatives, if you specify those rules.
- **Teach** – Weak. You can include an example for a field via `Field(example=123)`, which flows into generated documentation, but within the Pydantic class definition itself, the example is just metadata.
- **Extract** – Framework-level. In FastAPI, you declare an endpoint function that takes a Pydantic model as a parameter, and FastAPI will parse the request JSON into that model and hand it to your function. That is a clear linkage from spec to execution, albeit orchestrated by the framework. Pydantic itself doesn't know about external systems like "INDEXER".

**Limitations:** Pydantic is spec embedded in code; not a standalone artifact. There's no native concept of including an example and rules and actions all in one place. The model plus its docstring and field metadata cover format and rules, and the actions are in the Python functions that use the model.

**Integration note:** LangChain and Guardrails use Pydantic for output parsing, showing that combining Pydantic (validation) with LLM prompting can achieve a teach/validate/extract loop.

---

## Grammars and Executable Specifications

### Attribute Grammars and PEGs

**What they solve:** Parsing expression grammars (PEGs) and attribute grammars allow one to formally define the syntax of a language or data format. An attribute grammar extends a context-free grammar with attributes and semantic rules attached to grammar productions. These attributes can propagate information or perform computations as the parse tree is built, turning a purely declarative grammar into an executable specification.

**Teach/Validate/Extract:**
- **Validate** – Strong. A grammar will only parse strings that conform to the grammar, thus enforcing format.
- **Teach** – Weak. A plain grammar is a form of teaching a machine the language, but reading a formal grammar might be challenging for an LLM unless annotated.
- **Extract** – Strong. Attribute grammars can attach semantic actions that build output, compute values, or even produce target code as input is parsed. This means the spec is simultaneously validating syntax and executing semantics.

**Limitations:** Writing attribute grammars or PEGs is a specialized skill and can be quite verbose. They can become complex; ensuring that semantic rules don't have circular dependencies is non-trivial. A raw grammar is hard for humans to read as an example of the format. If used for generation, they can be too restrictive (the model might get stuck). If used for validation only, they often produce poor error messages.

**Key learning:** Attribute grammars demonstrate that it's possible to have a single artifact both describe and drive behavior, but with prohibitive complexity for most users.

---

### Behavior-Driven Development (Gherkin/Cucumber)

**What it solves:** BDD tools like Cucumber use a semi-structured natural language format (Gherkin syntax: "Given… When… Then…") to specify behavior examples. These scenarios read like plain English documentation of system behavior and are linked to code ("step definitions") that execute the described actions.

**Teach/Validate/Extract:**
- **Teach** – Strong. BDD specs are literally examples of system usage in readable form.
- **Validate** – Strong. They are run as tests; if the system's behavior deviates, the test fails.
- **Extract** – Strong. The link is through the step definition code that parses each step sentence and calls into the system.

**Limitations:** The BDD approach is domain-specific to testing and is less formal for data schemas. It's verbose (natural language) and the structure is not as compact as a single-line spec. A key failure mode is ambiguity – natural language steps can be misinterpreted.

**Key insight:** Mixing human-readable examples with machine-executable hooks is a proven concept, though in a different domain.

---

## LLM-Centric Structured Output Tools

### OpenAI Function Calling

**What it solves:** Function calling is a feature in the OpenAI API where the developer provides the model with a list of function signatures (name, description, and JSON-schema-like parameters for each function). The model can then output a JSON object indicating a function call with arguments. This allows a structured interface between the LLM and external tools.

**Teach/Validate/Extract:**
- **Teach** – Medium. The function schema guides the model via types, allowed values (enums), and descriptions for each field. While no concrete example is given, the model's training and the schema guide it to produce the correct format.
- **Validate** – Strong. The model's output is validated to be proper JSON and matches the schema. JSON mode ensures the output is valid.
- **Extract** – Strong. The model's structured output explicitly tells the application which function to call and with what data. This is essentially routing the content to a specific codepath.

**Limitations:** Function calling is narrower in scope, focused on JSON outputs for tool use. It doesn't allow arbitrary inline examples in the spec. The validation is primarily structural; semantic correctness still relies on the model's understanding. Also specific to certain model endpoints and has a token cost.

**Key insight:** OpenAI function calling is arguably the closest current technique to achieving a combined validate+execute spec for LLMs.

---

### Microsoft's Guidance Library

**What it solves:** Guidance is an open-source library that provides a programming model for templating LLM prompts and controlling the generation. You can write a prompt with special syntax to intermix constraints and model generation, ensuring that certain parts of the output match a regex or a type. Guidance can enforce structure by validating tokens as they stream and steering the model when it goes off course.

**Teach/Validate/Extract:**
- **Teach** – Strong. You often include an example or schema right in the prompt template, which is directly shown to the model.
- **Validate** – Strong. Guidance validates each generated token against constraints (regex, allowed set, type length, etc.) in real-time.
- **Extract** – Strong. The library allows you to directly extract the captured pieces because you set them in the template.

**Limitations:** Guidance is very powerful but requires the user to design a prompt program. The "spec" is not a static artifact; it's entwined with the prompting code. It's more like writing a small program to get structured output, rather than declaring a schema that is inherently understood by the model. Maintaining these templates for large schemas can become complicated.

**Key insight:** Guidance exemplifies executable spec – the spec literally executes as the prompt is processed.

---

### Outlines (Outlines.ai Library)

**What it solves:** Outlines is a library focused on structured LLM outputs. You specify the desired output format using Python type hints or Pydantic models, and it will ensure the LLM produces output of that shape. It supports constraints like `Literal["Yes","No"]` or giving a Pydantic `BaseModel` to have the model fill out a complex object.

**Teach/Validate/Extract:**
- **Teach** – Auto. The library injects appropriate guidance to the model based on the schema provided.
- **Validate** – Strong. Outlines guarantees the structure by constraining the decoding process using regex or grammars derived from the type spec.
- **Extract** – Strong. You end up with a validated Python object or an error if it didn't match.

**Limitations:** Like Guidance, the "spec" is embedded in code (Python types or Pydantic), not a standalone DSL. This is convenient for developer productivity but not ideal if you wanted a non-programmer to author the schema. Outlines currently supports types that can be expressed as Python type hints or simple regex.

**Key insight:** Outlines demonstrates that a schema-to-generation pipeline can be user-friendly, though the spec is code-driven rather than standalone.

---

### Guardrails (RAIL spec)

**What it solves:** Guardrails AI is an open-source framework specifically designed to validate and correct LLM outputs according to a schema or set of rules. It introduces the RAIL (Reliable AI Language) spec, often written in YAML or XML, where you define the expected output schema (JSON/XML), types, allowed values, and constraints like "this field should be a valid email" or "avoid profanity in this field". Guardrails monitors the LLM's output and, if it doesn't conform, it can automatically retry, ask the model to fix it, or apply fix-up rules.

**Teach/Validate/Extract:**
- **Teach** – Strong. Guardrails compiles the output schema into the prompt, prepending system messages that describe the output schema or providing examples.
- **Validate** – Strong. After generation, Guardrails uses the spec to check the model's output. It supports built-in validators (regex, length, JSON Schema types, even semantic checks) and can repair or retry on failure.
- **Extract** – Strong. Once the output passes validation, you have it parsed as a Python dict or Pydantic model.

**Limitations:** Guardrails is somewhat "heavyweight" in that you need to maintain a separate YAML spec file. This spec is quite close in spirit to the holographic concept – a single source of truth for output format and some semantic rules. However, the YAML syntax can be verbose, especially for nested JSON. It's primarily focused on after-the-fact validation and correction rather than token-level steering. Guardrails covers validate comprehensively and attaches an "operational intent" of sorts, but it doesn't inherently connect fields to arbitrary code actions beyond validation.

**Key insight:** Guardrails is the closest in the LLM domain to the holographic single-source ideal.

---

## Comparative Coverage: Teach vs Validate vs Extract

Summarizing the systems surveyed against the three goals:

| System | Teach | Validate | Extract |
|--------|-------|----------|---------|
| JSON Schema | Weak | Strong | None |
| OpenAPI | Medium | Strong | Partial |
| Protobuf/Avro | Weak | Strong | Compile-time |
| CUE | Strong | Strong | Partial |
| JSON-LD+SHACL | Semantic | Strong | Implicit |
| Zod | Weak | Strong | Code |
| Pydantic | Weak | Strong | Framework |
| Attribute Grammars | Weak | Strong | Strong |
| BDD/Gherkin | Strong | Strong | Strong |
| Function Calling | Medium | Strong | Strong |
| Guidance | Strong | Strong | Strong |
| Outlines | Auto | Strong | Strong |
| Guardrails | Strong | Strong | Strong |

**Key observation:** No single existing system achieves all three goals in a simple, unified way. The closest analogs are Guardrails, Outlines, CUE, and function calling – but each has its focus and assumptions.

---

## Novelty: What the Holographic Approach Brings

### The Gap

The holographic idea specifically emphasizes a single syntax that is simultaneously:
1. An **example** (showing the shape)
2. A **validation rule** (required, regex, etc.)
3. A **routing directive** (-> INDEXER)

This is a kind of literate, self-descriptive schema. Most existing solutions pick two of the three:
- JSON Schema + function calling covers validate + extract well but doesn't embed examples
- Guardrails covers teach + validate but stops short of automatic extract to multiple endpoints
- CUE covers teach + validate in a unified way, but not routing actions

### Self-Referential Design

The holographic idea leans towards a document that is **written in the format it defines**. This suggests a recursive, self-exemplifying structure. Not many schema languages do that – you wouldn't write a JSON Schema in JSON format to describe JSON Schema itself (though technically you could, it's just very meta). Here, the approach explicitly uses examples as part of the rule, not separate.

### LLM Legibility

Designing the spec language so that an AI can easily learn from it is a new angle. Traditional schemas prioritize machine validation or human developers, not AI comprehension. The holographic syntax is something an LLM can likely parse: it sees a key, an example in quotes, a tag like REQ, and an arrow indicating a destination. This mixes natural language with symbolic structure, more aligned with how LLMs have seen data in their corpus.

### Conclusion: Synthesis Over Invention

The novelty is in **synthesis**: combining proven ideas (examples in spec, formal constraints, runtime bindings) into one coherent language optimized for use with LLMs. This addresses a genuine gap – enabling high-level specs that both guide AI generation and drive program logic.

---

## Common Failure Modes: Lessons Learned

### Complexity vs. Expressiveness

Many attempts to unify specification and execution end up either too simplistic (can't express all needed logic) or too complex (essentially a programming language). Attribute grammars are powerful but not widely adopted because they require understanding of both parsing and programming. The lesson: aim for the 80% use-case and not the 100% if it complicates things.

### Spec Drift and Maintenance

One reason API specs and code often drift is that maintaining them in parallel is hard. A single-source spec would solve drift by being the truth for both validation and execution. However, if the spec is not directly usable (i.e., if one still has to write code to enforce parts of it), then you might end up updating one without the other.

### LLM Misinterpretation

While an LLM can be guided by a spec, it might misunderstand it if the spec is ambiguous or too terse. The spec needs to be written in a way that the LLM's likely interpretation aligns with the actual intent. This might mean including explanatory text or providing a meta-spec in the system prompt.

### Over-Reliance on Model Obedience

Systems like function calling and Guardrails show that models generally follow structural instructions, but not 100%. There are edge cases where the model produces something that technically fits the schema but is logically wrong. Therefore, even with a perfect spec, you need a validation process to catch deviations.

### Performance and Scalability

If the spec grows large, feeding that into the LLM prompt could consume excessive tokens. The system might need ways to selectively apply parts of the spec depending on context. A two-pass approach (generation, then validation) can help optimize this, which is what Guardrails does.

### User Adoption

If the holographic language is too similar to existing tools, developers might ask "Why not just use JSON Schema + conventions, or use CUE?" If it doesn't provide a clear benefit, it could be seen as reinventing the wheel. However, if it synthesizes the best of each and presents it coherently, it can fill a gap.

---

## Minimal Execution Layer Required

To make the holographic approach real, the smallest viable product would likely include:

### 1. **Parser**
- Read lines like `ID:: [ "sess_123" + REQ -> INDEXER ]`
- Understand the pieces: field name, example, constraint type, target
- Straightforward string parsing or simple PEG

### 2. **Validator**
- Convert the spec into validation rules
- Map REQ to "required field", REGEX to pattern check, ENUM to allowed set, etc.
- Could compile to JSON Schema for validation
- Leverage existing libraries (Pydantic, jsonschema, etc.)

### 3. **LLM Prompting Mechanism**
- Include the spec (or a derivative) in the system or few-shot prompt
- Tell the model "Follow this format"
- If the spec is self-exemplifying, the model can learn from it
- Optionally use function calling or constrained decoding (Guidance/Outlines)

### 4. **Routing Logic**
- Map target labels to actual handlers or endpoints
- After generating or receiving a document, dispatch fields to targets
- Could be a simple configuration: `INDEXER -> send_to_search_index()`
- Could be plugin-based for extensibility

### Architecture: Spec Compiler + Orchestrator

The minimal execution layer is a spec compiler that:
1. Parses the holographic spec
2. Generates prompts for the LLM (teach)
3. Creates validators (validate)
4. Produces routing configuration (extract)

This could even leverage existing components under the hood: translate to JSON Schema for validation, to OpenAI function calls for generation, etc.

---

## Conclusion: Meaningful Gap or Reinvented Wheel?

Given the survey, the holographic document language appears to be more of a **meaningful synthesis** of existing ideas than a wholesale reinvention. It's assembling pieces that have existed in isolation: the declarative rigor of schemas, the pedagogical value of examples, and the binding of spec to execution seen in some DSLs and modern LLM tooling.

**The gap:** No existing single system provides a one-stop solution that:
- A non-engineer could read to understand the format
- An LLM could reliably use to generate output
- A machine could execute against for routing logic

**The value:** If the holographic language integrates these seamlessly and is truly user-friendly, it addresses this gap. The integration is the novelty, not the individual components.

**Risk mitigation:** The holographic approach could even compile down to existing tech – generating JSON Schema for validation, a prompt snippet or OpenAI function spec for LLMs, and a routing config for execution. In that sense, it's not overthrowing prior art but standing on their shoulders.

**Summary:** The holographic document language is a synthesis that fills a genuine gap in LLM tooling – a single-source spec that guides AI generation and drives program logic. With careful design to avoid the pitfalls of others (complexity, drift, misinterpretation, poor scalability), it could provide significant value in the era of LLM-driven applications.
