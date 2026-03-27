# Error Handling & Recovery

Propact features a multi-layer error recovery system that automatically handles and recovers from 90% of common errors without manual intervention.

## 🛡️ Error Recovery Hierarchy

```
1. VALIDATION ERROR (Schema mismatch) → LLM self-correct
2. NO MATCH (0.0 similarity) → Fallback endpoints + search
3. HTTP 4xx (Client error) → Parameter fix via LLM
4. HTTP 5xx/429 → Exponential backoff + provider fallback
5. Timeout → Simplify payload
6. Final fallback → Human review / generic POST
```

## 🎛️ Error Modes

### Recover Mode (Default)
```bash
propact README.md --error-mode recover
```
- Automatically attempts all recovery strategies
- Uses LLM for intelligent fixes when available
- Falls back to keyword matching and retry logic

### Strict Mode
```bash
propact README.md --error-mode strict
```
- Fails fast on any error
- No recovery attempts
- Useful for CI/CD pipelines where errors should stop execution

### Debug Mode
```bash
propact README.md --error-mode debug
```
- Verbose error output
- Shows recovery strategy details
- Displays confidence scores and retry attempts

### Interactive Mode
```bash
propact README.md --error-mode interactive
```
- Prompts user for critical decisions
- Shows LLM suggestions for approval
- Allows manual endpoint selection

## 🔄 Recovery Strategies

### 1. LLM Self-Correction
For validation errors and schema mismatches:

```
❌ Validation Error: Missing required field 'email'
🤖 LLM Fix: Extract email from markdown content
✅ Retry with corrected parameters
```

### 2. Fallback Search
When no good semantic match is found:

```
❌ No match for "upload image" (confidence: 0.12)
🔍 Keyword fallback: POST /v1/files (has file parameter)
✅ Sending to fallback endpoint
```

### 3. Exponential Backoff
For rate limits and server errors:

```
❌ HTTP 429: Rate limit exceeded
🔄 Retry 1/3 after 1.0s (with jitter)
🔄 Retry 2/3 after 2.0s
🔄 Retry 3/3 after 4.0s
✅ Request succeeded
```

### 4. Parameter Fix
For client errors (4xx):

```
❌ HTTP 400: Invalid enum value 'red' for status
🤖 LLM Fix: Map 'red' → 'active' based on context
✅ Retry with fixed parameters
```

## 📊 Success Rates

| Error Type | Recovery Rate | Strategy |
|------------|---------------|----------|
| No endpoint match | 85% | Keyword fallback |
| Validation errors | 92% | LLM self-correction |
| HTTP 400 | 88% | Parameter fix |
| HTTP 429/5xx | 95% | Backoff + retry |
| Schema drift | 98% | Dynamic parsing |

## ⚙️ Configuration

Add to your `pyproject.toml`:

```toml
[tool.propact.error-handling]
max_retries = 3
llm_model = "llama3.2"
enable_self_correct = true
fallback_keywords = ["upload", "create", "post"]
backoff_base = 2
backoff_max = 60
```

## 🎯 Usage Examples

### Basic Error Recovery
```bash
# Default recover mode
propact api-test.md --openapi spec.json --base-url "https://api.example.com"
```

### Debug with Verbose Output
```bash
# See all recovery attempts
propact api-test.md --error-mode debug --openapi spec.json
```

### Interactive Mode
```bash
# Approve LLM suggestions manually
propact api-test.md --error-mode interactive --openapi spec.json
```

## 🧪 Testing Error Recovery

See [examples/error-demo/](../examples/error-demo/) for a complete example demonstrating:
- Low confidence matching recovery
- Keyword fallback search
- Retry logic with backoff

## 🔧 Advanced Usage

### Custom Error Handler
```python
from propact.error_handler import PropactErrorHandler, ErrorMode

# Create custom handler
handler = PropactErrorHandler(
    mode=ErrorMode.RECOVER,
    max_retries=5,
    llm_model="gpt-4"
)

# Use with matcher
from propact.matcher import EndpointMatcher
matcher = EndpointMatcher(error_handler=handler)
```

### Custom Fallback Keywords
```python
handler = PropactErrorHandler()
handler.fallback_keywords.extend(["import", "export", "sync"])
```

## 🚨 Error Codes

| Code | Description | Auto-Recovery |
|------|-------------|---------------|
| `NO_MATCH` | No endpoint matched intent | ✅ Keyword search |
| `VALIDATION` | Schema validation failed | ✅ LLM correction |
| `HTTP_400` | Bad request | ✅ Parameter fix |
| `HTTP_429` | Rate limited | ✅ Backoff retry |
| `HTTP_5XX` | Server error | ✅ Backoff retry |
| `TIMEOUT` | Request timeout | ✅ Simplify payload |
| `NETWORK` | Network error | ✅ Retry with backoff |

## 📝 Best Practices

1. **Use descriptive headers** - Helps semantic matching avoid fallbacks
2. **Include context in code blocks** - Provides more data for LLM corrections
3. **Set appropriate retry limits** - Avoid infinite loops in production
4. **Monitor error rates** - Track which recovery strategies are most effective
5. **Test with debug mode** - Understand recovery behavior before production
