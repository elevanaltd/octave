===OCTAVE_COMPRESSION_PRIMER===
META:
  TYPE::PRIMER
  VERSION::"6.5.0"
  TOKENS::"~300"
  COMPRESSION_TIER::ULTRA
  LOSS_PROFILE::"[preserve:tier_rules∧transforms,drop:rationale]"
§1::ESSENCE
PURPOSE::"Compress prose→OCTAVE with tier judgment"
OCTAVE::"Olympian Common Text And Vocabulary Engine — Semantic DSL for LLMs"
METHOD::"READ→SELECT_TIER→EXTRACT[why,evidence]→COMPRESS→VALIDATE"
TELEGRAPHIC_PHRASE::"quoted value, stopwords dropped, operators carry English connectives — e.g. 'security ⇌ usability' not 'security at odds with usability'"
§2::MAP
TIER_SELECTION::
```
audit∨critical→LOSSLESS[drop::none]
research∨design→CONSERVATIVE[drop::redundancy]
quick_ref→AGGRESSIVE[drop::nuance]
extreme_scarcity→ULTRA[drop::narrative]
identity∨binding→ULTRA_MYTHIC[drop::narrative,keep::soul∧constraints]
```
TRANSFORMS::
```
content→PRESERVE[causality[X→Y_because_Z]∧numbers∧IDs∧§_names]
noise→DROP[stopwords∧redundancy∧prose_connectors]
sentences→KEY::value
repetition→[array]
because∨therefore→A→B[reason]
tradeoffs→GAIN⇌LOSS
groupings→parent::[children]
```
§3::SYNTAX
OPERATORS::
```
::    assign (no spaces around)
→     flow / sequence
⊕     synthesis / combine
⇌     tension / opposition
∧     conjunction / all-required
∨     disjunction / alternative
[,]   list
```
§4::ONE_SHOT
IN::"Users authenticate before dashboard. Failed logins trigger alerts for security while maintaining usability."
OUT::"AUTH::login→validate→dashboard,FAIL::alert,INTENT::security⇌usability"
§5::VALIDATE
MUST::[
  valid_OCTAVE,
  "preserve_§_names_verbatim",
  preserve_numbers,
  preserve_IDs,
  preserve_causality,
  tier_selected_before_compress,
  no_markdown,
  no_JSON,
  no_YAML,
  "nesting<=3"
]
===END===
