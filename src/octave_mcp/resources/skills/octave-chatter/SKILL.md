---
name: octave-chatter
description: "OCTAVE on the wire — read and emit OCTAVE in agent-to-agent messages without authoring files. Syntax kernel, operator table, and the OCTAVE_WIRE primer v1.3 (provenance, hedges, verbatim IDs). For agents outside the workbench matrix."
allowed-tools: ["Read"]
triggers: ["octave chatter", "octave wire", "reply in octave", "octave message", "inter-agent message", "read octave", "answer in octave"]
version: "1.1.0"
---

===OCTAVE_CHATTER===
META:
  TYPE::SKILL
  VERSION::"1.1.0"
  STATUS::ACTIVE
  PURPOSE::"The chatter register — OCTAVE in message bodies, validated by the receiving model, never by octave_validate"
  AUDIENCE::"agents that read ∧ emit OCTAVE in conversation (anchor ceremonies, debate turns, cross-session messages) but never author .oct.md files"
  REQUIRES::[]
  RELATION::"octave-literacy §5 kernel ⊕ §2 operators, packaged standalone; file authoring → octave-literacy; tool receipts → octave-tool-reference"
  PRIMER::"OCTAVE_WIRE v1.3.0 — §4 below is its §1–§3 verbatim; canonical 554 tokens[cl100k_base] self-consistent; evidence base is v1.1 with 7 fewer rules; v1.3 UNTESTED until W3"
  KERNEL::"§5 = OCTAVE_WIRE FULL kernel, frozen 2026-09-05 — 138 tokens[cl100k_base, canonical]; the same string is stamped into workbench dispatch envelopes so hub kernel_only loads and dispatch never diverge; any edit re-opens its own count"
  PRIOR_ART::"octave-mcp thread 2026-01-30-octave-native-comms — RATIFIED across 3 models: a ~200-token primer enabled native OCTAVE output; an evidence point, not a ceiling — the 138-token kernel's SIZE is measured, its EFFICACY is untested until W3"
  KERNEL_SCOPE::"§5 covers the wire register only — file-syntax rules (no META on the wire → §1, no value on a §-header → §2, no chained ⇌ → §3) live in §1–§3 here and in octave-literacy §5; a kernel_only load of this skill gets wire rules, not file syntax, by design"
---
§1::REGISTER
  FORMAL::".oct.md files ∧ closing anchors → parsed by octave_validate → octave-literacy governs"
  WIRE::"message bodies → validated by the receiving model → this skill governs"
  SPLIT_RULE::"FORMAL ⇌ WIRE is decided by WHO VALIDATES, not by grammar — the syntax is the same"
  WIRE_DOES_NOT_NEED::[META_block, file_schema, canonicalisation, holographic_contracts, CANONICAL_SOURCE_paths]
  WHY_WIRE_EXISTS::"measured relay test on v1.1: 45 facts, 0 wrong, 1 lost — every loss was an IDENTIFIER. Syntax was never the failure. Provenance ∧ identifiers ∧ hedges are the value; compression is a side effect."
§2::SYNTAX_KERNEL
  // Same rules as octave-literacy §5 — restated so this skill loads alone
  ASSIGNMENT::"KEY::value — no spaces around ::"
  BLOCK::"KEY: then 2-space-indented children — for nested maps"
  LIST::"[a,b,c] — never YAML bullets"
  KEYS::"[A-Za-z_][A-Za-z0-9_]* — no bare numbers, no operator glyphs as keys"
  LITERALS::"true false null lowercase; numbers bare; quote anything with spaces, special chars, or §"
  SECTIONS::"§N::NAME opens a scope; a value on the header line is dropped"
  PROSE::"unkeyed sentences are not OCTAVE — key them or make them // comments"
  ENVELOPE::"===NAME=== … ===END=== optional on the wire; use it when the message must be quotable as a unit"
