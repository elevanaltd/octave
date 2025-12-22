"""CLI entry point for OCTAVE tools.

Stub for P1.7: cli_implementation
"""

import click


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """OCTAVE command-line tools."""
    pass


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--schema", help="Schema name for validation")
@click.option("--fix", is_flag=True, help="Apply TIER_REPAIR fixes")
@click.option("--verbose", is_flag=True, help="Show pipeline stages")
def ingest(file: str, schema: str | None, fix: bool, verbose: bool):
    """Ingest lenient OCTAVE and emit canonical."""
    from octave_mcp.core.emitter import emit
    from octave_mcp.core.parser import parse

    with open(file) as f:
        content = f.read()

    try:
        doc = parse(content)
        canonical = emit(doc)
        click.echo(canonical)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--schema", help="Schema name for validation")
@click.option("--mode", type=click.Choice(["canonical", "authoring", "executive", "developer"]), default="canonical")
def eject(file: str, schema: str | None, mode: str):
    """Eject OCTAVE to projected format."""
    from octave_mcp.core.emitter import emit
    from octave_mcp.core.parser import parse

    with open(file) as f:
        content = f.read()

    try:
        doc = parse(content)
        output = emit(doc)  # For now, just emit canonical
        click.echo(output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--schema", help="Schema name for validation")
@click.option("--strict", is_flag=True, help="Strict mode (reject unknown fields)")
def validate(file: str, schema: str | None, strict: bool):
    """Validate OCTAVE against schema."""
    from octave_mcp.core.parser import parse
    from octave_mcp.core.validator import validate as validate_doc

    with open(file) as f:
        content = f.read()

    try:
        doc = parse(content)
        errors = validate_doc(doc, strict=strict)

        if errors:
            for error in errors:
                click.echo(f"{error.code}: {error.message}", err=True)
            raise click.Abort()
        else:
            click.echo("Valid")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e


if __name__ == "__main__":
    cli()
