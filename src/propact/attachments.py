"""Attachment handler for Protocol Pact binary data."""

import base64
import mimetypes
from pathlib import Path
from typing import Dict, Optional, Union
import asyncio


class AttachmentHandler:
    """Handles binary attachments in Protocol Pact documents."""
    
    def __init__(self):
        """Initialize the attachment handler."""
        self.attachments: Dict[str, bytes] = {}
        
    async def load_attachment(self, path: Union[str, Path]) -> bytes:
        """
        Load an attachment from file path.
        
        Args:
            path: Path to the attachment file.
            
        Returns:
            File content as bytes.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Attachment not found: {path}")
            
        return path.read_bytes()
        
    async def save_attachment(self, data: bytes, path: Union[str, Path]) -> None:
        """
        Save attachment data to file.
        
        Args:
            data: Binary data to save.
            path: Destination path.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        
    def encode_base64(self, data: bytes) -> str:
        """Encode binary data as base64 string."""
        return base64.b64encode(data).decode('utf-8')
        
    def decode_base64(self, encoded: str) -> bytes:
        """Decode base64 string to binary data."""
        return base64.b64decode(encoded.encode('utf-8'))
        
    def get_mime_type(self, path: Union[str, Path]) -> str:
        """Get MIME type for a file."""
        mime_type, _ = mimetypes.guess_type(str(path))
        return mime_type or 'application/octet-stream'
        
    async def extract_from_markdown(self, content: str, base_path: Optional[Path] = None) -> Dict[str, bytes]:
        """
        Extract all attachments from markdown content.
        
        Args:
            content: Markdown document content.
            base_path: Base path for resolving relative attachment paths.
            
        Returns:
            Dictionary mapping attachment paths to binary data.
        """
        import re
        
        pattern = r'!\[(.*?)\]\((.*?)\)'
        attachments = {}
        
        for match in re.finditer(pattern, content):
            attachment_path = match.group(2)
            
            # Skip data URLs and external URLs
            if attachment_path.startswith(('data:', 'http://', 'https://')):
                continue
                
            # Resolve relative path
            if base_path and not Path(attachment_path).is_absolute():
                full_path = base_path / attachment_path
            else:
                full_path = Path(attachment_path)
                
            try:
                data = await self.load_attachment(full_path)
                attachments[attachment_path] = data
            except FileNotFoundError:
                # Attachment not found, skip it
                pass
                
        return attachments
