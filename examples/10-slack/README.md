# Slack File Upload with Semantic Matching

This example demonstrates uploading files and sending messages to Slack using propact with semantic endpoint matching.

## Content

![screenshot.png](screenshot.png)

Send notification to Slack channel with automated screenshot.

## Run with Semantic Matching

```bash
# Using semantic matching with OpenAPI spec
propact README.md --openapi slack-openapi.json --base-url "https://slack.com/api" --header "Authorization: Bearer $SLACK_TOKEN"

# With error recovery
propact README.md --openapi slack-openapi.json --base-url "https://slack.com/api" --error-mode recover
```

## Traditional Method

```bash
# Direct endpoint specification
propact README.md \
  --endpoint "https://slack.com/api/files.upload" \
  --header "Authorization: Bearer $SLACK_TOKEN"
```

## Semantic Matching Output

```
🧠 Top 3 semantic matches:
  1. POST /files.upload (score: 0.892)
  2. POST /chat.postMessage (score: 0.743)
  3. POST /files.share (score: 0.621)

✓ Selected: POST /files.upload
```

## Environment Variables

```bash
SLACK_TOKEN=<YOUR_SLACK_BOT_TOKEN>
```

## Requirements

- Slack workspace with bot app created
- Bot token with `files:write` scope
- Image file (screenshot.png) in the same directory
