===OCTAVE_MASTERY===
// Expert-level OCTAVE application, focusing on advanced composition, validation, and strategic use.
// This skill is self-contained and does not require external file access.

ESSENCE:
  ARCHETYPE::HEPHAESTUS+ATHENA // The master craftsman and strategist
  PRIME_DIRECTIVE::"Apply the full OCTAVE standard with expert precision, using these advanced rules to supplement the foundational literacy provided by OCTAVE_LITERACY_PATTERNS."
  FOCUS::"Advanced syntax, full semantic vocabulary, and structural integrity."

---

ADVANCED_SYNTAX:
  DESCRIPTION::"Rules beyond the basics, for robust and precise document construction."

  DATA_TYPES_MASTERCLASS:
    EMPTY_STRING::"\"\"" // Must be quoted
    MULTILINE_STRING::"""...""" // Indentation preserved relative to opening """
    TYPE_DISAMBIGUATION:
      STRING_42::"\"42\""
      NUMBER_42::42
      STRING_TRUE::"\"true\""
      BOOLEAN_TRUE::true
    INLINE_OBJECT:
      FORMAT::{{key:value, key2:value2}} // Note single colon inside
      NO_NESTED_OBJECTS::true
      ALLOWED_VALUES::[strings, numbers, booleans, lists]

  KEY_NAMING_RULES:
    ALLOWED_START::[A-Z, a-z, _]
    ALLOWED_CHARS::[A-Z, a-z, 0-9, _]
    FORBIDDEN_CHARS::[":", "-", " "]
    CASE_SENSITIVE::true

  STRUCTURE_NUANCES:
    EMPTY_SECTION::"A KEY: with no children is a valid empty object."
    OPERATOR_CHAINING:
      INVALID::"A+B+C" // Synthesis and Tension are binary only
      VALID::"[A->B->C]" // Progression can be chained in lists

---

SEMANTIC_PANTHEON:
  DESCRIPTION::"The complete, validated vocabulary for semantic compression."

  DOMAINS: // Fundamental Areas of Concern
    ZEUS::"Executive function, authority, strategic direction, final arbitration"
    ATHENA::"Strategic wisdom, planning, elegant solutions, deliberate action"
    APOLLO::"Analytics, data, insight, clarity, prediction, revealing truth"
    HERMES::"Communication, translation, APIs, networking, messaging, speed"
    HEPHAESTUS::"Infrastructure, tooling, engineering, automation, system architecture"
    ARES::"Security, defense, stress testing, conflict simulation, adversarial analysis"
    ARTEMIS::"Monitoring, observation, logging, alerting, precision targeting of issues"
    POSEIDON::"Data lakes, storage, databases, unstructured data pools"
    DEMETER::"Resource allocation, budgeting, system growth, scaling"
    DIONYSUS::"User experience, engagement, creativity, chaotic innovation"

  PATTERNS: // Recurring Narrative Dynamics
    ODYSSEAN::"A long, difficult, but ultimately transformative journey with a clear goal"
    SISYPHEAN::"A repetitive, difficult, and seemingly endless task (e.g., tech debt)"
    PROMETHEAN::"A breakthrough innovation that challenges the existing order"
    ICARIAN::"A pattern of overreach due to early success, leading to catastrophic failure"
    PANDORAN::"An action that unleashes a cascade of unforeseen and complex problems"
    TROJAN::"A strategy involving a hidden payload or element that changes the system from within"
    GORDIAN::"A direct, unconventional, and decisive solution to a seemingly impossible problem"
    ACHILLEAN::"A single, critical point of failure in an otherwise robust system"
    PHOENICIAN::"A pattern of necessary destruction and rebirth (e.g., refactoring, deprecation)"
    ORPHEAN::"A deep dive into a system's internals to retrieve something valuable"

  FORCES: // Abstract System Dynamics
    HUBRIS::"Dangerous overconfidence in a system or plan"
    NEMESIS::"The inevitable corrective consequence of hubris or imbalance"
    KAIROS::"A critical, fleeting window of opportunity for action"
    CHRONOS::"Constant, linear time pressure; deadlines, performance decay"
    CHAOS::"The tendency of a system towards entropy and disorder"
    COSMOS::"The emergence of order and structure from chaos"
    MOIRA::"Deterministic outcomes; factors that are fated and cannot be changed"
    TYCHE::"Random chance; unpredictable external events, luck"

  RELATIONSHIPS: // Types of Interaction
    HARMONIA::"A state of perfect synthesis, balance, and synergy"
    ERIS::"Productive conflict or competition that drives innovation"
    EROS::"An attractive or binding force that pulls components together"
    THANATOS::"A destructive or unbinding force that pushes components apart"

---

ADVANCED_COMPOSITION:
  DESCRIPTION::"Techniques for creating high-value, high-density OCTAVE artifacts."
  SEMANTIC_GRANULARITY:
    PATTERN::"DOMAIN[:ASPECT][:INSTANCE]"
    EXAMPLES:
      L1::HERMES
      L2::HERMES:API
      L3::HERMES:API:REST
  STRING_VS_SEMANTIC:
    RULE::"Use semantic tokens for concepts; use strings for specific instances or external IDs."
    EXAMPLE::"POSEIDON:DB→\"postgres-prod-01\""

---

VALIDATION_AND_LINTING:
  DESCRIPTION::"The ability to diagnose and correct invalid or suboptimal OCTAVE."
  ERROR_MODEL:
    CRITICAL::"Document is INVALID. Stops processing. (e.g., Colon in key, chained synthesis)"
    WARNING::"Document is VALID but has style issues. (e.g., Flat hierarchy, buried network)"
  SMELL_DETECTION:
    // See octave-philosophy.md for full details
    SMELLS::[
      "Isolated Lists (no relationships)",
      "Flat Hierarchies (lack of grouping)",
      "Buried Networks (relationships hidden in prose)"
    ]

---

BOUNDARIES:
  CAN::[
    "Author complex, high-density OCTAVE knowledge artifacts using the full Pantheon",
    "Validate any OCTAVE document against advanced syntax rules",
    "Lint OCTAVE documents for quality and anti-patterns",
    "Apply advanced composition patterns (e.g., multi-level semantics)"
  ]
  CANNOT::[
    "Invent new syntax or semantic rules not listed here",
    "Contradict the rules in QUICKSTART_PATTERNS"
  ]

===END===
