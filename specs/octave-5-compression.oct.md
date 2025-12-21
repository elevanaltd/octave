===OCTAVE_V5_COMPRESSION===
META:
  TYPE::      [ "PROTOCOL_DEFINITION" + CONST -> §META ]
  VERSION::   [ "1.0"                 + REQ   -> §META ]
  STATUS::    [ "DRAFT"               + REQ   -> §META ]
  NAME::      [ "OCTAVE v5 Compression Protocol" + OPT -> §META ]
  PURPOSE::   [ "Golden rules for lossless compression of prose into OCTAVE format" + OPT -> §META ]
  EXTENDS::   [ "octave-5.oct.md"     + REQ   -> §META ]

// =============================================================================
// OCTAVE v5 COMPRESSION: LOSSLESS TRANSFORMATION RULES
// "Compress everything around the anchors, never the anchors themselves."
// =============================================================================

POLICY:
  VERSION::        [ "1.0"   + REQ -> §SELF ]
  UNKNOWN_FIELDS:: [ "WARN"  + REQ -> §SELF ]
  RELATIONSHIP::   [ "Add-on to core DSL; defines compression semantics" + CONST -> §SELF ]

§1::COMPRESSION_CONTRACT
CONTRACT:
  MUST_PRESERVE::   [ [CONST_values, fenced_code_blocks, example_strings, quoted_canonical_text] + CONST -> §SELF ]
  MUST_INVARIANTS:: [ [SOLVES, TEACH, VALIDATE, EXTRACT, LIMITATION] + CONST -> §SELF ]
  MAY_COMPRESS::    [ [explanatory_prose, expanded_rationale, duplicate_phrasing] + CONST -> §SELF ]
  MUST_NOT::        [ "Introduce absolutes unless present in source" + CONST -> §SELF ]

VALIDATION_RULE:
  CONST_CHECK::  [ "CONST values must match source exactly (byte-for-byte or hash-match)" + CONST -> §SELF ]
  OPT_CHECK::    [ "OPT values may vary in phrasing while preserving semantic intent" + CONST -> §SELF ]

§2::ANCHOR_CATEGORIES
ANCHORS:
  DEFINITION:: [ "Immutable content that must be preserved verbatim during compression" + CONST -> §SELF ]

  CATEGORIES:
    CODE_BLOCKS::      [ "Fenced code, inline code, executable strings" + CONST -> §SELF ]
    EXAMPLE_STRINGS::  [ "Concrete values presented as canonical format" + CONST -> §SELF ]
    QUOTED_CANONICAL:: [ "Quoted text that defines behavior or format" + CONST -> §SELF ]
    API_KEYWORDS::     [ "Vocabulary (REQUIRED, -> INDEXER, JSON Schema, SHACL)" + CONST -> §SELF ]
    NUMBERS_ENUMS::    [ "Numeric values, scored matrices, enumerations" + CONST -> §SELF ]
    AXIS_DEFINITIONS:: [ "Framework definitions (TEACH/VALIDATE/EXTRACT)" + CONST -> §SELF ]

  RULE:: [ "If it's an example or executable-looking string, don't rewrite it—move it" + CONST -> §SELF ]

  EXAMPLES:
    PRESERVED::   [ "ID:: [ \"sess_123\" + REQUIRED -> INDEXER ]" + CONST -> §SELF ]
    PRESERVED::   [ "[WEAK, STRONG, NONE]" + CONST -> §SELF ]
    NOT_ANCHOR::  [ "This system provides validation capabilities" + OPT -> §SELF ]

§3::CLAIM_PRESERVATION
PROSE_COMPRESSION:
  PRINCIPLE:: [ "Compress prose by preserving claims, not sentences" + CONST -> §SELF ]

  PER_SYSTEM_KEEP:
    SOLVES::     [ "What problem the system addresses" + CONST -> §SELF ]
    TVE_RATING:: [ "Teach/Validate/Extract assessment" + CONST -> §SELF ]
    BREAKS::     [ "Where it fails relative to target ideal" + CONST -> §SELF ]
    NUANCE::     [ "One key caveat that prevents misclassification" + OPT -> §SELF ]

  DROP:
    EXTENDED_EXPOSITION::   [ "Multi-paragraph explanations" + OPT -> §SELF ]
    REPEATED_FRAMING::      [ "Restating the same point differently" + OPT -> §SELF ]
    SECONDARY_EXAMPLES::    [ "Additional examples after first canonical one" + OPT -> §SELF ]

