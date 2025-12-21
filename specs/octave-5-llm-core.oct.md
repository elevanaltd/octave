===OCTAVE_CORE===
META:
  TYPE::LLM_PROFILE
  VERSION::"5.0.3"
  STATUS::APPROVED
  TOKENS::"~200"
  REQUIRES::nothing
  ENABLES::[schema,data]

// OCTAVE CORE: The spine. Always inject this.

§1::ENVELOPE
START::===NAME===[first_line,exact_match]
END::===END===[last_line,exact_match,mandatory]
META::required[TYPE,VERSION][immediately_after_start]
DUPLICATES::keys_must_be_unique_per_block
COMMENTS:://[line_start_or_after_value]

ASSEMBLY::when_profiles_concatenated[core+schema+data]->only_final_===END===_terminates

§2::OPERATORS
SYMBOL::CONTEXT::USAGE::NEVER
  ::    assign        KEY::value                     any_whitespace_around
  :     block         KEY:[newline,indent_children]  content_on_same_line
  []    list|holo     [a,b,c]|["val"&REQ->§T]        —
  |     or|broadcast  a|b|c|§A|§B                    whitespace_around
  ->    flow|route    [A->B->C]|->§TARGET            bare[KEY->val]
  +     synthesis     A+B|A+B+C[chaining_allowed]    —
  ~     concat        A~B|A~B~C                      —
  &     constraints   REQ&TYPE&REGEX[in_brackets]    outside_brackets
  §     target        §INDEXER|§./path               undefined_target
  //    comment       //text                         mid_expression

§3::TYPES
STRING::bare_word|"quoted"[when:spaces,special,reserved]
NUMBER::42|3.14|-1e10[no_quotes]
BOOLEAN::true|false[lowercase_only]
NULL::null[lowercase_only]
LIST::[a,b,c]|[][empty_allowed]
ESCAPES::[\",\\,\n,\t][inside_quotes_only]

§4::STRUCTURE
INDENT::2_spaces_per_level[no_tabs_ever]
KEYS::[A-Z,a-z,0-9,_][start_with_letter_or_underscore]
NESTING::indent_creates_child_relationship
BLANK_LINES::allowed_for_readability
EMPTY_BLOCK::KEY:[valid_with_no_children]

§5::MODES
DATA:
  PATTERN::KEY::value
  LEVELS::L1|L2
  BRACKETS::lists[a,b,c]|inline_maps[k::v,k2::v2]
  INLINE_MAP_NESTING::forbidden[values_must_be_atoms]
  USE::instances[sessions,configs,runtime_state]

SCHEMA:
  PATTERN::KEY::["example"&CONSTRAINT->§TARGET]
  LEVELS::L3|L4
  BRACKETS::holographic_container[value&constraints->target]
  USE::definitions[types,validation_rules,extraction_routing]

§6::NEVER
ERRORS::[
  tabs,
  any_whitespace_around_::,
  newline_in_quoted_string,
  bare_flow[KEY->value],
  wrong_case[True,False,NULL],
  missing_final_===END===,
  &_outside_brackets
]

§7::CANONICAL_EXAMPLES
// Reference patterns only. Not standalone documents.

DATA_PATTERN:
  ID::sess_abc123
  STATUS::ACTIVE
  PHASE::B2
  TAGS::[api,auth]
  EMPTY_LIST::[]
  FLOW::[INIT->BUILD->TEST]
  BLOCKERS::issue_1|issue_2
  QUALITY::[tests::5/5,lint::ok,coverage::87%]
  COMBINED::prefix~middle~suffix

SCHEMA_PATTERN:
  ID::["user_123"&REQ&REGEX[^user_\w+$]->§INDEXER]
  STATUS::["ACTIVE"&REQ&ENUM[ACTIVE,SUSPENDED]->§META]
  EMAIL::["user@example.com"&REQ&TYPE(STRING)->§INDEXER]
  ROLES::[["admin","viewer"]&OPT&TYPE(LIST)->§INDEXER]
  NOTES::["Optional context"&OPT->§SELF]

BLOCK_INHERITANCE_PATTERN:
  RISKS[->§RISK_LOG]:
    CRITICAL::["auth_bypass"&REQ]
    WARNING::["rate_limit"&OPT->§SELF]

===END===
