---
name: octave-literacy
description: "LLM-native structured communication format. Teaches OCTAVE syntax rules, canonical forms, and warning prevention for zero-error .oct.md authoring."
allowed-tools: ["Read", "Write", "Edit"]
triggers: ["octave format", "write octave", "octave syntax", "structured output", "OCTAVE basics", "OCTAVE literacy", "OCTAVE structure", "key::value", "OCTAVE notation", "llm communication", "token economy", "loss accounting"]
version: "4.0.0"
---

===OCTAVE_LITERACY===
META:
  TYPE::SKILL
  VERSION::"4.0.0"
  STATUS::ACTIVE
  PURPOSE::"Zero-error OCTAVE authoring — syntax rules, canonical forms, warning prevention, governance-artefact grammar"
  OCTAVE::"Olympian Common Text And Vocabulary Engine — loss accounting system for LLM communication"
  AUDIENCE::LLM<exclusively>
  SPEC_REFERENCE::octave-core-spec.oct.md
  NEXT_SKILLS::[octave-mastery,octave-compression]
  PATTERNS::[octave-tool-reference]
  COMPRESSION_TIER::CONSERVATIVE
  LOSS_PROFILE::"[preserve:syntax_rules∧examples∧governance_grammar,drop:tool_release_timeline→octave-tool-reference]"
---
§0::CONSUMPTION_DIRECTIVE
  // You are writing for LLM consumption only. No prose. No narrative. Every token carries payload.
  // Optimize for parsing efficiency and token density. Readability is irrelevant.
  MYTHOLOGY::"Use as compression — zero-shot, trust it. ATHENA<strategic_wisdom> = 1 token replacing 15."
  MYTHOLOGY_ANTI_PATTERN::"ZEUS::executive_decision — use EXECUTIVE::decision when literal is equally clear"
  // Full vocabulary: octave-mastery §1
§1::CORE_SYNTAX
  ASSIGNMENT::"KEY::value — double colon, no spaces around ::"
  BLOCK::"KEY: + newline + 2-space indent — use when value has nested children"
  CHOICE::"scalar value → ASSIGNMENT. nested children → BLOCK. Never mix."
  LIST::"[a,b,c] — square brackets, no YAML bullets ever"
  STRING::"bare_word if no spaces/special chars, else double-quoted"
  NUMBER::"42 or 3.14 or -1e10 — no quotes"
  BOOLEAN::"true or false — lowercase only"
  NULL_VALUE::"null — lowercase only"
  COMMENT::"// — line start or after value"
  §1b::BRACKET_FORMS
    CONTAINER::"[a,b,c] — bare brackets = list"
    ANNOTATION::"NAME<qualifier> — semantic facet on identity (ATHENA<strategic_wisdom>, LLM<exclusively>)"
    ANNOTATION_DISCIPLINE::"Annotations are SHORT qualifiers (1-3 words, ≤32 chars, identifier-only). Multi-word reasoning belongs in a sibling RATIONALE value as a quoted telegraphic phrase (see octave-mastery §7a)."
    ANNOTATION_WRONG::"I6<migration_on_moving_target_is_anti_pattern_for_zero_warnings>"
    ANNOTATION_RIGHT::"I6<production_grade_quality> + RATIONALE::\"Migration on moving target is anti-pattern for strict typing during data model changes.\""
    CONSTRUCTOR::"NAME[args] — structured arguments on identifier (REGEX[pattern], ENUM[a,b], JIT_GRAMMAR_COMPILATION[META→GBNF])"
    // These are SEPARATE forms. <> qualifies what something IS. [] parameterizes what something DOES.
    // ATHENA<strategic_wisdom> = annotation (identity facet). ENUM[a,b,c] = constructor (validation args).
    // Lenient parser canonicalizes []→<> ONLY for annotation-context uses. Genuine constructors keep [].
    // When in doubt: identity/archetype qualifier → <>. Parameterized operation/schema → [].
    INLINE_MAP::"[key::val, key2::val2] — dense key-value pairs, values must be atoms, no nesting"
  §1c::LITERAL_ZONES
    // Fenced code blocks pass through with ZERO processing
    SYNTAX::"KEY then newline then fence of 3+ backticks"
    RULES::[
      zero_processing_between_fences,
      tabs_allowed,
      NFC_bypass,
      info_tag_preserved
    ]
    USE_CASES::[
      embedded_code,
      teaching_examples,
      verbatim_content,
      OCTAVE_about_OCTAVE
    ]
    FENCE_SCALING::"use N+1 backticks to wrap content containing N-backtick fences"
  §1d::BLOCK_CANONICAL_FORMS
    // Three shapes agents reach for when nesting — only one is correct
    RULE::"Multi-field token (any key whose value is a map) → BLOCK form. Never inline-array root. Never flat prefix-scalars."
    THREE_SHAPES:
      ```
      ✓ BLOCK (canonical):         ✗ inline-array root:              ✗ flat prefix-scalars:
        PLATFORM:                    PLATFORM::[                        PLATFORM_TOKEN::HO-v1
          TOKEN::HO-v1                 TOKEN::HO-v1,                   PLATFORM_RUNTIME_FLOOR::"Node >=22"
          RUNTIME:                     RUNTIME::[FLOOR::"Node >=22"]]  PLATFORM_RUNTIME_BECAUSE::"…"
            FLOOR::"Node >=22"
            BECAUSE::"…"
      ```
    SCALAR_LIST_ONLY::"Inline arrays ([a,b,c]) are for scalar lists only — IMMUTABLES::[…], CONSOLIDATES::[a,b] — never for maps-of-maps"
    WHY_BLOCK::"Indented children inherit parent context → fewer key tokens, better LLM attention, zero W_DUPLICATE_KEY collisions"
    WHY_NOT_INLINE_ARRAY_ROOT::"Inline map as token root is non-canonical for map tokens even when values are atomic (§1b::INLINE_MAP). Triggers E_NESTED_INLINE_MAP as soon as any child value needs nesting — restructuring after the fact is mechanical waste. Use BLOCK form from the start."
    WHY_NOT_FLAT_PREFIX::"PARENT_CHILD1 + PARENT_CHILD2 key proliferation destroys hierarchical grouping and LLM attention"
