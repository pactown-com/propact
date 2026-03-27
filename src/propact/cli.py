"""Command-line interface for propact."""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Tuple

import click
from rich.console import Console
from rich.table import Table

from propact import ToonPact, ProtocolType
from propact.enhanced import Propact
from propact.config import get_server_config
from propact.dsl_converter import DSLConverter
from propact.uniconverter import UniConverter, EmailConfig


console = Console()


@click.group()
def cli():
    """Propact: Protocol Pact via Markdown."""
    pass


@cli.command(name="run")
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--protocol", "-p",
    type=click.Choice(["shell", "mcp", "rest", "ws"]),
    help="Execute only blocks of the specified protocol"
)
@click.option(
    "--endpoint", "-e",
    help="Target endpoint for sending content (e.g., https://api.example.com/upload, mcp://localhost/tool)"
)
@click.option(
    "--openapi",
    type=click.Path(exists=True),
    help="OpenAPI specification file for semantic endpoint matching"
)
@click.option(
    "--base-url",
    type=str,
    help="Base URL for semantic matching (use with --openapi)"
)
@click.option(
    "--openapi-llm-session",
    type=str,
    help="Session ID from openapi-llm browser extension"
)
@click.option(
    "--generate-spec",
    is_flag=True,
    help="Generate OpenAPI spec dynamically from URL"
)
@click.option(
    "--llm-key",
    type=str,
    help="OpenAI API key for dynamic spec generation"
)
@click.option(
    "--error-mode",
    type=click.Choice(["strict", "recover", "debug", "interactive"]),
    default="recover",
    help="Error handling mode: strict (fail fast), recover (auto-fix), debug (verbose), interactive (human-in-loop)"
)
@click.option(
    "--max-retries",
    type=int,
    default=3,
    help="Maximum number of retries for failed requests"
)
@click.option(
    "--schema", "-s",
    type=click.Path(exists=True, path_type=Path),
    help="Schema file for intelligent content splitting (OpenAPI JSON, CLI help text, etc.)"
)
@click.option(
    "--mode", "-m",
    type=click.Choice(["execute", "server"]),
    default="execute",
    help="Operation mode: execute (default) or server"
)
@click.option(
    "--port",
    type=int,
    default=None,  # Will use config default if None
    help="Port for server mode (default: from config)"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Parse and validate without executing"
)
@click.option(
    "--list", "-l",
    is_flag=True,
    help="List all protocol blocks without executing"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Show detailed output"
)
@click.option(
    "--llm-provider",
    type=click.Choice(["local", "cloud", "groq", "anthropic", "openrouter", "bedrock"]),
    default="local",
    help="LLM provider for query generation and error correction (local=ollama, cloud=openai, groq=fast, anthropic=accurate)"
)
@click.option(
    "--llm-model",
    type=str,
    help="Specific LLM model to use (e.g., ollama/llama3.2, openai/gpt-4o-mini, groq/llama3-70b)"
)
def main(file_path: Path, protocol: Optional[str], endpoint: Optional[str], 
         openapi: Optional[str], base_url: Optional[str], openapi_llm_session: Optional[str],
         generate_spec: bool, llm_key: Optional[str], error_mode: str, max_retries: int,
         schema: Optional[Path], mode: str, port: int, list: bool, verbose: bool, dry_run: bool,
         llm_provider: str, llm_model: Optional[str]) -> None:
    """
    Execute Protocol Pact documents.
    
    FILE_PATH: Path to the markdown file containing protocol blocks.
    """
    async def run():
        # Get server config for default port
        nonlocal port, protocol
        server_config = get_server_config()
        if port is None:
            port = server_config.port
            
        # Handle dry-run mode
        if dry_run:
            console.print("[blue]Dry run mode: Parsing and validating without execution[/blue]")
            
        # Show LLM configuration if using enhanced features
        if endpoint or schema or openapi:
            model_display = llm_model or llm_provider
            console.print(f"[blue]Using LLM provider: {model_display}[/blue]")
            pact = Propact(file_path, endpoint=endpoint, schema=str(schema) if schema else None)
        else:
            pact = ToonPact(file_path)
        
        # Always load to validate
        await pact.load()
        
        if dry_run:
            console.print("[green]✓ Markdown file parsed successfully[/green]")
            console.print(f"[blue]Found {len(pact.blocks)} protocol blocks[/blue]")
            
            # Show blocks summary
            from collections import Counter
            protocol_counts = Counter(block.protocol.value for block in pact.blocks)
            for protocol, count in protocol_counts.items():
                console.print(f"  - {protocol}: {count} block(s)")
            
            # Show attachments
            all_attachments = set()
            for block in pact.blocks:
                all_attachments.update(block.attachments)
            
            if all_attachments:
                console.print(f"[blue]Attachments:[/blue]")
                for attachment in sorted(all_attachments):
                    if Path(file_path.parent / attachment).exists():
                        console.print(f"  ✓ {attachment}")
                    else:
                        console.print(f"  ❌ {attachment} (missing)")
            else:
                console.print("[blue]No attachments found[/blue]")
            
            return
        
        if mode == "server":
            if hasattr(pact, 'server_mode'):
                await pact.server_mode(port=port)
            else:
                console.print("[red]Server mode requires enhanced Propact class. Use --endpoint or --schema.[/red]")
                return
        
        if list:
            await list_blocks(pact)
            return
            
        # If openapi-llm session is provided, fetch spec from openapi-llm
        elif openapi_llm_session:
            if not base_url:
                console.print("[red]Error: --base-url is required when using --openapi-llm-session[/red]")
                return
            
            try:
                from .importer import OpenAPILLMImporter
                spec_url = OpenAPILLMImporter.from_browser_session(openapi_llm_session)
                console.print(f"[blue]Fetching spec from openapi-llm session: {openapi_llm_session}[/blue]")
                
                # For now, we'll need to download the spec locally
                # In a full implementation, we'd use httpx to fetch it
                console.print("[yellow]Note: Please download the spec from the URL and use --openapi[/yellow]")
                console.print(f"[yellow]Spec URL: {spec_url}[/yellow]")
                return
            except ImportError as e:
                console.print(f"[red]Error: {e}[/red]")
                return
        
        # If generate-spec is requested, generate spec dynamically
        elif generate_spec:
            if not base_url:
                console.print("[red]Error: --base-url is required when using --generate-spec[/red]")
                return
            
            if not llm_key:
                console.print("[red]Error: --llm-key is required for dynamic spec generation[/red]")
                return
            
            console.print(f"[blue]Generating OpenAPI spec for: {base_url}[/blue]")
            console.print("[yellow]Dynamic spec generation not yet implemented[/yellow]")
            return
            
        # If openapi is provided, use semantic matching
        elif openapi:
            if not base_url:
                console.print("[red]Error: --base-url is required when using --openapi[/red]")
                return
                
            if hasattr(pact, 'smart_send'):
                console.print(f"[blue]Using semantic matching with: {openapi}[/blue]")
                result = await pact.smart_send(
                    base_url=base_url, 
                    openapi_path=openapi,
                    error_mode=error_mode,
                    max_retries=max_retries
                )
                
                if "error" in result:
                    console.print(f"[red]Error: {result['error']}[/red]")
                else:
                    if "result" in result and "markdown_file" in result["result"]:
                        console.print(f"[green]✓ Response saved to: {result['result']['markdown_file']}[/green]")
            else:
                console.print("[red]Semantic matching requires enhanced Propact class[/red]")
                return
                    
        # If endpoint is provided, send to endpoint
        elif endpoint:
            if hasattr(pact, 'send_to_endpoint'):
                console.print(f"[blue]Sending to endpoint: {endpoint}[/blue]")
                result = await pact.send_to_endpoint(endpoint)
                
                if "error" in result:
                    console.print(f"[red]Error: {result['error']}[/red]")
                else:
                    console.print(f"[green]✓ Response saved to: {result['markdown_file']}[/green]")
                    
                    if verbose:
                        console.print("\n[bold]Extracted Content:[/bold]")
                        console.print(f"Files: {list(result['extracted_content'].media.keys())}")
                        console.print(f"Data: {list(result['extracted_content'].codeblocks.keys())}")
                        console.print(f"Text length: {len(result['extracted_content'].plain_text)}")
            else:
                console.print("[red]Endpoint sending requires enhanced Propact class. Use --endpoint or --schema.[/red]")
                return
            
        # Default protocol execution
        if protocol:
            protocol_type = ProtocolType(protocol)
            results = await pact.execute(protocol=protocol_type)
            display_results(results, verbose)
        
    try:
        asyncio.run(run())
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


