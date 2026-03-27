# Security Hardening Example

This example demonstrates how to secure your Propact implementation against common vulnerabilities.

## 🚨 Security Threats Demonstrated

1. **XSS Attacks**: JavaScript injection via links
2. **Base64 Bombs**: Large payloads causing DoS
3. **Script Injection**: HTML script tags
4. **SSRF**: Server-side request forgery
5. **Content Validation**: Schema-based validation

## 📁 Files

- `attack_samples.md` - Various attack vectors
- `secure_handler.py` - Secure implementation
- `run.sh` - Execute security demo
- `security_config.json` - Security configuration

## 🛡️ Security Features

```python
from propact.security import create_sanitizer
from propact.validation import ValidationPipeline
from propact.optimization import create_optimizer

# Create secure pipeline
sanitizer = create_sanitizer(strict=True)
optimizer = create_optimizer(enable_image_optimization=True)
pipeline = ValidationPipeline(sanitizer=sanitizer, optimizer=optimizer)

# Validate content
result = await pipeline.validate(markdown, strict=True)
```

## 🔍 What to Look For

- How dangerous links are blocked
- Base64 size limits in action
- Schema validation preventing malformed content
- Audit logging of security events

## ⚡ Quick Run

```bash
./run.sh
```

This will show how various attacks are mitigated.