§2::OPERATORS
  // Each operator encodes a relationship in a single token
  CONTAINER::"[] — List [a,b,c]"
  CONCAT::"⧺ — Mechanical join A⧺B | ASCII: ~"
  SYNTHESIS::"⊕ — Emergent whole A⊕B | ASCII: +"
  TENSION::"⇌ — Binary opposition A⇌B | ASCII: vs (requires word boundaries)"
  CONSTRAINT::"∧ — Inside brackets only [A∧B∧C] | ASCII: &"
  ALT::"∨ — Alternative A∨B | ASCII: |"
  FLOW::"→ — Right-associative A→B→C, often in lists [A→B→C] | ASCII: ->"
  SECTION_REF::"§ — target anchor e.g. §3c::ASSEMBLY_RULES"
  LINE_COMMENT::"// — line start or after value"
  ASCII_RULE::"All operators accept both unicode and ASCII. Always emit unicode in files; ASCII is acceptable on the wire (octave-chatter)."
  VS_RULE::"vs requires word boundaries: 'A vs B' valid, 'AvsB' invalid"
  TELEGRAPHIC_PHRASE::"see octave-compression §4::COMPRESSION_RULES R3a — operators carry the English connectives inside quoted values"
§3::CRITICAL_RULES
  R1::"No spaces around :: (KEY::value not KEY :: value)"
  R2::"Indent exactly 2 spaces per level — NO TABS"
  R3::"Keys must match [A-Za-z_][A-Za-z0-9_]* — start with letter or underscore"
  R4::"Envelopes: ===NAME=== open, ===END=== close (NAME must be [A-Z_][A-Z0-9_]*)"
  R5::"true, false, null — lowercase only (NOT True, False, NULL)"
  R6::"∧ only inside brackets: [A∧B∧C] valid, bare A∧B invalid"
  R6_CLARIFICATION::"Structural position: ∧ inside brackets only. Value position: operators inside quoted strings are valid telegraphic phrases — 'security ⇌ usability' not 'security at odds with usability' (see §2::TELEGRAPHIC_PHRASE, mastery §7a)"
  R7::"⇌ is binary only: A⇌B valid, chained A⇌B⇌C invalid"
  R8::"Values containing § must be quoted: \"see §3b\" not bare §3b"
  R9::"File extension .oct.md is canonical"
  R10::"Bare numeric keys trigger W_NUMERIC_KEY_DROPPED — use R1, STEP_1, not 1"
  R11::"Unkeyed prose sentences trigger W_BARE_LINE_DROPPED — comments (//) and list body lines are exempt"
  R12::"Section headers carry no value: §N::NAME then children on following lines. §N::NAME::\"value\" is parsed as a bare header — the value is silently dropped."
  R13::"KEY:: with nothing after it opens NO block — it becomes KEY::\"\\n\" and the indented lines below hoist into the enclosing scope, colliding with the next record's keys (W_DUPLICATE_KEY, last write wins). A block opener is KEY: with a single colon."
  §3b::V6_ENVELOPE_STRUCTURE
    FILE_STRUCTURE::"===NAME=== then META then optional --- separator then BODY then ===END==="
    SEPARATOR::"--- signals metadata boundary to discovery/indexing tools. Place after META block."
    META_REQUIRED::[TYPE,VERSION]
    META_COMMON_OPTIONAL::[
      STATUS,
      UPDATED,
      COMPRESSION_TIER,
      LOSS_PROFILE,
      CONTRACT,
      GRAMMAR
    ]
    // STATUS in META = document lifecycle (ACTIVE, DRAFT). STATUS in BODY = subject state. Both valid.
    COMPRESSION_TIER::ENUM[LOSSLESS,CONSERVATIVE,AGGRESSIVE,ULTRA]
    LOSS_PROFILE::"[preserve:causal_chains,drop:verbose_phrasing] — loss is explicit, never hidden"
    // NOTE: LOSS_PROFILE is spec-valid; older validators may not list it in allowed_meta — validator gap, not spec error
    CONTRACT::HOLOGRAPHIC<validation_law_in_document>
    GRAMMAR::GBNF_COMPILER<generate_constrained_output>
  §3c::ASSEMBLY_RULES
    RULE::"When concatenating profiles, omit intermediate ===END=== — only final one terminates"
    USE_CASES::[
      agent_context_injection,
      specification_layering,
      multi_part_documents
    ]
  §3d::SECTION_PATH_REFERENCES
    SYNTAX::"§N::NAME — section reference. §3b::V6_ENVELOPE_STRUCTURE is a valid cross-reference."
    QUOTING::"Quote § when used as content value: VALUE::\"see §3b\" not VALUE::§3b"
    NESTING::"§3b inside §3 — subsection. Prefix digit tracks depth."
