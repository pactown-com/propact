"""Enhanced Propact class with schema introspection and smart split capabilities."""

import re
import json
import subprocess
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import asyncio
from dataclasses import dataclass

try:
    import prance
    HAS_PRANCE = True
except ImportError:
    HAS_PRANCE = False

from .core import ToonPact
from .parser import MarkdownParser, ProtocolBlock, ProtocolType
from .attachments import AttachmentHandler
from .converter import MDConverter, ExtractedContent
from .adapters import get_protocol_adapter, PROTOCOL_ADAPTERS


@dataclass
class SplitContent:
    """Represents split content ready for transport."""
    files: Dict[str, bytes] = None
    json_data: Dict[str, Any] = None
    text: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.files is None:
            self.files = {}
        if self.json_data is None:
            self.json_data = {}
        if self.metadata is None:
            self.metadata = {}


class Propact(ToonPact):
    """
    Enhanced Propact class with schema introspection and intelligent content splitting.
    
    Capable of parsing schemas (OpenAPI, CLI, MCP) and intelligently splitting markdown
    content into appropriate payloads for different endpoints.
    """
    
    def __init__(self, file_path: Union[str, Path], endpoint: str = None, schema: str = None):
        """Initialize Propact with enhanced capabilities."""
        super().__init__(file_path)
        self.endpoint = endpoint
        self.schema_path = schema
        self.schema = self._introspect_schema(schema) if schema else {"generic": "multipart/form-data"}
        self.raw_content = self.file_path.read_text(encoding='utf-8')
        
    def _introspect_schema(self, schema_path: str) -> Dict[str, Any]:
        """Introspect schema from file (OpenAPI, CLI, etc.)."""
        if not schema_path:
            return {"generic": "multipart/form-data"}
            
        schema_file = Path(schema_path)
        
        if not schema_file.exists():
            return {"error": f"Schema file not found: {schema_path}"}
            
        if schema_path.endswith('.json'):
            # OpenAPI schema
            if HAS_PRANCE:
                try:
                    parser = prance.ResolvingParser(schema_path)
                    return parser.specification
                except Exception as e:
                    return {"error": f"Failed to parse OpenAPI schema: {e}"}
            else:
                # Fallback: load as JSON
                try:
                    with open(schema_path, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    return {"error": f"Failed to parse JSON schema: {e}"}
                    
        elif schema_path.endswith('.txt') or schema_path.endswith('.md'):
            # CLI help text
            try:
                with open(schema_path, 'r') as f:
                    help_text = f.read()
                return {"shell": {"help": help_text, "type": "cli"}}
            except Exception as e:
                return {"error": f"Failed to read CLI schema: {e}"}
                
        elif schema_path.endswith('.yaml') or schema_path.endswith('.yml'):
            # YAML schema (could be OpenAPI or MCP)
            try:
                import yaml
                with open(schema_path, 'r') as f:
                    return yaml.safe_load(f)
            except ImportError:
                return {"error": "PyYAML required for YAML schemas"}
            except Exception as e:
                return {"error": f"Failed to parse YAML schema: {e}"}
                
        return {"generic": "multipart/form-data"}
    
    def _smart_split_md(self, content: str, schema: Dict[str, Any]) -> ExtractedContent:
        """
        Intelligently split markdown content based on schema requirements.
        
        Uses MDConverter for consistent extraction and preparation.
        """
        # Extract content using converter
        extracted = MDConverter.extract_from_markdown(content)
        
        # Prepare payload based on schema
        payload = MDConverter.prepare_payload(extracted, schema)
        
        # Update metadata
        extracted.metadata.update({
            "schema_type": self._detect_schema_type(schema),
            "payload_structure": list(payload.keys())
        })
        
        return extracted
    
    def _detect_schema_type(self, schema: Dict[str, Any]) -> str:
        """Detect the type of schema."""
        if "paths" in schema or "openapi" in schema:
            return "openapi"
        elif "shell" in schema:
            return "shell"
        elif "mcp" in str(schema).lower():
            return "mcp"
        return "generic"
    
    def _adapt_to_openapi(self, content: SplitContent, schema: Dict[str, Any]) -> SplitContent:
        """Adapt content to OpenAPI schema requirements."""
        # Find matching endpoint based on content
        if "paths" in schema:
            # Simple heuristic: look for upload/analyze endpoints
            for path, methods in schema["paths"].items():
                if "post" in methods:
                    post_spec = methods["post"]
                    if "requestBody" in post_spec:
                        # Check if it expects multipart
                        content_type = post_spec["requestBody"].get("content", {})
                        if "multipart/form-data" in content_type:
                            content.metadata["endpoint"] = path
                            content.metadata["method"] = "POST"
                            content.metadata["content_type"] = "multipart/form-data"
                            break
        
        return content
    
    def _adapt_to_shell(self, content: SplitContent, schema: Dict[str, Any]) -> SplitContent:
        """Adapt content for shell/CLI commands."""
        content.metadata["format"] = "multipart"
        content.metadata["binary_flag"] = "--data-binary"
        content.metadata["text_flag"] = "--data"
        return content
    
    def _adapt_to_mcp(self, content: SplitContent, schema: Dict[str, Any]) -> SplitContent:
        """Adapt content for MCP protocol."""
        content.metadata["protocol"] = "mcp"
        content.metadata["attachments_as_resources"] = True
        return content
    
    def _get_mime_type(self, file_path: Path) -> str:
        """Get MIME type for a file."""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or "application/octet-stream"
    
    async def send_to_endpoint(self, endpoint: str = None) -> Dict[str, Any]:
        """
        Send split markdown content to endpoint and convert response to markdown.
        
        Args:
            endpoint: Target endpoint URL/command
            
        Returns:
            Response information and generated markdown
        """
        endpoint = endpoint or self.endpoint
        if not endpoint:
            return {"error": "No endpoint specified"}
        
        # Split content according to schema
        extracted = self._smart_split_md(self.raw_content, self.schema)
        
        # Prepare payload using converter
        payload = MDConverter.prepare_payload(extracted, self.schema)
        
        # Determine protocol and send
        response = None
        
        if endpoint.startswith(("http://", "https://")):
            response = await self._send_rest(endpoint, payload)
        elif endpoint.startswith("mcp://"):
            response = await self._send_mcp(endpoint, payload)
        elif endpoint.startswith(("ws://", "wss://")):
            response = await self._send_ws(endpoint, payload)
        elif endpoint.startswith("grpc://"):
            protocol = "grpc"
            adapter = get_protocol_adapter(protocol, endpoint)
            if adapter.is_available():
                response = await adapter.send(payload)
            else:
                response = {"error": f"Protocol {protocol} not available. Install with: pip install propact[grpc]"}
        elif endpoint.startswith(("gql://", "graphql://")):
            protocol = "gql"
            adapter = get_protocol_adapter(protocol, endpoint)
            if adapter.is_available():
                response = await adapter.send(payload)
            else:
                response = {"error": f"Protocol {protocol} not available. Install with: pip install propact[graphql]"}
        elif endpoint.startswith("mqtt://"):
            protocol = "mqtt"
            adapter = get_protocol_adapter(protocol, endpoint)
            if adapter.is_available():
                response = await adapter.send(payload)
            else:
                response = {"error": f"Protocol {protocol} not available. Install with: pip install propact[mqtt]"}
        elif endpoint.startswith(("soap://", "wsdl://")):
            protocol = "soap"
            adapter = get_protocol_adapter(protocol, endpoint, wsdl=endpoint)
            if adapter.is_available():
                response = await adapter.send(payload)
            else:
                response = {"error": f"Protocol {protocol} not available. Install with: pip install propact[soap]"}
        elif endpoint.startswith("smtp://"):
            protocol = "smtp"
            adapter = get_protocol_adapter(protocol, endpoint)
            response = await adapter.send(payload)
        else:
            # Assume shell command
            response = await self._send_shell(endpoint, payload)
        
        # Convert response to markdown using converter
        if response:
            content_type = response.get("headers", {}).get("content-type", "text/plain")
            response_md = MDConverter.response_to_markdown(
                response.get("data") or response.get("response") or response.get("stdout", ""),
                content_type,
                response.get("headers", {})
            )
            
            # Add error information if present
            if "error" in response:
                response_md += f"\n\n**Error:** {response['error']}"
            
            # Add metadata
            if "metadata" in response:
                response_md += f"\n\n**Metadata:**\n```json\n{json.dumps(response['metadata'], indent=2)}\n```"
        else:
            response_md = "# Empty Response\n\nNo data received from endpoint."
        
        # Save response markdown
        output_path = self.file_path.with_suffix('.response.md')
        output_path.write_text(response_md, encoding='utf-8')
        
        return {
            "response": response,
            "markdown_file": str(output_path),
            "extracted_content": extracted,
            "payload": payload
        }
    
    async def _send_rest(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send content via REST API."""
        import httpx
        
        # Prepare multipart form data
        files = {}
        data = {}
        
        # Add files if present
        if "files" in payload:
            for name, file_data in payload["files"].items():
                files[name] = (f"{name}.bin", file_data, "application/octet-stream")
        
        # Add data fields
        if "fields" in payload:
            for key, value in payload["fields"].items():
                if isinstance(value, (dict, list)):
                    data[key] = json.dumps(value)
                else:
                    data[key] = str(value)
        elif "data" in payload:
            for key, value in payload["data"].items():
                if isinstance(value, (dict, list)):
                    data[key] = json.dumps(value)
                else:
                    data[key] = str(value)
        
        # Add text
        if "text" in payload and payload["text"]:
            data["text"] = payload["text"]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, files=files, data=data)
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "json": response.json() if response.headers.get("content-type", "").startswith("application/json") else None
            }
    
    async def _send_mcp(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send content via MCP protocol."""
        # Placeholder for MCP implementation
        return {
            "protocol": "mcp",
            "endpoint": endpoint,
            "status": "not_implemented",
            "content_preview": {
                "files": list(payload.get("files", {}).keys()),
                "data_keys": list(payload.get("data", {}).keys()),
                "text_length": len(payload.get("text", ""))
            }
        }
    
    async def _send_ws(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send content via WebSocket."""
        # Placeholder for WebSocket implementation
        return {
            "protocol": "websocket",
            "endpoint": endpoint,
            "status": "not_implemented",
            "content_preview": {
                "files": list(payload.get("files", {}).keys()),
                "data_keys": list(payload.get("data", {}).keys()),
                "text_length": len(payload.get("text", ""))
            }
        }
    
    async def _send_shell(self, command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send content via shell command."""
        # Build command with content
        full_command = command
        
        # Add files as --data-binary
        if "files" in payload:
            for name in payload["files"]:
                if "--data-binary" not in full_command:
                    full_command += f" --data-binary {name}"
        
        # Add text as --data
        if "text" in payload and payload["text"] and "--data" not in full_command:
            # Escape and quote the text
            escaped_text = payload["text"].replace('"', '\\"')
            full_command += f' --data "{escaped_text}"'
        
        # Execute in directory with files
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=self.file_path.parent
        )
        
        return {
            "command": full_command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    def _response_to_md(self, response: Dict[str, Any]) -> str:
        """Convert response to markdown format."""
        md_lines = ["# Response from Propact\n"]
        
        if "status_code" in response:
            md_lines.append(f"**Status:** {response['status_code']}\n")
        
        if "json" in response and response["json"]:
            md_lines.append("## JSON Response\n")
            md_lines.append("```json\n")
            md_lines.append(json.dumps(response["json"], indent=2))
            md_lines.append("\n```\n")
        
        if "content" in response and response["content"]:
            md_lines.append("## Raw Response\n")
            md_lines.append("```\n")
            md_lines.append(response["content"][:1000] + "..." if len(response["content"]) > 1000 else response["content"])
            md_lines.append("\n```\n")
        
        if "stdout" in response and response["stdout"]:
            md_lines.append("## Command Output\n")
            md_lines.append("```bash\n")
            md_lines.append(response["stdout"])
            md_lines.append("\n```\n")
        
        if "stderr" in response and response["stderr"]:
            md_lines.append("## Errors\n")
            md_lines.append("```bash\n")
            md_lines.append(response["stderr"])
            md_lines.append("\n```\n")
        
        return "\n".join(md_lines)
    
    async def server_mode(self, port: int = 8080) -> None:
        """
        Run in server mode - markdown file acts as a server.
        
        Updates the markdown file with each request.
        """
        # Placeholder for server mode implementation
        print(f"Server mode not yet implemented - would serve on port {port}")
        print("Markdown file would be updated with each request")
