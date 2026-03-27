# GitHub Gist Creation

This example demonstrates creating multi-file GitHub Gists using propact.

## Content

```python path=main.py
print("Hello from Propact!")
print("Universal markdown transport for all APIs")
```

```yaml path=config.yaml
propact:
  version: 0.1.0
  description: Universal markdown transport
features:
  - file uploads
  - schema-aware parsing
  - multi-protocol support
```

```json
{
  "description": "Propact demo gist - Universal MD transport",
  "public": true,
  "files": {
    "main.py": {
      "content": "print(\"Hello from Propact!\")\nprint(\"Universal markdown transport for all APIs\")"
    },
    "config.yaml": {
      "content": "propact:\n  version: 0.1.0\n  description: Universal markdown transport\nfeatures:\n  - file uploads\n  - schema-aware parsing\n  - multi-protocol support"
    },
    "README.md": {
      "content": "# Propact Demo\n\nThis gist demonstrates propact's universal markdown transport capabilities."
    }
  }
}
```

## Expected Output

The response will include:
- Gist URL
- HTML URL for viewing
- Files information and IDs

## Run Command

```bash
propact README.md \
  --endpoint "https://api.github.com/gists" \
  --header "Authorization: token $GITHUB_TOKEN"
```

## Environment Variables

```bash
GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>
```

## Requirements

- GitHub personal access token with `gist` scope
- Token created at https://github.com/settings/tokens
