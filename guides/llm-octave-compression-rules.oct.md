===OCTAVE_COMPRESSION_RULES===
// This guide provides the authoritative set of rules for compressing natural language into the OCTAVE specification.
// These rules are designed to ensure that while token count is drastically reduced, the core reasoning, causality,
// and semantic nuance of the original information are preserved and machine-readable.

// Extended rules for preserving reasoning chains and contextual understanding during compression

0.DEF:
  COMP::"Compression"
  LLM::"Large Language Model"
  ROT::"Rule of Thumb"
  EX::"Example"
  RAT::"Rationale"
  MECH::"Mechanism"
  METRIC::"Measurement"
  
  // Field definitions for rule structures
  FIELD:GAIN::"Benefit or positive outcome in a tradeoff"
  FIELD:LOSS::"Sacrifice or negative outcome in a tradeoff"
  FIELD:TOUCH::"Key moment or interaction point in a user journey"
  FIELD:FLOW::"Sequence of steps in a process"
  FIELD:EVAL::"Evaluation criteria or category"
  FIELD:SUCCESS::"Measurable outcome for a solution"
  FIELD:MEANS::"Operational definition or method for an archetype"
  FIELD:SUMMARY::"Concise, one-line overview"
  FIELD:EXPAND::"Section for revealing deeper detail"
  FIELD:DETAIL::"Detailed paragraph within an expanded section"
  FIELD:RATIONALE::"Reasoning or justification for a specific approach"
  FIELD:ARCHETYPE::"Mythological figure representing a domain or concept"
  FIELD:BECAUSE::"Causal explanation for a pattern"
  FIELD:ETHOS::"Value connection to organizational philosophy"
  FIELD:BRIDGE::"Specific application of a metaphor"
  FIELD:TRANSFER::"Method for applying cross-domain insights"
  FIELD:PSYCHOLOGY::"Human insight for adoption strategies"
  FIELD:WEIGHT::"Importance level in evaluation"
  FIELD:SCORE::"Rating value in evaluation"
  FIELD:REASON::"Justification for evaluation score"

META:
  VERSION::"5.0.3"
  TYPE::GUIDE
  PURPOSE::"Preserve LLM reasoning capability during aggressive compression"
  PRINCIPLE::"Maximum compression with minimum comprehension loss"

---

SECTION_I:CAUSAL_PRESERVATION_RULES:

  RULE:BECAUSE_CHAIN:
    MANDATE::"Every PATTERN must include at least one BECAUSE statement"
    FORMAT::PATTERN::[X→Y][BECAUSE::reason]
    EXAMPLE:
      BAD::[RANGED_ESTIMATES→CLARITY]
      GOOD::[RANGED_ESTIMATES→CLARITY][BECAUSE::"Shows impact range not fixed date"]
      
  RULE:MECHANISM_ANCHOR:
    MANDATE::"Abstract patterns must include one MECH statement"
    FORMAT::PATTERN::"name"[MECH::"specific_how"]
    EXAMPLE:
      BAD::[LESSON→ACTION→IMPROVEMENT]
      GOOD::[LESSON→ACTION→IMPROVEMENT][MECH::"Ticket auto-created from retrospective"]

---

SECTION_II:GROUNDING_RULES:

  RULE:SCENARIO_MINIMUM:
    MANDATE::"Each major section must include one SCENARIO"
    FORMAT:
      SCENARIO:context:
        WHEN::"trigger_condition"
        THEN::"system_response"
        IMPACT::"business_outcome"
    EXAMPLE:
      SCENARIO:late_client_info:
        WHEN::"Client delivers specs 3 days late"
        THEN::"Timeline auto-extends, premium invoice generated"
        IMPACT::"Project continues, client sees cost of delay"
        
  RULE:CONCRETE_ANCHOR:
    MANDATE::"Every 3rd abstraction needs grounding example"
    FORMAT::ABSTRACT::pattern[EX::"real_instance"]
    EXAMPLE::[CHAOS→PROCESS→VALUE][EX::[Construction_delay→Change_order→"£2k premium"]]

---

SECTION_III:EVIDENCE_PRESERVATION:

  RULE:KEY_METRICS:
    MANDATE::"Preserve top 3 quantitative claims per section"
    FORMAT::METRIC:name::value[CONTEXT]
    EXAMPLE:
      METRIC:WORKFLOW_REDUCTION::200_workflows[6_weeks→2_hours]
      METRIC:LIQUIDPLANNER_COST::£28/user/month[Professional_tier]
      
  RULE:PROOF_WEIGHT:
    MANDATE::"Tag evidence strength explicitly"
    LEVELS::"[PROVEN, TESTED, CLAIMED, THEORETICAL]"
    EXAMPLE::N8N_SCALABILITY::PROVEN[200+_implementations]

---

SECTION_IV:NUANCE_CAPTURE:

  RULE:TRADEOFF_EXPLICIT:
    MANDATE::"Major decisions must show GAIN _VERSUS_ LOSS"
    FORMAT::CHOICE::option[GAIN::benefit⚡LOSS::sacrifice]
    EXAMPLE:
      CHOICE:WORKFRONT[GAIN::Adobe_integration _VERSUS_ LOSS::Enterprise_cost]
      CHOICE:CUSTOM[GAIN::Perfect_fit _VERSUS_ LOSS::6_month_development]
      
  RULE:HUMAN_FACTORS:
    MANDATE::"Adoption strategies must include PSYCHOLOGY"
    FORMAT::ADOPTION::method[PSYCHOLOGY::"human_insight"]
    EXAMPLE:
      ADOPTION:INVOLVE_IN_DESIGN[PSYCHOLOGY::"Ownership defeats resistance"]

