===OCTAVE_SYNTAX_v1.0===
// OCTAVE (Olympian Common Text And Vocabulary Engine) Syntax Specification - Essential rules for consistent usage
// This document IS OCTAVE, demonstrating its own format

META:
  NAME::"OCTAVE Syntax Specification"
  VERSION::"1.0"
  PURPOSE::"Define OCTAVE syntax through OCTAVE itself"
  ENCODING::"UTF-8"
  EXTENSIONS::[.oct.md, .octave, .oct]
  VERSIONING::"Increment only on breaking syntax changes"
  SEMANTIC_REFERENCE::"./octave-semantics.oct.md"

0.DEF:
  // Core operators (symbols only - see semantics file for meanings)
  ASSIGN::"::"         // Double colon for assignment
  COMMENT::"//"        // Comment to end of line
  PROGRESS::"→"        // Progression arrow in lists
  SYNTHESIS::"⊕"       // Binary combination operator
  TENSION::"⚡"        // Binary opposition operator

// =================================
// DOCUMENT STRUCTURE
// =================================

ORDERING:
  MANDATORY_SEQUENCE:
    FIRST::"===DOCUMENT_NAME=== marker"
    SECOND::"0.DEF section (if terms are defined)"
    THEN::"All other sections in any order"
  RATIONALE::"Terms must be defined before use"

// =================================
// SYNTAX RULES
// =================================

CORE:
  ASSIGNMENT:
    OPERATOR::ASSIGN
    FORMAT::"KEY::VALUE"
    EXAMPLE::STATUS::ACTIVE
    
  HIERARCHY:
    INDENT::"  "  // Exactly 2 spaces per level
    CONSISTENT::true
    EXAMPLE:
      PARENT:
        CHILD::value
        ANOTHER:
          DEEP::nested_value
          
  LISTS:
    FORMAT::"[item, item, item]"
    NO_TRAILING_COMMA::true
    CAN_NEST::true
    CAN_USE_OPERATORS::true
    EXAMPLES:
      SIMPLE::[a, b, c]
      WITH_PROGRESSION::[INIT→BUILD→DEPLOY]
      NESTED::[[inner], [another, [deep]]]
      
  COMMENTS:
    OPERATOR::COMMENT
    SCOPE::"To end of line"
    ALLOWED_LOCATIONS::[
      "Start of any line",
      "After complete value on same line",
      "Inside indented object blocks"
    ]
    FORBIDDEN_LOCATIONS::[
      "Inside [] list delimiters",
      "Inside {{}} inline object delimiters", 
      "Between KEY:: and VALUE"
    ]
    EXAMPLES:
      VALID:
        // Full line comment
        KEY::VALUE  // End of line
        OBJECT:
          // Comment in nested structure
          NESTED::VALUE
      INVALID::"LIST::[a, // NO: inside list]"

DATA_TYPES:
  STRING:
    BARE::identifier_no_spaces
    QUOTED::"\"text with spaces\""
    MULTILINE::"""
    Line one
    Line two (indent preserved)
    """
    EMPTY::"\"\""  // Must use quotes for empty
    ESCAPE_SEQUENCES::[
      "\\\" → quotation mark",
      "\\\\ → backslash",
      "\\n → newline", 
      "\\r → carriage return",
      "\\t → tab",
      "\\uXXXX → unicode character"
    ]
    
  NUMBER:
    SUPPORTED::[42, 3.14, -1e10, Infinity, NaN]
    UNSUPPORTED:
      FORMATS::[hex, octal, binary, underscore_separated]
      RULE::"Must quote as strings"
      EXAMPLES::[
        "\"0xFF\"",    // Hex
        "\"0o755\"",   // Octal  
        "\"0b1010\"",  // Binary
        "\"1_000\""    // Underscore
      ]
    NEVER_QUOTE::"Supported number formats"
    
  BOOLEAN:
    VALUES::[true, false]  // Lowercase only
    NEVER_QUOTE::true
    INVALID::[True, TRUE, "true"]
    
  NULL:
    VALUE::null  // Lowercase only
    NEVER_QUOTE::true
    INVALID::[Null, NULL, "null"]
    
  OBJECT:
    INLINE:
      FORMAT::{{key:value, key2:value2}}
      SINGLE_COLON::true
      NO_NESTED_OBJECTS::"Values cannot be objects"
      ALLOWED_VALUES::[strings, numbers, booleans, lists]
      EXAMPLE::{{name:"test", count:42, tags:[a, b]}}
    STRUCTURED:
      FORMAT::"Key with indented block"
      UNLIMITED_NESTING::true
      ANY_VALUE_TYPES::true
      EXAMPLE:
        CONFIG:
          name::"Example"
          settings:
            host::"localhost"
            nested:
              deep::true

STRUCTURE:
  KEYS:
    ALLOWED_START::[A-Z, a-z, _]
    ALLOWED_CHARS::[A-Z, a-z, 0-9, _]
    FORBIDDEN::":"  // No colons in key names
    CASE_SENSITIVE::true
    EXAMPLES:
      VALID::[userName, user_name, _private, KEY2]
      INVALID::["user:name", "my-key", "123start"]
      
  VALUES:
    WHITESPACE_PRESERVED::true
    EMPTY_STRING_REQUIRES_QUOTES::true
    TYPE_DISAMBIGUATION:
      STRING_42::"\"42\""      // String
      NUMBER_42::42            // Number
      STRING_TRUE::"\"true\""  // String  
      BOOLEAN_TRUE::true       // Boolean
      
  DOCUMENT_VS_DATA:
    HEADERS::"# lines organize content but aren't OCTAVE data"
    DATA::"Only KEY: and KEY:: patterns create data structure"
    COMMENTS::"// lines provide context but aren't data"
    
  SPECIAL_SECTIONS:
    META::"Document metadata (usually first)"
    0.DEF::"Define terms before use"

