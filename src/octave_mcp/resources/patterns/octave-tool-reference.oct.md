===OCTAVE_TOOL_REFERENCE===
META:
  TYPE::PATTERN_DEFINITION
  VERSION::"1.1.9"
  STATUS::ACTIVE
  PURPOSE::"Procedural contract for octave_write and octave_validate — modes, receipts, changes-mode semantics, warning remediation. Sole agent-facing home for tool behaviour."
  VERIFIED_AGAINST::"octave-mcp 1.15.0"
  CANONICAL::".hestai-sys/library/patterns/octave-tool-reference.oct.md"
  SOURCE::"src/hestai_mcp/_bundled_hub/library/patterns/octave-tool-reference.oct.md"
  SINGLE_HOME::"tool-behaviour text lives here and nowhere else in the skill family; invocation-level parameter facts belong in the tool descriptions themselves"
  REVERIFY_TRIGGER::"octave-mcp minor version bump → re-check every §7 pointer before trusting this pattern"
§1::CORE_PRINCIPLE
ESSENTIAL::"A write is not done when the tool returns — it is done when the receipt has been read"
ANTI_PATTERN::"trusting_status_success<empty_warnings⊕unread_corrections→silent_data_loss_shipped_as_clean>"
ENFORCEMENT::"Every octave_write ∨ octave_validate call → inspect status ∧ errors ∧ validation_status ∧ corrections ∧ warnings ∧ repairs before claiming VALIDATED"
WRITE_GATE::"*.oct.md files are written by mcp__octave__octave_write only — never Write ∨ Edit — content decisions belong to the requesting agent"
§2::TOOL_SURFACE
TOOLS::[
  octave_validate,
  octave_write,
  octave_eject,
  octave_compile_grammar
]
NOT_A_TOOL::"octave_fmt — not registered in 1.15.0; do not call it"
OCTAVE_WRITE_MODES:
  CONTENT::"content= full payload → create ∨ overwrite; accepts raw OCTAVE ∨ one markdown-fenced block"
  CHANGES::"changes= delta map → mutate existing file (see §4)"
  NORMALIZE::"omit both → re-emit existing file in canonical form"
  EXCLUSIVITY::"content XOR changes — supplying both is an error"
PARAMETERS:
  SCHEMA::"schema=NAME → I5 validation; unknown name → available_schemas listed ∧ validation_status UNVALIDATED"
  FORMAT_STYLE::"omitted → full canonical re-emit (today's default); preserve → span-aware, clean nodes byte-sliced from baseline; expanded → inline maps lifted to BLOCK; compact → atom-only blocks collapsed; explicit null → DeprecationWarning (default flips to preserve in a later release)"
  DRY_RUN::"dry_run=true ∨ corrections_only=true → receipt without disk write — use before any destructive changes-mode call"
  BASE_HASH::"base_hash=sha256 → compare-and-swap; mismatch → E_HASH, nothing written"
  LENIENT::"lenient=true → deterministic repairs ∧ salvage policy; default strict rejects on parse error"
