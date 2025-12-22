===OCTAVE_MCP_BUILD_PLAN===
META:
  TYPE::BUILD_PLAN
  VERSION::"1.1.0"
  STATUS::APPROVED
  DATE::"2025-12-22"
  PHASE::[B1_TASK_DECOMPOSITION]
  OCTAVE_VERSION::"5.1.0"
  TOTAL_TASKS::25

---

§1::CLARIFICATIONS_RECORD

QUESTIONS_ASKED::[
  "Technology stack confirmed: Python 3.9+ for core library and MCP server?",
  "Use existing octave-validator.py as starting point or rewrite?",
  "Schema repository location: embedded in package or external?",
  "CLI commands priority: validate-only first, or full ingest/eject/validate?",
  "Test framework: pytest (matches existing test_octave_validator.py)?",
  "MCP library version: mcp>=1.0.0 (matches PAL MCP pattern)?"
]

ANSWERS_RECEIVED::[
  "Python 3.9+ confirmed, matches PAL MCP patterns",
  "Refactor existing validator as foundation, don't start from scratch",
  "Embedded schema repository in package, custom schemas supported later",
  "Full CLI suite from start (ingest/eject/validate) - they share core pipeline",
  "pytest confirmed, existing test structure is good foundation",
  "MCP 1.0.0+ confirmed"
]

TECHNOLOGY_DECISIONS::[
  BUILD_TOOL::setuptools[matches_PAL_MCP],
  PACKAGE_MANAGER::pip[standard_python],
  TEST_FRAMEWORK::pytest[existing_tests_use_this],
  LINTING::[ruff,black][modern_python_standards],
  TYPECHECK::mypy[strict_mode_type_safety],
  CLI_FRAMEWORK::click[per_spec_§12],
  MCP_LIBRARY::"mcp>=1.0.0"[official_anthropic_sdk],
  STRUCTURE::src_layout[octave_mcp_package]
]

§2::ARCHITECTURE_OVERVIEW

PACKAGE_STRUCTURE:
  ROOT::octave-mcp/
  SRC::src/octave_mcp/[main_package]
  TOOLS::src/octave_mcp/tools/[mcp_tool_implementations]
  CLI::src/octave_mcp/cli/[command_line_interface]
  SCHEMAS::src/octave_mcp/schemas/[builtin_schema_definitions]
  TESTS::tests/[unit,integration,fixtures]

DEPENDENCY_GRAPH:
  CORE_PARSER→CANONICAL_EMITTER
  CORE_PARSER→VALIDATOR
  VALIDATOR→REPAIR_ENGINE
  REPAIR_ENGINE→REPAIR_LOG
  CLI→[CORE_PARSER,CANONICAL_EMITTER,VALIDATOR]
  MCP_TOOLS→[CORE_PARSER,CANONICAL_EMITTER,VALIDATOR,REPAIR_ENGINE]

CRITICAL_PATH::[
  P1.1→P1.2→P1.3→P1.4[core_library_foundation],
  P1.4→P1.5→P1.6[validation_and_repair],
  P1.6→P2.1→P2.2[mcp_integration]
]

§3::PHASE_1_CORE_LIBRARY

EPIC::P1[CORE_LIBRARY][foundation_for_all_operations]

P1.1:
  ID::setup_project_structure
  DESCRIPTION::Initialize Python package with pyproject.toml, directory structure, and development tooling
  TDD_SEQUENCE::"TEST: verify package imports and structure → FEAT: create package scaffold"

  FILES:
    PRIMARY::[
      `pyproject.toml`,
      `src/octave_mcp/__init__.py`,
      `src/octave_mcp/core/__init__.py`,
      `src/octave_mcp/tools/__init__.py`,
      `src/octave_mcp/cli/__init__.py`,
      `tests/conftest.py`
    ]

  DEPENDENCIES::[]

  ACCEPTANCE_CRITERIA::[
    "pip install -e . succeeds without errors",
    "import octave_mcp works in Python",
    "pytest discovers test directory",
    "ruff and black configuration present and working"
  ]

  COMPLEXITY::S

  TECHNOLOGY_RATIONALE::"Use src-layout to avoid package shadowing issues. Follow PAL MCP pyproject.toml patterns for MCP server compatibility."

