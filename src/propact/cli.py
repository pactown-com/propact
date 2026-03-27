"""Command-line interface for propact."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from propact import ToonPact, ProtocolType
from propact.enhanced import Propact
from propact.core import ProtocolBlock


console = Console()


@click.command()
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
    default=8080,
    help="Port for server mode (default: 8080)"
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
def main(file_path: Path, protocol: Optional[str], endpoint: Optional[str], 
         schema: Optional[Path], mode: str, port: int, list: bool, verbose: bool) -> None:
    """
    Execute Protocol Pact documents.
    
    FILE_PATH: Path to the markdown file containing protocol blocks.
    """
    async def run():
        # Use enhanced Propact if endpoint or schema is provided
        if endpoint or schema:
            pact = Propact(file_path, endpoint=endpoint, schema=str(schema) if schema else None)
        else:
            pact = ToonPact(file_path)
        
        if mode == "server":
            if hasattr(pact, 'server_mode'):
                await pact.server_mode(port=port)
            else:
                console.print("[red]Server mode requires enhanced Propact class. Use --endpoint or --schema.[/red]")
                return
        
        if list:
            await list_blocks(pact)
            return
            
        # If endpoint is provided, send to endpoint
        if endpoint:
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
        protocol_type = ProtocolType(protocol) if protocol else None
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
                output = result['stdout'][:100] + "..." if len(result['stdout']) > 100 else result['stdout']
            elif "error" in result:
                output = result['error'][:100] + "..." if len(result['error']) > 100 else result['error']
                
        table.add_row(block_name, status, output)
    
    console.print(table)


if __name__ == "__main__":
    main()
