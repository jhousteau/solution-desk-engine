"""CLI commands for solution-desk-engine."""

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="solution-desk-engine")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """A solution-desk-engine project created with Genesis"""
    ctx.ensure_object(dict)


@cli.command()
@click.option("--name", "-n", default="World", help="Name to greet")
@click.option("--count", "-c", default=1, help="Number of greetings")
def hello(name: str, count: int) -> None:
    """Say hello to someone."""
    for _ in range(count):
        console.print(f"Hello {name}! 👋")


@cli.command()
@click.argument("text")
@click.option(
    "--style",
    default="info",
    type=click.Choice(["info", "success", "warning", "error"]),
    help="Display style",
)
def display(text: str, style: str) -> None:
    """Display text with styling."""
    styles = {"info": "blue", "success": "green", "warning": "yellow", "error": "red"}

    panel = Panel(
        text,
        title=f"solution-desk-engine - {style.title()}",
        border_style=styles[style],
    )
    console.print(panel)


@cli.command()
def status() -> None:
    """Show application status."""
    console.print("✅ solution-desk-engine is running!")
    console.print("📦 Version: 0.1.0")
    console.print("🐍 Python CLI Tool")


if __name__ == "__main__":
    cli()