P1.2:
  ID::lenient_lexer_with_ascii_normalization
  DESCRIPTION::Implement lexer that accepts ASCII aliases and normalizes to unicode operators
  TDD_SEQUENCE::"TEST: ascii alias tokenization (-> to →, + to ⊕, vs to ⇌) → FEAT: lexer with normalization table"

  FILES:
    PRIMARY::[
      `src/octave_mcp/core/lexer.py`,
      `tests/unit/test_lexer.py`
    ]
    REFERENCE::[
      `tools/octave-validator.py`[existing_tokenization_logic]
    ]

  DEPENDENCIES::[P1.1]

  ACCEPTANCE_CRITERIA::[
    "Tokenizes canonical unicode operators (→,⊕,⧺,⇌,∨,∧,§,::,:)",
    "Normalizes ASCII aliases to unicode (->,+,~,vs,|,&,#)",
    "Enforces word boundaries for 'vs' operator (rejects SpeedvsQuality)",
    "Applies NFC unicode normalization",
    "Logs all normalizations with before/after in repairs list",
    "Rejects tabs with clear error E005",
    "Longest-match rule: :: recognized before :"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Lexer is foundation for all parsing. Deterministic normalization (not inference) is core architectural principle per §1 PHILOSOPHY."

P1.3:
  ID::lenient_parser_with_envelope_completion
  DESCRIPTION::Parse lenient OCTAVE into AST, infer envelope for single-doc inputs
  TDD_SEQUENCE::"TEST: parse with missing envelope, whitespace around ::, bare strings → FEAT: parser with inference rules"

  FILES:
    PRIMARY::[
      `src/octave_mcp/core/parser.py`,
      `src/octave_mcp/core/ast_nodes.py`,
      `tests/unit/test_parser.py`
    ]

  DEPENDENCIES::[P1.2]

  ACCEPTANCE_CRITERIA::[
    "Parses canonical strict OCTAVE without changes",
    "Infers ===INFERRED=== envelope for single-doc input without @schema",
    "Normalizes 'KEY :: value' to 'KEY::value' (whitespace removal)",
    "Handles block operator : for nested structures",
    "Enforces 2-space indentation (no tabs)",
    "All normalizations logged in repairs[] with TIER::NORMALIZATION",
    "Errors on single colon assignment with E001",
    "Errors on missing schema selector with E002"
  ]

  COMPLEXITY::L

  TECHNOLOGY_RATIONALE::"Parser enables lenient authoring mode while preserving semantic correctness. AST representation allows downstream validation and transformation."

P1.4:
  ID::canonical_emitter
  DESCRIPTION::Emit strict canonical OCTAVE from AST with deterministic formatting
  TDD_SEQUENCE::"TEST: emit canonical from various AST structures → FEAT: emitter with canonical rules"

  FILES:
    PRIMARY::[
      `src/octave_mcp/core/emitter.py`,
      `tests/unit/test_emitter.py`
    ]

  DEPENDENCIES::[P1.3]

  ACCEPTANCE_CRITERIA::[
    "Emits unicode operators (never ASCII aliases)",
    "No whitespace around :: assignment",
    "Explicit ===NAME=== envelope always present",
    "Quoted strings where required (spaces, special chars)",
    "2-space indentation consistent",
    "Idempotent: emit(parse(emit(parse(x)))) == emit(parse(x))",
    "Empty blocks emit as KEY: with no children"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Canonical form is storage/execution format. Deterministic emission ensures same AST always produces identical output for hashing/diffing."

P1.5:
  ID::schema_validator_with_constraint_checking
  DESCRIPTION::Validate AST against schema definitions, check constraints and types
  TDD_SEQUENCE::"TEST: validate against schema (required fields, types, enums, regex) → FEAT: validator engine"

  FILES:
    PRIMARY::[
      `src/octave_mcp/core/validator.py`,
      `src/octave_mcp/core/schema.py`,
      `src/octave_mcp/schemas/builtin/__init__.py`,
      `tests/unit/test_validator.py`
    ]

  DEPENDENCIES::[P1.4]

  ACCEPTANCE_CRITERIA::[
    "Validates required fields present (errors if missing)",
    "Type checking (STRING, NUMBER, BOOLEAN, LIST)",
    "Enum validation with exact match",
    "Regex pattern validation",
    "Unknown field detection (error in strict mode, warn in lenient)",
    "Block inheritance with →§TARGET validation",
    "Holographic constraint parsing (value∧CONSTRAINT→§TARGET)",
    "Never auto-fills missing required fields (E003)",
    "TEST: test_validator_required_fields_error, test_validator_enum_validation pass"
  ]

  COMPLEXITY::L

  RISK_MITIGATION::"Start with basic type validation, add constraint engine incrementally. Test unknown field detection in isolation before integrating with repair tiers."

  TECHNOLOGY_RATIONALE::"Schema validation enforces structural correctness. Constraints are checked, never auto-filled (forbidden repair tier)."

P1.6:
  ID::repair_engine_with_tier_classification
  DESCRIPTION::Implement schema-driven repair with NORMALIZATION/REPAIR/FORBIDDEN tiers
  TDD_SEQUENCE::"TEST: tier classification, enum casefold, forbidden repairs reject → FEAT: repair engine with tier logic"

  FILES:
    PRIMARY::[
      `src/octave_mcp/core/repair.py`,
      `src/octave_mcp/core/repair_log.py`,
      `tests/unit/test_repair.py`
    ]

  DEPENDENCIES::[P1.5]

  ACCEPTANCE_CRITERIA::[
    "TIER_NORMALIZATION: always applied (ascii→unicode, whitespace, quotes, envelope)",
    "TIER_REPAIR: only when fix=true, unique match required (enum casefold, type coercion)",
    "TIER_FORBIDDEN: always errors (no target inference, no field insertion, no structure changes)",
    "Repair log format with RULE_ID, BEFORE, AFTER, TIER, SAFE, SEMANTICS_CHANGED",
    "Ambiguous enum match errors with E006",
    "Cannot infer routing target errors with E004",
    "All repairs logged, no silent drift"
  ]

  COMPLEXITY::L

  TECHNOLOGY_RATIONALE::"Repair classification is architectural keystone per §5. Explicit control over semantic vs syntactic tolerance."

P1.7:
  ID::cli_implementation
  DESCRIPTION::Command-line interface for octave ingest, eject, validate commands
  TDD_SEQUENCE::"TEST: CLI invocations with args, output formats → FEAT: CLI with click"

  FILES:
    PRIMARY::[
      `src/octave_mcp/cli/main.py`,
      `src/octave_mcp/cli/commands.py`,
      `tests/integration/test_cli.py`
    ]

  DEPENDENCIES::[P1.6,P1.8]

  ACCEPTANCE_CRITERIA::[
    "octave ingest <file> --schema SCHEMA --fix --verbose",
    "octave eject <file> --schema SCHEMA --mode [canonical|authoring|executive|developer]",
    "octave validate <file> --schema SCHEMA --strict",
    "Exit codes: 0 success, 1 validation error, 2 usage error",
    "JSON output option for repair logs",
    "Verbose mode shows pipeline stages",
    "TEST: test_cli_ingest_valid_schema, test_cli_exit_codes pass"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"CLI framework is click per §12 DEPENDENCIES. Enables standalone usage and testing before MCP integration. Matches Phase 1 deliverable requirement."

P1.8:
  ID::builtin_schemas
  DESCRIPTION::Create builtin schema definitions for common OCTAVE document types
  TDD_SEQUENCE::"TEST: validate against builtin schemas (META, SESSION_LOG, DECISION_LOG) → FEAT: schema definitions"

  FILES:
    PRIMARY::[
      `src/octave_mcp/schemas/builtin/meta.oct.md`,
      `src/octave_mcp/schemas/builtin/session_log.oct.md`,
      `src/octave_mcp/schemas/builtin/decision_log.oct.md`,
      `tests/unit/test_builtin_schemas.py`
    ]

  DEPENDENCIES::[P1.5]

  ACCEPTANCE_CRITERIA::[
    "META schema validates TYPE, VERSION, STATUS fields",
    "SESSION_LOG schema for session artifacts",
    "DECISION_LOG schema for decision records",
    "Schemas written in OCTAVE L4 format",
    "Unknown Fields Policy enforced in META (strict mode rejects)"
  ]

  COMPLEXITY::S

  TECHNOLOGY_RATIONALE::"Builtin schemas provide immediate value and serve as examples. META schema critical for Unknown Fields Policy per §12A."

P1.9:
  ID::projection_modes
  DESCRIPTION::Implement eject() projection modes (canonical, authoring, executive, developer)
  TDD_SEQUENCE::"TEST: project to executive (omits technical fields), developer (omits executive) → FEAT: projection engine"

  FILES:
    PRIMARY::[
      `src/octave_mcp/core/projector.py`,
      `tests/unit/test_projector.py`
    ]

  DEPENDENCIES::[P1.4,P1.5]

  ACCEPTANCE_CRITERIA::[
    "MODE_CANONICAL: full document, lossy=false",
    "MODE_AUTHORING: lenient format, lossy=false",
    "MODE_EXECUTIVE: STATUS,RISKS,DECISIONS only, lossy=true",
    "MODE_DEVELOPER: TESTS,CI,DEPS only, lossy=true",
    "Returns LOSSY boolean and FIELDS_OMITTED list",
    "Field omission based on schema annotations"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Projection modes enable role-specific views per §9. Explicit lossy flag prevents silent information loss."

P1.10:
  ID::typecheck_baseline
  DESCRIPTION::Establish mypy typecheck baseline and configuration
  TDD_SEQUENCE::"TEST: mypy runs without errors on typed modules → FEAT: mypy.ini configuration and type annotations"

  FILES:
    PRIMARY::[
      `mypy.ini`,
      `src/octave_mcp/core/types.py`,
      `tests/unit/test_types.py`
    ]

  DEPENDENCIES::[P1.9]

  ACCEPTANCE_CRITERIA::[
    "mypy configuration with strict mode",
    "Type annotations for core modules (lexer, parser, emitter)",
    "Type stubs for AST nodes",
    "CI integration ready (python -m mypy src)",
    "TEST: mypy passes on all core modules"
  ]

  COMPLEXITY::S

  TECHNOLOGY_RATIONALE::"Type safety baseline prevents regression. Established early before codebase grows."

P1.11:
  ID::schema_loading_mechanism
  DESCRIPTION::Parse .oct.md schema files into core/schema.py Schema objects
  TDD_SEQUENCE::"TEST: load schema from .oct.md file, validate parsed structure → FEAT: schema loader"

  FILES:
    PRIMARY::[
      `src/octave_mcp/schemas/loader.py`,
      `tests/unit/test_schema_loader.py`
    ]

  DEPENDENCIES::[P1.5,P1.8]

  ACCEPTANCE_CRITERIA::[
    "Parse OCTAVE schema definitions from .oct.md files",
    "Extract field definitions with types, constraints, enums",
    "Build Schema objects for validator consumption",
    "Handle schema inheritance and references",
    "TEST: test_schema_loader_meta, test_schema_loader_constraints pass"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Schema loading bridges .oct.md schema definitions and validator engine. Self-hosting: uses OCTAVE parser to load OCTAVE schemas."

§4::PHASE_2_MCP_SERVER

EPIC::P2[MCP_SERVER][anthropic_mcp_integration]

P2.1:
  ID::mcp_tool_base_implementation
  DESCRIPTION::Base MCP tool infrastructure following PAL MCP patterns
  TDD_SEQUENCE::"TEST: MCP tool registration and schema generation → FEAT: base tool class"

  FILES:
    PRIMARY::[
      `src/octave_mcp/tools/base.py`,
      `src/octave_mcp/tools/schema_builder.py`,
      `tests/unit/test_mcp_base.py`
    ]
    REFERENCE::[
      `/Volumes/HestAI-Tools/pal-mcp-server/tools/shared/schema_builders.py`
    ]

  DEPENDENCIES::[P1.9]

  ACCEPTANCE_CRITERIA::[
    "BaseTool class with execute() method",
    "Schema builder for MCP tool parameters",
    "Parameter validation using pydantic",
    "Error handling with MCP-compatible error messages",
    "Tool registration mechanism working",
    "TEST: test_mcp_base_tool_registration, test_mcp_schema_builder pass"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Base infrastructure enables consistent tool implementation. Pattern proven in PAL MCP server."

P2.2:
  ID::octave_ingest_tool
  DESCRIPTION::MCP tool for octave.ingest (lenient→canonical with repair log)
  TDD_SEQUENCE::"TEST: ingest tool with various inputs, repair logging → FEAT: IngestTool class"

  FILES:
    PRIMARY::[
      `src/octave_mcp/tools/ingest.py`,
      `tests/integration/test_ingest_tool.py`
    ]

  DEPENDENCIES::[P2.1,P1.6]

  ACCEPTANCE_CRITERIA::[
    "Parameters: content, schema, tier, fix, verbose",
    "Returns: canonical, repairs[], warnings[], stages[] (if verbose)",
    "Pipeline: PREPARSE→PARSE→NORMALIZE→VALIDATE→REPAIR(if fix)→VALIDATE",
    "TIER parameter controls compression (LOSSLESS, CONSERVATIVE, AGGRESSIVE, ULTRA)",
    "All repairs logged with classification using REPAIR stage from P1.6",
    "Errors use E001-E007 format with educational rationale",
    "TEST: test_ingest_tool_repair_pipeline, test_ingest_tool_tier_stages pass"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Ingest is primary MCP tool per §7. Pipeline exposure via verbose enables debugging."

P2.3:
  ID::octave_eject_tool
  DESCRIPTION::MCP tool for octave.eject (canonical→projected format)
  TDD_SEQUENCE::"TEST: eject with projection modes, format conversion → FEAT: EjectTool class"

  FILES:
    PRIMARY::[
      `src/octave_mcp/tools/eject.py`,
      `tests/integration/test_eject_tool.py`
    ]

  DEPENDENCIES::[P2.1,P1.9]

  ACCEPTANCE_CRITERIA::[
    "Parameters: content (optional for template), schema, mode, format",
    "MODE: canonical, authoring, executive, developer using P1.9 projection modes",
    "FORMAT: octave, json, yaml, markdown",
    "Returns: output, lossy, fields_omitted[]",
    "Template generation when content=null",
    "Format conversion preserves structure",
    "TEST: test_eject_tool_projection_modes, test_eject_format_conversion pass"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Eject provides flexible output per §7 and §9. Template generation aids authoring."

P2.4:
  ID::mcp_server_entry_point
  DESCRIPTION::MCP server main entry point with tool registration
  TDD_SEQUENCE::"TEST: server initialization, tool discovery → FEAT: server.py with MCP integration"

  FILES:
    PRIMARY::[
      `src/octave_mcp/server.py`,
      `tests/integration/test_server.py`
    ]
    REFERENCE::[
      `/Volumes/HestAI-Tools/pal-mcp-server/server.py`
    ]

  DEPENDENCIES::[P2.2,P2.3]

  ACCEPTANCE_CRITERIA::[
    "MCP server starts and registers tools",
    "Tool discovery via MCP protocol",
    "octave.ingest and octave.eject available",
    "Error handling for tool execution failures",
    "Logging configuration with verbosity levels",
    "TEST: test_server_initialization, test_server_tool_discovery pass"
  ]

  COMPLEXITY::M

  RISK_MITIGATION::"Test server initialization in isolation before full MCP integration. Mock tool execution for initial tests, then add integration tests with real tools."

  TECHNOLOGY_RATIONALE::"Server entry point follows PAL MCP pattern. Enables Claude Desktop integration."

P2.5:
  ID::schema_repository_integration
  DESCRIPTION::Schema repository with builtin and custom schema support
  TDD_SEQUENCE::"TEST: load builtin schemas, register custom schemas → FEAT: SchemaRepository class"

  FILES:
    PRIMARY::[
      `src/octave_mcp/schemas/repository.py`,
      `src/octave_mcp/schemas/__init__.py`,
      `tests/unit/test_schema_repository.py`
    ]

  DEPENDENCIES::[P1.8,P2.1]

  ACCEPTANCE_CRITERIA::[
    "Load builtin schemas from package",
    "Register custom schemas from file paths",
    "Schema versioning support",
    "Schema lookup by name and version",
    "Validation against schema constraints",
    "TEST: test_schema_repository_builtin_load, test_schema_repository_custom_registration pass"
  ]

  COMPLEXITY::M

  RISK_MITIGATION::"Validate schema format on load to prevent invalid schema corruption. Test schema versioning with explicit version conflicts."

  TECHNOLOGY_RATIONALE::"Centralized schema management. Builtin schemas embedded, custom schemas loaded at runtime."

§5::VALIDATION_AND_TESTING

EPIC::P3[VALIDATION][property_based_testing]

P3.1:
  ID::canonicalization_property_tests
  DESCRIPTION::Property-based tests for canonicalization invariants
  TDD_SEQUENCE::"TEST: idempotence, determinism, totality properties → FEAT: property test suite"

  FILES:
    PRIMARY::[
      `tests/properties/test_canonicalization.py`
    ]

  DEPENDENCIES::[P1.4]

  ACCEPTANCE_CRITERIA::[
    "Idempotent: canon(canon(x)) == canon(x)",
    "Deterministic: same input always produces same output",
    "Total: every valid lenient input has exactly one canonical form",
    "Round-trip: parse(emit(ast)) == ast",
    "Uses hypothesis for property-based testing"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Property tests validate core architectural guarantees per §4 CANONICALIZATION_RULES."

P3.2:
  ID::repair_tier_enforcement_tests
  DESCRIPTION::Verify forbidden repairs always error, never silently apply
  TDD_SEQUENCE::"TEST: forbidden repair attempts (target inference, field insertion) → FEAT: enforcement test suite"

  FILES:
    PRIMARY::[
      `tests/unit/test_forbidden_repairs.py`
    ]

  DEPENDENCIES::[P1.6]

  ACCEPTANCE_CRITERIA::[
    "Target inference always errors (E004)",
    "Missing required field always errors (E003)",
    "Structure repair always errors",
    "Semantic rewrite always errors",
    "Schema inference without selector errors (E002)",
    "fix=true never adds new fields"
  ]

  COMPLEXITY::S

  TECHNOLOGY_RATIONALE::"Forbidden repair enforcement is critical trust boundary per §5 TIER_FORBIDDEN."

P3.3:
  ID::test_vectors_suite
  DESCRIPTION::Comprehensive test vectors from §12 VALIDATION_CRITERIA
  TDD_SEQUENCE::"TEST: all specified test vectors → FEAT: test data fixtures"

  FILES:
    PRIMARY::[
      `tests/fixtures/lenient_inputs.py`,
      `tests/fixtures/whitespace_variations.py`,
      `tests/fixtures/enum_cases.py`,
      `tests/integration/test_vectors.py`
    ]

  DEPENDENCIES::[P1.9]

  ACCEPTANCE_CRITERIA::[
    "Lenient inputs with ASCII aliases",
    "Whitespace variations (around ::, indentation)",
    "Enum casefold unique vs ambiguous",
    "Missing envelope single doc",
    "Forbidden repair attempts",
    "Projection mode field omission",
    "All vectors pass validation"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Test vectors from spec ensure implementation matches design. Fixtures enable reuse across test suites."

P3.4:
  ID::unknown_fields_policy_tests
  DESCRIPTION::Test unknown field detection in strict and lenient modes
  TDD_SEQUENCE::"TEST: unknown fields in META (strict rejects, lenient warns) → FEAT: policy enforcement tests"

  FILES:
    PRIMARY::[
      `tests/unit/test_unknown_fields.py`
    ]

  DEPENDENCIES::[P1.5,P1.8]

  ACCEPTANCE_CRITERIA::[
    "Strict mode rejects unknown fields with E007",
    "Lenient mode warns unknown fields (logged only)",
    "Scope: META block initially, document body in v1.1",
    "Error includes field path for debugging"
  ]

  COMPLEXITY::S

  TECHNOLOGY_RATIONALE::"Unknown Fields Policy per §12A prevents schema surface drift."

P3.5:
  ID::format_conversion_golden_tests
  DESCRIPTION::Golden master tests for format conversion (OCTAVE↔JSON↔YAML↔Markdown)
  TDD_SEQUENCE::"TEST: convert to all formats, verify round-trip fidelity → FEAT: golden test fixtures"

  FILES:
    PRIMARY::[
      `tests/golden/test_format_conversion.py`,
      `tests/golden/fixtures/sample.oct.md`,
      `tests/golden/fixtures/sample.json`,
      `tests/golden/fixtures/sample.yaml`,
      `tests/golden/fixtures/sample.md`
    ]

  DEPENDENCIES::[P2.3]

  ACCEPTANCE_CRITERIA::[
    "OCTAVE→JSON conversion preserves structure",
    "OCTAVE→YAML conversion preserves structure",
    "OCTAVE→Markdown conversion preserves structure (lossy acknowledged)",
    "Round-trip tests for lossless formats (OCTAVE↔JSON↔YAML)",
    "Golden files committed to track conversion stability",
    "TEST: test_format_conversion_round_trip_octave_json pass"
  ]

  COMPLEXITY::M

  TECHNOLOGY_RATIONALE::"Golden tests detect unintended format conversion changes. Ensures cross-format interoperability stability."

§6::DOCUMENTATION_AND_PACKAGING

EPIC::P4[DELIVERY][publication_ready]

P4.1:
  ID::package_documentation
  DESCRIPTION::README, API docs, usage examples for package
  TDD_SEQUENCE::"TEST: example code runs without errors → FEAT: documentation with runnable examples"

  FILES:
    PRIMARY::[
      `README.md`,
      `docs/api.md`,
      `docs/usage.md`,
      `examples/basic_ingest.py`,
      `examples/projection_modes.py`
    ]

  DEPENDENCIES::[P2.4]

  ACCEPTANCE_CRITERIA::[
    "README with installation and quick start",
    "API documentation for all public classes",
    "Usage examples that run successfully",
    "Error message documentation (E001-E007)",
    "Architecture overview diagram"
  ]

  COMPLEXITY::S

  TECHNOLOGY_RATIONALE::"Documentation enables adoption. Runnable examples serve as integration tests."

P4.2:
  ID::mcp_configuration_guide
  DESCRIPTION::Claude Desktop MCP configuration guide and installation
  TDD_SEQUENCE::"TEST: MCP config validates and loads → FEAT: configuration template and guide"

  FILES:
    PRIMARY::[
      `docs/mcp-setup.md`,
      `examples/claude_desktop_config.json`,
      `scripts/install-mcp.sh`
    ]

  DEPENDENCIES::[P2.4]

  ACCEPTANCE_CRITERIA::[
    "Claude Desktop configuration template",
    "Installation script for MCP server",
    "Troubleshooting guide",
    "Schema repository setup instructions",
    "Example tool invocations"
  ]

  COMPLEXITY::S

  TECHNOLOGY_RATIONALE::"MCP setup guide critical for user onboarding. Template reduces configuration errors."

P4.3:
  ID::ci_pipeline
  DESCRIPTION::GitHub Actions CI for lint, typecheck, test, build
  TDD_SEQUENCE::"TEST: CI pipeline runs successfully → FEAT: GitHub Actions workflow"

  FILES:
    PRIMARY::[
      `.github/workflows/ci.yml`
    ]

  DEPENDENCIES::[P3.3,P1.10]

  ACCEPTANCE_CRITERIA::[
    "Runs on pull request and push to main",
    "Steps: ruff check, black check, mypy, pytest, build",
    "Code coverage reporting",
    "Matrix testing: Python 3.9, 3.10, 3.11, 3.12",
    "TEST: CI workflow validates successfully"
  ]

  COMPLEXITY::S

  TECHNOLOGY_RATIONALE::"CI ensures quality gates per HestAI methodology. Requires mypy baseline from P1.10."

P4.4:
  ID::pypi_publishing
  DESCRIPTION::PyPI package publishing workflow and release preparation
  TDD_SEQUENCE::"TEST: build dist packages, validate metadata → FEAT: publish workflow"

  FILES:
    PRIMARY::[
      `.github/workflows/publish.yml`,
      `MANIFEST.in`,
      `scripts/release-check.sh`
    ]

  DEPENDENCIES::[P4.3]

  ACCEPTANCE_CRITERIA::[
    "Publish workflow triggers on git tag",
    "Version validation from pyproject.toml",
    "Build wheel and sdist distributions",
    "Upload to PyPI using trusted publishing",
    "Release notes generation from CHANGELOG",
    "TEST: test package install from TestPyPI"
  ]

  COMPLEXITY::S

  TECHNOLOGY_RATIONALE::"Automated publishing prevents manual release errors. Trusted publishing improves security over API tokens."

§7::DEPENDENCY_MATRIX

TASK_DEPENDENCIES:
  P1.1::[foundation]
  P1.2::[P1.1]
  P1.3::[P1.2]
  P1.4::[P1.3]
  P1.5::[P1.4]
  P1.6::[P1.5]
  P1.7::[P1.6,P1.8]
  P1.8::[P1.5]
  P1.9::[P1.4,P1.5]
  P1.10::[P1.9]
  P1.11::[P1.5,P1.8]
  P2.1::[P1.9]
  P2.2::[P2.1,P1.6]
  P2.3::[P2.1,P1.9]
  P2.4::[P2.2,P2.3]
  P2.5::[P1.8,P2.1]
  P3.1::[P1.4]
  P3.2::[P1.6]
  P3.3::[P1.9]
  P3.4::[P1.5,P1.8]
  P3.5::[P2.3]
  P4.1::[P2.4]
  P4.2::[P2.4]
  P4.3::[P3.3,P1.10]
  P4.4::[P4.3]

CRITICAL_PATH::[P1.1→P1.2→P1.3→P1.4→P1.5→P1.6→P1.9→P2.1→P2.2→P2.4]

PARALLEL_OPPORTUNITIES::[
  [P1.7,P1.8,P1.9][after_P1.6],
  [P1.10,P1.11][after_P1.9],
  [P2.2,P2.3,P2.5][after_P2.1],
  [P3.1,P3.2,P3.3,P3.4][after_P1.9],
  [P3.5][after_P2.3],
  [P4.1,P4.2][after_P2.4],
  [P4.3][after_P3.3+P1.10]
]

§8::RISK_ASSESSMENT

HIGH_RISK_TASKS::[
  P1.3[lenient_parser_complexity],
  P1.6[repair_tier_classification_logic],
  P2.2[ingest_pipeline_integration]
]

MITIGATION_STRATEGIES::[
  P1.3::"Reuse existing octave-validator.py parsing logic, refactor incrementally",
  P1.6::"Start with NORMALIZATION only, add REPAIR tier after tests green",
  P2.2::"Test pipeline stages independently before integration"
]

TECHNICAL_DEBT_PREVENTION::[
  "No forbidden repairs implemented (maintain trust boundary)",
  "All repairs logged (no silent drift)",
  "Idempotent canonicalization (property tests enforce)",
  "Schema-driven validation (no ad-hoc rules)"
]

§9::EFFORT_ESTIMATES

EPIC_TOTALS:
  P1_CORE_LIBRARY::11_tasks[~22-28_hours]
  P2_MCP_SERVER::5_tasks[~10-12_hours]
  P3_VALIDATION::5_tasks[~9-12_hours]
  P4_DELIVERY::4_tasks[~6-8_hours]

TOTAL_ESTIMATE::25_tasks[~47-60_hours]

TASK_SIZE_DISTRIBUTION:
  SMALL::11_tasks[~2_hours_each]
  MEDIUM::10_tasks[~3_hours_each]
  LARGE::4_tasks[~5_hours_each]

§10::MILESTONE_ALIGNMENT

M1_CORE_FOUNDATION::[P1.1,P1.2,P1.3,P1.4][lenient_to_canonical_pipeline]
M2_VALIDATION::[P1.5,P1.6][schema_and_repair]
M3_CLI_COMPLETE::[P1.7,P1.8,P1.9,P1.10,P1.11][standalone_usability]
M4_MCP_ALPHA::[P2.1,P2.2,P2.3,P2.4][mcp_tools_working]
M5_MCP_BETA::[P2.5,P3.1,P3.2,P3.3,P3.4,P3.5][production_quality]
M6_RELEASE::[P4.1,P4.2,P4.3,P4.4][documentation_ci_publishing]

§11::SUCCESS_CRITERIA

PHASE_1_COMPLETE::[
  "octave ingest accepts lenient OCTAVE, emits canonical",
  "octave eject projects to multiple modes",
  "octave validate checks schemas with clear errors",
  "pip install octave-mcp works",
  "All property tests pass (idempotence, determinism)"
]

PHASE_2_COMPLETE::[
  "Claude Desktop can invoke octave.ingest and octave.eject",
  "MCP tools return proper repair logs",
  "Schema repository loads builtin and custom schemas",
  "Integration tests pass in MCP environment"
]

ARCHITECTURAL_VALIDATION::[
  "No forbidden repairs implemented (trust boundary maintained)",
  "All transformations logged (audit trail complete)",
  "Canonicalization is idempotent (property proven)",
  "Schema constraints enforced (no auto-fill)",
  "Unknown Fields Policy working (E007 errors)"
]

§12::TECHNOLOGY_STACK_SUMMARY

LANGUAGE::Python_3.9+
PACKAGE_MANAGER::pip
BUILD_TOOL::setuptools[src_layout]
TEST_FRAMEWORK::pytest[with_hypothesis_for_properties]
LINTING::[ruff,black,mypy]
MCP_SDK::"mcp>=1.0.0"
DEPENDENCIES::[
  pydantic[validation],
  python-dotenv[configuration],
  click[cli_framework]
]

===END===
