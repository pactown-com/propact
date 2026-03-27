"""Core ToonPact class for Protocol Pact implementation."""

from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import json

from propact.parser import MarkdownParser, ProtocolBlock, ProtocolType
from propact.attachments import AttachmentHandler


class ToonPact:
    """
    Main class for executing Protocol Pact documents.
    
    Handles markdown documents with protocol blocks for Shell, MCP, REST, and WebSocket.
    """
    
    def __init__(self, file_path: Union[str, Path]):
        """Initialize ToonPact with a markdown file."""
        self.file_path = Path(file_path)
        self.parser = MarkdownParser()
        self.attachment_handler = AttachmentHandler()
        self.blocks: List[ProtocolBlock] = []
        
    async def smart_send(self, base_url: str, openapi_spec: Optional[Dict[str, Any]] = None, 
                        openapi_path: Optional[str] = None, top_k: int = 3,
                        error_mode: str = "recover", max_retries: int = 3) -> Dict[str, Any]:
        """
        Send markdown content to the best-matched endpoint using semantic matching.
        
        Args:
            base_url: Base URL for the API
            openapi_spec: OpenAPI specification dictionary
            openapi_path: Path to OpenAPI spec file (JSON/YAML)
            top_k: Number of top matches to consider
            error_mode: Error handling mode (strict, recover, debug, interactive)
            max_retries: Maximum number of retries
            
        Returns:
            Dictionary with matches and execution results
        """
        from .matcher import create_matcher
        from .error_handler import PropactErrorHandler, ErrorMode, MatchError
        from rich.console import Console
        
        console = Console()
        
        # Load the markdown content
        if not self.blocks:
            await self.load()
        
        md_content = self.file_path.read_text()
        
        # Create error handler
        error_handler = PropactErrorHandler(
            mode=ErrorMode(error_mode),
            max_retries=max_retries
        )
        
        # Create matcher with error handler
        matcher = create_matcher(error_handler=error_handler)
        if not matcher:
            console.print("[red]Semantic matching not available. Install with: pip install propact[semantic][/red]")
            return {"error": "Semantic matching not available"}
        
        # Load OpenAPI spec
        spec = openapi_spec
        if openapi_path and not spec:
            if openapi_path.endswith('.json'):
                with open(openapi_path, 'r') as f:
                    spec = json.load(f)
            else:
                try:
                    from prance import ResolvingParser
                    parser = ResolvingParser(openapi_path)
                    spec = parser.specification
                except ImportError:
                    console.print("[red]YAML parsing requires prance. Install with: pip install propact[semantic][/red]")
                    return {"error": "YAML parsing not available"}
        
        if not spec:
            console.print("[red]No OpenAPI specification provided[/red]")
            return {"error": "No OpenAPI specification provided"}
        
        # Find matches with error recovery
        matches = await matcher.match(md_content, spec, top_k)
        
        if not matches:
            console.print("[yellow]No matching endpoints found[/yellow]")
            return {"error": "No matching endpoints found"}
        
        # Display matches
        console.print(f"\n[blue]🧠 Top {len(matches)} semantic matches:[/blue]")
        for i, match in enumerate(matches, 1):
            status = "🔄" if match.get("recovered") else "✓"
            console.print(f"  {i}. {status} {match['endpoint']} (score: {match['score']:.3f})")
        
        # Use the best match
        best_match = matches[0]
        console.print(f"\n[green]✓ Selected: {best_match['endpoint']}[/green]")
        
        # Create a REST block for the best match
        rest_content = f"""REST {best_match['method']} {best_match['path']}

Headers:
{json.dumps({"Content-Type": "application/json"}, indent=2)}

Payload:
{json.dumps({}, indent=2)}
"""
        
        rest_block = ProtocolBlock(
            protocol=ProtocolType.REST,
            content=rest_content
        )
        
        # Execute the REST block
        try:
            result = await self._execute_rest(rest_block)
            return {
                "matches": matches,
                "selected": best_match,
                "result": result
            }
        except Exception as e:
            # Try error recovery for execution errors
            error = MatchError(
                type="http_5xx",  # Generic execution error
                confidence=0.0,
                error_msg=str(e),
                candidates=matches,
                endpoint=best_match['endpoint']
            )
            
            recovered = await error_handler.handle_match_failure(
                error, md_content, spec
            )
            
            if recovered:
                console.print(f"[blue]🔄 Retrying with: {recovered}[/blue]")
                # In a full implementation, we would retry with the recovered endpoint
                # For now, just return the error
                return {
                    "matches": matches,
                    "selected": best_match,
                    "error": str(e),
                    "recovered": recovered
                }
            
            console.print(f"[red]Error executing request: {e}[/red]")
            return {
                "matches": matches,
                "selected": best_match,
                "error": str(e)
            }
        
    async def load(self) -> None:
        """Load and parse the markdown document."""
        content = self.file_path.read_text(encoding='utf-8')
        self.blocks = await self.parser.parse(content)
        
    async def execute(self, protocol: Optional[ProtocolType] = None) -> Dict[str, Any]:
        """
        Execute protocol blocks.
        
        Args:
            protocol: If specified, only execute blocks of this protocol type.
            
        Returns:
            Dictionary with execution results.
        """
        if not self.blocks:
            await self.load()
            
        results = {}
        
        for block in self.blocks:
            if protocol and block.protocol != protocol:
                continue
                
            if block.protocol == ProtocolType.SHELL:
                results[f"shell_{len(results)}"] = await self._execute_shell(block)
            elif block.protocol == ProtocolType.MCP:
                results[f"mcp_{len(results)}"] = await self._execute_mcp(block)
            elif block.protocol == ProtocolType.REST:
                results[f"rest_{len(results)}"] = await self._execute_rest(block)
            elif block.protocol == ProtocolType.WS:
                results[f"ws_{len(results)}"] = await self._execute_ws(block)
                
        return results
        
    async def _execute_shell(self, block: ProtocolBlock) -> Dict[str, Any]:
        """Execute shell protocol block."""
        import subprocess
        
        result = subprocess.run(
            block.content,
            shell=True,
            capture_output=True,
            text=True
        )
        
        return {
            "protocol": "shell",
            "command": block.content,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    async def _execute_mcp(self, block: ProtocolBlock) -> Dict[str, Any]:
        """Execute MCP protocol block."""
        # Placeholder for MCP execution
        return {
            "protocol": "mcp",
            "content": block.content,
            "status": "not_implemented"
        }
        
    async def _execute_rest(self, block: ProtocolBlock) -> Dict[str, Any]:
        """Execute REST protocol block."""
        # Placeholder for REST execution
        return {
            "protocol": "rest",
            "content": block.content,
            "status": "not_implemented"
        }
        
    async def _execute_ws(self, block: ProtocolBlock) -> Dict[str, Any]:
        """Execute WebSocket protocol block."""
        # Placeholder for WebSocket execution
        return {
            "protocol": "ws",
            "content": block.content,
            "status": "not_implemented"
        }
