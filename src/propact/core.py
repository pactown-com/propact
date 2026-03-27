"""Core ToonPact class for Protocol Pact implementation."""

from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import asyncio
from dataclasses import dataclass, field
from enum import Enum

from .parser import MarkdownParser
from .attachments import AttachmentHandler


class ProtocolType(Enum):
    """Supported protocol types."""
    SHELL = "shell"
    MCP = "mcp"
    REST = "rest"
    WS = "ws"


@dataclass
class ProtocolBlock:
    """Represents a protocol block in markdown."""
    protocol: ProtocolType
    content: str
    attachments: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


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