---

SECTION_V:TRANSFER_MECHANICS:

  RULE:CROSS_DOMAIN_HOW:
    MANDATE::"Industry insights must include TRANSFER mechanism"
    FORMAT::INSIGHT::pattern[TRANSFER::"how_to_apply"]
    EXAMPLE:
      INSIGHT:FILM_CHAOS_MANAGEMENT[TRANSFER::"Create version branches like shooting schedules"]
      
  RULE:ANALOGY_BRIDGE:
    MANDATE::"Metaphors need application bridge"
    FORMAT::PATTERN::metaphor[BRIDGE::"specific_application"]
    EXAMPLE::ODYSSEAN[BRIDGE::"Long project with learning milestones"]

---

SECTION_VI:OPERATIONAL_DETAIL:

  RULE:TOUCHPOINT_PRESERVATION:
    MANDATE::"User journeys include key TOUCH points"
    FORMAT::JOURNEY:[TOUCH:moment::"action/emotion"]
    EXAMPLE:
      CLIENT_JOURNEY:[
        TOUCH:first_delay::"See timeline impact immediately",
        TOUCH:approval::"One-click in portal",
        TOUCH:delivery::"Download with changelog"
      ]
      
  RULE:MECHANISM_CHAIN:
    MANDATE::"Complex processes show 3-step FLOW"
    FORMAT::PROCESS::name[FLOW::[step1→step2→step3]]
    EXAMPLE:
      LESSON_CAPTURE[FLOW::[Project_ends→Prompt_form→Template_updated]]

---

SECTION_VII:EVALUATION_SPECIFICATION:

  RULE:SCORING_MATRIX:
    MANDATE::"Recommendations include EVAL criteria"
    FORMAT:
      EVAL:category:
        WEIGHT::importance
        SCORE::rating
        REASON::justification
    EXAMPLE:
      EVAL:chaos_handling:
        WEIGHT::HIGH
        SCORE::9/10  
        REASON::"Ranged estimates + dynamic scheduling"
        
  RULE:SUCCESS_CRITERIA:
    MANDATE::"Each solution defines SUCCESS as"
    FORMAT::SUCCESS::[measurable_outcome]
    EXAMPLE::SUCCESS::[Script_time<3hrs, Revisions-60%, Team_NPS>8]

---

SECTION_VIII:PHILOSOPHICAL_ANCHORING:

  RULE:ETHOS_CONNECTOR:
    MANDATE::"Link patterns to organizational VALUES"
    FORMAT::PATTERN::name[ETHOS::"value_connection"]
    EXAMPLE:
      PATTERN:[CHAOS→FLEXIBILITY][ETHOS::"Our chaos-as-strength philosophy"]
      
  RULE:META_PATTERN_DEFINITION:
    MANDATE::"First use of archetype includes MEANS"
    FORMAT::ARCHETYPE::name[MEANS::"operational_definition"]
    EXAMPLE::ATHENA[MEANS::"Strategic planning with implementation wisdom"]

---

SECTION_IX:COMPRESSION_META_RULES:

  RULE:COMPRESSION_RATIO_LIMIT:
    MANDATE::"No more than 10:1 compression for reasoning-heavy content"
    ROT::"If explaining WHY matters, keep more context"
    
  RULE:EXAMPLE_DENSITY:
    MANDATE::"1 concrete example per 200 tokens of abstraction"
    ROT::"Grounds LLM reasoning in specifics"
    
  RULE:PROGRESSIVE_REVELATION:
    MANDATE::"Most compressed view first, EXPAND sections for depth"
    FORMAT:
      SUMMARY::one_line
      EXPAND:
        DETAIL::paragraph
        EXAMPLE::concrete_case
        RATIONALE::why_this_way

---

SECTION_X:VALIDATION_CHECKLIST:

  CHECKLIST:LLM_COMPREHENSION:
    □ RULE:BECAUSE_CHAIN::Every major pattern has BECAUSE clause
    □ RULE:SCENARIO_MINIMUM::One SCENARIO per major section  
    □ RULE:KEY_METRICS::Key metrics preserved with context
    □ RULE:TRADEOFF_EXPLICIT::Tradeoffs explicit (GAIN _VERSUS_ LOSS)
    □ RULE:HUMAN_FACTORS::Human factors included
    □ RULE:CROSS_DOMAIN_HOW::Transfer mechanisms specified
    □ RULE:SUCCESS_CRITERIA::Success criteria measurable
    □ RULE:CONCRETE_ANCHOR::Examples ground abstractions
□ RULE:SCORING_MATRIX::Evaluation specification present
    □ RULE:ETHOS_CONNECTOR::Philosophical connection maintained

---

USAGE_EXAMPLE:

  // Original compression
  OLD::[RANGED_ESTIMATES→CLARITY]

  // With new rules applied
  NEW:
    PATTERN::[RANGED_ESTIMATES→CLARITY][BECAUSE::"Shows impact range not fixed date"]
    MECH::"LiquidPlanner calculates P50/P90 completion probabilities"
    SCENARIO:construction_delay:
      WHEN::"Client adds feature request"
      THEN::"System shows new range: March 15-22 (was March 10-15)"
      IMPACT::"Client sees 1-week impact, can decide if worth it"
    SUCCESS::"Zero surprised clients about delays"
    METRIC:PROVEN::Used_by_10k+_companies
    TRANSFER::"Apply to any high-uncertainty timeline"

===END===