OCTAVE_VALIDATE::"content= XOR file_path=; profile STRICT ∨ STANDARD ∨ LENIENT ∨ ULTRA; schema required; compact=true → counts only; diff_only=true → diff not canonical body"
FILE_PATH_WHITELIST::"file_path= accepts .md ∨ .oct.md ∨ .octave only — anything else → E_PATH; content= has no extension constraint"
§3::RECEIPT_GATES
RESULT_FIELDS::[
  status,
  errors,
  validation_status,
  validation_errors,
  corrections,
  warnings,
  repairs,
  repair_log,
  diff,
  canonical_hash,
  schema_name,
  available_schemas,
  zone_report,
  literal_zone_repair_log
]
STATUS::"success ⇌ error — error carries errors[] with code (E_PARSE, E_HASH, E_UNRESOLVABLE_PATH, E_OP_TARGET_MISMATCH, …) ∧ nothing is written"
VALIDATION_STATUS::"VALIDATED ∨ UNVALIDATED (no ∨ unknown schema) ∨ INVALID (schema violations in validation_errors[])"
CORRECTIONS::"every normalisation ∧ repair the pipeline applied — entries carry rule_id ∧ before ∧ after ∧ safe ∧ semantics_changed ∧ tier (NORMALIZATION ∨ REPAIR ∨ LENIENT_PARSE)"
WARNINGS::"the subset of corrections[] with safe:false — data-affecting only; a benign normalisation never appears here"
REPAIRS::"octave_validate ∧ lenient writes: schema repairs suggested (fix=false) ∨ applied (fix=true); repair_log is the per-repair audit trail that accompanies it — both [] on a clean artefact; read them alongside corrections[]"
EMPTY_WARNINGS_RULE::"warnings:[] ≠ untouched — read corrections[] to learn what changed; only corrections:[] ∧ warnings:[] ∧ repairs:[] together mean the bytes were already canonical"
TRIAGE:
  DISCARDING::"content lost ∨ corrupted — W_BARE_LINE_DROPPED ∨ W_NUMERIC_KEY_DROPPED ∨ W_DUPLICATE_KEY ∨ W_UNQUOTED_SECTION_IN_VALUE ∨ W_LENIENT_MULTI_WORD_COALESCE (unquoted multi-word value silently joined) ∨ W_BARE_FLOW (flow arrow outside brackets, legacy form) → fix the source and rewrite. Hidden cause of W_DUPLICATE_KEY: an empty KEY:: where KEY: was meant opens no block, its children hoist into the parent scope and collide with the next record (literacy R13) — STRICT reports VALIDATED and warnings:[]; only repairs[] shows it"
  ADVISORY::"form debt, non-blocking — W_ANNOTATION_TOO_LONG ∨ W_SNAKE_CASE_BLOB → §6 value remediation; W_INLINE_ARRAY_ROOT ∨ W_FLAT_PREFIX_SCALAR ∨ W_CONSTRUCTOR_MISUSE → §6 STRUCTURAL_ADVISORY; each fires independently; all JIT, only when already amending the record"
  BENIGN::"tier NORMALIZATION ∧ safe:true — whitespace, blank lines, identifier dequoting, TN_INLINE_MAP_TO_BLOCK → no action"
