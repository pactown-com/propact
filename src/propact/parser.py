"""Markdown parser for Protocol Pact documents."""

import re
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path

from .core import ProtocolBlock, ProtocolType


class MarkdownParser:
    """Parser for extracting protocol blocks from markdown documents."""
    
    def __init__(self):
        """Initialize the markdown parser."""
        self.protocol_pattern = re.compile(
            r'```propact:(shell|mcp|rest|ws)\n(.*?)\n```',
            re.DOTALL
        )
        self.attachment_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
        
    async def parse(self, content: str) -> List[ProtocolBlock]:
        """
        Parse markdown content and extract protocol blocks.
        
        Args:
            content: The markdown document content.
            
        Returns:
            List of ProtocolBlock objects.
        """
        blocks = []
        
        # Find all protocol blocks
        for match in self.protocol_pattern.finditer(content):
            protocol_str = match.group(1)
            block_content = match.group(2)
            
            # Convert protocol string to enum
            protocol = ProtocolType(protocol_str)
            
            # Extract attachments from the block content
            attachments = self._extract_attachments(block_content)
            
            # Extract metadata (if any)
            metadata = self._extract_metadata(block_content)
            
            block = ProtocolBlock(
                protocol=protocol,
                content=block_content.strip(),
                attachments=attachments,
                metadata=metadata
            )
            
            blocks.append(block)
            
        return blocks
        
    def _extract_attachments(self, content: str) -> List[str]:
        """Extract attachment references from block content."""
        attachments = []
        for match in self.attachment_pattern.finditer(content):
            attachments.append(match.group(2))  # URL/path
        return attachments
        
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from block content."""
        metadata = {}
        
        # Look for metadata lines at the beginning
        lines = content.split('\n')
        for line in lines:
            if ':' in line and not line.strip().startswith('#'):
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
            else:
                break
                
        return metadata