// =================================
// SYNTACTIC OPERATORS
// =================================

OPERATOR_RULES:
  SEMANTIC_REFERENCE::"./octave-semantics.oct.md#SECTION_I:SEMANTIC_OPERATORS*:

  // For the full list of validated patterns, see the guides
  GUIDE_REFERENCE::"../guides/llm-octave-quick-reference.oct.md"
  
  SYNTHESIS:
    SYMBOL::SYNTHESIS  // ⊕
    USAGE::"Between exactly two elements"
    BINARY_ONLY::true  // No chaining allowed
    EXAMPLE::APOLLO⊕HERMES
    INVALID::"A⊕B⊕C"  // Cannot chain
    
  TENSION:
    SYMBOL::TENSION  // ⚡
    USAGE::"Between exactly two elements"
    BINARY_ONLY::true  // No chaining allowed
    EXAMPLE::SPEED⚡RELIABILITY
    INVALID::"A⚡B⚡C"  // Cannot chain
    
  PROGRESSION:
    SYMBOL::PROGRESS  // →
    USAGE::"Inside lists ONLY"
    CAN_CHAIN::true
    VALID::[START→MIDDLE→END]
    INVALID::"KEY::START→END"  // Not outside lists

// =================================
// KEY CLARIFICATIONS
// =================================

SINGLE_VS_DOUBLE_COLON:
  ASSIGNMENT::"KEY::VALUE uses double colon"
  STRUCTURE::"KEY: starts nested block"
  IN_OBJECTS::"{{key:value}} uses single colon"
  IN_DEFINITIONS::"CATEGORY:TERM in 0.DEF only"
  
EMPTY_SECTIONS:
  SYNTACTIC_BEHAVIOR::"KEY: with no content = empty object"
  VALID::true
  EXAMPLE:
    PLACEHOLDER:
    NEXT::value
  SEMANTIC_REFERENCE::"/config/_system/octave-semantics.oct.md#EMPTY_SECTIONS"
    
MULTILINE_STRINGS:
  INDENTATION::"Preserved relative to opening \"\"\""
  CLOSING::"\"\"\" on its own line"
  ESCAPES::"Work inside multiline strings"

// =================================
// ERROR HANDLING
// =================================

ERROR_MODEL:
  PURPOSE::"Define validity for consistent validation"
  
  ERROR_CATEGORIES:
    CRITICAL::"Document is INVALID - cannot be processed"
    WARNING::"Document is VALID but has style issues"
    
  CRITICAL_ERRORS:
    SYNTAX_VIOLATIONS::[
      "Colon in key name",
      "Invalid operator usage",
      "Malformed structure",
      "Undefined term usage"
    ]
    EXAMPLES::[
      "KEY:NAME::value",  // Colon in key
      "VALUE::A⊕B⊕C",     // Chained synthesis
      "{{nested:{{bad}}}}",  // Nested inline objects
    ]
    
  VALIDATION_BEHAVIOR:
    ON_CRITICAL::"Stop processing, mark document INVALID"
    ON_WARNING::"Continue processing, note issues"
    
  ERROR_REPORTING:
    REQUIRED_INFO::[
      "line: <number>",
      "column: <position>", 
      "error_type: <category>",
      "found: <actual>",
      "expected: <valid_form>"
    ]
    EXAMPLE:
      ERROR::{{
        line:45,
        column:8,
        error_type:"COLON_IN_KEY",
        found:"USER:NAME",
        expected:"USER_NAME"
      }}

// =================================
// COMPLETE EXAMPLE
// =================================

FULL_EXAMPLE::"""
===CONFIG_EXAMPLE===
// Demonstrates all OCTAVE features

META:
  NAME::"Example Configuration"
  VERSION::"1.0"
  TYPE::CONFIG

0.DEF:
  ENV:PROD::"Production environment"
  HEX_PORT::"\"0x1F90\""  // Hex as quoted string
  
### System Configuration
CONFIG:
  environment::ENV:PROD
  server:
    host::"localhost"
    port::8080  // Decimal number
    alt_port::HEX_PORT  // Using defined hex string
    features::[auth, cache, logs]
    
  database:
    // Comment inside structured object
    connection::"postgresql://localhost/mydb"
    pool::{{min:5, max:20, timeout:30}}
    
  workflow::[CONNECT→VALIDATE→PROCESS→RESPOND]
  architecture::APOLLO⊕HERMES  // Syntactic example only
  balance::PERFORMANCE⚡CONSISTENCY
  
  description::"""
  Multi-line with \n escapes
  and preserved   spacing
  """

===END_EXAMPLE===
"""

// =================================
// REFERENCES
// =================================

REFERENCES:
  SEMANTIC_LAYER::"/config/_system/octave-semantics.oct.md"
  AUTHORING_GUIDE::"/docs/guides/octave-authoring-guide.oct.md"
  REVIEW_CHECKLIST::"/docs/guides/octave-review-checklist.oct.md"

===END_SYNTAX===