ALIAS::"octave_validate repairs[] entries carry type ∧ subtype; map to TRIAGE by subtype — DISCARDING (content lost ∨ corrupted, measured): duplicate_key ∨ bare_line_dropped ∨ numeric_key_dropped ∨ multi_word_coalesce (unquoted multi-word value silently joined — the parser records original vs result because the bytes diverge semantically) ∨ bare_flow (type spec_violation: flow arrow outside brackets, the legacy form UPOG migration exists to eradicate); REPAIR-tier form changes (1.15.0 lenient_parse set: wrong_case, pattern_autoquote, unquoted_timestamp, curly_brace_annotation, constraint_outside_brackets, chained_tension, nested_inline_map, deep_nesting, constructor_misuse, source_compile_value, unclosed_list, boundary_missing) → BENIGN by construction at a mechanical gate (form changes, content preserved); an authoring agent additionally reads before/after and fixes the source when meaning shifted; type normalization → BENIGN; other type spec_violation subtypes → surface in validation_errors[], not triage; UNMAPPED subtype → depends on call site: authoring/write call sites treat it as DISCARDING (fail closed — retry is cheap, nothing is destroyed); gate call sites operating under a retry cap (ceremony FLUKES, dispatch egress) record it in the gate verdict as UNKNOWN_SUBTYPES (implementations may alias the field) and HOLD — no pass, no void, no retry consumed; the ACCEPTOR is the operator in the gated agent's own session (a peer relay is never acceptance, per PEER_AUTHORITY); the hold is BOUNDED by the implementation's timeout and on expiry degrades to the named terminal outcome HELD: the artefact is not activated, the binding is not voided, the retry budget is untouched, and HELD is surfaced to the dispatching side as STATUS::NEED_INPUT carrying UNKNOWN_SUBTYPES — never auto-accept, never silently stall; an upstream version adding a benign subtype must not void bindings fleet-wide. Write-side equivalents: duplicate_key⇌W_DUPLICATE_KEY, bare_line_dropped⇌W_BARE_LINE_DROPPED, numeric_key_dropped⇌W_NUMERIC_KEY_DROPPED, multi_word_coalesce⇌W_LENIENT_MULTI_WORD_COALESCE"
SCOPE_NOTE::"column-0 keys under a §N header are file-top-level — TARGET ∧ NEVER ∧ MUST ∧ GATE of a kernel must be unique in the file or W_DUPLICATE_KEY drops the earlier one"
NOOP_INVARIANT::"content identical to target bytes → true no-op: no normalisation, corrections:[] (octave-mcp 1.12.0, #407)"
RECEIPT_GATE::"status:success ∧ errors:[] ∧ validation_status ≠ INVALID ∧ warnings:[] ∧ every corrections[] entry AND every repairs[] entry triaged per §3::TRIAGE (repairs[] subtypes mapped by §3::ALIAS) as BENIGN ∨ consciously accepted — a DISCARDING entry on either side fails the gate even when validation_status says VALIDATED; an unmapped subtype fails the gate when authoring and HOLDS it at retry-capped gates (UNKNOWN_SUBTYPES; no pass, no void, no retry consumed) pending operator acceptance in-session, degrading on bounded timeout to HELD → NEED_INPUT, never to PASS and never to VOID"
§4::CHANGES_MODE
  // octave-mcp 1.15.0 STRATEGY_S3 — HARD BREAK from earlier releases
PATHS::"top-level KEY; META.FIELD; PARENT.CHILD into a top-level Block; §N.KEY ∨ §N::NAME.KEY into a Section — single child key only; a §-section itself is not a MERGE target; deeper paths → content= rewrite"
BARE_DICT_AT_KEY::"changes={PARENT: {CHILD: x}} against an existing block = FULL REPLACE — unmentioned children are DROPPED"
PRESERVE_SIBLINGS::"to add ∨ change one child and keep the rest → {PARENT: {$op: MERGE, value: {CHILD: x}}}"
NESTED_DICTS::"bare dict with nested dict values → synthesised as canonical BLOCK form (logged TN_INLINE_MAP_TO_BLOCK); flat dict → inline map; the old dict→InlineMap coercion that re-parsed to E_NESTED_INLINE_MAP is gone"
MERGE_GUARD::"nested dict inside a $op:MERGE payload → E_NESTED_DICT_IN_MERGE_PAYLOAD; scalar over an existing child block via MERGE → E_OP_TARGET_MISMATCH — DELETE first ∨ send a bare-dict REPLACE at the parent"
SCALAR_OVER_BLOCK::"bare scalar at a KEY holding a block → replaces the block with one flat assignment; never emits duplicate keys"
NO_AUTO_CREATE::"changes cannot add a key at a path that does not exist → E_UNRESOLVABLE_PATH; new keys need content= rewrite ∨ MERGE into an existing block parent"
OPS::[
  "{$op: DELETE} → remove target",
  "{$op: APPEND, value: x} → push onto array (nested list ∨ dict items re-emitted as parseable OCTAVE)",
  "{$op: PREPEND, value: x} → unshift onto array",
  "{$op: MERGE, value: {…}} → deep-merge into block, unmentioned children kept; inner $op:DELETE removes"
]
ERRORS::"E_UNRESOLVABLE_PATH → path absent ∨ section-as-target, no auto-create; E_INVALID_OP_DESCRIPTOR → malformed $op; E_AMBIGUOUS_PATH ∨ W_AMBIGUOUS_PATH → anchor the path with §N"
LITERAL_ZONES::"a changes value replacing a fenced child keeps fence form ∧ info tag under format_style=preserve — content-only edits round-trip byte-identical"
RULE_OF_THUMB::"scalar-array appends ∧ single-key edits → changes mode; anything block-nested ∨ structural ∨ a new key → content= with format_style=preserve after a dry_run"
§5::ANCHOR_KERNEL
TARGET::verified_OCTAVE_writes_with_read_receipts
NEVER::[
  write_oct_md_with_Write_or_Edit,
  claim_VALIDATED_without_receipt,
  trust_empty_warnings_alone,
  bare_dict_replace_when_siblings_must_survive,
  call_octave_fmt,
  remediate_frozen_archives
]
MUST::[
  "octave_write only; schema= when one applies; dry_run before destructive changes",
  "read status ∧ errors ∧ validation_status ∧ corrections ∧ warnings ∧ repairs — triage DISCARDING ∨ ADVISORY ∨ BENIGN",
  "changes mode: MERGE to keep siblings; bare dict = FULL REPLACE; nested ∨ new key → content= preserve",
  "advisory warnings → remediate JIT per §6, only on the record already being amended"
]
GATE::"Did I read the receipt, and can I name every correction and every repair the tool applied?"
§6::REMEDIATION
  // JIT policy — remediate only when already amending the record that surfaced the warning
