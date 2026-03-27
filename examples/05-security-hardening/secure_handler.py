#!/usr/bin/env python3
"""Secure handler for processing markdown with security safeguards."""

import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from propact.security import create_sanitizer, MDSanitizer
from propact.validation import ValidationPipeline, SchemaRegistry
from propact.optimization import create_optimizer
from propact.parser import MarkdownParser, ProtocolType


class SecurityEventHandler:
    """Handles security events and logging."""
    
    def __init__(self):
        self.logger = logging.getLogger("security")
        self.events = []
        
    def handle_violation(self, violation_type: str, details: dict):
        """Handle a security violation."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": violation_type,
            "details": details
        }
        self.events.append(event)
        self.logger.warning(f"Security violation: {violation_type} - {details}")
        
        # In production, you might:
        # - Send to SIEM system
        # - Alert administrators
        # - Block the user/IP
        # - Create incident ticket
    
    def get_report(self) -> dict:
        """Get security event report."""
        return {
            "total_events": len(self.events),
            "events": self.events
        }


class SecureMarkdownHandler:
    """Secure handler for processing markdown content."""
    
    def __init__(self, strict_mode: bool = True):
        """Initialize secure handler.
        
        Args:
            strict_mode: Enable strict security validation
        """
        self.strict_mode = strict_mode
        self.security_handler = SecurityEventHandler()
        
        # Initialize security components
        self.sanitizer = create_sanitizer(
            strict=strict_mode,
            allow_html=False
        )
        
        self.optimizer = create_optimizer(
            enable_compression=True,
            enable_image_optimization=True,
            chunk_size=10 * 1024
        )
        
        # Create validation pipeline
        self.pipeline = ValidationPipeline(
            sanitizer=self.sanitizer,
            optimizer=self.optimizer
        )
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    async def process(self, markdown_content: str, source: str = "unknown") -> dict:
        """Process markdown content with security checks.
        
        Args:
            markdown_content: Raw markdown content
            source: Source identifier for logging
            
        Returns:
            Processing result with security info
        """
        result = {
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "security": {
                "blocked_items": [],
                "warnings": [],
                "optimizations": {}
            },
            "processed": False,
            "output": None
        }
        
        try:
            # Step 1: Audit content
            audit = self.sanitizer.audit(markdown_content)
            
            if audit["issues"]:
                for issue in audit["issues"]:
                    self.security_handler.handle_violation("SECURITY_ISSUE", {
                        "source": source,
                        "issue": issue
                    })
                    result["security"]["blocked_items"].append(issue)
            
            if audit["warnings"]:
                result["security"]["warnings"].extend(audit["warnings"])
            
            # Step 2: Sanitize content
            sanitized_content = self.sanitizer.sanitize(
                markdown_content, 
                strict=self.strict_mode
            )
            
            # Step 3: Optimize content
            optimized_content, opt_stats = self.optimizer.optimize(sanitized_content)
            result["security"]["optimizations"] = opt_stats
            
            # Step 4: Validate structure
            validation_result = await self.pipeline.validate(
                optimized_content,
                strict=self.strict_mode
            )
            
            if not validation_result.is_valid:
                for error in validation_result.errors:
                    self.security_handler.handle_violation("VALIDATION_ERROR", {
                        "source": source,
                        "error": error
                    })
                    result["security"]["blocked_items"].append(error)
                return result
            
            # Step 5: Parse protocol blocks
            parser = MarkdownParser()
            blocks = await parser.parse(optimized_content)
            
            # Step 6: Process blocks (simulation)
            processed_blocks = []
            for block in blocks:
                # Simulate processing
                processed_block = {
                    "protocol": block.protocol.value,
                    "content_length": len(block.content),
                    "attachments": len(block.attachments),
                    "metadata": block.metadata
                }
                processed_blocks.append(processed_block)
            
            result["processed"] = True
            result["output"] = {
                "blocks": processed_blocks,
                "optimized_content": optimized_content
            }
            
            self.logger.info(f"Successfully processed {len(blocks)} blocks from {source}")
            
        except Exception as e:
            self.logger.error(f"Processing failed for {source}: {e}")
            self.security_handler.handle_violation("PROCESSING_ERROR", {
                "source": source,
                "error": str(e)
            })
        
        return result
    
    def get_security_report(self) -> dict:
        """Get comprehensive security report."""
        return self.security_handler.get_report()


async def demo_security():
    """Demonstrate security features with attack samples."""
    print("🔒 Propact Security Hardening Demo\n")
    
    # Initialize secure handler
    handler = SecureMarkdownHandler(strict_mode=True)
    
    # Load attack samples
    attack_file = Path(__file__).parent / "attack_samples.md"
    if not attack_file.exists():
        print(f"❌ Attack samples file not found: {attack_file}")
        return
    
    attack_content = attack_file.read_text()
    
    print("📋 Processing attack samples...\n")
    
    # Process the malicious content
    result = await handler.process(attack_content, source="attack_samples.md")
    
    # Display results
    print("=" * 60)
    print("SECURITY REPORT")
    print("=" * 60)
    
    security = result["security"]
    
    print(f"\n🚫 Blocked Items: {len(security['blocked_items'])}")
    for item in security["blocked_items"]:
        print(f"   • {item}")
    
    print(f"\n⚠️  Warnings: {len(security['warnings'])}")
    for warning in security["warnings"]:
        print(f"   • {warning}")
    
    print(f"\n📊 Optimizations:")
    opt = security["optimizations"]
    if opt:
        print(f"   • Original size: {opt.get('original_size', 0):,} bytes")
        print(f"   • Final size: {opt.get('final_size', 0):,} bytes")
        print(f"   • Bytes saved: {opt.get('bytes_saved', 0):,}")
        print(f"   • Base64 removed: {opt.get('base64_removed', 0)}")
        print(f"   • Images compressed: {opt.get('images_compressed', 0)}")
    
    print(f"\n✅ Processed: {result['processed']}")
    
    if result["processed"] and result["output"]:
        blocks = result["output"]["blocks"]
        print(f"📦 Protocol blocks processed: {len(blocks)}")
        for block in blocks:
            print(f"   • {block['protocol']}: {block['content_length']} chars")
    
    # Get full security report
    print("\n" + "=" * 60)
    print("FULL SECURITY LOG")
    print("=" * 60)
    
    security_report = handler.get_security_report()
    for event in security_report["events"]:
        print(f"\n[{event['timestamp']}] {event['type']}")
        print(f"  Details: {event['details']}")
    
    print("\n✨ Demo completed!")


if __name__ == "__main__":
    asyncio.run(demo_security())