§4::WARNING_PREVENTION
  // Parser-drop codes — each one is silent data loss at parse time.
  // Receipt inspection (corrections[] ∧ warnings[]), changes-mode semantics, remediation → octave-tool-reference.
  W_BARE_LINE_DROPPED::"Cause: line has no key:: prefix. Fix: add a key or use // comment."
  W_NUMERIC_KEY_DROPPED::"Cause: bare integer key (1::thing). Fix: use R1::thing or STEP_1::thing."
  W_DUPLICATE_KEY::"Cause: same key twice in one scope — last write wins. Fix: BLOCK form per §1d ∨ §7b. Frequent hidden cause: an empty KEY:: where KEY: was meant (R13) — STRICT still says VALIDATED; the loss shows only in repairs[]."
  W_UNQUOTED_SECTION_IN_VALUE::"Cause: bare § inside a value. Fix: quote per R8."
  W_INLINE_ARRAY_ROOT::"Cause: TOKEN::[KEY::v,…] map-as-inline-root. Fix: BLOCK form per §1d."
  W_FLAT_PREFIX_SCALAR::"Cause: PARENT_CHILD::v key-prefix flattening. Fix: BLOCK form per §1d."
  RECEIPTS::"octave_write ∧ octave_validate return corrections[] ⊕ warnings[] — empty warnings[] is NOT proof of no normalisation; read octave-tool-reference §3 before trusting a receipt"
§5::ANCHOR_KERNEL
TARGET::parser_valid_OCTAVE_read_and_author
NEVER::[spaces_around_double_colon,tabs,YAML_bullets,markdown_headings_in_envelope,bare_numeric_keys,unkeyed_prose_lines,nested_inline_maps,bare_section_ref_in_value,conjunction_outside_brackets,chained_tension,value_on_section_header]
MUST::[
  "scalar → KEY::value; nested map → KEY: + 2-space children; list → [a,b,c]",
  "keys match [A-Za-z_][A-Za-z0-9_]*; true false null lowercase; quote spaces ∧ special chars ∧ §",
  "envelope ===NAME=== → META[TYPE,VERSION] → --- → body → ===END===",
  "operators ⊕ ⇌ → ∧ ∨ emitted unicode; ∧ inside brackets only; ⇌ binary only",
  "<facet> qualifies identity; [args] parameterizes; neither inside a quoted value"
]
GATE::"octave_validate STRICT → errors:[] ∧ warnings:[] ∧ repairs:[]"
§6::WORKED_EXAMPLE
  // Shows: envelope, META with optional fields, separator, operators, annotation, loss accounting
  EXAMPLE:
    ```
===DECISION===
META:
  TYPE::DECISION
  VERSION::"1.0.0"
  COMPRESSION_TIER::CONSERVATIVE
  LOSS_PROFILE::"[preserve:causal_chains,drop:verbose_phrasing]"
---
STATUS::ACTIVE
CONTEXT::API_redesign[KAIROS<Q2_window>]
DECISION::microservice_extraction[auth⊕payments→independent_services]
PHASES:
  PLAN::[Research→Design]
  BUILD::[Code⊕Test]
METRICS:
  LATENCY::"<200ms p99"
  AVAILABILITY::"99.95%"
===END===
    ```
  // KAIROS<Q2_window> = annotation form. Semantic facet on identifier, not a list.
  // META carries COMPRESSION_TIER and LOSS_PROFILE — loss is auditable.
  // PHASES uses BLOCK because children are nested. STATUS uses ASSIGNMENT because scalar.
