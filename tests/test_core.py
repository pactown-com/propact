"""Test suite for propact package."""

import pytest
import asyncio
from pathlib import Path

from propact import ToonPact, ProtocolType
from propact.core import ProtocolBlock
from propact.parser import MarkdownParser
from propact.attachments import AttachmentHandler


@pytest.fixture
def sample_markdown():
    """Sample markdown content with protocol blocks."""
    return """
# Test Document

Some text here.

```propact:shell
echo "Hello from shell!"
ls -la
```

More text.

```propact:mcp
{
  "method": "tools/call",
  "params": {
    "name": "example_tool",
    "arguments": {"input": "test"}
  }
}
```

```propact:rest
GET https://api.example.com/data
Content-Type: application/json
```

```propact:ws
{
  "type": "subscribe",
  "channel": "updates"
}
```
"""


@pytest.fixture
def parser():
    """Create a MarkdownParser instance."""
    return MarkdownParser()


@pytest.fixture
def attachment_handler():
    """Create an AttachmentHandler instance."""
    return AttachmentHandler()


class TestMarkdownParser:
    """Test cases for MarkdownParser."""
    
    @pytest.mark.asyncio
    async def test_parse_shell_block(self, parser, sample_markdown):
        """Test parsing shell protocol blocks."""
        blocks = await parser.parse(sample_markdown)
        shell_blocks = [b for b in blocks if b.protocol == ProtocolType.SHELL]
        
        assert len(shell_blocks) == 1
        assert 'echo "Hello from shell!"' in shell_blocks[0].content
        assert 'ls -la' in shell_blocks[0].content
        
    @pytest.mark.asyncio
    async def test_parse_mcp_block(self, parser, sample_markdown):
        """Test parsing MCP protocol blocks."""
        blocks = await parser.parse(sample_markdown)
        mcp_blocks = [b for b in blocks if b.protocol == ProtocolType.MCP]
        
        assert len(mcp_blocks) == 1
        assert '"method": "tools/call"' in mcp_blocks[0].content
        
    @pytest.mark.asyncio
    async def test_parse_rest_block(self, parser, sample_markdown):
        """Test parsing REST protocol blocks."""
        blocks = await parser.parse(sample_markdown)
        rest_blocks = [b for b in blocks if b.protocol == ProtocolType.REST]
        
        assert len(rest_blocks) == 1
        assert 'https://api.example.com/data' in rest_blocks[0].content
        
    @pytest.mark.asyncio
    async def test_parse_ws_block(self, parser, sample_markdown):
        """Test parsing WebSocket protocol blocks."""
        blocks = await parser.parse(sample_markdown)
        ws_blocks = [b for b in blocks if b.protocol == ProtocolType.WS]
        
        assert len(ws_blocks) == 1
        assert '"channel": "updates"' in ws_blocks[0].content
        
    @pytest.mark.asyncio
    async def test_parse_empty_content(self, parser):
        """Test parsing empty markdown content."""
        blocks = await parser.parse("")
        assert len(blocks) == 0


class TestAttachmentHandler:
    """Test cases for AttachmentHandler."""
    
    def test_encode_decode_base64(self, attachment_handler):
        """Test base64 encoding and decoding."""
        original_data = b"Hello, World!"
        encoded = attachment_handler.encode_base64(original_data)
        decoded = attachment_handler.decode_base64(encoded)
        
        assert decoded == original_data
        
    def test_get_mime_type(self, attachment_handler):
        """Test MIME type detection."""
        assert attachment_handler.get_mime_type("test.txt") == "text/plain"
        assert attachment_handler.get_mime_type("test.json") == "application/json"
        assert attachment_handler.get_mime_type("unknown.xyz") == "application/octet-stream"


class TestProtocolBlock:
    """Test cases for ProtocolBlock dataclass."""
    
    def test_protocol_block_creation(self):
        """Test creating a ProtocolBlock."""
        block = ProtocolBlock(
            protocol=ProtocolType.SHELL,
            content="echo 'test'",
            attachments=["file.txt"],
            metadata={"key": "value"}
        )
        
        assert block.protocol == ProtocolType.SHELL
        assert block.content == "echo 'test'"
        assert block.attachments == ["file.txt"]
        assert block.metadata == {"key": "value"}
        
    def test_protocol_block_defaults(self):
        """Test ProtocolBlock with default values."""
        block = ProtocolBlock(
            protocol=ProtocolType.SHELL,
            content="echo 'test'"
        )
        
        assert block.attachments == []
        assert block.metadata == {}


class TestToonPact:
    """Test cases for ToonPact class."""
    
    @pytest.fixture
    def temp_markdown_file(self, tmp_path, sample_markdown):
        """Create a temporary markdown file."""
        file_path = tmp_path / "test.md"
        file_path.write_text(sample_markdown)
        return file_path
        
    @pytest.mark.asyncio
    async def test_load_document(self, temp_markdown_file):
        """Test loading a markdown document."""
        pact = ToonPact(temp_markdown_file)
        await pact.load()
        
        assert len(pact.blocks) == 4  # shell, mcp, rest, ws
        
    @pytest.mark.asyncio
    async def test_execute_shell_protocol(self, temp_markdown_file):
        """Test executing shell protocol blocks."""
        pact = ToonPact(temp_markdown_file)
        results = await pact.execute(protocol=ProtocolType.SHELL)
        
        assert len(results) == 1
        assert "shell_0" in results
        assert results["shell_0"]["protocol"] == "shell"
        assert results["shell_0"]["returncode"] == 0
