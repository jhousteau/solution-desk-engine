"""CLI commands for solution-desk-engine."""

from typing import Optional

import click
from rich.console import Console

from .sow.sow_generator import SOWContext, SOWGenerator

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="solution-desk-engine")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Technical Sales Solutioning Framework - 11-Phase Methodology"""
    ctx.ensure_object(dict)


@cli.command()
def status() -> None:
    """Show framework status."""
    console.print("🔧 solution-desk-engine Framework")
    console.print("📦 Version: 0.1.0 (Framework Design Phase)")
    console.print("📋 11-Phase Technical Sales Methodology")
    console.print("")
    console.print("🚧 Core implementation coming soon...")
    console.print("📁 Export infrastructure ready")
    console.print("📄 Templates and documentation in development")


@cli.group()
def sow() -> None:
    """Statement of Work (SOW) generation commands."""
    pass


@sow.command()
@click.option(
    "--template-id", required=True, help="Google Drive file ID of the SOW template"
)
@click.option("--customer-name", required=True, help="Customer name (e.g., 'Penske')")
@click.option(
    "--project-name",
    required=True,
    help="Project name (e.g., 'Franchise Lease Management')",
)
@click.option("--output-name", help="Name for the generated SOW document")
@click.option(
    "--output-folder-id", help="Google Drive folder ID to save the generated SOW"
)
@click.option("--contractor-poc-name", help="Contractor point of contact name")
@click.option("--contractor-poc-email", help="Contractor point of contact email")
@click.option("--google-poc-name", help="Google point of contact name")
@click.option("--google-poc-email", help="Google point of contact email")
@click.option("--max-total-cost", help="Maximum total cost for the SOW")
def generate(
    template_id: str,
    customer_name: str,
    project_name: str,
    output_name: Optional[str],
    output_folder_id: Optional[str],
    contractor_poc_name: Optional[str],
    contractor_poc_email: Optional[str],
    google_poc_name: Optional[str],
    google_poc_email: Optional[str],
    max_total_cost: Optional[str],
) -> None:
    """Generate a SOW document from a Google Docs template."""
    try:
        console.print("🔨 Generating SOW document...")

        # Create SOW context
        context = SOWContext(
            customer_name=customer_name,
            project_name=project_name,
            contractor_poc_name=contractor_poc_name or "",
            contractor_poc_email=contractor_poc_email or "",
            google_poc_name=google_poc_name or "",
            google_poc_email=google_poc_email or "",
            max_total_cost=max_total_cost or "",
        )

        # Generate output name if not provided
        if not output_name:
            output_name = f"{customer_name} SOW - {project_name}"

        # Initialize generator and create SOW
        generator = SOWGenerator()

        console.print(f"📥 Downloading template: {template_id}")
        console.print("✏️  Processing template with customer data...")

        result = generator.generate_sow(
            template_file_id=template_id,
            context=context,
            output_name=output_name,
            output_folder_id=output_folder_id,
        )

        console.print("✅ SOW generated successfully!")
        console.print(f"📄 Document Name: {result['name']}")
        console.print(f"🔗 View Link: {result['web_view_link']}")
        console.print(f"🆔 Document ID: {result['id']}")

    except Exception as error:
        console.print(f"❌ Failed to generate SOW: {error}")
        raise click.ClickException(str(error))


@sow.command()
@click.option("--template-id", required=True, help="Google Drive file ID to validate")
def validate_template(template_id: str) -> None:
    """Validate a Google Docs template for SOW generation."""
    try:
        console.print(f"🔍 Validating template: {template_id}")

        generator = SOWGenerator()

        if generator.validate_template(template_id):
            template_info = generator.get_template_info(template_id)
            console.print("✅ Template is valid!")
            console.print(f"📄 Name: {template_info.get('name')}")
            console.print(f"📅 Modified: {template_info.get('modifiedTime')}")
            console.print(f"🔗 Link: {template_info.get('webViewLink')}")
        else:
            console.print("❌ Template is not valid or not accessible")
            console.print(
                "Make sure the file ID is correct and you have access to the document."
            )

    except Exception as error:
        console.print(f"❌ Failed to validate template: {error}")
        raise click.ClickException(str(error))


if __name__ == "__main__":
    cli()
