"""Validation pipeline for markdown content with schema support."""

import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Union
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Try to import jsonschema for validation
try:
    import jsonschema
    from jsonschema import Draft7Validator, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    logging.warning("jsonschema not installed. Schema validation will be limited.")

# Try to import pydantic for type safety
try:
    from pydantic import BaseModel, ValidationError as PydanticValidationError
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    logging.warning("pydantic not installed. Type safety will be limited.")

from .parser import MarkdownParser, ProtocolBlock, ProtocolType
from .security import MDSanitizer
from .optimization import MDOptimizer


@dataclass
class ValidationResult:
    """Result of validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    schema_version: Optional[str] = None
    validation_hash: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SchemaInfo:
    """Information about a schema."""
    name: str
    version: str
    file_path: Path
    hash: str
    last_modified: datetime
    content: Dict[str, Any]


class SchemaRegistry:
    """Registry for managing API schemas."""
    
    def __init__(self, schema_dir: Optional[Path] = None):
        """Initialize schema registry.
        
        Args:
            schema_dir: Directory containing schema files
        """
        self.schema_dir = schema_dir or Path("./schemas")
        self.schemas: Dict[str, SchemaInfo] = {}
        self.logger = logging.getLogger(__name__)
        
        # Create schema directory if it doesn't exist
        self.schema_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing schemas
        self._load_schemas()
    
    def _load_schemas(self):
        """Load all schemas from the schema directory."""
        for schema_file in self.schema_dir.glob("*.json"):
            try:
                with open(schema_file, 'r') as f:
                    schema_content = json.load(f)
                
                # Extract name and version from filename
                # Format: {api}_{version}.json or {api}.json
                stem = schema_file.stem
                if '_' in stem:
                    name, version = stem.rsplit('_', 1)
                else:
                    name, version = stem, 'latest'
                
                # Calculate hash
                content_hash = hashlib.sha256(
                    json.dumps(schema_content, sort_keys=True).encode()
                ).hexdigest()
                
                schema_info = SchemaInfo(
                    name=name,
                    version=version,
                    file_path=schema_file,
                    hash=content_hash,
                    last_modified=datetime.fromtimestamp(schema_file.stat().st_mtime),
                    content=schema_content
                )
                
                key = f"{name}_{version}"
                self.schemas[key] = schema_info
                
            except Exception as e:
                self.logger.error(f"Failed to load schema {schema_file}: {e}")
    
    def get_schema(self, name: str, version: str = "latest") -> Optional[SchemaInfo]:
        """Get a schema by name and version.
        
        Args:
            name: Schema name (e.g., 'stripe')
            version: Schema version (e.g., '2026-01-01')
            
        Returns:
            SchemaInfo if found
        """
        key = f"{name}_{version}"
        return self.schemas.get(key)
    
    def register_schema(self, name: str, version: str, schema: Dict[str, Any]) -> SchemaInfo:
        """Register a new schema.
        
        Args:
            name: Schema name
            version: Schema version
            schema: Schema content
            
        Returns:
            Registered SchemaInfo
        """
        # Save to file
        filename = f"{name}_{version}.json" if version != "latest" else f"{name}.json"
        file_path = self.schema_dir / filename
        
        with open(file_path, 'w') as f:
            json.dump(schema, f, indent=2)
        
        # Create schema info
        content_hash = hashlib.sha256(
            json.dumps(schema, sort_keys=True).encode()
        ).hexdigest()
        
        schema_info = SchemaInfo(
            name=name,
            version=version,
            file_path=file_path,
            hash=content_hash,
            last_modified=datetime.now(),
            content=schema
        )
        
        # Register in memory
        key = f"{name}_{version}"
        self.schemas[key] = schema_info
        
        return schema_info
    
    def detect_drift(self, name: str, version: str, old_hash: str) -> bool:
        """Detect if schema has drifted.
        
        Args:
            name: Schema name
            version: Schema version
            old_hash: Previously known hash
            
        Returns:
            True if schema has changed
        """
        schema = self.get_schema(name, version)
        if not schema:
            return True
        
        return schema.hash != old_hash


class ValidationPipeline:
    """Pipeline for validating markdown content."""
    
    def __init__(self, 
                 schema_registry: Optional[SchemaRegistry] = None,
                 sanitizer: Optional[MDSanitizer] = None,
                 optimizer: Optional[MDOptimizer] = None):
        """Initialize validation pipeline.
        
        Args:
            schema_registry: Schema registry instance
            sanitizer: Security sanitizer
            optimizer: Content optimizer
        """
        self.schema_registry = schema_registry or SchemaRegistry()
        self.sanitizer = sanitizer
        self.optimizer = optimizer
        self.parser = MarkdownParser()
        self.logger = logging.getLogger(__name__)
        
        # Validation cache
        self._validation_cache: Dict[str, ValidationResult] = {}
    
    async def validate(self, 
                      markdown: str, 
                      schema_name: Optional[str] = None,
                      schema_version: str = "latest",
                      strict: bool = False) -> ValidationResult:
        """Validate markdown content.
        
        Args:
            markdown: Markdown content to validate
            schema_name: Name of schema to validate against
            schema_version: Version of schema
            strict: Enable strict validation
            
        Returns:
            ValidationResult
        """
        # Generate content hash for caching
        content_hash = hashlib.sha256(markdown.encode()).hexdigest()
        
        # Check cache
        cache_key = f"{content_hash}_{schema_name}_{schema_version}_{strict}"
        if cache_key in self._validation_cache:
            return self._validation_cache[cache_key]
        
        result = ValidationResult(
            is_valid=True,
            validation_hash=content_hash,
            schema_version=f"{schema_name}_{schema_version}" if schema_name else None
        )
        
        try:
            # Step 1: Security sanitization
            if self.sanitizer:
                audit_result = self.sanitizer.audit(markdown)
                if audit_result['issues']:
                    result.errors.extend(audit_result['issues'])
                    result.is_valid = False
                
                if audit_result['warnings']:
                    result.warnings.extend(audit_result['warnings'])
                
                # Sanitize content
                markdown = self.sanitizer.sanitize(markdown, strict)
            
            # Step 2: Parse protocol blocks
            blocks = await self.parser.parse(markdown)
            
            if not blocks:
                result.warnings.append("No protocol blocks found in markdown")
            
            # Step 3: Validate against schema if specified
            if schema_name and HAS_JSONSCHEMA:
                schema = self.schema_registry.get_schema(schema_name, schema_version)
                if schema:
                    validation_errors = await self._validate_against_schema(blocks, schema.content)
                    if validation_errors:
                        result.errors.extend(validation_errors)
                        result.is_valid = False
                else:
                    result.warnings.append(f"Schema {schema_name}_{schema_version} not found")
            
            # Step 4: Type safety validation
            if HAS_PYDANTIC:
                type_errors = await self._validate_types(blocks)
                if type_errors:
                    result.errors.extend(type_errors)
                    result.is_valid = False
            
            # Step 5: Optimization check
            if self.optimizer:
                optimized, stats = self.optimizer.optimize(markdown)
                if stats['bytes_saved'] > 0:
                    result.warnings.append(
                        f"Content could be optimized: {stats['bytes_saved']} bytes could be saved"
                    )
            
        except Exception as e:
            result.is_valid = False
            result.errors.append(f"Validation failed: {str(e)}")
            self.logger.error(f"Validation error: {e}")
        
        # Cache result
        self._validation_cache[cache_key] = result
        
        return result
    
    async def _validate_against_schema(self, 
                                     blocks: List[ProtocolBlock], 
                                     schema: Dict[str, Any]) -> List[str]:
        """Validate protocol blocks against JSON schema.
        
        Args:
            blocks: Protocol blocks to validate
            schema: JSON schema to validate against
            
        Returns:
            List of validation errors
        """
        errors = []
        
        for block in blocks:
            try:
                # Convert block to dict for validation
                block_dict = {
                    'protocol': block.protocol.value,
                    'content': block.content,
                    'attachments': block.attachments,
                    'metadata': block.metadata
                }
                
                # Validate against schema
                jsonschema.validate(block_dict, schema)
                
            except ValidationError as e:
                errors.append(f"Block validation error: {e.message}")
            except Exception as e:
                errors.append(f"Schema validation failed: {str(e)}")
        
        return errors
    
    async def _validate_types(self, blocks: List[ProtocolBlock]) -> List[str]:
        """Validate types using Pydantic models.
        
        Args:
            blocks: Protocol blocks to validate
            
        Returns:
            List of type validation errors
        """
        if not HAS_PYDANTIC:
            return []
        
        errors = []
        
        # Define Pydantic models for type validation
        class ProtocolBlockModel(BaseModel):
            protocol: str
            content: str
            attachments: List[str]
            metadata: Dict[str, Any]
        
        for block in blocks:
            try:
                ProtocolBlockModel(
                    protocol=block.protocol.value,
                    content=block.content,
                    attachments=block.attachments,
                    metadata=block.metadata
                )
            except PydanticValidationError as e:
                errors.append(f"Type validation error: {e}")
        
        return errors
    
    def create_schema_pin(self, markdown: str, schema_name: str, schema_version: str) -> str:
        """Create a pinned markdown with schema version.
        
        Args:
            markdown: Original markdown
            schema_name: Schema name
            schema_version: Schema version
            
        Returns:
            Markdown with schema pin
        """
        # Add frontmatter with schema pin
        frontmatter = f"""---