§4::BOUNDARY_PRESERVATION
BOUNDARIES:
  PRINCIPLE:: [ "When original makes a distinction, keep it even if shortened" + CONST -> §SELF ]

  CRITICAL_DISTINCTIONS:
    VALIDITY_TYPES::      [ "structural _VERSUS_ semantic _VERSUS_ operational" + CONST -> §SELF ]
    ENFORCEMENT_MODES::   [ "constrained_decoding _VERSUS_ validate_repair_loops" + CONST -> §SELF ]
    BINDING_TIMES::       [ "compile_time _VERSUS_ runtime" + CONST -> §SELF ]

  FAILURE_MODE:: [ "Compression fails by collapsing boundaries that matter" + CONST -> §SELF ]

  EXAMPLE:
    ORIGINAL::   [ "Constrained decoding prevents errors during generation; validate-repair catches them after" + CONST -> §SELF ]
    CORRECT::    [ "Two modes: decoding-time prevention vs post-hoc repair" + CONST -> §SELF ]
    WRONG::      [ "Systems validate outputs" + OPT -> §SELF ]

§5::LANGUAGE_HEDGING
HEDGING_RULES:
  PRINCIPLE:: [ "Do not strengthen or weaken language beyond source" + CONST -> §SELF ]

  ABSOLUTES:
    RULE::     [ "MUST NOT introduce absolutes ('cannot', 'always', 'never') unless present in source" + CONST -> §SELF ]
    HEDGE::    [ "Use source hedging ('may', 'could', 'limited to', 'does not cover')" + CONST -> §SELF ]

  EXAMPLES:
    SOURCE::   [ "doesn't cover scenarios where you might want to produce a document" + CONST -> §SELF ]
    CORRECT::  [ "Does not cover scenarios where model produces documents" + CONST -> §SELF ]
    WRONG::    [ "Cannot produce documents" + OPT -> §SELF ]

  SEVERITY:
    SOURCE::   [ "One common challenge" + CONST -> §SELF ]
    CORRECT::  [ "Common challenge" + CONST -> §SELF ]
    WRONG::    [ "Most painful failure" + OPT -> §SELF ]

§6::CONST_OPT_SEMANTICS
CONSTRAINT_SEMANTICS:
  CONTEXT:: [ "CONST and OPT have additional meaning in compression context" + CONST -> §SELF ]

  CONST:
    CORE_MEANING::        [ "exact_match (from octave-5.oct.md)" + CONST -> §SELF ]
    COMPRESSION_MEANING:: [ "Immutable anchor; must match source exactly; validation enforces" + CONST -> §SELF ]
    USE_FOR::             [ [claims, ratings, definitions, examples, code, keywords] + CONST -> §SELF ]

  OPT:
    CORE_MEANING::        [ "optional (from octave-5.oct.md)" + CONST -> §SELF ]
    COMPRESSION_MEANING:: [ "Compressible; may vary in phrasing; preserves intent not words" + CONST -> §SELF ]
    USE_FOR::             [ [nuances, explanations, secondary_context, precedent_notes] + CONST -> §SELF ]

§7::FIELD_STRUCTURE
STANDARD_FIELDS:
  CONTEXT:: [ "Each system/concept in compressed doc should have consistent field structure" + CONST -> §SELF ]

  REQUIRED_FIELDS:
    SOLVES::     [ "What it addresses" + CONST -> §SELF ]
    TEACH::      [ "Format learning rating" + CONST -> §SELF ]
    VALIDATE::   [ "Constraint enforcement rating" + CONST -> §SELF ]
    EXTRACT::    [ "Routing/execution rating" + CONST -> §SELF ]
    LIMITATION:: [ "Where it breaks" + CONST -> §SELF ]

  OPTIONAL_FIELDS:
    NUANCE::        [ "Key caveat or boundary clarification" + OPT -> §SELF ]
    EXTENSIBILITY:: [ "How people attempt to extend beyond core" + OPT -> §SELF ]
    PRECEDENT::     [ "What this shows about the problem space" + OPT -> §SELF ]
    SCOPE_LIMIT::   [ "Explicit scope boundary" + OPT -> §SELF ]