ANNOTATION_MIGRATION:
  POLICY::"JIT — refactor long annotations only when you are already amending that record"
  TRIGGER::"Any record amendment where the record contains annotations exceeding 32 chars OR 4 underscore-tokens (W_ANNOTATION_TOO_LONG in octave_write corrections[])"
  ACTION::["Replace long annotation qualifier with a short qualifier (≤32 chars, ≤4 underscore-tokens)","Add a sibling RATIONALE (or PRINCIPLE, GUIDANCE) field with the full reasoning as a quoted telegraphic phrase"]
  EXAMPLE_BEFORE::I6<migration_on_moving_target_is_anti_pattern_for_zero_warnings>
  EXAMPLE_AFTER::"I6<production_grade_quality> + RATIONALE::\"migration ⇌ moving target → strict typing anti-pattern\""
  FROZEN_ARCHIVES::"Archives (DECISIONS-ARCHIVE, docs/research/, benchmark docs) stay frozen — zero ROI to batch-rewrite historical records"
  DETECTION::"W_ANNOTATION_TOO_LONG in octave_write corrections[] is non-blocking and advisory only"
SNAKE_CASE_BLOB:
  POLICY::"JIT — rewrite snake-fragmented prose only when amending a record whose corrections[] surfaces W_SNAKE_CASE_BLOB"
  TRIGGER::"Any record amendment where octave_validate or octave_write returns W_SNAKE_CASE_BLOB in corrections[] for a value or list-element in a reasoning-field position (octave-mcp 1.13.0 advisory)"
  DETECTOR::"W_SNAKE_CASE_BLOB (octave-mcp:src/octave_mcp/mcp/write_detection.py) — mechanical triggers: length>40 chars + ≥4 underscores (bulk) OR ≥2 stopwords across underscore-delimited tokens (semantic); ALL-CAPS ≤16-char tokens excluded"
  REASONING_FIELDS::[
    DECISION,
    BECAUSE,
    RATIONALE,
    RETAINS,
    GUIDANCE,
    WHY,
    NOTE,
    PRINCIPLE,
    ESCAPE_HATCH,
    CONTEXT,
    EVIDENCE,
    OBSERVATION,
    FINDING,
    CONSEQUENCES,
    TRADEOFFS,
    NEXT_STEPS,
    CAVEAT,
    ASSUMPTION
  ]
  ACTION::[
    "Rewrite the offending snake-case value as a TELEGRAPHIC_PHRASE per octave-compression §4::COMPRESSION_RULES R3a",
    "Quoted value, stopwords dropped, operators ⊕ ⇌ ∧ ∨ → carry English connectives",
    "ATOMS belong in structural positions (keys, enum values), not reasoning-field values"
  ]
  EXAMPLE_BEFORE::"BECAUSE::migration_on_moving_target_is_anti_pattern_for_zero_warnings_during_strict_typing"
  EXAMPLE_AFTER::"BECAUSE::\"migration ⇌ moving target → strict typing anti-pattern\""
  DETECTION::"W_SNAKE_CASE_BLOB in octave_write corrections[] is non-blocking and advisory only"
