"""Security module for Markdown sanitization and validation."""

import re
import html
from typing import List, Set, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import logging

# Try to import bleach for HTML sanitization
try:
    import bleach
    HAS_BLEACH = True
except ImportError:
    HAS_BLEACH = False
    logging.warning("bleach not installed. HTML sanitization will be limited.")

# Try to import markdown-it-py for better parsing
try:
    import markdown_it
    from markdown_it import MarkdownIt
    HAS_MARKDOWN_IT = True
except ImportError:
    HAS_MARKDOWN_IT = False
    logging.warning("markdown-it-py not installed. Using basic regex-based sanitization.")


@dataclass
class SanitizationConfig:
    """Configuration for markdown sanitization."""
    allow_html_tags: bool = False
    allowed_tags: Set[str] = None
    allowed_attributes: Dict[str, Set[str]] = None
    allowed_protocols: Set[str] = None
    strict_mode: bool = False
    max_base64_size: int = 1024 * 1024  # 1MB default
    
    def __post_init__(self):
        if self.allowed_tags is None:
            self.allowed_tags = {'p', 'b', 'i', 'em', 'strong', 'code', 'pre', 'a', 'img', 'ul', 'ol', 'li', 'br', 'hr'}
        if self.allowed_attributes is None:
            self.allowed_attributes = {
                'a': {'href', 'title'},
                'img': {'src', 'alt', 'title', 'width', 'height'},
                '*': {'class'}
            }
        if self.allowed_protocols is None:
            self.allowed_protocols = {'http', 'https', 'mailto', 'ftp', 'tel'}


