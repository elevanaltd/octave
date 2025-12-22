"""Tests for CLI (P1.7)."""

from click.testing import CliRunner

from octave_mcp.cli.main import cli


class TestCLI:
    """Test CLI commands."""

    def test_cli_help(self):
        """Should show help message."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "OCTAVE command-line tools" in result.output
