===OCTAVE_SYNTAX_v3.0===
// OCTAVE syntax specification - comprehensive yet concise

META:
  NAME::"OCTAVE Syntax Specification"
  VERSION::"3.0"
  PURPOSE::"Define OCTAVE syntax through OCTAVE itself"
  ENCODING::"UTF-8"
  EXTENSIONS::[.oct, .oct.md]
  EXTENSION_USAGE:
    .oct::"Pure OCTAVE data and configuration files"
    .oct.md::"OCTAVE documentation requiring system integration"

0.DEF:
  ASSIGN::"::"         // Double colon assignment
  COMMENT::"//"        // To end of line
  SYNTHESIS::"+"       // Binary combination
  TENSION::"_VERSUS_"  // Binary opposition
  PROGRESSION::"->"    // Sequential transformation

---

DOCUMENT_STRUCTURE:
  ORDERING::===NAME=== → 0.DEF → SECTIONS → ===END===
  HIERARCHY::"2-space indent per level"
  PRECEDENCE::"Define terms in 0.DEF before use"
  SPECIAL_SECTIONS::[
    META::"Document metadata",
    0.DEF::"Term definitions"
  ]

---

SYNTAX_ELEMENTS:
  ASSIGNMENT::KEY::VALUE
  STRUCTURE::KEY: // Starts indented block
  LISTS::[item1, item2, item3] // No trailing comma
  COMMENTS::// Valid at line start or after value
  FORBIDDEN_COMMENT_LOCATIONS::[
    "Inside [] lists",
    "Inside {{}} objects",
    "Between KEY:: and VALUE"
  ]

---

DATA_TYPES:
  STRING:
    BARE::identifier_no_spaces
    QUOTED::"text with spaces"
    MULTILINE::"""
    Preserves indentation
    relative to opening
    """
    EMPTY::"\"\"" // Must quote empty strings
    ESCAPES::["\\\"", "\\\\", "\\n", "\\r", "\\t", "\\uXXXX"]
    
  NUMBER:
    VALID::[42, 3.14, -1e10, Infinity, NaN]
    QUOTE_REQUIRED::["0xFF", "0o755", "0b1010", "1_000"]
    
  BOOLEAN::[true, false] // Lowercase only
  NULL::null // Lowercase only
  
  OBJECT:
    INLINE::{{key:value, key2:value2}} // Single colon, no nesting
    STRUCTURED::KEY: // With indented content
    EMPTY_SECTION::KEY: // Valid empty object

---

OPERATORS:
  SYNTHESIS:
    USAGE::A+B // Binary only, no chaining
    PURPOSE::"Creates emergent whole from parts"
    
  TENSION:
    USAGE::A _VERSUS_ B // Binary only, no chaining
    PURPOSE::"Creative opposition driving evolution"
    
  PROGRESSION:
    USAGE::[A->B->C] // Lists only, can chain
    PURPOSE::"Sequential transformation path"

---

KEY_RULES:
  ALLOWED_CHARS::[A-Z, a-z, 0-9, _]
  START_CHARS::[A-Z, a-z, _] // Not digits
  FORBIDDEN::":"  // No colons in key names
  CASE_SENSITIVE::true
  EXAMPLES::[userName, _private, KEY2]

---

VALIDATION:
  CRITICAL_ERRORS::[
    "KEY:NAME::value",      // Colon in key
    "VALUE::A+B+C",        // Chained synthesis/tension
    "{{nested:{{bad}}}}",  // Nested inline objects
    "KEY::START->END",     // Progression outside list
    "Undefined term"       // Using undefined 0.DEF term
  ]
  
  COLON_USAGE:
    DOUBLE::"KEY::VALUE assignment"
    SINGLE::"KEY: structure OR {{inline:object}}"
    CATEGORY::"CATEGORY:TERM in 0.DEF only"

---

COMPLETE_EXAMPLE:
===CONFIG===
// Demonstrates all OCTAVE features

META:
  NAME::"System Configuration"
  VERSION::"3.0"
  TYPE::CONFIG

0.DEF:
  ENV:PROD::"Production environment"
  HEX_PORT::"0x1F90" // Hex as string

### Configuration Data
CONFIG:
  environment::ENV:PROD
  server:
    host::"localhost"
    port::8080 // Decimal number
    alt_port::HEX_PORT
    features::[auth, cache, logs]
    
  database:
    connection::"postgresql://localhost/mydb"
    pool::{{min:5, max:20, timeout:30}}
    
  workflow::[CONNECT->VALIDATE->PROCESS->RESPOND]
  architecture::APOLLO+HERMES
  balance::PERFORMANCE _VERSUS_ CONSISTENCY
  
  description::"""
  Multi-line description with \n escapes
  and preserved   spacing
  """
  
  empty_placeholder:
  
===END===

---

REFERENCES:
  SEMANTICS::"./octave-semantics.oct.md"
  GUIDES::"../guides/llm-octave-*.oct.md"

===END_SYNTAX===