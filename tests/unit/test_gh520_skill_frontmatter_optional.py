"""RED reproducers for GH#520 — SKILL schema mandates YAML where the spec makes it optional.

``src/octave_mcp/resources/specs/octave-skills-spec.oct.md`` is VERSION
``9.1.0``. Its §7 ``PLATFORM_ADAPTATION.YAML_FRONTMATTER_RULES`` splits the
requirement by deployment context::

    PLATFORM_SKILLS  LOCATION [".claude/skills/", ".codex/skills/", ...]
                     YAML::REQUIRED   (platforms parse YAML for discovery)
    HUB_SKILLS       LOCATION [".hestai-sys/library/skills/"]
                     YAML::OPTIONAL   (anchor ceremony reads OCTAVE META)

``src/octave_mcp/resources/specs/schemas/skill.oct.md`` scopes itself to
exactly the HUB location yet declares ``name`` / ``description`` /
``allowed-tools`` as ``REQUIRED::true``. A spec-compliant hub skill — OCTAVE
envelope, no frontmatter — is therefore rejected with three
``E_FM_REQUIRED`` errors. 50 of the 73 on-disk hub skills are in that state.

Resolution pinned by these tests (option b′): the schema language has no
deployment-context vocabulary and the validation engine has no path input
(``Validator.validate`` and ``validate_frontmatter`` never see a filesystem
location; ``octave_validate(content=...)`` has none to give). What IS
expressible — and what the schema language already uses for §-sections via
``POLICY.SECTION_CONDITIONAL_REQUIRED`` — is a presence-conditional:

    POLICY.FRONTMATTER_PRESENCE::OPTIONAL

  * frontmatter block absent  -> required-field checks are skipped (hub case)
  * frontmatter block present -> every REQUIRED field is enforced (platform
    and dual-deployed case)

This is PROD::I2 DETERMINISTIC_ABSENCE applied to Zone 2: "absent because
not required here" is a different fact from "present but incomplete", and
the validator must not collapse them. The default
(``FRONTMATTER_PRESENCE::REQUIRED``) preserves today's behaviour for every
other schema.

North Star compliance:
- PROD::I2 DETERMINISTIC_ABSENCE — absent frontmatter is distinguished from
  incomplete frontmatter.
- PROD::I4 TRANSFORM_AUDITABILITY — the schema records which skills-spec
  version it implements, so spec/schema drift is visible at a glance.
- PROD::I5 SCHEMA_SOVEREIGNTY — the verdict the validator emits must be one
  it has earned; a false INVALID is as much a sovereignty breach as a false
  clean.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import pytest

from octave_mcp.schemas.loader import load_schema_by_name

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SKILLS_DIR = _REPO_ROOT / ".hestai-sys" / "library" / "skills"

# A hub SKILL exactly as skills-spec v9.1 permits: OCTAVE envelope only,
# no YAML frontmatter at all.
_YAMLLESS_HUB_SKILL = (
    "===SKILL:HUB_ONLY===\n"
    "META:\n"
    "  TYPE::SKILL\n"
    '  VERSION::"1.0"\n'
    "  STATUS::ACTIVE\n"
    "§1::CORE\n"
    "PURPOSE::hub_skill_consumed_by_anchor_ceremony_not_by_a_platform_parser\n"
    "§5::ANCHOR_KERNEL\n"
    "TARGET::demonstrate_yaml_less_hub_skill_validity\n"
    "NEVER::[require_yaml_where_spec_v9_1_makes_it_optional]\n"
    "MUST::[carry_octave_meta_as_sole_source_of_truth]\n"
    'GATE::"Does the OCTAVE envelope stand alone?"\n'
    "===END===\n"
)


def _validate_content(content: str) -> dict[str, Any]:
    """Validate ``content`` against the SKILL schema through the MCP tool."""
    from octave_mcp.mcp.validate import ValidateTool

    return asyncio.run(ValidateTool().execute(content=content, schema="SKILL"))


def _frontmatter_errors(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every ``E_FM_*`` diagnostic surfaced by a validation result."""
    entries = list(result.get("validation_errors") or []) + list(result.get("errors") or [])
    return [e for e in entries if isinstance(e, dict) and str(e.get("code", "")).startswith("E_FM_")]