schema: {schema_name}
schema_version: {schema_version}
pinned_at: {datetime.now().isoformat()}
---

"""
        
        return frontmatter + markdown
    
    def detect_schema_drift(self, markdown: str) -> Dict[str, bool]:
        """Detect schema drift in markdown content.
        
        Args:
            markdown: Markdown content with schema pins
            
        Returns:
            Dictionary of schema drift status
        """
        drift_status = {}
        
        # Extract schema pins from frontmatter
        if markdown.startswith('---\n'):
            try:
                end_idx = markdown.find('\n---\n', 4)
                if end_idx > 0:
                    frontmatter = markdown[4:end_idx]
                    for line in frontmatter.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            if key.strip() == 'schema':
                                schema_name = value.strip()
                            elif key.strip() == 'schema_version':
                                schema_version = value.strip()
                                # Check for drift
                                old_hash = hashlib.sha256(markdown.encode()).hexdigest()
                                has_drift = self.schema_registry.detect_drift(
                                    schema_name, schema_version, old_hash
                                )
                                drift_status[f"{schema_name}_{schema_version}"] = has_drift
            except Exception as e:
                self.logger.error(f"Failed to parse frontmatter: {e}")
        
        return drift_status


# Create default validation pipeline
default_pipeline = ValidationPipeline()