class MDSanitizer:
    """Markdown sanitizer for security protection."""
    
    def __init__(self, config: Optional[SanitizationConfig] = None):
        """Initialize the sanitizer with configuration.
        
        Args:
            config: Sanitization configuration. Uses default if None.
        """
        self.config = config or SanitizationConfig()
        self.logger = logging.getLogger(__name__)
        
        # Initialize markdown parser if available
        if HAS_MARKDOWN_IT:
            self.md = MarkdownIt("commonmark", {
                "html": self.config.allow_html_tags,
                "linkify": True,
                "typographer": True
            })
        
        # Pre-compile regex patterns for performance
        self._dangerous_protocols = [
            'javascript:', 'vbscript:', 'data:', 'file:', 
            'chrome:', 'chrome-extension:', 'callto:', 'sms:'
        ]
        self._protocol_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
        self._base64_pattern = re.compile(r'!\[([^\]]*)\]\(data:([^;]+);base64,([A-Za-z0-9+/=]+)\)')
        self._html_tag_pattern = re.compile(r'<[^>]+>')
        self._script_pattern = re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL)
        
    def sanitize(self, markdown: str, strict: Optional[bool] = None) -> str:
        """Sanitize markdown content.
        
        Args:
            markdown: Raw markdown content
            strict: Override strict mode setting
            
        Returns:
            Sanitized markdown content
        """
        if strict is None:
            strict = self.config.strict_mode
            
        sanitized = markdown
        
        # Remove script tags immediately
        sanitized = self._remove_scripts(sanitized)
        
        # Sanitize dangerous links
        sanitized = self._sanitize_links(sanitized)
        
        # Handle base64 images
        sanitized = self._sanitize_base64_images(sanitized)
        
        # Sanitize HTML tags if not allowed
        if not self.config.allow_html_tags:
            sanitized = self._sanitize_html(sanitized)
        
        # Additional strict mode checks
        if strict:
            sanitized = self._strict_sanitization(sanitized)
            
        return sanitized
    
    def _remove_scripts(self, content: str) -> str:
        """Remove all script tags and content."""
        return self._script_pattern.sub('[REMOVED SCRIPT]', content)
    
    def _sanitize_links(self, content: str) -> str:
        """Sanitize links to remove dangerous protocols."""
        def replace_link(match):
            text, url = match.groups()
            
            # Check for dangerous protocols
            for proto in self._dangerous_protocols:
                if url.lower().startswith(proto):
                    if proto in self.config.allowed_protocols:
                        return match.group(0)  # Keep if explicitly allowed
                    return f'[{text}](#BLOCKED-{proto.upper()}-LINK)'
            
            # Additional validation
            if 'javascript:' in url.lower() or 'vbscript:' in url.lower():
                return f'[{text}](#BLOCKED-DANGEROUS-LINK)'
                
            return match.group(0)
        
        return self._protocol_pattern.sub(replace_link, content)
    
    def _sanitize_base64_images(self, content: str) -> str:
        """Sanitize base64 images and check size limits."""
        def replace_base64(match):
            alt, mime_type, base64_data = match.groups()
            
            # Check size
            decoded_size = len(base64_data) * 3 // 4  # Approximate decoded size
            if decoded_size > self.config.max_base64_size:
                return f'![{alt}](#BLOCKED-TOO-LARGE-{decoded_size//1024}KB)'
            
            # Check for dangerous MIME types
            dangerous_mimes = {'text/html', 'application/javascript', 'text/javascript'}
            if mime_type.lower() in dangerous_mimes:
                return f'![{alt}](#BLOCKED-DANGEROUS-MIME-{mime_type})'
            
            return match.group(0)
        
        return self._base64_pattern.sub(replace_base64, content)
    
    def _sanitize_html(self, content: str) -> str:
        """Remove or escape HTML tags."""
        if HAS_BLEACH:
            # Convert markdown to HTML, sanitize, then back to markdown-like format
            # This is a simplified approach - in practice, you might want more sophisticated handling
            html_content = self.md.render(content) if HAS_MARKDOWN_IT else content
            sanitized_html = bleach.clean(
                html_content,
                tags=self.config.allowed_tags,
                attributes=self.config.allowed_attributes,
                strip=True
            )
            # For now, return the sanitized HTML as-is
            # In a full implementation, you'd convert back to markdown
            return sanitized_html
        else:
            # Basic HTML tag removal
            return self._html_tag_pattern.sub('', content)
    
    def _strict_sanitization(self, content: str) -> str:
        """Apply strict mode sanitization rules."""
        # Remove HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Block potentially dangerous markdown features
        content = re.sub(r'\!\[.*?\]\(javascript:.*?\)', '[BLOCKED]', content)
        content = re.sub(r'\[.*?\]\(data:.*?\)', '[BLOCKED]', content)
        
        # Limit URL length to prevent DoS
        def limit_url_length(match):
            text, url = match.groups()
            if len(url) > 2048:
                return f'[{text}](#URL-TOO-LONG)'
            return match.group(0)
        
        content = self._protocol_pattern.sub(limit_url_length, content)
        
        return content
    
    def audit(self, markdown: str) -> Dict[str, Any]:
        """Audit markdown content for security issues.
        
        Args:
            markdown: Markdown content to audit
            
        Returns:
            Dictionary with audit results
        """
        issues = []
        warnings = []
        
        # Check for dangerous links
        dangerous_links = self._protocol_pattern.findall(markdown)
        for _, url in dangerous_links:
            for proto in self._dangerous_protocols:
                if url.lower().startswith(proto) and proto not in self.config.allowed_protocols:
                    issues.append(f"Dangerous protocol detected: {proto}")
        
        # Check for scripts
        if self._script_pattern.search(markdown):
            issues.append("Script tags detected")
        
        # Check for large base64 images
        base64_images = self._base64_pattern.findall(markdown)
        for alt, mime_type, base64_data in base64_images:
            size = len(base64_data) * 3 // 4
            if size > self.config.max_base64_size:
                warnings.append(f"Large base64 image: {alt} ({size//1024}KB)")
        
        # Check for HTML tags if not allowed
        if not self.config.allow_html_tags:
            html_tags = self._html_tag_pattern.findall(markdown)
            if html_tags:
                warnings.append(f"HTML tags found: {len(html_tags)} tags")
        
        return {
            'issues': issues,
            'warnings': warnings,
            'dangerous_links': len([url for _, url in dangerous_links 
                                   if any(url.lower().startswith(p) for p in self._dangerous_protocols)]),
            'base64_images': len(base64_images),
            'has_scripts': bool(self._script_pattern.search(markdown)),
            'has_html': bool(self._html_tag_pattern.search(markdown))
        }


def create_sanitizer(strict: bool = False, allow_html: bool = False) -> MDSanitizer:
    """Create a sanitizer with common configurations.
    
    Args:
        strict: Enable strict mode
        allow_html: Allow HTML tags
        
    Returns:
        Configured MDSanitizer instance
    """
    config = SanitizationConfig(
        strict_mode=strict,
        allow_html_tags=allow_html,
        max_base64_size=512 * 1024 if strict else 1024 * 1024  # 512KB in strict mode
    )
    return MDSanitizer(config)


# Default sanitizer instance
default_sanitizer = create_sanitizer()