def _skill_files() -> list[Path]:
    if not _SKILLS_DIR.is_dir():
        return []
    return sorted(_SKILLS_DIR.glob("*/SKILL.md"))


class TestSchemaDeclaresSpecAlignment:
    """The schema must state which skills-spec version it implements (PROD::I4)."""

    def test_schema_declares_frontmatter_presence_optional(self) -> None:
        """SKILL POLICY must declare ``FRONTMATTER_PRESENCE::OPTIONAL``.

        Without a presence discriminator the schema can only express
        "always required" or "never required", and neither matches
        skills-spec v9.1 §7.
        """
        schema = load_schema_by_name("SKILL")
        assert schema is not None
        presence = getattr(schema.policy, "frontmatter_presence", None)
        assert presence == "OPTIONAL", (
            "SKILL schema POLICY must declare FRONTMATTER_PRESENCE::OPTIONAL — "
            "the schema governs .hestai-sys/library/skills/ where skills-spec "
            f"v9.1 §7 makes YAML OPTIONAL. Got {presence!r} (GH#520)."
        )

    def test_schema_records_implemented_spec_version(self) -> None:
        """SKILL schema META must name the skills-spec version it implements.

        The schema sat at VERSION "1.0" across skills-spec v9.0 -> v9.1,
        so the drift that produced GH#520 was invisible. PROD::I4 requires
        the transformation to leave a receipt.
        """
        schema_path = _REPO_ROOT / "src" / "octave_mcp" / "resources" / "specs" / "schemas" / "skill.oct.md"
        text = schema_path.read_text(encoding="utf-8")
        assert "IMPLEMENTS_SPEC" in text, (
            "skill.oct.md META must carry IMPLEMENTS_SPEC naming octave-skills-spec "
            "and its version, so spec/schema drift is visible at a glance (GH#520)."
        )
        assert "9.1.0" in text, "skill.oct.md must record that it implements octave-skills-spec v9.1.0 (GH#520)."

    def test_schema_version_bumped_past_1_0(self) -> None:
        """The schema version must move when its contract changes."""
        schema = load_schema_by_name("SKILL")
        assert schema is not None
        assert schema.version not in (None, "1.0"), (
            f"SKILL schema VERSION must be bumped past 1.0 to record the v9.1 "
            f"realignment; got {schema.version!r} (GH#520)."
        )


class TestYamlLessHubSkillValidatesClean:
    """A spec-compliant hub SKILL (no YAML at all) must not be rejected."""

    def test_yamlless_hub_skill_emits_no_frontmatter_errors(self) -> None:
        result = _validate_content(_YAMLLESS_HUB_SKILL)
        fm_errors = _frontmatter_errors(result)
        assert not fm_errors, (
            "A hub SKILL with no YAML frontmatter is valid under skills-spec "
            f"v9.1 §7 HUB_SKILLS YAML::OPTIONAL. Got {fm_errors!r} (GH#520)."
        )

    def test_yamlless_hub_skill_is_valid(self) -> None:
        result = _validate_content(_YAMLLESS_HUB_SKILL)
        assert result.get("validation_status") == "VALIDATED", (
            f"Expected VALIDATED for a spec-compliant YAML-less hub SKILL; got "
            f"status={result.get('validation_status')!r} errors={result.get('validation_errors')!r}"
        )
        assert result.get("valid") is True


