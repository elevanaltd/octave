"""Tests for GitHub issue #519: unpinned `mcp` dependency breaks CI.

`pyproject.toml` declared the `mcp` SDK dependency with no upper bound
(`mcp>=1.27.0`). CI installs fresh via `pip install -e ".[dev]"` (no
lockfile), so it resolves whatever satisfies that constraint from PyPI at
install time. mcp 2.x is a breaking release (camelCase kwargs renamed to
snake_case, `Server` generic arity changed, `ReadResourceContents` moved),
so an unbounded `mcp>=1.27.0` silently drifts CI onto an incompatible major
version the moment mcp 2.x is published -- exactly what happened: CI
resolved mcp 2.2.0 and `mypy src` failed with 17 errors across 4 files.

This is NOT reproducible by checking the *installed* mcp version: a
contributor's local `.venv` (synced via `uv sync` against `uv.lock`, which
pins mcp==1.27.0) stays green while CI silently drifts red, since `pip
install -e ".[dev]"` in CI does not consult `uv.lock` at all. The only
locally-verifiable regression test is against the *declared constraint*
in pyproject.toml itself -- that is the actual root cause and the only
artifact that is identical between a contributor's checkout and CI.

Tests verify:
- The `mcp` runtime dependency specifier in pyproject.toml declares an
  explicit upper bound excluding the breaking 2.x major series.
"""

import re
import tomllib
from pathlib import Path

PYPROJECT_PATH = Path(__file__).resolve().parents[2] / "pyproject.toml"


def _mcp_dependency_specifier() -> str:
    """Return the raw `mcp` dependency specifier string from [project.dependencies]."""
    data = tomllib.loads(PYPROJECT_PATH.read_text())
    dependencies = data["project"]["dependencies"]
    mcp_specifiers = [dep for dep in dependencies if re.match(r"^mcp\s*(>=|==|~=|<)", dep)]
    assert len(mcp_specifiers) == 1, (
        f"Expected exactly one 'mcp' runtime dependency declaration in "
        f"[project.dependencies], found {len(mcp_specifiers)}: {mcp_specifiers}"
    )
    return mcp_specifiers[0]


class TestMcpDependencyUpperBound:
    """GH#519: the mcp dependency must not float across a breaking major version."""

    def test_mcp_dependency_has_upper_bound_excluding_v2(self):
        """The `mcp` specifier in [project.dependencies] must cap below 2.0.

        mcp 2.x renamed camelCase kwargs to snake_case and changed the
        `Server` generic arity (see GH#519), breaking `mypy src` on CI
        the moment an unbounded `mcp>=1.27.0` resolves to 2.2.0+. This
        test pins the constraint itself, since that is the artifact CI's
        `pip install -e ".[dev]"` actually consults -- unlike a locally
        installed mcp version, which can stay at 1.27.0 (via uv.lock)
        even while the unbounded declaration silently breaks CI.
        """
        specifier = _mcp_dependency_specifier()

        assert "<2" in specifier, (
            f"mcp dependency specifier {specifier!r} has no upper bound excluding "
            f"the breaking mcp 2.x major release. GH#519: CI's `pip install -e "
            f"\".[dev]\"` resolved mcp 2.2.0 against an unbounded 'mcp>=1.27.0' "
            f"and `mypy src` failed with 17 errors (camelCase->snake_case kwarg "
            f"renames, Server generic arity change, ReadResourceContents move). "
            f"Expected a specifier containing '<2', e.g. 'mcp>=1.27.0,<2'."
        )
