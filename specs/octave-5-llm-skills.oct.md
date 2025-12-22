===OCTAVE_SKILLS===
META:
  TYPE::LLM_PROFILE
  VERSION::"5.3.0"
  STATUS::DRAFT
  TOKENS::"~140"
  REQUIRES::octave-5-llm-core
  PURPOSE::L5_skill_document_format[platform_agnostic]

---

// OCTAVE SKILLS: Universal format for AI agent skill documents.
// Validated with Claude Code and Codex. OCTAVE body works on both platforms.

§1::SKILL_DOCUMENT_STRUCTURE
ENVELOPE::[yaml_frontmatter,separator,body]
FRONTMATTER::required[name,description][yaml_format]
BODY::octave_syntax∨markdown[octave_preferred]

REQUIRED_FRONTMATTER::[
  name::skill_identifier[lowercase_hyphens_digits],
  description::trigger_rich_summary[keywords_for_discovery]
]

PLATFORM_SPECIFIC_FRONTMATTER::[
  claude_code::[allowed-tools::tool_whitelist[optional]],
  codex::[metadata.short-description::optional_brief]
]

§2::BODY_FORMAT

OCTAVE_BODY::[
  STATUS::recommended[works_on_claude_and_codex],
  ENVELOPE::===SKILL_NAME===[UPPERCASE],
  SYNTAX::follows_octave_core_spec,
  BENEFITS::[3-20x_compression,semantic_density,machine_parseable,cross_platform]
]

MARKDOWN_BODY::[
  STATUS::allowed[when_human_readability_priority],
  FORMAT::standard_github_markdown,
  USE_WHEN::[extensive_code_examples,mixed_human_ai_audience]
]

§3::DOCUMENT_TEMPLATE
FORMAT::"
---
name: skill-name
description: Comprehensive description. Use when X. Triggers on Y, Z.
---

===SKILL_NAME===

VERSION::1.0.0
STATUS::ACTIVE
PURPOSE::skill_mission_statement

§1::SECTION_NAME
CONTENT::follows_octave_syntax

===END===
"

§4::SIZE_CONSTRAINTS
TARGET::<500_lines[all_skills]
MAX_BREACH::5_files>500[system_wide]
HARD_LIMIT::600_lines[NEVER_exceed]
OVERFLOW_STRATEGY::progressive_disclosure[main→resources]

§5::TRIGGER_DESIGN
DESCRIPTION_KEYWORDS::[action_verbs,domain_terms,problem_patterns]
DENSITY::3-5_keywords_per_trigger_category
PATTERN::"Use when [actions]. Triggers on [keywords]."

§6::RESOURCE_STRUCTURE

CLAUDE_CODE::[
  PATH::.claude/skills/{skill-name}/,
  MAIN::SKILL.md,
  OVERFLOW::resources/
]

CODEX::[
  PATH::.codex/skills/{skill-name}/,
  MAIN::SKILL.md,
  SCRIPTS::scripts/[executable_code],
  REFERENCES::references/[documentation],
  ASSETS::assets/[templates,images]
]

UNIVERSAL_PRINCIPLES::[
  one_level_deep::avoid_nested_references,
  progressive_disclosure::main_links_to_resources,
  no_auxiliary_docs::no_README_CHANGELOG
]

§7::PLATFORM_DIFFERENCES

CLAUDE_CODE::[
  TOOL_RESTRICTIONS::allowed-tools_field[optional],
  PACKAGING::directory_based[auto_discovered]
]

CODEX::[
  TOOL_RESTRICTIONS::none,
  PACKAGING::.skill_file[zip_format]
]

SHARED::[
  BODY_FORMAT::octave_works_on_both,
  DISCOVERY::automatic_by_path,
  FRONTMATTER::[name,description]_required
]

§8::VALIDATION
UNIVERSAL::[
  frontmatter::valid_yaml,
  name::matches_directory,
  description::non_empty_with_triggers,
  size::under_limit
]

OCTAVE_BODY::[
  envelope::present_and_matching,
  syntax::passes_octave_validation
]

§9::FORBIDDEN
NEVER::[
  auxiliary_files::[README.md,CHANGELOG.md],
  deeply_nested_references::max_one_level,
  duplicate_information::main_or_resources_not_both,
  table_of_contents::agents_scan_natively
]

===END===
