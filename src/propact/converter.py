"""Bidirectional format converter for Propact.

Handles conversion between markdown and various formats:
- JSON/YAML/XML ↔ Markdown codeblocks
- Binary data (images, audio, video) ↔ Base64 embeddings
- Protocol-specific payload preparation
"""

import base64
import json
import re
import xml.etree.ElementTree as ET
from typing import Dict, Any, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    import pypandoc
    HAS_PANDOC = True
except ImportError:
    HAS_PANDOC = False


class MediaType(Enum):
    """Supported media types for conversion."""
    JSON = "application/json"
    YAML = "text/yaml"
    XML = "text/xml"
    HTML = "text/html"
    TEXT = "text/plain"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_GIF = "image/gif"
    AUDIO_MP3 = "audio/mpeg"
    AUDIO_WAV = "audio/wav"
    VIDEO_MP4 = "video/mp4"
    VIDEO_WEBM = "video/webm"


@dataclass
class ExtractedContent:
    """Represents content extracted from markdown."""
    media: Dict[str, bytes] = None
    codeblocks: Dict[str, Any] = None
    plain_text: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.media is None:
            self.media = {}
        if self.codeblocks is None:
            self.codeblocks = {}
        if self.metadata is None:
            self.metadata = {}


class MDConverter:
    """Universal converter for markdown ↔ various formats."""
    
    # Regex patterns
    MEDIA_PATTERN = re.compile(r'!\[(.*?)\]\((data:(.+?);base64,(.+?)|(.+?))\)')
    CODEBLOCK_PATTERN = re.compile(r'```(\w+)?\s*\n(.*?)\n```', re.DOTALL)
    
    @staticmethod
    def response_to_markdown(response: Any, content_type: str = None, headers: Dict[str, str] = None) -> str:
        """Convert any response to markdown format.
        
        Args:
            response: The response data (bytes, str, dict, etc.)
            content_type: MIME type of the response
            headers: Response headers
            
        Returns:
            Markdown-formatted string
        """
        headers = headers or {}
        
        # Determine content type
        if not content_type:
            content_type = headers.get("content-type", "text/plain")
        
        # Handle different response types
        if isinstance(response, bytes):
            return MDConverter._binary_to_markdown(response, content_type)
        elif isinstance(response, (dict, list)):
            return MDConverter._dict_to_markdown(response, content_type)
        elif isinstance(response, str):
            return MDConverter._text_to_markdown(response, content_type)
        else:
            return f"```\n{str(response)}\n```"
    
    @staticmethod
    def _binary_to_markdown(data: bytes, content_type: str) -> str:
        """Convert binary data to markdown."""
        # Encode as base64
        b64_data = base64.b64encode(data).decode()
        
        # Determine media type and extension
        if "image" in content_type:
            ext = content_type.split("/")[-1] or "png"
            return f"![response_image.{ext}](data:{content_type};base64,{b64_data})"
        elif "audio" in content_type:
            ext = content_type.split("/")[-1] or "mp3"
            return f"![response_audio.{ext}](data:{content_type};base64,{b64_data})"
        elif "video" in content_type:
            ext = content_type.split("/")[-1] or "mp4"
            return f"![response_video.{ext}](data:{content_type};base64,{b64_data})"
        else:
            # Generic binary
            return f"```binary\n{b64_data}\n```"
    
    @staticmethod
    def _dict_to_markdown(data: Union[dict, list], content_type: str) -> str:
        """Convert dictionary/list to markdown."""
        if "json" in content_type:
            return f"```json\n{json.dumps(data, indent=2)}\n```"
        elif "yaml" in content_type and HAS_YAML:
            return f"```yaml\n{yaml.dump(data, default_flow_style=False)}\n```"
        elif "xml" in content_type:
            # Convert dict to XML (simplified)
            if isinstance(data, dict):
                root = ET.Element("response")
                for key, value in data.items():
                    child = ET.SubElement(root, key)
                    child.text = str(value)
                xml_str = ET.tostring(root, encoding='unicode')
                return f"```xml\n{xml_str}\n```"
        
        # Default to JSON
        return f"```json\n{json.dumps(data, indent=2)}\n```"
    
    @staticmethod
    def _text_to_markdown(text: str, content_type: str) -> str:
        """Convert text to markdown."""
        if "html" in content_type:
            if HAS_PANDOC:
                try:
                    md = pypandoc.convert_text(text, 'md', format='html')
                    return md
                except:
                    pass
            # Fallback: wrap in codeblock
            return f"```html\n{text}\n```"
        elif "xml" in content_type:
            return f"```xml\n{text}\n```"
        else:
            # Plain text
            return text
    
    @staticmethod
    def extract_from_markdown(md_content: str) -> ExtractedContent:
        """Extract all content from markdown.
        
        Args:
            md_content: Markdown content to parse
            
        Returns:
            ExtractedContent with media, codeblocks, and text
        """
        result = ExtractedContent()
        
        # Extract media (images, audio, video)
        for match in MDConverter.MEDIA_PATTERN.finditer(md_content):
            name, mime, b64_data, _, file_path = match.groups()
            
            if b64_data:
                # Embedded base64 data
                try:
                    data = base64.b64decode(b64_data)
                    result.media[name] = data
                    result.metadata[f"{name}_mime"] = mime
                except Exception as e:
                    print(f"Warning: Failed to decode base64 for {name}: {e}")
            elif file_path:
                # External file reference
                file_obj = Path(file_path)
                if file_obj.exists():
                    result.media[name] = file_obj.read_bytes()
                    result.metadata[f"{name}_path"] = file_path
                else:
                    print(f"Warning: File not found: {file_path}")
        
        # Extract codeblocks
        for lang, content in MDConverter.CODEBLOCK_PATTERN.findall(md_content):
            lang = lang or "text"
            content = content.strip()
            
            try:
                if lang.lower() in ["json", "jsonc"]:
                    result.codeblocks[lang] = json.loads(content)
                elif lang.lower() in ["yaml", "yml"] and HAS_YAML:
                    result.codeblocks[lang] = yaml.safe_load(content)
                elif lang.lower() == "xml":
                    result.codeblocks[lang] = content
                else:
                    result.codeblocks[lang] = content
            except (json.JSONDecodeError, yaml.YAMLError) as e:
                # Keep as raw text if parsing fails
                result.codeblocks[lang] = content
        
        # Extract plain text (remove media and codeblocks)
        plain_text = MDConverter.CODEBLOCK_PATTERN.sub("", md_content)
        plain_text = MDConverter.MEDIA_PATTERN.sub("", plain_text)
        result.plain_text = plain_text.strip()
        
        return result
    
    @staticmethod
    def prepare_payload(extracted: ExtractedContent, schema: Dict[str, Any] = None) -> Dict[str, Any]:
        """Prepare payload for different protocols based on schema.
        
        Args:
            extracted: Extracted content from markdown
            schema: Optional schema for payload structure
            
        Returns:
            Protocol-specific payload
        """
        schema = schema or {}
        
        # Default payload structure
        payload = {
            "text": extracted.plain_text,
            "data": extracted.codeblocks,
            "files": extracted.media
        }
        
        # Adapt based on schema
        if "openapi" in str(schema).lower():
            return MDConverter._prepare_openapi_payload(extracted, schema)
        elif "multipart" in str(schema).lower():
            return MDConverter._prepare_multipart_payload(extracted)
        elif "json" in str(schema).lower():
            return MDConverter._prepare_json_payload(extracted)
        elif "form" in str(schema).lower():
            return MDConverter._prepare_form_payload(extracted)
        
        return payload
    
    @staticmethod
    def _prepare_openapi_payload(extracted: ExtractedContent, schema: Dict) -> Dict[str, Any]:
        """Prepare payload for OpenAPI endpoints."""
        # Look for multipart/form-data in schema
        for path, path_item in schema.get("paths", {}).items():
            for method, operation in path_item.items():
                if method.lower() == "post" and "requestBody" in operation:
                    content = operation["requestBody"].get("content", {})
                    if "multipart/form-data" in content:
                        return {
                            "files": extracted.media,
                            "fields": {
                                "text": extracted.plain_text,
                                **extracted.codeblocks
                            }
                        }
        
        # Default to JSON
        return MDConverter._prepare_json_payload(extracted)
    
    @staticmethod
    def _prepare_multipart_payload(extracted: ExtractedContent) -> Dict[str, Any]:
        """Prepare multipart form data payload."""
        return {
            "files": extracted.media,
            "fields": {
                "text": extracted.plain_text,
                **{k: v if not isinstance(v, (dict, list)) else json.dumps(v) 
                   for k, v in extracted.codeblocks.items()}
            }
        }
    
    @staticmethod
    def _prepare_json_payload(extracted: ExtractedContent) -> Dict[str, Any]:
        """Prepare JSON payload."""
        return {
            "text": extracted.plain_text,
            "data": extracted.codeblocks
        }
    
    @staticmethod
    def _prepare_form_payload(extracted: ExtractedContent) -> Dict[str, Any]:
        """Prepare form-encoded payload."""
        data = {"text": extracted.plain_text}
        
        # Flatten codeblocks
        for key, value in extracted.codeblocks.items():
            if isinstance(value, (dict, list)):
                data[key] = json.dumps(value)
            else:
                data[key] = str(value)
        
        return {"data": data}
    
    @staticmethod
    def embed_media(file_path: Union[str, Path], alt_text: str = None) -> str:
        """Embed a media file as base64 in markdown format.
        
        Args:
            file_path: Path to media file
            alt_text: Alternative text for the media
            
        Returns:
            Markdown string with embedded media
        """
        file_path = Path(file_path)
        alt_text = alt_text or file_path.name
        
        if not file_path.exists():
            raise FileNotFoundError(f"Media file not found: {file_path}")
        
        # Read file and encode
        data = file_path.read_bytes()
        b64_data = base64.b64encode(data).decode()
        
        # Determine MIME type
        mime_type = MDConverter._get_mime_type(file_path)
        
        return f"![{alt_text}](data:{mime_type};base64,{b64_data})"
    
    @staticmethod
    def _get_mime_type(file_path: Path) -> str:
        """Get MIME type for a file."""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or "application/octet-stream"
    
    @staticmethod
    def create_codeblock(content: Any, language: str = "text") -> str:
        """Create a markdown codeblock with content.
        
        Args:
            content: Content to include in codeblock
            language: Language identifier for syntax highlighting
            
        Returns:
            Markdown codeblock string
        """
        if isinstance(content, (dict, list)):
            if language.lower() in ["json", "jsonc"]:
                content_str = json.dumps(content, indent=2)
            elif language.lower() in ["yaml", "yml"] and HAS_YAML:
                content_str = yaml.dump(content, default_flow_style=False)
            else:
                content_str = json.dumps(content, indent=2)
        else:
            content_str = str(content)
        
        return f"```{language}\n{content_str}\n```"
    
    @staticmethod
    def merge_markdown(*sections: str) -> str:
        """Merge multiple markdown sections with proper spacing.
        
        Args:
            *sections: Markdown sections to merge
            
        Returns:
            Combined markdown string
        """
        sections = [s.strip() for s in sections if s.strip()]
        return "\n\n".join(sections)