STRUCTURAL_ADVISORY:
  POLICY::"JIT — reshape only the block being amended; never batch-restructure a file for shape warnings alone"
  W_INLINE_ARRAY_ROOT::"TOKEN::[KEY::v,…] map-as-inline-root → BLOCK form per octave-literacy §1d (TOKEN: + indented children)"
  W_FLAT_PREFIX_SCALAR::"PARENT_CHILD::v siblings → group under PARENT: block per octave-literacy §1d — EXCEPT named-sequence families the skills mandate (R1…Rn, STEP_1…, P1…, W_* code tables); those are accepted advisories, leave them"
  W_CONSTRUCTOR_MISUSE::"a known constructor name (REGEX, PATTERN, ENUM…) used as an assignment key → either the constructor form NAME[args] or a different key; agent GRAMMAR blocks (REGEX::\"^\\[X\\]\") are a known accepted case"
  DETECTION::"all three are STRUCTURAL_CHECK tier, safe:true — never data loss"
§7::PROVENANCE
  // Every behavioural claim above points at the 1.15.0 source it was read from. Re-verify on version bump.
P1::"tool registry [validate, write, eject, compile_grammar], no octave_fmt → octave-mcp src/octave_mcp/mcp/server.py tool table"
P2::"content XOR changes XOR normalize → src/octave_mcp/mcp/write.py module docstring"
P3::"omitted format_style = full canonical re-emit; preserve ∧ expanded ∧ compact → src/octave_mcp/mcp/write_format.py header comment ∧ FORMAT_STYLE_VALUES; explicit None deprecated → CHANGELOG 1.13.0"
P4::"warnings[] = corrections with safe:false → src/octave_mcp/mcp/write.py result[warnings] comprehension (drain block)"
P5::"corrections[] drained from TIER_NORMALIZATION log; entry shape rule_id ∧ before ∧ after ∧ safe ∧ semantics_changed → src/octave_mcp/core/grammar/tier_normalize.py log_repair"
P6::"no-op invariant on identical bytes → CHANGELOG 1.12.0 (#407, labelled SR1-T4 there)"
P7::"changes-mode hard break: bare-dict FULL REPLACE, MERGE preserves, nested dict → BLOCK, MERGE guards, APPEND re-parseable → CHANGELOG 1.15.0 STRATEGY_S3 (#443, #440, #488, #484)"
P8::"literal-zone fence preservation under changes → CHANGELOG 1.14.0 (#460)"
P9::"W_SNAKE_CASE_BLOB detector → src/octave_mcp/mcp/write_detection.py _detect_snake_case_blob"
P10::"column-0 keys under § are top-level (W_DUPLICATE_KEY on a second kernel GATE) → observed on this pattern's own first write, octave-mcp 1.15.0"
P11::"§-section is not a MERGE target ∧ changes cannot create a key (E_UNRESOLVABLE_PATH: single child key only) → observed adding ALIAS to this pattern, octave-mcp 1.15.0"
P12::"repairs[] ∧ repair_log[] fields on every octave_validate receipt (both [] on clean input) ∧ file_path extension whitelist (.md .oct.md .octave, E_PATH on .txt) → observed on octave_validate receipts this session, octave-mcp 1.15.0"
§8::USED_BY
AGENTS::[octave-secretary,octave-specialist]
KERNEL_ONLY::"any agent that calls octave_write directly — north-star-architect, system-steward, agent-expert, skills-expert"
CONTEXT::document_authoring⊕context_maintenance⊕governance_artefact_amendment
===END===
