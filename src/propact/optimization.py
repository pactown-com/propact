"""Payload optimization module for markdown content."""

import re
import base64
import hashlib
import mimetypes
from typing import Dict, List, Optional, Tuple, Union, BinaryIO
from pathlib import Path
from dataclasses import dataclass
from urllib.parse import urlparse
import logging

# Try to import compression libraries
try:
    import gzip
    import zlib
    HAS_COMPRESSION = True
except ImportError:
    HAS_COMPRESSION = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from PIL import Image
    import io
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


@dataclass
class OptimizationConfig:
    """Configuration for payload optimization."""
    enable_compression: bool = True
    enable_image_optimization: bool = True
    max_image_width: int = 1920
    max_image_height: int = 1080
    image_quality: int = 85
    enable_external_refs: bool = True
    external_storage_url: str = "https://storage.example.com"
    cache_dir: Path = None
    enable_chunking: bool = True
    chunk_size: int = 10 * 1024  # 10KB chunks
    
    def __post_init__(self):
        if self.cache_dir is None:
            self.cache_dir = Path("./cache/optimization")


class MediaRefManager:
    """Manages external media references."""
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.ref_cache: Dict[str, str] = {}
        
    def generate_ref(self, content: bytes, mime_type: str) -> str:
        """Generate a reference for media content.
        
        Args:
            content: Binary content
            mime_type: MIME type of the content
            
        Returns:
            Reference URL
        """
        # Generate hash for the content
        content_hash = hashlib.sha256(content).hexdigest()[:16]
        
        # Generate filename based on MIME type
        extension = mimetypes.guess_extension(mime_type) or '.bin'
        filename = f"{content_hash}{extension}"
        
        # Return external reference URL
        return f"{self.config.external_storage_url.rstrip('/')}/{filename}"
    
    def should_externalize(self, content_size: int, mime_type: str) -> bool:
        """Determine if content should be externalized.
        
        Args:
            content_size: Size of content in bytes
            mime_type: MIME type of the content
            
        Returns:
            True if content should be externalized
        """
        # Externalize if larger than 100KB or if it's an image
        return (content_size > 100 * 1024 or 
                mime_type.startswith('image/')) and self.config.enable_external_refs