§8::VALIDATION_PROTOCOL
VALIDATION:
  PURPOSE:: [ "How to verify compression is lossless" + CONST -> §SELF ]

  CHECKS:
    ANCHOR_EXACT::      [ "All CONST values byte-match source anchors" + CONST -> §SELF ]
    INVARIANTS_PRESENT::[ "Each system has SOLVES/TEACH/VALIDATE/EXTRACT/LIMITATION" + CONST -> §SELF ]
    BOUNDARIES_KEPT::   [ "Original distinctions preserved, not collapsed" + CONST -> §SELF ]
    NO_ABSOLUTES::      [ "No introduced absolutes; hedging matches source" + CONST -> §SELF ]
    RATINGS_MATCH::     [ "T/V/E ratings match original assessment" + CONST -> §SELF ]

  SEVERITY:
    ERROR::   [ "CONST value mismatch or missing invariant field" + CONST -> §SELF ]
    WARNING:: [ "Boundary collapsed or hedging changed" + CONST -> §SELF ]
    INFO::    [ "OPT field could be more concise" + CONST -> §SELF ]

§9::COMPRESSION_WORKFLOW
WORKFLOW:
  STEPS:: [ ["IDENTIFY_ANCHORS", "EXTRACT_CLAIMS", "MARK_BOUNDARIES", "COMPRESS_PROSE", "VALIDATE"] + CONST -> §SELF ]

  IDENTIFY_ANCHORS:
    ACTION:: [ "Scan source for code, examples, definitions, keywords, numbers" + CONST -> §SELF ]
    OUTPUT:: [ "List of verbatim strings to preserve" + CONST -> §SELF ]

  EXTRACT_CLAIMS:
    ACTION:: [ "For each system/section, identify SOLVES/TVE/LIMITATION" + CONST -> §SELF ]
    OUTPUT:: [ "Core claims in condensed form" + CONST -> §SELF ]

  MARK_BOUNDARIES:
    ACTION:: [ "Find distinctions that must be preserved (A vs B patterns)" + CONST -> §SELF ]
    OUTPUT:: [ "List of critical distinctions" + CONST -> §SELF ]

  COMPRESS_PROSE:
    ACTION:: [ "Reduce exposition while preserving claims and anchors" + CONST -> §SELF ]
    OUTPUT:: [ "OCTAVE-formatted document with CONST/OPT marking" + CONST -> §SELF ]

  VALIDATE:
    ACTION:: [ "Run validation checks per §8" + CONST -> §SELF ]
    OUTPUT:: [ "Pass/fail with specific violations" + CONST -> §SELF ]

§10::RELATIONSHIP_TO_CORE
MODULARITY:
  PRINCIPLE:: [ "This protocol extends but does not modify core octave-5.oct.md" + CONST -> §SELF ]

  CORE_UNCHANGED:
    SYNTAX::      [ "All core operators and patterns still apply" + CONST -> §SELF ]
    CONSTRAINTS:: [ "REQ/OPT/CONST/REGEX/ENUM/TYPE still defined by core" + CONST -> §SELF ]
    MECHANICS::   [ "Envelope, encoding, tokenization from core" + CONST -> §SELF ]

  THIS_ADDS:
    COMPRESSION_SEMANTICS:: [ "Additional meaning for CONST/OPT in compression context" + CONST -> §SELF ]
    ANCHOR_IDENTIFICATION:: [ "Rules for what must be preserved" + CONST -> §SELF ]
    VALIDATION_CONTRACT::   [ "Checks for lossless verification" + CONST -> §SELF ]

  SISTER_MODULES:
    octave-5-agents::   [ "Cognition binding, RAPH vectors, constitutional patterns" + OPT -> §SELF ]
    octave-5-sessions:: [ "Session context, extraction patterns, temporal state" + OPT -> §SELF ]
    octave-5-skills::   [ "Skill definitions, trigger patterns, tool restrictions" + OPT -> §SELF ]

===END===
