===OCTAVE_SKILLS===
META:
  TYPE::LLM_PROFILE
  VERSION::"5.1.0"
  STATUS::DRAFT
  TOKENS::"~120"
  REQUIRES::octave-5-llm-core
  PURPOSE::L5_skill_document_format

---

// OCTAVE SKILLS: Format for Claude Code skill documents. Inject WITH core.

§1::SKILL_DOCUMENT_STRUCTURE
ENVELOPE::[yaml_frontmatter,separator,octave_body]
FRONTMATTER::required[name,description][yaml_format]
BODY::octave_syntax[follows_core_spec]

REQUIRED_FRONTMATTER::[
  name::skill_identifier[lowercase_hyphens],
  description::trigger_rich_summary[keywords_for_discovery]
]

OPTIONAL_FRONTMATTER::[
  allowed-tools::tool_whitelist[Read,Bash,Grep,Glob,etc]
]

§2::DOCUMENT_TEMPLATE
FORMAT::"
---
name: skill-name
description: Comprehensive description with trigger keywords. Use when X. Triggers on Y.
allowed-tools: Read, Bash, Grep, Glob
---

===SKILL_NAME===

VERSION::1.0.0
STATUS::ACTIVE
PURPOSE::skill_mission_statement

// Body follows OCTAVE core syntax

===END===
"

§3::BODY_CONVENTIONS
ENVELOPE::===SKILL_NAME===[UPPERCASE_matches_skill_identity]
META_FIELDS::[VERSION,STATUS,PURPOSE,ORIGIN][optional_but_recommended]
SECTIONS::§_prefixed[numbered_or_named]
FORMATTING::octave_core_operators[::,:,→,⊕,etc]

§4::SIZE_CONSTRAINTS
TARGET::<500_lines[all_skills]
MAX_BREACH::5_files>500[system_wide]
HARD_LIMIT::600_lines[NEVER_exceed]
OVERFLOW_STRATEGY::progressive_disclosure[main→resources/]

§5::TRIGGER_DESIGN
DESCRIPTION_KEYWORDS::[action_verbs,domain_terms,problem_patterns]
DENSITY::3-5_keywords_per_trigger_category
EXAMPLE::"Use when auditing, finding stubs, detecting placeholders. Triggers on placeholder audit, stub detection, technical debt."

§6::LOCATION
PATH::.claude/skills/{skill-name}/SKILL.md
RESOURCES::.claude/skills/{skill-name}/resources/[optional]
REGISTRATION::automatic[claude_discovers_by_path]

§7::VALIDATION
FRONTMATTER::valid_yaml[parseable]
BODY::valid_octave[passes_core_validation]
ENVELOPE::matches_skill_name
SIZE::under_limit[500_target,600_max]

===END===