class TestPlatformEnforcementPreserved:
    """Relaxation must not become abdication: present-but-incomplete still fails."""

    def test_partial_frontmatter_still_reports_missing_required_fields(self) -> None:
        """A SKILL that authors frontmatter must author all required fields.

        This is the enforcement that a blanket ``REQUIRED::false`` would
        throw away: a platform-deployed skill declaring only ``name`` would
        silently pass despite being undiscoverable without ``description``.
        """
        content = "---\nname: partial-skill\n---\n\n" + _YAMLLESS_HUB_SKILL
        result = _validate_content(content)
        fm_errors = _frontmatter_errors(result)
        missing = {str(e.get("field", "")) for e in fm_errors}
        assert "frontmatter.description" in missing, (
            "A SKILL that authors YAML frontmatter must still satisfy every "
            f"REQUIRED field; 'description' was not reported. Got {fm_errors!r} (GH#520)."
        )
        assert "frontmatter.allowed-tools" in missing, (
            f"'allowed-tools' must still be enforced when frontmatter is present. Got {fm_errors!r}"
        )

    def test_complete_frontmatter_still_validates(self) -> None:
        """A dual-deployed SKILL with complete frontmatter remains valid."""
        content = (
            "---\n"
            "name: dual-deployed-skill\n"
            "description: skill present in both hub and platform locations\n"
            "allowed-tools: [Bash]\n"
            "---\n\n"
        ) + _YAMLLESS_HUB_SKILL
        result = _validate_content(content)
        assert not _frontmatter_errors(result)
        assert result.get("valid") is True


class TestFrontmatterPresencePolicyEngine:
    """Unit-level contract for the presence discriminator in the validation engine."""

    @staticmethod
    def _schema(presence: str | None) -> Any:
        from octave_mcp.core.schema_extractor import FrontmatterFieldDef, PolicyDefinition, SchemaDefinition

        policy = PolicyDefinition()
        if presence is not None:
            policy.frontmatter_presence = presence
        return SchemaDefinition(
            name="TEST",
            version="1.0",
            policy=policy,
            fields={},
            frontmatter={"name": FrontmatterFieldDef(name="name", required=True, field_type="STRING")},
        )

    def test_absent_frontmatter_skipped_when_presence_optional(self) -> None:
        from octave_mcp.core.grammar.entry import validate_frontmatter

        errors = validate_frontmatter(None, self._schema("OPTIONAL"))
        assert errors == [], f"FRONTMATTER_PRESENCE::OPTIONAL must skip absent frontmatter; got {errors!r}"

    def test_absent_frontmatter_still_reported_by_default(self) -> None:
        """Regression guard: schemas that do not opt in keep today's behaviour."""
        from octave_mcp.core.grammar.entry import validate_frontmatter

        errors = validate_frontmatter(None, self._schema(None))
        assert [e.code for e in errors] == ["E_FM_REQUIRED"], (
            f"Default FRONTMATTER_PRESENCE must remain REQUIRED so other schemas are "
            f"unaffected; got {errors!r}"
        )

    def test_present_but_incomplete_reported_when_presence_optional(self) -> None:
        from octave_mcp.core.grammar.entry import validate_frontmatter

        errors = validate_frontmatter("version: 1\n", self._schema("OPTIONAL"))
        assert [e.code for e in errors] == ["E_FM_REQUIRED"], (
            f"FRONTMATTER_PRESENCE::OPTIONAL relaxes absence only, never an "
            f"incomplete present block; got {errors!r}"
        )

    def test_empty_frontmatter_block_still_enforced(self) -> None:
        """TMG-required: present-but-vacuous is presence, not absence.

        ``---\\n---`` authors a frontmatter block and leaves it empty. That
        is the "present but incomplete" case taken to its limit, so the
        required fields must still be reported.
        """
        from octave_mcp.core.grammar.entry import validate_frontmatter

        errors = validate_frontmatter("", self._schema("OPTIONAL"))
        assert [e.code for e in errors] == ["E_FM_REQUIRED"], (
            f"An empty-but-present frontmatter block must still surface missing "
            f"required fields; got {errors!r}"
        )

    def test_type_validation_survives_optional_presence(self) -> None:
        """TMG-required: OPTIONAL relaxes presence only, never type checking."""
        from octave_mcp.core.grammar.entry import validate_frontmatter

        errors = validate_frontmatter("name: 42\n", self._schema("OPTIONAL"))
        assert [e.code for e in errors] == ["E_FM_TYPE"], (
            f"A present field of the wrong type must still surface E_FM_TYPE under "
            f"FRONTMATTER_PRESENCE::OPTIONAL; got {errors!r}"
        )

    def test_invalid_presence_value_is_audited_and_fails_closed(self) -> None:
        """TMG-required: an unrecognised POLICY value must not silently relax.

        PROD::I4 requires the malformed shape to be logged (W_MALFORMED_POLICY)
        and PROD::I5 requires the validator to keep the stricter verdict it
        can actually justify, so an invalid value falls back to REQUIRED.
        """
        from octave_mcp.core.parser import parse
        from octave_mcp.core.schema_extractor import extract_schema_from_document

        doc = parse(
            "===TEST_SCHEMA===\n"
            "META:\n"
            "  TYPE::SCHEMA\n"
            '  VERSION::"1.0"\n'
            "POLICY:\n"
            '  VERSION::"1.0"\n'
            "  FRONTMATTER_PRESENCE::BANANA\n"
            "===END===\n"
        )
        schema = extract_schema_from_document(doc)
        codes = [w.code for w in schema.warnings]
        assert "W_MALFORMED_POLICY" in codes, (
            f"An unrecognised FRONTMATTER_PRESENCE value must emit W_MALFORMED_POLICY "
            f"(PROD::I4); got warnings={schema.warnings!r}"
        )
        assert schema.policy.frontmatter_presence == "REQUIRED", (
            f"An unrecognised FRONTMATTER_PRESENCE value must fail closed to REQUIRED; "
            f"got {schema.policy.frontmatter_presence!r}"
        )

    def test_policy_extractor_reads_frontmatter_presence(self) -> None:
        from octave_mcp.core.parser import parse
        from octave_mcp.core.schema_extractor import extract_schema_from_document

        doc = parse(
            "===TEST_SCHEMA===\n"
            "META:\n"
            "  TYPE::SCHEMA\n"
            '  VERSION::"1.0"\n'
            "POLICY:\n"
            '  VERSION::"1.0"\n'
            "  FRONTMATTER_PRESENCE::OPTIONAL\n"
            "===END===\n"
        )
        schema = extract_schema_from_document(doc)
        assert schema.policy.frontmatter_presence == "OPTIONAL"


