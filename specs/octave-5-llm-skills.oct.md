===OCTAVE_SKILLS===
META:
  TYPE::LLM_PROFILE
  VERSION::"5.1.0"
  STATUS::DRAFT
  TOKENS::"~180"
  REQUIRES::octave-5-llm-core
  PURPOSE::L5_skill_document_format[platform_agnostic]

---

// OCTAVE SKILLS: Universal format for AI agent skill documents.
// Supports Claude Code, Codex, and other YAML-frontmatter skill systems.

§1::SKILL_DOCUMENT_STRUCTURE
ENVELOPE::[yaml_frontmatter,separator,body]
FRONTMATTER::required[name,description][yaml_format]
BODY::platform_choice[octave_syntax∨markdown]

REQUIRED_FRONTMATTER::[
  name::skill_identifier[lowercase_hyphens_digits],
  description::trigger_rich_summary[keywords_for_discovery]
]

PLATFORM_SPECIFIC_FRONTMATTER::[
  claude_code::[allowed-tools::tool_whitelist],
  codex::[metadata.short-description::optional_brief]
]

§2::BODY_FORMAT_OPTIONS

OCTAVE_BODY::[
  USE_WHEN::[semantic_compression_needed,token_efficiency_critical,structured_protocols],
  ENVELOPE::===SKILL_NAME===[UPPERCASE],
  SYNTAX::follows_octave_core_spec,
  BENEFITS::[3-20x_compression,semantic_density,machine_parseable]
]

MARKDOWN_BODY::[
  USE_WHEN::[human_readability_priority,mixed_audience,extensive_code_blocks],
  FORMAT::standard_github_markdown,
  HEADERS::h1_for_title_h2_for_sections,
  BENEFITS::[familiar_syntax,wide_tooling_support,easy_editing]
]

HYBRID_BODY::[
  USE_WHEN::[octave_sections_with_markdown_code_blocks],
  PATTERN::octave_structure_with_markdown_fenced_code,
  EXAMPLE::COMMANDS section containing ```bash blocks
]

§3::DOCUMENT_TEMPLATES

OCTAVE_TEMPLATE::"
---
name: skill-name
description: Comprehensive description. Use when X. Triggers on Y, Z.
allowed-tools: Read, Bash, Grep, Glob
---

===SKILL_NAME===

VERSION::1.0.0
STATUS::ACTIVE
PURPOSE::skill_mission_statement

§1::SECTION_NAME
CONTENT::follows_octave_syntax

===END===
"

MARKDOWN_TEMPLATE::"
---
name: skill-name
description: Comprehensive description. Use when X. Triggers on Y, Z.
---

# Skill Name

Brief overview of the skill's purpose.

## Section Name

Content in standard markdown format.
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
EXAMPLE::"Use when auditing codebases, finding stubs. Triggers on placeholder audit, stub detection, technical debt."

§6::RESOURCE_STRUCTURE

CLAUDE_CODE_RESOURCES::[
  PATH::.claude/skills/{skill-name}/,
  MAIN::SKILL.md,
  OVERFLOW::resources/[deep_dives,examples]
]

CODEX_RESOURCES::[
  PATH::.codex/skills/{skill-name}/,
  MAIN::SKILL.md,
  SCRIPTS::scripts/[executable_code],
  REFERENCES::references/[documentation],
  ASSETS::assets/[templates,images,fonts]
]

UNIVERSAL_PRINCIPLES::[
  one_level_deep::avoid_nested_references,
  progressive_disclosure::main_file_links_to_resources,
  no_auxiliary_docs::no_README_CHANGELOG_etc
]

§7::PLATFORM_DIFFERENCES

CLAUDE_CODE::[
  BODY_FORMAT::octave_preferred[markdown_allowed],
  TOOL_RESTRICTIONS::allowed-tools_field,
  DISCOVERY::automatic_by_path,
  PACKAGING::none[directory_based]
]

CODEX::[
  BODY_FORMAT::markdown_required,
  TOOL_RESTRICTIONS::none,
  DISCOVERY::automatic_by_path,
  PACKAGING::.skill_file[zip_with_extension]
]

COMPATIBILITY_STRATEGY::[
  SAME_SKILL_BOTH_PLATFORMS::[
    maintain_parallel_versions,
    claude::.claude/skills/{name}/SKILL.md[octave],
    codex::.codex/skills/{name}/SKILL.md[markdown]
  ],
  CONTENT_PARITY::same_information_different_format
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

MARKDOWN_BODY::[
  structure::has_h1_title,
  formatting::valid_github_markdown
]

§9::FORBIDDEN

NEVER::[
  auxiliary_files::[README.md,CHANGELOG.md,INSTALLATION.md],
  deeply_nested_references::max_one_level,
  duplicate_information::SKILL.md_or_resources_not_both,
  table_of_contents::agents_scan_natively,
  line_number_references::stale_and_fragile
]

===END===