async def list_blocks(pact: ToonPact) -> None:
    """List all protocol blocks in the document."""
    await pact.load()
    
    table = Table(title="Protocol Blocks")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Content Preview", style="magenta")
    table.add_column("Attachments", style="green")
    
    for i, block in enumerate(pact.blocks):
        content_preview = block.content[:50] + "..." if len(block.content) > 50 else block.content
        attachments = ", ".join(block.attachments) if block.attachments else "None"
        
        table.add_row(
            block.protocol.value,
            content_preview,
            attachments
        )
    
    console.print(table)


def display_results(results: dict, verbose: bool) -> None:
    """Display execution results."""
    table = Table(title="Execution Results")
    table.add_column("Block", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Output", style="white")
    
    for block_name, result in results.items():
        if result.get("success", True):
            status = "[green]✓ Success[/green]"
        else:
            status = "[red]✗ Failed[/red]"
            
        output = ""
        if verbose:
            if "stdout" in result:
                output += f"STDOUT: {result['stdout']}\n"
            if "stderr" in result and result['stderr']:
                output += f"STDERR: {result['stderr']}\n"
            if "error" in result:
                output += f"ERROR: {result['error']}"
        else:
            if "stdout" in result:
                output = f"{result['stdout'][:100]}..." if len(result['stdout']) > 100 else result['stdout']
            elif "error" in result:
                output = f"{result['error'][:100]}..." if len(result['error']) > 100 else result['error']
                
        table.add_row(block_name, status, output)
    
    console.print(table)


if __name__ == "__main__":
    cli()


@cli.group()
def convert():
    """Convert between different formats (SQL, GraphQL, YAML, CSV, XML)."""
    pass


@convert.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option("--from", "from_format", required=True, 
              type=click.Choice(["sql", "graphql", "yaml", "csv", "xml", "markdown"]),
              help="Input format")
@click.option("--to", "to_format", required=True,
              type=click.Choice(["sql", "graphql", "yaml", "csv", "xml", "markdown"]),
              help="Output format")
@click.option("--output", "-o", type=click.Path(path_type=Path),
              help="Output file (default: stdout)")
@click.option("--dialect", default="postgres",
              type=click.Choice(["postgres", "mysql", "sqlite", "snowflake", "bigquery"]),
              help="SQL dialect (for SQL conversions)")
@click.option("--table-name", default="generated_table",
              help="Table name for SQL INSERT/UPDATE")
@click.option("--operation", default="INSERT",
              type=click.Choice(["INSERT", "UPDATE"]),
              help="SQL operation type")
@click.option("--api-type", help="API type for GraphQL (github, stripe, generic)")
@click.option("--db-connection", help="Database connection string for SQL queries")
def file(input_file: Path, from_format: str, to_format: str, output: Optional[Path],
         dialect: str, table_name: str, operation: str, api_type: Optional[str],
         db_connection: Optional[str]):
    """Convert a file from one format to another."""
    try:
        # Read input file
        content = input_file.read_text(encoding='utf-8')
        
        # Initialize converter
        converter = DSLConverter()
        
        # Prepare conversion options
        kwargs = {}
        if from_format == "markdown" and to_format == "sql":
            kwargs.update({"dialect": dialect, "table_name": table_name, "operation": operation})
        elif from_format == "sql" and to_format == "markdown":
            if db_connection:
                kwargs["db_connection"] = db_connection
        elif from_format == "markdown" and to_format == "graphql":
            if api_type:
                kwargs["api_type"] = api_type
        
        # Perform conversion
        result = converter.convert(content, from_format, to_format, **kwargs)
        
        if result.success:
            # Output result
            if output:
                output.write_text(result.content, encoding='utf-8')
                console.print(f"[green]✓ Converted {from_format} → {to_format}[/green]")
                console.print(f"[blue]Output saved to: {output}[/blue]")
            else:
                console.print(result.content)
            
            # Show warnings if any
            if result.warnings:
                for warning in result.warnings:
                    console.print(f"[yellow]Warning: {warning}[/yellow]")
        else:
            console.print("[red]Conversion failed:[/red]")
            for error in result.errors:
                console.print(f"[red]  • {error}[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@convert.command()
@click.argument("content", type=str)
@click.option("--from", "from_format", required=True,
              type=click.Choice(["sql", "graphql", "yaml", "csv", "xml", "markdown"]),
              help="Input format")
@click.option("--to", "to_format", required=True,
              type=click.Choice(["sql", "graphql", "yaml", "csv", "xml", "markdown"]),
              help="Output format")
@click.option("--dialect", default="postgres",
              type=click.Choice(["postgres", "mysql", "sqlite", "snowflake", "bigquery"]),
              help="SQL dialect (for SQL conversions)")
@click.option("--table-name", default="generated_table",
              help="Table name for SQL INSERT/UPDATE")
@click.option("--operation", default="INSERT",
              type=click.Choice(["INSERT", "UPDATE"]),
              help="SQL operation type")
@click.option("--api-type", help="API type for GraphQL (github, stripe, generic)")
def string(content: str, from_format: str, to_format: str, dialect: str,
           table_name: str, operation: str, api_type: Optional[str]):
    """Convert a string from one format to another."""
    try:
        # Initialize converter
        converter = DSLConverter()
        
        # Prepare conversion options
        kwargs = {}
        if from_format == "markdown" and to_format == "sql":
            kwargs.update({"dialect": dialect, "table_name": table_name, "operation": operation})
        elif from_format == "markdown" and to_format == "graphql":
            if api_type:
                kwargs["api_type"] = api_type
        
        # Perform conversion
        result = converter.convert(content, from_format, to_format, **kwargs)
        
        if result.success:
            console.print(result.content)
            
            # Show warnings if any
            if result.warnings:
                for warning in result.warnings:
                    console.print(f"[yellow]Warning: {warning}[/yellow]")
        else:
            console.print("[red]Conversion failed:[/red]")
            for error in result.errors:
                console.print(f"[red]  • {error}[/red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@convert.command()
def formats():
    """List all supported formats."""
    converter = DSLConverter()
    formats_list = converter.list_formats()
    
    table = Table(title="Supported Formats")
    table.add_column("Format", style="cyan")
    table.add_column("Description", style="white")
    
    descriptions = {
        "markdown": "Markdown tables and structured content",
        "sql": "SQL queries and INSERT/UPDATE statements",
        "graphql": "GraphQL queries and schemas",
        "yaml": "YAML configuration and data",
        "csv": "Comma-separated values",
        "xml": "XML documents"
    }
    
    for fmt in sorted(formats_list):
        desc = descriptions.get(fmt, "Format converter")
        table.add_row(fmt, desc)
    
    console.print(table)


@cli.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.option("--to-md", is_flag=True, help="Convert to Markdown")
@click.option("--to-pdf", type=click.Path(path_type=Path), help="Convert to PDF")
@click.option("--to-docx", type=click.Path(path_type=Path), help="Convert to DOCX")
@click.option("--to-pptx", type=click.Path(path_type=Path), help="Convert to PPTX")
@click.option("--to-xlsx", type=click.Path(path_type=Path), help="Convert to XLSX")
@click.option("--to-html", type=click.Path(path_type=Path), help="Convert to HTML")
@click.option("--to-email", type=click.Path(path_type=Path), help="Convert to EML file")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file (auto-detect format)")
def universal(input_path: Path, to_md: bool, to_pdf: Optional[Path], 
              to_docx: Optional[Path], to_pptx: Optional[Path], 
              to_xlsx: Optional[Path], to_html: Optional[Path],
              to_email: Optional[Path], output: Optional[Path]):
    """Universal document converter (PDF, DOCX, PPTX, XLSX, HTML, Email ↔ MD)."""
    try:
        converter = UniConverter()
        
        # Determine conversion type
        if to_md:
            # Convert to Markdown
            result = converter.to_markdown(input_path)
            if result.success:
                if output:
                    output.write_text(result.content, encoding='utf-8')
                    console.print(f"[green]✓ Converted to Markdown: {output}[/green]")
                else:
                    console.print(result.content)
            else:
                console.print("[red]Conversion failed:[/red]")
                for error in result.errors:
                    console.print(f"[red]  • {error}[/red]")
        
        elif output or any([to_pdf, to_docx, to_pptx, to_xlsx, to_html, to_email]):
            # Convert from Markdown
            md_content = input_path.read_text(encoding='utf-8')
            
            # Determine output format and path
            if output:
                result = converter.from_markdown(md_content, output)
            elif to_pdf:
                result = converter.from_markdown(md_content, to_pdf)
            elif to_docx:
                result = converter.from_markdown(md_content, to_docx)
            elif to_pptx:
                result = converter.from_markdown(md_content, to_pptx)
            elif to_xlsx:
                result = converter.from_markdown(md_content, to_xlsx)
            elif to_html:
                result = converter.from_markdown(md_content, to_html)
            elif to_email:
                result = converter.from_markdown(md_content, to_email)
            else:
                console.print("[red]Error: No output format specified[/red]")
                return
            
            if result.success:
                console.print(f"[green]✓ Conversion successful: {result.output_path}[/green]")
            else:
                console.print("[red]Conversion failed:[/red]")
                for error in result.errors:
                    console.print(f"[red]  • {error}[/red]")
        
        else:
            console.print("[red]Error: No conversion direction specified[/red]")
            console.print("Use --to-md to convert to Markdown or specify output format")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.argument("markdown_file", type=click.Path(exists=True, path_type=Path))
@click.option("--to", "to_emails", required=True, help="Recipient email(s), comma-separated")
@click.option("--subject", default="Propact Document", help="Email subject")
@click.option("--smtp-host", required=True, help="SMTP server host")
@click.option("--smtp-port", default=587, type=int, help="SMTP server port")
@click.option("--smtp-user", required=True, help="SMTP username")
@click.option("--smtp-password", required=True, help="SMTP password")
@click.option("--from", "from_email", help="From email (default: SMTP username)")
@click.option("--attach", multiple=True, type=click.Path(exists=True, path_type=Path),
              help="Attach files (can be used multiple times)")
def send_email(markdown_file: Path, to_emails: str, subject: str,
               smtp_host: str, smtp_port: int, smtp_user: str, 
               smtp_password: str, from_email: Optional[str],
               attach: Tuple[Path, ...]):
    """Send Markdown as rich HTML email."""
    try:
        # Read markdown content
        md_content = markdown_file.read_text(encoding='utf-8')
        
        # Configure email
        config = EmailConfig(
            host=smtp_host,
            port=smtp_port,
            username=smtp_user,
            password=smtp_password,
            from_email=from_email
        )
        
        # Parse recipients
        recipients = [email.strip() for email in to_emails.split(',')]
        
        # Send email
        converter = UniConverter()
        result = converter.send_email(
            md_content, 
            recipients, 
            subject, 
            config,
            list(attach) if attach else None
        )
        
        if result.success:
            console.print(f"[green]✓ Email sent to {len(recipients)} recipient(s)[/green]")
        else:
            console.print("[red]Failed to send email:[/red]")
            for error in result.errors:
                console.print(f"[red]  • {error}[/red]")
                
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--to-md", is_flag=True, help="Convert all files to Markdown")
@click.option("--output-dir", type=click.Path(path_type=Path), help="Output directory")
@click.option("--pattern", default="*", help="File pattern (e.g., '*.docx')")
def batch(directory: Path, to_md: bool, output_dir: Optional[Path], pattern: str):
    """Batch convert files in a directory."""
    try:
        converter = UniConverter()
        
        # Find files
        files = list(directory.glob(pattern))
        
        if not files:
            console.print(f"[yellow]No files found matching pattern: {pattern}[/yellow]")
            return
        
        # Set output directory
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
        
        console.print(f"[blue]Found {len(files)} files to convert[/blue]")
        
        success_count = 0
        for file_path in files:
            console.print(f"  Processing: {file_path.name}")
            
            if to_md:
                result = converter.to_markdown(file_path)
                if result.success:
                    if output_dir:
                        output_file = output_dir / f"{file_path.stem}.md"
                        output_file.write_text(result.content, encoding='utf-8')
                    success_count += 1
                else:
                    console.print(f"    [red]Failed: {result.errors[0]}[/red]")
        
        console.print(f"[green]✓ Converted {success_count}/{len(files)} files[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