class TestOnDiskHubCorpusHasNoFrontmatterErrors:
    """Integration: no on-disk hub SKILL is rejected for lacking YAML."""

    def test_corpus_collection_floor(self) -> None:
        """TMG-required: guard against a silent collection-path breakage.

        The parametrized assertion below vacuously passes if the corpus
        resolves to zero files (e.g. ``.hestai-sys`` unlinked in a fresh
        worktree). Pin a floor so the empty case is loud.
        """
        files = _skill_files()
        if not _SKILLS_DIR.exists():
            pytest.skip(f"{_SKILLS_DIR} not present (gitignored delivery path)")
        assert len(files) >= 50, (
            f"Expected the hub skills corpus to hold at least 50 SKILL.md files; "
            f"found {len(files)} under {_SKILLS_DIR}. A near-empty corpus makes the "
            f"parametrized assertion below vacuous."
        )

    @pytest.mark.parametrize(
        "skill_path",
        _skill_files(),
        ids=lambda p: p.parent.name,
    )
    def test_hub_skill_file_emits_no_frontmatter_errors(self, skill_path: Path) -> None:
        content = skill_path.read_text(encoding="utf-8")
        result = _validate_content(content)
        fm_errors = _frontmatter_errors(result)
        assert not fm_errors, (
            f"{skill_path.parent.name}/SKILL.md is a hub skill; skills-spec v9.1 §7 "
            f"makes YAML OPTIONAL there. Got {fm_errors!r} (GH#520)."
        )