class MDOptimizer:
    """Markdown payload optimizer."""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize optimizer with configuration.
        
        Args:
            config: Optimization configuration
        """
        self.config = config or OptimizationConfig()
        self.logger = logging.getLogger(__name__)
        self.ref_manager = MediaRefManager(self.config)
        
        # Ensure cache directory exists
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Pre-compile regex patterns
        self.base64_pattern = re.compile(
            r'!\[([^\]]*)\]\(data:([^;]+);base64,([A-Za-z0-9+/=]+)\)'
        )
        self.large_text_pattern = re.compile(
            r'```(\w+)?\n(.*?)\n```', re.DOTALL
        )
        
    def optimize(self, markdown: str) -> Tuple[str, Dict[str, int]]:
        """Optimize markdown content.
        
        Args:
            markdown: Raw markdown content
            
        Returns:
            Tuple of (optimized_markdown, optimization_stats)
        """
        stats = {
            'original_size': len(markdown),
            'base64_removed': 0,
            'images_compressed': 0,
            'chunks_created': 0,
            'bytes_saved': 0
        }
        
        optimized = markdown
        
        # Optimize base64 images
        optimized, img_stats = self._optimize_base64_images(optimized)
        stats.update(img_stats)
        
        # Optimize large code blocks
        if self.config.enable_chunking:
            optimized, chunk_stats = self._optimize_code_blocks(optimized)
            stats.update(chunk_stats)
        
        # Compress if enabled
        if self.config.enable_compression and HAS_COMPRESSION:
            optimized = self._add_compression_metadata(optimized)
        
        stats['final_size'] = len(optimized)
        stats['bytes_saved'] = stats['original_size'] - stats['final_size']
        
        return optimized, stats
    
    def _optimize_base64_images(self, content: str) -> Tuple[str, Dict[str, int]]:
        """Optimize base64 encoded images."""
        stats = {'base64_removed': 0, 'images_compressed': 0}
        
        def replace_image(match):
            alt_text, mime_type, base64_data = match.groups()
            
            try:
                # Decode base64
                image_data = base64.b64decode(base64_data)
                
                # Optimize image if PIL is available
                if self.config.enable_image_optimization and HAS_PIL and mime_type.startswith('image/'):
                    image_data = self._optimize_image(image_data, mime_type)
                    stats['images_compressed'] += 1
                
                # Check if should externalize
                if self.ref_manager.should_externalize(len(image_data), mime_type):
                    ref_url = self.ref_manager.generate_ref(image_data, mime_type)
                    stats['base64_removed'] += 1
                    return f'![{alt_text}]({ref_url})'
                
                # Re-encode with optimized data
                optimized_base64 = base64.b64encode(image_data).decode()
                return f'![{alt_text}](data:{mime_type};base64,{optimized_base64})'
                
            except Exception as e:
                self.logger.warning(f"Failed to optimize image: {e}")
                return match.group(0)
        
        return self.base64_pattern.sub(replace_image, content), stats
    
    def _optimize_image(self, image_data: bytes, mime_type: str) -> bytes:
        """Optimize image data."""
        if not HAS_PIL:
            return image_data
            
        try:
            # Open image
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize if necessary
            if (img.width > self.config.max_image_width or 
                img.height > self.config.max_image_height):
                img.thumbnail((self.config.max_image_width, self.config.max_image_height), 
                            Image.Resampling.LANCZOS)
            
            # Save with compression
            output = io.BytesIO()
            format_map = {
                'image/jpeg': 'JPEG',
                'image/png': 'PNG',
                'image/webp': 'WEBP'
            }
            img_format = format_map.get(mime_type, 'JPEG')
            
            if img_format == 'JPEG':
                img.save(output, format='JPEG', quality=self.config.image_quality, optimize=True)
            else:
                img.save(output, format=img_format, optimize=True)
            
            return output.getvalue()
            
        except Exception as e:
            self.logger.warning(f"Image optimization failed: {e}")
            return image_data
    
    def _optimize_code_blocks(self, content: str) -> Tuple[str, Dict[str, int]]:
        """Optimize large code blocks by chunking them."""
        stats = {'chunks_created': 0}
        
        def replace_block(match):
            lang, code = match.groups()
            
            # Check if block is large enough to chunk
            if len(code) < self.config.chunk_size:
                return match.group(0)
            
            # Split into chunks
            chunks = []
            for i in range(0, len(code), self.config.chunk_size):
                chunk = code[i:i + self.config.chunk_size]
                chunk_hash = hashlib.md5(chunk.encode()).hexdigest()[:8]
                chunk_path = f"./chunks/{lang}_{chunk_hash}.md"
                
                # Save chunk to cache
                chunk_file = self.config.cache_dir / "chunks" / f"{lang}_{chunk_hash}.md"
                chunk_file.parent.mkdir(parents=True, exist_ok=True)
                chunk_file.write_text(f"```{lang}\n{chunk}\n```")
                
                chunks.append(chunk_path)
                stats['chunks_created'] += 1
            
            # Replace with reference
            ref_text = f"Code split into {len(chunks)} chunks:\n"
            for i, chunk in enumerate(chunks, 1):
                ref_text += f"[Chunk {i}]({chunk})\n"
            
            return ref_text
        
        return self.large_text_pattern.sub(replace_block, content), stats
    
    def _add_compression_metadata(self, content: str) -> str:
        """Add compression metadata to markdown."""
        # Add frontmatter with compression info
        if HAS_COMPRESSION:
            compressed_size = len(gzip.compress(content.encode()))
            ratio = compressed_size / len(content)
            
            metadata = f"---\ncompression: gzip\ncompressed_size: {compressed_size}\ncompression_ratio: {ratio:.2f}\n---\n\n"
            return metadata + content
        
        return content
    
    def create_chunks(self, content: str, chunk_size: Optional[int] = None) -> List[str]:
        """Split content into chunks for parallel processing.
        
        Args:
            content: Content to chunk
            chunk_size: Size of each chunk in bytes
            
        Returns:
            List of content chunks
        """
        if chunk_size is None:
            chunk_size = self.config.chunk_size
            
        chunks = []
        
        # Split by lines to avoid breaking markdown structure
        lines = content.split('\n')
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line) + 1  # +1 for newline
            
            if current_size + line_size > chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size
        
        # Add final chunk
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    def get_optimization_report(self, original: str, optimized: str) -> Dict[str, Union[int, float, str]]:
        """Generate optimization report.
        
        Args:
            original: Original content
            optimized: Optimized content
            
        Returns:
            Optimization report
        """
        original_size = len(original)
        optimized_size = len(optimized)
        
        return {
            'original_size': original_size,
            'optimized_size': optimized_size,
            'bytes_saved': original_size - optimized_size,
            'compression_ratio': optimized_size / original_size if original_size > 0 else 0,
            'space_saved_percent': ((original_size - optimized_size) / original_size * 100) if original_size > 0 else 0
        }


def create_optimizer(enable_compression: bool = True, 
                    enable_image_optimization: bool = True,
                    chunk_size: int = 10 * 1024) -> MDOptimizer:
    """Create an optimizer with common configurations.
    
    Args:
        enable_compression: Enable compression
        enable_image_optimization: Enable image optimization
        chunk_size: Chunk size in bytes
        
    Returns:
        Configured MDOptimizer instance
    """
    config = OptimizationConfig(
        enable_compression=enable_compression,
        enable_image_optimization=enable_image_optimization,
        chunk_size=chunk_size
    )
    return MDOptimizer(config)


# Default optimizer instance
default_optimizer = create_optimizer()