§3::OPERATORS
  // Reference table — which forms exist. The wire policy (when ASCII is legal, what the canonicaliser does) is §4b::ASCII.
  SYNTHESIS::"⊕ emergent whole — ASCII form: +"
  TENSION::"⇌ binary opposition, never chained — ASCII form: vs (word boundaries required)"
  FLOW::"→ causality ∨ sequence, right-associative — ASCII form: ->"
  CONSTRAINT::"∧ joint condition, inside brackets ∨ quoted values — ASCII form: &"
  ALT::"∨ alternative — ASCII form: the pipe character |"
  CONCAT::"⧺ mechanical join — ASCII form: ~"
  ANNOTATION::"NAME<facet> qualifies identity — HERMES<messenger>"
  CONSTRUCTOR::"NAME[args] parameterises — ENUM[a,b]"
  IN_VALUES::"inside a quoted value only operators carry relations — <> and [] there are opaque text, never validated: SISYPHEAN<endless re-explaining> in the primer is a gloss, who[role] is a slot; when a form must be checked by the parser, put it in a key"
§4::WIRE_PRIMER
  // OCTAVE_WIRE v1.3.0 §1–§3 verbatim (ASCII wire form preserved — the canonicaliser leaves quoted-value ASCII alone). Do not edit here; edit the primer and re-freeze.
  // Mythology = semantic zip, not decoration. HERMES = messenger. Meaning already in weights -> never literal, never a system name. First use in a thread carries its gloss, like this line.
  §4a::WHY
    LOSS::"prose across hops -> facts merge + provenance lost -> SISYPHEAN<endless re-explaining>"
    RISK::"structure without hedges -> ICARIAN<confident + wrong>"
  §4b::HOW
    RULE::"quote the phrase & drop stopwords & operators carry the connectives"
    BAD::"cause_is_fixture_flake_affecting_auth_and_payments_rather_than_runner"
    GOOD::"fixture flake -> auth + payments vs runner fault?" // ? = unverified; doubt lives here
    VERB::"verb lives in the key, never in the arrow" // e.g. RENAMED::old -> new ; -> is cause or sequence only
    TENSION::"vs = genuine opposition only -> a mismatch gets words: served 13 lines, actual 314"
    KEEP::"numbers & IDs & SHAs & roles & hedges & reasons -> copied verbatim, never paraphrased"
    SUM::"buckets total the whole -> 43 + 10 + 9 = 62"
    COMPRESS::"words vs claims"
    ASCII::"operators accept both forms: -> + vs & | on the wire; the canonicaliser normalises to unicode on write; vs needs word boundaries -> A vs B, never AvsB"
  §4c::SHAPE
    HEAD::"FROM::who[role]  PROVENANCE::measured@sha | relayed | inferred"
    STATE_FIELD::"every artifact says STATE::authored | installed | live"
    TAIL::"ASK::one question | STATUS::OK|BLOCKED|DONE|NEED_INPUT"
    ECHO::"a reply names UNCLEAR::[...] for what it could not resolve" // convention not rule; evidence 2 relay pairs, thin
    ASK::"reply in this register -> your SEA receipt is your first wire message"
§5::ANCHOR_KERNEL
TARGET::auditable_OCTAVE_messages_between_agents
NEVER::[
  paraphrase_an_id,
  verb_in_the_arrow,
  tension_for_mismatch,
  doubt_without_a_home,
  unkeyed_prose
]
MUST::[
  "HEAD FROM + PROVENANCE + STATE; TAIL one ASK | STATUS",
  "quote the phrase, drop stopwords, operators carry connectives",
  "numbers IDs SHAs roles hedges verbatim; ? marks unverified",
  "reply names UNCLEAR::[...]"
]
GATE::"Could the receiver act on this without asking what any ID or arrow meant?"
§6::EXAMPLE
  // A wire message — no META, no file schema, HEAD ∧ TAIL present, one hedge with a home
  MESSAGE:
    ```
    ===OCTAVE_WIRE===
    FROM::octave-secretary[align-octave-skills]
    PROVENANCE::"measured@fd67ef2 -> 3 octave_validate probes"
    STATE::authored
    FINDING::"literacy 21,163 chars & 51% non-syntax -> §6/§7/§8 reallocated"
    RISK::"stale ~/.claude/skills copy -> drift repeats without sync?" // operator-owned; unverified
    UNCLEAR::[which_profile_control_tower_loads_first]
    ASK::"confirm kernel_only for control-tower profiles"
    ===END===
    ```
===END===
