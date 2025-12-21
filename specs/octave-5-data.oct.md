===OCTAVE_V5_DATA===
META:
  TYPE::CONFIGURATION
  VERSION::"5.0"
  STATUS::ACTIVE
  EXTENDS::octave-5.oct.md

PURPOSE::compression[maximum_token_density]

ACTIVATION::[SESSION_CONTEXT,KNOWLEDGE_ARTIFACT,CONFIGURATION]

PATTERN:
  SYNTAX::KEY::value
  LEVEL::L1|L2

COMPRESSION:
  PRESERVE::[numbers,names,codes,operators,anchors]
  DROP::[articles,prepositions,filler]
  FLATTEN::prefer_pipes_over_nesting

ABBREVIATIONS:
  impl::implementation
  config::configuration
  DONE::completed
  WIP::in_progress
  PENDING::not_started

LIST_FORMS:
  PIPE::a|b|c
  BRACKET::[a,b,c]
  INLINE::[a->b->c]

VALIDATION:
  EXTERNAL::META.SCHEMA::path/to/schema.oct.md

RATIOS:
  VS_PROSE::5-10x
  VS_MARKDOWN::1.5-3x

EXAMPLE_DATA:
  PROJECT:
    PHASE::B1_FOUNDATION
    STATUS::WIP
    QUALITY::[tests::5/5,lint::2_errors,types::pending]
    BLOCKERS::ruff_B904|mypy_not_run
    NEXT::[fix_lint|run_types|impl_feature]
    COMMITS::[abc123::init,def456::port,ghi789::server]

===END===