§7::GOVERNANCE_AUTHORING
  // UPOG (Universal Parse-Only Governance) — structural composition for governance artefacts
  // (North Stars, ADRs, RFCs, project-context docs, agent definitions). Composes on top of §2 R3a value-form
  // and §3 critical rules. Establishes parse-only validation as the gate, eliminating
  // per-doctype schema registration tax. Convention IS the schema, enforced by the strict
  // parser ⊕ this skill ⊕ octave-secretary write gate.
  §7a::ORGANIZING_PRINCIPLE
    MOTTO::"strict AST parse → gate. skill → schema. doctypes → zero registration tax."
    INSIGHT::"governance bodies → schema-exempt by declaration. META envelope → still validates."
    APPLIES_TO::[
      North_Star_Summary,
      Architectural_Decision_Record,
      Request_For_Comments,
      project_context_documents,
      agent_definitions,
      any_repeated_entity_governance_artefact
    ]
  §7b::BLOCK_FORM_FOR_REPEATED_ENTITIES
    // The structural anti-pattern that broke pre-UPOG governance docs:
    // I1::NAME::[PRINCIPLE::v, WHY::v, STATUS::v]
    // The chained ::NAME::[...] form reads as ASSIGNMENT under strict 1.13 lexer,
    // hoisting inner KV pairs to file-top-level. Across I1..IN, PRINCIPLE/WHY/STATUS
    // collide with W_DUPLICATE_KEY × 3N — last-write-wins data loss.
    PATTERN::"ID<LABEL>: + indented children"
    SYNTAX::"Block opener uses ID<LABEL>: form. NAME<facet> annotation (§1b; archetype usage in octave-mastery §3) carries the human-readable label. Indented children scope KEY tokens per-parent."
    EXAMPLE_FORBIDDEN::"I1::PERSISTENT_COGNITIVE_CONTINUITY::[PRINCIPLE::v,WHY::v,STATUS::v]"
    EXAMPLE_CANONICAL:
      ```
      §1::IMMUTABLES
        COUNT::6
        I1<PERSISTENT_COGNITIVE_CONTINUITY>:
          PRINCIPLE::"persist context⊕decisions⊕learnings → cross-session continuity"
          WHY::"amnesia → system failure [prevent re-learning cost]"
          STATUS::PENDING
          OWNER::implementation-lead
          GATE::B1
        I2<STRUCTURAL_INTEGRITY_PRIORITY>:
          PRINCIPLE::"correctness⊕compliance → precedence over velocity"
          ...
      ```
    GUARANTEE::"each I<N> block scopes children → ZERO W_DUPLICATE_KEY across the §"
    APPLIES_ALSO_TO::[
      assumptions<A1..AN>,
      ADR_records<ADR-NNNN>,
      RFC_records<RFC-NNN>,
      constrained_variables,
      any_homogeneous_repeated_record_block
    ]
  §7c::MARKDOWN_ERADICATION
    // Mixed markdown ## headings inside ===NAME=== envelopes fail E_TOKENIZE under
    // strict 1.13 lexer (the `(` in "## IMMUTABLES (6 Total)" trips the lexer).
    RULE::"governance .oct.md → ZERO markdown headings inside envelope"
    SCOPE::"applies to active governance artefacts. Generators (template files, /ns-summary-create skill, north-star-architect agent) that still emit legacy ## headings are Phase B follow-up — not retro-non-compliant, but MUST migrate before next governance amendment cycle."
    TRANSFORM:
      FROM::"^## (.*)$"
      TO::"§N::SECTION_NAME"
    EXAMPLE_BEFORE::"## IMMUTABLES (6 Total)"
    EXAMPLE_AFTER:
      ```
      §1::IMMUTABLES
        COUNT::6
      ```
    RATIONALE::"§N::NAME is structurally targetable. ## is text annotation lexer rejects."
  §7d::SCHEMA_EXEMPTION_VIA_CONTRACT
    // Declaratively scope schema validation to the META envelope; body fields are governed
    // by parse correctness, NOT by per-doctype schema registration. Eliminates the tax of
    // creating NORTH_STAR_SUMMARY / ADR / RFC schemas for every new artefact class.
    META_ANNOTATION::"CONTRACT::HOLOGRAPHIC<parse_only_governance>"
    SEMANTIC::"META → still validates against generic META schema. Body → parse-only governed. Body schema_validation_errors → non-load-bearing by declaration."
    PRECEDENT::"§3b META_COMMON_OPTIONAL already permits the HOLOGRAPHIC contract facet — we are using the existing hook, no spec change required."
    SUCCESS_CRITERION::"octave_validate STRICT → warnings:[] ⊕ errors:[] ⊕ repairs:[]"
  §7e::CANONICAL_AND_SOURCE_META
    // Path-tracking META fields enforced by canonical-paths pre-commit hook.
    CANONICAL::"runtime delivery path (e.g. .hestai/north-star/… or .hestai-sys/…)"
    SOURCE::"git-committed source path (e.g. src/<pkg>/_bundled_hub/… or repo-local)"
    RULE::"every governance .oct.md → META.CANONICAL ⊕ META.SOURCE required"
    PROJECT_LOCAL::"if file lives only in project tree → CANONICAL == SOURCE"
    BUNDLED_HUB::"source ≠ canonical → CANONICAL points to .hestai-sys/, SOURCE points to _bundled_hub/"
  §7f::VALUE_FORM_DELEGATION
    // Reasoning-field values (PRINCIPLE, WHY, RATIONALE, EVIDENCE, …) → octave-compression §4::COMPRESSION_RULES R3a.
    // Do NOT use snake_case_blobs in reasoning fields → triggers W_SNAKE_CASE_BLOB advisory
    // (see octave-tool-reference §6::SNAKE_CASE_BLOB, octave-mcp 1.13.0).
    SEE_COMPRESSION::"octave-compression §4::COMPRESSION_RULES R3a"
    SEE_TOOL_REFERENCE::"octave-tool-reference §6::SNAKE_CASE_BLOB"
    RULE::"quoted prose ∨ telegraphic operator form. NEVER bare snake_case_blob in reasoning fields."
  §7g::MIGRATION_CHECKLIST
    // Mechanical migration recipe — every legacy field preserved verbatim, only shape changes.
    STEP_1::"replace every ## Heading → §N::SECTION_NAME"
    STEP_2::"replace every I#::NAME::[KEY::v,…] → I#<NAME>:\\n  KEY::v indented children"
    STEP_3::"add META.CONTRACT::HOLOGRAPHIC<parse_only_governance>"
    STEP_4::"add META.CANONICAL ⊕ META.SOURCE"
    STEP_5::"telegraphic-compress reasoning values per R3a (operators carry connectives)"
    STEP_6::"octave_validate STRICT → confirm warnings:[] ⊕ errors:[] ⊕ repairs:[]"
    INVARIANT::"core structural field names preserved (PRINCIPLE, WHY, STATUS, INHERITS, IS, IS_NOT, GATES, LOAD_FULL_NORTH_STAR_IF, THE_OATH, …). Permitted semantic splits where the legacy form encoded multiple values in one slot: ASSUMPTIONS::N[note] → ASSUMPTIONS_COUNT::N ⊕ ASSUMPTIONS_NOTE::note. RELATED::[issues]∨[adrs] → RELATED_ISSUES::[…] ⊕ RELATED_ADRS::[…]. IF::trigger,THEN::[actions] → TRIGGER::trigger ⊕ ACTION::[actions] (within §::PROTECTION_CLAUSE block). Splits are mechanical and lossless — no semantic content dropped."
  §7h::ENFORCEMENT_LOCI
    // The convention is enforced at three structural points — drift in any one is detectable.
    LOCUS_1::"this skill — declares the pattern (vault delivery via _bundled_hub)"
    LOCUS_2::"octave-secretary agent — sole valid .oct.md write path, invokes octave_write (procedure: octave-tool-reference)"
    LOCUS_3::"octave-mcp 1.13 STRICT lexer — refuses non-compliant grammar at parse"
    DRIFT_DETECTION::"file hash on bundled-hub skill source ⊕ pre-commit OCTAVE validation"
===END===
